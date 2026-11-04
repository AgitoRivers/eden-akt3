/* Eden menu (25.10.2026): one full-screen pause frame for Inventory, Character, Relationships and Codex (tabs, Q/E),
   plus the Map. index.html hands every overlay this plugin handles to EdenMenu.html(z, overlay).
   Uses the client's globals: overlay, V, beschaeftigt, esc, geld, punkte, senden, zeichnen, profilFigur, profilOeffnen,
   codexErmittlungHtml, ortAuswahlHtml, PHASE, EdenSkills. */
(() => {
  "use strict";
  const TABS = [["inventory", "Inventory", "I"], ["character", "Character", "C"], ["bez", "Relationships", "B"], ["journal", "Journal", "N"], ["codex", "Codex", "J"]];
  const S = {item: null, ansicht: "overview", codex: "investigation"};
  // Fragen, deren Proven-Moment schon gezeigt wurde - je Spielstand im Browser gemerkt, damit ein Neuladen nichts wiederholt
  const TAFEL_GESEHEN = {
    _id: null, _s: new Set(),
    _laden(){ const id = (typeof V !== "undefined" && V && V.z && V.z.id) || "";
      if (id !== this._id){ this._id = id; try { this._s = new Set(JSON.parse(localStorage.getItem("eden_tafel_" + id) || "[]")); } catch (_) { this._s = new Set(); } } },
    has(k){ this._laden(); return this._s.has(k); },
    add(k){ this._laden(); this._s.add(k); try { localStorage.setItem("eden_tafel_" + this._id, JSON.stringify([...this._s])); } catch (_) {} }
  };
  // jacket -> look and weapon -> class of the character portraits (werkzeuge\charakter_bild.py)
  const LOOK = {jacket_earth: "Erde", jacket_water: "Wasser", jacket_fire: "Feuer", jacket_air: "Luft", cyber_armor: "Cyber"};
  const KLASSE = {bat: "Bat", sword: "Sword", knife: "Knife", spear: "Spear", gun: "Gun", mop: "Mop"};
  const uiIc = (id, klasse) => window.EdenUI ? EdenUI.icon(id, klasse) : "";
  const ELEMENT = {erde: "Earth", wasser: "Water", feuer: "Fire", luft: "Air"};
  const ATTR = {strength: ["Strength", "strength"], charm: ["Charm", "charm"], empathy: ["Empathy", "empathy"], perception: ["Perception", "perception"],
                cunning: ["Cunning", "cunning"], courage: ["Courage", "courage"]};
  const ART = {geschenk: "Gift", einzigartig: "Unique gift", attribut: "Attribute", gluecksbringer: "Lucky charm",
               ressource: "Supplies", teil: "Errand", werkzeug: "Tool", kampf: "Combat", schluessel: "Key",
               schmuggel: "Contraband", andenken: "Keepsake", snack: "Snack", gericht: "Dish", essen: "Food",
               material: "Material", quest: "Key item", rohstoff: "Raw material", fisch: "Fish"};
  // what the player sees: seven rubrics over the internal kinds (Brain Trust 26.10.2026, JRPG convention);
  // rohstoff/fisch = what Duc fells, breaks or catches on an expedition (stacking, 28.10.2026)
  const RUBRIK = {ressource: "Consumables", snack: "Consumables", gericht: "Consumables", kampf: "Consumables", essen: "Consumables",
                  geschenk: "Gifts", einzigartig: "Gifts", attribut: "Charms", gluecksbringer: "Charms", werkzeug: "Charms",
                  material: "Materials", quest: "Key Items", schluessel: "Key Items", teil: "Key Items",
                  andenken: "Keepsakes", schmuggel: "Contraband", rohstoff: "Materials", fisch: "Catch"};
  const RUBRIK_REIHE = ["Consumables", "Gifts", "Charms", "Materials", "Catch", "Contraband"];
  const OHNE_PLATZ = ["andenken", "quest", "schluessel"];

  const TITEL = {map: "Map", menue: "Menu"};       // frames without tabs
  const handles = o => o === "laden" || o === "menue" || TABS.some(t => t[0] === o);
  const frei = z => ["wahl", "kabine"].includes(z.status) && !(z.kampf && !z.kampf.ergebnis) && !beschaeftigt;

  const lookKlasse = z => "look-" + (LOOK[((z.kampf_profil || {}).ruestung || {}).id] || "Erde").toLowerCase();
  function portraet(z){
    const kp = z.kampf_profil;
    if (!kp) return null;
    const look = LOOK[(kp.ruestung || {}).id] || "Erde";
    let w = KLASSE[(kp.waffe || {}).id] || "Bat";
    if (w === "Mop" && look !== "Erde") w = "Bat";          // the scrubber portrait exists for Terra Scura only
    return "/charakterbild/Duc" + look + w;
  }
  const bild = (src, cls, stil) => src ? `<img class="${cls}" src="${src}" alt=""${stil ? ` style="${stil}"` : ""} onerror="this.classList.add('weg')">` : "";

  // ---------------------------------------------------------------- frame
  function rahmen(z, aktiv, body, still){
    const tabs = TABS.map(([id, label, k]) => `<button type="button" class="em-tab" aria-pressed="${id === aktiv}" onclick="EdenMenu.tab('${id}')">
      ${esc(label)}<kbd>${k}</kbd>${id !== aktiv && punkt(z, id) ? `<i class="em-dot" title="Something new"></i>` : ""}</button>`).join("");
    return `<div class="em${still ? " em-still" : ""}" data-tab="${aktiv}" role="dialog" aria-label="${esc(TITEL[aktiv] || (TABS.find(t => t[0] === aktiv) || [0, ""])[1])}">
      <header class="em-top">
        <div class="em-tag"><b>Day ${Math.min(z.tag, z.tage)}</b><small>${esc(PHASE[z.phase] || "")}</small></div>
        ${TITEL[aktiv] ? `<h2 class="em-titel">${TITEL[aktiv]}</h2>` : `<nav class="em-tabs"><kbd class="em-q">Q</kbd>${tabs}<kbd class="em-q">E</kbd></nav>`}
        <div class="em-rechts">${z.handel ? `<span class="em-geld">${geld(z.handel.konto)}</span>` : ""}
          <button type="button" class="em-zu" onclick="EdenMenu.zu()" aria-label="Close">Close <kbd>Esc</kbd></button></div>
      </header>
      <main class="em-body em-${aktiv}">${body}</main></div>`;
  }

  // ---------------------------------------------------------------- inventory
  // what changes if Duc puts this on (Brain Trust 26.10.: equipping is a decision, not a click)
  const eigen = x => ((x && x.eigenschaft) || "").split(":")[0];
  function vergleich(x, slot, aktuell){
    if (!aktuell || aktuell.id === x.id) return "";
    const teile = [];
    const wert = slot === "weapon" ? ["schaden", "damage"] : ["schutz", "protection"];
    const d = (x[wert[0]] || 0) - (aktuell[wert[0]] || 0);
    teile.push(`<span class="${d > 0 ? "plus" : d < 0 ? "minus" : ""}">${d > 0 ? "+" + d : d < 0 ? "−" + (-d) : "±0"} ${wert[1]}</span>`);
    if (slot === "weapon" && x.element !== aktuell.element)
      teile.push(`<span>${x.element ? (ELEMENT[x.element] || x.element) : "No element"} instead of ${aktuell.element ? (ELEMENT[aktuell.element] || aktuell.element) : "none"}</span>`);
    if (slot === "armor" && eigen(x) && eigen(x) !== eigen(aktuell)) teile.push(`<span>${esc(eigen(x))} instead of ${esc(eigen(aktuell))}</span>`);
    return `<span class="em-vergleich">${teile.join("")}</span>`;
  }
  function gearKarte(z, x, slot, aktuell, stueck, pool){
    const an = !!aktuell && aktuell.id === x.id;
    const chips = stueck ? Array.from({length: stueck.plaetze}, (_, i) => {
      const f = stueck.belegt[i], c = f && pool.find(p => p.familie === f);
      return `<i class="${f ? "an" : ""}" title="${esc(c ? c.label : "Empty chip slot")}"></i>`;
    }).join("") : "";
    const wert = slot === "weapon" ? `<b>${x.schaden}</b> damage` : `<b>${x.schutz}</b> protection`;
    return `<button type="button" class="em-gear ${esc(x.seltenheit || "")}${an ? " an" : ""}" ${an || !frei(z) ? "disabled" : ""}
        onclick="EdenMenu.anlegen('${slot}','${esc(x.id)}')" title="${esc(x.eigenschaft || "")}">
      ${bild("/itembild/" + x.id, "em-gear-bild")}
      <span class="em-gear-t"><b>${esc(x.label)}</b><small>${esc(x.untertitel || "")}</small></span>
      <span class="em-gear-m"><span class="em-stat">${wert}</span>${x.element ? `<span class="em-el ${x.element}">${ELEMENT[x.element] || x.element}</span>` : ""}
        ${x.stufe ? `<span class="em-up" title="Upgraded by Rosi">${"◆".repeat(x.stufe)}</span>` : ""}${chips ? `<span class="em-chips">${chips}</span>` : ""}</span>
      ${an ? `<span class="em-badge">Equipped</span>` : vergleich(x, slot, aktuell)}</button>`;
  }

  function namen(z){
    return Object.assign((z.werte || []).reduce((m, w) => (m[w.id] = w.name.split(" ")[0], m), {}), (z.handel && z.handel.namen) || {});
  }

  function itemDetail(z, it){
    if (!it) return `<div class="em-detail leer"><p>Select an item to see what it does.</p></div>`;
    const n = namen(z), aus = beschaeftigt ? "disabled" : "";
    return `<div class="em-detail">${bild(it.bild, "em-detail-bild")}
      <div><small class="em-art">${esc([RUBRIK[it.art], it.intim ? "Intimate" : ART[it.art] || it.art].filter((x, i, a) => x && a.indexOf(x) === i).join(" · "))}</small>
<h4>${esc(it.label)}${it.n > 1 ? ` <span class="em-zahl">×${it.n}</span>` : ""}${it.sterne ? ` <span class="em-sterne">${it.sterne.map(s => uiIc("quality", "klein").repeat(s)).join(" · ")}</span>` : ""}</h4><p>${esc(it.text || "")}</p>${it.wirkung_text ? `<p class="em-wirkung">${esc(it.wirkung_text)}</p>` : ""}
        ${it.stapel > 1 ? `<p class="em-hinweis">Stacks up to ${it.stapel} on one place.</p>` : ""}
        ${it.intim ? `<p class="em-hinweis">Only for someone close enough: ${[it.intim.begehren ? "desire " + it.intim.begehren : "", it.intim.vertrauen ? "trust " + it.intim.vertrauen : ""].filter(Boolean).join(", ")}. Never in front of others.</p>` : ""}
      <div class="em-aktionen">${it.benutzbar ? `<button type="button" class="em-knopf gold" ${aus} onclick="senden('benutzen',{id:'${it.id}'},'…')">Use</button>` : ""}
        ${(it.geben || []).map(p => `<button type="button" class="em-knopf" ${aus} onclick="overlay=null;senden('geben',{id:'${it.id}',an:'${p}'},'${esc(n[p] || p)} unwraps it …')">Give to ${esc(n[p] || p)}</button>`).join("")}</div></div></div>`;
  }

  function inventar(z){
    const h = z.handel, kp = z.kampf_profil;
    const alle = h ? h.inventar_info : [];
    const platz = (h && h.plaetze) || 6;          // bag size from the server (8 / 12 / 16), 6 only for old saves without it
    const rang = it => { const i = RUBRIK_REIHE.indexOf(RUBRIK[it.art]); return i < 0 ? 99 : i; };
    const rubrik = it => it.intim ? "Intimate" : RUBRIK[it.art];
    const tasche = alle.filter(it => !OHNE_PLATZ.includes(it.art)).sort((a, b) => rang(a) - rang(b)),
          schluessel = alle.filter(it => it.art === "quest" || it.art === "schluessel"), andenken = alle.filter(it => it.art === "andenken");
    if (S.item && !alle.some(it => it.id === S.item)) S.item = null;
    const kachel = it => `<button type="button" class="em-slot${it.id === S.item ? " an" : ""}" onclick="EdenMenu.item('${it.id}')" title="${esc(it.label)}">
      ${bild(it.bild, "")}<span>${esc(it.label)}</span>${rubrik(it) && !OHNE_PLATZ.includes(it.art) ? `<i class="em-rubrik${it.intim ? " intim" : ""}">${esc(rubrik(it))}</i>` : ""}${it.n > 1 || it.stapel > 1 ? `<b class="em-anzahl${it.n >= it.stapel ? " voll" : ""}" title="${it.n} of ${it.stapel} on this place">×${it.n}</b>` : ""}</button>`;
    const leer = n => Array.from({length: Math.max(0, n)}, () => `<span class="em-slot leer"></span>`).join("");
    let ruest = `<p class="em-hinweis">This adventure has no fights.</p>`;
    if (kp){
      const pool = (kp.chips && kp.chips.pool) || [], st = (kp.chips && kp.chips.stuecke) || [];
      const stueck = (slot, id) => st.find(s => s.slot === slot && s.id === id);
      // before Terremoto the deck scrubber is what Duc holds: it is not in the list of owned weapons, so show it as equipped
      const waffen = kp.waffe && !kp.waffen.some(x => x.id === kp.waffe.id) ? [kp.waffe].concat(kp.waffen) : kp.waffen;
      ruest = `<section><h3>Weapons</h3><div class="em-gearliste">${waffen.map(x => gearKarte(z, x, "weapon", kp.waffe, stueck("weapon", x.id), pool)).join("")
          || `<p class="em-hinweis">No weapon yet. Duc fights with whatever is at hand.</p>`}</div></section>
        <section><h3>Jackets</h3><div class="em-gearliste">${kp.ruestungen.map(x => gearKarte(z, x, "armor", kp.ruestung, stueck("armor", x.id), pool)).join("")}</div></section>
        <p class="em-hinweis">${frei(z) ? "Click to equip. Rosi upgrades and fits chips in her workshop." : "You can change between scenes, not in the middle of one."}</p>`;
    }
    const p = portraet(z);
    return `<div class="em-spalte em-ruestkammer">${ruest}</div>
      <div class="em-spalte em-mitte">${S.meldung ? `<div class="em-meldung" role="status">${esc(S.meldung)}</div>` : ""}${p ? `<div class="em-portraet klein ${lookKlasse(z)}">${bild(p, "")}</div>` : ""}
        ${kp ? `<div class="em-getragen"><span><small>Weapon</small><b>${esc(kp.waffe ? kp.waffe.label : "–")}</b></span><span><small>Jacket</small><b>${esc(kp.ruestung ? kp.ruestung.label : "–")}</b></span></div>
          ${kp.waffe && kp.waffe.eigenschaft ? `<p class="em-zitat">${esc(kp.waffe.eigenschaft)}</p>` : ""}${kp.ruestung && kp.ruestung.eigenschaft ? `<p class="em-zitat">${esc(kp.ruestung.eigenschaft)}</p>` : ""}` : ""}</div>
      <div class="em-spalte em-tasche">
        <section><h3>Bag <span class="em-zahl">${h ? h.belegt : 0}/${platz}</span></h3><div class="em-slots">${tasche.map(kachel).join("")}${leer(platz - tasche.length)}</div></section>
        ${h && (h.tasche || []).length + (h.tasche_plaetze || 0) ? `<section><h3>Errands <span class="em-zahl">${(h.tasche || []).length}/${h.tasche_plaetze || 3}</span></h3>
          <div class="em-slots klein">${(h.tasche || []).map(it => `<span class="em-slot" title="${esc(it.label + (it.fuer ? " · for " + it.fuer : ""))}">${bild(it.bild, "")}<span>${esc(it.label)}</span></span>`).join("")}${leer((h.tasche_plaetze || 3) - (h.tasche || []).length)}</div></section>` : ""}
        ${schluessel.length ? `<section><h3>Key Items</h3><div class="em-slots klein">${schluessel.map(kachel).join("")}</div>
          <p class="em-hinweis">Keep these. They will matter.</p></section>` : ""}
        ${andenken.length ? `<section><h3>Keepsakes</h3><div class="em-slots klein">${andenken.map(kachel).join("")}</div></section>` : ""}
        ${itemDetail(z, alle.find(it => it.id === S.item))}</div>`;
  }

  // ---------------------------------------------------------------- character
  function charakter(z){
    const kp = z.kampf_profil, p = z.persona;
    if (S.ansicht === "skills" && kp && window.EdenSkills)
      return `<div class="em-skillbaum"><button type="button" class="em-knopf zurueck" onclick="EdenMenu.ansicht('overview')">← Character</button>${EdenSkills.html(z)}</div>`;
    const attr = kp ? kp.attribute : Object.entries(p.attribute).map(([id, wert]) => ({id, wert, basis: wert}));
    const ap = kp ? kp.attributpunkte || 0 : 0;      // level-up (26.10.2026, like BG3): open points are spent here, attributes first
    const balken = (wert, max) => `<span class="em-balken"><i style="width:${Math.max(0, Math.min(100, wert / max * 100))}%"></i></span>`;
    const pfade = kp ? kp.pfade.map(pf => {
      const n = pf.skills.filter(s => s.gelernt).length;
      return `<div class="em-pfad"><b>${esc(pf.name)}</b><span class="em-pfadpunkte">${pf.skills.map(s => `<i class="${s.gelernt ? "an" : ""}" title="${esc(s.label)}"></i>`).join("")}</span><small>${n}/${pf.skills.length}</small></div>`;
    }).join("") : "";
    const bildUrl = portraet(z);
    return `<div class="em-spalte em-werte">
        <div class="em-name"><h2>Duc</h2><p>${esc(p.titel)}</p></div>
        ${kp ? `<div class="em-level"><span class="em-ring"><b>${kp.level}</b><small>Level</small></span>
          <div class="em-leiste"><span><small>Experience</small><b>${kp.level < kp.level_max ? `${kp.xp} / ${kp.xp_next}` : "Max"}</b></span>${balken(kp.level < kp.level_max ? kp.xp : 1, kp.level < kp.level_max ? kp.xp_next : 1)}
          <span><small>Health</small><b>${kp.lp} / ${kp.lp_max}</b></span>${balken(kp.lp, kp.lp_max)}
          <span><small>Stamina</small><b>${kp.ausdauer}</b></span></div></div>` : ""}
        <section><h3>Attributes ${ap ? `<span class="em-punkt">Spend ${ap} point${ap > 1 ? "s" : ""}</span>` : ""}</h3>
          <div class="em-attr ${ap ? "steigern" : ""}">${attr.map(a => `<div title="${esc(a.wirkung || "")}"><span class="em-attr-ic">${ATTR[a.id] ? uiIc(ATTR[a.id][1], "klein") : "·"}</span><span>${esc((ATTR[a.id] || [a.label])[0])}</span>
          ${balken(a.wert, a.max || 5)}<b>${a.wert}${a.wert > a.basis ? `<sup>▲</sup>` : ""}</b>
          ${ap ? `<button type="button" class="em-plus" ${beschaeftigt || a.wert >= (a.max || 5) ? "disabled" : ""} aria-label="Raise ${esc((ATTR[a.id] || [a.label])[0])}"
            onclick="senden('attribut_steigern',{id:'${esc(a.id)}'},'…')">+1</button>${a.wirkung ? `<small class="em-wirk">${esc(a.wirkung)}</small>` : ""}` : ""}</div>`).join("")}</div></section></div>
      <div class="em-spalte em-mitte">${bildUrl ? `<div class="em-portraet ${lookKlasse(z)}"><span class="em-wappen"></span>${bild(bildUrl, "")}
          <div class="em-schild"><b>${esc(kp.waffe ? kp.waffe.label : "–")}</b><span>·</span><b>${esc(kp.ruestung ? kp.ruestung.label : "")}</b></div></div>`
        : `<div class="em-portraet leer"></div>`}</div>
      <div class="em-spalte em-seite">
        ${kp ? `<section><h3>Skills</h3>
          <div class="em-pfade">${pfade}</div>
          <button type="button" class="em-knopf breit ${kp.skillpunkte ? "gold" : ""}" onclick="EdenMenu.ansicht('skills')">${kp.skillpunkte ? `Spend ${kp.skillpunkte} point${kp.skillpunkte > 1 ? "s" : ""} in the skill tree` : "Open skill tree"}</button></section>` : ""}
        <section class="em-notiz"><h3>Your secret</h3><p>${esc(p.geheimnis || "")}</p></section>
        <section><h3>Who you are</h3><p class="em-text">${esc(p.oeffentlich || "")}</p>
          <button type="button" class="em-knopf" onclick="profilOeffnen('duc')">Change chat portrait</button></section></div>`;
  }

  // ---------------------------------------------------------------- album (Duc 31.10.2026): selfies and big moments, notes in her own hand
  function album(z){
    const leute = z.album || [];
    const wer = leute.find(p => p.id === S.albumWer) || leute[0];
    const ICON = {selfie: "photo", szene: "love", kiss: "love", confession: "love", intimate: "desire"};
    const neu = selfiesNeu(z);
    // ihre Seite ist jetzt offen: der Punkt geht aus, NEW bleibt, bis Duc das Album verlaesst
    const frisch = new Set([...(S.albumFrisch || []), ...neu.filter(s => wer && s.wer === wer.id).map(s => s.bild)]);
    S.albumFrisch = [...frisch];
    selfiesMerken(z, S.albumFrisch);
    const karte = e => `<article class="em-polaroid">${frisch.has(e.bild) ? `<span class="em-neu neu">NEW</span>` : ""}
        ${e.bild ?`<img class="em-album-foto" src="${e.bild}" alt="${esc(e.titel)}" onclick="this.classList.toggle('gross')">`
          : `<div class="em-album-leer">${uiIc(ICON[e.art] || "love")}</div>`}
        <small>Day ${e.tag} · ${esc(e.titel)}</small>${e.notiz ? `<p>${esc(e.notiz)}</p>` : ""}</article>`;
    return `<div class="em-album"><button type="button" class="em-knopf zurueck" onclick="EdenMenu.ansicht('overview')">← Relationships</button>
      ${leute.length ? `<div class="em-album-wer">${leute.map(p => `<button type="button" class="em-knopf ${p === wer ? "gold" : ""}" onclick="EdenMenu.albumWer('${p.id}')">${esc(p.name)}${p !== wer && neu.some(s => s.wer === p.id) ? licht : ""}</button>`).join("")}</div>
        <div class="em-album-raster">${wer.eintraege.map(karte).join("")}</div>`
      : `<p class="em-hinweis">Nothing here yet. Her photos and your best moments will collect here.</p>`}</div>`;
  }

  // ---------------------------------------------------------------- relationships
  function beziehungen(z){
    if (S.ansicht === "album") return album(z);
    S.albumFrisch = null;
    const profile = z.profile || [], werte = {};
    (z.werte || []).forEach(w => werte[w.id] = w);
    const frauen = profile.filter(p => p.frau), neben = profile.filter(p => !p.frau);
    // Karten-Ausschnitt (Duc 01.11.2026): der gemessene Kopf sitzt in jeder Karte gleich gross und gleich hoch, das Bild reicht bis unter die dunkle Infozeile
    const KOPF_Y = .26, KOPF_D = .44, BILD_BIS = .88;
    const ausschnitt = a => {
      if (!a) return "";
      const s = Math.max(KOPF_D * a.r * a.zoom, (BILD_BIS - KOPF_Y) / (1 - a.cy));
      return `--s:${s.toFixed(3)};--y:${(KOPF_Y - a.cy * s).toFixed(3)};--cx:${a.cx.toFixed(3)};--r:${a.r.toFixed(3)}`;
    };
    const karte = p => {
      const w = werte[p.id] || {}, src = p.sprite || p.avatar, a = ausschnittFuer(src);
      return `<button type="button" class="em-person" onclick="profilFigur('${p.id}','vorlieben')" style="${p.bild ? `--bg:url('${p.bild}')` : ""}">
        ${bild(src, "em-person-bild" + (a ? " genau" : ""), ausschnitt(a))}
        <span class="em-person-info"><b>${esc(p.kurz || p.name)}</b><small>${esc(p.ort || "")}${p.lieblingsort ? " · her place" : ""}</small>
          <span class="em-ringe">${bezRing("v", p.vertrauen, w.v_anteil || 0)}${p.begehren !== null && p.begehren !== undefined ? bezRing("b", p.begehren, w.b_anteil || 0) : ""}</span></span></button>`;
    };
    const seg = (n, max, cls) => `<span class="em-seg ${cls || ""}">${Array.from({length: max}, (_, i) => `<i class="${i < n ? "an" : ""}"></i>`).join("")}</span>`;
    return `<div class="em-spalte em-personen"><div class="em-frauen">${frauen.map(karte).join("")}</div>
        ${neben.length ? `<h3>Crew and locals</h3><div class="em-neben">${neben.map(p => `<button type="button" class="em-nebenkarte" onclick="profilFigur('${p.id}','vorlieben')">
          ${avatar(p.avatar || p.sprite)}<span><b>${esc(p.kurz || p.name)}</b><small>${STUFEN_WORT.v[Math.max(0, Math.min(5, p.vertrauen || 0))]}</small></span>${bezRing("v", p.vertrauen, 0, true)}</button>`).join("")}</div>` : ""}</div>
      <aside class="em-spalte em-seite">
        <section><h3>Album</h3><p class="em-hinweis">Her photos and your best moments, with her notes.</p>
          <button type="button" class="em-knopf gold breit" onclick="EdenMenu.ansicht('album')">Open album${selfiesNeu(z).length ? licht : ""}</button></section>
        <section><h3>Tension between them</h3>${(z.rivalitaet || []).map(r => `<div class="em-uhr"><span>${esc(r.label.replace("Tension ", "").replace("Spannung ", ""))}</span>${seg(r.wert, 5, "rot")}</div>`).join("") || `<p class="em-hinweis">Calm waters.</p>`}</section>
        <section><h3>Clocks</h3>${(z.uhren || []).map(u => `<div class="em-uhr"><span>${esc(u.label)}</span>${seg(u.stand, u.segmente)}</div>`).join("") || `<p class="em-hinweis">No clocks are ticking.</p>`}</section></aside>`;
  }

  // ---------------------------------------------------------------- journal: orders (from the engine: z.journal) + favours + the day's quick jobs
  // UX pass (Duc 29.10.2026): counts and jump links on top, the next step highlighted in the list instead of a second box,
  // finished and missed orders folded to one line, done steps dimmed with a tick (no strike-through), NEW / UPDATED marks.
  const jKey = z => "eden_journal_" + z.id;
  function jLesen(z){ try { const t = localStorage.getItem(jKey(z)); return t === null ? null : JSON.parse(t); } catch (_) { return null; } }
  function jSchreiben(z, o){ try { localStorage.setItem(jKey(z), JSON.stringify(o)); } catch (_) {} }
  const sigAuftrag = a => a.status + ":" + a.schritte.filter(s => s.erledigt).length + ":" + (a.grau || []).filter(g => g.entschieden).length;
  const sigFavour = f => f.teile.length + ":" + (f.foto ? 1 : 0);
  // What changed since the last visit: computed once when the journal is opened (a re-render must not drop the marks),
  // then the current state is stored. No stored state at all = everything is new.
  function jNeu(z, neuerBesuch){
    if (!neuerBesuch && S.jNeu && S.jId === z.id) return S.jNeu;
    const jetzt = {}, neu = {}, alt = jLesen(z);
    (z.journal || []).forEach(a => { jetzt["a:" + a.id] = sigAuftrag(a); });
    (z.favours || []).forEach(f => { jetzt["f:" + f.kette] = sigFavour(f); });
    Object.keys(jetzt).forEach(k => { if (alt === null || !(k in alt)) neu[k] = "NEW"; else if (alt[k] !== jetzt[k]) neu[k] = "UPDATED"; });
    S.jNeu = neu; S.jId = z.id;
    jSchreiben(z, jetzt);
    return neu;
  }
  function journal(z, neuerBesuch){
    const liste = z.journal || [], aktiv = liste.filter(a => a.status === "aktiv"), fertig = liste.filter(a => a.status === "fertig" || a.status === "verpasst");
    const neu = jNeu(z, neuerBesuch);
    // Open / folded: main orders and anything NEW / UPDATED start open, other side orders and finished ones folded; a click overrides
    // that until the journal is opened again (Duc 29.10.2026).
    if (neuerBesuch || !S.jUm) S.jUm = {};
    const offen = a => a.id in S.jUm ? S.jUm[a.id] : a.status === "aktiv" && (!a.neben || !!neu["a:" + a.id]);
    const umschalten = a => `onclick="EdenMenu.auf('${a.id}',${offen(a)})" onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();this.click()}"`;
    const marke = k => neu[k] ? `<span class="em-neu ${neu[k] === "NEW" ? "neu" : "upd"}">${neu[k]}</span>` : "";
    const stand = a => a.status === "fertig" ? `<span class="em-fertig">Done</span>` : a.status === "verpasst" ? `<span class="em-fertig verpasst">Missed</span>` : "";
    // Where and until when (Duc 29.10.2026): place + times of day the place is open, and the last day with a countdown (<= 2 days = urgent)
    const ZEIT = {fruehstueck: "Breakfast", tag: "Midday", nachmittag: "Afternoon", dinner: "Dinner", abend: "Evening", nacht: "Night"};
    const rest = a => a.frist == null ? null : a.frist - z.tag + 1;
    const restKurz = a => { const n = rest(a); return n == null || a.status !== "aktiv" ? "" : n <= 1 ? "last day" : n + " days left"; };
    const frist = a => a.frist == null ? "" : a.status === "verpasst" ? `<span class="em-frist aus">${uiIc("deadline", "klein")}ended day ${a.frist}</span>`
      : `<span class="em-frist${rest(a) <= 2 ? " dringend" : ""}">${uiIc("deadline", "klein")}until day ${a.frist} · ${restKurz(a)}</span>`;
    const wo = a => a.status === "aktiv" && a.ort ? `<span class="em-wo">${uiIc("place", "klein")}${esc(a.ort)}${(a.zeiten || []).length ? " · " + a.zeiten.map(t => ZEIT[t] || t).join(", ") : ""}</span>` : "";
    const meta = a => wo(a) || frist(a) ? `<div class="em-meta">${wo(a)}${frist(a)}</div>` : "";
    const karte = a => {
      const jetzt = a.status === "aktiv" ? a.schritte.findIndex(s => !s.erledigt && !s.optional) : -1;
      return `<article class="em-auftrag ${a.status}">
      <div class="em-auftrag-kopf em-kopf-klick" role="button" tabindex="0" aria-expanded="true" ${umschalten(a)}>${avatar(a.sprite)}<div><h4>${esc(a.titel)}</h4><small>${esc(a.von_name)}${a.status !== "aktiv" && a.ort ? " · " + esc(a.ort) : ""}</small></div>
        ${marke("a:" + a.id)}${stand(a)}<i class="em-zuklapp" aria-hidden="true">${uiIc("collapse", "klein")}</i></div>
      ${meta(a)}
      <p>${esc(a.text)}</p>
      ${a.rueckblick ? `<div class="em-grau"><small>Last time</small><p>${esc(a.rueckblick)}</p></div>` : ""}
      <ul class="em-schritte">${a.schritte.map((s, i) => `<li class="${s.erledigt ? "an" : ""}${s.optional ? " opt" : ""}${i === jetzt ? " jetzt" : ""}">${s.erledigt ? uiIc("done", "klein") : ""}${esc(s.text)}${s.optional ? ` <small>· optional</small>` : ""}${i === jetzt ? ` <small>· next</small>` : ""}</li>`).join("")}</ul>
      ${(a.grau || []).length ? `<div class="em-grau"><small>Your call</small>${a.grau.map(g => `<p>${esc(g.text)}${g.entschieden ? ` <b>→ ${esc(g.entschieden)}</b>` : ""}</p>`).join("")}</div>` : ""}
      ${a.belohnung ? `<div class="em-lohn"><small>Reward</small>${esc(a.belohnung)}</div>` : ""}</article>`;
    };
    // folded: one line (running orders show their next step), click to unfold
    const zeile = a => `<button type="button" class="em-auftrag em-zeile ${a.status}" aria-expanded="false" ${umschalten(a)}>${avatar(a.sprite)}
      <span><b>${esc(a.titel)}</b><small>${esc(a.von_name)}${restKurz(a) ? ` · <span class="em-frist${rest(a) <= 2 ? " dringend" : ""}">${restKurz(a)}</span>` : ""}${a.status === "aktiv" && a.naechster ? " · next: " + esc(a.naechster) : ""}</small></span>${marke("a:" + a.id)}${stand(a)}<i>${uiIc("expand", "klein")}</i></button>`;
    const eintrag = a => offen(a) ? karte(a) : zeile(a);
    const jobs = (z.handel && z.handel.jobs) || [], gezeigt = new Set();
    const schnell = jobs.filter(j => !j.gruppe || (!gezeigt.has(j.gruppe) && gezeigt.add(j.gruppe))).map(j =>
      `<button type="button" class="em-job" onclick="overlay=null;missionOeffnen('${j.id}')">${avatar(j.sprite)}<span><b>${esc(j.gruppe ? j.gruppe_titel : j.titel)}</b>
        <small>${esc(j.von_kurz || "")}${j.ort_name ? " · " + esc(j.ort_name) : ""}</small></span></button>`).join("");
    // main and side orders apart; favours = what Duc has already been asked (engine z.favours), photo at the end (29.10.2026)
    const haupt = aktiv.filter(a => !a.neben), neben = aktiv.filter(a => a.neben);
    const AUSGANG = {ok: ["done", "helped"], daneben: ["failed", "didn't work out"], abgelehnt: ["declined", "said no"]};
    const favour = f => `<article class="em-favour">
      <div class="em-auftrag-kopf"><div><h4>${esc(f.titel)}</h4><small>${esc(f.von_name || "")}</small></div>${marke("f:" + f.kette)}</div>
      <ul class="em-schritte">${f.teile.map(t => `<li class="${t.ausgang === "ok" ? "an" : esc(t.ausgang || "")}" title="${esc(t.weg || "")}">${AUSGANG[t.ausgang] ? uiIc(AUSGANG[t.ausgang][0], "klein") : ""}${esc(t.titel)} <small>· ${(AUSGANG[t.ausgang] || ["", ""])[1]}</small></li>`).join("")}</ul>
      ${f.foto ? `<img class="em-favour-foto" src="${f.foto}" alt="Photo from ${esc(f.von_name || "")}" onclick="this.classList.toggle('gross')">` : ""}</article>`;
    const favours = z.favours || [];
    const sprung = (id, n, text) => `<button type="button" class="em-sprung" ${n ? `onclick="EdenMenu.sprung('${id}')"` : "disabled"}><b>${n}</b> ${text}</button>`;
    return `<div class="em-spalte em-auftraege">
        <div class="em-uebersicht">${sprung("em-j-haupt", haupt.length, "main")}${sprung("em-j-neben", neben.length, "side")}${sprung("em-j-fertig", fertig.length, "done")}${sprung("em-j-favours", favours.length, "favours")}</div>
        <h3 id="em-j-haupt">Main orders</h3>
        ${haupt.length ? haupt.map(eintrag).join("") : `<p class="em-hinweis">No orders yet. People will ask you for things once they trust you.</p>`}
        ${neben.length ? `<h3 class="em-abstand" id="em-j-neben">Side orders</h3>${neben.map(eintrag).join("")}` : ""}
        ${fertig.length ? `<h3 class="em-abstand" id="em-j-fertig">Done</h3>${fertig.map(eintrag).join("")}` : ""}</div>
      <aside class="em-spalte em-seite"><section><h3 id="em-j-favours">Favours</h3>
        ${favours.length ? favours.map(favour).join("") : `<p class="em-hinweis">Nobody has asked you for a favour yet. Your phone will tell you.</p>`}</section>
        ${schnell ? `<section><h3>Quick jobs today</h3>${schnell}<p class="em-hinweis">Quick jobs also start from your phone.</p></section>` : ""}</aside>`;
  }

  // ---------------------------------------------------------------- codex: the investigation as Duc's notebook (Brain Trust 26.10.)
  const ZUV = {"secured": "fest", "solid": "fest", "seen yourself": "gesehen", "only a statement": "aussage", "rumour": "geruecht"};
  function ermittlung(e){
    if (!e) return `<p class="em-hinweis">Nothing to investigate yet.</p>`;
    // Fall-Tafel (Duc 28.10.2026): Open / Partly (x of y) / Proven und nur die ART dessen, was fehlt. Springt eine Frage
    // auf Proven, leuchtet sie beim ersten Anblick kurz auf, mit Ton (einmal je Frage und Spielstand-Sitzung).
    const tafel = e.tafel && e.tafel.length ? e.tafel : e.fragen.map(f => ({id: f.id, frage: f.frage, stand: f.belegt ? "proven" : "open", fehlt: []}));
    const neu = tafel.filter(f => f.stand === "proven" && !TAFEL_GESEHEN.has(f.id + "|" + f.frage));
    if (neu.length){ neu.forEach(f => TAFEL_GESEHEN.add(f.id + "|" + f.frage)); if (window.EdenSfx) try { EdenSfx.play("auftrag_siegel", 250); } catch (_) {} }
    const fragen = tafel.map((f, i) => `<div class="em-frage${f.stand === "proven" ? " an" : f.stand === "partly" ? " teil" : ""}${neu.includes(f) ? " frisch" : ""}"><span class="em-frage-nr">${i + 1}</span>
      <span>${esc(f.frage)}${(f.fehlt || []).length ? `<em class="em-fehlt">${f.fehlt.map(esc).join(" ")}</em>` : ""}</span>
      <small>${f.stand === "proven" ? "Proven" : f.stand === "partly" ? `Partly · ${f.x} of ${f.y}` : "Open"}</small></div>`).join("");
    const fakten = e.eintraege.map(x => `<li class="em-fakt"><span class="em-zeit">${esc(x.zeit)}</span>
      <span class="em-fakt-text">${esc(x.text)}</span>
      <span class="em-zuv ${ZUV[x.zuv] || ""}">${esc(x.zuv)}</span><small class="em-gefunden">${esc(x.gefunden)}</small></li>`).join("");
    const aktion = a => `<button type="button" class="em-erm" onclick="overlay=null;ermitteln('${a.weg}')" ${beschaeftigt ? "disabled" : ""}>
      <b>${ermIc(a)} ${esc(a.verb)}${a.tipp ? ` <span class="em-tipp" title="Someone pointed you here">${uiIc("talk", "klein")}</span>` : ""}</b>
      <span>${esc(a.text)}</span>${a.kosten ? `<small>${uiIc("time", "klein")} ${esc(a.kosten)}</small>` : ""}${a.sperre ? `<small class="zu">${uiIc("locked", "klein")} ${esc(a.sperre)}</small>` : ""}</button>`;
    return `<section class="em-fall"><h3>The case</h3><div class="em-fragen">${fragen}</div>
        ${e.kette ? `<p class="em-kette">The chain holds. You can confront someone with the evidence.</p>` : ""}</section>
      ${(e.aussen || []).length ? `<section><h3>Possible now · no scene needed</h3><div class="em-erms">${e.aussen.map(aktion).join("")}</div></section>` : ""}
      <section><h3>What you know · by time</h3>${fakten ? `<ul class="em-fakten">${fakten}</ul>` : `<p class="em-hinweis">Nothing secured yet. Start where it happened.</p>`}</section>
      ${(e.widersprueche || []).length ? `<section><h3>The times don't add up</h3><ul class="em-notizen rot">${e.widersprueche.map(w => `<li>${uiIc("time", "klein")} ${esc(w)}</li>`).join("")}</ul></section>` : ""}
      ${(e.geruechte || []).length ? `<section><h3>Rumours · not evidence, only a hint where to look</h3><ul class="em-notizen kursiv">${e.geruechte.map(g => `<li>${uiIc("talk", "klein")} ${esc(g)}</li>`).join("")}</ul></section>` : ""}`;
  }

  // ---------------------------------------------------------------- codex
  function codex(z){
    const seiten = [["investigation", "Investigation"], ["discoveries", "Discoveries"], ["chronicle", "Chronicle"]];
    if (z.mochis && window.EdenMochis) seiten.push(["fieldbook", "Field Book"]);   // Bibis Tiere (Duc 01.11.2026)
    if ((z.bestiarium || []).length) seiten.push(["bestiary", "Bestiary"]);           // Rhythmus je Gegnerart nach der ersten Parade (Duc 03.11.2026)
    let inhalt = "";
    if (S.codex === "fieldbook" && z.mochis && window.EdenMochis) inhalt = EdenMochis.codexHtml(z);
    else if (S.codex === "investigation" || S.codex === "fieldbook") inhalt = ermittlung(z.ermittlung);
    else if (S.codex === "bestiary") inhalt = `<p class="em-hinweis">You learn a fighter by parrying them. Their rhythm, never their numbers.</p>
      <ul class="em-eintraege">${(z.bestiarium || []).map(b => `<li><b>${esc(b.name)}</b> <span class="em-hinweis">· parried ${b.paraden}×</span>${b.rhythmus.map(r => `<small>${esc(r)}</small>`).join("")}</li>`).join("")}</ul>`;
    else if (S.codex === "discoveries") inhalt = (z.codex || []).length ? `<ul class="em-eintraege">${z.codex.map(c => `<li>${esc(c)}</li>`).join("")}</ul>` : `<p class="em-hinweis">Nothing discovered yet.</p>`;
    else {
      const tage = {};
      (z.chronik || []).forEach(c => (tage[c.tag] = tage[c.tag] || []).push(c));
      inhalt = Object.keys(tage).sort((a, b) => b - a).map(t => `<div class="em-tagblock"><h4>Day ${esc(t)}</h4><ul class="em-eintraege">${tage[t].map(c =>
        `<li class="${c.abgelaufen ? "alt" : ""}">${esc(c.text)}${(c.weiss || []).length ? `<small>Known to ${esc(c.weiss.join(", "))}</small>` : ""}</li>`).join("")}</ul></div>`).join("")
        || `<p class="em-hinweis">Nothing has happened yet. Give it a day.</p>`;
    }
    return `<nav class="em-spalte em-seiten">${seiten.map(([id, l]) => `<button type="button" aria-pressed="${S.codex === id}" onclick="EdenMenu.codex('${id}')">${l}</button>`).join("")}</nav>
      <div class="em-spalte em-blatt">${inhalt}</div>`;
  }

  // ---------------------------------------------------------------- map
  function karte(z){
    const h = z.handel;
    if (!h) return `<p class="em-hinweis">Nowhere to go in this adventure.</p>`;
    const alle = Object.entries(h.laeden);
    const schiff = ORT_REIHE.filter(k => h.laeden[k]).concat(alle.filter(([k, l]) => !l.nur_an_land && !ORT_REIHE.includes(k)).map(([k]) => k));
    const insel = alle.filter(([, l]) => l.nur_an_land).map(([k]) => k);
    const kachel = lid => {
      const l = h.laeden[lid], t = ortBuehne(z, lid), sp = ortSprite(t), offen = ortOffen(l);
      const wahl = (() => { const alt = ORT; ORT = {lid}; try { return ortWahlen(z).map(w => w[1]); } catch (e) { return []; } finally { ORT = alt; } })();
      return `<button type="button" class="em-ort" ${offen ? `onclick="ortBetreten('${lid}')"` : "disabled"} style="${t && t.bild ? `--bg:url('${t.bild}')` : ""}">
        ${bild(sp, "em-ort-figur")}${offen && ortNeu(z, lid) ? `<span class="neu-marke em-ort-neu" title="New goods or someone new here">New</span>` : ""}
        <span class="em-ort-info"><b>${esc(ortName(z, lid))}</b><small>${esc(l.name)}</small>
          ${offen ? `<span class="em-ort-wahl">${wahl.map(w => `<i>${esc(w)}</i>`).join("")}</span>`
                  : `<span class="em-ort-zu">The tender only runs on days you went ashore.</span>`}</span></button>`;
    };
    return `<section><h3>On board</h3><div class="em-orte">${schiff.map(kachel).join("")}</div></section>
      ${insel.length ? `<section><h3>${uiIc("tender", "klein")} Cala d'Orsu · by tender</h3><div class="em-orte">${insel.map(kachel).join("")}</div></section>` : ""}`;
  }

  // ---------------------------------------------------------------- menu (Esc): settings only, grouped
  function menue(z){
    const s = z.szene;
    const zeile = (titel, sub, klick, an) => `<button type="button" class="em-zeile" onclick="${klick}" ${an === false ? "disabled" : ""}><b>${titel}</b><small>${sub}</small></button>`;
    const tasten = [["Enter", "send"], ["1–3", "suggestion or choice"], ["H", "phone"], ["M", "map"], ["I", "inventory"], ["C", "character"],
                    ["B", "relationships"], ["J", "codex"], ["Q / E", "previous / next tab"], ["P", "conversation"], ["R", "rewrite answers"], ["Esc", "menu"]];
    return `<div class="em-spalte em-gruppen">
        <section><h3>Sound</h3>
          <div class="em-regler"><span>Music</span><div id="musikEinstellungen"></div></div>
          <div class="em-regler"><span>Effects</span><div id="sfxEinstellungen"></div></div>
          ${zeile("Voice", STIMME ? "On · characters speak their lines" : "Off", "stimmeUmschalten()")}
          <div class="em-regler tempo"><label for="tempoRegler">Speech speed</label>
            <input id="tempoRegler" type="range" min="${TEMPO_MIN}" max="${TEMPO_MAX}" step="0.05" value="${TEMPO}" oninput="tempoSetzen(this.value)" aria-label="Speech speed">
            <b id="tempoWert">×${TEMPO.toFixed(2)}</b>
            <button type="button" class="em-knopf" onclick="tempoSetzen(${TEMPO_STD});document.getElementById('tempoRegler').value=${TEMPO_STD}">Default</button></div></section>
        <section><h3>Game</h3>
          ${zeile("Conversation", (chatOffen ? "Shown" : "Collapsed") + " · P", "chatUmschalten()")}
          ${window.EdenCombat ? `<div class="em-kampfopt">${EdenCombat.optionenHtml()}</div>` : ""}
          ${zeile("Combat wiki", "Rules to look up · opens in a new tab", "window.open('/wiki/kampf','_blank','noopener')")}</section>
        ${s ? `<section><h3>This scene</h3>
          ${zeile("Rewrite answers", "Back to your last message · R", "overlay=null;senden('swipe',{},'Rewriting …')", !!s.kann_swipen)}
          ${zeile("End scene", "The consequences are counted", "if(confirm('End the scene now?')){overlay=null;senden('ende',{},'The scene fades …')}")}
          ${z.modus === "entspannt" ? zeile("Restart scene", "Relaxed mode only", "if(confirm('Start the scene again?')){overlay=null;senden('szene_neu',{},'The scene starts again …')}") : ""}</section>` : ""}
      </div>
      <div class="em-spalte em-gruppen">
        <section><h3>Studio</h3>
          ${zeile("Assign voices", "Chatterbox · like in SillyTavern", "stimmenOeffnen()")}
          ${zeile("Portrait crops", "The circles of the women and side characters", "ausschnitteOeffnen()")}</section>
        <section><h3>Keys</h3><div class="em-tasten">${tasten.map(([k, l]) => `<span><kbd>${k}</kbd>${l}</span>`).join("")}</div></section>
        <section><h3>Run</h3>
          ${zeile("New run", "Back to the title screen · this run stays saved", "if(confirm('Start a new run? This one stays saved.')){overlay=null;V.z=null;zeichnen()}")}
          <p class="em-hinweis">Story model ${V.kobold ? "ready" : "not reachable"} · ${z.modus === "ironman" ? "Ironman" : "Relaxed"} mode</p></section>
      </div>`;
  }

  // ---------------------------------------------------------------- dock dots (Brain Trust 26.10., Sora's rule): only for things
  // Duc can DO - a skill point to spend, a new step in an order, something new in the bag or armoury - and gone once the tab was open.
  const SPUR = {
    character: z => { const kp = z.kampf_profil || {}, n = kp.skillpunkte || 0, a = kp.attributpunkte || 0;
                      return n || a ? "sp" + n + "ap" + a : ""; },
    journal: z => (z.journal || []).filter(a => a.status === "aktiv").map(a => a.id + ":" + (a.naechster || "")).join("|"),
    inventory: z => [...((z.handel || {}).inventar_info || []).map(i => i.id), ...((z.kampf_profil || {}).waffen || []).map(w => w.id),
                     ...((z.kampf_profil || {}).ruestungen || []).map(r => r.id)].sort().join(","),
  };
  const gesehenKey = z => "eden_gesehen_" + z.id;
  function gesehen(z){
    try { return JSON.parse(localStorage.getItem(gesehenKey(z)) || "{}"); } catch (e) { return S.gesehen || {}; }
  }
  function merken(z, tab){
    if (!SPUR[tab]) return;
    const g = gesehen(z);
    g[tab] = SPUR[tab](z);
    S.gesehen = g;
    try { localStorage.setItem(gesehenKey(z), JSON.stringify(g)); } catch (e) {}
  }
  // Neues Selfie (Duc 02.11.2026): Punkt auf Herz, Reiter und "Open album", bis das Album ihre Seite gezeigt hat.
  // Erster Lauf: was schon im Album liegt, gilt als gesehen.
  const licht = `<i class="em-licht" title="New selfie"></i>`;
  const selfies = z => (z.album || []).flatMap(p => p.eintraege.filter(e => e.art === "selfie" && e.bild).map(e => ({wer: p.id, bild: e.bild})));
  function selfiesMerken(z, bilder){
    const g = gesehen(z);
    g.selfies = [...new Set([...(g.selfies || []), ...bilder])];
    S.gesehen = g;
    try { localStorage.setItem(gesehenKey(z), JSON.stringify(g)); } catch (e) {}
  }
  function selfiesNeu(z){
    if (!z || !z.id) return [];
    const g = gesehen(z), alle = selfies(z);
    if (!g.selfies) { selfiesMerken(z, alle.map(s => s.bild)); return []; }
    return alle.filter(s => !g.selfies.includes(s.bild));
  }
  function punkt(z, tab){
    if (tab === "bez") return selfiesNeu(z).length > 0;
    if (!SPUR[tab] || !z || !z.id) return false;
    const jetzt = SPUR[tab](z), g = gesehen(z);
    if (!(tab in g)) { merken(z, tab); return tab === "character" && !!jetzt; }   // first run: only open points count as new
    if (!jetzt) return false;
    if (tab === "inventory") { const alt = new Set((g[tab] || "").split(",")); return jetzt.split(",").some(i => i && !alt.has(i)); }
    return jetzt !== g[tab];
  }

  function html(z, o){
    const aktiv = o === "laden" ? "map" : o;
    merken(z, aktiv);
    // a re-render of an open menu (a click, a state update) must not replay the fade-in and must keep the scroll positions
    const offen = document.querySelector(".em");
    const scroll = offen ? [...offen.querySelectorAll(".em-spalte, .em-body")].map(e => e.scrollTop) : [];
    const gleich = offen && offen.dataset.tab === aktiv;
    const body = aktiv === "map" ? karte(z) : aktiv === "inventory" ? inventar(z) : aktiv === "character" ? charakter(z)
      : aktiv === "bez" ? beziehungen(z) : aktiv === "menue" ? menue(z) : aktiv === "journal" ? journal(z, aktiv === "journal" && !gleich) : codex(z);
    if (gleich && scroll.some(s => s)) setTimeout(() => {
      const neu = document.querySelector(".em");
      if (neu) [...neu.querySelectorAll(".em-spalte, .em-body")].forEach((e, i) => { if (scroll[i]) e.scrollTop = scroll[i]; });
    }, 0);
    return rahmen(z, aktiv, body, !!offen);
  }

  // ---------------------------------------------------------------- actions and keys
  function tab(id){ if (id !== "character") S.ansicht = "overview"; overlay = id; zeichnen(); }
  function blaettern(d){
    const i = TABS.findIndex(t => t[0] === overlay);
    if (i >= 0) tab(TABS[(i + d + TABS.length) % TABS.length][0]);
  }
  document.addEventListener("keydown", ev => {
    if (!TABS.some(t => t[0] === overlay) || ev.ctrlKey || ev.metaKey || ev.altKey || /INPUT|TEXTAREA/.test(ev.target.tagName)) return;
    const k = ev.key.toLowerCase();
    if (k === "q" || k === "e"){ ev.preventDefault(); ev.stopImmediatePropagation(); blaettern(k === "e" ? 1 : -1); }
  }, true);

  window.EdenMenu = {
    handles, html, tab, portraet, punkt,
    zu(){ overlay = null; S.ansicht = "overview"; zeichnen(); },
    item(id){ S.item = S.item === id ? null : id; zeichnen(); },
    ansicht(a){
      S.ansicht = a;
      if (a === "album") { const n = selfiesNeu(V && V.z); if (n.length) S.albumWer = n[n.length - 1].wer; }   // gleich zu ihr, die etwas Neues geschickt hat
      zeichnen();
    },
    albumWer(id){ S.albumWer = id; zeichnen(); },
    auf(id, offen){ (S.jUm || (S.jUm = {}))[id] = !offen; zeichnen(); },       // fold / unfold an order (offen = how it is shown now)
    sprung(id){ const e = document.getElementById(id); if (e) e.scrollIntoView({block: "start", behavior: "smooth"}); },
    codex(id){ S.codex = id; zeichnen(); },
    anlegen(platz, id){
      const kp = (V.z && V.z.kampf_profil) || {}, x = [...(kp.waffen || []), ...(kp.ruestungen || [])].find(g => g.id === id);
      S.meldung = x ? x.label + " equipped" : "";
      clearTimeout(S.meldungUhr);
      S.meldungUhr = setTimeout(() => { S.meldung = ""; if (overlay === "inventory") zeichnen(); }, 2600);
      senden("ausruesten", {platz, id}, "…");
    },
  };
})();
