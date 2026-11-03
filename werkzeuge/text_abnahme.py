# -*- coding: utf-8 -*-
r"""Approval page for rewritten game texts (Duc 25.10.2026: English rewrite, "show me old | new before you build").

Takes a JSON spec and serves one page where Duc marks every text OK / Change, with an optional note. Decisions are
saved next to the spec as <spec>_urteil.json (Claude reads them back), and can be copied as text.

Spec (JSON):
    {"id": "pilot_tag0_hafen", "titel": "...", "hinweis": "...",
     "gruppen": [{"titel": "Tag 0 · Limousine", "items": [
         {"key": "t0_limousine#z1", "wer": "toto", "gefuehl": "amusement", "feld": "Rede",
          "alt": "old text", "neu": "new text", "vertont": true, "notiz": "why (optional)",
          "audio_alt": "C:\\path\\old.wav", "audio_neu": "C:\\path\\new.wav"}]}]}     (audio optional: shows a player)

    text_abnahme.py --serve spec.json [port]      (default port 8343)
"""
import html, json, os, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def urteil_pfad(spec_pfad):
    return os.path.splitext(spec_pfad)[0] + "_urteil.json"


def lesen(pfad, leer):
    try:
        return json.load(open(pfad, encoding="utf-8"))
    except (OSError, ValueError):
        return leer


def seite(spec, urteile):
    data = json.dumps({"spec": spec, "urteile": urteile}, ensure_ascii=False).replace("</", "<\\/")
    return PAGE.replace("__TITEL__", html.escape(spec["titel"])) \
               .replace("__HINWEIS__", html.escape(spec.get("hinweis", ""))).replace("__DATA__", data)


def serve(spec_pfad, port):
    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _send(self, code, body, typ="text/html; charset=utf-8"):
            b = body.encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", typ)
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)

        def do_GET(self):
            spec = lesen(spec_pfad, None)
            if spec is None:
                return self._send(500, "spec fehlt: " + spec_pfad, "text/plain; charset=utf-8")
            if self.path.startswith("/a?"):                # optional audio: /a?k=<key>&w=alt|neu, only files named in the spec
                import urllib.parse
                q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
                schluessel, seite_ = (q.get("k") or [""])[0], "audio_" + ((q.get("w") or ["neu"])[0])
                for g in spec["gruppen"]:
                    for it in g["items"]:
                        if it["key"] == schluessel and it.get(seite_) and os.path.isfile(it[seite_]):
                            daten = open(it[seite_], "rb").read()
                            self.send_response(200)
                            self.send_header("Content-Type", "audio/wav" if it[seite_].endswith(".wav") else "audio/mpeg")
                            self.send_header("Content-Length", str(len(daten)))
                            self.end_headers()
                            self.wfile.write(daten)
                            return
                return self._send(404, "kein Audio", "text/plain; charset=utf-8")
            if self.path.startswith("/urteile"):
                return self._send(200, json.dumps(lesen(urteil_pfad(spec_pfad), {}), ensure_ascii=False),
                                  "application/json; charset=utf-8")
            self._send(200, seite(spec, lesen(urteil_pfad(spec_pfad), {})))

        def do_POST(self):
            n = int(self.headers.get("Content-Length") or 0)
            try:
                neu = json.loads(self.rfile.read(n).decode("utf-8"))
            except ValueError:
                return self._send(400, "bad json", "text/plain")
            urteile = lesen(urteil_pfad(spec_pfad), {})
            urteile.update(neu)
            tmp = urteil_pfad(spec_pfad) + ".tmp"
            json.dump(urteile, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            os.replace(tmp, urteil_pfad(spec_pfad))
            self._send(200, "ok", "text/plain")

    print("Text-Abnahme: http://localhost:%d  (Urteile: %s)" % (port, urteil_pfad(spec_pfad)), flush=True)
    ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()


PAGE = r"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITEL__</title>
<style>
:root{--bg:#16130f;--card:#211d17;--line:#3a3328;--text:#efe6d6;--mut:#a89c88;--beige:#d9c39a;--ok:#5fae6e;--neu:#d0644f;--alt:#8d8170}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.5 system-ui,Segoe UI,sans-serif}
header{position:sticky;top:0;z-index:5;background:#16130fee;backdrop-filter:blur(6px);border-bottom:1px solid var(--line);
 padding:12px 20px;display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center}
h1{font-size:18px;margin:0;color:var(--beige);font-weight:600}.sp{flex:1}.zahl{color:var(--mut)}.zahl b{color:var(--text)}
button{font:inherit;border:1px solid var(--line);background:#2b251d;color:var(--text);border-radius:8px;padding:5px 12px;cursor:pointer}
button:hover{border-color:var(--beige)}button.an{background:var(--beige);color:#16130f;border-color:var(--beige)}
.hinweis{color:var(--mut);padding:12px 20px 0;max-width:1200px;white-space:pre-line}
main{padding:8px 20px 60px;max-width:1300px}
h2{color:var(--beige);font-size:16px;margin:28px 0 8px;font-weight:600;border-bottom:1px solid var(--line);padding-bottom:6px}
.z{display:grid;grid-template-columns:150px minmax(0,1fr) minmax(0,1fr) 190px;gap:12px;align-items:start;
 background:var(--card);border:1px solid var(--line);border-left:4px solid var(--line);border-radius:8px;padding:10px 12px;margin:6px 0}
.z.ok{border-left-color:var(--ok)}.z.neu{border-left-color:var(--neu)}
.wer{font-size:13px;color:var(--mut)}.wer b{color:var(--text);font-weight:600;display:block}
.alt{color:var(--alt);font-size:14px}.neutext{color:var(--text)}.lab{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);margin-bottom:2px}
.notiz{font-size:12px;color:var(--mut);margin-top:4px}.ton{font-size:11px;color:var(--beige);margin-left:4px}
.knoepfe{display:flex;flex-direction:column;gap:6px}.knoepfe div{display:flex;gap:6px}
textarea{width:100%;min-height:44px;background:#1a1712;color:var(--text);border:1px solid var(--line);border-radius:6px;font:13px system-ui;padding:4px 6px}
.gleich .alt{display:none}audio{width:100%;margin-top:6px;height:34px}
@media (max-width:900px){.z{grid-template-columns:1fr}}
</style></head><body>
<header><h1>__TITEL__</h1><span class="zahl" id="zahl"></span><span class="sp"></span>
<button id="alleok">Restliche OK</button><button id="kopie">Ergebnis kopieren</button></header>
<div class="hinweis">__HINWEIS__</div><main id="m"></main>
<script>
const D=__DATA__;const U=D.urteile||{};
const m=document.getElementById("m");
function esc(s){return (s||"").replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]))}
function speichern(obj){fetch("/",{method:"POST",body:JSON.stringify(obj)}).catch(()=>{})}
function zaehlen(){let n=0,ok=0,neu=0;D.spec.gruppen.forEach(g=>g.items.forEach(it=>{n++;const u=U[it.key];if(u&&u.u==="ok")ok++;if(u&&u.u==="neu")neu++;}));
 document.getElementById("zahl").innerHTML=`<b>${ok}</b> OK · <b>${neu}</b> ändern · ${n-ok-neu} offen · ${n} Texte`}
D.spec.gruppen.forEach(g=>{const h=document.createElement("h2");h.textContent=g.titel;m.appendChild(h);
 g.items.forEach(it=>{const d=document.createElement("div");const u=U[it.key]||{};d.className="z "+(u.u||"")+(it.alt===it.neu?" gleich":"");
  d.innerHTML=`<div class="wer"><b>${esc(it.wer||"")}</b>${esc(it.feld||"")}${it.gefuehl?" · "+esc(it.gefuehl):""}${it.vertont?'<span class="ton">🔊</span>':""}<div class="notiz">${esc(it.key)}</div></div>
  <div><div class="lab">alt</div><div class="alt">${esc(it.alt)||"<i>neu</i>"}</div>${it.audio_alt?`<audio controls preload="none" src="/a?k=${encodeURIComponent(it.key)}&w=alt"></audio>`:""}</div>
  <div><div class="lab">neu</div><div class="neutext">${esc(it.neu)}</div>${it.audio_neu?`<audio controls preload="none" src="/a?k=${encodeURIComponent(it.key)}&w=neu"></audio>`:""}${it.notiz?`<div class="notiz">${esc(it.notiz)}</div>`:""}</div>
  <div class="knoepfe"><div><button data-u="ok">OK</button><button data-u="neu">Ändern</button></div><textarea placeholder="Notiz">${esc(u.n||"")}</textarea></div>`;
  const bs=d.querySelectorAll("button"),ta=d.querySelector("textarea");
  function setze(v){U[it.key]={u:v,n:ta.value};d.className="z "+v+(it.alt===it.neu?" gleich":"");bs.forEach(b=>b.classList.toggle("an",b.dataset.u===v));speichern({[it.key]:U[it.key]});zaehlen()}
  bs.forEach(b=>{b.classList.toggle("an",b.dataset.u===u.u);b.onclick=()=>setze(b.dataset.u)});
  ta.onchange=()=>{U[it.key]={u:(U[it.key]||{}).u||"neu",n:ta.value};setze(U[it.key].u)};
  m.appendChild(d)})});
document.getElementById("alleok").onclick=()=>{const neu={};D.spec.gruppen.forEach(g=>g.items.forEach(it=>{if(!U[it.key]||!U[it.key].u){U[it.key]={u:"ok",n:""};neu[it.key]=U[it.key]}}));speichern(neu);location.reload()};
document.getElementById("kopie").onclick=()=>{const z=[];D.spec.gruppen.forEach(g=>g.items.forEach(it=>{const u=U[it.key];if(u&&u.u==="neu")z.push(it.key+": "+(u.n||"(ändern)"))}));
 const t=z.length?z.join("\n"):"Alles OK";navigator.clipboard.writeText(t).catch(()=>{prompt("Ergebnis",t)})};
zaehlen();
</script></body></html>"""


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--serve":
        serve(os.path.abspath(a[1]), int(a[2]) if len(a) > 2 else 8343)
    else:
        sys.exit(__doc__)
