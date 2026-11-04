/* Kommission an Tag 35 (Akt 3, Duc 04.11.2026): Verhandlung nach dem Vorbild Ace Attorney.
   BLIND GESCHRIEBEN in der Cloud-Sitzung (keine Bilder, kein Server-Lauf): lokal pruefen, bevor kern/kommission.AN = True.
   Nur Darstellung: Regeln, Geduld und Urteil kommen vom Server (z.kommission = kern/kommission.ansicht).
   Index ruft EdenCommission.html(z) in mitte(), wenn z.status === "kommission".
   Aktionen ueber senden("kommission", {was, ...}):
     press {satz} · vorlegen {satz, karte} · nichts · plaedoyer {art: "alles"|"teil"} · schliessen
   Ablauf fuer den Spieler: Delorme sagt drei Saetze. "Press" laesst ihn sich festlegen. Eine Karte waehlen, auf einen
   Satz legen, "OBJECTION!". Falsche Karte kostet Geduld. "I have nothing" gibt die Runde ab. Am Ende das Plaedoyer. */
(function(){
  "use strict";
  const ST = {karte: null, hilfe: false, logAuf: false};
  const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
  const busy = () => (typeof beschaeftigt !== "undefined" && beschaeftigt);
  const neu = () => { if (typeof zeichnen === "function") zeichnen(); };
  const ERG = {gewonnen: ["ok", "won"], verloren: ["aus", "lost"]};
  const ROLLE = {anwalt: "FOR MONACO", kommissar: "PRESIDING", duc: "YOU"};

  function los(was, extra){ if (!busy()) senden("kommission", Object.assign({was}, extra || {}), "…"); }
  function name(v, wer){
    if (v.sprecher && v.sprecher[wer]) return v.sprecher[wer];
    if (wer === "duc") return "You";
    return wer ? wer.charAt(0).toUpperCase() + wer.slice(1) : "";
  }

  function kopf(v){
    const kette = v.runden.map((r, i) => {
      const e = ERG[r.ergebnis];
      const kl = e ? e[0] : (i === v.runde ? "jetzt" : "");
      return `<span class="km-glied ${kl}" title="${esc(r.titel)}${e ? " · " + e[1] : ""}">${i + 1}. ${esc(r.titel)}</span>`;
    }).join("");
    const g = "●".repeat(Math.max(0, v.geduld)) + "○".repeat(Math.max(0, v.geduld_max - v.geduld));
    return `<div class="km-kopf"><span class="km-titel">The Commission</span>${kette}
      <span class="km-geduld" title="The commissioner's patience. A wrong card costs one.">Patience ${g}</span>
      <button type="button" class="km-k" onclick="EdenCommission.hilfe()" aria-label="How the commission works">?</button></div>`;
  }

  function hilfe(){
    if (!ST.hilfe) return "";
    return `<div class="km-hilfe" role="dialog">
      <p><b>How it works.</b> The lawyer for Monaco makes three statements in each round.</p>
      <p><b>Press</b> a statement to make him say it clearly. Some lies only show after that.</p>
      <p><b>Pick a card</b> below, a witness or a piece of proof. Then press <b>OBJECTION!</b> on the statement it shows to be false.</p>
      <p>A wrong card costs the commissioner's patience. When it runs out, the other rounds are lost.</p>
      <p><b>I have nothing</b> gives up the round, but costs no patience.</p>
      <button type="button" onclick="EdenCommission.hilfe()">Close</button></div>`;
  }

  function letzte(v){
    const e = [...(v.log || [])].reverse().find(x => x.art !== "aussage");
    if (!e) return "";
    return `<div class="km-satz ${esc(e.art || "")}"><b>${esc(name(v, e.wer).toUpperCase())}<small>${esc(ROLLE[e.wer] || "")}</small></b>“${esc(e.text)}”</div>`;
  }

  function aussage(v){
    if (!v.aussage.length || v.fertig || v.schritt === "plaedoyer") return "";
    const karte = ST.karte && v.karten.find(c => c.id === ST.karte);
    const spalten = v.aussage.map((s, i) => `<div class="km-spalte ${s.gepresst ? "gepresst" : ""}">
        <p>“${esc(s.text)}”</p>
        <div class="km-knoepfe">
          <button type="button" ${s.gepresst || busy() ? "disabled" : ""} onclick="EdenCommission.press(${i})">${s.gepresst ? "Pressed" : "Press"}</button>
          <button type="button" class="einspruch" ${!karte || busy() ? "disabled" : ""} onclick="EdenCommission.vorlegen(${i})"
            title="${karte ? "Present: " + esc(karte.titel) : "Pick a card first"}">OBJECTION!</button>
        </div></div>`).join("");
    return `<div class="km-aussage"><div class="km-rtitel">${esc(v.titel)}<small>Round ${Math.min(v.runde + 1, v.runden.length)} of ${v.runden.length}</small></div>
      <div class="km-spalten">${spalten}</div>
      <button type="button" class="km-nichts" ${busy() ? "disabled" : ""} onclick="EdenCommission.nichts()">I have nothing</button></div>`;
  }

  function karten(v){
    if (v.fertig || v.schritt === "plaedoyer") return "";
    if (!v.karten.length) return `<div class="km-karten leer">You have no witnesses and no proof. You can only press, or give up the round.</div>`;
    const h = v.karten.map(c => `<button type="button" class="km-karte ${esc(c.art)} ${ST.karte === c.id ? "an" : ""}"
        onclick="EdenCommission.karte('${esc(c.id)}')" title="${esc(c.text)}">
        <small>${c.art === "zeuge" ? "Witness" : "Proof"}</small>${esc(c.titel)}</button>`).join("");
    const k = ST.karte && v.karten.find(c => c.id === ST.karte);
    return `<div class="km-karten">${h}</div>${k ? `<div class="km-kartetext"><b>${esc(k.titel)}.</b> ${esc(k.text)}</div>` : ""}`;
  }

  function plaedoyer(v){
    if (v.schritt !== "plaedoyer" || v.fertig) return "";
    return `<div class="km-plaedoyer"><p>The commissioner waits for your last words. What do you put on the table?</p>
      ${v.plaedoyer.map(p => `<button type="button" ${busy() ? "disabled" : ""} onclick="EdenCommission.plaedoyer('${esc(p.id)}')">${esc(p.chip)}</button>`).join("")}</div>`;
  }

  function ende(v){
    if (!v.fertig) return "";
    return `<div class="km-ende"><button type="button" ${busy() ? "disabled" : ""} onclick="EdenCommission.schliessen()">Continue</button></div>`;
  }

  function verlauf(v){
    const n = (v.log || []).length;
    if (!ST.logAuf) return `<button type="button" class="km-log-k" onclick="EdenCommission.log()">Transcript (${n})</button>`;
    const z = (v.log || []).map(e => `<p class="${esc(e.art || "")}"><b>${esc(name(v, e.wer))}:</b> ${esc(e.text)}</p>`).join("");
    return `<div class="km-log"><button type="button" onclick="EdenCommission.log()">Close transcript</button>${z}</div>`;
  }

  function html(z){
    const v = z && z.kommission;
    if (!v) return `<div class="zentrum"><p class="unter">The commission is getting ready.</p></div>`;
    if (ST.karte && !v.karten.some(c => c.id === ST.karte)) ST.karte = null;
    return `<div class="km">${kopf(v)}${hilfe()}${letzte(v)}${aussage(v)}${karten(v)}${plaedoyer(v)}${ende(v)}${verlauf(v)}</div>`;
  }

  window.EdenCommission = {
    html,
    hilfe(){ ST.hilfe = !ST.hilfe; neu(); },
    log(){ ST.logAuf = !ST.logAuf; neu(); },
    karte(id){ ST.karte = ST.karte === id ? null : id; neu(); },
    press(i){ los("press", {satz: i}); },
    vorlegen(i){ if (!ST.karte) return; const k = ST.karte; ST.karte = null; los("vorlegen", {satz: i, karte: k}); },
    nichts(){ ST.karte = null; los("nichts"); },
    plaedoyer(art){ los("plaedoyer", {art}); },
    schliessen(){ ST.karte = null; ST.logAuf = false; los("schliessen"); },
  };
})();
