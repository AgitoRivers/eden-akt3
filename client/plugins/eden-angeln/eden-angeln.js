/* Fishing (27.10.2026, E-079). The engine (kern/angeln.py) decides what bites and books the catch; this plugin plays the cast:
     ready -> cast (Space) -> wait -> the float dips: strike in time (Space) -> reel:
     a dot bounces up and down a vertical bar; hit Space while it is inside the golden band (like a parry). 3-4 hits land the fish.
     The band shrinks all the time, a miss takes a slice more; when it is gone, the line snaps.
   Sends: angeln_wurf, angeln_ergebnis {gefangen, fehler, leicht, grund}, angeln_ende. Journal (J), Pack up (Esc), relaxed reel toggle.
   The overlay keeps its own state; redraws of the game never restart a cast. */
window.EdenAngeln = (function(){
  const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}[c]));
  const uiIc = (id, klasse) => window.EdenUI ? EdenUI.icon(id, klasse) : "";
  const FUND_ICON = {driftwood: "timber", rusty_chain: "steel", river_stones: "slate", old_branch: "leaf"};
  const STUFE_NAME = {0: "", 1: "common", 2: "uncommon", 3: "rare"};
  const merk = {lesen(k, d){ try { return localStorage.getItem(k) ?? d; } catch(e){ return d; } }, schreiben(k, v){ try { localStorage.setItem(k, v); } catch(e){} }};
  let S = null;            // {phase, aktiv, t0, raf, ...} for the running session
  let journalOffen = false, endeBis = 0, jWahl = null;
  let leicht = merk.lesen("eden_angeln_leicht", "0") === "1";

  const spiel = () => (typeof V !== "undefined" && V && V.z) || {};   // V: top-level let in index.html
  const sfx = id => { if (window.EdenSfx && EdenSfx.play) { try { EdenSfx.play(id); } catch(e){} } };
  const send = (aktion, daten) => (typeof senden === "function" ? senden(aktion, daten || {}, "…") : Promise.resolve());
  const $ = sel => document.querySelector("#angeln " + sel);

  // ---------------------------------------------------------------- circle next to the cabin (Duc 29.10.2026)
  // Fishing costs no time, like the cabin, so it sits as a round button left of "Cabin" instead of a choice card.
  // One spot: click starts. Several spots: click (or F) opens a small list. Badge = casts left; grey = nothing bites.
  function ortText(o){
    return o.rest ? `${o.rest} cast${o.rest > 1 ? "s" : ""} left` : `back in ${o.in_tagen} day${o.in_tagen === 1 ? "" : "s"}`;
  }
  // One round button, shared with the rest sites (eden-abbau). k = {bild, zahl, lab, zu, titel, klick, aria}; zu = grey and not clickable.
  function kreisKnopf(k){
    return `<button class="eakreis${k.zu ? " zu" : ""}" type="button" ${k.zu ? "disabled" : `onclick="${k.klick}"`}
        title="${esc(k.titel || "")}" aria-label="${esc(k.aria || "")}">
      <span class="bild" style="background-image:url('${esc(k.bild || "")}')"></span>${k.zahl ? `<i class="eakreis-zahl">${k.zahl}</i>` : ""}
      <span class="lab">${k.lab}</span></button>`;
  }
  function kreis(z){
    const orte = z && z.angel_orte;
    if (!orte || !orte.length) return "";
    const offen = orte.filter(o => o.rest), rest = offen.reduce((s, o) => s + o.rest, 0);
    const bild = (offen[0] || orte[0]).bild;
    const zu = !offen.length;
    const titel = orte.length === 1 ? `${orte[0].label} · ${ortText(orte[0])} · costs no time` : `Fishing · ${orte.length} spots · costs no time`;
    const liste = orte.length > 1 ? `<div class="eakreis-liste glas" hidden>${orte.map(o =>
      `<button type="button" ${o.rest ? `onclick="senden('angeln_start',{ort:'${esc(o.id)}'},'You fetch the rod …')"` : "disabled"}>
         <span class="bild" style="background-image:url('${esc(o.bild)}')"></span><span><b>${esc(o.label)}</b><small>${o.wasser === "meer" ? "sea" : "fresh water"} · ${ortText(o)}</small></span></button>`).join("")}</div>` : "";
    return `<div class="eakreis-wrap">${kreisKnopf({bild, zahl: rest, zu, klick: "EdenAngeln.kreisKlick()", aria: "Fishing",
      titel: zu ? "Nothing is biting right now" : titel,
      lab: zu ? esc(ortText(orte.reduce((a, b) => (a.in_tagen || 99) <= (b.in_tagen || 99) ? a : b))) : `Fishing <kbd>F</kbd>`})}${liste}</div>`;
  }
  function kreisKlick(){
    const z = spiel(), orte = (z.angel_orte || []).filter(o => o.rest);
    if (!orte.length || (typeof beschaeftigt !== "undefined" && beschaeftigt)) return;
    if ((z.angel_orte || []).length === 1){
      if (typeof senden === "function") senden("angeln_start", {ort: orte[0].id}, "You fetch the rod …");
      return;
    }
    const l = document.querySelector(".eakreis-liste");
    if (l) l.hidden = !l.hidden;
  }

  // ---------------------------------------------------------------- place cards on the choice screen
  // (until 29.10.2026; since then the circle above replaces them on the choice screen)
  function karten(z){
    const orte = z && z.angel_orte;
    if (!orte || !orte.length) return "";
    // Since 28.10.2026 fishing costs no time: the spot is empty after a few casts and grows back in a few days
    return orte.map(o => `<button class="karte glas option ea-karte${o.rest ? "" : " ea-zu"}" type="button"
        ${o.rest ? `onclick="senden('angeln_start',{ort:'${esc(o.id)}'},'You fetch the rod …')"` : "disabled"} title="${o.rest ? "" : "Nothing is biting here for now."}">
        <div class="bild" style="background-image:url('${esc(o.bild)}')"><span class="ea-karte-icon">${uiIc("fish", "imtext")}</span></div>
        <div class="txt"><h3>${esc(o.label)}</h3><small>fishing · ${o.wasser === "meer" ? "sea" : "fresh water"} · ${o.rest ? `${o.rest} cast${o.rest > 1 ? "s" : ""} left · no time` : `back in ${o.in_tagen} day${o.in_tagen === 1 ? "" : "s"}`}</small><p>${esc(o.text)}</p></div></button>`).join("");
  }

  // ---------------------------------------------------------------- overlay skeleton
  function geruest(a){
    const box = document.createElement("div");
    box.id = "angeln";
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-label", "Fishing");
    box.innerHTML = `
      <div class="ea-vignette"></div>
      <header class="ea-kopf glas">
        <div class="ea-ort"><small>${a.wasser === "meer" ? "Sea" : "River"}</small><b>${esc(a.label)}</b></div>
        <div class="ea-wuerfe" aria-label="Casts"></div>
        <div class="ea-knoepfe">
          <label class="ea-leicht" title="Slower dot, slower band. Catches give at most two stars."><input type="checkbox" ${leicht ? "checked" : ""}> Relaxed reel</label>
          <button type="button" class="ea-knopf" data-ea="journal"><kbd>J</kbd> Journal <span class="ea-jzahl"></span></button>
          <button type="button" class="ea-knopf ea-ende" data-ea="ende"><kbd>Esc</kbd> <span>Pack up</span></button>
        </div>
        <div class="ea-hinweis" aria-live="polite"></div>
      </header>
      <section class="ea-wasser" aria-hidden="true" data-zustand="bereit" style="--px:${a.pose[0]}%;--py:${a.pose[1]}%">
        <svg class="ea-leine" viewBox="0 0 100 100" preserveAspectRatio="none">${["rand", "faden"].map(k =>
          `<path class="${k}" d="M100,0 Q${(100 + a.pose[0]) / 2},${a.pose[1] * 0.25} ${a.pose[0]},${a.pose[1] - 3}" />`).join("")}</svg>
        <div class="ea-pose${a.koeder ? " ea-pose-koeder" : ""}"><i>${a.koeder ? `<img src="${esc(a.koeder.bild)}" alt="${esc(a.koeder.label)}">` : ""}</i></div>
        <div class="ea-welle"></div><div class="ea-welle w2"></div>
        <img class="ea-schatten" alt="">
      </section>
      <section class="ea-drill" aria-label="Reel">
        <div class="ea-drill-titel"></div>
        <div class="ea-pips"></div>
        <div class="ea-balken"><div class="ea-zone"></div><div class="ea-punkt"></div></div>
        <button type="button" class="ea-reel" data-ea="taste"><kbd>Space</kbd> Reel</button>
      </section>
      <div class="ea-karte-mitte glas"></div>
      <aside class="ea-journal glas" hidden></aside>`;
    box.addEventListener("click", e => {
      const b = e.target.closest("[data-ea]");
      if (b){ e.stopPropagation(); aktion(b.dataset.ea); return; }
      const f = e.target.closest("[data-fisch]");
      if (f){ e.stopPropagation(); jWahl = f.dataset.fisch; const a = spiel().angeln; if (a) journal(a); return; }
      if (e.target.closest(".ea-balken") || e.target.closest(".ea-wasser")) taste();
    });
    box.querySelector(".ea-leicht input").addEventListener("change", e => { leicht = e.target.checked; merk.schreiben("eden_angeln_leicht", leicht ? "1" : "0"); });
    document.getElementById("app").appendChild(box);
    return box;
  }

  function kopf(a){
    const pips = [];
    for (let i = 0; i < a.wuerfe; i++){
      const f = a.faenge[i];
      const weg = f && f.moewe === "weg";                    // the gull took it (29.10.2026)
      const k = !f ? (a.aktiv && a.aktiv.nr === i + 1 ? "jetzt" : "frei") : !f.ok || weg ? "fehl" : f.art === "fund" ? "fund" : "fisch";
      const t = !f ? "" : !f.ok ? uiIc("failed", "imtext") : weg ? uiIc("feather", "imtext") : f.art === "fund" ? (FUND_ICON[f.id] ? uiIc(FUND_ICON[f.id], "imtext") : "•") : uiIc("quality", "imtext").repeat(f.stern || 0);
      pips.push(`<span class="ea-wpip ${k}" title="Cast ${i + 1}">${t || (k === "jetzt" ? uiIc("fish", "imtext") : "")}</span>`);
    }
    $(".ea-wuerfe").innerHTML = pips.join("");
    $(".ea-jzahl").textContent = a.journal.gefangen + "/20";
  }

  function hinweis(html){
    const h = $(".ea-hinweis");
    if (!h) return;
    h.innerHTML = html;
    h.classList.toggle("an", !!html);
  }

  // ---------------------------------------------------------------- the middle card (ready, result, tutorial)
  function karteMitte(html, klasse){
    const k = $(".ea-karte-mitte");
    k.className = "ea-karte-mitte glas " + (klasse || "");
    k.innerHTML = html;
    k.hidden = !html;
  }
  function bereitZeigen(a){
    wasserZustand("bereit");
    const rest = a.wuerfe - a.wurf;
    const neu = merk.lesen("eden_angeln_tutorial", "0") !== "1";
    karteMitte(rest > 0 ? `<small>${rest} cast${rest > 1 ? "s" : ""} left</small><b>Cast your line</b>
        ${neu ? `<p class="ea-hilfe">Wait until the float dips, then <b>strike</b>. While you reel, a dot bounces up and down the bar:
          hit <kbd>Space</kbd> whenever it is inside the <span class="gold">golden band</span>. Three or four hits land the fish.
          A miss shrinks the band, and when the band is gone, the line snaps.</p>` : `<p>${esc(a.text)}</p>`}
        <button type="button" class="ea-gross" data-ea="taste"><kbd>Space</kbd> Cast</button>`
      : `<small>Nothing more is biting</small><b>That's it for this spot</b><p>${zusammenfassung(a)} The fish come back in a few days.</p>
        <button type="button" class="ea-gross" data-ea="ende"><kbd>Space</kbd> Pack up</button>`, "bereit");
  }
  function zusammenfassung(a){
    const ok = a.faenge.filter(f => f.ok).length;
    return ok ? `${ok} of ${a.faenge.length} casts landed something.` : "Nothing today. The sea doesn't hurry.";
  }
  function ergebnisZeigen(a, e){
    setTimeout(() => { if (S && S.phase === "ergebnis") wasserZustand("bereit"); }, 900);   // the splash first, then a calm deck
    const rest = a.voll ? 0 : a.wuerfe - a.wurf;             // bag full (stacking 28.10.2026): pack up
    const weiter = rest > 0 ? `<button type="button" class="ea-gross" data-ea="taste"><kbd>Space</kbd> Cast again <small>${rest} left</small></button>`
                            : `<button type="button" class="ea-gross" data-ea="ende"><kbd>Space</kbd> Pack up${a.voll ? ` <small>${uiIc("backpack", "imtext")} bag full</small>` : ""}</button>`;
    if (!e.ok){
      const T = {biss: ["bite", "Too slow – it spat the hook", "Strike the moment the float goes under."],
                 riss: ["snap", "The line snapped", "Hit while the dot is in the golden band, before the band shrinks away."],
                 abbruch: ["letgo", "You let it go", "Back into the water with it."]}[e.grund] || ["snap", "The line snapped", ""];
      karteMitte(`<div class="ea-fehl-icon">${uiIc(T[0], "imtext")}</div><b>${T[1]}</b><p>${T[2]}</p>${weiter}`, "fehl");
      return;
    }
    if (e.art === "fund"){
      karteMitte(`<div class="ea-fund-icon">${uiIc(FUND_ICON[e.id] || "package", "imtext")}</div><small>Something else on the hook</small><b>${esc(e.label)}</b>
        <p>${esc(e.text)}</p><div class="ea-plus">${e.rohstoffe.length ? `${e.rohstoffe.map(r => `+${r.n} ${esc(r.label)}`).join(" · ")} <small>${e.tasche ? "into your bag" : "for Nonna's sheds"}</small>` : ""}${(e.liegen || []).length ? ` <small>${uiIc("backpack", "imtext")} bag full · ${e.liegen.map(r => `${r.n} ${esc(r.label)}`).join(", ")} left in the water</small>` : ""}</div>${weiter}`, "fund");
      return;
    }
    if (e.moewe === "weg"){                                    // a gull snatched it and got away (29.10.2026)
      karteMitte(`<div class="ea-fehl-icon">${uiIc("feather", "imtext")}</div><small>${esc(e.label)}</small><b>The gull got away with it</b>
        <p>Still in your journal. The gull will remember this as a good day.</p>${weiter}`, "fehl");
      return;
    }
    const sterne = `<span class="ea-sterne">${uiIc("quality", "imtext").repeat(e.stern)}<i>${uiIc("quality", "imtext").repeat(3 - e.stern)}</i></span>`;
    karteMitte(`${e.neu ? `<span class="ea-neu">New in your journal</span>` : ""}
      <img class="ea-fang-bild" src="${esc(e.sprite)}" alt="${esc(e.label)}">
      <small>${STUFE_NAME[e.stufe]} · ${e.wasser === "meer" ? "sea" : "river"}</small><b>${esc(e.label)}</b>${sterne}
      <p class="ea-roh">${e.frei ? `${uiIc("backpack", "imtext")} No room in your bag. It slips back into the water.`
        : e.tasche ? `Into your bag: <b>${esc(e.roh)}</b> · the kitchen gets it when you're home` : `Into your pantry: <b>${esc(e.roh)}</b>`}</p>
      ${e.moewe === "zurueck" ? `<p class="ea-perfekt">${uiIc("feather", "imtext")} Won back from a gull.</p>` : e.stern === 3 ? `<p class="ea-perfekt">Clean reel – not a single miss.</p>` : ""}
      ${e.bonus ? `<div class="ea-bonus"><b>${esc(e.bonus.label)}</b><span>${esc(e.bonus.text)}</span></div>` : ""}${weiter}`, "fang");
  }

  // ---------------------------------------------------------------- journal
  function journal(a){
    const j = a.journal, el = $(".ea-journal");
    const teil = w => {
      const fs = j.fische.filter(f => f.wasser === w), n = fs.filter(f => f.n).length, b = j.boni.find(x => x.wasser === w);
      return `<section><h4>${w === "meer" ? "Sea" : "Fresh water"} <small>${n}/10</small></h4>
        <div class="ea-jbalken"><i style="width:${n * 10}%"></i></div>
        <div class="ea-jgitter">${fs.map(f => `<div class="ea-jfisch${f.n ? "" : " unbekannt"}${f.id === jWahl ? " gewaehlt" : ""}" ${f.n ? `data-fisch="${esc(f.id)}"` : ""} title="${esc(f.n ? f.text : "Not caught yet")}">
          <img src="${esc(f.sprite)}" alt=""><b>${f.n ? esc(f.label) : "???"}</b>
          <small>${"●".repeat(f.stufe)}${"○".repeat(3 - f.stufe)}${f.n ? ` · ×${f.n} · ${uiIc("quality", "imtext").repeat(f.bester)}` : ""}</small></div>`).join("")}</div>
        <p class="ea-jbonus${b.frei ? " frei" : ""}">${b.frei ? uiIc("done", "imtext") + " " : uiIc("locked", "imtext") + " All ten: "}<b>${esc(b.label)}</b>${b.frei ? " – the golden band stays wider." : ""}</p></section>`;
    };
    const w = j.fische.find(f => f.id === jWahl && f.n);          // notes of the chosen fish, with Petru's line after the first sale (28.10.2026)
    const notiz = w ? `<div class="ea-jnotiz"><b>${esc(w.label)}</b><p>${esc(w.text)}</p>
        <p class="ea-jpetru">${w.petru ? `<span>Petru:</span> “${esc(w.petru)}”` : "Ask Petru about it."}</p></div>`
      : (j.gefangen ? `<p class="ea-jnotiz leer">Click a fish you've caught for its notes.</p>` : "");
    el.innerHTML = `<header><b>Fish journal</b><small>${j.gefangen}/20</small><button type="button" class="ea-knopf" data-ea="journal">Close <kbd>J</kbd></button></header>${notiz}${teil("meer")}${teil("fluss")}`;
  }

  // ---------------------------------------------------------------- one cast: wait, bite, reel
  function wasserZustand(k){ const w = $(".ea-wasser"); if (w) w.dataset.zustand = k; }
  function warten(a){
    const akt = a.aktiv;
    S.phase = "warten";
    karteMitte("");
    wasserZustand("warten");
    $(".ea-drill").classList.remove("an");
    const schatten = $(".ea-schatten");
    if (akt.sprite){ schatten.src = akt.sprite; schatten.hidden = false; } else { schatten.hidden = true; schatten.removeAttribute("src"); }
    clearTimeout(S.timer);
    S.timer = setTimeout(() => {
      if (!S || S.phase !== "warten") return;
      S.phase = "biss";
      S.bissBis = performance.now() + akt.biss.fenster * 1000 * (leicht ? 1.4 : 1);
      wasserZustand("biss");
      sfx("angeln_biss");
      karteMitte(`<b class="ea-strike">Strike!</b><small><kbd>Space</kbd></small>`, "strike");
      S.timer = setTimeout(() => { if (S && S.phase === "biss") melden(false, 0, "biss"); }, akt.biss.fenster * 1000 * (leicht ? 1.4 : 1));
    }, akt.biss.warten * 1000);
  }
  function drillStart(a){
    const akt = a.aktiv;
    karteMitte("");
    S.phase = "drill";
    wasserZustand("drill");
    sfx("angeln_treffer");
    const lam = leicht ? 0.7 : 1;
    S.d = {y: akt.start, dir: Math.random() < 0.5 ? 1 : -1, tempo: akt.tempo * lam, zone: akt.zone, mitte: 0.5, treffer: 0, fehler: 0,
           noetig: akt.treffer, schwund: akt.schwund * lam, t: performance.now(), sperre: 0};
    S.d.mitte = neueMitte(S.d.zone, S.d.y);
    $(".ea-pips").innerHTML = Array.from({length: akt.treffer}, () => `<i></i>`).join("");
    const titel = $(".ea-drill-titel");
    titel.textContent = {0: "Something snagged …", 1: "A nibble!", 2: "Something strong!", 3: "Something BIG!"}[akt.stufe] || "Fish on!";
    titel.className = "ea-drill-titel s" + akt.stufe;
    $(".ea-drill").classList.add("an");
    cancelAnimationFrame(S.raf);
    S.raf = requestAnimationFrame(schritt);
  }
  function neueMitte(zone, y){
    // the band never starts right on the dot: at least a third of the bar away, always fully inside
    const h = zone / 2;
    for (let i = 0; i < 12; i++){
      const m = h + Math.random() * (1 - 2 * h);
      if (Math.abs(m - y) > 0.3) return m;
    }
    return y > 0.5 ? h : 1 - h;
  }
  function schritt(t){
    if (!S || S.phase !== "drill") return;
    const d = S.d, dt = Math.min(0.05, (t - d.t) / 1000);
    d.t = t;
    d.y += d.dir * d.tempo * dt;
    if (d.y > 1){ d.y = 2 - d.y; d.dir = -1; d.tempo *= 0.9 + Math.random() * 0.2; }
    if (d.y < 0){ d.y = -d.y; d.dir = 1; d.tempo *= 0.9 + Math.random() * 0.2; }
    d.zone -= d.schwund * dt;
    zeichneDrill();
    if (d.zone <= 0.015){ melden(false, d.fehler, "riss"); return; }
    S.raf = requestAnimationFrame(schritt);
  }
  function zeichneDrill(){
    const d = S.d, zone = $(".ea-zone"), punkt = $(".ea-punkt");
    zone.style.height = (Math.max(0, d.zone) * 100) + "%";
    zone.style.bottom = ((d.mitte - Math.max(0, d.zone) / 2) * 100) + "%";
    zone.classList.toggle("knapp", d.zone < 0.08);
    punkt.style.bottom = (d.y * 100) + "%";
    punkt.classList.toggle("drin", Math.abs(d.y - d.mitte) <= d.zone / 2);
    const leine = $(".ea-leine");          // the tighter the zone, the more the line strains (thicker, in px)
    if (leine) leine.style.setProperty("--spannung", (Math.min(1, (0.3 - Math.min(0.3, d.zone)) / 0.3)).toFixed(2));
  }
  function drillTaste(){
    const d = S.d, jetzt = performance.now();
    if (jetzt < d.sperre) return;
    d.sperre = jetzt + 140;
    if (Math.abs(d.y - d.mitte) <= d.zone / 2){
      d.treffer += 1;
      sfx("angeln_treffer");
      const pip = $(".ea-pips").children[d.treffer - 1];
      if (pip) pip.classList.add("voll");
      blitz("treffer");
      if (d.treffer >= d.noetig){ melden(true, d.fehler, ""); return; }
      d.tempo *= S.aktiv.tempo_je_treffer;
      d.mitte = neueMitte(d.zone, d.y);
    } else {
      d.fehler += 1;
      d.zone -= S.aktiv.fehler;
      sfx("angeln_fehl");
      blitz("fehl");
    }
  }
  function blitz(k){
    const b = $(".ea-balken");
    b.classList.remove("treffer", "fehl");
    void b.offsetWidth;
    b.classList.add(k);
  }
  async function melden(gefangen, fehler, grund){
    if (!S || S.phase === "melden") return;
    S.phase = "melden";
    cancelAnimationFrame(S.raf);
    clearTimeout(S.timer);
    wasserZustand(gefangen ? "fang" : grund === "riss" ? "riss" : "ruhig");
    sfx(gefangen ? "angeln_fang" : grund === "riss" ? "angeln_riss" : "angeln_fehl");
    $(".ea-drill").classList.remove("an");
    if (merk.lesen("eden_angeln_tutorial", "0") !== "1") merk.schreiben("eden_angeln_tutorial", "1");
    await send("angeln_ergebnis", {gefangen, fehler, leicht, grund});
    const a = spiel().angeln;
    if (!a || !S) return;
    S.phase = "ergebnis";
    S.aktivNr = null;
    ergebnisZeigen(a, a.faenge[a.faenge.length - 1]);
  }

  // ---------------------------------------------------------------- input
  function taste(){
    const a = spiel().angeln;
    if (!a || !S || (typeof beschaeftigt !== "undefined" && beschaeftigt)) return;
    if (S.phase === "bereit" || S.phase === "ergebnis"){
      if (a.wurf >= a.wuerfe || a.voll) return aktion("ende");
      S.phase = "wirft";
      sfx("angeln_wurf");
      wasserZustand("wurf");
      karteMitte("");
      send("angeln_wurf").then(() => { const n = spiel().angeln; if (n && n.aktiv && S){ S.aktiv = n.aktiv; S.aktivNr = n.aktiv.nr; kopf(n); warten(n); } });
      return;
    }
    if (S.phase === "warten"){                      // too early: the fish is scared off
      clearTimeout(S.timer);
      karteMitte(`<b>Too early</b><small>Wait for the float to go under.</small>`, "zufrueh");
      setTimeout(() => melden(false, 0, "biss"), 700);
      S.phase = "melden0";
      return;
    }
    if (S.phase === "biss"){ clearTimeout(S.timer); drillStart(a); return; }
    if (S.phase === "drill") drillTaste();
  }
  function aktion(k){
    const a = spiel().angeln;
    if (k === "taste") return taste();
    if (k === "journal"){
      if (!journalOffen && S && ["warten", "biss", "drill", "wirft"].includes(S.phase)) return;   // not while a fish is on the line
      journalOffen = !journalOffen;
      const el = $(".ea-journal");
      if (a) journal(a);
      el.hidden = !journalOffen;
      document.getElementById("angeln").classList.toggle("journal-auf", journalOffen);
      return;
    }
    if (k === "ende"){
      if (!a || !S) return;
      const amHaken = ["warten", "biss", "drill"].includes(S.phase);
      const frage = amHaken ? "The fish on the line gets away." : "";     // packing up costs nothing: what's left stays in the water
      const jetzt = performance.now();
      if (frage && jetzt > endeBis){                 // ask once: a second Esc or click within 3 seconds packs up
        endeBis = jetzt + 3000;
        hinweis(`Pack up? ${frage} <kbd>Esc</kbd> again`);
        const b = $(".ea-ende span"); if (b) b.textContent = "Sure? Click again";
        setTimeout(() => { if (performance.now() > endeBis){ const x = $(".ea-ende span"); if (x) x.textContent = "Pack up"; hinweis(""); } }, 3100);
        return;
      }
      endeBis = 0;
      hinweis("");
      if (amHaken) return melden(false, S.d ? S.d.fehler : 0, "abbruch").then(() => send("angeln_ende"));
      send("angeln_ende");
    }
  }
  document.addEventListener("keydown", e => {
    if (!document.getElementById("angeln") || (e.target && e.target.closest && e.target.closest("input, textarea"))) return;
    if (e.key === " " || e.key === "Enter"){ e.preventDefault(); e.stopPropagation(); taste(); }
    else if (e.key === "j" || e.key === "J"){ e.preventDefault(); e.stopPropagation(); aktion("journal"); }
    else if (e.key === "Escape"){ e.preventDefault(); e.stopPropagation(); if (journalOffen) aktion("journal"); else aktion("ende"); }
  }, true);

  // ---------------------------------------------------------------- sync with the game
  function update(z){
    const a = z && z.status === "angeln" && z.angeln;
    document.body.classList.toggle("angeln-modus", !!a);
    let box = document.getElementById("angeln");
    if (!a){
      if (box) box.remove();
      if (S){ cancelAnimationFrame(S.raf); clearTimeout(S.timer); }
      S = null; journalOffen = false;
      return;
    }
    const neu = !box;
    if (neu){ box = geruest(a); S = {phase: "bereit", raf: 0, timer: 0, aktiv: null, aktivNr: null}; }
    kopf(a);
    if (journalOffen) journal(a);
    if (neu){
      if (a.aktiv){ S.aktiv = a.aktiv; S.aktivNr = a.aktiv.nr; warten(a); }       // reload in the middle of a cast: the fish bites again
      else if (a.faenge.length){ S.phase = "ergebnis"; ergebnisZeigen(a, a.faenge[a.faenge.length - 1]); }
      else bereitZeigen(a);
    } else if (S.phase === "bereit") bereitZeigen(a);
  }
  return {karten, kreis, kreisKnopf, kreisKlick, update};
})();
