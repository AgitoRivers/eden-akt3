/* Table scene (27.10.2026, Cooking star 1): the first time Duc plates a person's favourite dish and she eats it whole.
   The engine (kern/tisch.py) puts the scene into z.tisch; this plugin shows it beat by beat - title card, plate, first bite,
   "your answer", two memories, consequences - with Continue (click, Enter, Space), Skip, and the figure's voiced lines
   (/api/zeile?id=tisch.<figure>.<0|1|2>). Nothing is decided here: Continue/Skip only end the scene (action tisch_fertig). */
window.EdenTisch = (function(){
  let st = {key: null, i: 0, gezeigt: -1, audio: null};
  const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}[c]));

  function stopp(){
    if (st.audio){ try { st.audio.pause(); } catch(e){} st.audio = null; }
  }
  function sprich(b){
    stopp();
    if (!b || b.art !== "rede" || !b.id || (typeof STIMME !== "undefined" && !STIMME)) return;
    const a = new Audio("/api/zeile?id=" + encodeURIComponent(b.id));
    st.audio = typeof mitTempo === "function" ? mitTempo(a) : a;
    st.audio.play().catch(() => {});
  }
  function karte(t, b, letzte){
    if (b.art === "titel"){
      const teile = String(b.titel || "").split(" · ");
      return `<div class="tisch-karte tisch-titel"><small>Favourite dish</small><b>${esc(teile[0] || b.label)}</b><span>${esc(teile[1] || "")}</span></div>`;
    }
    if (b.art === "folgen"){
      return `<div class="tisch-karte tisch-folgen"><small>${esc(b.titel)}</small><b>${esc(b.label || t.label)}</b>
        <ul>${(b.zeilen || []).map(x => `<li>${esc(x)}</li>`).join("")}</ul></div>`;
    }
    if (b.art === "rede"){
      return `<div class="tisch-karte tisch-rede"><small>${esc(t.name)}</small><p>“${esc(b.text)}”</p></div>`;
    }
    return `<div class="tisch-karte tisch-text"><p>${esc(b.text)}</p></div>`;          // plate / "your answer": narrator text
  }
  function zeichne(t){
    let box = document.getElementById("tisch");
    if (!box){
      box = document.createElement("div"); box.id = "tisch"; box.setAttribute("role", "dialog"); box.setAttribute("aria-label", "Table scene");
      box.addEventListener("click", e => {
        if (e.target.closest("[data-tisch-skip]")) return ueberspringen();
        weiter();
      });
      document.getElementById("app").appendChild(box);
    }
    const b = t.beats[st.i], letzte = st.i === t.beats.length - 1;
    box.className = "tisch-" + b.art;
    box.innerHTML = `${b.sprite ? `<img class="tisch-figur" src="${esc(b.sprite)}" alt="">` : ""}
      ${karte(t, b, letzte)}
      <button class="tisch-skip knopf leise" type="button" data-tisch-skip>Skip</button>
      <div class="tisch-weiter"><kbd>Enter</kbd> ${letzte ? "Continue" : "Next"} · ${st.i + 1}/${t.beats.length}</div>`;
    st.gezeigt = st.i;
    sprich(b);
  }
  function weiter(){
    const t = V && V.z && V.z.tisch;
    if (!t) return;
    if (st.i < t.beats.length - 1){ st.i++; zeichne(t); }
    else ueberspringen();
  }
  function ueberspringen(){
    stopp();
    const box = document.getElementById("tisch"); if (box) box.remove();
    st = {key: null, i: 0, gezeigt: -1, audio: null};
    if (typeof senden === "function") senden("tisch_fertig", {}, "…");
  }
  function update(z){
    const t = z && z.tisch;
    if (!t){
      const box = document.getElementById("tisch");
      if (box) box.remove();
      if (st.key){ stopp(); st = {key: null, i: 0, gezeigt: -1, audio: null}; }
      return;
    }
    const key = t.pid + "|" + t.item;
    if (st.key !== key) st = {key, i: 0, gezeigt: -1, audio: null};
    if (st.gezeigt !== st.i || !document.getElementById("tisch")) zeichne(t);       // redraws of the game must not replay the beat
  }
  document.addEventListener("keydown", e => {
    if (!document.getElementById("tisch") || (e.target && e.target.closest && e.target.closest("input, textarea"))) return;
    if (e.key === "Enter" || e.key === " " || e.key === "ArrowRight"){ e.preventDefault(); e.stopPropagation(); weiter(); }
  }, true);
  return {update};
})();
