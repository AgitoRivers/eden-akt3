/* Sturm an Tag 5 (Duc 27.10.2026, Brain Trust "Alle, bau um") - gescriptetes Ereignis im Stil der Anhoerung.
   Teil "vorbereitung": Megan, Bitten der Crew, dann fuenf Posten-Karten + sechs Chips (inkl. Duc) zum Einteilen.
   Teil "nacht": Krisen nacheinander (Blitz, Ton, Notlicht beim Stromausfall), Rufe der Crew, einmal hinrennen (Sprint).
   Darstellung nutzt die Moment-Bausteine der Anhoerung (Klassen vh-moment, vh-mblase, vh-tratsch aus eden-hearing.css).
   Nur Darstellung: Regeln kommen vom Server (z.sturm, kern/sturm.py). Aktionen ueber senden('sturm', {was, ...}):
     einteilen {posten: {id: pid}} · sprint {rennen} · schliessen */
(function(){
  "use strict";
  const ST = {chip: null, plan: {}, hilfe: false, erg: {}, teil: null};
  const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
  const busy = () => (typeof beschaeftigt !== "undefined" && beschaeftigt);
  const neu = () => { if (typeof zeichnen === "function") zeichnen(); };
  const IC = {ok: uiIc("done", "imtext"), knapp: uiIc("partial", "imtext"), weg: uiIc("failed", "imtext")};
  const ROLLE = {megan: " · WATCHING", bitte: " · ASKS FOR", zusage: " · ON THE POST", ruhe: " · RESTING", posten_ruf: "",
                 panik: " · CALLING FOR HELP", hilfe: "", morgen: " · AT DAWN"};

  function senden2(was, extra){ if (!busy()) senden("sturm", Object.assign({was}, extra || {}), "…"); }

  // ------------------------------------------------------------------ Einteilen
  function chipWaehlen(pid){ ST.chip = ST.chip === pid ? null : pid; neu(); }
  function postenKlick(po){
    if (ST.chip){
      for (const k of Object.keys(ST.plan)) if (ST.plan[k] === ST.chip) delete ST.plan[k];
      ST.plan[po] = ST.chip; ST.chip = null;
      if (window.EdenSfx) try { EdenSfx.play("chip_einrasten"); } catch (e) {}
    } else if (ST.plan[po]) delete ST.plan[po];       // Chip zurueck in die Reihe
    neu();
  }
  function ziehen(ev, pid){ try { ev.dataTransfer.setData("text/plain", pid); } catch (e) {} ST.chip = pid; }
  function ablegen(ev, po){ ev.preventDefault(); const pid = (ev.dataTransfer && ev.dataTransfer.getData("text/plain")) || ST.chip;
    if (pid){ ST.chip = pid; postenKlick(po); } }
  function schicken(){ senden2("einteilen", {posten: Object.assign({}, ST.plan)}); }

  // ------------------------------------------------------------------ Teile
  function avatar(c){ return c && c.sprite ? `<span class="st-av" style="background-image:url('${esc(c.sprite)}');${ausschnittStil(ausschnittFuer(c.sprite))}"></span>`
    : `<span class="st-av du">${c && c.id === "duc" ? "You" : "?"}</span>`; }

  function brett(s){
    const crew = Object.fromEntries(s.crew.map(c => [c.id, c]));
    const einteilen = s.teil === "vorbereitung" && s.schritt === "einteilen" && !TON.moment && !TON.schlange.length;
    const plan = einteilen ? ST.plan : Object.fromEntries(s.posten.filter(p => p.wer).map(p => [p.id, p.wer]));
    const bitteJetzt = TON.moment && TON.moment.art === "bitte" ? TON.moment.posten : null;
    const krise = TON.krise;
    const karten = s.posten.map(p => {
      const wer = plan[p.id] ? crew[plan[p.id]] : null;
      const erg = ST.erg[p.id];
      const kl = [erg ? "e-" + erg : "", krise === p.id ? "krise" : "", bitteJetzt === p.id ? "wunsch" : "",
                  einteilen && ST.chip ? "bereit" : ""].join(" ");
      return `<button type="button" class="st-posten ${kl}" ${einteilen ? "" : "tabindex=-1"} onclick="EdenStorm.posten('${p.id}')"
        ondragover="event.preventDefault()" ondrop="EdenStorm.ablegen(event,'${p.id}')">
        <b>${esc(p.titel)}${erg ? `<i class="st-erg">${IC[erg]}</i>` : ""}</b><small>${esc(p.text)}</small>
        <span class="st-slot">${wer ? `${avatar(wer)}<em>${esc(wer.name)}</em>` : `<em class="leer">${einteilen ? (ST.chip ? "Put them here" : "Nobody yet") : "Nobody"}</em>`}</span>
      </button>`;
    }).join("");
    let unten = "";
    if (einteilen){
      const vergeben = new Set(Object.values(ST.plan));
      const chips = s.crew.map(c => {
        const w = c.wunsch ? (s.posten.find(p => p.id === c.wunsch) || {}).titel : null;
        return `<button type="button" draggable="true" ondragstart="EdenStorm.ziehen(event,'${c.id}')"
          class="st-chip ${ST.chip === c.id ? "gewaehlt" : ""} ${vergeben.has(c.id) ? "weg" : ""}" onclick="EdenStorm.chip('${c.id}')">
          ${avatar(c)}<span><b>${esc(c.name)}</b><small>${c.id === "duc" ? "you can take a post - or stay free to run once" : "asked for: " + esc(w || "–")}</small></span></button>`;
      }).join("");
      const ruhen = s.crew.filter(c => c.id !== "duc" && !vergeben.has(c.id)).map(c => c.name);
      const leer = s.posten.filter(p => !ST.plan[p.id]).length;
      const hinweis = ST.chip ? "Now click a post above." : leer ? `${leer} post${leer > 1 ? "s" : ""} still empty – an empty post goes wrong tonight.`
        : ruhen.length ? `${ruhen.join(" and ")} will rest.` : "Everyone has a post – nobody rests.";
      unten = `<div class="st-reihe">${chips}</div><div class="st-fuss"><span>${esc(hinweis)}</span>
        <button type="button" class="knopf" ${busy() ? "disabled" : ""} onclick="EdenStorm.schicken()">Send them</button></div>`;
    }
    return `<div class="st-brett ${einteilen ? "aktiv" : ""}"><div class="st-karten">${karten}</div>${unten}</div>`;
  }

  function sprintHtml(s){
    if (s.schritt !== "sprint" || !s.sprint || TON.moment || TON.schlange.length) return "";
    const wer = s.sprint.wer && s.sprint.wer !== "duc" ? s.namen[s.sprint.wer] : null;
    return `<div class="vh-anklage-box vh-wahlbox st-sprint"><div class="vh-frage">${wer ? `${esc(wer)} can't hold ${esc(s.sprint.titel.toLowerCase())}.`
      : `Nobody is on ${esc(s.sprint.titel.toLowerCase())}.`}</div>
      <p class="st-klein">You can run to one place tonight. The night isn't over yet.</p>
      <div class="vh-wkarten"><button type="button" class="vh-wk" ${busy() ? "disabled" : ""} onclick="EdenStorm.senden('sprint',{rennen:true})">
        <b>Run there</b><small>Save this post yourself – then you're spent for the night.</small></button>
        <button type="button" class="vh-wk" ${busy() ? "disabled" : ""} onclick="EdenStorm.senden('sprint',{rennen:false})">
        <b>Stay put</b><small>Let it go. Something worse might still come.</small></button></div></div>`;
  }

  function endeHtml(s){
    if (!s.fertig || TON.moment || TON.schlange.length) return "";
    if (s.teil === "vorbereitung")
      return `<div class="vh-anklage-box vh-ende st-ende"><div class="vh-frage">Everyone to their posts</div>
        <p class="st-klein">The storm comes in after midnight.</p>
        <button class="knopf" type="button" ${busy() ? "disabled" : ""} onclick="EdenStorm.senden('schliessen')">Continue</button></div>`;
    const b = s.bilanz || {zeilen: []};
    const posten = s.posten.map(p => `<li><span>${esc(p.titel)}</span><b class="${p.ergebnis === "weg" ? "aus" : "ok"}">${
      {ok: uiIc("done", "imtext") + " held", knapp: uiIc("partial", "imtext") + " held, barely", weg: uiIc("failed", "imtext") + " lost"}[p.ergebnis] || "–"}${p.wer ? " · " + esc(s.namen[p.wer] || p.wer) : ""}</b></li>`).join("");
    return `<div class="vh-anklage-box vh-ende vh-bilanz st-ende"><div class="vh-frage">The night of the storm</div>
      <ul class="vh-bpunkte">${posten}</ul>${b.zeilen.length ? `<ul class="vh-folgen">${b.zeilen.map(z => `<li>${esc(z)}</li>`).join("")}</ul>` : ""}
      <button class="knopf" type="button" ${busy() ? "disabled" : ""} onclick="EdenStorm.senden('schliessen')">Continue</button></div>`;
  }

  // ------------------------------------------------------------------ Stimme + Momente (wie eden-hearing.js)
  const TON = {letztesN: null, schlange: [], laeuft: null, moment: null, uhr: null, dunkel: false, krise: null, blitz: 0};
  function tonAn(){ return typeof STIMME === "undefined" || STIMME; }
  function audio(key, fertig){
    if (!key || !tonAn()){ fertig(); return null; }
    let a;
    try { a = new Audio("/api/zeile?id=" + encodeURIComponent(key)); if (typeof mitTempo === "function") mitTempo(a); }
    catch (e) { fertig(); return null; }
    let gemeldet = false;
    const ende = () => { if (!gemeldet){ gemeldet = true; fertig(); } };
    a.addEventListener("ended", ende); a.addEventListener("error", ende);
    a.play().catch(ende);
    return a;
  }
  const lesezeit = text => Math.min(8000, 2000 + String(text || "").length * 55);
  const FLUSS = ["tratsch", "ruf", "bitte"];
  function abspielen(){
    if (TON.laeuft || TON.moment || !TON.schlange.length) return;
    if (TON.pauseBis && Date.now() < TON.pauseBis){ setTimeout(abspielen, TON.pauseBis - Date.now() + 10); return; }
    const it = TON.schlange.shift();
    it.fort = FLUSS.includes(it.art) && TON.letzteArt === it.art;
    TON.letzteArt = it.art;
    if (it.art === "krise"){ TON.krise = it.posten || null; TON.blitz = Date.now(); if (it.dunkel) TON.dunkel = true; }
    if (it.effekt2 === "strom_zurueck" || (it.art === "titel" && it.text === "Morning")) TON.dunkel = false;
    if (it.art === "titel") TON.krise = null;
    if (it.posten && it.ausgang) ST.erg[it.posten] = it.ausgang;
    TON.moment = it; neu();
    if (window.EdenSfx) try {
      if (it.effekt) EdenSfx.play(it.effekt);
      if (it.effekt2) EdenSfx.play(it.effekt2, 900);
      if (it.art === "krise"){ EdenSfx.play("donner", 250); TON.donner = Date.now(); }   // Donnerschlag zu jedem Blitz
    } catch (e) {}
    let stimmeFertig = false, zeitFertig = false;
    const vielleicht = () => { if (stimmeFertig && zeitFertig && !it.warte) setTimeout(() => momentWeiter(it), FLUSS.includes(it.art) ? 150 : 500); };
    TON.laeuft = audio(it.key, () => { TON.laeuft = null; stimmeFertig = true; vielleicht(); });
    if (!TON.laeuft) stimmeFertig = true;
    TON.uhr = setTimeout(() => { zeitFertig = true; vielleicht(); },
      FLUSS.includes(it.art) && it.key ? 900 : it.art === "krise" ? 2600 : lesezeit(it.sub || it.text));
  }
  function momentWeiter(it){
    if (it && TON.moment !== it) return;
    clearTimeout(TON.uhr);
    if (TON.laeuft){ try { TON.laeuft.pause(); } catch (e) {} TON.laeuft = null; }
    const war = TON.moment, naechstes = TON.schlange[0];
    const fliessend = war && naechstes && FLUSS.includes(war.art) && naechstes.art === war.art;
    TON.moment = null; TON.pauseBis = fliessend ? 0 : Date.now() + 600;
    if (fliessend){ abspielen(); return; }
    neu(); abspielen();
  }
  function alleUeberspringen(){
    clearTimeout(TON.uhr);
    if (TON.laeuft){ try { TON.laeuft.pause(); } catch (e) {} TON.laeuft = null; }
    for (const it of TON.schlange){                    // Ergebnisse und Licht trotzdem nachziehen
      if (it.posten && it.ausgang) ST.erg[it.posten] = it.ausgang;
      if (it.art === "krise" && it.dunkel) TON.dunkel = true;
      if (it.effekt2 === "strom_zurueck" || (it.art === "titel" && it.text === "Morning")) TON.dunkel = false;
    }
    TON.schlange = []; TON.moment = null; TON.krise = null; TON.pauseBis = 0; neu();
  }
  function tonPruefen(s){
    if (ST.teil !== s.teil + "|" + s.lauf){               // neuer Teil (oder Neustart): von vorn
      ST.teil = s.teil + "|" + s.lauf; TON.letztesN = null; TON.schlange = []; TON.moment = null;
      TON.dunkel = false; TON.krise = null; ST.erg = {}; ST.plan = {}; ST.chip = null;
    }
    const maxN = Math.max(-1, ...s.log.map(e => e.n));
    const neue = s.log.filter(e => TON.letztesN === null || e.n > TON.letztesN);
    if (s.log.length) TON.letztesN = Math.max(TON.letztesN ?? -1, maxN);
    TON.schlange.push(...neue.filter(e => e.moment));
    abspielen();
  }

  function momentHtml(s){
    const m = TON.moment;
    if (!m) return "";
    const skip = `<button type="button" class="vh-skip" onclick="EdenStorm.ueberspringen()">Skip ▸▸</button>`;
    const weiter = label => `<button type="button" class="knopf vh-mweiter" onclick="EdenStorm.weiter()">${label}</button>`;
    const klick = `onclick="if(!event.target.closest('button'))EdenStorm.weiter()"`;
    const name = w => w === "duc" ? "You" : (s.namen[w] || w);
    const postTitel = po => ((s.posten.find(p => p.id === po) || {}).titel || "");
    if (m.art === "titel")
      return `<div class="vh-moment titel st-titel" onclick="EdenStorm.weiter()"><div class="vh-mkarte"><h1>${esc(m.text)}</h1>
        ${m.sub ? `<p>${esc(m.sub)}</p>` : ""}${m.warte ? weiter(m.text === "Before the Storm" ? "Begin" : "Continue") : ""}</div>${skip}</div>`;
    if (m.art === "krise")
      return `<div class="vh-moment st-krise ${m.dunkel ? "dunkel" : ""}" ${klick}><div class="st-krise-karte">
        <span class="st-zeit">${esc(m.zeit || "")}</span><h2>${esc(m.text)}</h2><p>${esc(m.sub || "")}</p></div>${skip}</div>`;
    if (m.art === "erzaehlung" || m.art === "notiz")
      return `<div class="vh-moment st-erz ${esc(m.ausgang || m.art)}" ${klick}><div class="vh-mkarte klein st-erz-karte">
        ${m.ausgang ? `<b>${esc(postTitel(m.posten)).toUpperCase()} ${IC[m.ausgang]}</b>` : m.art === "notiz" ? "<b>MEGAN</b>" : ""}
        <p>${esc(m.text)}</p>${m.warte ? weiter("See the night") : "<small>click to continue</small>"}</div>${skip}</div>`;
    if (["tratsch", "ruf", "bitte"].includes(m.art) && m.gruppe_bilder){
      const reihe = m.gruppe_bilder.map(p => {
        const bild = p.id === m.wer && m.sprite ? m.sprite : p.sprite;
        return `<div class="vh-tr-kopf ${p.id === m.wer ? "an" : ""}">${bild ? `<img src="${esc(bild)}" alt="">` : ""}<span>${esc(p.name)}</span></div>`;
      }).join("");
      const lbl = m.art === "bitte" ? "ASKS FOR · " + postTitel(m.posten).toUpperCase() : m.art === "ruf" ? "SHOUTING" : "WHISPERING";
      return `<div class="vh-moment tratsch st-${m.art} ${m.fort ? "fort" : ""}" ${klick}>
        <div class="vh-tratsch"><div class="vh-tr-blase"><b>${esc(name(m.wer).toUpperCase())} · ${esc(lbl)}</b><p>“${esc(m.text)}”</p>
        <small>click to continue</small></div><div class="vh-tr-reihe">${reihe}</div></div>${skip}</div>`;
    }
    const rolle = m.art === "zusage" || m.art === "posten_ruf" || m.art === "hilfe" ? " · " + postTitel(m.posten).toUpperCase() : (ROLLE[m.art] || "");
    return `<div class="vh-moment blase st-blase ${esc(m.art)} ${m.ausgang ? "a-" + m.ausgang : ""}" ${klick}>
      <div class="vh-mblase">${m.sprite ? `<img src="${esc(m.sprite)}" alt="">` : ""}<div><b>${esc(name(m.wer).toUpperCase())}${esc(rolle)}</b>
      <p>“${esc(m.text)}”</p>${m.warte ? weiter(m.sub || "Continue") : `<small>click to continue</small>`}</div></div>${skip}</div>`;
  }
  document.addEventListener("keydown", ev => {
    if (TON.moment && (ev.key === "Enter" || ev.key === " ")){ ev.preventDefault(); momentWeiter(TON.moment); }
  });

  // ------------------------------------------------------------------ Hilfe
  function hilfe(){ ST.hilfe = !ST.hilfe; neu(); }
  function hilfeHtml(){
    return `<div class="vh-hilfe" onclick="if(event.target===this)EdenStorm.hilfe()"><div class="vh-hilfe-box glas">
      <button type="button" class="vh-hilfe-zu" onclick="EdenStorm.hilfe()" aria-label="Close">×</button>
      <h3>How the storm works</h3>
      <p>Five posts need someone tonight. Click a person below, then a post – or drag them there. Click a post again to
        take them off. Whoever has no post <b>rests</b> and helps everyone at dawn.</p>
      <div class="vh-hilfe-grid">
        <div><b>Listen to them</b> Each person said where they'd like to go – and their answer when you assign them tells
          you whether they're sure of it.</div>
        <div><b>You</b> can take a post yourself. If you stay free instead, you can <b>run once</b> during the night to a post
          that is going wrong.</div>
        <div><b>The night</b> One crisis per post. The right person holds it (${uiIc("done", "imtext")}), a decent one only just (${uiIc("partial", "imtext")}), the wrong
          one – or nobody – loses it (${uiIc("failed", "imtext")}).</div>
        <div><b>Megan is watching</b> Four posts held: she trusts you more at the hearing. Two or fewer: less. Whoever held
          the post they asked for trusts you more.</div>
      </div></div></div>`;
  }

  // ------------------------------------------------------------------ Gesamt
  function html(z){
    const s = z.sturm;
    if (!s) return `<div class="zentrum"><p class="unter">Storm loading …</p></div>`;
    try { tonPruefen(s); } catch (e) {}
    const nacht = s.teil === "nacht";
    const blitz = TON.blitz && Date.now() - TON.blitz < 700;
    const titel = nacht ? "The night of the storm" : "Before the Storm";
    const sprint = nacht && s.sprint_frei ? `<span class="st-sprint-k" title="You stayed free: you can run to one post tonight">${uiIc("sprint", "imtext")} run once</span>` : "";
    return `<div class="vh st ${nacht ? "nacht" : "abend"} ${TON.dunkel ? "dunkel" : ""}">
      <div class="st-regen"></div>${blitz ? `<div class="st-blitz"></div>` : ""}
      ${s.megan ? `<img class="vh-fig rechts st-megan" src="${esc(s.megan)}" alt="">` : ""}
      <div class="vh-rtitel">${esc(titel)}<small>${nacht ? "Day 5 · at anchor in the bay" : "Day 5 · 18:00 · aft deck"}</small></div>
      <div class="vh-kopf glas"><span class="vh-titel">Storm</span>${sprint}
        <button type="button" class="vh-hilfe-k" onclick="EdenStorm.hilfe()" aria-label="How the storm works">?</button></div>
      ${brett(s)}${sprintHtml(s)}${endeHtml(s)}${momentHtml(s)}${ST.hilfe ? hilfeHtml() : ""}</div>`;
  }

  function leisten(){
    const an = typeof V !== "undefined" && V && V.z && V.z.status === "sturm";
    document.body.classList.toggle("st-aktiv", !!an);
  }
  // Donner ab und an (Duc 27.10.2026): alle 25-50 s ein Schlag, nachts mit Blitz, nie kurz nach einer Krise
  let naechsterDonner = Date.now() + 15000;
  function donnerAbUndAn(){
    const an = typeof V !== "undefined" && V && V.z && V.z.status === "sturm" && V.z.sturm;
    if (!an){ naechsterDonner = Date.now() + 15000; return; }
    if (Date.now() < naechsterDonner) return;
    naechsterDonner = Date.now() + 25000 + Math.random() * 25000;
    if (TON.donner && Date.now() - TON.donner < 10000) return;
    TON.donner = Date.now();
    if (V.z.sturm.teil === "nacht"){ TON.blitz = Date.now(); neu(); setTimeout(neu, 750); }
    if (window.EdenSfx) try { EdenSfx.play("donner", V.z.sturm.teil === "nacht" ? 250 : 0); } catch (e) {}
  }
  setInterval(() => {
    leisten();
    try { donnerAbUndAn(); } catch (e) {}
    if (typeof V !== "undefined" && V && V.z && V.z.status !== "sturm" && (TON.laeuft || TON.schlange.length || TON.moment)) alleUeberspringen();
  }, 400);

  window.EdenStorm = {html, senden: senden2, chip: chipWaehlen, posten: postenKlick, ziehen, ablegen, schicken, hilfe,
                      weiter: () => momentWeiter(TON.moment), ueberspringen: alleUeberspringen, _st: ST, _ton: TON};
  try { if (typeof V !== "undefined" && V && V.z && V.z.status === "sturm" && typeof zeichnen === "function"){ leisten(); zeichnen(); } }
  catch (e) {}
})();
