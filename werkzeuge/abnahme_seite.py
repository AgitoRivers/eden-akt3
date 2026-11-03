# -*- coding: utf-8 -*-
r"""Approval page for generated images (Duc 22.10.2026: "always build an HTML page where I can sign off").

Takes a small JSON spec and writes one self-contained HTML page next to it (images are linked as file:/// URLs, so
nothing is copied). Duc marks every image OK / Neu with an optional note; the decisions live in the page's
localStorage and can be copied as text ("Ergebnis kopieren") or read by Claude from the browser pane.

Spec (JSON):
    {"id": "kampf_nachholen_test", "titel": "...", "hinweis": "...",
     "items": [{"id": "RatAlpha", "titel": "Ratte (Alpha)", "bild": "X:\\...\\outfit_check.png",
                "soll": "what the image should show", "vergleich": "X:\\...\\idle.png" (optional),
                "vergleich_titel": "Grundgegner" (optional)}]}

    abnahme_seite.py spec.json [ziel.html]
"""
import html, json, os, sys, time
from urllib.request import pathname2url


def file_url(path):
    return "file:" + pathname2url(os.path.abspath(path))


def build(spec, served=False, verdicts=None):
    """served=True: images come from the little server (/bild/<n>, /vergleich/<n>) and decisions are saved to disk."""
    items = []
    for n, it in enumerate(spec["items"]):
        stamp = time.strftime("%d.%m. %H:%M", time.localtime(os.path.getmtime(it["bild"]))) \
            if os.path.isfile(it["bild"]) else "fehlt"
        has_b = os.path.isfile(it["bild"])
        has_v = bool(it.get("vergleich")) and os.path.isfile(it["vergleich"])
        items.append({"id": it["id"], "titel": it.get("titel", it["id"]), "soll": it.get("soll", ""),
                      "bild": ("bild/%d?t=%d" % (n, os.path.getmtime(it["bild"])) if served else file_url(it["bild"]))
                      if has_b else "", "stand": stamp,
                      "vergleich": ("vergleich/%d" % n if served else file_url(it["vergleich"])) if has_v else "",
                      "vergleich_titel": it.get("vergleich_titel", "Vergleich")})
    data = json.dumps({"id": spec["id"], "titel": spec["titel"], "items": items, "server": served,
                       "urteile": verdicts or {}}, ensure_ascii=False)
    return PAGE.replace("__TITEL__", html.escape(spec["titel"])) \
               .replace("__HINWEIS__", html.escape(spec.get("hinweis", ""))) \
               .replace("__DATA__", data.replace("</", "<\\/"))


PAGE = r"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITEL__</title>
<style>
:root{--bg:#16130f;--card:#211d17;--line:#3a3328;--text:#efe6d6;--mut:#a89c88;--beige:#d9c39a;--ok:#5fae6e;--neu:#d0644f}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.45 system-ui,Segoe UI,sans-serif}
header{position:sticky;top:0;z-index:5;background:#16130fee;backdrop-filter:blur(6px);border-bottom:1px solid var(--line);
 padding:12px 16px;display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center}
h1{font-size:18px;margin:0;color:var(--beige);font-weight:600}
.zahl{color:var(--mut)}.zahl b{color:var(--text)}
.sp{flex:1}
button{font:inherit;border:1px solid var(--line);background:#2b251d;color:var(--text);border-radius:8px;padding:6px 12px;cursor:pointer}
button:hover{border-color:var(--beige)}
.hinweis{color:var(--mut);padding:10px 16px 0;max-width:1100px}
.filter button.an{background:var(--beige);color:#16130f;border-color:var(--beige)}
main{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,420px),1fr));gap:16px;padding:16px}
.k{background:var(--card);border:2px solid var(--line);border-radius:12px;overflow:hidden;display:flex;flex-direction:column}
.k.ok{border-color:var(--ok)}.k.neu{border-color:var(--neu)}
.bilder{display:flex;gap:2px;background:#000}
.bilder figure{margin:0;flex:1;position:relative;min-width:0}
.bilder figure.v{flex:0 0 45%}
.bilder img{width:100%;height:300px;object-fit:contain;display:block;cursor:zoom-in;background:#8f897e}   /* Grau: freigestellte Sprites (auch dunkle) bleiben sichtbar */
.bilder .leer{height:300px;display:flex;align-items:center;justify-content:center;background:#0c0a08;color:var(--mut);
 font-size:14px;letter-spacing:.04em;border:1px dashed var(--line)}
.bilder figcaption{position:absolute;left:6px;top:6px;font-size:12px;background:#000a;padding:1px 6px;border-radius:4px;color:var(--mut)}
.inh{padding:10px 12px;display:flex;flex-direction:column;gap:8px}
.kopf{display:flex;gap:8px;align-items:baseline}.kopf b{font-size:16px}.kopf span{color:var(--mut);font-size:12px;margin-left:auto}
.soll{color:var(--mut);font-size:13px}
.knoepfe{display:flex;gap:8px}
.knoepfe button{flex:1;padding:8px}
.k.ok .b-ok{background:var(--ok);border-color:var(--ok);color:#0d1a10}
.k.neu .b-neu{background:var(--neu);border-color:var(--neu);color:#1a0d0a}
textarea{font:inherit;font-size:13px;width:100%;min-height:38px;resize:vertical;background:#16130f;color:var(--text);
 border:1px solid var(--line);border-radius:8px;padding:6px 8px}
#gross{position:fixed;inset:0;background:#000e;display:none;align-items:center;justify-content:center;z-index:9;cursor:zoom-out}
#gross img{max-width:96vw;max-height:94vh}
#kopiert{color:var(--ok);display:none}
</style></head><body>
<header><h1>__TITEL__</h1>
 <span class="zahl"><b id="n-ok">0</b> OK · <b id="n-neu">0</b> neu · <b id="n-offen">0</b> offen</span>
 <span class="filter"><button data-f="alle" class="an">Alle</button> <button data-f="offen">Offen</button> <button data-f="neu">Neu</button></span>
 <span class="sp"></span>
 <button id="alle-ok">Rest OK</button>
 <button id="kopieren">Ergebnis kopieren</button><span id="kopiert">kopiert</span>
</header>
<div class="hinweis">__HINWEIS__</div>
<main id="liste"></main>
<div id="gross"><img alt=""></div>
<script>
const D = __DATA__;
const KEY = "abnahme:" + D.id;
let S = D.urteile || {};
if (!D.server) { try { S = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { S = {}; } }
let timer = null;
const save = () => {
  try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {}
  if (D.server) { clearTimeout(timer); timer = setTimeout(() => fetch("urteil", {method: "POST", body: JSON.stringify(S)}), 300); }
  zaehlen();
};
let filter = "alle";
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

function karte(it) {
  const st = S[it.id] || {};
  const el = document.createElement("section");
  el.className = "k " + (st.urteil || "");
  el.dataset.id = it.id;
  el.innerHTML =
    '<div class="bilder"><figure>' + (it.bild ? '<img loading="lazy" src="' + it.bild + '" alt="">'
      : '<div class="leer">noch kein Bild</div>') + '<figcaption>neu</figcaption></figure>' +
    (it.vergleich ? '<figure class="v"><img loading="lazy" src="' + it.vergleich + '" alt=""><figcaption>' + esc(it.vergleich_titel) + '</figcaption></figure>' : '') +
    '</div><div class="inh"><div class="kopf"><b>' + esc(it.titel) + '</b><span>' + esc(it.stand) + '</span></div>' +
    (it.soll ? '<div class="soll">' + esc(it.soll) + '</div>' : '') +
    '<div class="knoepfe"><button class="b-ok">✓ OK</button><button class="b-neu">✗ Neu</button></div>' +
    '<textarea placeholder="Notiz (was soll anders werden?)">' + esc(st.notiz || "") + '</textarea></div>';
  el.querySelector(".b-ok").onclick = () => setze(it.id, "ok");
  el.querySelector(".b-neu").onclick = () => setze(it.id, "neu");
  el.querySelector("textarea").oninput = e => { (S[it.id] = S[it.id] || {}).notiz = e.target.value; save(); };
  el.querySelectorAll("img").forEach(i => i.onclick = () => { gross.querySelector("img").src = i.src; gross.style.display = "flex"; });
  return el;
}
function setze(id, urteil) {
  const st = S[id] = S[id] || {};
  st.urteil = st.urteil === urteil ? "" : urteil;
  document.querySelector('[data-id="' + id + '"]').className = "k " + st.urteil;
  save(); zeigen();
}
function zaehlen() {
  const u = D.items.map(it => (S[it.id] || {}).urteil || "");
  document.getElementById("n-ok").textContent = u.filter(x => x === "ok").length;
  document.getElementById("n-neu").textContent = u.filter(x => x === "neu").length;
  document.getElementById("n-offen").textContent = u.filter(x => !x).length;
}
function zeigen() {
  document.querySelectorAll(".k").forEach(el => {
    const u = (S[el.dataset.id] || {}).urteil || "";
    el.style.display = filter === "alle" || (filter === "offen" ? !u : u === filter) ? "" : "none";
  });
}
function ergebnis() {
  const z = ["Abnahme " + D.titel + ":"];
  for (const it of D.items) {
    const st = S[it.id] || {};
    z.push("- " + it.id + ": " + (st.urteil === "ok" ? "OK" : st.urteil === "neu" ? "NEU" : "offen") + (st.notiz ? " – " + st.notiz.trim() : ""));
  }
  return z.join("\n");
}
window.abnahme = () => ({id: D.id, urteile: S, text: ergebnis()});   // read by Claude from the browser pane
const liste = document.getElementById("liste"), gross = document.getElementById("gross");
D.items.forEach(it => liste.appendChild(karte(it)));
gross.onclick = () => gross.style.display = "none";
document.querySelectorAll(".filter button").forEach(b => b.onclick = () => {
  filter = b.dataset.f; document.querySelectorAll(".filter button").forEach(x => x.classList.toggle("an", x === b)); zeigen();
});
document.getElementById("alle-ok").onclick = () => {
  D.items.forEach(it => { const st = S[it.id] = S[it.id] || {}; if (!st.urteil) st.urteil = "ok"; });
  document.querySelectorAll(".k").forEach(el => el.className = "k " + (S[el.dataset.id].urteil || ""));
  save(); zeigen();
};
document.getElementById("kopieren").onclick = async () => {
  try { await navigator.clipboard.writeText(ergebnis()); } catch (e) { prompt("Ergebnis:", ergebnis()); return; }
  const k = document.getElementById("kopiert"); k.style.display = "inline"; setTimeout(() => k.style.display = "none", 1500);
};
zaehlen();
</script></body></html>
"""


def serve(spec_path, port):
    """Serve the page; decisions go to <spec>_urteil.json (read by Claude), the spec is re-read on every page load."""
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    verdict_path = os.path.splitext(spec_path)[0] + "_urteil.json"

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def send(self, code, body, ctype):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            spec = json.load(open(spec_path, encoding="utf-8"))
            parts = self.path.split("?")[0].strip("/").split("/")
            if parts == [""]:
                verdicts = json.load(open(verdict_path, encoding="utf-8")) if os.path.isfile(verdict_path) else {}
                page = build(spec, served=True, verdicts=verdicts)
                return self.send(200, page.encode("utf-8"), "text/html; charset=utf-8")
            if len(parts) == 2 and parts[0] in ("bild", "vergleich") and parts[1].isdigit() \
                    and int(parts[1]) < len(spec["items"]):
                path = spec["items"][int(parts[1])].get(parts[0])
                if path and os.path.isfile(path):
                    ext = os.path.splitext(path)[1].lower().lstrip(".")
                    return self.send(200, open(path, "rb").read(), "image/" + ("jpeg" if ext == "jpg" else ext))
            self.send(404, b"not found", "text/plain")

        def do_POST(self):
            if self.path.strip("/") != "urteil":
                return self.send(404, b"not found", "text/plain")
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            with open(verdict_path, "w", encoding="utf-8") as f:
                json.dump(body, f, ensure_ascii=False, indent=1)
            self.send(200, b"ok", "text/plain")

    print("Abnahme-Seite: http://127.0.0.1:%d  (Urteile -> %s)" % (port, verdict_path), flush=True)
    ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()


def main():
    if sys.argv[1] == "--serve":
        return serve(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 8340)
    spec_path = sys.argv[1]
    spec = json.load(open(spec_path, encoding="utf-8"))
    target = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(spec_path)[0] + ".html"
    with open(target, "w", encoding="utf-8") as f:
        f.write(build(spec))
    print("Abnahme-Seite: %s (%d Bilder)" % (target, len(spec["items"])))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
