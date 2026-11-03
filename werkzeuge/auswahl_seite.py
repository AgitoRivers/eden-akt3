# -*- coding: utf-8 -*-
r"""Pick page: from each group of candidate images Duc keeps exactly one (Duc 27.10.2026, selfie stages).

Unlike abnahme_seite.py (OK/Neu per image) every group here is a row of variants and one click marks the keeper.
The choices are saved next to the spec as <spec>_auswahl.json ({gruppen_id: dateipfad}).

Spec (JSON):
    {"id": "selfies_r2", "titel": "...", "hinweis": "...",
     "abschnitte": [{"titel": "Alva", "gruppen": [{"id": "alva|bar|knapp", "titel": "Bar · knapp",
                                                  "bilder": ["X:\\...\\a.png", ...]}]}]}

    auswahl_seite.py spec.json [port]
"""
import hashlib, html, io, json, os, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


VORSCHAU = os.path.join(os.environ.get("TEMP", "."), "eden_auswahl_vorschau")


def vorschau(pfad):
    """Small JPEG (480 px high) cached in %TEMP%, so a page with 150 full PNGs stays quick."""
    os.makedirs(VORSCHAU, exist_ok=True)
    ziel = os.path.join(VORSCHAU, hashlib.md5(("%s|%s" % (pfad, os.path.getmtime(pfad))).encode()).hexdigest() + ".jpg")
    if not os.path.isfile(ziel):
        from PIL import Image
        im = Image.open(pfad).convert("RGB")
        im.thumbnail((480, 480))
        im.save(ziel, quality=85)
    return open(ziel, "rb").read()


def lade(spec_path):
    spec = json.load(open(spec_path, encoding="utf-8"))
    pfade = [b for a in spec["abschnitte"] for g in a["gruppen"] for b in g["bilder"]]
    return spec, pfade


def build(spec, pfade, wahl):
    nr = {p: i for i, p in enumerate(pfade)}
    data = {"titel": spec["titel"], "wahl": wahl,
            "abschnitte": [{"titel": a["titel"], "gruppen": [
                {"id": g["id"], "titel": g["titel"],
                 "bilder": [{"pfad": b, "url": "bild/%d" % nr[b], "klein": "klein/%d" % nr[b], "name": os.path.basename(b)} for b in g["bilder"]]}
                for g in a["gruppen"]]} for a in spec["abschnitte"]]}
    return PAGE.replace("__TITEL__", html.escape(spec["titel"])) \
               .replace("__HINWEIS__", html.escape(spec.get("hinweis", ""))) \
               .replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))


PAGE = r"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITEL__</title>
<style>
:root{--bg:#16130f;--card:#211d17;--line:#3a3328;--text:#efe6d6;--mut:#a89c88;--beige:#d9c39a;--ok:#5fae6e}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.45 system-ui,Segoe UI,sans-serif}
header{position:sticky;top:0;z-index:5;background:#16130fee;backdrop-filter:blur(6px);border-bottom:1px solid var(--line);
 padding:12px 16px;display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center}
h1{font-size:18px;margin:0;color:var(--beige);font-weight:600}
.zahl{color:var(--mut)}.zahl b{color:var(--text)}.sp{flex:1}
button{font:inherit;border:1px solid var(--line);background:#2b251d;color:var(--text);border-radius:8px;padding:6px 12px;cursor:pointer}
button:hover{border-color:var(--beige)}button.an{background:var(--beige);color:#16130f;border-color:var(--beige)}
nav{display:flex;flex-wrap:wrap;gap:6px}nav a{color:var(--mut);text-decoration:none;font-size:13px;padding:2px 8px;border:1px solid var(--line);border-radius:12px}
nav a.fertig{color:var(--ok);border-color:var(--ok)}
.hinweis{color:var(--mut);padding:10px 16px 0;max-width:1100px}
section{padding:8px 16px 16px}
h2{font-size:20px;color:var(--beige);margin:18px 0 10px;font-weight:600;display:flex;gap:12px;align-items:baseline}
h2 small{font-size:13px;color:var(--mut);font-weight:400}
.gruppen{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,560px),1fr));gap:14px}
.g{background:var(--card);border:2px solid var(--line);border-radius:12px;padding:10px;min-width:0}
.g.fertig{border-color:var(--ok)}.g.versteckt{display:none}
.g h3{margin:0 0 8px;font-size:15px;display:flex;gap:8px}.g h3 span{margin-left:auto;color:var(--mut);font-weight:400;font-size:12px}
.g.fertig h3 span{color:var(--ok)}
.reihe{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:6px}
.b{position:relative;border:3px solid transparent;border-radius:8px;overflow:hidden;cursor:pointer;background:#0c0a08}
.b img{width:100%;aspect-ratio:2/3;object-fit:cover;display:block}
.b.wahl{border-color:var(--ok)}.g.fertig .b:not(.wahl) img{opacity:.45}
.b.wahl::after{content:"✓";position:absolute;left:6px;top:4px;background:var(--ok);color:#0d1a10;font-weight:700;border-radius:50%;width:24px;height:24px;display:grid;place-items:center}
.lupe{position:absolute;right:4px;top:4px;background:#000a;border:0;padding:2px 7px;border-radius:6px;font-size:13px}
#gross{position:fixed;inset:0;background:#000e;display:none;align-items:center;justify-content:center;z-index:9;flex-direction:column;gap:10px}
#gross img{max-width:96vw;max-height:86vh}
#gross .leiste{display:flex;gap:10px;align-items:center;color:var(--mut)}
</style></head><body>
<header><h1>__TITEL__</h1>
 <span class="zahl"><b id="n-ok">0</b> von <b id="n-alle">0</b> gewählt</span>
 <span class="sp"></span>
 <button id="f-offen">Nur offene</button>
</header>
<p class="hinweis">__HINWEIS__ Klick aufs Bild = behalten (nochmal = abwählen), 🔍 = groß. Im Großbild: ← → blättern, Enter = behalten, Esc = zu. Wird sofort gespeichert.</p>
<div style="padding:8px 16px 0"><nav id="nav"></nav></div>
<div id="inhalt"></div>
<div id="gross"><img alt=""><div class="leiste"><button id="g-zurueck">←</button><span id="g-text"></span><button id="g-weiter">→</button><button id="g-wahl">Behalten</button><button id="g-zu">Schließen</button></div></div>
<script>
const D = __DATA__;
const W = D.wahl || {};
let nurOffen = false, timer = null, offen = null;
const speichern = () => { clearTimeout(timer); timer = setTimeout(() => fetch("auswahl", {method: "POST", body: JSON.stringify(W)}), 250); };
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
const alleG = D.abschnitte.flatMap(a => a.gruppen);
function render() {
  document.getElementById("inhalt").innerHTML = D.abschnitte.map((a, ai) => `<section id="a${ai}"><h2>${esc(a.titel)} <small>${a.gruppen.length} Gruppen</small></h2><div class="gruppen">` +
    a.gruppen.map(g => `<div class="g" data-g="${esc(g.id)}"><h3>${esc(g.titel)}<span></span></h3><div class="reihe">` +
      g.bilder.map((b, bi) => `<div class="b" data-p="${esc(b.pfad)}" title="${esc(b.name)}"><img src="${b.klein}" alt=""><button class="lupe" data-bi="${bi}">🔍</button></div>`).join("") +
      `</div></div>`).join("") + `</div></section>`).join("");
  document.getElementById("nav").innerHTML = D.abschnitte.map((a, ai) => `<a href="#a${ai}" data-ai="${ai}">${esc(a.titel)}</a>`).join("");
  zustand();
}
function zustand() {
  let ok = 0;
  document.querySelectorAll(".g").forEach(el => {
    const w = W[el.dataset.g]; if (w) ok++;
    el.classList.toggle("fertig", !!w);
    el.classList.toggle("versteckt", nurOffen && !!w);
    el.querySelector("h3 span").textContent = w ? "✓ gewählt" : el.querySelectorAll(".b").length + " Varianten";
    el.querySelectorAll(".b").forEach(b => b.classList.toggle("wahl", b.dataset.p === w));
  });
  D.abschnitte.forEach((a, ai) => document.querySelector(`nav a[data-ai="${ai}"]`).classList.toggle("fertig", a.gruppen.every(g => W[g.id])));
  document.getElementById("n-ok").textContent = ok;
  document.getElementById("n-alle").textContent = alleG.length;
}
function waehle(gid, pfad) { if (W[gid] === pfad) delete W[gid]; else W[gid] = pfad; zustand(); speichern(); }
function zeige() {
  const g = alleG.find(x => x.id === offen.g), b = g.bilder[offen.i];
  const box = document.getElementById("gross");
  box.querySelector("img").src = b.url; box.style.display = "flex";
  document.getElementById("g-text").textContent = `${g.titel} · ${offen.i + 1}/${g.bilder.length}`;
  document.getElementById("g-wahl").className = W[g.id] === b.pfad ? "an" : "";
}
function blaettern(d) { const g = alleG.find(x => x.id === offen.g); offen.i = (offen.i + d + g.bilder.length) % g.bilder.length; zeige(); }
function zu() { document.getElementById("gross").style.display = "none"; offen = null; }
document.getElementById("inhalt").addEventListener("click", e => {
  const gEl = e.target.closest(".g"); if (!gEl) return;
  if (e.target.classList.contains("lupe")) { offen = {g: gEl.dataset.g, i: +e.target.dataset.bi}; zeige(); return; }
  const b = e.target.closest(".b"); if (b) waehle(gEl.dataset.g, b.dataset.p);
});
document.getElementById("g-zurueck").onclick = () => blaettern(-1);
document.getElementById("g-weiter").onclick = () => blaettern(1);
document.getElementById("g-zu").onclick = zu;
document.getElementById("g-wahl").onclick = () => { const g = alleG.find(x => x.id === offen.g); waehle(g.id, g.bilder[offen.i].pfad); zeige(); };
document.getElementById("gross").addEventListener("click", e => { if (e.target.id === "gross") zu(); });
document.addEventListener("keydown", e => {
  if (!offen) return;
  if (e.key === "Escape") zu(); else if (e.key === "ArrowLeft") blaettern(-1); else if (e.key === "ArrowRight") blaettern(1);
  else if (e.key === "Enter") document.getElementById("g-wahl").click();
});
document.getElementById("f-offen").onclick = e => { nurOffen = !nurOffen; e.target.classList.toggle("an", nurOffen); zustand(); };
render();
</script></body></html>
"""


def serve(spec_path, port):
    wahl_path = os.path.splitext(spec_path)[0] + "_auswahl.json"

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
            spec, pfade = lade(spec_path)
            if self.path.startswith(("/bild/", "/klein/")):
                n = int(self.path.split("/")[2].split("?")[0])
                if 0 <= n < len(pfade) and os.path.isfile(pfade[n]):
                    if self.path.startswith("/klein/"):
                        return self.send(200, vorschau(pfade[n]), "image/jpeg")
                    ext = os.path.splitext(pfade[n])[1].lower()
                    return self.send(200, open(pfade[n], "rb").read(), "image/png" if ext == ".png" else "image/jpeg")
                return self.send(404, b"", "text/plain")
            wahl = json.load(open(wahl_path, encoding="utf-8")) if os.path.isfile(wahl_path) else {}
            self.send(200, build(spec, pfade, wahl).encode("utf-8"), "text/html; charset=utf-8")

        def do_POST(self):
            daten = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            with open(wahl_path, "w", encoding="utf-8") as fh:
                json.dump(daten, fh, ensure_ascii=False, indent=1)
            self.send(200, b"ok", "text/plain")

    print("Auswahl-Seite: http://127.0.0.1:%d  (Wahl -> %s)" % (port, wahl_path), flush=True)
    ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()


if __name__ == "__main__":
    serve(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 8347)
