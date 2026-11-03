# -*- coding: utf-8 -*-
r"""Abnahme der Granaten-Einschlaege (Duc 28.10.2026: "bau die JangaFX-Effekte ein und zeig es mir in der Abnahme").

Zwei Buehnen nebeneinander, beide mit dem echten Effekt-Code: links der Stand vor den JangaFX-Boegen (Commit ALT, per
git show), rechts der jetzige Stand der Arbeitskopie. Ein Klick wirft dieselbe Granate auf beiden Seiten, mit Ducs Klaengen.
Zeitlupe verlangsamt beide Buehnen. Je Granate: "Neu nehmen" / "Alt behalten" / "Nochmal ran" + Notiz -> sofort in
docs\abnahme\granaten_fx_urteil.json (liest Claude). Bilder, Sprites, Klaenge und Effekt-Dateien reicht der Server vom
laufenden Eden-Vorschauserver durch (Standard http://127.0.0.1:8369, der braucht einen Kampf, z. B. launch eden-kampf-heiler).

    python werkzeuge\granaten_fx_abnahme.py [port=8391] [eden=http://127.0.0.1:8369]"""
import json, os, subprocess, sys, time, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URTEIL = os.path.join(EDEN, "docs", "abnahme", "granaten_fx_urteil.json")
ALT = "037e410"                       # letzter Stand mit den alten Einschlaegen (Klaenge + Wurf schon neu)
EFFEKTE = "client/plugins/eden-combat/eden-combat-effects.js"
GRANATEN = [
    {"id": "brennend", "item": "grenade_fire", "titel": "Feuer", "farbe": "#ff7a2a", "ton": "feuer",
     "alt": "Labor-Feuerball, Nachbrennen", "neu": "nur Bodenexplosion, wächst von unten, größer; Nachbrennen später"},
    {"id": "nass", "item": "grenade_water", "titel": "Wasser", "farbe": "#3fa7ff", "ton": "wasser",
     "alt": "gespiegelte LiquiGen-Fontäne", "neu": "Ducs LiquiGen-Wasserball, größer"},
    {"id": "erschuettert", "item": "grenade_concussion", "titel": "Erschütterung", "farbe": "#c8b89a", "ton": "erschuetterung",
     "alt": "Goldring + Staub", "neu": "Rauchring am Körper + flach am Boden, Staubpilz aus der Bodenexplosion"},
    {"id": "blutend", "item": "grenade_shrapnel", "titel": "Splitter", "farbe": "#ff4a4a", "ton": "splitter",
     "alt": "EmberGen-Druckstoß", "neu": "EmberGen-Druckstoß wie alt, aber gedreht: qualmt nach oben"},
    {"id": "strom", "item": "grenade_shock", "titel": "Schock", "farbe": "#ffe14a", "ton": "schock",
     "alt": "", "neu": "unverändert (kein neues Material) – zum Vergleich"},
    {"id": "geblendet", "item": "grenade_flash", "titel": "Flash", "farbe": "#ffffff", "ton": "flash",
     "alt": "", "neu": "unverändert (kein neues Material) – zum Vergleich"},
]


def buehne(seite, zeit):
    skript = "/alt/eden-combat-effects.js" if seite == "alt" else "/plugins/eden-combat/eden-combat-effects.js?t=%d" % time.time()
    return BUEHNE.replace("__ZEIT__", str(zeit)).replace("__SKRIPT__", skript).replace("__SEITE__", seite)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8391
    quelle = (sys.argv[2] if len(sys.argv) > 2 else "http://127.0.0.1:8369").rstrip("/")

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def senden(self, code, body, typ):
            self.send_response(code)
            self.send_header("Content-Type", typ)
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            u = urlparse(self.path)
            if u.path == "/":
                urteil = json.load(open(URTEIL, encoding="utf-8")) if os.path.isfile(URTEIL) else {}
                daten = json.dumps({"granaten": GRANATEN, "urteil": urteil}, ensure_ascii=False).replace("</", "<\\/")
                return self.senden(200, PAGE.replace("__DATEN__", daten).encode("utf-8"), "text/html; charset=utf-8")
            if u.path == "/buehne":
                q = parse_qs(u.query)
                seite = "alt" if q.get("v", ["neu"])[0] == "alt" else "neu"
                zeit = max(.05, min(1.0, float(q.get("zeit", ["1"])[0])))
                return self.senden(200, buehne(seite, zeit).encode("utf-8"), "text/html; charset=utf-8")
            if u.path == "/alt/eden-combat-effects.js":
                js = subprocess.run(["git", "-C", EDEN, "show", "%s:%s" % (ALT, EFFEKTE)], capture_output=True, check=True).stdout
                return self.senden(200, js, "text/javascript; charset=utf-8")
            try:                                          # alles andere: vom Eden-Vorschauserver durchreichen
                with urllib.request.urlopen(quelle + self.path, timeout=20) as r:
                    return self.senden(r.status, r.read(), r.headers.get("Content-Type", "application/octet-stream"))
            except Exception as f:
                return self.senden(502, ("Eden-Vorschau %s nicht erreichbar: %s" % (quelle, f)).encode("utf-8"), "text/plain; charset=utf-8")

        def do_POST(self):
            if self.path.strip("/") != "urteil":
                return self.senden(404, b"nicht gefunden", "text/plain")
            daten = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            daten["_stand"] = time.strftime("%Y-%m-%d %H:%M:%S")
            with open(URTEIL, "w", encoding="utf-8") as f:
                json.dump(daten, f, ensure_ascii=False, indent=1)
            self.senden(200, b"ok", "text/plain")

    print("Granaten-Abnahme: http://127.0.0.1:%d  (Eden: %s, Urteile -> %s)" % (port, quelle, URTEIL), flush=True)
    ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()


# Eine Buehne: Kampfhintergrund, Duc links, Keiler rechts, der Effekt-Code der Seite. Zeitlupe: Uhr, Timer, rAF-Zeit und
# Web-Animationen laufen mit dem Faktor __ZEIT__ (vor dem Effekt-Code gesetzt, damit er nur die langsame Uhr sieht).
BUEHNE = r"""<!doctype html>
<html lang="de"><head><meta charset="utf-8">
<style>
html,body{margin:0;height:100%;background:#000;overflow:hidden}
#app{position:relative;width:100%;height:100%;overflow:hidden;background:#000 url(/bg/eden_rise_macchia_creek_bridge.png) center/cover}
.dsprite{position:absolute;left:36%;bottom:1%;height:46%;transform:translateX(-50%)}
.gsprite{position:absolute;left:66%;bottom:1%;height:28%;transform:translateX(-50%)}
</style>
<script>
(() => {
  const F = __ZEIT__; if (F >= 1) return;
  const echt = performance.now.bind(performance), t0 = echt();
  performance.now = () => t0 + (echt() - t0) * F;
  const st = window.setTimeout.bind(window);
  window.setTimeout = (f, ms, ...a) => st(f, (ms || 0) / F, ...a);
  const raf = window.requestAnimationFrame.bind(window);
  window.requestAnimationFrame = f => raf(() => f(performance.now()));
  const an = Element.prototype.animate;
  Element.prototype.animate = function(k, o){ const a = an.call(this, k, o); a.playbackRate = F; return a; };
})();
</script>
<script src="__SKRIPT__"></script>
</head><body>
<div id="app"><img class="dsprite" src="/kampfbild/DucErdeBat/idle.webp" alt=""><img class="gsprite" src="/kampfbild/LionAlpha/idle.webp" alt=""></div>
<script>
addEventListener("message", ev => {
  const m = ev.data || {};
  if (!m.werfen || !window.EdenCombatEffects) return;
  document.querySelectorAll("#app > div").forEach(d => d.remove());     // Reste des letzten Wurfs
  EdenCombatEffects.play("granate", document.querySelector(".gsprite"), {zustand: m.werfen, id: m.id, von: document.querySelector(".dsprite")});
});
if (window.EdenCombatEffects && EdenCombatEffects.vorladen) EdenCombatEffects.vorladen();   // kein Kampf hier: selbst vorladen
parent.postMessage({bereit: "__SEITE__", wurf: window.EdenCombatEffects && EdenCombatEffects.WURF_MS, vor: (window.EdenCombatEffects && EdenCombatEffects.WURF_VOR) || 0}, "*");
</script>
</body></html>"""

PAGE = r"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Granaten-Einschläge</title>
<style>
:root{--bg:#0e0c0a;--karte:#1a1612;--karte2:#221d17;--linie:#362e25;--text:#efe6d6;--leise:#a3977f;--akz:#e0b46c;--gut:#7fc28d;--nein:#d0644f}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:15px/1.5 system-ui,Segoe UI,sans-serif}
header{position:sticky;top:0;z-index:5;background:rgba(14,12,10,.95);backdrop-filter:blur(8px);border-bottom:1px solid var(--linie);
 padding:12px 24px;display:flex;gap:18px;align-items:center;flex-wrap:wrap}
h1{font-size:19px;margin:0;font-weight:650;letter-spacing:.01em}
.stand{color:var(--leise);font-variant-numeric:tabular-nums}
.stand b{color:var(--text)}
#gespeichert{color:var(--gut);opacity:0;transition:opacity .3s}
.tempo{margin-left:auto;display:flex;gap:6px;align-items:center;color:var(--leise)}
button{font:inherit;color:var(--text);background:var(--karte2);border:1px solid var(--linie);border-radius:8px;padding:6px 12px;cursor:pointer}
button:hover{border-color:var(--akz)}
button.an{background:var(--akz);color:#1a1209;border-color:var(--akz);font-weight:600}
main{padding:18px 24px 60px;display:grid;grid-template-columns:300px minmax(0,1fr);gap:22px;align-items:start}
.liste{display:flex;flex-direction:column;gap:10px;position:sticky;top:74px}
.gr{background:var(--karte);border:1px solid var(--linie);border-radius:12px;padding:12px 14px;display:flex;flex-direction:column;gap:8px;cursor:pointer}
.gr.aktiv{border-color:var(--akz);box-shadow:0 0 0 1px var(--akz) inset}
.kopf{display:flex;align-items:center;gap:10px}
.punkt{width:12px;height:12px;border-radius:50%;flex:none;box-shadow:0 0 8px currentColor}
.kopf b{font-size:16px}
.status{margin-left:auto;font-size:12.5px;color:var(--leise)}
.status.neu{color:var(--gut)} .status.alt{color:var(--akz)} .status.nochmal{color:var(--nein)}
.wahl{display:flex;gap:6px;flex-wrap:wrap}
.wahl button{padding:4px 10px;font-size:13px}
.wahl button.neu.an{background:var(--gut);border-color:var(--gut)}
.wahl button.nochmal.an{background:var(--nein);border-color:var(--nein);color:#fff}
textarea{width:100%;min-height:36px;resize:vertical;background:var(--bg);color:var(--text);border:1px solid var(--linie);border-radius:8px;padding:6px 8px;font:13px/1.4 inherit}
.buehnen{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.b{display:flex;flex-direction:column;gap:6px;min-width:0}
.b .t{display:flex;justify-content:space-between;align-items:baseline;gap:10px}
.b .t b{font-size:15px}
.b .t span{color:var(--leise);font-size:13px;text-align:right}
.rahmen{width:100%;aspect-ratio:16/9;border:1px solid var(--linie);border-radius:10px;background:#000;overflow:hidden;position:relative}
iframe{width:1600px;height:900px;border:0;transform-origin:0 0;position:absolute;left:0;top:0}
.werfen{display:flex;gap:12px;align-items:center;margin-top:14px}
.werfen button{font-size:17px;padding:10px 22px}
.hinweis{color:var(--leise);font-size:13.5px;max-width:70ch}
</style></head><body>
<header>
 <h1>Granaten-Einschläge · JangaFX</h1>
 <span class="stand"><b id="zahl">0</b> von <span id="gesamt">0</span> entschieden</span>
 <span id="gespeichert">gespeichert ✓</span>
 <span class="tempo">Tempo
  <button data-z="1" class="an">normal</button><button data-z="0.5">½</button><button data-z="0.25">¼</button><button data-z="0.1">⅒</button></span>
</header>
<main>
 <div class="liste" id="liste"></div>
 <div>
  <div class="buehnen">
   <div class="b"><div class="t"><b>Alt</b><span id="altText"></span></div><div class="rahmen"><iframe id="alt" title="Alt"></iframe></div></div>
   <div class="b"><div class="t"><b>Neu</b><span id="neuText"></span></div><div class="rahmen"><iframe id="neu" title="Neu"></iframe></div></div>
  </div>
  <div class="werfen"><button id="los" class="an">▶ Werfen</button>
   <span class="hinweis">Leertaste wirft nochmal. Beide Seiten nutzen den echten Kampf-Code und dieselben Klänge; links der Stand vor den JangaFX-Bögen.</span></div>
 </div>
</main>
<script>
const D = __DATEN__, G = D.granaten, U = D.urteil || {};
let aktiv = G[0].id, zeit = 1, wurf = 1200, vor = {alt: 0, neu: 350}, timer = null;
const $ = id => document.getElementById(id);
function speichern(){
  clearTimeout(timer);
  timer = setTimeout(async () => {
    try { await fetch("/urteil", {method: "POST", body: JSON.stringify(U)}); const s = $("gespeichert");
          s.style.opacity = 1; setTimeout(() => s.style.opacity = 0, 1200); } catch (e) {}
  }, 250);
}
function zeichnen(){
  $("liste").innerHTML = G.map(g => {
    const u = U[g.id] || {}, w = u.wahl || "";
    const st = {neu: "Neu nehmen", alt: "Alt behalten", nochmal: "Nochmal ran"}[w] || "offen";
    return `<div class="gr ${g.id === aktiv ? "aktiv" : ""}" data-id="${g.id}">
      <div class="kopf"><span class="punkt" style="color:${g.farbe};background:${g.farbe}"></span><b>${g.titel}</b>
       <span class="status ${w}">${st}</span></div>
      <div class="wahl">${["neu", "alt", "nochmal"].map(x => `<button class="${x} ${w === x ? "an" : ""}" data-w="${x}">${{neu: "Neu nehmen", alt: "Alt behalten", nochmal: "Nochmal ran"}[x]}</button>`).join("")}</div>
      <textarea placeholder="Notiz (z. B. größer, früher, weniger Rauch)">${(u.notiz || "").replace(/</g, "&lt;")}</textarea></div>`;
  }).join("");
  const g = G.find(x => x.id === aktiv);
  $("altText").textContent = g.alt || "wie neu"; $("neuText").textContent = g.neu;
  $("zahl").textContent = G.filter(x => (U[x.id] || {}).wahl).length; $("gesamt").textContent = G.length;
}
$("liste").addEventListener("click", ev => {
  const k = ev.target.closest(".gr"); if (!k) return;
  const id = k.dataset.id, b = ev.target.closest("button[data-w]");
  if (b){ U[id] = U[id] || {}; U[id].wahl = U[id].wahl === b.dataset.w ? "" : b.dataset.w; speichern(); }
  if (ev.target.tagName === "TEXTAREA") { if (aktiv !== id){ aktiv = id; zeichnen(); } return; }
  const neu = aktiv !== id; aktiv = id; zeichnen(); if (neu && !b) werfen();
});
$("liste").addEventListener("input", ev => {
  if (ev.target.tagName !== "TEXTAREA") return;
  const id = ev.target.closest(".gr").dataset.id; U[id] = U[id] || {}; U[id].notiz = ev.target.value; speichern();
});
function ton(name, ms){
  setTimeout(() => { const a = new Audio("/sfx/kampf_granate_" + name + "_1.mp3"); a.volume = .7; a.playbackRate = Math.max(.5, zeit); a.play().catch(() => {}); }, ms / zeit);
}
function werfen(){
  const g = G.find(x => x.id === aktiv);
  const vorlauf = Math.max(vor.alt, vor.neu);            // beide Buehnen schlagen gleichzeitig ein: die ohne Splint-Vorlauf wirft spaeter
  for (const s of ["alt", "neu"]) setTimeout(() => $(s).contentWindow.postMessage({werfen: g.id, id: g.item}, "*"), (vorlauf - vor[s]) / zeit);
  ton("wurf", 0); ton(g.ton, wurf);
  if (g.id === "geblendet") ton("pfeifen", wurf + 500);
}
addEventListener("message", ev => { const m = ev.data || {}; if (!m.bereit) return; vor[m.bereit] = m.vor || 0; if (m.bereit === "neu" && m.wurf) wurf = m.wurf; });
function laden(){ for (const s of ["alt", "neu"]) $(s).src = "/buehne?v=" + s + "&zeit=" + zeit; }
document.querySelectorAll(".tempo button").forEach(b => b.onclick = () => {
  zeit = Number(b.dataset.z); document.querySelectorAll(".tempo button").forEach(x => x.classList.toggle("an", x === b)); laden();
});
$("los").onclick = werfen;
addEventListener("keydown", ev => { if (ev.code === "Space" && ev.target.tagName !== "TEXTAREA"){ ev.preventDefault(); werfen(); } });
function passen(){                                    // Buehne laeuft in Spielgroesse 1600x900 und wird nur verkleinert
  for (const s of ["alt", "neu"]){ const f = $(s), w = f.parentElement.clientWidth; f.style.transform = "scale(" + (w / 1600) + ")"; }
}
addEventListener("resize", passen);
zeichnen(); laden(); passen();
</script>
</body></html>"""

if __name__ == "__main__":
    main()
