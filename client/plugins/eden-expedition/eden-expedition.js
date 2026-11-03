/* Expedition screen (26.10.2026, Duc + Brain Trust, mockup docs/abnahme/expedition_mockup): frames of a location chapter
   (event art "ort", e.g. the Kloster) as one immersive screen. Place name as a title card when a frame opens, a small
   minimap that only shows what Duc has seen, Duc's state + loot bag, the text card with choices that say what follows
   (fight - who only with the Scout chip -, test, end of the trip), foldable interface (H).
   Data: z.ereignis (options with .exp from eden.py/kern/expedition.wahl_info), z.ort_weg, z.kampf_profil, z.expedition.
   Choices use the client's evWahl(i); number keys are handled by the client. */
(function(){
  "use strict";
  const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}[c]));
  const ATTR = {charm: "Charm", empathy: "Empathy", perception: "Perception", cunning: "Cunning", courage: "Courage", strength: "Strength"};
  const LOOK = {jacket_earth: "Erde", jacket_water: "Wasser", jacket_fire: "Feuer", jacket_air: "Luft", cyber_armor: "Cyber"};
  const KLASSE = {bat: "Bat", sword: "Sword", knife: "Knife", spear: "Spear", gun: "Gun", mop: "Mop"};
  // Kopfzeile je Ortskapitel (29.10.2026, Spieltest: die Grotte stand unter "San Martinu")
  const ORT = {kloster: "San Martinu", berge: "The Mountains", grotte: "Punta d'Orsu", grotte_flut: "Punta d'Orsu · High Tide"};
  let zuletzt = null;                                        // last frame id: title card only when a new frame opens
  let hudAus = false;
  let figurenZuletzt = "";                                   // who stood in the last drawn frame
  const fundGesehen = {};                                    // discovery card shown once per frame visit
  function fundZu(id){ fundGesehen[id] = true; const f = document.querySelector(".exp-fund"); if (f) f.remove(); }
  try { hudAus = localStorage.getItem("eden.exp.hud") === "aus"; } catch (e) {}

  function portraet(kp){
    if (!kp) return null;
    const look = LOOK[(kp.ruestung || {}).id] || "Erde";
    let w = KLASSE[(kp.waffe || {}).id] || "Bat";
    if (w === "Mop" && look !== "Erde") w = "Bat";
    return "/charakterbild/Duc" + look + w;
  }
  function karteMini(z, e){
    const weg = (z.ort_weg || []).filter(x => x.titel);
    const punkte = weg.map((x, i) => `<span class="exp-p ${i === weg.length - 1 ? "hier" : "war"}${x.rast ? " feuer" : ""}${x.geruht ? " geruht" : ""}" title="${esc(x.titel)}${x.rast ? " · rest site" : ""}">${x.rast ? uiIc("campfire", "imtext") : i === weg.length - 1 ? "●" : ""}</span>`);
    const weiter = (e.optionen || []).some(o => o.exp && o.exp.weiter);
    if (weiter) punkte.push(`<span class="exp-p nebel" title="Unknown">?</span>`);
    return punkte.join(`<span class="exp-s"></span>`).replace(/<span class="exp-s"><\/span>(<span class="exp-p nebel")/, `<span class="exp-s nebel"></span>$1`);
  }
  function folge(o, ruhig){
    const x = o.exp || {};
    if (x.kampf && ruhig) return `<span class="exp-folge exp-ruhig">${uiIc("leaf", "imtext")} Quiet · beaten until you rest</span>`;
    if (x.kampf){
      const k = x.kampf;
      const kopf = k.bekannt && k.bild ? `<span class="exp-kopfbild" style="background-image:url('${esc(k.bild)}')"></span>` : `<span class="exp-kopfbild">?</span>`;
      const wer = k.bekannt ? esc(k.name) : "Something is waiting";
      const lv = k.level != null ? ` <span class="exp-bedr ${esc((k.bedrohung || {}).id)}">Lv ${k.level} · ${esc((k.bedrohung || {}).label)}</span>` : "";
      const nur = x.kampf_nur_fehlschlag ? ` <span class="exp-leise">if it fails</span>` : "";
      return `<span class="exp-folge exp-kampf">${kopf}${uiIc("fight", "imtext")} ${wer}${lv}${nur}</span>`;
    }
    if (x.ende) return `<span class="exp-folge exp-wegpille">↩ Ends the trip · the phase is gone</span>`;
    return "";
  }
  // Chase them off (Duc 02.11.2026, like EarthBound): enemies clearly below Duc run from him. One click, half the xp, no loot.
  // The server decides (kern/kampf.verjagbar); the choice itself is the same option with "verjagen".
  function verjagenHtml(o, i, ruhig){
    if (!(o.exp || {}).verjagbar || ruhig) return "";
    return `<button class="exp-wahl exp-verjagen" type="button" onclick="EdenExpedition.verjagen(${i})" ${typeof beschaeftigt !== "undefined" && beschaeftigt ? "disabled" : ""}>
      <span class="exp-taste">${uiIc("onfoot", "imtext")}</span><span class="exp-wtext">Chase them off</span><span class="exp-folgen"><span class="exp-folge exp-wegpille">no fight · half XP · no loot</span></span></button>`;
  }
  function verjagen(i){ if (typeof senden === "function") senden("event_wahl", {index: i, verjagen: true}, "…"); }
  // Fast travel (Duc + Brain Trust 29.10.2026, like the flags in Clair Obscur): at the entrance "on foot" or straight to a
  // camp found on an earlier visit; at a camp on to another one. A moment, not a menu - cards with the camp's picture,
  // and what the jump skips. Server: kern/wegpunkte.py, action ort_reisen.
  function reisenHtml(r){
    if (!r || !(r.ziele || []).length) return "";
    const eingang = r.von === "eingang";
    const karten = r.ziele.map(w => `<button class="exp-reise" type="button" onclick="EdenExpedition.reisen('${esc(w.id)}')"
        ${typeof beschaeftigt !== "undefined" && beschaeftigt ? "disabled" : ""}>
        <span class="exp-reise-bild" ${w.bild ? `style="background-image:url('${esc(w.bild)}')"` : ""}></span>
        <span class="exp-reise-text"><b>${uiIc("campfire", "imtext")} ${esc(w.titel)}</b><small>${eingang
          ? (w.kaempfe ? `skips ${w.kaempfe} fight${w.kaempfe > 1 ? "s" : ""} on the way` : "no fights on the way")
          : "travel there"}</small></span></button>`).join("");
    return `<div class="exp-reisen ${eingang ? "eingang" : "rast"}">
      <div class="exp-reisen-kopf">${uiIc("travel", "imtext")} ${eingang ? "Or travel" : "Travel to another camp"}<small>${eingang
        ? "Your old trail markers are still there." : "Nothing heals on the way. Rest first, if you need it."}</small></div>
      <div class="exp-reisen-karten">${karten}</div></div>`;
  }
  function reisen(id){ if (typeof senden === "function") senden("ort_reisen", {id}, "…"); }
  function probe(o){
    return o.probe ? `<span class="exp-folge exp-probe">${uiIc("dice", "imtext")} ${esc(ATTR[o.probe.attribut] || o.probe.attribut)} ${esc(o.probe.sg)}</span>` : "";
  }
  // Figures of the frame (Duc 29.10.2026: Casanova was invisible in her own office). The engine sends them in
  // e.rollen with sprite and mood; whoever speaks stands in front, the others a little behind. After a choice the
  // answering figure shows the mood of her answer.
  function figuren(e){
    const R = e.rollen || {}, seen = new Set(), list = [];
    [R.handelnd, R.sprecher, R.links, R.rechts, R.pid, R.gegner, ...(R.betroffen || [])].forEach(f => {
      if (f && f.sprite && !seen.has(f.id)) { seen.add(f.id); list.push(Object.assign({}, f)); }
    });
    if (!list.length) return "";
    const antwort = e.ergebnis && e.ergebnis.zeile;
    const sprechen = new Set(antwort ? [antwort.wer] : (e.zeilen || []).map(l => l.wer));
    list.forEach(f => { if (antwort && antwort.wer === f.id && antwort.sprite) f.sprite = antwort.sprite; });
    const shown = list.slice(0, 4);
    // fade in only when someone new steps in: every redraw builds the images anew and made the figure see-through again
    const wer = shown.map(f => f.id).join();
    const ein = wer !== figurenZuletzt ? " ein" : "";
    figurenZuletzt = wer;
    // the scene card moves to the left (class exp-mit-figuren), the figures stand in the right third
    const pos = {1: [77], 2: [70, 87], 3: [66, 79, 92], 4: [64, 75, 86, 97]}[shown.length];
    return `<div class="exp-figuren n${shown.length}" aria-hidden="true">${shown.map((f, i) =>
      `<img class="exp-figur${ein}${sprechen.has(f.id) ? " spricht" : ""}" src="${esc(f.sprite)}" alt="" style="left:${pos[i]}%">`).join("")}</div>`;
  }
  let flottOffen = null;
  function html(z){
    const e = z.ereignis, kp = z.kampf_profil || {};
    const neu = e.id !== zuletzt;
    zuletzt = e.id;
    document.body.classList.add("exp-modus");
    document.body.classList.toggle("exp-hud-aus", hudAus);
    // visual-novel frames (The Long Table, Duc 30.10.2026): no "Your answer" step, straight to the next frame
    if (e.flott && e.ergebnis){
      if (flottOffen !== e.id){ flottOffen = e.id; setTimeout(evWeiter, 0); }
      return `<div class="exp" style="${e.bild ? `background-image:url('${esc(e.bild)}')` : ""}"></div>`;
    }
    flottOffen = null;
    // warning before a choice with lasting consequences (The Long Table, Duc 30.10.2026)
    if (e.warnung && !e.ergebnis) return `<div class="exp exp-warnung" style="${e.bild ? `background-image:url('${esc(e.bild)}')` : ""}">
      <section class="exp-karte exp-warnkarte glas" role="alertdialog" aria-label="${esc(e.titel)}"><h2>${esc(e.titel)}</h2><p>${esc(e.lage)}</p>
        <div class="exp-wahlen">${e.optionen.map((o, i) => `<button class="exp-wahl" type="button" onclick="evWahl(${i})"><span class="exp-taste">${i + 1}</span><span class="exp-wtext">${esc(o.text)}</span></button>`).join("")}</div></section></div>`;
    const bild = portraet(kp);
    const lp = kp.lp != null ? kp.lp : kp.lp_max, lpMax = kp.lp_max || 1;
    const beute = ((z.expedition || {}).beute || []);
    // vor dem ersten Schritt gibt es noch keine Expedition: dann am Frame-Praefix erkennen
    const PRAEFIX = {kl: "kloster", bg: "berge", gr: "grotte", fn: "grotte_flut"};
    const ort = ORT[(z.expedition || {}).id] || ORT[PRAEFIX[String(e.id || "").split("_")[0]]] || "";
    const zeilen = (e.zeilen || []).map(l => `<p class="exp-zeile"><b>${esc(l.name)}</b> ${esc(l.text)}</p>`).join("");
    const figs = figuren(e);
    const unterwegs = !!z.expedition;                     // no way map and no loot before the trip has begun (Duc 01.11.2026)
    const lpProzent = Math.max(0, Math.min(100, 100 * lp / lpMax));
    return `<div class="exp${figs ? " exp-mit-figuren" : ""}" style="${e.bild ? `background-image:url('${esc(e.bild)}')` : ""}">
      ${figs}
      ${neu ? `<div class="exp-titel" aria-hidden="true"><small>${esc(ort)}</small><b>${esc(e.titel)}</b></div>` : ""}
      <section class="exp-ort glas exp-hud" aria-label="Location"><small>${esc(ort)}</small><div class="exp-ortname">${esc(e.titel)}</div>
        ${unterwegs ? `<div class="exp-mini" aria-label="What you have seen of the way">${karteMini(z, e)}</div>` : ""}
        ${figs && lp < lpMax ? `<div class="exp-ort-leben" aria-label="Life">${uiIc("hp", "imtext")}<span class="exp-bar"><i style="width:${lpProzent}%"></i></span><span class="zahl">${esc(lp)}/${esc(lpMax)}</span></div>` : ""}
        ${e.spur ? `<div class="exp-spur">${uiIc("deadline", "imtext")} ${esc(e.spur.label || "")} ${esc(e.spur.wert)}/${esc(e.spur.segmente)}</div>` : ""}</section>
      ${figs ? "" : `<section class="exp-duc glas exp-hud" aria-label="Duc">
        <div class="exp-portrait" ${bild ? `style="background-image:url('${esc(bild)}')"` : ""} role="img" aria-label="Duc"></div>
        <div class="exp-kopf"><b>Duc</b><span>Lv ${esc(kp.level || 1)}${kp.waffe ? " · " + esc(kp.waffe.label) : ""}</span></div>
        <div class="exp-balken"><span class="exp-lbl">Life</span><span class="exp-bar"><i style="width:${lpProzent}%"></i></span><span class="zahl">${esc(lp)}/${esc(lpMax)}</span></div>
        <div class="exp-balken"><span class="exp-lbl">Stamina</span><span class="exp-pips">${"<i></i>".repeat(kp.ausdauer || 0)}</span></div>
        ${unterwegs ? `<div class="exp-tasche"><span>${uiIc("backpack", "imtext")} Found on the way</span><span class="exp-pillen">${beute.length ? beute.map(b => `<span class="exp-pille">${esc(b.label)}</span>`).join("") : `<span class="exp-pille">nothing yet</span>`}</span></div>` : ""}
      </section>`}
      ${e.rast && window.EdenAbbau ? EdenAbbau.quellenHtml(e) : ""}
      ${e.tier_bild ? `<img class="exp-tier" src="${esc(e.tier_bild)}" alt="">` : ""}
      <section class="exp-karte glas" aria-label="Scene">
        ${e.ergebnis && typeof evErgebnis === "function" ? `<p class="exp-lage">${esc(e.lage)}</p>${evErgebnis(e)}` : `<p class="exp-lage">${esc(e.lage)}</p>${zeilen}
        ${e.reisen && e.reisen.von === "eingang" ? `<div class="exp-reisen-kopf exp-zufuss">${uiIc("onfoot", "imtext")} On foot</div>` : ""}
        <div class="exp-wahlen">${(e.optionen || []).map((o, i) => `<button class="exp-wahl" type="button" onclick="evWahl(${i})" ${typeof beschaeftigt !== "undefined" && beschaeftigt ? "disabled" : ""}>
          <span class="exp-taste">${i + 1}</span><span class="exp-wtext">${esc(o.text)}</span><span class="exp-folgen">${probe(o)}${folge(o, e.ruhig)}</span></button>${verjagenHtml(o, i, e.ruhig)}`).join("")}
          ${e.rast ? `<button class="exp-wahl exp-rast" type="button" onclick="senden('ort_rasten',{},'…')"><span class="exp-taste">R</span><span class="exp-wtext">Rest by the fire</span><span class="exp-folgen"><span class="exp-folge exp-feuer">${uiIc("campfire", "imtext")} Full HP · the animals on the path come back</span></span></button>` : ""}
          ${e.zurueck ? `<button class="exp-wahl exp-zurueck" type="button" onclick="senden('ort_zurueck',{},'…')"><span class="exp-taste">B</span><span class="exp-wtext">Go back to ${esc(e.zurueck)}</span><span class="exp-folgen"><span class="exp-folge exp-wegpille">← one step back</span></span></button>` : ""}</div>
        ${reisenHtml(e.reisen)}`}
      </section>
      <button class="exp-hudknopf glas" type="button" onclick="EdenExpedition.hud()" aria-label="Fold the interface away"><kbd>H</kbd> <span>${hudAus ? "Show interface" : "Hide interface"}</span></button>
      ${anruf(z.rast_anruf)}
      ${e.fund && !fundGesehen[e.id] && !z.rast_anruf ? `<div class="exp-fund" onclick="EdenExpedition.fundZu('${esc(e.id)}')"><div class="exp-fund-karte">
        <small>${uiIc("campfire", "imtext")} A place to rest</small><p>${esc(e.fund)}</p><span class="exp-fund-weiter">click to continue</span></div></div>` : ""}
    </div>`;
  }
  let anrufStimme = {id: null, audio: null};
  function anrufSprechen(a){                            // the call is voiced (rast.<pid>.<level>.<n>), once per call
    if (!a || anrufStimme.id === a.id) return;
    if (anrufStimme.audio) anrufStimme.audio.pause();
    const au = new Audio("/api/zeile?id=" + encodeURIComponent("rast." + a.id));
    anrufStimme = {id: a.id, audio: typeof mitTempo === "function" ? mitTempo(au) : au};
    anrufStimme.audio.play().catch(() => {});
  }
  function anrufAntwort(i){
    if (anrufStimme.audio) anrufStimme.audio.pause();
    senden("rast_antwort", {index: i}, "…");
  }
  function anruf(a){                                    // rest call on the smartphone (26.10.2026, Duc: like the phone overlay)
    if (!a) { if (anrufStimme.audio) anrufStimme.audio.pause(); anrufStimme = {id: null, audio: null}; return ""; }
    setTimeout(() => anrufSprechen(a), 0);
    return `<div class="exp-anruf" role="dialog" aria-label="Call from ${esc(a.name)}"><div class="geraet exp-geraet"><div class="scr"><div class="insel"></div>
      <div class="exp-anruf-karte">
        <span class="exp-anruf-live">${uiIc("phone", "imtext")} INCOMING CALL · ON BOARD</span>
        <div class="exp-anruf-bild" ${a.sprite ? `style="background-image:url('${esc(a.sprite)}');${ausschnittStil(ausschnittFuer(a.sprite))}"` : ""}></div>
        <b class="exp-anruf-name">${esc(a.name)}</b>
        <div class="hb sie exp-anruf-text">${esc(a.text)}</div>
        <div class="exp-anruf-wahl">${(a.antworten || []).map((x, i) => `<button type="button" onclick="EdenExpedition.anrufAntwort(${i})"><kbd>${i + 1}</kbd>${esc(x.text)}</button>`).join("")}</div>
      </div></div></div></div>`;
  }
  function hud(){
    hudAus = !hudAus;
    try { localStorage.setItem("eden.exp.hud", hudAus ? "aus" : "an"); } catch (e) {}
    document.body.classList.toggle("exp-hud-aus", hudAus);
    const t = document.querySelector(".exp-hudknopf span");
    if (t) t.textContent = hudAus ? "Show interface" : "Hide interface";
  }
  document.addEventListener("keydown", ev => {
    if (!document.querySelector(".exp") || /TEXTAREA|INPUT/.test(ev.target.tagName)) return;
    const k = ev.key.toLowerCase(), z = typeof V !== "undefined" && V && V.z;
    if (z && z.rast_anruf && /^[12]$/.test(k)){ ev.preventDefault(); ev.stopImmediatePropagation(); anrufAntwort(+k - 1); return; }
    if (k === "h"){ ev.preventDefault(); hud(); }
    else if (k === "r" && z && z.ereignis && z.ereignis.rast && !z.ereignis.ergebnis){ ev.preventDefault(); senden("ort_rasten", {}, "…"); }
    else if (k === "b" && z && z.ereignis && z.ereignis.zurueck && !z.ereignis.ergebnis){ ev.preventDefault(); senden("ort_zurueck", {}, "…"); }
  }, true);
  // leave expedition mode as soon as another screen is drawn
  const aufraeumen = () => { if (!document.querySelector(".exp")) document.body.classList.remove("exp-modus", "exp-hud-aus"); };
  new MutationObserver(aufraeumen).observe(document.documentElement, {childList: true, subtree: true});
  window.EdenExpedition = {html, hud, fundZu, anrufAntwort, reisen, verjagen};
  // The client may have drawn before this (defer) script arrived: draw once more, like eden-combat does.
  const v0 = typeof V !== "undefined" ? V : null;
  if (v0 && v0.z && v0.z.status === "ereignis" && v0.z.ereignis && v0.z.ereignis.art === "ort" && typeof zeichnen === "function") zeichnen();
})();
