// Gemeinsame Bausteine der Oberflaeche (Duc 30.10.2026, Regeln: docs/wiki/systeme/ui_stil.md).
// EdenUI.icon("name") = Icon aus dem Woerterbuch (werkzeuge/ui_icons.py), EdenUI.icon("name", "klein") = in Text und Pillen. EdenUI.status(box, werte, {spiel, namen}) = Status-Knoepfe
// mit Infokarte und Rueckmeldung. werte: [{key, label, kurz, wort, icon, wert, min, max, niedrig, info}].
window.EdenUI = (() => {
  const SPRITE = (window.EDEN_UI_SPRITE || "/plugins/eden-ui/icons.svg") + "?v=10";
  let quelle = SPRITE;        // bis der Sprite im Dokument liegt, sonst leer: Neuzeichnen laedt dann nichts nach und nichts blinkt
  document.addEventListener("DOMContentLoaded", async () => {
    try {
      const t = await (await fetch(SPRITE)).text();
      const h = document.createElement("div");
      h.style.cssText = "position:absolute;width:0;height:0;overflow:hidden";
      h.setAttribute("aria-hidden", "true");
      h.innerHTML = t;
      if (!h.querySelector("symbol")) return;
      document.body.prepend(h);
      quelle = "";
      document.querySelectorAll("use").forEach(u => { const a = u.getAttribute("href") || ""; if (a.includes("icons.svg")) u.setAttribute("href", a.slice(a.indexOf("#"))); });
    } catch (_) {}
  });
  const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
  const icon = (id, klasse = "") => `<svg class="ui-ic ${klasse}" aria-hidden="true"><use href="${quelle}#${esc(id)}"></use></svg>`;
  const anteil = w => w.max > w.min ? Math.round(100 * (w.wert - w.min) / (w.max - w.min)) : 0;
  const zustaende = new Set();

  function karteZeichnen(box, st){
    let k = box.querySelector(":scope > .ui-infokarte");
    if (!st.offen){ if (k) k.remove(); return; }
    if (!k){ k = document.createElement("div"); k.className = "ui-infokarte"; k.setAttribute("role", "dialog"); box.appendChild(k); }
    k.setAttribute("aria-label", "Status");
    k.innerHTML = st.werte.map(w => `<button type="button" class="ui-zeile${w.niedrig ? " niedrig" : ""}" data-k="${esc(w.key)}">${icon(w.icon)}<span>${esc(w.label)}</span><em>${esc(w.wort)}</em></button>
      ${st.offen === w.key ? `<div class="ui-mehr"><div class="ui-balken"><i style="width:${anteil(w)}%"></i></div><p>${esc(w.info)}</p></div>` : ""}`).join("");
  }
  function umschalten(box, st, key){
    st.offen = st.offen === key ? null : key;
    box.querySelectorAll(":scope > .ui-status").forEach(b => b.setAttribute("aria-expanded", String(st.offen === b.dataset.k)));
    karteZeichnen(box, st);
  }
  function melden(box, w, diff){
    const b = box.querySelector(`:scope > .ui-status[data-k="${w.key}"]`);
    if (!b) return;
    b.classList.remove("puls"); void b.offsetWidth; b.classList.add("puls");
    const z = document.createElement("span");
    z.className = "ui-delta " + (diff > 0 ? "plus" : "minus");
    z.textContent = (diff > 0 ? "+" : "−") + Math.abs(diff);
    z.addEventListener("animationend", () => z.remove());
    b.appendChild(z);
    box.querySelectorAll(":scope > .ui-wertmeldung").forEach(x => x.remove());
    const t = document.createElement("div");
    t.className = "ui-wertmeldung"; t.setAttribute("role", "status");
    t.textContent = `${w.label}: ${w.wort}`;
    box.appendChild(t);
    setTimeout(() => t.remove(), 2000);
  }
  function status(box, werte, opt = {}){
    let st = box._uiStatus;
    if (!st){
      st = box._uiStatus = {offen: null, vorher: {}, spiel: undefined, werte: []};
      zustaende.add({box, st});
      box.classList.add("ui-statusleiste");
      box.addEventListener("click", e => {
        const b = e.target.closest(".ui-status,.ui-zeile");
        if (!b) return;
        if (b.classList.contains("ui-zeile")) st.offen = null;      // Zeile der Karte: dieselbe Logik wie ein Knopf
        umschalten(box, st, b.dataset.k);
      });
    }
    const neuesSpiel = st.spiel !== opt.spiel;
    st.spiel = opt.spiel; st.werte = werte;
    box.classList.toggle("mit-namen", !!opt.namen);
    if (st.offen && !werte.some(w => w.key === st.offen)) st.offen = null;
    const reihe = werte.map(w => w.key).join();
    if (box.dataset.reihe !== reihe){
      box.querySelectorAll(":scope > .ui-status").forEach(b => b.remove());
      box.insertAdjacentHTML("afterbegin", werte.map(w => `<button type="button" class="ui-status" data-k="${esc(w.key)}"><span class="ui-ring"><svg class="ui-ic" aria-hidden="true"><use></use></svg></span><span class="ui-name"></span></button>`).join(""));
      box.dataset.reihe = reihe;
    }
    werte.forEach(w => {
      const b = box.querySelector(`:scope > .ui-status[data-k="${w.key}"]`);
      b.classList.toggle("niedrig", !!w.niedrig);
      b.title = w.label;
      b.setAttribute("aria-label", `${w.label}: ${w.wort}`);
      b.setAttribute("aria-expanded", String(st.offen === w.key));
      b.querySelector(".ui-ring").style.setProperty("--ui-p", anteil(w));
      b.querySelector("use").setAttribute("href", `${quelle}#${w.icon}`);
      b.querySelector(".ui-name").textContent = w.kurz || w.label;
      const alt = st.vorher[w.key];
      if (!neuesSpiel && alt !== undefined && alt !== w.wert) melden(box, w, w.wert - alt);
      st.vorher[w.key] = w.wert;
    });
    karteZeichnen(box, st);
  }
  function alleSchliessen(ausser){
    let zu = false;
    zustaende.forEach(({box, st}) => {
      if (st.offen && box !== ausser){ umschalten(box, st, null); zu = true; }
    });
    return zu;
  }
  document.addEventListener("click", e => {
    const pfad = e.composedPath();                   // nicht contains: das Neuzeichnen kann das Ziel schon entfernt haben
    alleSchliessen([...zustaende].map(z => z.box).find(b => pfad.includes(b)));
  });
  // Vor dem Spiel-Handler (Esc = Menue): Eine offene Karte schliesst zuerst.
  document.addEventListener("keydown", e => {
    if (e.key === "Escape" && alleSchliessen()){ e.preventDefault(); e.stopImmediatePropagation(); }
  }, true);
  window.uiIc = icon;        // fuer alle Plugins: uiIc("name", "klein" oder "imtext")
  // Emoji aus Servertexten werden an dieser einen Stelle zu Icons. Der Handy-Chat bleibt, dort tippen die Figuren selbst.
  const EMOJI = {"📱": "phone", "📞": "phone", "🎣": "fish", "🐟": "fish", "🌿": "leaf", "🍳": "cooking", "🛏": "bunk", "🔎": "investigate", "🔍": "investigate", "📜": "rule",
    "🎒": "backpack", "🚩": "travel", "🔥": "burn", "⚔": "fight", "🗡": "fight", "🪓": "axe", "⛏": "pick", "🔨": "pick", "★": "quality", "⚖": "confront", "⚠": "warning",
    "🎁": "gift", "⚡": "energy", "🤝": "trade", "💬": "talk", "🗣": "talk", "🧸": "charm", "👂": "listen", "💔": "dislike", "📌": "secure", "💭": "memory", "📅": "calendar",
    "✓": "done", "✔": "done", "✕": "failed", "✗": "failed", "⏳": "deadline", "⏱": "time", "⏰": "time", "🎭": "gag", "♥": "love", "♡": "love", "📣": "order", "🧩": "compare",
    "😵": "stunned", "🏃": "dodge", "🎶": "music", "🛡": "guard"};
  const EMOJI_RE = new RegExp(Object.keys(EMOJI).join("|"), "u");
  const EMOJI_ALLE = new RegExp("(" + Object.keys(EMOJI).join("|") + ")️?", "gu");
  const NICHT = "script,style,textarea,input,svg,.geraet";
  function emojiErsetzen(wurzel){
    const lauf = document.createTreeWalker(wurzel, NodeFilter.SHOW_TEXT), treffer = [];
    while (lauf.nextNode()) if (EMOJI_RE.test(lauf.currentNode.nodeValue) && !lauf.currentNode.parentElement?.closest(NICHT)) treffer.push(lauf.currentNode);
    treffer.forEach(k => {
      const f = document.createElement("template");
      f.innerHTML = esc(k.nodeValue).replace(EMOJI_ALLE, (_, e) => icon(EMOJI[e], "imtext"));
      k.replaceWith(f.content);
    });
  }
  let wartet = false;
  const beobachter = new MutationObserver(() => {
    if (wartet) return;
    wartet = true;
    queueMicrotask(() => { wartet = false; if (document.body) emojiErsetzen(document.body); });
  });
  document.addEventListener("DOMContentLoaded", () => { emojiErsetzen(document.body); beobachter.observe(document.body, {childList: true, subtree: true, characterData: true}); });
  return {icon, status, emojiErsetzen};
})();
