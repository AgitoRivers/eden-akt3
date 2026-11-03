/* Bibis Tierstation (Duc 31.10.2026, Wiki systeme/tierstation.md): das Field Book als Safari-Sammelbuch (Duc 01.11.2026), im Laden Mochi's und im Codex.
   Links die Sammlung, rechts die Seite des Tiers mit Zetteln wie bei der Anhoerung. Liest z.mochis, sendet mochis_spur, mochis_fuettern, mochis_besuch, mochis_begleiter, mochis_einsammeln. Nur die Spur kostet eine Phase. */
window.EdenMochis = (function(){
  const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}[c]));
  const knopf = (text, aufruf, geht = true, leise = false) =>
    `<button class="mini${leise ? " leise" : ""}" type="button" ${geht ? "" : "disabled"} onclick="${aufruf}">${esc(text)}</button>`;
  const STEMPEL = {spur: "Trail open", pflege: "Needs feeding", heilt: "Recovering", bleibt: "At the station", mochi: "No trail"};
  let gewaehlt = null;
  function wieder(k){                                  // zweiter Fang: Bibi hat von einem weiteren Tier gehoert
    const w = k.wieder, id = esc(k.id);
    if (!w) return "";
    if (w.heute_schon) return `<span class="mo-hinweis">The new trail has gone cold today.</span>`;
    return knopf(`Another ${k.name}: follow the trail`, `EdenMochis.spur('${id}', false)`, w.geht) +
      (w.koeder ? knopf(`Bring ${w.koeder}`, `EdenMochis.spur('${id}', true)`, w.geht, true) : "");
  }
  function taten(k){
    const id = esc(k.id);
    if (k.status === "spur"){
      if (k.spur.heute_schon) return `<span class="mo-hinweis">The trail has gone cold today. Try again tomorrow.</span>`;
      if (!k.spur.geht) return `<span class="mo-hinweis">A trail needs a free phase.</span>`;
      return knopf("Follow the trail", `EdenMochis.spur('${id}', false)`) +
        (k.spur.koeder ? knopf(`Bring ${k.spur.koeder}`, `EdenMochis.spur('${id}', true)`, true, true) : "") +
        `<span class="mo-hinweis">Takes the whole phase. Wear it down, then throw the Sleep Grenade.</span>`;
    }
    if (k.status === "pflege"){
      const f = k.fuettern;
      return (f.lieb ? knopf(`Feed ${f.lieb}`, `EdenMochis.fuettern('${id}', 'lieb')`) : "") +
        knopf(`Bibi's feed, ${f.geld} €`, `EdenMochis.fuettern('${id}', 'einfach')`, f.geht_geld, !!f.lieb);
    }
    if (k.status === "heilt") return `<span class="mo-hinweis">Getting stronger. ${k.gesund_in === 1 ? "Ready tomorrow." : `Ready in ${k.gesund_in} days.`}</span>`;
    if (k.status === "bleibt") return `<span class="mo-hinweis">Bond ${k.stufe} of 3</span>` + knopf("Visit", `EdenMochis.besuch('${id}')`) +
      knopf(k.begleiter ? "Leave at the pen" : "Take along on trips", `EdenMochis.begleiter('${id}')`, true, k.begleiter) + wieder(k);
    return "";
  }
  // Die Sammlung: ein Foto je Tier, unbekannte als schwarzer Umriss, offene Aufgaben mit Marke
  function foto(k, an){
    const zu = k.status === "nicht_da", marke = k.status === "spur" || (k.wieder && k.wieder.geht) ? "trail" : k.status === "pflege" ? "feed" : "";
    return `<button class="mo-foto mo-${esc(k.status)}${an ? " an" : ""}" type="button" ${zu ? "disabled" : ""} aria-pressed="${!!an}" onclick="EdenMochis.waehlen('${esc(k.id)}')">
      <img src="${esc(k.bild)}" alt=""><span class="mo-foto-name">${esc(k.name)}</span>
      ${k.anzahl > 1 ? `<span class="mo-paar zahl">×${esc(k.anzahl)}</span>` : ""}${marke ? `<span class="mo-marke">${marke}</span>` : ""}</button>`;
  }
  // Zettel wie bei der Anhoerung: liniert, leicht schief, in Bibis Handschrift
  const zettel = (text, art, titel, i) => `<div class="mo-zettel ${art} d${i % 3}">${titel ? `<b>${esc(titel)}</b>` : ""}${esc(text)}</div>`;
  const FEHLT = {zweites: "There may be a second one out there. Then Bibi will tell you more.", besuch: "Visit this one, and Bibi will tell you more."};
  // Bibis Selfie als Mini-Szene (Duc 02.11.2026): zwei Polaroids A, B mit ihrem Titel, darunter ihre Nachricht und die Notiz im Field Book
  const polaroid = p => `<figure class="mo-polaroid"><img src="${esc(p.bild)}" alt="" onclick="this.classList.toggle('gross')" onerror="this.parentNode.remove()"><figcaption>${esc(p.titel)}</figcaption></figure>`;
  const selfie = s => s ? `<div class="mo-selfie"><div class="mo-polaroids">${(s.bilder || []).map(polaroid).join("")}</div>
      <p class="mo-selfie-text">${esc(s.text)}</p>${s.log ? `<p class="mo-selfie-log">${esc(s.log)}</p>` : ""}</div>` : "";
  function seite(k, mitTaten){
    const name = k.name === "?" ? "Unknown" : k.name;
    const notizen = (k.fakten || []).map((s, i) => zettel(s, "fakt", "Did you know?", i)).concat(
      k.fakt_fehlt ? [`<div class="mo-zettel leer">${esc(FEHLT[k.fakt_fehlt])}</div>`] : [],
      (k.seiten || []).map((s, i) => zettel(s, "", "", i + 1)),
      k.futter ? [zettel(k.futter.join(", "), "futter", "Loves", 2)] : []).join("");
    const akt = mitTaten ? taten(k) : "";
    return `<article class="mo-seite">
      <div class="mo-seite-kopf"><div class="mo-tierbild"><img src="${esc(k.bild)}" alt=""></div>
        <div class="mo-seite-titel"><h3>${(k.gestrichen || []).map(n => `<s class="mo-gestrichen">${esc(n)}</s> `).join("")}${esc(name)}${k.anzahl > 1 ? ` <small class="zahl">×${esc(k.anzahl)}</small>` : ""}</h3><small class="mo-art">${esc(k.art)}</small>
          ${STEMPEL[k.status] ? `<span class="mo-stempel mo-${esc(k.status)}">${esc(STEMPEL[k.status])}</span>` : ""}${k.seit ? `<small class="mo-art">Found on day ${esc(k.seit)}</small>` : ""}</div></div>
      ${akt ? `<div class="mo-taten">${akt}</div>` : ""}
      <div class="mo-zettel-reihe">${notizen}</div>
      ${selfie(k.selfie)}${k.szene ? `<p class="mo-szene">${esc(k.szene)}</p>` : ""}</article>`;
  }
  function buch(z, mitTaten){
    const m = z.mochis;
    if (!m) return `<p class="leer">The book is still empty.</p>`;
    const offen = m.karten.filter(k => k.status !== "nicht_da");
    const k = m.karten.find(x => x.id === gewaehlt && x.status !== "nicht_da") ||
      (mitTaten && offen.find(x => x.status === "pflege" || x.status === "spur")) || offen[0];
    const kopf = `<header class="mo-buchkopf"><h2>Field Book</h2><span class="mo-zaehler zahl">${esc(m.gerettet)} / ${esc(m.gesamt)}</span>
      ${m.halsbaender ? `<small class="mo-art">Collars in the box: ${esc(m.halsbaender)}</small>` : ""}
      ${m.begleiter ? `<small class="mo-art">With you: ${esc(m.begleiter)}</small>` : ""}
      ${mitTaten && m.funde ? `<div class="mo-taten">${knopf("See what they found", "EdenMochis.einsammeln()")}</div>` : ""}</header>`;
    return `<div class="mo-buch"><section class="mo-sammlung">${kopf}<div class="mo-fotos">${m.karten.map(x => foto(x, k && x.id === k.id)).join("")}</div></section>
      ${k ? seite(k, mitTaten) : `<article class="mo-seite"><p class="mo-szene">Nobody has come to Bibi yet.</p></article>`}</div>`;
  }
  // Overlay nach dem ersten Fang: Bibi spricht ihre Zeilen nacheinander, die laufende leuchtet
  let briefId = null, briefTon = null;
  function briefHtml(b){
    const sp = (b.zeilen[0] || {}).sprite;
    return `<div class="mo-brief glas" role="dialog" aria-label="${esc(b.name)}">
      ${sp ? `<img class="mo-brief-figur" src="${esc(sp)}" alt="">` : ""}
      <div class="mo-brief-mitte">
        <img class="mo-brief-tier" src="${esc(b.bild)}" alt="">
        <div class="mo-brief-name name">${esc(b.name)}</div><small class="mo-brief-art">${esc(b.art)}</small>
        ${selfie(b.selfie)}
        ${b.zeilen.map((z, i) => `<p class="mo-brief-zeile" data-i="${i}"><b>${esc(z.name)}</b> ${esc(z.text)}</p>`).join("")}
        <div class="mo-brief-fuss"><span class="mo-hinweis">New in your Field Book</span>
          <button class="knopf" id="mo-brief-zu" type="button" onclick="EdenMochis.briefZu()">Continue</button></div>
      </div></div>`;
  }
  function briefSprich(b){
    if (briefId === b.tier) return;
    briefId = b.tier; gewaehlt = b.tier;
    const los = i => {
      document.querySelectorAll(".mo-brief-zeile").forEach((el, n) => el.classList.toggle("an", n === i));
      if (i >= b.zeilen.length || !STIMME){ if (!STIMME) document.querySelectorAll(".mo-brief-zeile").forEach(el => el.classList.add("an")); return; }
      briefTon = mitTempo(new Audio("/api/zeile?id=" + encodeURIComponent(b.zeilen[i].id)));
      briefTon.onended = briefTon.onerror = () => los(i + 1);
      briefTon.play().catch(() => los(i + 1));
    };
    los(0);
    const k = document.getElementById("mo-brief-zu"); if (k) k.focus({preventScroll: true});
  }
  return {html: z => buch(z, true), codexHtml: z => buch(z, false), briefHtml, briefSprich,
    waehlen(id){ gewaehlt = id; zeichnen(); },
    briefZu(){ if (briefTon){ briefTon.onended = briefTon.onerror = null; briefTon.pause(); briefTon = null; } briefId = null; overlay = null; senden("mochis_brief_zu", {}, "…"); },
    spur: (id, koeder) => { ortVerlassen(); senden("mochis_spur", {id, koeder}, "…"); },
    fuettern: (id, art) => senden("mochis_fuettern", {id, art}, "…"),
    besuch: id => senden("mochis_besuch", {id}, "…"),
    begleiter: id => senden("mochis_begleiter", {id}, "…"),
    einsammeln: () => senden("mochis_einsammeln", {}, "…")};
})();
