# -*- coding: utf-8 -*-
r"""Click demo for a location frame (21.10.2026): Macchia frame 1-2 with hotspots, an encounter, a clue check,
the bag and the trail clock - to judge how exploration feels with static backgrounds. Not engine code.

    python orte_demo.py <background.png> [enemy_sprite.png]   -> docs\orte_demo.html (self-contained)
"""
import base64, io, os, sys

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "docs", "orte_demo.html")


def data_uri(path, max_w):
    im = Image.open(path)
    im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
    im.thumbnail((max_w, max_w))
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=82)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


def main():
    bg = data_uri(sys.argv[1], 1600)
    enemy = data_uri(sys.argv[2], 500) if len(sys.argv) > 2 else ""
    html = TEMPLATE.replace("__BG__", bg).replace("__ENEMY__", enemy)
    open(OUT, "w", encoding="utf-8").write(html)
    print(OUT, os.path.getsize(OUT) // 1024, "KB")


TEMPLATE = r"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Macchia Demo</title>
<style>
:root{--gold:#d8bd86;--ink:#f3eee4;--glass:rgba(14,15,19,.72);--green:#5fd07a;--orange:#f0a040;--red:#e05555}
*{box-sizing:border-box}html,body{margin:0;height:100%;background:#0d0e12;color:var(--ink);font:15px/1.45 system-ui,Segoe UI,sans-serif}
.stage{position:relative;width:100%;max-width:1400px;margin:0 auto;aspect-ratio:16/9;overflow:hidden;background:#222 center/cover no-repeat;background-image:url('__BG__')}
@media (max-width:700px){.stage{aspect-ratio:auto;height:100vh}}
.top{position:absolute;inset:10px 10px auto 10px;display:flex;justify-content:space-between;gap:8px;align-items:flex-start}
.pill{background:var(--glass);border:1px solid #ffffff22;border-radius:10px;padding:6px 10px;backdrop-filter:blur(4px)}
.pill b{color:var(--gold)}.clock{display:flex;gap:4px}.seg{width:22px;height:10px;border-radius:3px;background:var(--gold)}.seg.off{background:#ffffff25}
.bag{display:flex;gap:4px;flex-wrap:wrap;max-width:260px}.slot{width:30px;height:30px;border-radius:6px;background:#ffffff14;border:1px solid #ffffff22;display:grid;place-items:center;font-size:17px}
.hot{position:absolute;transform:translate(-50%,-50%);cursor:pointer;border:none;background:none;padding:0}
.hot .ring{width:44px;height:44px;border-radius:50%;display:grid;place-items:center;font-size:20px;background:rgba(20,20,24,.55);border:2px solid var(--gold);box-shadow:0 0 0 0 rgba(216,189,134,.7);animation:pulse 2s infinite}
.hot.used{opacity:.25;pointer-events:none}.hot span{display:block;margin-top:4px;font-size:12px;text-shadow:0 1px 3px #000;white-space:nowrap}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(216,189,134,.6)}70%{box-shadow:0 0 0 14px rgba(216,189,134,0)}100%{box-shadow:0 0 0 0 rgba(216,189,134,0)}}
.enemy{position:absolute;right:16%;bottom:22%;height:42%;cursor:pointer;filter:drop-shadow(0 8px 10px #000a);transition:opacity .4s}
.enemy.gone{opacity:0;pointer-events:none}
.tag{position:absolute;right:16%;bottom:65%;transform:translateX(30%);font-weight:700;padding:3px 8px;border-radius:8px;background:var(--glass)}
.box{position:absolute;left:10px;right:10px;bottom:10px;background:var(--glass);border:1px solid #ffffff22;border-radius:12px;padding:12px 14px;backdrop-filter:blur(5px)}
.box .who{color:var(--gold);font-size:13px;margin-bottom:2px}.box p{margin:0 0 8px}
.btns{display:flex;gap:8px;flex-wrap:wrap}.btn{background:var(--gold);color:#15161a;border:0;border-radius:9px;padding:8px 14px;font-weight:700;cursor:pointer}
.btn.ghost{background:#ffffff1a;color:var(--ink);border:1px solid #ffffff30}.btn:disabled{opacity:.35;cursor:default}
.arrow{position:absolute;right:10px;top:46%;font-size:30px}
.dice{display:inline-block;padding:2px 8px;border-radius:6px;background:#ffffff1a;margin-left:6px}
.legend{max-width:1400px;margin:10px auto;padding:0 12px;color:#a8a294;font-size:13px}
</style></head><body>
<div class="stage" id="stage">
  <div class="top">
    <div class="pill">Tag 4 · <b>Mittag</b> · Macchia, Frame <b id="frame">1</b>/8 · Level 1–2</div>
    <div class="pill"><div style="font-size:12px;margin-bottom:4px">Spur-Uhr: Rette Frederico</div><div class="clock" id="clock"></div></div>
    <div class="pill"><div style="font-size:12px;margin-bottom:4px">Tasche <span id="bagc"></span></div><div class="bag" id="bag"></div></div>
  </div>
  <button class="hot" id="h_herb" style="left:18%;top:72%"><div class="ring">✨</div><span>Wildkräuter</span></button>
  <button class="hot" id="h_wood" style="left:36%;top:58%"><div class="ring">⛏️</div><span>Hartholz (Axt)</span></button>
  <button class="hot" id="h_clue" style="left:55%;top:48%"><div class="ring">🔍</div><span>Spur</span></button>
  <img class="enemy" id="enemy" src="__ENEMY__" alt="">
  <div class="tag" id="etag" style="color:var(--green)">Ratte · Lv 1 · Gefährlich</div>
  <div class="arrow pill" id="next" title="Weiter">➡️</div>
  <div class="box"><div class="who" id="who">Erzähler</div><p id="txt">Der Pfad hinter dem Dorf windet sich durch die Macchia. Myrte und Zistrose duften in der Mittagshitze. Irgendwo knackt ein Ast – zu laut für den Wind.</p>
    <div class="btns" id="btns"></div></div>
</div>
<p class="legend">Demo: Fundstelle sammeln, mit Werkzeug abbauen, Spur untersuchen (Wahrnehmungs-Probe), Gegner anklicken für den Kampf, Pfeil für das nächste Bild. Kein Spielcode, nur das Gefühl.</p>
<script>
const S = {bag: [], size: 6, clock: 4, frame: 1, fought: false};
const $ = id => document.getElementById(id);
function draw(){
  $("bag").innerHTML = Array.from({length:S.size}, (_, i) => `<div class="slot">${S.bag[i] || ""}</div>`).join("");
  $("bagc").textContent = S.bag.length + "/" + S.size;
  $("clock").innerHTML = Array.from({length:4}, (_, i) => `<div class="seg ${i < S.clock ? "" : "off"}"></div>`).join("");
  $("frame").textContent = S.frame;
}
function say(who, text, buttons){ $("who").textContent = who; $("txt").innerHTML = text; $("btns").innerHTML = "";
  (buttons || []).forEach(([label, fn, ghost]) => { const b = document.createElement("button"); b.className = "btn" + (ghost ? " ghost" : ""); b.textContent = label; b.onclick = fn; $("btns").appendChild(b); }); }
function take(icon, name, el){ if (S.bag.length >= S.size) return say("Tasche", "Die Tasche ist voll. Lass etwas zurück oder kehre an einem Rastplatz zur Yacht zurück.");
  S.bag.push(icon); el.classList.add("used"); draw(); say("Fund", `<b>${name}</b> eingesteckt.`); }
$("h_herb").onclick = e => take("🌿", "Wildkräuter ★★", e.currentTarget);
$("h_wood").onclick = e => { const el = e.currentTarget; say("Abbaustelle", "Eine abgestorbene Korkeiche. Mit der <b>Feuerwehraxt</b> ließe sich Hartholz schlagen.",
  [["Hacken (Feuerwehraxt)", () => take("🪵", "Hartholz", el)], ["Lassen", () => say("Erzähler", "Du lässt den Stamm stehen."), true]]); };
$("h_clue").onclick = e => { const el = e.currentTarget; const w = 1 + Math.floor(Math.random()*20), sum = w + 3;
  el.classList.add("used");
  if (sum >= 12) say("Spur · Wahrnehmung", `Wurf <span class="dice">${w} + 3 = ${sum}</span> gegen SG 12 – <b>Erfolg</b>.<br>Tiefe Krallenspuren an der Korkeiche, auf Brusthöhe. <i>Viel zu groß für einen Hund.</i> (Codex: „Etwas Großes ist in der Macchia“)`);
  else say("Spur · Wahrnehmung", `Wurf <span class="dice">${w} + 3 = ${sum}</span> gegen SG 12 – Fehlschlag. Nur zerkratzte Rinde. Wildschweine, vermutlich.`); };
$("enemy").onclick = () => { if (S.fought) return; say("Begegnung", 'Eine fette <b style="color:var(--green)">Ratte (Lv 1, Gefährlich)</b> versperrt den Pfad und faucht.',
  [["⚔️ Kämpfen", fight], ["💬 Verscheuchen (Mut-Probe)", () => { S.fought = true; $("enemy").classList.add("gone"); $("etag").style.display = "none"; say("Erzähler", "Du stampfst auf. Die Ratte flieht ins Gebüsch – keine Beute, keine Erfahrung."); }, true], ["🏃 Umgehen", () => say("Erzähler", "Du schleichst am Rand vorbei. Die Ratte lässt dich ziehen."), true]]); };
function fight(){ S.fought = true; say("Kampf", "→ Hier öffnet sich der Kampfbildschirm (Parade, Spezialangriffe, Zustände) …", [["Sieg simulieren", () => {
  $("enemy").classList.add("gone"); $("etag").style.display = "none"; say("Sieg", "Die Ratte ist besiegt. <b>+40 Erfahrung</b> (grün = 100 %).", []); }]]); }
$("next").onclick = () => { if (S.frame === 1) { S.frame = 2; S.clock = Math.max(0, S.clock - 1); draw();
  say("Erzähler", "Ein Bachlauf unter einer alten Steinbrücke. Im Wasser ziehen Forellen ihre Kreise. Am Ufer liegt eine tote Ziege – um ihren Hals ein Metallring, auf dem ein winziges rotes Licht blinkt.",
  [["🎣 Angeln (Flussfisch)", () => say("Angelplatz", "Hier startet das Angel-Minispiel (Reaktionsprobe wie die Parade). Seltene Fänge: ★★★-Forelle.")], ["🔍 Ring untersuchen", () => say("Spur", "Kein Hersteller, nur eine Seriennummer: <b>BCU-0417</b>. Du steckst den Ring ein (Missionsgegenstand, belegt keinen Taschenplatz).")], ["🔥 Rasten & zur Yacht", () => say("Rastplatz", "Du kehrst sicher zur Yacht zurück – mit allem in der Tasche. Die Spur-Uhr läuft weiter.", []), true]]); } };
draw();
</script></body></html>"""

if __name__ == "__main__":
    main()
