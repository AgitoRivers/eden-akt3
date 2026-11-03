/* Kampfbildschirm (Etappe 3, 19.10.2026; Etappe 4b, 24.10.2026) - Entwurf A1 "Schwaechen & Schild" mit Parade-Proben,
   Spezialangriffen, Zustands-Chips, Reaktionen und Skillwahl.
   Nur Darstellung und Zeitmessung: Regeln, Wuerfe und Fenstergroessen kommen vom Server (z.kampf, kern/kampf.py).
   Index ruft EdenCombat.html(z, V) in mitte() und danach EdenCombat.nachZeichnen(z, V). Aktionen gehen ueber senden():
     kampf_zug {befehl, ziel, revision} · kampf_parade {ergebnis, revision} · kampf_schliessen {} · skill_lernen {id}
     ausruesten {platz, id} (Reiter "Ausrüstung" im Laden-&-Inventar-Fenster: EdenCombat.ausruestungHtml(z))
   Effekte: window.EdenCombatEffects.play(name, ankerElement, info) (eden-combat-effects.js, austauschbar) und das
   DOM-Ereignis "eden-kampf-effekt" {name, anker, info}. Spezialangriffe: name "spezial", info {id, effekt, phase}
   (effekt = ID im Effektlabor, Tabelle EFFEKT_ID). */
(function(){
  "use strict";
  const ATTR = {strength: "Strength", charm: "Charisma", empathy: "Empathy", perception: "Perception", cunning: "Cunning", courage: "Courage"};
  // Pfadfarbe der Karten: Kaempfer (k), Schmuggler (s), Schuetze (j), Berserker (m), Grundfaehigkeit (g)
  const PFAD = {K: "k", L: "s", W: "j", M: "m", H: "h"};
  // Attribute: Icons unter ihrem Namen im Woerterbuch (ui_stil.md)
  const ELEMENT = {wasser: "Water", feuer: "Fire", erde: "Earth", luft: "Air"};
  const ELEMENT_IC = {wasser: "water", feuer: "burn", erde: "earth", luft: "air"};
  const elementHtml = id => (ELEMENT_IC[id] ? uiIc(ELEMENT_IC[id], "imtext") + " " : "") + esc(ELEMENT[id] || id);
  const ENDE = {ko: "Victory", aufgabe: "Peaceful Victory", entkommen: "They Got Away", flucht: "You Fled", niederlage: "Defeat"};
  const URTEIL = {perfekt: "PERFECT PARRY!", gut: "Parried", ausweichen: "Dodged", verfehlt: "Hit"};
  // Code-ID des Spezialangriffs -> Effekt-ID im Effektlabor (docs/effekt-auswahl/status-labor/freigabe-spezialangriffe.json)
  const EFFEKT_ID = {mistral: "mistral", ressac: "wave", libeccio: "wind", lame_de_fond: "tidal", doppio_gioco: "doubleSlash",
                     sotto_voce: "blur", vendetta: "vendetta", omerta: "blackSlash", point_de_mire: "reticle", bonaccia: "calm",
                     phare: "beam", pluie_d_etoiles: "rain", scirocco: "scirocco", retour: "retour", furia: "furia", vulcano: "vulcano",
                     elicriso: "balm", ponente: "westWind", risveglio: "awaken", arcangelo: "archangel",
                     parry_the_dirt: "wind", maximum: "vulcano", approves: "awaken"};   // Maxwell (Duc 01.11.2026): Rauch, Explosion, Buff aus dem Labor
  const CHIP_ICON = {brennend: "burn", nass: "water", strom: "shock", blutend: "bleed", erschuettert: "dazed", erschoepft: "exhausted", schlamm: "mud",
                     geblendet: "blinded", geschwaecht: "weakened", ungedeckt: "exposed", betaeubt: "stunned", silence: "silenced", buff: "strength", armor_up: "guard",
                     wall: "wall", dodge: "dodge", skip: "skip", aussetzen: "skip", guard: "guard"};
  const REAKTION_FARBE = {Steam: "#cfe3f2", "Short Circuit": "#8ec5ff", Burst: "#d97b7b", Sparks: "#f0a050", Mud: "#b69a6f", Interrupted: "#e0c080", Bibi: "#8ec5ff", Charly: "#f0d060", Danzel: "#d87060"};   // reaction names from kern/kampf.py
  const ERSATZ = {attack: ["attack", "heavy_attack", "idle"], heavy_attack: ["heavy_attack", "attack", "idle"], konter: ["konter", "attack", "idle"],
                  windup: ["windup", "heavy_windup", "idle"], heavy_windup: ["heavy_windup", "windup", "idle"],
                  flee: ["flee", "weakened", "idle"], surrender: ["surrender", "weakened", "idle"], defeated: ["defeated", "hurt", "idle"],
                  victory: ["victory", "enraged", "idle"], hurt: ["hurt", "idle"], weakened: ["weakened", "idle"], guard: ["guard", "idle"]};
  const ST = {dpose: null, dposeBis: 0, panel: null, letzte: null, pose: null, poseBis: 0, bewegung: "", probe: null, probeRev: null, kampfId: null};

  const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
  const bar = (w, max, kl) => `<div class="balken"><i class="${kl}" style="width:${Math.max(0, 100 * w / max)}%"></i></div>`;
  const pips = (n, max) => `<div class="pips">${Array.from({length: max}, (_, i) => `<i class="${i < n ? "voll" : ""}"></i>`).join("")}</div>`;
  const app = () => document.getElementById("app");
  // V und beschaeftigt sind im Client mit let deklariert (gemeinsamer globaler Bereich, aber keine window-Eigenschaften)
  const stand = () => (typeof V !== "undefined" ? V : null);
  const busy = () => (typeof beschaeftigt !== "undefined" && beschaeftigt) || !!ST.cutin;      // auch waehrend der Spezialangriff-Sequenz

  // Optionen (25.10.2026): UI-Größe und Parade-Hilfe, lokal gespeichert - das Spiel erklärt dabei nichts;
  // fx (26.10.2026): Spezialangriffe als Zwischensequenz an/aus
  const OPT = {ui: 1, hilfe: 1, fx: 1};
  try { Object.assign(OPT, JSON.parse(localStorage.getItem("eden.kampfopt") || "{}")); } catch (e) {}
  function optAnwenden(){ document.documentElement.style.setProperty("--ui-opt", String(OPT.ui)); }
  function optSetzen(was, wert){
    OPT[was] = Number(wert); optAnwenden();
    try { localStorage.setItem("eden.kampfopt", JSON.stringify(OPT)); } catch (e) {}
    if (typeof zeichnen === "function") zeichnen();
  }
  function optionenHtml(){
    const gruppe = (was, titel, werte) => `<div class="tempo"><span>${titel}</span><span class="optgruppe">${werte.map(([w, l]) => `<button type="button" aria-pressed="${OPT[was] === w}"
        onclick="EdenCombat.optSetzen('${was}',${w})">${l}</button>`).join("")}</span></div>`;
    return gruppe("ui", "Combat UI", [[0.9, "small"], [1, "normal"], [1.2, "large"], [1.45, "extra large"]])
      + gruppe("hilfe", "Parry help", [[1, "off"], [1.25, "a little"], [1.5, "a lot"]])
      + gruppe("fx", "Special attack scenes", [[1, "on"], [0, "off"]]);
  }
  optAnwenden();
  function bild(g, pose){
    const b = g.bilder || {};
    for (const p of (ERSATZ[pose] || [pose, "idle"])) if (b[p]) return b[p];
    return null;
  }
  // Mehrere Gegner (29.10.2026, wie Final Fantasy): k.zielgegner = auf wen Duc zielt, k.parade.gegner = wer zuschlaegt.
  // Jedes Gegner-Sprite traegt data-i (Index) und data-inst (Instanz aus den Ereignissen).
  const mehrere = k => (k.gegner || []).length > 1;
  const zielI = k => (ST.zielwahl ? ST.zielwahl.i : k.zielgegner) || 0;
  const zielG = k => k.gegner[zielI(k)] || k.gegner[0];
  const angreiferI = k => (k.parade && k.parade.gegner) || 0;
  const gspr = i => document.querySelector(`#mitte .kampf .gsprite[data-i="${i}"]`) || document.querySelector("#mitte .kampf .gsprite");
  const gsprInst = inst => (inst && document.querySelector(`#mitte .kampf .gsprite[data-inst="${inst}"]`)) || null;
  function grundPose(k, i){
    if (i == null) i = zielI(k);
    const g = k.gegner[i] || k.gegner[0];
    if (performance.now() < (ST.einschlafenAb || 0)) return "weakened";    // Schlafgranate: Das Tier steht noch, bis der Nebel wirkt
    if (g.aus) return {ko: "defeated", aufgabe: "surrender", entkommen: "flee"}[g.aus] || "defeated";
    if (k.ergebnis) return {ko: "defeated", aufgabe: "surrender", entkommen: "flee", flucht: "idle", niederlage: "victory"}[k.ergebnis.art];
    if (k.phase === "parade" && angreiferI(k) === i) return k.parade && k.parade.schwer ? "heavy_windup" : "windup";
    if ((g.absicht || {}).flucht) return "flee";
    if (g.geschwaecht || g.erschoepft) return "weakened";
    return "idle";
  }
  const aktuellePose = (k, i) => {
    if (i == null) i = zielI(k);
    return (ST.pose && performance.now() < ST.poseBis && (ST.poseI == null ? zielI(k) : ST.poseI) === i) ? ST.pose : grundPose(k, i);
  };
  // Ducs eigenes Sprite (25.10.2026): Look der Jacke x Waffe; Posen aus dem Kampfstand, kurze Ausschlaege nach Aktionen
  function dbild(k, pose){
    const b = k.duc_bilder || {};
    for (const p of (ERSATZ[pose] || [pose, "idle"])) if (b[p]) return b[p];
    return null;
  }
  function dGrundPose(k){
    const sp = k.spieler;
    if (k.ergebnis) return {ko: "victory", aufgabe: "victory", entkommen: "flee", flucht: "flee", niederlage: "defeated"}[k.ergebnis.art] || "idle";
    if (k.phase === "parade") return "guard";
    if (sp.lp <= sp.lp_max * 0.3) return "weakened";
    return "idle";
  }
  const dAktuell = k => (ST.dpose && performance.now() < ST.dposeBis) ? ST.dpose : dGrundPose(k);
  function dSetzen(k, pose, ms, klasse){
    const img = document.querySelector("#mitte .kampf .dsprite"); if (!img || !k) return;
    ST.dpose = pose; ST.dposeBis = performance.now() + ms;
    const src = dbild(k, pose); if (src) img.src = src;
    img.classList.remove("vor", "treffer");
    if (klasse){ void img.offsetWidth; img.classList.add(klasse); }
    setTimeout(() => {
      if (performance.now() < ST.dposeBis) return;
      const v = stand(), kk = v && v.z && v.z.kampf; if (!kk) return;
      const s2 = dbild(kk, dGrundPose(kk)); if (s2) img.src = s2; img.classList.remove("vor", "treffer");
    }, ms + 50);
  }

  // Ducs Schlag als Bildfolge (Duc 03.11.2026, werkzeuge/kampf_schwung.py): bei "Attack" und beim Konter nach der perfekten
  // Parade. Takt aus Ducs Lieferung, der Schlag sitzt bei Bild e (SCHWUNG_TREFFER): Zahl, Treffer-Pose und Klang des Gegners
  // warten bis dahin. Der Konter beginnt beim zweiten Bild, Duc hat ja schon pariert. Ohne Bildfolge (Gemelli) die alte Pose.
  const SCHWUNG = ["schwung_a", "schwung_b", "schwung_c", "schwung_d", "schwung_e", "schwung_f"];
  const SCHWUNG_MS = [380, 100, 70, 50, 70, 500], SCHWUNG_TREFFER = 4, SCHWUNG_VOR = 2;
  const WENIG_BEWEGUNG = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const schwungDa = k => !WENIG_BEWEGUNG && !!k && SCHWUNG.every(n => (k.duc_bilder || {})[n]);
  const schwungBisTreffer = ab => SCHWUNG_MS.slice(ab, SCHWUNG_TREFFER).reduce((a, b) => a + b, 0);
  function schwungLaden(k){                                    // einmal je Sprite vorladen, sonst flackert das erste Mal
    if (!schwungDa(k) || ST.schwungGeladen === k.duc_bilder.schwung_a) return;
    ST.schwungGeladen = k.duc_bilder.schwung_a;
    SCHWUNG.forEach(n => { const i = new Image(); i.src = k.duc_bilder[n]; });
  }
  function schwung(k, ab){
    if (!schwungDa(k)) return false;
    ab = ab || 0;
    const jetzt = performance.now(), dauer = SCHWUNG_MS.slice(ab).reduce((a, b) => a + b, 0);
    ST.schwungTreffer = jetzt + schwungBisTreffer(ab);
    ST.dposeBis = jetzt + dauer;
    let t = 0;
    SCHWUNG.slice(ab).forEach((n, i) => {
      setTimeout(() => {
        ST.dpose = n;                                          // ein Neuzeichnen mitten im Schlag zeigt dasselbe Bild
        const img = document.querySelector("#mitte .kampf .dsprite"); if (!img) return;
        img.src = k.duc_bilder[n];
        if (ab + i === SCHWUNG_VOR) img.classList.add("vor");
      }, t);
      t += SCHWUNG_MS[ab + i];
    });
    setTimeout(() => {
      if (performance.now() < ST.dposeBis) return;
      const img = document.querySelector("#mitte .kampf .dsprite"), v = stand(), kk = v && v.z && v.z.kampf;
      if (img) img.classList.remove("vor");
      const s2 = kk && dbild(kk, dGrundPose(kk)); if (img && s2) img.src = s2;
    }, dauer + 50);
    return true;
  }
  const schwungLaeuft = () => SCHWUNG.includes(ST.dpose) && performance.now() < ST.dposeBis;

  function effekt(name, anker, info){
    try { if (window.EdenCombatEffects) EdenCombatEffects.play(name, anker, info || {}); } catch(e){ console.warn(e); }
    document.dispatchEvent(new CustomEvent("eden-kampf-effekt", {detail: {name, anker, info: info || {}}}));
  }
  // Kampftoene (27.10.2026): Einzeltoene aus dem SFX-Katalog; An/Aus und Lautstaerke regelt eden-sfx
  const GRANATEN_TON = {brennend: "kampf_granate_feuer", nass: "kampf_granate_wasser", strom: "kampf_granate_schock",
    geblendet: "kampf_granate_flash", erschuettert: "kampf_granate_erschuetterung", blutend: "kampf_granate_splitter", schlaf: "kampf_granate_schlaf"};
  function ton(id, ms, opt){ if (id && window.EdenSfx) try { EdenSfx.play(id, ms || 0, opt); } catch (e) {} }
  // Muendungsfeuer (Duc 01.11.2026): Punkt aus k.muendung je Sprite und Pose, Klang wie in Holms Wette. Fehlt der Punkt, kein Blitz
  function schuss(k, el, url, pose, richtung){
    const name = ((url || "").match(/\/kampfbild\/([A-Za-z0-9_]+)\//) || [])[1], p = ((k.muendung || {})[name] || {})[pose];
    if (el && p) effekt("muendung", el, {x: p[0], y: p[1], richtung});
    ton("gun_shot");
  }
  function ducSchuss(k, pose){                                 // Gemelli: zwei Laeufe, zwei Knalle
    const sp = k.spieler, w = sp.weapon || {}; if (w.kind !== "fern") return;
    const feuer = () => schuss(k, document.querySelector("#mitte .kampf .dsprite"), dbild(k, pose), pose, 1);
    feuer(); if (w.sig === "twin") setTimeout(feuer, 150);
  }
  function gegnerSchuss(k, g, p, ai){
    if (!p || !p.schuss || ST.schussRev === k.revision) return;
    ST.schussRev = k.revision;
    const pose = p.schwer ? "heavy_attack" : "attack";
    schuss(k, gspr(ai || 0), bild(g, pose) || bild(g, "attack"), pose, -1);
  }
  function pop(anker, text, art){
    const k = document.querySelector("#mitte .kampf"); if (!k || !anker) return;
    const box = k.getBoundingClientRect(), r = anker.getBoundingClientRect();
    const el = document.createElement("div"); el.className = "kampf-pop " + art; el.textContent = text;
    el.style.left = (r.left - box.left + r.width / 2 - 60) + "px"; el.style.top = (r.top - box.top + 30) + "px";
    k.appendChild(el); setTimeout(() => el.remove(), 1400);
  }
  function banner(text, klasse, farbe, verzoegerung){
    setTimeout(() => {
      const t = document.createElement("div"); t.className = "kampf-urteil " + klasse; t.textContent = text;
      if (farbe) t.style.color = farbe;
      app().appendChild(t); setTimeout(() => t.remove(), 1300);
    }, verzoegerung || 0);
  }
  // Ruhige Buehne (Duc 02.11.2026): jedes senden() zeichnet den Kampf zweimal neu (vor und nach der Antwort). Dabei brachen
  // laufende Ausschlaege (Stoss, Treffer, Ducs Vorschritt) und fliegende Zahlen mitten im Bild ab. Die alten Sprite-Knoten
  // ziehen in den neuen Stand um und behalten ihre laufende Animation, Zahlen und Sprueche wandern mit.
  const FLUECHTIG = ["vor", "treffer", "stoss", "zurueck", "treffer-stark"];
  const spriteKey = img => img.classList.contains("dsprite") ? "d" : "g" + (img.dataset.inst || img.dataset.i || "");
  function einsetzen(M, h){
    const alt = M.querySelector(".kampf"), sprites = {}, mit = [];
    if (alt){
      alt.querySelectorAll(":scope > img.dsprite, :scope > img.gsprite").forEach(img => { sprites[spriteKey(img)] = img; });
      alt.querySelectorAll(":scope > .kampf-pop, :scope > .kampf-codex, :scope > canvas.datem").forEach(x => mit.push(x));
    }
    M.innerHTML = h;
    const neu = M.querySelector(".kampf"); if (!neu || !alt) return;
    neu.querySelectorAll(":scope > img.dsprite, :scope > img.gsprite").forEach(img => {
      const o = sprites[spriteKey(img)]; if (!o) return;
      const bleibt = FLUECHTIG.concat("atmet").filter(c => o.classList.contains(c));
      for (const a of [...o.attributes]) if (!img.hasAttribute(a.name)) o.removeAttribute(a.name);
      for (const a of [...img.attributes]) if (o.getAttribute(a.name) !== a.value) o.setAttribute(a.name, a.value);
      bleibt.forEach(c => o.classList.add(c));
      img.replaceWith(o);
    });
    mit.forEach(x => neu.appendChild(x));
  }
  // Atmen (Duc 04.11.2026, Paket eden-duc-heavy-20261103-v1/idle-guard): Ducs Ruheposen idle, guard und weakened atmen.
  // Der Oberkoerper hebt und senkt sich, die Verformung laeuft durch die Beine aus, die Stiefel bleiben stehen. Gezeichnet
  // wird auf eine Leinwand gleich hinter dem Bild (Klassen des Bildes + datem, also dieselbe Lage); das <img> bleibt fuer
  // alle Posenwechsel zustaendig und ist nur in Ruhe versteckt (atmet). Andere Posen und kurze Ausschlaege zeigen das Bild.
  const ATEM = {idle: {s: 3.8, amp: .004, sway: .0012, sign: -1}, guard: {s: 3.2, amp: .0025, sway: .0015, sign: -1},
                weakened: {s: 2.6, amp: .014, sway: .0018, sign: 1}};
  const atemRand = {};                                      // je Bild-URL: oberste und unterste deckende Zeile
  function atemKanten(img){
    const key = img.currentSrc || img.src;
    if (key in atemRand) return atemRand[key];
    atemRand[key] = null;
    try {
      const w = img.naturalWidth, h = img.naturalHeight, c = document.createElement("canvas"); c.width = w; c.height = h;
      const x = c.getContext("2d", {willReadFrequently: true}); x.drawImage(img, 0, 0);
      const d = x.getImageData(0, 0, w, h).data, deckt = y => { for (let i = y * w * 4 + 3, e = i + w * 4; i < e; i += 4) if (d[i] > 24) return true; return false; };
      let top = 0, bottom = h - 1;
      while (top < h && !deckt(top)) top++;
      while (bottom > top && !deckt(bottom)) bottom--;
      if (top < bottom) atemRand[key] = {top, bottom: bottom + 1};
    } catch (e) {}
    return atemRand[key];
  }
  function atemVerschub(y, r, p, phase){
    const h = r.bottom - r.top, taille = r.top + h * .55, stiefel = r.top + h * .87;
    const t = Math.max(0, Math.min(1, (y - taille) / (stiefel - taille))), gewicht = 1 - t * t * (3 - 2 * t);
    return {y: p.sign * h * p.amp * phase * gewicht, x: h * p.sway * phase * gewicht};
  }
  let atemGezeichnet = 0;
  function atmen(now){
    requestAnimationFrame(atmen);
    const img = document.querySelector("#mitte .kampf > img.dsprite");
    let cv = img && img.parentNode.querySelector(":scope > canvas.datem");
    const p = img && ATEM[((img.getAttribute("src") || "").match(/\/([a-z_]+)\.webp/) || [])[1]];
    const r = p && img.complete && img.naturalWidth && !document.hidden && !(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches)
      && !FLUECHTIG.some(c => img.classList.contains(c)) && atemKanten(img);
    if (!r){ if (img) img.classList.remove("atmet"); if (cv) cv.hidden = true; return; }
    const neu = !cv || cv.hidden || cv.dataset.src !== img.src;
    if (!neu && now - atemGezeichnet < 33) return;            // 30 Bilder je Sekunde reichen fuer so wenig Bewegung
    atemGezeichnet = now;
    if (!cv){ cv = document.createElement("canvas"); img.after(cv); }
    const w = img.naturalWidth, h = img.naturalHeight;
    if (cv.width !== w || cv.height !== h){ cv.width = w; cv.height = h; }
    const phase = .5 - .5 * Math.cos((now / 1000 / p.s) % 1 * Math.PI * 2), ctx = cv.getContext("2d");
    ctx.clearRect(0, 0, w, h);
    for (let y = 0; y < h; y += 2){                           // Streifen: oben alles zusammen, zu den Stiefeln hin auslaufend
      const sh = Math.min(2, h - y), a = atemVerschub(y, r, p, phase), b = atemVerschub(y + sh, r, p, phase);
      ctx.drawImage(img, 0, y, w, sh, a.x, y + a.y, w, sh + b.y - a.y + .1);
    }
    cv.dataset.src = img.src;
    cv.className = img.className.replace(/\batmet\b/g, "").trim() + " datem"; cv.hidden = false;
    img.classList.add("atmet");
  }
  requestAnimationFrame(atmen);
  function spriteSetzen(src, klasse, i){
    const v0 = stand(), k0 = v0 && v0.z && v0.z.kampf;
    if (i == null) i = k0 ? zielI(k0) : 0;
    ST.poseI = i;
    const img = gspr(i); if (!img) return;
    if (src) img.src = src;
    img.classList.remove("zurueck", "stoss", "treffer", "treffer-stark");
    if (klasse){ void img.offsetWidth; img.classList.add(klasse); }
  }
  // Zustands-Chips: Brand mit Stufen (x1..5), sonst Runden als Hochzahl
  function chips(liste){
    return (liste || []).map(c => `<span class="chip ${esc(c.id)}" title="${esc(c.label)}${c.id === "brennend" ? " – stack " + c.wert : c.wert > 1 ? " – " + c.wert + " rounds" : ""}">${CHIP_ICON[c.id] ? uiIc(CHIP_ICON[c.id], "imtext") : "•"} ${esc(c.label)}${c.id === "brennend" ? ` ×${c.wert}` : ""}</span>`).join("");
  }

  // ------------------------------------------------------------------ Bildschirm
  function karte(f, i, wahl){
    const pf = f.art === "spezial" ? PFAD[f.pfad] : "g";
    return `<button class="fk ${pf} ${f.schwaeche ? "schwach" : ""}" type="button" ${f.gesperrt || !wahl ? "disabled" : ""}
        onclick="EdenCombat.zug('faehigkeit','${esc(f.id)}')" title="${esc(f.text)} (key ${i + 1}${f.kuerzel ? " · " + f.kuerzel : ""})">
        <span class="taste">${i + 1}</span>
        <span class="kopf"><span class="name">${esc(f.label)}</span><span class="pfad">${esc(f.art === "spezial" ? f.pfad_name + " " + f.stufe : (ATTR[f.attribut] || ""))}</span></span>
        <span class="wirk">${esc(f.text)}</span>
        <span class="fuss"><span class="pill kosten">${f.kosten} ${uiIc("stamina", "imtext")}</span>
          ${f.probe ? (f.chance == null ? "" : `<span class="pill">${f.chance} %${f.vorteil ? " ▲" : ""}</span>`) : `<span class="pill ok">sure</span>`}
          ${f.schaden ? `<span class="pill">≈ ${f.schaden}</span>` : ""}
          ${f.gesperrt ? `<span class="pill bed">${esc(f.gesperrt)}</span>` : ""}
          ${f.hinweis && !f.gesperrt ? `<span class="pill warn">${esc(f.hinweis)}</span>` : ""}</span></button>`;
  }
  // Ducs letzter W20 im Kampf (Duc 03.11.2026): der goldene Wuerfel laeuft kompakt (0,8 s) ueber Ducs Karte, danach bleibt
  // das Ergebnis mit Rechnung dort stehen, bis Duc den naechsten Befehl gibt
  function wurfRestHtml(){
    const p = ST.wurfRest; if (!p) return "";
    const boni = (p.boni || []).map(([l, b]) => `${b >= 0 ? "+" : "−"}${Math.abs(b)} ${esc(l)}`).join(" ");
    const w = p.wuerfe.length > 1 ? `${p.wuerfe.join(" / ")} → ${p.wurf}` : p.wurf;
    return `<div class="kampf-wurf wurf ${esc(p.ergebnis)}"><span class="w">${p.wurf}</span><div><b>${esc(ATTR[p.attribut] || p.attribut)} check · needs ${p.sg}</b>
      <span class="zahl">${w} ${boni} = ${p.summe}</span> · <span class="erg">${esc(p.text)}</span></div></div>`;
  }
  // Schlafgranate gewirkt (Duc 01.11.2026): Wurf, Nebel steigt, erst dann sackt das Tier zusammen und die Z steigen auf.
  function einschlafen(k){
    if (ST.schlafFuer === k.id || !k.ergebnis || k.ergebnis.art !== "aufgabe" || !(k.events || []).some(e => e.art === "gegenstand" && e.granate === "schlaf")) return;
    ST.schlafFuer = k.id;
    const warte = ((window.EdenCombatEffects && EdenCombatEffects.WURF_MS) || 520) + SCHLAF_NEBEL_MS;   // nur als Rueckfall, falls die Wolke ausbleibt (Bewegung reduziert)
    ST.einschlafenAb = performance.now() + warte + 4000;
    ST.einschlafTimer = setTimeout(eingeschlafen, warte + 4000, k);
    document.addEventListener("eden-nebel-wirkt", () => { if (ST.einschlafenAb) eingeschlafen(k); }, {once: true});
  }
  function eingeschlafen(k){
    if (!ST.einschlafenAb) return;
    clearTimeout(ST.einschlafTimer);
    ST.einschlafenAb = 0;
    spriteSetzen(bild(k.gegner[0], "surrender"), "", 0);
    effekt("zzz", gspr(0));
  }
  // Sieg erst nach der Zwischensequenz (Duc 02.11.2026): Kommt das Ende, solange der Spezialangriff laeuft, zeigt die Buehne
  // dahinter noch den Stand davor - kein Umfallen, keine Ergebnis-Karte, keine Siegmusik (index.html fragt musikHalten)
  const endeHalten = k => !!(ST.cutin && k.ergebnis && ST.letzte && ST.letzte.id === k.id && !ST.letzte.ende);
  function html(z, V){
    const k0 = z.kampf, k = endeHalten(k0) ? Object.assign({}, k0, {ergebnis: null,
      gegner: k0.gegner.map(x => x.aus && !(ST.letzte.aus || []).includes(x.instanz) ? Object.assign({}, x, {aus: null}) : x)}) : k0;
    const sp = k.spieler, multi = mehrere(k);
    const paket = V && V.wuerfel_anzeige, rolls = (paket && paket.rolls) || [];
    if (rolls.length && ST.wurfPaket !== paket){ ST.wurfPaket = paket; ST.wurfRest = rolls[rolls.length - 1].probe; }
    einschlafen(k);
    if (ST.kampfId !== k.id){ ST.zielwahl = null; ST.poseI = null; }
    const g = zielG(k), a = g.absicht || {};
    if (ST.kampfId !== k.id){ ST.kampfId = k.id; ST.panel = null; ST.letzte = null;
      try { window.EdenCombatEffects && EdenCombatEffects.vorladen && EdenCombatEffects.vorladen(); } catch(e){}     // Granaten-Bildboegen erst jetzt
      // Fernwaffe: der freie Schuss vor Runde 1 (Gemelli) ist auch zu sehen und zu hoeren
      if (k.runde === 1 && (k.log || []).some(l => l.befehl === "erstschlag")) setTimeout(() => { dSetzen(k, "attack", 650, "vor"); ducSchuss(k, "attack"); }, 500);
      try {                                                    // Zwischensequenz vorladen, sonst bleibt der Schirm beim ersten Spezialangriff lange schwarz
        const eff = (k.faehigkeiten || []).map(f => EFFEKT_ID[f.id]).find(Boolean), ichBild = (k.duc_bilder || {}).idle || "";
        const set = k.held ? k.held.fx_set : (ichBild.match(/\/kampfbild\/(Duc[A-Za-z]+)\//) || [])[1];
        if (eff && set && OPT.fx && window.EdenCombatEffects && EdenCombatEffects.cutinVorladen)
          EdenCombatEffects.cutinVorladen({effekt: eff, duc: k.held ? set : set.replace(/Mop$/, "Bat"), gegner: {idle: bild(g, "idle"), hurt: bild(g, "hurt"), guard: bild(g, "guard")}});
      } catch(e){} }
    const ducIdle = dbild(k, "idle");
    const ich = (!k.held && V && V.profil && V.profil.aktiv) || (ducIdle ? ducIdle.replace(/\/[^\/?]+\.webp/, "/avatar.webp") : null);
    const zf = (k.zugfolge || []).slice(0, 3);
    // eine Gegnerin: Duc und sie im Wechsel; mehrere (29.10.2026): Duc, dann alle der Reihe nach - mit dem Bild des jeweiligen
    const kette = multi ? [{wer: "du"}, ...zf.map(x => ({wer: "g", x, g: k.gegner.find(y => y.instanz === x.instanz) || g}))]
      : zf.flatMap(x => [{wer: "du"}, {wer: "g", x, g}]);
    const laeuft = !k.ergebnis, wahl = laeuft && k.phase !== "parade" && !busy();
    const zeilen = (k.log || []).flatMap(e => e.zeilen).slice(-2);
    const pose = aktuellePose(k, 0);
    const marken = [k.parade_serie ? `<span class="marke offen">Parries ${k.parade_serie}/3</span>` : ""].join(" ");
    const fz = k.faehigkeiten.map((f, i) => [f, i]);
    const grund = fz.filter(([f]) => f.art !== "spezial"), spezial = fz.filter(([f]) => f.art === "spezial");
    const liste = ST.panel === "faehigkeit" ? `<h5>Skills · Stamina ${sp.ausdauer}/${sp.ausdauer_max}</h5>
        ${spezial.length ? `<div class="kgrid">${spezial.map(([f, i]) => karte(f, i, wahl)).join("")}</div>` : `<p class="leer">No special attacks yet. Skill points start at level 3.</p>`}
        <h5>Always available</h5><div class="grund">${grund.map(([f, i]) => karte(f, i, wahl)).join("")}</div>`
      : ST.panel === "gegenstand" ? k.gegenstaende.map((x, i) => `
        <button class="fz item" type="button" ${x.gesperrt || !wahl ? "disabled" : ""} onclick="EdenCombat.zug('gegenstand','${esc(x.id)}')" title="Key ${i + 1}${x.schnell ? " · quick: costs no turn" : ""}">
          <span class="ic"><img src="/itembild/${esc(x.id)}" alt="" onerror="this.remove()"></span><span><b>${esc(x.label)}${x.n > 1 ? ` <small style="display:inline;color:var(--akz)">×${x.n}</small>` : ""}</b><small>${esc(x.gesperrt || x.text || "")}</small></span>
          <span class="zahl schnell">${x.schnell ? uiIc("stamina", "imtext") + " quick" : ""}</span><span class="zahl" style="color:var(--gut)">${esc(x.zahl || "")}</span></button>`).join("") : "";
    let h = `<div class="kampf ${ST.panel ? "mit-liste" : ""} ${ST.probe ? "probe" : ""} ${multi ? "gruppe" : ""} ${ST.zielwahl ? "zielwahl" : ""}">${k.vorschau_hinweis ? `
      <div class="vorschau-hinweis" style="position:absolute;top:8px;left:50%;transform:translateX(-50%);z-index:50;max-width:70%;padding:6px 14px;border-radius:var(--r-taste);background:rgba(160,40,20,.92);color:#fff;font-size:var(--t-klein);text-align:center;pointer-events:none">${uiIc("warning", "imtext")} ${esc(k.vorschau_hinweis)}</div>` : ""}
      <div class="zugfolge rauch">${kette.map((x, i) => `${i ? `<span class="zpfeil">›</span>` : ""}<span class="zf z${x.wer} ${i === 0 && laeuft ? "an" : ""} ${x.wer === "g" && x.x.sa ? (x.x.tut_weh ? "sa weh" : "sa") : ""}"
          ${x.wer === "du" ? (ich ? `style="background-image:url('${esc(ich)}')"` : "") : (x.g.bilder.avatar ? `style="background-image:url('${esc(x.g.bilder.avatar)}')"` : "")}
          title="${x.wer === "du" ? esc((k.held || {}).name || "Duc") : esc(x.g.name + ": " + x.x.label + (x.x.sa ? (x.x.tut_weh ? " – special attack, hurts" : " – special attack, harmless") : ""))}">${x.wer === "du" ? (ich ? "" : "D") : (x.g.bilder.avatar ? "" : esc(x.g.name[0]))}${x.wer === "g" ? `<b>${esc(x.x.icon)}</b>` : ""}</span>`).join("")}
        <small>Round ${k.runde}</small></div>
      <div class="log1">${zeilen.map(t => `<span>${esc(t)}</span>`).join("")}</div>
      <div class="schatten d"></div><div class="schatten g"></div>
      ${dbild(k, dAktuell(k)) ? `<img class="dsprite" src="${esc(dbild(k, dAktuell(k)))}" alt="${esc((k.held || {}).name || "Duc")}">` : ""}
      ${multi ? gruppeHtml(k) : bild(g, pose) ? `<img class="gsprite ziel ${k.ergebnis && k.ergebnis.art === "entkommen" ? "weg" : ""} ${ST.bewegung}" data-i="0" data-inst="${esc(g.instanz)}" src="${esc(bild(g, pose))}" alt="${esc(g.name)}">` : ""}
      ${multi ? gleisteHtml(k, laeuft, marken) : ""}
      ${ST.zielwahl ? `<div class="zielwahl-hinweis">${uiIc("target", "imtext")} Choose a target <small>← → or 1–${k.gegner.filter(x => !x.aus).length} · Enter · Esc to go back</small></div>` : ""}
      ${laeuft ? wurfRestHtml() : ""}
      ${multi ? "" : `<div class="gk rauch"><h4><span class="schild" title="Composure – at 0 they give up">${g.fassung}</span><span>${esc(g.name)}<small>Lv ${g.level} · <span class="bedrohung ${esc(g.bedrohung.id)}">${esc(g.bedrohung.label)}</span>${g.element ? " · " + elementHtml(g.element) : ""}</small></span></h4>
        <div class="zeile"><span>Life</span>${bar(g.lp, g.lp_max, "lp")}<span class="zahl">${g.lp}/${g.lp_max}</span></div>
        <div class="zeile"><span>Composure</span>${bar(g.fassung, g.fassung_max, "fas")}<span class="zahl">${g.fassung}/${g.fassung_max}</span></div>
        <div class="icon-reihe">${g.attribute.map(x => `<span class="ic ${x.status === "schwach" ? "schwach" : x.status === "getestet" ? "getestet" : ""}"
            title="${ATTR[x.id]}${x.status === "schwach" ? " – weakness!" : x.status === "getestet" ? " – no weakness" : " – unknown"}">${x.status === "unbekannt" ? "?" : uiIc(x.id, "imtext")}</span>`).join("")}</div>
        <div class="chips">${chips(g.zustaende)} ${marken}</div></div>`}
      <div class="du rauch"><h4>${esc((k.held || {}).name || "Duc")} <small>Lv ${sp.level}${sp.hauptpfad && !k.held ? " · " + esc(sp.hauptpfad) : ""}</small></h4>
        <div class="zeile"><span>Life</span>${bar(sp.lp, sp.lp_max, "lp du")}<span class="zahl">${sp.lp}/${sp.lp_max}</span></div>
        <div class="zeile"><span>Stamina</span>${pips(sp.ausdauer, sp.ausdauer_max)}<span class="zahl">${sp.ausdauer}/${sp.ausdauer_max}</span></div>
        <div class="ausr-kurz" title="${esc(sp.weapon.label)}${sp.weapon.untertitel ? " (" + esc(sp.weapon.untertitel) + ")" : ""}${sp.armor ? " · " + esc(sp.armor.label) + (sp.armor.untertitel ? " (" + esc(sp.armor.untertitel) + ")" : "") : ""} · Crit ${sp.krit} %">
          <span><b>${esc(sp.weapon.label)}</b>${sp.armor ? ` · <b>${esc(sp.armor.label)}</b>` : ""}</span><em>${sp.weapon.element ? elementHtml(sp.weapon.element) : "no element"}</em></div>
        <div class="chips">${chips(sp.zustaende)}${sp.charged ? `<span class="chip glut">${uiIc("burn", "imtext")} Weapon charged</span>` : ""}${sp.rausch > 0 ? `<span class="chip glut">${uiIc("burn", "imtext")} Furia ${sp.rausch}</span>` : ""}${sp.wind > 0 ? `<span class="chip">${uiIc("air", "imtext")} Libeccio ${sp.wind}</span>` : ""}${sp.sure_crit ? `<span class="chip">${uiIc("target", "imtext")} sure crit</span>` : ""}</div>
        <div class="cmds">${(k.befehle || []).map((b, i) => `<button class="cmd ${ST.panel === b.id ? "an" : ""}" type="button" ${b.gesperrt || !wahl ? "disabled" : ""}
            onclick="EdenCombat.befehl('${b.id}')"><span class="kbd">${i + 1}</span><b>${esc(b.label)}</b><small>${esc(b.gesperrt || unter(b.id, k))}</small></button>`).join("")}
          ${k.phase === "parade" ? `<div class="zahl" style="padding:6px 10px;color:var(--akz)">They strike – parry!</div>
            ${!ST.probe && !busy() ? `<button class="cmd" type="button" onclick="EdenCombat.paradeNeu()"><span class="kbd">␣</span><b>Start parry</b><small>if the test didn't appear</small></button>` : ""}` : ""}</div></div>
      ${liste && wahl ? `<div class="liste rauch ${ST.panel === "faehigkeit" ? "karten" : ""}">${liste}</div>` : ""}`;
    if (k.ergebnis) h += endeBereit(k) ? endeHtml(z, k) : `<div class="kampf-ende-halt" onclick="EdenCombat.endeJetzt()"></div>`;
    return h + `</div>`;
  }
  // Gruppe auf der Buehne (29.10.2026): 2-3 Sprites nebeneinander, das Ziel leuchtet, Besiegte bleiben blass liegen.
  // Klick auf einen Gegner waehrend der Zielwahl bestaetigt ihn.
  const GRUPPE_X = {2: [12, 38], 3: [6, 28, 50]};          // vh rechts von der Mitte, wie die Einzelfigur bei 25vh
  function gruppeHtml(k){
    const xs = GRUPPE_X[k.gegner.length] || GRUPPE_X[3], zi = zielI(k);
    return k.gegner.map((x, i) => {
      const src = bild(x, aktuellePose(k, i)); if (!src) return "";
      return `<img class="gsprite gi ${i === zi && !x.aus ? "ziel" : ""} ${x.aus ? "aus" : ""} ${ST.zielwahl && !x.aus ? "waehlbar" : ""}"
        data-i="${i}" data-inst="${esc(x.instanz)}" style="left:calc(52% + ${xs[i]}vh);z-index:${10 + i}" src="${esc(src)}" alt="${esc(x.name)}"
        ${ST.zielwahl && !x.aus ? `onclick="EdenCombat.zielBestaetigen(${i})"` : ""}>`;
    }).join("");
  }
  // Gegnerleiste: je Gegner Name, Leben und die naechste Absicht - wie die Gegnerliste in Final Fantasy
  function gleisteHtml(k, laeuft, marken){
    const zi = zielI(k);
    return `<div class="gleiste rauch">${k.gegner.map((x, i) => {
      const a = x.absicht || {};
      return `<button type="button" class="gl ${i === zi && !x.aus ? "ziel" : ""} ${x.aus ? "aus" : ""} ${a.sa ? (a.tut_weh ? "sa-weh" : "sa") : ""}"
        ${x.aus || !ST.zielwahl ? "disabled" : `onclick="EdenCombat.zielBestaetigen(${i})"`} title="${esc(x.name)}${x.aus ? " – out" : a.label ? ": " + esc(a.label) : ""}">
        <b>${i === zi && !x.aus ? "▶ " : ""}${esc(x.name)}</b>${bar(x.lp, x.lp_max, "lp")}
        <small>${x.aus ? ({ko: "down", aufgabe: "gave up", entkommen: "fled"}[x.aus] || "out") : laeuft && a.label ? `${esc(a.icon || "")} ${esc(a.label)}` : ""}</small>${i === zi && !x.aus ? gZiel(x, marken) : ""}</button>`;
    }).join("")}</div>`;
  }
  // Das aktuelle Ziel klappt in der Gegnerleiste auf: Fassung, Schwaechen, Zustaende (Duc 30.10.2026)
  function gZiel(x, marken){
    return `<span class="gl-mehr"><span class="gl-rang">Lv ${x.level} · <span class="bedrohung ${esc(x.bedrohung.id)}">${esc(x.bedrohung.label)}</span>${x.element ? " · " + elementHtml(x.element) : ""}</span>
      <span class="zeile"><span>Composure</span>${bar(x.fassung, x.fassung_max, "fas")}<span class="zahl">${x.fassung}/${x.fassung_max}</span></span>
      <span class="icon-reihe">${x.attribute.map(y => `<span class="ic ${y.status === "schwach" ? "schwach" : y.status === "getestet" ? "getestet" : ""}"
        title="${ATTR[y.id]}${y.status === "schwach" ? " – weakness!" : y.status === "getestet" ? " – no weakness" : " – unknown"}">${y.status === "unbekannt" ? "?" : uiIc(y.id, "imtext")}</span>`).join("")}</span>
      <span class="chips">${chips(x.zustaende)} ${marken}</span></span>`;
  }
  function unter(id, k){
    const sp = k.spieler;
    const voll = sp.ausdauer >= sp.ausdauer_max ? " (full)" : "";   // stamina is capped, so say so instead of a promise
    if (id === "angriff") return sp.angriff + " damage · crit " + sp.krit + " % · +1 stamina" + voll;
    if (id === "faehigkeit") return k.faehigkeiten.filter(f => !f.gesperrt).length + " possible";
    if (id === "verteidigen") return "Hit halved · +2 stamina" + voll + " · easier parry";
    if (id === "gegenstand") return k.gegenstaende.length ? k.gegenstaende.map(x => x.label).join(", ") : "nothing on you";
    if (id === "fliehen") return "Courage test · fail and they strike";
    if (id === "aussetzen") return "You have to skip this round";
    return "";
  }
  const SCHLAF_NEBEL_MS = 1800;                            // so lange nach dem Einschlag, bis die Wolke das Tier verhuellt
  // Erst atmen, dann die Karte (Duc 01.11.2026): Der letzte Treffer und die Wolke der Schlafgranate sollen wirken, bevor Ergebnis und Level-up kommen. Klick oder Taste ueberspringt.
  function endeBereit(k){
    if (ST.endeFuer !== k.id){
      const gran = (k.events || []).find(e => e.art === "gegenstand" && e.granate);
      const warte = 1500 + (gran ? ((window.EdenCombatEffects && EdenCombatEffects.WURF_MS) || 520) + (gran.granate === "schlaf" ? 3200 : 400) : 0);
      ST.endeFuer = k.id; ST.endeAb = performance.now() + warte;
      setTimeout(() => zeichnen(), warte + 20);
    }
    return performance.now() >= ST.endeAb;
  }
  // Ergebnis-Karte mit Erfahrung und Skillwahl beim Levelaufstieg
  function endeHtml(z, k){
    const e = k.ergebnis, sp = k.spieler, pr = z.kampf_profil;
    // Level-up ceremony (28.10.2026): every level up, Maxwell's training included, gets the full screen (eden-levelup.js)
    if (e.aufstieg && pr && window.EdenLevelUp) return EdenLevelUp.html(z, k, {titel: ENDE[e.art] || "Over"});
    const lernbar = pr ? pr.pfade.flatMap(p => p.skills.filter(s => !s.gelernt && !s.grund).map(s => ({...s, pfad: p}))) : [];
    // Level-up (26.10.2026): first the attribute points, then the skill points; "Later" keeps them for the Character menu
    const ap = pr ? pr.attributpunkte || 0 : 0, auf = e.aufstieg;
    const gewinn = auf ? [`+${auf.lp} HP`, auf.ausdauer ? `+${auf.ausdauer} stamina` : "", `+${auf.auf - auf.von} attribute point${auf.auf - auf.von > 1 ? "s" : ""}`,
      e.skillpunkte && pr && pr.skillpunkte ? `skill point ready` : ""].filter(Boolean) : [];
    const attrwahl = pr && ap > 0 ? `<div class="attrwahl"><h3>${ap} attribute point${ap > 1 ? "s" : ""} to spend</h3>
        <div class="agrid">${pr.attribute.map(a => `<button class="attr" type="button" ${busy() || a.wert >= (a.max || 5) ? "disabled" : ""}
          onclick="EdenSfx&&EdenSfx.play('level_up');senden('attribut_steigern',{id:'${esc(a.id)}'},'…')"><span class="attr-kopf"><b>${esc(a.label)}</b><span class="zahl">${a.wert}/${a.max || 5}</span></span>
          <span class="attr-pips">${Array.from({length: a.max || 5}, (_, i) => `<i class="${i < a.wert ? "an" : ""}"></i>`).join("")}</span>
          <span class="attr-wirk">${esc(a.wirkung || "")}</span><span class="attr-plus">+1</span></button>`).join("")}</div></div>` : "";
    if (auf && ST.aufstiegTon !== k.id + ":" + auf.auf) { ST.aufstiegTon = k.id + ":" + auf.auf; ton("level_up", 900); }   // einmal je Ergebnis, nach dem Siegton
    const aufstieg = auf ? `<div class="aufstieg"><small>Level up</small><b>LEVEL ${auf.auf}</b><span class="gewinne">${gewinn.map(g => `<span>${esc(g)}</span>`).join("")}</span></div>` : "";
    const wahl = pr && pr.skillpunkte > 0 && ap === 0 ? `<div class="skillwahl"><h3>${pr.skillpunkte} skill point${pr.skillpunkte > 1 ? "s" : ""} free – choose a special attack</h3>
        <div class="kgrid">${lernbar.map(s => `<button class="fk ${PFAD[s.pfad.id]}" type="button" ${busy() ? "disabled" : ""} onclick="EdenSfx&&EdenSfx.play('level_up');senden('skill_lernen',{id:'${esc(s.id)}'},'…')">
          <span class="kopf"><span class="name">${esc(s.label)}</span><span class="pfad">${esc(s.pfad.name)} ${s.stufe}</span></span>
          <span class="wirk">${esc(s.text)}</span><span class="fuss"><span class="pill kosten">${s.kosten} ${uiIc("stamina", "imtext")}</span></span></button>`).join("")}</div>
        ${pr.hinweis ? `<p class="hinweis">${esc(pr.hinweis)}</p>` : ""}</div>` : "";
    // Try again (Duc 03.11.2026): once per fight the same fight again, same HP and bag; otherwise the usual defeat
    if (e.nochmal) return `<div class="ende"><div class="karte"><h2>${ENDE[e.art] || "Over"}</h2><p>${esc(e.text)}</p>
      <p class="leer">One more try: the same fight, with the HP and the bag you came in with. Lose again and the defeat counts.</p>
      <div class="knopfzeile"><button class="knopf" type="button" onclick="senden('kampf_nochmal',{},'…')" ${busy() ? "disabled" : ""}>Try again</button>
      <button class="knopf leise" type="button" onclick="senden('kampf_nochmal',{annehmen:true},'…')" ${busy() ? "disabled" : ""}>Accept the defeat</button></div></div></div>`;
    // Expedition (26.10.2026): nach einer Niederlage behaelt Duc genau EIN Stueck der Beute, der Rest ist weg
    const ex = e.art === "niederlage" && z.expedition, beute = ex ? ex.beute : [];
    const behalten = beute.length ? `<div class="behalten"><h3>Everything goes black. What do you still have in your hand?</h3>
        <p class="leer">You keep one thing you found on the way. The rest is lost. Experience stays.</p>
        <div class="kgrid">${beute.map(b => `<button class="fk ${ex.behalten === b.id ? "an" : ""}" type="button" ${busy() ? "disabled" : ""}
          onclick="senden('expedition_behalten',{id:'${esc(b.id)}'},'…')"><span class="name">${esc(b.label)}</span></button>`).join("")}
          <button class="fk ${ex.gewaehlt && !ex.behalten ? "an" : ""}" type="button" ${busy() ? "disabled" : ""} onclick="senden('expedition_behalten',{id:''},'…')"><span class="name">Nothing</span></button></div></div>` : "";
    const warten = beute.length && !ex.gewaehlt;
    const offen = ap > 0 || (pr && pr.skillpunkte > 0);
    return `<div class="ende"><div class="karte ${wahl || behalten || attrwahl ? "breit" : ""}">${aufstieg}<h2>${ENDE[e.art] || "Over"}</h2><p>${esc(e.text)}</p>
      ${(e.zeilen || []).length ? `<div class="folgen">${e.zeilen.map(t => `<span>${esc(t)}</span>`).join("")}</div>` : ""}
      <p class="zahl">${e.wieder_auf != null ? `Duc ${uiIc("hp", "imtext")} 0/${sp.lp_max} · you come to with ${e.wieder_auf} HP` : `${esc((k.held || {}).name || "Duc")} ${uiIc("hp", "imtext")} ${pr && auf ? pr.lp : sp.lp}/${pr && auf ? pr.lp_max : sp.lp_max}`} · Level ${e.level || sp.level} · ${k.runde} rounds</p>${attrwahl}${wahl}${behalten}
      <button class="knopf" type="button" onclick="senden('kampf_schliessen',{},'…')" ${busy() || warten ? "disabled" : ""}>${warten ? "Choose first" : offen ? "Later · Continue" : "Continue"}</button>
      ${offen && !warten ? `<p class="leer">Points you don't spend now wait for you in the Character menu.</p>` : ""}</div></div>`;
  }

  // ------------------------------------------------------------------ Reiter "Ausrüstung" (Laden & Inventar)
  function gearZeile(x, art){
    if (!x) return "–";
    const name = `${esc(x.label)}${x.untertitel ? ` <i>(${esc(x.untertitel)})</i>` : ""}${x.stufe ? ` · level ${x.stufe}` : ""}`;
    return art === "waffe" ? `${name} · damage +${x.schaden} · ${esc(x.art)}${x.stein ? " · stone: " + esc(x.stein) : ""}${x.element ? " · " + esc(ELEMENT[x.element]) : ""}${x.slots > 1 ? " · two-handed" : ""}`
      : `${name} · protection +${x.schutz}${x.widerstand ? " · resists " + esc(ELEMENT[x.widerstand] || "every element") : ""}${x.schwer ? " · heavy" : ""}`;
  }
  function ausruestungHtml(z, nurAnsicht){
    const p = z.kampf_profil;
    if (!p) return `<p class="leer">This adventure has no fights.</p>`;
    const imKampf = (z.kampf && !z.kampf.ergebnis) || nurAnsicht;
    const knopf = (platz, x, an) => `<button class="mini" type="button" ${an || imKampf || busy() ? "disabled" : ""}
        onclick="senden('ausruesten',{platz:'${platz}',id:${x ? `'${esc(x.id)}'` : "null"}},'…')">${an ? "Angelegt" : "Anlegen"}</button>`;
    const liste = (xs, platz, aktuell, art) => xs.map(x => `<div class="ware ${x.seltenheit || ""}"><span class="art">${esc({gewoehnlich: "Common", selten: "Rare", episch: "Epic", legendaer: "Legendary"}[x.seltenheit] || "")}</span>
        <b>${esc(x.label)}${x.untertitel ? ` <i>(${esc(x.untertitel)})</i>` : ""}</b><small>${gearZeile(x, art)}${x.eigenschaft ? `<br>${esc(x.eigenschaft)}` : ""}</small><div class="zeile">${knopf(platz, x, aktuell && aktuell.id === x.id)}</div></div>`).join("");
    return `<div class="ausruestung">
      <div class="werte"><b>Level ${p.level}</b>${p.level < p.level_max ? ` · experience ${p.xp}/${p.xp_next}` : " · max level"} · ${uiIc("hp", "imtext")} ${p.lp}/${p.lp_max} · stamina ${p.ausdauer}${p.hauptpfad ? " · main path " + esc(p.hauptpfad) : ""}${p.test ? ` <span class="tag">test switch</span>` : ""}
        <div class="attr">${p.attribute.map(a => `<span title="${a.wert > a.basis ? "grows with your main path" : ""}">${esc(a.label)} <b>${a.wert}</b>${a.wert > a.basis ? " ▲" : ""}</span>`).join("")}</div></div>
      ${nurAnsicht ? `<p class="hinweis">You can only look here. Changing, chips and upgrades happen in Rosi's workshop (Shop &amp; Inventory).</p>`
        : imKampf ? `<p class="leer">You can't change in the middle of a fight.</p>` : ""}
      <h3>Weapon <small class="leer">· ${gearZeile(p.waffe, "waffe")}</small></h3><div class="inv">${liste(p.waffen, "weapon", p.waffe, "waffe")}</div>
      <h3>Jacket <small class="leer">· ${gearZeile(p.ruestung, "ruestung")}</small></h3>
      <div class="inv">${liste(p.ruestungen, "armor", p.ruestung, "ruestung")}</div>
    </div>`;
  }

  // ------------------------------------------------------------------ Upgrade-Fenster: Chips und Rosis Verbesserungen (Kabine)
  const UP = {tab: "umziehen", chip: null, charm: null, filter: "alle"};
  const KAT_DE = {wucht: "Impact", praezision: "Precision", technik: "Technique", konter: "Counter", zustand: "Condition", element: "Element",
                  schutz: "Protection", parade: "Parry", ausdauer: "Stamina", erholung: "Recovery", auftritt: "Presence", abwehr: "Resistance", aufklaerung: "Scouting"};   // display names (English)
  const STUFE_NAME = ["", "bronze", "silver", "gold"];
  const FORM = {waffe: "M32 4 L60 32 L32 60 L4 32 Z", jacke: "M32 4 L56 11 V32 C56 46 46 55 32 61 C18 55 8 46 8 32 V11 Z"};
  function chipBild(c){
    return c.bekannt ? `/chipbild/${esc(c.id)}.png` : `/chipbild/kat/${esc(c.kategorie)}-${STUFE_NAME[c.stufe]}.png`;
  }
  function slotSvg(gruppe, art, hinweis){
    const o = FORM[gruppe];
    const rand = art === "frei" ? `fill="rgba(216,189,134,.07)" stroke="#d8bd86" stroke-width="2" stroke-dasharray="4 4"`
      : `fill="rgba(255,255,255,.02)" stroke="#444a55" stroke-width="2"`;
    const inh = art === "frei" ? `<text x="32" y="41" text-anchor="middle" font-size="24" fill="#d8bd86" font-family="system-ui">+</text>`
      : `<g transform="translate(22 22)" fill="none" stroke="#6b7280" stroke-width="2" stroke-linecap="round"><rect x="2" y="9" width="16" height="11" rx="2"/><path d="M5 9V6a5 5 0 0 1 10 0v3"/></g>`;
    return `<svg viewBox="0 0 64 64" width="64" height="64" aria-hidden="true"><path d="${o}" ${rand} stroke-linejoin="round"/>${inh}</svg>`;
  }
  function chipKnopf(c, z){
    const gew = UP.chip === c.familie, steckt = c.ort ? "steckt an " + c.ort.split(":")[1] : "";
    return `<button type="button" class="chipk ${gew ? "an" : ""} ${c.ort ? "belegt" : ""}" onclick="EdenCombat.chipWahl('${esc(c.familie)}')" title="${esc(c.text)}">
      <img src="${chipBild(c)}" alt="" width="52" height="52"><span><b>${c.bekannt ? esc(c.label) : "Unidentified Chip"}</b>
      <small>${esc(KAT_DE[c.kategorie])} · ${c.gruppe === "waffe" ? "Weapon" : "Jacket"}${c.ort ? " · fitted" : ""}</small></span></button>`;
  }
  function slotKnopf(st, i, chip, z){
    const key = `${st.slot}:${st.id}`;
    if (i < st.belegt.length){
      const c = chip(st.belegt[i]);
      return `<button type="button" class="slotk voll" onclick="EdenCombat.chipWeg('${st.slot}','${esc(st.id)}','${esc(c.familie)}')" title="${esc(c.label)} – entfernen (${esc(c.text)})">
        <img src="${chipBild(c)}" alt="" width="60" height="60"></button>`;
    }
    if (i < st.plaetze){
      const sel = UP.chip && chip(UP.chip), ok = sel && sel.bekannt && sel.gruppe === st.gruppe && (!sel.nur_waffe || sel.nur_waffe === st.id);
      return `<button type="button" class="slotk frei ${ok ? "ziel" : ""}" ${ok ? `onclick="EdenCombat.chipSetzen('${st.slot}','${esc(st.id)}')"` : "disabled"}
        title="${ok ? "Fit here" : "Free slot – pick a matching chip first"}">${slotSvg(st.gruppe, "frei")}</button>`;
    }
    return `<div class="slotk zu" title="More slots through Rosi's upgrades">${slotSvg(st.gruppe, "zu")}<small>Rosi ${i}</small></div>`;
  }
  // Jacken-Charm (28.10.2026): runder Platz, versetzt neben den Erweiterungen; erscheint mit dem ersten Charm
  function charmSlot(st, ch){
    if (st.gruppe !== "jacke" || !(ch.charms || []).length) return "";
    const c = st.charm && ch.charms.find(x => x.id === st.charm);
    if (c) return `<button type="button" class="slotk charmslot voll" onclick="EdenCombat.charmWeg('${esc(st.id)}','${esc(c.id)}')" title="${esc(c.label)} – take off (${esc(c.wirkung)})"><img src="${esc(c.bild)}" alt="" width="62" height="62"></button>`;
    const ok = !!UP.charm;
    return `<button type="button" class="slotk charmslot frei ${ok ? "ziel" : ""}" ${ok ? `onclick="EdenCombat.charmSetzen('${esc(st.id)}')"` : "disabled"} title="${ok ? "Hang it here" : "Charm slot – pick a charm first"}"><span>+</span></button>`;
  }
  function charmKnopf(c){
    return `<button type="button" class="chipk charmk ${UP.charm === c.id ? "an" : ""} ${c.an ? "belegt" : ""} ${esc(c.seltenheit)}" onclick="EdenCombat.charmWahl('${esc(c.id)}')" title="${esc(c.text)}">
      <img src="${esc(c.bild)}" alt="" width="52" height="52"><span><b>${esc(c.label)}</b><small>${esc(c.wirkung)}${c.an ? " · on a jacket" : ""}</small></span></button>`;
  }
  function upgradeHtml(z){
    const p = z.kampf_profil, w = p && p.werkstatt, ch = p && p.chips;
    if (!p || !ch) return `<p class="leer">No upgrades here.</p>`;
    const reiter = `<div class="reiterzeile up-reiter">${[["umziehen", "Change"], ["chips", "Chips"], ["rosi", "Upgrade"]].map(([k, l]) =>
      `<button type="button" aria-pressed="${UP.tab === k}" onclick="EdenCombat.upTab('${k}')">${l}</button>`).join("")}</div>`;
    if (UP.tab === "umziehen") return reiter + ausruestungHtml(z);
    if (UP.tab === "rosi") return reiter + werkstattHtml(z);
    const byFam = {};
    ch.pool.forEach(c => { byFam[c.familie] = c; });
    const chip = f => byFam[f];
    if (UP.chip && !byFam[UP.chip]) UP.chip = null;
    const pool = ch.pool.filter(c => UP.filter === "alle" || c.gruppe === UP.filter);
    const sel = UP.chip && byFam[UP.chip];
    const charmsAll = ch.charms || [], selC = UP.charm && charmsAll.find(c => c.id === UP.charm);
    if (UP.charm && !selC) UP.charm = null;
    const rosiSatz = sel && sel.bekannt && ch.rosi && ch.rosi[sel.kategorie];
    return `${reiter}<div class="upgrade">
      ${ch.nutzbar ? "" : `<p class="hinweis">You've found strange chips, but you don't know what they do. Rosi's workshop is still wrecked.</p>`}
      <div class="up-stuecke">${ch.stuecke.map(st => `<div class="up-stueck ${st.getragen ? "getragen" : ""}"><div class="up-kopf"><b>${esc(st.label)}</b>
          <small>${esc(st.untertitel || "")}${st.getragen ? " · getragen" : ""}</small></div>
          <div class="up-slots">${[0, 1, 2].map(i => slotKnopf(st, i, chip, z)).join("")}${charmSlot(st, ch)}</div></div>`).join("") || `<p class="leer">No gear.</p>`}</div>
      <div class="up-pool"><div class="up-filter">${[["alle", "Alle"], ["waffe", "Waffen"], ["jacke", "Jacken"]].map(([k, l]) =>
        `<button type="button" aria-pressed="${UP.filter === k}" onclick="EdenCombat.upFilter('${k}')">${l}</button>`).join("")}
        <span class="leer">${ch.pool.length} Chips</span></div>
        <div class="chipraster">${pool.map(c => chipKnopf(c, z)).join("") || `<p class="leer">No chips yet. Animals with collars and agents carry them.</p>`}</div>
        ${charmsAll.length ? `<h4 class="up-charms">Charms <small>${charmsAll.length}</small></h4><div class="chipraster">${charmsAll.map(charmKnopf).join("")}</div>` : ""}
        <div class="up-info">${selC ? `<b>${esc(selC.label)}</b> <small>${esc(selC.wirkung)}</small><br>${esc(selC.text)}
          ${selC.an ? `<br><small class="leer">On ${esc((ch.stuecke.find(s => s.id === selC.an) || {}).label || selC.an)}. Pick another jacket's round slot and it moves.</small>` : `<br><small class="leer">Pick a jacket's round slot. Only the jacket you wear counts.</small>`}` : sel ? `<b>${sel.bekannt ? esc(sel.label) : "Unidentified Chip"}</b> <small>${esc(KAT_DE[sel.kategorie])} · level ${sel.stufe}</small><br>
          ${sel.bekannt ? esc(sel.text) : "A strange chip. Maybe Rosi can make something out of it."}
          ${rosiSatz ? `<br><i>Rosi: “${esc(rosiSatz)}”</i>` : ""}
          ${sel.ort ? `<br><small class="leer">Fitted to ${esc(sel.ort.split(":")[1])}. Pick another slot and it moves.</small>` : ""}` :
          `<span class="leer">Pick a chip, then a free slot. A chip only ever sits on one piece.</span>`}</div></div></div>`;
  }
  function chipWahl(f){ UP.chip = UP.chip === f ? null : f; UP.charm = null; if (typeof zeichnen === "function") zeichnen(); }
  function charmWahl(c){ UP.charm = UP.charm === c ? null : c; UP.chip = null; if (typeof zeichnen === "function") zeichnen(); }
  function charmSetzen(jacke){ if (UP.charm){ ton("chip_einrasten"); senden("chip_einsetzen", {platz: "armor", id: jacke, familie: "charm:" + UP.charm}, "…"); UP.charm = null; } }
  function charmWeg(jacke, c){ senden("chip_entfernen", {platz: "armor", id: jacke, familie: "charm:" + c}, "…"); }
  function chipSetzen(slot, id){ if (UP.chip){ ton("chip_einrasten"); senden("chip_einsetzen", {platz: slot, id, familie: UP.chip}, "…"); } }
  function chipWeg(slot, id, familie){ senden("chip_entfernen", {platz: slot, id, familie}, "…"); }
  function upTab(t, still){ UP.tab = t; if (!still && typeof zeichnen === "function") zeichnen(); }
  function upFilter(f){ UP.filter = f; if (typeof zeichnen === "function") zeichnen(); }

  // ------------------------------------------------------------------ Rosis Werkstatt (Kabine, "Für Rosi", 25.10.2026)
  function werkstattHtml(z){
    const w = z.kampf_profil && z.kampf_profil.werkstatt;
    if (!w) return `<p class="leer">No workshop here.</p>`;
    const zeile = x => `<div class="ware"><b>${esc(x.label)}${x.untertitel ? ` <i>(${esc(x.untertitel)})</i>` : ""}</b>
        <small>Level ${x.stufe}/${x.stufe_max}${x.kosten ? ` · next: ${x.kosten.geld} € + ${esc(x.kosten.material)}` : " · fully upgraded"}</small>
        ${x.kosten && x.fehlt ? `<small class="leer">${esc(x.fehlt)}</small>` : ""}
        <div class="zeile">${x.kosten ? `<button class="mini" type="button" ${x.fehlt || busy() ? "disabled" : ""}
          onclick="LADEN.stimmung='kauf';senden('werkstatt_abgeben',{platz:'${x.slot}',id:'${esc(x.id)}'},'Rosi takes it …')">Hand to Rosi</button>` : ""}</div></div>`;
    return `<div class="ausruestung">
      ${w.offen ? `<p class="leer">Rosi upgrades one piece a night: +1 damage or +1 protection, twice per piece. Handing it in costs no action, and she texts you the next morning. Account: ${w.konto} €.</p>`
        : `<p class="hinweis">${esc(w.text_zu)}</p>`}
      ${w.auftrag ? `<p class="hinweis">With Rosi: ${esc(w.auftrag.label)} (level ${w.auftrag.stufe}) – ready tomorrow morning.</p>` : ""}
      <h3>Weapons</h3><div class="inv">${w.waffen.map(zeile).join("")}</div>
      <h3>Jackets</h3><div class="inv">${w.ruestungen.map(zeile).join("")}</div>${taschenHtml(w.tasche)}</div>`;
  }
  // Tasche bei Rosi (Duc 29.10.2026): je Akt ein Upgrade, nur Geld, sofort fertig
  function taschenHtml(t){
    if (!t) return "";
    const n = t.naechste;
    return `<h3>Bag <small class="leer">· ${t.plaetze} slots</small></h3><div class="inv">${n ? `<div class="ware">
        ${n.bild ? `<img src="${esc(n.bild)}" alt="" width="52" height="52">` : ""}<b>${esc(n.label)}</b>
        <small>${t.plaetze} → ${n.plaetze} slots · ${n.geld} € · ready at once</small><small>${esc(n.text)}</small>
        ${n.fehlt ? `<small class="leer">${esc(n.fehlt)}</small>` : ""}
        <div class="zeile"><button class="mini" type="button" ${n.fehlt || busy() ? "disabled" : ""}
          onclick="LADEN.stimmung='kauf';senden('tasche_kaufen',{},'Rosi fetches the bag …')">Buy from Rosi</button></div></div>`
      : `<p class="leer">Fully upgraded. Rosi says it's her best work.</p>`}</div>`;
  }

  // ------------------------------------------------------------------ Nach dem Zeichnen: Unterschiede zeigen, Parade starten
  function ereignisse(k, spriteEl0, duEl){
    let t = 0;
    for (const e of k.events || []){
      const spriteEl = gsprInst(e.gegner) || spriteEl0;            // mehrere Gegner: der Effekt sitzt am getroffenen (29.10.2026)
      if (e.art === "aus"){ spriteEl.classList.add("aus"); if (((k.gegner || []).find(x => x.instanz === e.gegner) || {}).klasse === "maschine") effekt("funke", spriteEl, {}); continue; }
      if (e.art === "spezial"){
        effekt("spezial", e.phase === "aufladen" || e.phase === "rettung" ? duEl : spriteEl, {id: e.id, effekt: EFFEKT_ID[e.id], phase: e.phase});
        if (e.phase === "start") banner((k.faehigkeiten.find(f => f.id === e.id) || {}).label || "", "spezial", null, 0);
      } else if (e.art === "reaktion"){
        banner(e.name + "!", "reaktion", REAKTION_FARBE[e.name], 350 + t); t += 650;
        effekt("reaktion", spriteEl, {name: e.name});
      } else if (e.art === "krit"){
        pop(spriteEl, "Critical!", "info");
      } else if (e.art === "codex"){
        const kb = document.querySelector("#mitte .kampf");
        if (kb){ const t = document.createElement("div"); t.className = "kampf-codex"; t.innerHTML = `<small>${uiIc("codex", "imtext")} New in the codex</small><b>${esc(e.text)}</b>`;
          kb.appendChild(t); setTimeout(() => t.remove(), 4200); }
      } else if (e.art === "bestiarium"){                   // erste Parade dieser Art: ihr Rhythmus steht jetzt im Codex (03.11.2026)
        const kb = document.querySelector("#mitte .kampf");
        if (kb){ const t = document.createElement("div"); t.className = "kampf-codex"; t.innerHTML = `<small>${uiIc("codex", "imtext")} New in the Bestiary</small><b>${esc(e.name)}: rhythm noted</b>`;
          kb.appendChild(t); setTimeout(() => t.remove(), 4200); }
      } else if (e.art === "zustand" && e.id === "brennend"){
        effekt("brennend", spriteEl, {stufen: e.stufen});
      } else if (e.art === "stimme" && e.schluessel){     // vertonte Zeilen im Kampf: Sirenen-Hinweise, Sprueche der Riccis (29.10.2026)
        try { new Audio("/api/zeile?id=" + encodeURIComponent(e.schluessel)).play().catch(() => {}); } catch (_) {}
        const kb = document.querySelector("#mitte .kampf");
        if (kb && e.text){ kb.querySelectorAll(".kampf-codex.stimme").forEach(x => x.remove());   // nur der neueste Satz
          const t = document.createElement("div"); t.className = "kampf-codex stimme";
          t.innerHTML = `<small>${e.icon ? esc(e.icon) : uiIc("talk", "imtext")} ${esc(e.name || (k.gegner[0] || {}).name || "")}</small><b>“${esc(e.text)}”</b>`;
          kb.appendChild(t); setTimeout(() => t.remove(), 6500); }
      }
    }
  }
  function nachZeichnen(z, V){
    const k = z.kampf, g = zielG(k), sp = k.spieler, vorher0 = ST.letzte;
    const spriteEl = gspr(zielI(k)), duEl = document.querySelector("#mitte .kampf .du");
    // Vergleich je Gegner-Instanz (29.10.2026): das Ziel kann gewechselt haben, Flaechentreffer zeigen bei allen eine Zahl
    const vg = (vorher0 && vorher0.gs && vorher0.gs[g.instanz]) || {};
    const vorher = vorher0 && Object.assign({}, vorher0, {glp: vg.lp ?? vorher0.glp, gfas: vg.fas ?? vorher0.gfas});
    const tw = (k.events || []).filter(e => e.art === "treffer").map(e => e.wirkung);
    const wirk = tw.includes("stark") ? "stark" : tw.includes("schwach") ? "schwach" : "";      // Zahl groß/warm oder klein/blass - kein Text
    // Schaden waehrend der Spezialattacke (27.10.2026): kommt die Antwort, solange die Sequenz laeuft, zeigt die Sequenz die
    // Zahlen im Einschlag; der Kampfbildschirm haelt seinen Vergleichsstand bis danach (ST.letzte bleibt stehen)
    const halten = ST.cutin && vorher && vorher.id === k.id && vorher.rev !== k.revision;
    if (halten && ST.cutinZahlRev !== k.revision && window.EdenCombatEffects && EdenCombatEffects.cutinZahlen){
      ST.cutinZahlRev = k.revision;
      EdenCombatEffects.cutinZahlen({schaden: Math.max(0, vorher.glp - g.lp), wirkung: wirk, krit: (k.events || []).some(e => e.art === "krit"),
                                     fassung: Math.max(0, vorher.gfas - g.fassung), heil: Math.max(0, sp.lp - vorher.dlp)});
    }
    if (!halten && vorher && vorher.id === k.id && vorher.rev !== k.revision){
      const nachCutin = ST.nachCutin, gezeigt = ST.zahlGezeigt;
      ST.nachCutin = false; ST.zahlGezeigt = false;           // die Zwischensequenz hatte ihren eigenen Treffer-/Heilklang
      // Granate (27.10.2026): erst fliegt sie, dann platzt sie - Treffer, Zahl, Zustaende und Reaktionen kommen beim Einschlag
      const gran = (k.events || []).find(e => e.art === "gegenstand" && e.granate);
      const schwungRest = ST.schwungTreffer ? Math.max(0, ST.schwungTreffer - performance.now()) : 0;
      ST.schwungTreffer = 0;
      const wurf = gran ? ((window.EdenCombatEffects && EdenCombatEffects.WURF_MS) || 520) : schwungRest;   // Granate oder Ducs Schlag
      const spaeter = f => wurf ? setTimeout(f, wurf) : f();
      ST.wurfExtra = wurf ? wurf + 650 : 0;
      if (gran){ effekt("granate", spriteEl, {zustand: gran.granate, id: gran.id, von: document.querySelector("#mitte .kampf .dsprite") || duEl});
        ton("kampf_granate_wurf");                             // Klaenge: Ducs Abnahme 28.10. (docs/abnahme/granaten_klang)
        ton(GRANATEN_TON[gran.granate] || "kampf_granate_splitter", wurf);
        if (gran.granate === "geblendet") ton("kampf_granate_pfeifen", wurf + 500);   // Ohrenpfeifen unter der Weissblende
        setTimeout(() => dSetzen(k, "attack", 650, "vor"), EdenCombatEffects.WURF_VOR || 0); }   // Wurfpose erst nach dem Splint-Klick
      else if (g.lp < vorher.glp && !nachCutin) ton(k.held && k.held.id === "maxwell" ? "tk_maxwell_schlag" : "kampf_treffer", wurf);   // Maxwell: Hammer auf Material (Duc 02.11.2026)
      if (g.lp < vorher.glp && !gezeigt) spaeter(() => { pop(spriteEl, "−" + (vorher.glp - g.lp), "schaden " + wirk); effekt("treffer_gegner", spriteEl, {schaden: vorher.glp - g.lp, wirkung: wirk});
        ST.pose = "hurt"; ST.poseBis = performance.now() + (wirk === "stark" ? 850 : 650); spriteSetzen(bild(g, "hurt"), wirk === "stark" ? "treffer-stark" : "treffer", zielI(k));
        setTimeout(() => { if (performance.now() >= ST.poseBis) spriteSetzen(bild(g, grundPose(k, zielI(k))), "", zielI(k)); }, 700); });
      if (mehrere(k) && vorher.gs) k.gegner.forEach((x, i) => {      // die anderen: Flaeche, Brennen, Konter
        const alt = vorher.gs[x.instanz]; if (!alt || x === g) return;
        const el = gspr(i);
        if (x.lp < alt.lp && !gezeigt) spaeter(() => { pop(el, "−" + (alt.lp - x.lp), "schaden"); effekt("treffer_gegner", el, {schaden: alt.lp - x.lp});
          el.classList.remove("treffer"); void el.offsetWidth; el.classList.add("treffer"); });
        if (x.fassung < alt.fas && !gezeigt) pop(el, "Composure −" + (alt.fas - x.fassung), "fassung");
      });
      if (g.fassung < vorher.gfas && !gezeigt){ pop(spriteEl, "Composure −" + (vorher.gfas - g.fassung), "fassung"); effekt("fassung", spriteEl, {minus: vorher.gfas - g.fassung}); }
      const letzter = (k.log || [])[(k.log || []).length - 1];
      if (letzter && letzter.befehl === "angriff" && g.lp === vorher.glp && !tw.length) ton("kampf_ausweichen", wurf);   // Schlag geht daneben
      if (letzter && letzter.befehl === "angriff" && !schwungLaeuft()){ dSetzen(k, "attack", 650, "vor"); ducSchuss(k, "attack"); }
      else if (letzter && letzter.befehl === "faehigkeit") dSetzen(k, "heavy_attack", 650, "vor");
      else if (letzter && letzter.befehl === "verteidigen") dSetzen(k, "guard", 900);
      if (sp.lp < vorher.dlp) ton("kampf_treffer", g.lp < vorher.glp ? 380 : 0);
      if (sp.lp > vorher.dlp && !nachCutin) ton("heilung");
      if ((k.events || []).some(e => e.art === "zustand" || e.art === "zustand_duc")) ton("status", 200 + wurf);
      if (sp.lp < vorher.dlp){ pop(duEl, "−" + (vorher.dlp - sp.lp), "schaden"); effekt("treffer_duc", duEl, {schaden: vorher.dlp - sp.lp});
        dSetzen(k, "hurt", 650, "treffer"); }
      if (sp.lp > vorher.dlp && !gezeigt){ pop(duEl, "+" + (sp.lp - vorher.dlp), "heil"); effekt("heilung", duEl, {plus: sp.lp - vorher.dlp}); }
      if (k.letzte_parade && vorher.phase === "parade" && k.phase !== "parade"){
        banner(URTEIL[k.letzte_parade] || k.letzte_parade, k.letzte_parade, null, 0); effekt("parade_" + k.letzte_parade, spriteEl, {});
        if (!(k.letzte_parade === "perfekt" && ST.klangRev === vorher.rev)) ton({perfekt: KLANG.perfekt, gut: "kampf_parade", ausweichen: "kampf_ausweichen"}[k.letzte_parade] || "");
        if (k.letzte_parade === "perfekt") effekt("konter", spriteEl, {});
      }
      spaeter(() => ereignisse(k, spriteEl, duEl));
      if (k.ergebnis && !vorher.ende) spaeter(() => { effekt("ende_" + k.ergebnis.art, spriteEl, {});
        if (k.ergebnis.art === "ko" && ((k.gegner || [])[k.zielgegner || 0] || {}).klasse === "maschine") effekt("funke", spriteEl, {});
        ton({ko: "kampf_sieg", aufgabe: "kampf_sieg", niederlage: "kampf_niederlage"}[k.ergebnis.art] || "", 500); });
    }
    schwungLaden(k);
    const liste = document.querySelector("#mitte .kampf .liste"), kb = document.querySelector("#mitte .kampf");
    if (kb) kb.style.setProperty("--lh", liste ? Math.round(liste.getBoundingClientRect().height) + "px" : "300px");   // Figuren über die offene Liste
    const duK = document.querySelector("#mitte .kampf .du");
    if (kb && duK) kb.style.setProperty("--duh", Math.round(duK.getBoundingClientRect().height) + "px");   // Wuerfel sitzt ueber Ducs Karte
    if (!halten) ST.letzte = {id: k.id, rev: k.revision, glp: g.lp, gfas: g.fassung, dlp: sp.lp, phase: k.phase, ende: !!k.ergebnis,
                              aus: k.gegner.filter(x => x.aus).map(x => x.instanz), gs: Object.fromEntries(k.gegner.map(x => [x.instanz, {lp: x.lp, fas: x.fassung}]))};
    if (k.phase === "parade" && !k.ergebnis && !ST.probe && ST.probeRev !== k.revision && !busy()){
      ST.probeRev = k.revision;
      setTimeout(() => paradeStarten(), 450 + (ST.wurfExtra || 0));         // nach einer Granate erst Wurf und Knall zeigen
      ST.wurfExtra = 0;
    }
  }

  // ------------------------------------------------------------------ Aktionen
  // Zielwahl wie in Final Fantasy (29.10.2026): bei mehreren stehenden Gegnern erst den Befehl, dann das Ziel (← → / 1-3 /
  // Klick, Enter). Flaechenangriffe, Granaten und alles, was nur Duc betrifft, brauchen kein Ziel.
  function brauchtZiel(k, befehl, ziel){
    if (!mehrere(k) || k.gegner.filter(x => !x.aus).length < 2) return false;
    if (befehl === "angriff") return true;
    if (befehl === "faehigkeit") return !!((k.faehigkeiten || []).find(f => f.id === ziel) || {}).zielt;
    if (befehl === "gegenstand") return !!((k.gegenstaende || []).find(x => x.id === ziel) || {}).zielt;
    return false;
  }
  function zielBestaetigen(i){
    const zw = ST.zielwahl; if (!zw) return;
    const v = stand(), k = v && v.z && v.z.kampf;
    if (i == null) i = zw.i;
    if (!k || !k.gegner[i] || k.gegner[i].aus) return;
    ST.zielwahl = null;
    zug(zw.befehl, zw.ziel, i);
  }
  function zielSchritt(d){
    const v = stand(), k = v && v.z && v.z.kampf, zw = ST.zielwahl; if (!k || !zw) return;
    const frei = k.gegner.map((x, i) => i).filter(i => !k.gegner[i].aus);
    zw.i = frei[(frei.indexOf(zw.i) + d + frei.length) % frei.length];
    zeichnen();
  }
  function zug(befehl, ziel, gegnerI){
    const v = stand(), k = v && v.z && v.z.kampf; if (!k || busy()) return;
    ST.panel = null; ST.wurfRest = null;
    if (gegnerI == null && brauchtZiel(k, befehl, ziel)){
      const i = k.zielgegner || 0;
      ST.zielwahl = {befehl, ziel, i: k.gegner[i] && !k.gegner[i].aus ? i : k.gegner.findIndex(x => !x.aus)};
      zeichnen(); return;
    }
    ST.zielwahl = null;
    const mitZiel = gegnerI != null ? {gegner: gegnerI} : {};
    const fx = window.EdenCombatEffects, effektId = befehl === "faehigkeit" && EFFEKT_ID[ziel];
    if (effektId && OPT.fx && fx && fx.cutin){                 // Spezialangriff: Zwischensequenz und Zug zugleich, Zahlen im Einschlag
      ST.cutin = true; ST.cutinZahlRev = null; zeichnen();
      const g = k.gegner[gegnerI != null ? gegnerI : (k.zielgegner || 0)] || k.gegner[0], ich = (k.duc_bilder || {}).idle || "", duc = (ich.match(/\/kampfbild\/(Duc[A-Za-z]+)\//) || [])[1] || "";
      // das Labor hat kein Schrubber-Set: im Training nimmt die Sequenz die Schlaeger-Posen
      const name = ((k.faehigkeiten || []).find(f => f.id === ziel) || {}).label || "";
      fx.cutin({effekt: effektId, name, duc: k.held ? k.held.fx_set : duc.replace(/Mop$/, "Bat"), gegner: {idle: bild(g, "idle"), hurt: bild(g, "hurt"), guard: bild(g, "guard")},
                hintergrund: v.z.hintergrund || ""})
        .then(r => { ST.cutin = false; ST.nachCutin = true; ST.zahlGezeigt = !!(r && r.gezeigt);
          if (!(typeof beschaeftigt !== "undefined" && beschaeftigt)) zeichnen(); });   // sonst zeichnet senden() gleich selbst
      senden("kampf_zug", Object.assign({befehl, ziel, revision: k.revision}, mitZiel), "…");
      return;
    }
    const zieht = befehl === "angriff" && (k.spieler.weapon || {}).kind !== "fern" && schwung(k);   // Schlag als Bildfolge, sofort im Klick
    if (zieht) ton("kampf_schwung", SCHWUNG_MS[0] + SCHWUNG_MS[1]);   // Zischen, wenn er durchzieht (Bild c)
    else if ((befehl === "angriff" && (k.spieler.weapon || {}).kind !== "fern") || befehl === "faehigkeit") ton("kampf_schwung");   // sofort im Klick, vor der Serverantwort
    senden("kampf_zug", Object.assign({befehl, ziel: ziel || null, revision: k.revision}, mitZiel), "…");
  }
  function befehl(id){
    if (id === "faehigkeit" || id === "gegenstand"){ ST.panel = ST.panel === id ? null : id; zeichnen(); return; }
    zug(id);
  }
  function paradeNeu(){ ST.probeRev = null; paradeStarten(); }

  // ------------------------------------------------------------------ Parade-Proben
  function bewerten(dt, fe){ dt = Math.abs(dt); return dt <= fe.perf / 2 ? "perfekt" : dt <= fe.gut / 2 ? "gut" : "verfehlt"; }
  function flaeche(html){
    const d = document.createElement("div"); d.className = "kampf-qte"; d.innerHTML = html; app().appendChild(d); return d;
  }
  function paradeStarten(){
    const v = stand(), k = v && v.z && v.z.kampf;
    if (!k || k.phase !== "parade" || ST.probe || busy()) return;
    const p = k.parade, rev = k.revision;
    const hf = OPT.hilfe, fe = Object.assign({}, p.fenster, {gut: Math.round(p.fenster.gut * hf), perf: Math.round(p.fenster.perf * hf)});   // Parade-Hilfe (Option)
    ST.probe = {rev, aufraeumen: () => {}};
    if (p.aufgeladen) effekt("spezial", document.querySelector("#mitte .kampf .du"), {id: "retour", effekt: EFFEKT_ID.retour, phase: "glut"});
    qteProbe(k, p, fe);
  }
  function paradeEnde(erg){
    const pr = ST.probe; if (!pr) return;
    pr.aufraeumen(); ST.probe = null;
    const kb = document.querySelector("#mitte .kampf"); if (kb) kb.classList.remove("probe");
    document.querySelectorAll(".kampf-qte").forEach(x => { x.classList.add("weg"); setTimeout(() => x.remove(), 260); });   // ausblenden: Ring und Punkt sieht man noch
    ST.bewegung = "";
    const k = stand().z.kampf, ai = angreiferI(k), g = k.gegner[ai] || k.gegner[0];
    const weiter = () => {
      ST.pose = erg === "perfekt" ? "hurt" : (k.parade && k.parade.schwer ? "heavy_attack" : "attack");
      ST.poseBis = performance.now() + 650;
      spriteSetzen(bild(g, ST.pose), erg === "perfekt" ? "treffer" : "stoss", ai);
      gegnerSchuss(k, g, k.parade, ai);                        // falls schon vor dem Schlag pariert: der Schuss faellt trotzdem
      if (erg === "perfekt" && !schwung(k, 1)){ dSetzen(k, "konter", 650, "vor"); ducSchuss(k, "konter"); }
      // Duc 01.11.2026: eigener Sprite fuer den Konter nach der perfekten Parade; seit 03.11. die Bildfolge ab dem zweiten Bild
    };
    if (erg === "perfekt" && schwungDa(k)) ST.schwungTreffer = performance.now() + HALT_MS + schwungBisTreffer(1);   // die Antwort kann vor dem Schlag kommen
    if (erg === "perfekt"){ halt(g, ai); setTimeout(weiter, HALT_MS); } else weiter();
    paradeSenden(erg, pr.rev);
  }
  // Perfekte Parade mit Gewicht (Duc 03.11.2026, Sekiro): im Moment des Drueckens Klang, heller Blitz und ein kurzer
  // Halt (Hit-Stop) - das Bild steht 120 ms still, dann erst Konter und Treffer. Werte im Rahmen von ui_stil.md 2b
  // (Rueckmeldung 100-150 ms, ein Klang je grossem Moment); bei reduzierter Bewegung nur Klang und Blitz ohne Halt.
  const HALT_MS = matchMedia("(prefers-reduced-motion: reduce)").matches ? 0 : 120;
  // Klaenge (Duc 03.11.2026, Liste der Review-Sitzung, Runde 1). kette/finte: Platzhalter, bis die Pixabay-Klaenge da sind
  // warnung: Ankuendigung der Taeuschung (Duc waehlte den Gong, Download offen: bis dahin "glocke")
  // Duc 03.11.2026 (Pixabay-Auswahl der Review-Sitzung): Gong als Warnung, Kettenklaenge 2 und 3, Finte reihum, Konter nach
  // voller Kette. nachklang: warmer Ausklang der perfekten Parade, Kandidaten im Showcase (Duc waehlt)
  const KLANG = {perfekt: "kampf_parade_perfekt", ausholen: "kampf_schwung", finte: "kampf_finte", warnung: "kampf_warnung",
                 kette: ["kampf_parade", "kampf_kette_2", "kampf_kette_3"], konter_kette: "kampf_konter_kette", nachklang: "kampf_parade_erfolg"};   // nachklang: Ducs Klang (03.11.2026)
  function halt(g, ai){
    ton(KLANG.perfekt); ST.klangRev = stand().z.kampf.revision;
    const spr = gspr(ai || 0);
    if (spr) spriteSetzen(bild(g, (stand().z.kampf.parade || {}).schwer ? "heavy_attack" : "attack"), "", ai);
    const bl = document.createElement("div"); bl.className = "kampf-blitz perle"; app().appendChild(bl); setTimeout(() => bl.remove(), 420);
    if (spr) effekt("funke", spr, {});
    if (HALT_MS){ app().classList.add("kampf-halt"); setTimeout(() => app().classList.remove("kampf-halt"), HALT_MS); }   // am #app: senden() zeichnet .kampf neu
    // nach dem Halt ein warmer, leiser Ausklang (Duc 03.11.2026: "positiv, nicht zu verspielt"); nach einer vollen Kette der Konter
    const kette = ((stand().z.kampf.parade || {}).finte || {}).art === "kette";
    ton(kette ? KLANG.konter_kette : KLANG.nachklang, HALT_MS + 80, {leise: kette ? 0.8 : 0.7});
  }
  function paradeSenden(erg, rev){ senden("kampf_parade", {ergebnis: erg, revision: rev}, "…"); }
  // Parade-Probe (Duc 03.11.2026): Baustein EdenQTE (eden-qte.js). Kein "PARRY!" mehr: der Gegner holt aus und leuchtet 1 s
  // (Perle = parieren, Blau = nur ausweichen), dann laeuft der Marker ueber eine schmale Leiste auf die Zone. Dort kommen
  // Funke und Schlag. Der Ring ist weg: Gegner, bei denen man waehlen darf, zeigen dieselbe Leiste mit breiter blauer Zone.
  const LAUF = {leicht: 1700, mittel: 1500, stark: 1250};      // ms vom Start des Markers bis zum Schlag
  function abdunkeln(d){
    d.classList.add("dunkel");
    const kb = document.querySelector("#mitte .kampf"); if (kb) kb.classList.add("probe");
  }
  function funkeUndSchlag(g, p, ai, letzter){
    const spr = gspr(ai || 0);
    if (spr) effekt("funke", spr, {});
    ST.pose = p.schwer ? "heavy_attack" : "attack"; ST.bewegung = "stoss";
    spriteSetzen(bild(g, ST.pose), "stoss", ai || 0);
    if (!letzter) return;                                      // Kette: Blitz und Schuss nur beim letzten Schlag
    gegnerSchuss(stand().z.kampf, g, p, ai);
    const bl = document.createElement("div"); bl.className = "kampf-blitz"; app().appendChild(bl); setTimeout(() => bl.remove(), 260);
    effekt("schlag", spr, {schwer: p.schwer});
  }
  // Taunt beim Zoegern (Duc 03.11.2026): Menschen sprechen eine Zeile ihrer Stimmgruppe (Text kurz ueber dem Gegner),
  // Tiere knurren nur. Daten: kaempfe.json enemies[].taunt {sfx?, zeilen?: [{id, text}]}; reihum je Runde, nie Zufall.
  function taunt(t, g, ai, runde){
    if (!t) return;
    if (t.sfx) ton(t.sfx);
    const z = (t.zeilen || [])[(runde || 0) % Math.max(1, (t.zeilen || []).length)];
    if (!z) return;
    try { new Audio("/api/zeile?id=" + encodeURIComponent(z.id)).play().catch(() => {}); } catch (_) {}
    const spr = gspr(ai || 0); if (!spr || !z.text) return;
    const r = spr.getBoundingClientRect(), box = app().getBoundingClientRect(), d = document.createElement("div");
    d.className = "kampf-taunt"; d.textContent = "“" + z.text + "”";
    d.style.left = (r.left - box.left + r.width / 2) + "px"; d.style.top = (r.top - box.top + r.height * 0.12) + "px";
    app().appendChild(d); setTimeout(() => d.remove(), 1800);
  }
  function qteArt(p){ return p.nur_ausweichen ? "ausweichen" : p.modus === "ring" ? "wahl" : "parieren"; }
  function qteProbe(k, p, fe){
    const ai = angreiferI(k), g = k.gegner[ai] || k.gegner[0], art = qteArt(p);
    const d = flaeche(`<div class="block"></div>`); abdunkeln(d);
    const spr = () => gspr(ai);
    const q = EdenQTE.start(d.querySelector(".block"), {art, lauf: LAUF[p.tempo] || LAUF.mittel, ziel: p.ziel, fenster: fe, finte: p.finte, bekannt: p.finte_bekannt, serie: p.serie, serie_max: p.serie_max, name: p.label}, {
      tell(an){
        const el = spr(); if (!el) return;
        if (an){
          ST.pose = p.schwer ? "heavy_windup" : "windup"; ST.poseBis = Infinity; ST.bewegung = "zurueck";
          spriteSetzen(bild(g, ST.pose), "zurueck", ai);
          el.classList.add("tell", art === "ausweichen" ? "tell-aus" : "tell-par");
          // Taeuschung wird angekuendigt (Duc 03.11.2026), sonst ist sie zu schwer: eigener Warnklang statt des Ausholens
          ton((p.finte || {}).art === "taeuschung" ? KLANG.warnung : KLANG.ausholen);
        } else el.classList.remove("tell", "tell-aus", "tell-par");
      },
      finte(){                                                 // Taeuschung: der Gegner zuckt, schlaegt aber nicht
        spriteSetzen(bild(g, "attack"), "stoss", ai); ton(KLANG.finte);
        setTimeout(() => { if (ST.probe) spriteSetzen(bild(g, p.schwer ? "heavy_windup" : "windup"), "zurueck", ai); }, 220);
      },
      halten(){ taunt(p.taunt, g, ai, k.runde); },
      schlag(i, letzter){ funkeUndSchlag(g, p, ai, letzter); },
      // Kettentreffer pariert: leiser Klang, je Treffer etwas hoeher (Spannung bis zum letzten Schlag)
      treffer(i){ ton(KLANG.kette[i] || KLANG.kette[KLANG.kette.length - 1], 0, {leise: 0.55, hoehe: 1 + 0.06 * i}); },
      ende(erg){ paradeEnde(erg); }
    });
    ST.probe.druck = q.druck; ST.probe.ausweichen = q.ausweichen;
    ST.probe.aufraeumen = () => q.stop();
    d.addEventListener("pointerdown", ST.probe.druck);
  }

  // ------------------------------------------------------------------ Tastatur (nur im Kampf)
  document.addEventListener("keydown", e => {
    const v = stand(), z = v && v.z; if (!z || z.status !== "kampf" || !z.kampf) return;
    if (ST.probe){
      if (e.code === "Space"){ e.preventDefault(); e.stopImmediatePropagation(); ST.probe.druck(); }
      else if ((e.key === "d" || e.key === "D") && ST.probe.ausweichen){ e.stopImmediatePropagation(); ST.probe.ausweichen(); }
      return;
    }
    const k = z.kampf;
    if (k.ergebnis && performance.now() < (ST.endeAb || 0)){ if (ST.einschlafenAb) eingeschlafen(k); ST.endeAb = 0; zeichnen(); return; }
    if (k.ergebnis || k.phase === "parade" || busy()) return;
    if (ST.zielwahl){                                             // Zielwahl (29.10.2026): ← → / 1-3 / Enter / Esc
      e.stopImmediatePropagation();
      if (e.key === "ArrowLeft" || e.key === "ArrowUp") { e.preventDefault(); zielSchritt(-1); }
      else if (e.key === "ArrowRight" || e.key === "ArrowDown" || e.key === "Tab") { e.preventDefault(); zielSchritt(1); }
      else if (e.key === "Enter" || e.code === "Space") { e.preventDefault(); zielBestaetigen(); }
      else if (e.key === "Escape") { ST.zielwahl = null; zeichnen(); }
      else { const n = parseInt(e.key, 10), frei = k.gegner.map((x, i) => i).filter(i => !k.gegner[i].aus);
        if (n && frei[n - 1] != null) zielBestaetigen(frei[n - 1]); }
      return;
    }
    if (e.key === "Escape" && ST.panel){ e.stopImmediatePropagation(); ST.panel = null; zeichnen(); return; }
    const n = parseInt(e.key, 10); if (!n) return;
    e.stopImmediatePropagation();
    if (ST.panel === "faehigkeit"){ const f = k.faehigkeiten[n - 1]; if (f && !f.gesperrt) zug("faehigkeit", f.id); return; }
    if (ST.panel === "gegenstand"){ const x = k.gegenstaende[n - 1]; if (x && !x.gesperrt) zug("gegenstand", x.id); return; }
    const b = (k.befehle || [])[n - 1]; if (b && !b.gesperrt) befehl(b.id);
  }, true);

  window.EdenCombat = {endeJetzt(){ const k = (stand() || {z: {}}).z.kampf; if (k && ST.einschlafenAb) eingeschlafen(k); ST.endeAb = 0; zeichnen(); }, einsetzen, musikHalten(){ const k = ((stand() || {}).z || {}).kampf; return !!(k && endeHalten(k)); }, html, nachZeichnen, zug, befehl, paradeNeu, zielBestaetigen, ausruestungHtml, werkstattHtml, upgradeHtml, chipWahl, chipSetzen, chipWeg, charmWahl, charmSetzen, charmWeg, upTab, upFilter, optionenHtml, optSetzen, EFFEKT_ID, _st: ST};
  // Kam der Stand schon vor diesem (defer-)Skript an, hat der Client ohne Plugin gezeichnet: einmal nachholen.
  const v = stand();
  if (v && v.z && typeof zeichnen === "function" && (v.z.status === "kampf" || (typeof overlay !== "undefined" && overlay === "laden"))) zeichnen();
})();
