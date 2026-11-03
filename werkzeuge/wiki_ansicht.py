# -*- coding: utf-8 -*-
"""Eden wiki viewer (Duc 26.10.2026: "ein Link statt zwanzig").

Reads the Markdown in docs/ live and renders it in the browser - no copy, nothing goes stale, no installs.
The sidebar is built from the folder structure, so a new page shows up by itself. Read-only: it never writes a file.

    python werkzeuge\\wiki_ansicht.py [--port 8310]      ->  http://127.0.0.1:8310/
"""
import json, os, sys, urllib.parse
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(EDEN, "docs")
SKIP = {"abnahme", "effekt-auswahl", "ui_bilder", "auszuege", "__pycache__"}       # image/tool folders, not reading matter
# sidebar groups: (title, folder relative to docs, recursive); the rest of docs/*.md lands in "More docs"
GROUPS = [("Wiki", "wiki", True), ("Register & Brain Trust", "brain_trust", False), ("More docs", "", False),
          ("Archive", "archiv", True), ("Brain Trust archive", "brain_trust/archiv", True)]
EXTRA = [{"titel": "Combat guide (in game)", "pfad": "@kampf"}]


def _title(path):
    try:
        with open(path, encoding="utf-8-sig") as f:
            for line in f:
                if line.startswith("# "):
                    return line[2:].strip()
    except OSError:
        pass
    return os.path.splitext(os.path.basename(path))[0]


def tree():
    groups = []
    for title, rel, deep in GROUPS:
        base = os.path.join(DOCS, rel)
        if not os.path.isdir(base):
            continue
        pages = []
        for root, dirs, files in os.walk(base):
            dirs[:] = sorted(d for d in dirs if d not in SKIP)
            for f in sorted(files):
                if f.lower().endswith(".md"):
                    full = os.path.join(root, f)
                    r = os.path.relpath(full, DOCS).replace("\\", "/")
                    sub = os.path.relpath(root, base).replace("\\", "/")
                    pages.append({"pfad": r, "titel": _title(full), "ordner": "" if sub == "." else sub,
                                  "datei": f, "geaendert": int(os.path.getmtime(full))})
            if not deep:
                break
        if title == "Wiki":
            pages = EXTRA + pages
        if pages:
            groups.append({"titel": title, "seiten": pages})
    return groups


def _safe(rel):
    full = os.path.normpath(os.path.join(DOCS, rel))
    return full if full.startswith(DOCS + os.sep) and full.lower().endswith(".md") and os.path.isfile(full) else None


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code, body, typ):
        b = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", typ)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        if u.path == "/":
            return self.send(200, open(os.path.join(EDEN, "werkzeuge", "wiki_ansicht.html"), encoding="utf-8").read(),
                             "text/html; charset=utf-8")
        if u.path == "/api/baum":
            return self.send(200, json.dumps(tree(), ensure_ascii=False), "application/json; charset=utf-8")
        if u.path == "/api/seite":
            full = _safe((q.get("p") or [""])[0])
            if not full:
                return self.send(404, "not found", "text/plain; charset=utf-8")
            return self.send(200, open(full, encoding="utf-8-sig").read(), "text/plain; charset=utf-8")
        if u.path == "/api/alle":                     # for the search: every page's text in one go
            out = {p["pfad"]: open(_safe(p["pfad"]), encoding="utf-8-sig").read()
                   for g in tree() for p in g["seiten"] if not p["pfad"].startswith("@")}
            return self.send(200, json.dumps(out, ensure_ascii=False), "application/json; charset=utf-8")
        if u.path == "/kampf":
            return self.send(200, open(os.path.join(EDEN, "client", "wiki", "kampf.html"), encoding="utf-8").read(),
                             "text/html; charset=utf-8")
        return self.send(404, "not found", "text/plain; charset=utf-8")


def main():
    port = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else 8310
    print("Eden wiki: http://127.0.0.1:%d/" % port)
    ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()


if __name__ == "__main__":
    main()
