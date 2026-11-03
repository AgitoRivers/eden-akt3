# -*- coding: utf-8 -*-
r"""Abnahme-Seite fuer Klaenge (Duc 27.10.2026: "bau eine richtige Abnahme-Seite, wo ich auswaehlen kann").

Gegenstueck zu abnahme_seite.py (Bilder): Gruppen mit Kandidaten, je Gruppe 1..max Favoriten, "keiner passt" und eine
Notiz. Jede Aenderung landet sofort in <spec>_urteil.json (liest Claude). Pixabay-Kandidaten spielen direkt vom CDN,
lokale Dateien (Pfad relativ zur Spec) liefert der Server unter /ton/<gruppe>/<nr>.

    python werkzeuge\klang_abnahme.py docs\abnahme\granaten_klang.json [port]

Spec: {"id", "titel", "hinweis", "gruppen": [{"id", "titel", "farbe", "soll", "max", "optional", "zusammen": <gruppe>,
       "kandidaten": [{"titel", "unter", "cdn": "<Pfad nach cdn.pixabay.com/audio/>" | "datei": "<relativ>", "seite"}]}]}"""
import json, os, sys, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

MIME = {".mp3": "audio/mpeg", ".ogg": "audio/ogg", ".wav": "audio/wav"}


def seite(spec, urteil):
    daten = json.dumps({"spec": spec, "urteil": urteil}, ensure_ascii=False).replace("</", "<\\/")
    return PAGE.replace("__TITEL__", spec["titel"]).replace("__DATEN__", daten)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    spec_pfad = os.path.abspath(sys.argv[1])
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8386
    urteil_pfad = os.path.splitext(spec_pfad)[0] + "_urteil.json"
    basis = os.path.dirname(spec_pfad)

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
            spec = json.load(open(spec_pfad, encoding="utf-8"))
            teile = self.path.split("?")[0].strip("/").split("/")
            if teile == [""]:
                urteil = json.load(open(urteil_pfad, encoding="utf-8")) if os.path.isfile(urteil_pfad) else {}
                return self.senden(200, seite(spec, urteil).encode("utf-8"), "text/html; charset=utf-8")
            if len(teile) == 3 and teile[0] == "ton" and teile[2].isdigit():
                g = next((g for g in spec["gruppen"] if g["id"] == teile[1]), None)
                k = g and int(teile[2]) < len(g["kandidaten"]) and g["kandidaten"][int(teile[2])]
                pfad = k and k.get("datei") and os.path.normpath(os.path.join(basis, k["datei"]))
                if pfad and os.path.isfile(pfad) and os.path.splitext(pfad)[1].lower() in MIME:
                    return self.senden(200, open(pfad, "rb").read(), MIME[os.path.splitext(pfad)[1].lower()])
            self.senden(404, b"nicht gefunden", "text/plain")

        def do_POST(self):
            if self.path.strip("/") != "urteil":
                return self.senden(404, b"nicht gefunden", "text/plain")
            daten = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            daten["_stand"] = time.strftime("%Y-%m-%d %H:%M:%S")
            with open(urteil_pfad, "w", encoding="utf-8") as f:
                json.dump(daten, f, ensure_ascii=False, indent=1)
            self.senden(200, b"ok", "text/plain")

    print("Klang-Abnahme: http://127.0.0.1:%d  (Urteile -> %s)" % (port, urteil_pfad), flush=True)
    ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()


PAGE = r"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITEL__</title>
<style>
:root{--bg:#0e0c0a;--karte:#1a1612;--karte2:#221d17;--linie:#362e25;--text:#efe6d6;--leise:#a3977f;--akz:#e0b46c;--gut:#7fc28d;--nein:#d0644f}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:15px/1.5 system-ui,Segoe UI,sans-serif}
header{position:sticky;top:0;z-index:5;background:rgba(14,12,10,.94);backdrop-filter:blur(8px);border-bottom:1px solid var(--linie);
 padding:12px 24px;display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center}
h1{font-size:20px;margin:0;color:var(--akz);font-weight:650}
.stand{color:var(--leise)}.stand b{color:var(--text)}
.leer{flex:1}
#gespeichert{color:var(--gut);font-size:13px;opacity:0;transition:opacity .3s}#gespeichert.an{opacity:1}
button{font:inherit;cursor:pointer;border-radius:999px;border:1px solid var(--linie);background:var(--karte2);color:var(--text);padding:6px 14px}
button:hover{border-color:var(--akz)}
main{max-width:1060px;margin:0 auto;padding:18px 24px 80px;display:grid;gap:18px}
.hinweis{color:var(--leise);max-width:80ch;margin:4px 0 0}
section{background:var(--karte);border:1px solid var(--linie);border-radius:16px;overflow:hidden}
section.fertig{border-color:rgba(127,194,141,.55)}section.keiner{border-color:rgba(208,100,79,.55)}
.kopf{display:flex;align-items:center;gap:12px;padding:14px 18px 6px}
.kopf i{width:14px;height:14px;border-radius:50%;flex:none;box-shadow:0 0 12px currentColor}
.kopf h2{font-size:17px;margin:0;font-weight:650}
.kopf .status{margin-left:auto;font-size:13px;color:var(--leise)}
section.fertig .status{color:var(--gut)}section.keiner .status{color:var(--nein)}
.soll{color:var(--leise);font-size:13.5px;margin:0;padding:0 18px 10px 44px}
.zeile{display:grid;grid-template-columns:34px 44px minmax(0,1fr) auto;gap:12px;align-items:center;padding:9px 18px;border-top:1px solid var(--linie);position:relative}
.zeile.gewaehlt{background:rgba(224,180,108,.09)}
.nr{font:700 17px ui-monospace,monospace;color:var(--akz);text-align:center}
.play{width:40px;height:40px;padding:0;display:grid;place-items:center;font-size:15px;border-color:var(--akz);color:var(--akz);background:rgba(224,180,108,.1)}
.zeile.spielt .play{background:var(--akz);color:#1a1612}
.name b{font-size:15px;font-weight:600}.name small{display:block;color:var(--leise);font-size:12.5px}
.name a{color:var(--leise)}
.balken{position:absolute;left:0;bottom:0;height:2px;background:var(--akz);width:0}
.wahl{min-width:116px;border-color:var(--linie)}
.zeile.gewaehlt .wahl{background:var(--akz);border-color:var(--akz);color:#1a1612;font-weight:650}
.fuss{display:flex;flex-wrap:wrap;gap:10px;align-items:center;padding:12px 18px;border-top:1px solid var(--linie);background:var(--karte2)}
.fuss textarea{flex:1;min-width:220px;min-height:38px;resize:vertical;font:inherit;font-size:14px;color:var(--text);background:var(--bg);border:1px solid var(--linie);border-radius:10px;padding:8px 10px}
.keinerknopf.an{background:var(--nein);border-color:var(--nein);color:#fff}
.zus{font-size:13px}
#blitz{position:fixed;inset:0;pointer-events:none;opacity:0;z-index:20}
#blitz.an{animation:b .6s ease-out}@keyframes b{0%{opacity:.4}100%{opacity:0}}
</style></head><body><div id="blitz"></div>
<header><h1>__TITEL__</h1><span class="stand" id="stand"></span><span class="leer"></span>
<span id="gespeichert">gespeichert ✓</span><button id="stop" type="button">■ Stopp</button><button id="kopieren" type="button">Ergebnis kopieren</button></header>
<main><p class="hinweis" id="hinweis"></p><div id="gruppen" style="display:grid;gap:18px"></div></main>
<script>
const D = __DATEN__, S = D.spec, U = Object.assign({}, D.urteil); delete U._stand;
const CDN = "https://cdn.pixabay.com/audio/";
document.getElementById("hinweis").textContent = S.hinweis || "";
const quelle = (g, i) => { const k = g.kandidaten[i]; return k.cdn ? CDN + k.cdn : `/ton/${g.id}/${i}`; };
const zustand = g => U[g.id] || (U[g.id] = {wahl: [], keiner: false, notiz: ""});
let laufend = [], aktZeile = null, raf = 0;
function stopp(){ laufend.forEach(a => a.pause()); laufend = []; if (aktZeile) aktZeile.classList.remove("spielt"); aktZeile = null; cancelAnimationFrame(raf);
  document.querySelectorAll(".balken").forEach(b => b.style.width = 0); }
function spielen(urls, zeile, farbe){
  const war = aktZeile === zeile; stopp(); if (war) return;
  laufend = urls.map(([u, verz]) => { const a = new Audio(u); setTimeout(() => a.play().catch(() => {}), verz || 0); return a; });
  aktZeile = zeile; zeile.classList.add("spielt");
  const b = document.getElementById("blitz"); b.style.background = farbe; b.classList.remove("an"); void b.offsetWidth; b.classList.add("an");
  const haupt = laufend[0], balken = zeile.querySelector(".balken");
  const tick = () => { if (haupt.duration) balken.style.width = (100 * haupt.currentTime / haupt.duration) + "%"; raf = requestAnimationFrame(tick); };
  tick(); haupt.onended = () => { if (aktZeile === zeile) stopp(); };
}
let speicherTimer = 0;
function speichern(){
  clearTimeout(speicherTimer);
  speicherTimer = setTimeout(async () => {
    try { await fetch("/urteil", {method: "POST", body: JSON.stringify(U)}); const s = document.getElementById("gespeichert");
      s.classList.add("an"); setTimeout(() => s.classList.remove("an"), 1200); } catch (e) {}
  }, 250);
  zaehlen();
}
function zaehlen(){
  let fertig = 0;
  S.gruppen.forEach(g => { const z = zustand(g), sec = document.getElementById("g-" + g.id);
    const ok = z.wahl.length > 0, nein = z.keiner && !ok;
    if (ok || nein || g.optional) fertig++;
    sec.classList.toggle("fertig", ok); sec.classList.toggle("keiner", nein);
    sec.querySelector(".status").textContent = ok ? "Gewählt: " + z.wahl.map(n => n + 1).join(" + ") : nein ? "Keiner passt" : g.optional ? "optional" : "offen";
    sec.querySelectorAll(".zeile").forEach((r, i) => { const an = z.wahl.includes(i); r.classList.toggle("gewaehlt", an);
      r.querySelector(".wahl").textContent = an ? "✓ gewählt" : "Wählen"; });
    sec.querySelector(".keinerknopf").classList.toggle("an", z.keiner);
  });
  document.getElementById("stand").innerHTML = `<b>${fertig}</b> von ${S.gruppen.length} entschieden`;
}
const wurzel = document.getElementById("gruppen");
S.gruppen.forEach(g => {
  const sec = document.createElement("section"); sec.id = "g-" + g.id;
  sec.innerHTML = `<div class="kopf"><i style="color:${g.farbe};background:${g.farbe}"></i><h2></h2><span class="status"></span></div><p class="soll"></p>`;
  sec.querySelector("h2").textContent = g.titel; sec.querySelector(".soll").textContent = g.soll || "";
  g.kandidaten.forEach((k, i) => {
    const r = document.createElement("div"); r.className = "zeile";
    const seite = k.seite ? ` · <a href="https://pixabay.com/sound-effects/${k.seite}/" target="_blank" rel="noopener">Seite</a>` : "";
    r.innerHTML = `<span class="nr">${i + 1}</span><button class="play" type="button" title="Abspielen">▶</button>
      <span class="name"><b></b><small>${k.unter || ""}${seite}</small></span>
      <span style="display:flex;gap:8px;align-items:center">${g.zusammen ? '<button class="zus" type="button">▶ mit Knall</button>' : ""}<button class="wahl" type="button">Wählen</button></span><span class="balken"></span>`;
    r.querySelector("b").textContent = k.titel;
    r.querySelector(".play").onclick = () => spielen([[quelle(g, i)]], r, g.farbe);
    if (g.zusammen) r.querySelector(".zus").onclick = () => {
      const p = S.gruppen.find(x => x.id === g.zusammen), w = zustand(p).wahl[0];
      spielen([[quelle(g, i), 250], ...(w === undefined ? [] : [[quelle(p, w)]])].reverse(), r, g.farbe);
    };
    r.querySelector(".wahl").onclick = () => {
      const z = zustand(g), pos = z.wahl.indexOf(i);
      if (pos >= 0) z.wahl.splice(pos, 1); else { z.wahl.push(i); if (z.wahl.length > (g.max || 1)) z.wahl.shift(); z.keiner = false; }
      speichern();
    };
    sec.appendChild(r);
  });
  const f = document.createElement("div"); f.className = "fuss";
  f.innerHTML = `<button class="keinerknopf" type="button">Keiner passt</button><textarea placeholder="Notiz (z. B. kürzer schneiden, lauter, Knall von 2 + Hall von 4 …)"></textarea>`;
  const ta = f.querySelector("textarea"); ta.value = zustand(g).notiz || "";
  ta.oninput = () => { zustand(g).notiz = ta.value; speichern(); };
  f.querySelector(".keinerknopf").onclick = () => { const z = zustand(g); z.keiner = !z.keiner; if (z.keiner) z.wahl = []; speichern(); };
  sec.appendChild(f); wurzel.appendChild(sec);
});
document.getElementById("stop").onclick = stopp;
document.addEventListener("keydown", e => { if (e.code === "Space" && e.target.tagName !== "TEXTAREA"){ e.preventDefault(); stopp(); } });
document.getElementById("kopieren").onclick = async () => {
  const t = S.gruppen.map(g => { const z = zustand(g); return g.titel + ": " + (z.wahl.length ? z.wahl.map(n => n + 1).join("+") : z.keiner ? "keiner" : "–") + (z.notiz ? " (" + z.notiz + ")" : ""); }).join(" · ");
  try { await navigator.clipboard.writeText(t); } catch (e) { window.prompt("Ergebnis:", t); }
};
zaehlen();
</script></body></html>
"""

if __name__ == "__main__":
    main()
