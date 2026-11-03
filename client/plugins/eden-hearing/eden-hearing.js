/* Spielbare Anhoerung (Variante B, 25.10.2026) - Ace-Attorney-Verhandlung vor Megan.
   Umbau "Drei Spalten" (Duc 25.10.: "Megan stellt drei Spalten dar, unten Platzhalter, Notiz anklicken und zuordnen";
   "Menues ausblenden - das ist eine Endszene"):
     - Spielleisten (Kopf, Dock, Chat, Meldungen) sind waehrend der Anhoerung ausgeblendet (body.vh-aktiv).
     - Oben links Runde, oben rechts schmale Leiste (Punkte, Adern, Hilfe); Megans letzter Satz oben mittig.
     - Drei Spalten = drei Zeilen der Aussage: "Ask" (Antwort in der Spalte), Platzhalter fuer einen Zettel, OBJECT!.
     - Unten Zettel-Thumbnails (Stapel-Reiter, nur Thema der Runde), klicken oder ziehen; "No proof?" = Bluff/Aufgeben.
   Nur Darstellung: Regeln, Adern und Urteil kommen vom Server (z.verhandlung, kern/anhoerung.py).
   Index ruft EdenHearing.html(z) in mitte(). Aktionen ueber senden('verhandlung', {was, ...}):
     anklage {pid} · press {satz} · present {fid, satz} · bluff · joker {id} · aufgeben · schliessen */
(function(){
  "use strict";
  const ST = {karte: null, ablage: null, runde: null, stapel: null, alle: false, hilfe: undefined, noproof: false,
              aussageSchl: "", verlauf: false};
  const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
  const busy = () => (typeof beschaeftigt !== "undefined" && beschaeftigt);
  const neu = () => { if (typeof zeichnen === "function") zeichnen(); };
  const KURZ = ["What?", "Who?", "Why?"];
  const RUNDE_ICON = {beweis: "done", gestaendnis: "done", bluff: "partial", verloren: "failed"};
  const KETTE_STAT = {beweis: ["done", "proven"], gestaendnis: ["done", "confessed"], bluff: ["partial", "bluffed"], verloren: ["failed", "not proven"]};
  const BLASE_ROLLE = {reaktion: " · ACCUSED", plaedoyer: " · DEFENCE", publikum: " · FROM THE CREW", zeuge: " · WITNESS",
                       zusammenbruch: " · ACCUSED", aufatmen: " · ACCUSED", blick: " · ACCUSED", gestaendnis: " · WHY",
                       urteil_reaktion: " · ON THE VERDICT", warum: " · PRESIDING", ruhe: " · PRESIDING"};
  const ZUV = {gesichert: "secured", belastbar: "solid", beobachtet: "seen", aussage: "word only"};
  const ICON = {
    monitoring: '<path d="M3 17l4-6 4 3 4-7 6 9"/><path d="M3 21h18"/>',
    computer: '<rect x="3" y="4" width="18" height="12" rx="1.5"/><path d="M8 20h8M12 16v4"/>',
    kamera: '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
    navigation: '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
    logbuch: '<path d="M5 4h11a3 3 0 013 3v13H8a3 3 0 01-3-3z"/><path d="M5 17a3 3 0 013-3h11M9 8h6"/>',
    unterlagen: '<path d="M3 7h6l2 2h10v10H3z"/><path d="M3 7V5h6l2 2"/>',
    telefon: '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a1 1 0 01-1 1A16 16 0 014 5a1 1 0 011-1z"/>',
    lupe: '<circle cx="10.5" cy="10.5" r="6"/><path d="M15 15l5.5 5.5"/>',
    person: '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0116 0"/>',
  };
  const STAPEL_ICON = {people: "person", systems: "monitoring", papers: "logbuch", own: "lupe"};
  const svg = (id, kl = "") => `<svg class="ic ${kl}" viewBox="0 0 24 24" aria-hidden="true">${ICON[id] || ""}</svg>`;
  const avatarHtml = url => typeof avatar === "function" ? avatar(url) : `<span class="av" style="background-image:url('${esc(url)}')"></span>`;

  // ------------------------------------------------------------------ Aktionen
  function senden2(was, extra){ if (!busy()) senden("verhandlung", Object.assign({was}, extra || {}), "…"); }
  function karteWaehlen(fid){
    ST.karte = ST.karte === fid ? null : fid;
    if (ST.karte && ST.ablage && ST.ablage.fid === fid) ST.ablage = null;
    neu();
  }
  function platz(i){                                   // Platzhalter einer Spalte angeklickt
    if (ST.karte){ ST.ablage = {i, fid: ST.karte}; ST.karte = null; }
    else if (ST.ablage && ST.ablage.i === i) ST.ablage = null;      // liegender Zettel zurueck auf den Tisch
    neu();
  }
  function einspruch(i){
    if (!ST.ablage || ST.ablage.i !== i) return;
    const a = ST.ablage; ST.ablage = null;
    senden2("present", {fid: a.fid, satz: a.i});
  }
  function fragen(i){ senden2("press", {satz: i}); }
  // Gefuehrte erste Zeile (Duc 29.10.2026): nur in der allerersten Anhoerung, Punkt 1, danach nie wieder (Browser merkt es).
  // Schritte: 1 "Ask line X" -> 2 "Place a note here" -> 3 "OBJECT!". Erledigt, sobald ein Zettel auf dieser Zeile liegt und
  // vorgelegt wurde oder Punkt 1 vorbei ist.
  const FUEHRUNG_SCHL = "eden.hearing.gefuehrt";
  function fuehrungFertig(){ try { return !!localStorage.getItem(FUEHRUNG_SCHL); } catch (e) { return true; } }
  function fuehrungAus(){ try { localStorage.setItem(FUEHRUNG_SCHL, "1"); } catch (e) {} }
  function fuehrungPruefen(v){
    if (fuehrungFertig()) return;
    if (v.runde > 0 || v.fertig || (v.log || []).some(e => e.art === "karte")) fuehrungAus();
  }
  function fuehrungHtml(v, i, s, lieg){
    if (fuehrungFertig() || v.fuehrung == null || v.fuehrung !== i || busy()) return "";
    const tipp = !s.gepresst ? `<b>Try it: Ask line ${i + 1}.</b> Something about it doesn't sit right – press the witness on it.`
      : !lieg ? `<b>Place a note here.</b> The glowing stack below holds a note that contradicts this line – drag it onto this column.`
      : `<b>Now: OBJECT!</b> If the note really contradicts the line, the point is yours.`;
    return `<div class="vh-fuehrung" role="status">${tipp}<small>First hearing only · all rules under “?”</small></div>`;
  }
  function ziehen(ev, fid){ try { ev.dataTransfer.setData("text/plain", fid); } catch (e) {} ST.karte = fid; }
  function ablegen(ev, i){ ev.preventDefault(); const fid = (ev.dataTransfer && ev.dataTransfer.getData("text/plain")) || ST.karte;
    if (fid){ ST.ablage = {i, fid}; ST.karte = null; neu(); } }
  function stapel(id){ ST.stapel = id; neu(); }
  function alleZeigen(){ ST.alle = !ST.alle; neu(); }
  function noproof(){ ST.noproof = !ST.noproof; neu(); }
  function verlauf(){ ST.verlauf = !ST.verlauf; neu(); }

  // ------------------------------------------------------------------ Teile
  function kopf(v){
    const kette = v.runden.map((r, i) => {
      const kl = r.ergebnis ? (r.ergebnis === "verloren" ? "aus" : "ok") : (i === v.runde ? "jetzt" : "");
      const ic = r.ergebnis ? uiIc(RUNDE_ICON[r.ergebnis], "imtext") : (i === v.runde ? "●" : "○");
      return `<span class="vh-glied ${kl}" title="${esc(r.titel)}">${ic} ${KURZ[i]}</span>`;
    }).join("");
    const adern = "●".repeat(v.adern) + "○".repeat(Math.max(0, v.max - v.adern));
    if (ST.adernAlt !== undefined && v.adern < ST.adernAlt){             // eine Ader platzt: Klang + Ruck
      ST.platztBis = Date.now() + 900;
      if (window.EdenSfx) try { EdenSfx.play("wuerfel_fehlschlag"); } catch (e) {}
      setTimeout(neu, 950);
    }
    ST.adernAlt = v.adern;
    const platzt = ST.platztBis && ST.platztBis > Date.now();
    return `<div class="vh-kopf glas"><span class="vh-titel">Hearing</span>${kette}
      <span class="vh-adern ${platzt ? "platzt" : ""}" title="Megan's patience: a true line attacked or a note that doesn't fit −1, failed bluff −2">${adern}</span>
      <button type="button" class="vh-hilfe-k" onclick="EdenHearing.hilfe()" aria-label="How the hearing works">?</button></div>`;
  }

  function rundenTitel(v){
    if (v.fertig) return `<div class="vh-rtitel">The questioning is over</div>`;
    return `<div class="vh-rtitel">${esc(v.titel || "")}<small>Point ${Math.min(v.runde + 1, 3)} of 3${v.stufe ? " · revised testimony" : ""}</small></div>`;
  }

  function buehne(v){
    const rolle = (f, i) => f.id === "megan" ? "Presiding" : (i === 1 ? "Accused" : "Witness");
    const ungeduldig = TON.ungeduldZeile && TON.ungeduldZeile.bis > Date.now();
    // Paket A (Duc 28.10.2026): f.sprite is the LAST feeling in the finished log - while a line plays, the figure on stage
    // shows that line's feeling instead (sprite fits the moment, not the end of the batch)
    const m = TON.moment;
    let h = v.figuren.map((f, i) => {
      const seite = f.id === "megan" ? "rechts" : (i === 1 ? "links" : "mitte");
      const jetzt = m && m.wer === f.id && m.sprite;
      const bild = jetzt ? m.sprite : f.id === "megan" && ungeduldig && v.megan_ungeduld ? v.megan_ungeduld : f.sprite;
      const spricht = m && m.wer ? m.wer === f.id : f.spricht || (f.id === "megan" && ungeduldig);
      return (bild ? `<img class="vh-fig ${seite} ${spricht ? "spricht" : ""}" src="${esc(bild)}" alt="">` : "")
        + `<div class="vh-schild ${seite}"><small>${rolle(f, i)}</small>${esc(f.name)}</div>`;
    }).join("");
    if (v.zeuge) h += `<div class="vh-schild zeuge ${v.zeuge.anruf ? "anruf" : ""}">${v.zeuge.sprite ? avatarHtml(v.zeuge.sprite) : ""}
      <span><small>Witness${v.zeuge.anruf ? " · on call" : ""}</small>${esc(v.zeuge.name)}</span></div>`;
    if (v.angeklagt === "niemand") h += `<div class="vh-schild links"><small>Your claim</small>Nobody alone</div>`;
    else if (!v.angeklagt) h += `<div class="vh-platz"><div class="vh-silhouette">${svg("person")}</div></div>
      <div class="vh-schild links offen"><small>Accused</small>Not named yet</div>`;
    return h;
  }

  function megansatz(v){
    const u = TON.ungeduldZeile;
    if (u && u.bis > Date.now()) return `<div class="vh-megan ungeduld"><b>MEGAN</b>“${esc(u.text)}”</div>`;
    const e = [...v.log].reverse().find(x => x.wer !== "duc" && x.satz === undefined && (!x.moment || x.art === "punkt"));   // Spalten-Antworten stehen in der Spalte
    if (!e) return "";
    return `<div class="vh-megan"><b>${esc((v.namen[e.wer] || e.wer).toUpperCase())}</b>“${esc(e.text)}”</div>`;
  }

  function spalten(v){
    const a = v.aussage;
    if (!a) return "";
    const schl = a.saetze.map(s => s.text).join("|");
    if (ST.aussageSchl !== schl){ ST.aussageSchl = schl; ST.ablage = null; }
    const karten = Object.fromEntries(v.karten.map(k => [k.id, k]));
    const zuSatz = i => v.log.filter(e => e.satz === i && e.r === v.runde);
    // Ablehnung mit Grund (Duc 28.10.2026): alle Gruende sehen aus wie die alte Ablehnung (gleiche Farbe)
    const ABLEHNUNG = ["falsche_karte", "anderer_punkt", "nur_aussage", "andere_behauptung", "warum_nicht"];
    return `<div class="vh-spalten n${a.saetze.length}">${a.saetze.map((s, i) => {
      const eintraege = zuSatz(i);
      const antwort = [...eintraege].reverse().find(e => e.art === "press");
      const gedanke = [...eintraege].reverse().find(e => e.art === "gedanke");   // Ducs Frage im Kopf
      const nervoes = [...eintraege].reverse().find(e => e.art === "nervoes");   // die Angeklagte stockt

      const passt = [...eintraege].reverse().find(e => e.art === "bestaetigt");   // wahre Zeile, von einem Zettel gestuetzt
      const urteil = [...eintraege].reverse().find(e => ABLEHNUNG.includes(e.art) || ["satz_haelt", "luecke"].includes(e.art));
      const lieg = ST.ablage && ST.ablage.i === i ? karten[ST.ablage.fid] : null;
      const slot = lieg
        ? `<button type="button" class="vh-slot voll" onclick="EdenHearing.platz(${i})" title="Take the note back">${mini(lieg)}</button>
           <button type="button" class="vh-object" ${busy() ? "disabled" : ""} onclick="EdenHearing.einspruch(${i})">OBJECT!</button>`
        : `<button type="button" class="vh-slot ${ST.karte ? "bereit" : ""}" onclick="EdenHearing.platz(${i})"
             ondragover="event.preventDefault()" ondrop="EdenHearing.ablegen(event,${i})">${ST.karte ? "Place your note here" : "Place a note here"}</button>`;
      const liest = TON.liest && (TON.liest.key === s.key || (TON.liest.satz === i && TON.liest.r === v.runde));
      const fuehr = fuehrungHtml(v, i, s, lieg);
      return `<div class="vh-sp ${fuehr ? "gefuehrt" : ""} ${lieg ? "aktiv" : ""} ${urteil ? "u-" + (ABLEHNUNG.includes(urteil.art) ? "falsche_karte" : urteil.art) : ""} ${passt ? "geprueft" : ""} ${liest ? "liest" : ""}">
        <div class="vh-nr">LINE ${i + 1} · ${esc((a.name || "").toUpperCase())}</div>
        <div class="vh-text">“${esc(s.text)}”</div>
        <button type="button" class="vh-ask" ${busy() ? "disabled" : ""} onclick="EdenHearing.fragen(${i})">${s.gepresst ? "Ask again" : "Ask"}</button>
        ${antwort ? `<div class="vh-antwort">“${esc(antwort.text)}”${nervoes ? `<em class="vh-nervoes">${esc((v.namen[nervoes.wer] || "").toUpperCase())} · “${esc(nervoes.text)}”</em>` : ""}${gedanke ? `<i>${esc(gedanke.text)}</i>` : ""}</div>` : ""}
        ${passt ? `<div class="vh-passt"><b>${uiIc("done", "imtext")} Fits your note</b>${esc(passt.text)}</div>` : ""}
        ${urteil ? `<div class="vh-urteil">${esc(urteil.text)}</div>` : ""}
        ${fuehr}${slot}</div>`;
    }).join("")}</div>`;
  }

  function mini(k){
    const pin = k.portrait ? avatarHtml(k.portrait) : `<span class="vh-pin">${svg(k.icon)}</span>`;
    return `<span class="vh-mini">${pin}<span class="vh-schrift">${esc(k.klar || k.text)}</span></span>`;
  }

  function tray(v){
    if (ST.runde !== v.runde){ ST.runde = v.runde; ST.karte = null; ST.ablage = null; ST.stapel = null; ST.alle = false; ST.noproof = false; }
    const rid = (v.runden[v.runde] || {}).id;
    const thema = ST.alle || !rid ? v.karten : v.karten.filter(k => (k.runden || []).includes(rid));
    const zahl = id => thema.filter(k => k.stapel === id).length;
    const tipp = v.tipp_stapel && zahl(v.tipp_stapel) ? v.tipp_stapel : null;
    const offen = (ST.stapel && zahl(ST.stapel) ? ST.stapel : null) || tipp || (v.stapel.find(s => zahl(s.id)) || {}).id || "people";
    const reiter = v.stapel.map(s => `<button type="button" class="vh-stapel ${s.id === offen ? "offen" : ""} ${tipp === s.id ? "tipp" : ""}"
      ${zahl(s.id) ? "" : "disabled"} onclick="EdenHearing.stapel('${s.id}')">${svg(STAPEL_ICON[s.id])}<span>${esc(s.titel)}</span><b>${zahl(s.id)}</b></button>`).join("")
      + `<button type="button" class="vh-alle" onclick="EdenHearing.alle()">${ST.alle ? "only this point" : "show all notes"}</button>`;
    const daliegt = ST.ablage ? ST.ablage.fid : null;
    const thumbs = thema.filter(k => k.stapel === offen).map((k, n) => {
      const pin = k.portrait ? avatarHtml(k.portrait) : `<span class="vh-pin">${svg(k.icon)}</span>`;
      return `<button type="button" draggable="true" ondragstart="EdenHearing.ziehen(event,'${esc(k.id)}')"
        class="vh-th f${n % 3} ${ST.karte === k.id ? "gewaehlt" : ""} ${daliegt === k.id ? "weg" : ""}" title="${esc(k.text)}"
        onclick="EdenHearing.karte('${esc(k.id)}')">${pin}<span class="vh-quelle">${esc(k.wer)}${ZUV[k.zuv] ? " · " + ZUV[k.zuv] : ""}</span>
        <span class="vh-schrift">${esc(k.klar || k.text)}</span></button>`;
    }).join("") + v.joker.map(j => `<button type="button" class="vh-th joker" ${busy() ? "disabled" : ""}
        onclick="EdenHearing.senden('joker',{id:'${esc(j.id)}'})"><span class="vh-quelle">Joker · +${j.plus} ●</span>
        <span class="vh-schrift">${esc(j.label)}</span></button>`).join("");
    const b = v.bluff;
    const np = ST.noproof ? `<div class="vh-np-menu glas">
        <button type="button" ${busy() ? "disabled" : ""} onclick="EdenHearing.senden('bluff')"><b>Bluff</b><small>${esc(b.wert)} +${b.bonus} vs ${b.sg} · if it fails −2 ●</small></button>
        <button type="button" ${busy() ? "disabled" : ""} onclick="EdenHearing.senden('aufgeben')"><b>Give up this point</b><small>it stays open and counts against you</small></button></div>` : "";
    const wer = v.aussage && v.angeklagt && v.aussage.sprecher === v.angeklagt ? (v.namen[v.angeklagt] || "") : "";
    const hinweis = v.schritt === "anklage" ? "Go through your notes – then name a person above."
      : wer && !ST.karte ? `Ask about each line and watch how ${wer} reacts – then lay a note on the one that's wrong.`
      : ST.karte ? "Now click a line's empty slot above." : "Pick a note – or drag it onto a line.";
    return `<div class="vh-tisch"><div class="vh-reiter">${reiter}</div>
      <div class="vh-tray-mitte"><div class="vh-tray-hinweis">${hinweis}</div><div class="vh-thumbs">${thumbs || `<p class="vh-leer">No notes here.</p>`}</div></div>
      <div class="vh-np">${np}<button type="button" class="vh-np-k" onclick="EdenHearing.noproof()">No proof? ${ST.noproof ? "▴" : "▾"}</button></div></div>`;
  }

  function anklage(v){
    return `<div class="vh-anklage-box"><div class="vh-frage">Who do you name before Megan?</div>
      <div class="vh-wahl">${v.verdaechtige.map(p => `<button class="vh-person" type="button" ${busy() ? "disabled" : ""}
        onclick="EdenHearing.senden('anklage',{pid:'${esc(p.id)}'})">${p.sprite ? avatarHtml(p.sprite) : `<i>∅</i>`}<span>${esc(p.name)}</span></button>`).join("")}</div></div>`;
  }

  function rolleHtml(v){
    return `<div class="vh-anklage-box vh-wahlbox"><div class="vh-frage">Megan asks about your own part that night.</div>
      <div class="vh-wkarten">
        <button type="button" class="vh-wk" ${busy() ? "disabled" : ""} onclick="EdenHearing.senden('rolle',{ehrlich:true})">
          <b>Tell the truth about your night</b><small>Everything – including what you did wrong. Megan counts honesty.</small></button>
        <button type="button" class="vh-wk" ${busy() ? "disabled" : ""} onclick="EdenHearing.senden('rolle',{ehrlich:false})">
          <b>Say nothing</b><small>Keep your own part to yourself.</small></button></div></div>`;
  }
  // Duc himself (29.10.2026): his front portrait from the Character menu (jacket + weapon) at the plea and the OBJECTION!
  function duc(v, klasse){ return v.duc_sprite ? `<img class="vh-duc ${klasse}" src="${esc(v.duc_sprite)}" alt="">` : ""; }
  function plaedoyerHtml(v){
    const liste = (v.erbarmen || []).map(e => `<li class="${e.ok ? "ok" : "nein"}">${uiIc(e.ok ? "done" : "failed", "imtext")} ${esc(e.text)}</li>`).join("");
    const kopf = v.duc_sprite ? `<span class="vh-duc-plea" style="background-image:url('${esc(v.duc_sprite)}')"></span>` : "";   // face only
    return `<div class="vh-anklage-box vh-wahlbox">${kopf}<div class="vh-frage">Your plea. What do you ask Megan for?</div>
      <div class="vh-wkarten">${(v.plaedoyer || []).map(p => `<button type="button" class="vh-wk ${p.id}" ${busy() ? "disabled" : ""}
        onclick="EdenHearing.senden('plaedoyer',{art:'${esc(p.id)}'})"><b>${esc(p.titel)}</b><small>${esc(p.text)}</small></button>`).join("")}</div>
      ${liste ? `<div class="vh-gnade"><b>Megan only shows mercy if:</b><ul>${liste}</ul></div>` : ""}</div>`;
  }
  function ende(v){
    const n = v.runden.filter(r => ["beweis", "gestaendnis", "bluff"].includes(r.ergebnis)).length;
    const folgen = [v.rolle_ehrlich === true ? "You told Megan the truth about your night." : v.rolle_ehrlich === false
      ? "You kept your own part to yourself." : "", v.urteil_text ? "Verdict: " + v.urteil_text : ""]
      .filter(Boolean).map(z => `<li>${esc(z)}</li>`).join("");
    const b = v.bilanz;
    const punkte = v.runden.map((r, i) => `<li><span>${KURZ[i]}</span><b class="${r.ergebnis === "verloren" ? "aus" : "ok"}">${
      {beweis: uiIc("done", "imtext") + " proven", gestaendnis: uiIc("done", "imtext") + " confessed", bluff: uiIc("partial", "imtext") + " half / bluffed", verloren: uiIc("failed", "imtext") + " not proven"}[r.ergebnis] || "–"}</b></li>`).join("");
    return `<div class="vh-anklage-box vh-ende vh-bilanz"><div class="vh-frage">Your hearing</div>
      <ul class="vh-bpunkte">${punkte}<li><span>Megan's patience</span><b>${"●".repeat(v.adern)}${"○".repeat(Math.max(0, v.max - v.adern))}</b></li>
      ${b ? `<li><span>Notes found</span><b>${b.gefunden} of ${b.gesamt}</b></li>` : ""}</ul>
      ${folgen ? `<ul class="vh-folgen">${folgen}</ul>` : ""}${b && b.besser ? `<p class="vh-besser">A different verdict was possible.</p>` : ""}
      <button class="knopf" type="button" ${busy() ? "disabled" : ""} onclick="EdenHearing.senden('schliessen')">Continue</button></div>`;
  }

  function verlaufHtml(v){
    if (!ST.verlauf) return `<button type="button" class="vh-verlauf-k" onclick="EdenHearing.verlauf()">history</button>`;
    const name = w => w === "duc" ? "You" : (v.namen[w] || w);
    return `<div class="vh-verlauf glas"><button type="button" class="vh-verlauf-k" onclick="EdenHearing.verlauf()">close</button>
      ${v.log.map(e => `<div class="vh-zeile"><b>${e.wer === "duc" && v.duc_sprite ? avatarHtml(v.duc_sprite) : ""}${esc(name(e.wer))}</b><span>${esc(e.text)}</span></div>`).join("")}</div>`;
  }

  // ------------------------------------------------------------------ Hilfe
  const ICON_LEGENDE = [["monitoring", "Monitoring", "ship monitoring, inverter module, meters"],
    ["computer", "Office PC", "office computer and printer"], ["kamera", "Camera", "on-board camera footage"],
    ["navigation", "Navigation", "chart plotter and course data"], ["logbuch", "Logbook", "engine log, captain's log, notebooks, books"],
    ["unterlagen", "Files", "folders, manufacturer papers, notices, head office"], ["telefon", "Phone", "calls and phone records"],
    ["lupe", "You", "what you saw or worked out yourself"]];
  function hilfe(){ ST.hilfe = !ST.hilfe; try { localStorage.setItem("eden.hearing.hilfe", "1"); } catch (e) {} neu(); }
  function hilfeHtml(){
    const leg = ICON_LEGENDE.map(([id, n, t]) => `<li><span class="vh-pin">${svg(id)}</span><b>${n}</b><span>${t}</span></li>`).join("");
    return `<div class="vh-hilfe" onclick="if(event.target===this)EdenHearing.hilfe()"><div class="vh-hilfe-box glas">
      <button type="button" class="vh-hilfe-zu" onclick="EdenHearing.hilfe()" aria-label="Close">×</button>
      <h3>How the hearing works</h3>
      <p>Megan wants three points proven, one after another: <b>What?</b> happened that night, <b>Who?</b> did it,
        and <b>Why?</b> it could break the drive. In each point someone makes a statement of three lines – one column
        each. <b>Two lines are true, one is wrong.</b> You don't have to guess: compare the lines with what you found
        this week. The line that clashes with one of your notes is the wrong one – put that note into its column and
        object.</p>
      <div class="vh-hilfe-grid">
        <div><b>Ask</b> Ask about a line, as often as you like, for free. If you have a note that backs a line up, it
          shows <b>${uiIc("done", "imtext")} Fits your note</b> – that line is true. If something doesn't sit right, you'll notice, and the
          stack with the right note starts to glow.</div>
        <div><b>Place a note</b> Click a note below, then the empty slot of a line – or drag it there. Click it again to
          take it back.</div>
        <div><b>OBJECT!</b> It counts if your note proves that line wrong – and you know the rest of the evidence that goes
          with it. If something is missing, Megan asks for more; that costs nothing.</div>
        <div><b>Megan's patience ●</b> Attacking a true line or using a note that doesn't fit costs one. At zero she stops
          listening and decides herself.</div>
        <div><b>No proof?</b> Bluff with Charm or Cunning against 14 (it counts, but mercy needs real proof; failing costs
          two ●) – or give the point up.</div>
        <div><b>Jokers</b> Some items calm Megan down (+1 ●). They appear as green notes.</div>
      </div>
      <p class="vh-hilfe-klein">In <b>Who?</b> you first name a person, who then answers for themselves. If you accuse the
        wrong one, the proof points elsewhere – the point is lost. Top right: ${uiIc("done", "imtext")} proven · ${uiIc("partial", "imtext")} bluffed · ${uiIc("failed", "imtext")} lost.</p>
      <h3>Your notes</h3>
      <p>Everything you found this week sits on the desk in four stacks: <b>People</b> (with the face of whoever told
        you), <b>Ship systems</b>, <b>Papers &amp; logs</b> and <b>Your own findings</b>. Each point only shows the notes
        on its topic – the right ones and the misleading ones; “show all notes” lifts the filter. Each note says in plain
        words what you found. Most reliable first: <i>secured</i> &gt; <i>solid</i> &gt; <i>seen</i> &gt; <i>word only</i>.</p>
      <ul class="vh-legende">${leg}<li><span class="vh-pin vh-pin-av">${svg("person")}</span><b>Face</b><span>a person told you this</span></li></ul>
    </div></div>`;
  }

  // ------------------------------------------------------------------ Stimme + Momente (Duc 25.10.: "vertont, geht automatisch
  // los" / "Uebergaenge fehlen"). Eine Warteschlange fuer alles Neue im Log: normale Saetze werden nur abgespielt,
  // Momente (Titelkarte, OBJECTION!, Saal, Reaktion, Plaedoyer, Punkt) zusaetzlich gross gezeigt. Momente mit "warte"
  // gehen erst auf Klick weiter, die anderen nach der Stimme bzw. einer Lesezeit. Eine neue Aussage wird danach
  // vorgelesen. Eine Handlung des Spielers bricht laufende Saetze (nicht Momente) ab, damit die Antwort sofort kommt.
  const TON = {letztesN: null, schlange: [], laeuft: null, aussage: "", aktiv: Date.now(), ungeduld: 0, ungeduldZeile: null,
               moment: null, uhr: null};
  function tonAn(){ return typeof STIMME === "undefined" || STIMME; }
  function audio(key, fertig){
    if (!key || !tonAn()){ fertig(); return null; }
    let a;
    try { a = new Audio("/api/zeile?id=" + encodeURIComponent(key)); if (typeof mitTempo === "function") mitTempo(a); }
    catch (e) { fertig(); return null; }
    let fertigGemeldet = false;
    const ende = () => { if (!fertigGemeldet){ fertigGemeldet = true; fertig(); } };
    a.addEventListener("ended", ende); a.addEventListener("error", ende);
    a.play().catch(ende);
    return a;
  }
  const lesezeit = text => Math.min(8000, 2000 + String(text || "").length * 55);
  const ATEM = 700;                                    // kurze Pause zwischen zwei Momenten
  const FLUSS = ["tratsch", "plaedoyer", "gestaendnis", "zusammenbruch"];   // laufen ohne Aus-/Einblenden durch
  // Gestaendnis (Duc 27.10.2026): leise traurige Musik ab Megans "Why?" bis zur Titelkarte "The Verdict", dann wieder
  // die Musik des Servers (bei Rolle und Plaedoyer Stille).
  function musikMoment(art){
    if (!window.EdenMusic || !EdenMusic.vorrang) return;
    const g = typeof V !== "undefined" && V && V.musik && V.musik.gestaendnis;
    if ((art === "warum" || art === "gestaendnis") && g){ if (!TON.gMusik){ TON.gMusik = true; EdenMusic.vorrang(g); } }
    else if (TON.gMusik && (art === "titel" || art === null)){ TON.gMusik = false; EdenMusic.vorrang(null); }
  }
  function abspielen(){
    if (TON.laeuft || TON.moment || !TON.schlange.length) return;
    if (TON.pauseBis && Date.now() < TON.pauseBis){ setTimeout(abspielen, TON.pauseBis - Date.now() + 10); return; }
    const it = TON.schlange.shift();
    if (it.moment){
      it.fort = FLUSS.includes(it.art) && TON.letzteArt === it.art;   // Fortsetzung derselben Szene (kein Einblenden)
      TON.letzteArt = it.art;
      musikMoment(it.art);
      TON.moment = it; neu();
      if (window.EdenSfx) try {                       // OBJECTION!: erst knallt der Zettel, dann der Stinger
        const slam = it.art === "objection";
        if (slam) EdenSfx.play("anhoerung_slam");
        if (it.effekt) EdenSfx.play(it.effekt, slam ? 220 : 0);
        if (it.effekt2) EdenSfx.play(it.effekt2, 900);   // z. B. nach dem Hammer der Ausgangs-Klang
      } catch (e) {}
      let stimmeFertig = false, zeitFertig = false;
      const vielleicht = () => { if (stimmeFertig && zeitFertig && !it.warte) setTimeout(() => momentWeiter(it), FLUSS.includes(it.art) ? 150 : 500); };
      TON.laeuft = audio(it.key, () => { TON.laeuft = null; stimmeFertig = true; vielleicht(); });
      if (!TON.laeuft) stimmeFertig = true;
      TON.uhr = setTimeout(() => { zeitFertig = true; vielleicht(); }, it.art === "objection" ? 1500
        : FLUSS.includes(it.art) && it.key ? 900 : lesezeit(it.text));   // im Fluss gibt die Stimme den Takt vor
      return;
    }
    // Erst als "laeuft" markieren, dann neu zeichnen - sonst startet html() -> tonPruefen() den Abspieler ein zweites
    // Mal und die ganze Warteschlange rauscht auf einmal durch.
    TON.letzteArt = null;
    TON.laeuft = "spricht"; TON.liest = it; neu();      // Spalte der gerade gesprochenen Zeile hervorheben
    // Zeilen der Aussage leuchten mindestens eine Lesezeit lang - auch ohne Ton (stumm, Autoplay gesperrt)
    let a = null, tonFertig = false, zeitFertig = !it.zeile, erledigt = false;
    const weiter = () => {
      if (!tonFertig || !zeitFertig || erledigt) return;
      erledigt = true;
      if (TON.laeuft === a || TON.laeuft === "spricht") TON.laeuft = null;
      TON.liest = null; neu(); abspielen();
    };
    if (it.zeile) setTimeout(() => { zeitFertig = true; weiter(); }, Math.min(3500, lesezeit(it.text)));
    a = audio(it.key, () => { tonFertig = true; weiter(); });
    if (a && !erledigt) TON.laeuft = a;
  }
  function momentWeiter(it){
    if (it && TON.moment !== it) return;
    clearTimeout(TON.uhr);
    if (TON.laeuft){ try { TON.laeuft.pause(); } catch (e) {} TON.laeuft = null; }
    const war = TON.moment, naechstes = TON.schlange[0];
    const fliessend = war && naechstes && naechstes.moment && FLUSS.includes(war.art)
      && (naechstes.art === war.art || (war.art === "tratsch" && naechstes.art === "ruhe"));
    TON.moment = null; TON.aktiv = Date.now(); TON.pauseBis = fliessend ? 0 : Date.now() + ATEM;
    if (fliessend){ abspielen(); return; }            // kein leeres Bild zwischen zwei Tuschel-Zeilen
    neu(); abspielen();
  }
  function alleUeberspringen(){
    clearTimeout(TON.uhr);
    if (TON.laeuft){ try { TON.laeuft.pause(); } catch (e) {} TON.laeuft = null; }
    TON.schlange = []; TON.moment = null; TON.pauseBis = 0; TON.aktiv = Date.now(); musikMoment(null); neu();
  }
  function stoppen(){
    if (TON.laeuft && !TON.moment){ try { TON.laeuft.pause(); } catch (e) {} TON.laeuft = null; }
    TON.schlange = TON.schlange.filter(x => x.moment);
  }
  function tonPruefen(v){
    const maxN = Math.max(-1, ...v.log.map(e => e.n));
    if (TON.letztesN !== null && maxN < TON.letztesN){  // Anhoerung neu begonnen (Neustart): Protokoll faengt bei 0 an
      alleUeberspringen(); TON.letztesN = null; TON.aussage = "";
    }
    const erste = TON.letztesN === null;
    const neue = erste ? v.log.filter(e => e.r === undefined && (e.key || e.moment)) : v.log.filter(e => e.n > TON.letztesN);
    if (v.log.length) TON.letztesN = Math.max(TON.letztesN ?? -1, ...v.log.map(e => e.n));
    const items = neue.filter(e => e.key || e.moment);
    if (items.length && !erste) stoppen();
    if (items.length) TON.aktiv = Date.now();
    TON.schlange.push(...items);
    const aSchl = v.aussage ? v.aussage.saetze.map(s => s.key || s.text).join("|") : "";
    if (aSchl && aSchl !== TON.aussage){
      TON.aussage = aSchl;
      TON.schlange.push(...v.aussage.saetze.filter(s => s.key).map(s => ({key: s.key, text: s.text, zeile: true})));
      TON.ungeduld = 0;
    }
    abspielen();
  }
  function momentHtml(v){
    const m = TON.moment;
    if (!m) return "";
    const skip = `<button type="button" class="vh-skip" onclick="EdenHearing.ueberspringen()">Skip ▸▸</button>`;
    const weiter = label => `<button type="button" class="knopf vh-mweiter" onclick="EdenHearing.weiter()">${label}</button>`;
    const name = w => w === "duc" ? "You" : (v.namen[w] || w);
    // whoever stands on stage already shows the line's sprite there - no second, tiny copy in the bubble (Paket A 28.10.2026)
    const klein = m.sprite && !v.figuren.some(f => f.id === m.wer) ? `<img src="${esc(m.sprite)}" alt="">` : "";
    if (m.art === "nachbessern")
      return `<div class="vh-moment blase nachbessern" onclick="if(!event.target.closest('button'))EdenHearing.weiter()">
        <div class="vh-mblase">${klein}<div><b>${esc(name(m.wer).toUpperCase())} · BACKPEDALLING</b>
        <p>“${esc(m.text)}”</p><small>click to continue</small></div></div>${skip}</div>`;
    if (m.art === "bericht")                           // der Werftbericht liegt auf dem Tisch, Megan erklaert ihn (27.10.2026)
      return `<div class="vh-moment bericht" onclick="if(!event.target.closest('button'))EdenHearing.weiter()">
        <div class="vh-bericht"><div class="vh-blatt"><b>EDEN MARINE WORKS · REPAIR &amp; SURVEY</b><h2>Incident Report</h2>
        <dl><dt>Subject</dt><dd>Main drive, total failure</dd><dt>Finding</dt><dd>Wear and tear</dd>
        <dt>Liability</dt><dd>None identified</dd></dl><span class="vh-stempel">Preliminary</span></div>
        <div class="vh-mkarte klein"><b>MEGAN</b><p>“${esc(m.text)}”</p>${m.warte ? weiter("Read the report") : ""}</div></div>${skip}</div>`;
    if (m.art === "titel")
      return `<div class="vh-moment titel" onclick="EdenHearing.weiter()"><div class="vh-mkarte"><h1>${esc(m.text)}</h1>
        ${m.sub ? `<p>${esc(m.sub)}</p>` : ""}${m.tipp ? `<p class="vh-tafel-tipp">${uiIc("memory", "imtext")} ${esc(m.tipp)}</p>` : ""}${m.warte ? weiter(m.knopf || (m.text === "The Hearing" ? "Begin" : "Continue")) : ""}</div>${skip}</div>`;
    if (m.art === "objection"){
      const karte = [...v.log].reverse().find(e => e.art === "karte" && e.n < m.n);
      return `<div class="vh-moment objection" onclick="EdenHearing.weiter()">${karte ? `<div class="vh-slam">${esc(karte.text)}</div>` : ""}
        ${duc(v, "vh-duc-objection")}<div class="vh-objection">${esc(m.text)}</div>${skip}</div>`;
    }
    if (m.art === "kette"){                            // What / Who / Why als Zettel am Brett, roter Faden dazwischen
      const zettel = (m.kette || []).map((e, i) => {
        const s = KETTE_STAT[e];
        const neu = i === 2 && ["zu", "zu_teil", "riss"].includes(m.zustand);
        return `<div class="vh-kz ${!e ? "leer" : e === "verloren" ? "aus" : "ok"} ${neu ? "neu" : ""}"><b>${KURZ[i]}</b>
          <span>${s ? s[0] : "?"}</span><small>${s ? s[1] : "still open"}</small></div>`;
      }).join(`<i class="vh-faden"></i>`);
      return `<div class="vh-moment kette ${esc(m.zustand || "")}" onclick="if(!event.target.closest('button'))EdenHearing.weiter()">
        <div class="vh-mkarte vh-brett"><div class="vh-kzeile">${zettel}</div><b>MEGAN</b><p>“${esc(m.text)}”</p>
        ${m.warte ? weiter(m.sub || "Continue") : `<small>click to continue</small>`}</div>${skip}</div>`;
    }
    if (m.art === "tratsch" || (m.art === "plaedoyer" && m.gruppe_bilder)){   // Reihe bleibt, die sprechende Person leuchtet
      const reihe = (m.gruppe_bilder || []).map(p => {
        const bild = p.id === m.wer && m.sprite ? m.sprite : p.sprite;
        return `<div class="vh-tr-kopf ${p.id === m.wer ? "an" : ""}">${bild ? `<img src="${esc(bild)}" alt="">` : ""}<span>${esc(p.name)}</span></div>`;
      }).join("");
      return `<div class="vh-moment tratsch ${m.art} ${m.fort ? "fort" : ""}" onclick="if(!event.target.closest('button'))EdenHearing.weiter()">
        <div class="vh-tratsch ${m.art}"><div class="vh-tr-blase"><b>${esc(name(m.wer).toUpperCase())} · ${m.art === "plaedoyer" ? "DEFENCE" : "WHISPERING"}</b><p>“${esc(m.text)}”</p>
        <small>click to continue</small></div><div class="vh-tr-reihe">${reihe}</div></div>${skip}</div>`;
    }
    if (["punkt", "geduld_weg", "ende", "urteil"].includes(m.art))
      return `<div class="vh-moment punkt ${m.art} ${m.effekt === "blackout" ? "dunkel" : ""}" onclick="if(!event.target.closest('button'))EdenHearing.weiter()">
        <div class="vh-mkarte klein"><b>MEGAN${m.art === "urteil" ? " · THE VERDICT" : ""}</b><p>“${esc(m.text)}”</p>${weiter("Continue")}</div>${skip}</div>`;
    return `<div class="vh-moment blase ${esc(m.art)} ${m.anruf ? "anruf" : ""} ${m.fort ? "fort" : ""}" onclick="if(!event.target.closest('button'))EdenHearing.weiter()">
      <div class="vh-mblase">${klein}<div><b>${esc(name(m.wer).toUpperCase())}${
        m.anruf ? " · WITNESS · VIDEO CALL" : BLASE_ROLLE[m.art] || ""}</b>
        <p>“${esc(m.text)}”</p>${m.warte ? weiter(m.sub || "Continue") : `<small>click to continue</small>`}</div></div>${skip}</div>`;
  }
  // Ungeduld: Wer zu lange nichts tut, bekommt Megans Spitze (hoechstens dreimal je Runde, nie waehrend jemand spricht)
  const UNGEDULD_NACH = 45000;
  function ungeduldPruefen(){
    const v = typeof V !== "undefined" && V && V.z && V.z.verhandlung;
    if (!v || V.z.status !== "verhandlung" || v.fertig || v.schritt !== "aussage" || ST.hilfe) return;
    if (TON.laeuft || TON.moment || TON.schlange.length || busy() || TON.ungeduld >= 3) return;
    if (Date.now() - TON.aktiv < UNGEDULD_NACH) return;
    const liste = v.ungeduld || [];
    if (!liste.length) return;
    let z = liste[Math.floor(Math.random() * liste.length)];
    if (TON.ungeduldZeile && z.key === TON.ungeduldZeile.key) z = liste[(liste.indexOf(z) + 1) % liste.length];
    TON.ungeduld += 1; TON.aktiv = Date.now();
    TON.ungeduldZeile = Object.assign({bis: Date.now() + 7000}, z);
    TON.schlange.push({key: z.key}); abspielen(); neu();
    setTimeout(neu, 7100);
  }
  document.addEventListener("pointerdown", ev => { if (ev.target.closest && ev.target.closest(".vh")) TON.aktiv = Date.now(); }, true);
  document.addEventListener("keydown", ev => {
    if (TON.moment && (ev.key === "Enter" || ev.key === " ")){ ev.preventDefault(); momentWeiter(TON.moment); }
  });

  // ------------------------------------------------------------------ Gesamt
  function html(z){
    const v = z.verhandlung;
    if (!v) return `<div class="zentrum"><p class="unter">Loading the hearing …</p></div>`;
    try { tonPruefen(v); } catch (e) {}
    if (ST.hilfe === undefined) ST.hilfe = false;        // Regeln nur unter "?" (29.10.2026: die erste Zeile wird gefuehrt)
    fuehrungPruefen(v);
    const mitte = v.fertig ? ende(v) : v.schritt === "anklage" ? anklage(v) : v.schritt === "rolle" ? rolleHtml(v)
      : v.schritt === "plaedoyer" ? plaedoyerHtml(v) : v.schritt === "urteil" ? "" : spalten(v);
    const unten = v.fertig || ["rolle", "plaedoyer", "urteil"].includes(v.schritt) ? "" : tray(v);
    return `<div class="vh ${ST.karte ? "traegt" : ""}">${buehne(v)}${rundenTitel(v)}${kopf(v)}${megansatz(v)}${mitte}${unten}
      ${verlaufHtml(v)}${momentHtml(v)}${ST.hilfe ? hilfeHtml() : ""}</div>`;
  }

  // Spiel-Leisten waehrend der Anhoerung ausblenden (Duc: "das ist eine Endszene")
  function leisten(){
    const an = typeof V !== "undefined" && V && V.z && V.z.status === "verhandlung";
    document.body.classList.toggle("vh-aktiv", !!an);
  }

  // Testversion (Vorschau-Server mit TEST_START): fester Knopf "Restart hearing" - in jedem Status
  function neustart(){
    if (busy()) return;
    alleUeberspringen(); Object.assign(TON, {letztesN: null, aussage: "", ungeduld: 0, ungeduldZeile: null, aktiv: Date.now()});
    Object.assign(ST, {karte: null, ablage: null, runde: null, stapel: null, alle: false, noproof: false});
    senden("test_neustart", {}, "…");
  }
  setInterval(() => {
    leisten();
    try { ungeduldPruefen(); } catch (e) {}
    if (typeof V !== "undefined" && V && V.z && V.z.status !== "verhandlung" && (TON.laeuft || TON.schlange.length || TON.moment)) alleUeberspringen();
    const an = typeof V !== "undefined" && V && V.test_neustart;
    let k = document.getElementById("vh-test-neustart");
    if (an && !k){
      k = document.createElement("button");
      k.id = "vh-test-neustart"; k.type = "button"; k.textContent = "↺ Restart hearing (test)";
      k.onclick = neustart;
      document.body.appendChild(k);
    } else if (!an && k) k.remove();
    if (k){                                                   // Vorschau mit --tag: derselbe Knopf setzt den Tag zurueck
      const text = V.z && V.z.status === "verhandlung" ? "↺ Restart hearing (test)" : "↺ Restart day (test)";
      if (k.textContent !== text) k.textContent = text;
    }
  }, 400);

  window.EdenHearing = {html, senden: senden2, karte: karteWaehlen, platz, einspruch, fragen, ziehen, ablegen, stapel,
                        alle: alleZeigen, noproof, verlauf, hilfe, neustart, weiter: () => momentWeiter(TON.moment),
                        ueberspringen: alleUeberspringen, _st: ST, _ton: TON};
  try { if (typeof V !== "undefined" && V && V.z && V.z.status === "verhandlung" && typeof zeichnen === "function"){ leisten(); zeichnen(); } }
  catch (e) {}
})();
