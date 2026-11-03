/* Nonna's farm and the kitchen builder (27.10.2026, E-079). The engine (kern/farm.py, kern/kuechen.py) decides and books everything;
   this plugin only draws z.kueche and sends actions: garten_pflanzen, stall_kaufen, tier_kaufen, tier_benennen, tier_schlachten,
   nonna_kaufen, nonna_verlassen, fred_gehoert, kochen_baukasten. Animals are single-frame sprites that hop (baby), trip (adult)
   or shuffle (old) with CSS; a click plays the animal's sound if EdenSfx has it. Missing sprites fall back to an emoji. */
window.EdenFarm = (function(){
  const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}[c]));
  const uiIc = (id, klasse) => window.EdenUI ? EdenUI.icon(id, klasse) : "";
  const EMOJI = {chicken: "animal-chicken", pig: "animal-pig", cow: "animal-cow"};
  const STUFE = {1: "Baby", 2: "Adult", 3: "Old"};
  const ROLLEN = [["basis", "Base"], ["haupt", "Main"], ["akzent", "Accent"]];
  const geld = n => (typeof window.geld === "function" ? window.geld(n) : n + " €");
  let wahl = {basis: null, haupt: null, akzent: null, fuer: "crew"};
  let vorschau = {key: "", daten: null, fehler: null};
  let fredId = null, fredAudio = null;

  const act = (name, daten, text) => { if (typeof senden === "function") senden(name, daten || {}, text || "…"); };
  const sterne = n => uiIc("quality", "imtext").repeat(n) + uiIc("quality", "imtext leer").repeat(3 - n);

  // ---------------------------------------------------------------- Farm window (Garden / Animals / Shop / Pantry)
  function tier(s, t){
    const sprite = `<img class="ef-sprite ef-${esc(t.variante)}" src="${esc(t.sprite)}" alt="" style="--gr:${t.groesse}" onerror="this.style.display='none';this.nextElementSibling.hidden=false">`
      + `<span class="ef-emoji ef-${esc(t.variante)}" style="--gr:${t.groesse}" hidden>${uiIc(EMOJI[s.art] || "animal", "imtext")}</span>`;
    const name = t.neu
      ? `<span class="ef-neu"><input type="text" maxlength="16" value="${esc(t.name)}" id="eft-${esc(s.art)}-${t.id}" aria-label="Name"><button class="mini" type="button" onclick="EdenFarm.benennen('${esc(s.art)}', ${t.id})">Name</button></span>`
      : `<b>${esc(t.name)}</b>`;
    return `<div class="ef-tier" onclick="EdenFarm.laut('${esc(s.laut)}', ${t.stufe === 1})">${sprite}<small>${name}</small>
      <small class="ef-stufe">${STUFE[t.stufe]}${t.geschlecht === "f" ? " " + uiIc("female", "imtext") : " " + uiIc("male", "imtext")}${t.bringt ? " · " + esc(s.produkt) : ""}</small>
      ${t.schlachtbar ? `<button class="mini" type="button" onclick="event.stopPropagation();EdenFarm.schlachten('${esc(s.art)}', ${t.id}, '${esc(t.name)}')">Slaughter</button>` : ""}</div>`;
  }
  const ROH_ICON = {timber: "timber", slate: "slate", granite: "granite", steel: "steel", iron: "iron", cork: "cork", feather: "feather", cloth: "cloth", wool: "wool", leather: "leather", coral: "coral"};
  const rohIc = id => ROH_ICON[id] ? uiIc(ROH_ICON[id], "imtext") : "";
  function kostenHtml(k){
    return `<span class="ef-kosten"><span class="${f_konto >= k.geld ? "ok" : "fehlt"}">${geld(k.geld)}</span>${k.rohstoffe.map(r =>
      `<span class="${r.hast >= r.n ? "ok" : "fehlt"}" title="${esc(r.label)}: you have ${r.hast}">${rohIc(r.id)} ${r.hast}/${r.n} ${esc(r.label)}</span>`).join("")}</span>`;
  }
  let f_konto = 0;
  function staelle(f){
    f_konto = f.konto;
    return f.staelle.map(s => {
      const n = s.naechste;
      if (!s.gekauft) return `<section class="ef-stall ef-zu"><h4>${esc(s.label)} shed <small>${esc(s.rasse)} · ${n.plaetze} places</small></h4>
          <p class="leer">${esc(n.text)} Gives ${esc(s.produkt.toLowerCase())}; old animals can be slaughtered for ${esc(s.fleisch.toLowerCase())}.</p>
          <div class="ef-ausbau">${kostenHtml(n)}<button class="mini" type="button" ${n.geht ? "" : "disabled"} onclick="EdenFarm.act('stall_kaufen', {art:'${esc(s.art)}'})">Build the shed</button></div></section>`;
      return `<section class="ef-stall"><h4>${esc(s.label)} shed <span class="ef-stufe-badge">Level ${s.stufe}/${s.stufe_max}</span>
            <small>${esc(s.rasse)} · ${s.tiere.length}/${s.plaetze}</small></h4>
          <div class="ef-weide">${s.tiere.map(t => tier(s, t)).join("") || `<p class="leer">Empty. Buy a baby.</p>`}</div>
          <div class="ef-zeile"><button class="mini" type="button" ${s.tiere.length >= s.plaetze || f.konto < s.baby_preis ? "disabled" : ""} onclick="EdenFarm.act('tier_kaufen', {art:'${esc(s.art)}'})">Buy a baby ${esc(s.label.toLowerCase())} · ${geld(s.baby_preis)}</button>
            ${s.tiere.length >= s.plaetze ? `<small class="leer">The shed is full${n ? " – an upgrade makes room" : ""}.</small>` : ""}</div>
          ${n ? `<div class="ef-ausbau"><div><b>Upgrade to level ${n.stufe}</b><small>${esc(n.text)}</small></div>${kostenHtml(n)}
            <button class="mini" type="button" ${n.geht ? "" : "disabled"} onclick="EdenFarm.act('stall_ausbauen', {art:'${esc(s.art)}'})">Upgrade</button></div>`
              : `<p class="ef-voll">Fully built.</p>`}</section>`;
    }).join("");
  }
  function rohstoffLeiste(f){
    return `<div class="ef-rohstoffe" title="Building materials: Nonna sells some each day, and the sea and the creek wash some up while you fish.">
      ${(f.rohstoffe || []).map(r => `<span>${rohIc(r.id)} <b>${r.n}</b> ${esc(r.label)}</span>`).join("")}</div>`;
  }
  function garten(f){
    return `<div class="ef-beete">${f.garten.map(b => b.leer
      ? `<div class="ef-beet leer"><small>Bed ${b.beet + 1}</small><select id="efb-${b.beet}" aria-label="Plant for bed ${b.beet + 1}">${f.pflanzen.map(p => `<option value="${esc(p.id)}">${esc(p.label)} · ${geld(p.preis)}</option>`).join("")}</select>
          <button class="mini" type="button" onclick="EdenFarm.pflanzen(${b.beet})">Plant</button></div>`
      : `<div class="ef-beet"><small>Bed ${b.beet + 1}</small><b>${esc(b.label)}</b><span>${b.rest > 0 ? "Ready in " + b.rest + " day" + (b.rest > 1 ? "s" : "") : "Ready tomorrow morning"}</span><small>${b.ertrag} × ${uiIc("quality", "imtext").repeat(3)}</small></div>`).join("")}</div>
      <p class="leer">Plant today, harvest tomorrow morning in your pantry. Home-grown gives ${uiIc("quality", "imtext").repeat(3)}.</p>`;
  }
  function laden(k){
    const n = k.nonna;
    if (!n) return `<p class="leer">Nonna has not opened yet.</p>`;
    const konto = typeof V !== "undefined" && V && V.z && V.z.handel ? V.z.handel.konto : 0;   // V: top-level let in index.html
    const ware = w => `<div class="ware">${w.bild ? `<img class="ef-wbild" src="${esc(w.bild)}" alt="">` : w.art === "rohstoff" ? `<span class="ef-wicon">${rohIc(w.id)}</span>` : ""}
      <b>${esc(w.label)}</b><small>${esc(w.text)}</small>
      <div class="zeile"><span class="preis">${geld(w.preis)}</span>${w.n != null ? `<small>${w.n} left today</small>` : ""}
      <button class="mini" type="button" ${w.preis > konto || w.n === 0 ? "disabled" : ""} onclick="EdenFarm.act('nonna_kaufen', {id:'${esc(w.id)}', n:1})">Buy</button></div></div>`;
    const essen = n.waren.filter(w => w.art !== "rohstoff"), bau = n.waren.filter(w => w.art === "rohstoff");
    const liefer = n.lieferung.length ? `<p class="ef-liefer">${uiIc("cart", "imtext")} On Frederico's cart: ${n.lieferung.map(l => `${l.n} × ${esc(l.label || l.id)}`).join(", ")} <small>– he brings it over when you leave.</small></p>` : "";
    return `${liefer}<h3 class="ef-h3">Food <small class="leer">basics every day, animal goods while they last</small></h3><div class="inv">${essen.map(ware).join("")}</div>
      <h3 class="ef-h3">Building materials <small class="leer">for the sheds</small></h3><div class="inv">${bau.map(ware).join("")}</div>`;
  }
  function vorrat(k){
    if (!k.vorrat.length) return `<p class="leer">Your pantry is empty.</p>`;
    return `<div class="inv">${k.vorrat.map(x => `<div class="ware">${x.bild ? `<img class="ef-wbild" src="${esc(x.bild)}" alt="">` : ""}<span class="art">${esc(x.rolle)}${x.effekt ? " · " + esc(x.effekt) : ""}</span>
      <b>${esc(x.label)} <small>${sterne(x.stern)}</small></b><small>${esc(x.text)}</small><small>× ${x.n}</small></div>`).join("")}</div>`;
  }
  function panelHtml(z, panel){
    const k = z.kueche;
    if (!k || !k.farm) return `<p class="leer">Nonna has not opened yet.</p>`;
    const kopf = rohstoffLeiste(k.farm);
    if (panel === "garten") return kopf + garten(k.farm);
    if (panel === "tiere") return kopf + `<div class="ef-staelle">${staelle(k.farm)}</div>`;
    if (panel === "vorrat") return kopf + vorrat(k);
    return kopf + laden(k);
  }
  function wahlpunkte(){ return [["garten", "Garden"], ["tiere", "Animals"], ["kaufen", "Shop"], ["vorrat", "Pantry"]]; }

  // ---------------------------------------------------------------- Kitchen builder (in Lola's galley)
  async function vorschauLaden(){
    const w = wahl, key = [w.basis, w.haupt, w.akzent, w.fuer].join("|");
    if (!(w.basis && w.haupt && w.akzent)){ vorschau = {key, daten: null, fehler: null}; return; }
    if (vorschau.key === key) return;
    vorschau = {key, daten: null, fehler: null};
    try {
      const r = await fetch(`/api/kuechen_vorschau?basis=${encodeURIComponent(w.basis)}&haupt=${encodeURIComponent(w.haupt)}&akzent=${encodeURIComponent(w.akzent)}&fuer=${encodeURIComponent(w.fuer)}`);
      const j = await r.json();
      vorschau = r.ok ? {key, daten: j, fehler: null} : {key, daten: null, fehler: j.fehler || "?"};
    } catch(e){ vorschau = {key, daten: null, fehler: "Preview failed."}; }
    if (typeof zeichnen === "function") zeichnen();
  }
  function baukastenHtml(z, ziele){
    const k = z.kueche;
    if (!k || !k.vorrat.length) return "";
    for (const [r] of ROLLEN) if (wahl[r] && !k.vorrat.some(x => x.key === wahl[r])) wahl[r] = null;
    setTimeout(vorschauLaden, 0);
    const spalte = ([r, name]) => `<div class="ef-spalte"><small>${name}</small>${k.vorrat.filter(x => x.rolle === r).map(x =>
      `<button type="button" class="ef-zutat" aria-pressed="${wahl[r] === x.key}" onclick="EdenFarm.pick('${r}', '${esc(x.key)}')">${x.bild ? `<img src="${esc(x.bild)}" alt="">` : ""}<span>${esc(x.label)} <small>${sterne(x.stern)} ×${x.n}</small></span></button>`).join("") || `<p class="leer">–</p>`}</div>`;
    const v = vorschau.daten;
    const bereit = wahl.basis && wahl.haupt && wahl.akzent && v && k.essen_frei;
    return `<h3 style="margin:18px 0 6px">Cook from your pantry <small class="leer">· 1 base + 1 main + 1 accent, replaces the meal of the day</small></h3>
      <div class="zeile ziel">${(ziele || []).map(t => `<button type="button" aria-pressed="${t.id === wahl.fuer}" onclick="EdenFarm.fuer('${esc(t.id)}')">for ${esc(t.name)}</button>`).join("")}</div>
      <div class="ef-baukasten">${ROLLEN.map(spalte).join("")}</div>
      <div class="ef-vorschau">${v ? `<b>${esc(v.name)}</b><span>DC ${v.sg} · heals ${v.heilt} · ${esc(v.bonus)}</span>
          <small>${v.mag.length ? "Likes it: " + v.mag_namen.map(esc).join(", ") : "Nobody here especially likes it"}${v.mag_nicht.length ? " · Doesn't like it: " + v.mag_nicht_namen.map(esc).join(", ") : ""}</small>`
        : vorschau.fehler ? `<small class="warn">${esc(vorschau.fehler)}</small>` : `<small class="leer">Pick one of each to see the dish.</small>`}</div>
      <div class="zeile"><button class="mini" type="button" ${bereit ? "" : "disabled"} onclick="EdenFarm.kochen()">${k.essen_frei ? "Cook" : "Already ate today"}</button></div>`;
  }

  // ---------------------------------------------------------------- Frederico (after leaving the shop)
  function update(z){
    const f = z && z.kueche && z.kueche.fred;
    if (!f){ fredId = null; return; }
    if (fredId === f.id) return;
    fredId = f.id;
    let box = document.getElementById("fredbox");
    if (!box){ box = document.createElement("div"); box.id = "fredbox"; box.className = "glas ef-fred"; document.getElementById("app").appendChild(box); }
    box.innerHTML = `<small>FREDERICO</small><p>“${esc(f.text)}”</p>`;
    box.hidden = false;
    if (fredAudio){ try { fredAudio.pause(); } catch(e){} }
    if (!(typeof STIMME !== "undefined" && !STIMME)){
      const a = new Audio("/api/zeile?id=" + encodeURIComponent(f.id));
      fredAudio = typeof mitTempo === "function" ? mitTempo(a) : a;
      fredAudio.play().catch(() => {});
    }
    setTimeout(() => { const b = document.getElementById("fredbox"); if (b) b.hidden = true; act("fred_gehoert", {}, "…"); }, 6500);
  }

  // ---------------------------------------------------------------- handlers
  function pflanzen(beet){ const s = document.getElementById("efb-" + beet); if (s) act("garten_pflanzen", {beet, pflanze: s.value}); }
  function benennen(art, id){ const i = document.getElementById(`eft-${art}-${id}`); if (i) act("tier_benennen", {art, id, name: i.value}); }
  function schlachten(art, id, name){ if (confirm(`Slaughter ${name}? ${name} is old and will go into your pantry.`)) act("tier_schlachten", {art, id}); }
  function laut(was, baby){                                 // tier_cluck / tier_grunt / tier_moo, Baby: tier_<laut>_baby (sfx_eden_rise.py)
    if (window.EdenSfx && EdenSfx.play) { try { EdenSfx.play("tier_" + was + (baby ? "_baby" : "")); } catch(e){} }
  }
  function pick(rolle, key){ wahl[rolle] = wahl[rolle] === key ? null : key; if (typeof zeichnen === "function") zeichnen(); }
  function fuer(id){ wahl.fuer = id; if (typeof zeichnen === "function") zeichnen(); }
  function kochen(){
    const w = wahl; act("kochen_baukasten", {basis: w.basis, haupt: w.haupt, akzent: w.akzent, fuer: w.fuer}, "You cook …");
    wahl = {basis: null, haupt: null, akzent: null, fuer: w.fuer};
  }
  return {panelHtml, wahlpunkte, baukastenHtml, update, act, pflanzen, benennen, schlachten, laut, pick, fuer, kochen};
})();
