/* Kampf-Effekte (Platzhalter, 19.10.2026) - austauschbar, siehe docs/wiki/systeme/kampf_effekte.md.
   Vertrag: window.EdenCombatEffects.play(name, anker, info). anker = DOM-Element (Gegner-Sprite oder Duc-Karte), darf null
   sein. Effekte duerfen nie Eingaben blockieren (pointer-events:none), muessen sich selbst entfernen und sollen
   prefers-reduced-motion beachten. Fehlt diese Datei oder wirft sie, laeuft der Kampf unveraendert weiter. */
(function(){
  "use strict";
  const ruhig = () => window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function ebene(){
    const app = document.getElementById("app"); if (!app) return null;
    const d = document.createElement("div");
    d.style.cssText = "position:absolute;inset:0;pointer-events:none;z-index:33;overflow:hidden";
    app.appendChild(d); return d;
  }
  // Sichtbarer Koerper (Duc 28.10.): alle Kampfbilder haben dieselbe Flaeche, die Tiere fuellen sie verschieden aus (Keiler
  // nur die untere Haelfte, schwarzer Loewe fast alles). Einmal je Bild die deckenden Pixel messen, dann zielen und skalieren
  // die Effekte auf das Tier statt auf die Bildflaeche. Bruchteile des Bildes, Cache je Bild-URL.
  const KOERPER = {};
  const KOERPER_BASIS = 200;                                 // sichtbare Tierhoehe in px, bei der die Effekte Faktor 1 haben
  function koerperAnteil(img){
    const src = (img.currentSrc || img.src || "").split("?")[0];
    if (src in KOERPER) return KOERPER[src];
    if (!img.complete || !img.naturalWidth) return null;
    let a = null;
    try {
      const w = 160, h = Math.max(1, Math.round(160 * img.naturalHeight / img.naturalWidth)), c = document.createElement("canvas");
      c.width = w; c.height = h;
      const g = c.getContext("2d", {willReadFrequently: true}); g.drawImage(img, 0, 0, w, h);
      const d = g.getImageData(0, 0, w, h).data;
      let x0 = w, y0 = h, x1 = -1, y1 = -1;
      for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) if (d[(y * w + x) * 4 + 3] > 60){
        if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
      if (x1 >= 0) a = {l: x0 / w, t: y0 / h, r: (x1 + 1) / w, b: (y1 + 1) / h};
    } catch (_){ /* fremde Quelle: Bildflaeche nehmen */ }
    return (KOERPER[src] = a);
  }
  function koerper(el){                                       // Rechteck des sichtbaren Tiers in #app-Koordinaten
    const app = document.getElementById("app").getBoundingClientRect(), r = el.getBoundingClientRect();
    const box = {x: r.left - app.left, y: r.top - app.top, w: r.width, h: r.height};
    const a = el.tagName === "IMG" ? koerperAnteil(el) : null;
    if (!a) return box;
    const s = Math.min(box.w / el.naturalWidth, box.h / el.naturalHeight), bw = el.naturalWidth * s, bh = el.naturalHeight * s;
    const ox = box.x + (box.w - bw) / 2, oy = box.y + box.h - bh;    // object-fit:contain, object-position:bottom
    return {x: ox + a.l * bw, y: oy + a.t * bh, w: (a.r - a.l) * bw, h: (a.b - a.t) * bh};
  }
  function mitte(anker, hoehe = 0.4){
    if (anker && anker.punkt) return anker.punkt;              // fester Punkt statt Element (Granaten-Einschlag)
    const app = document.getElementById("app").getBoundingClientRect();
    if (!anker) return {x: app.width / 2, y: app.height / 2};
    const r = koerper(anker);
    return {x: r.x + r.w / 2, y: r.y + r.h * hoehe};
  }
  function ring(anker, farbe, groesse, dauer){
    const e = ebene(); if (!e) return; const m = mitte(anker), d = document.createElement("div");
    d.style.cssText = `position:absolute;left:${m.x}px;top:${m.y}px;width:20px;height:20px;margin:-10px 0 0 -10px;border-radius:50%;border:4px solid ${farbe};box-shadow:0 0 24px ${farbe}`;
    e.appendChild(d);
    d.animate([{transform: "scale(.2)", opacity: 1}, {transform: `scale(${groesse})`, opacity: 0}], {duration: dauer, easing: "ease-out"}).onfinish = () => e.remove();
  }
  function hieb(anker, farbe){
    const e = ebene(); if (!e) return; const m = mitte(anker), d = document.createElement("div");
    d.style.cssText = `position:absolute;left:${m.x - 110}px;top:${m.y - 4}px;width:220px;height:8px;border-radius:var(--r-taste);background:linear-gradient(90deg,transparent,${farbe},transparent);transform:rotate(-28deg)`;
    e.appendChild(d);
    d.animate([{opacity: 0, transform: "rotate(-28deg) scaleX(.2)"}, {opacity: 1, transform: "rotate(-28deg) scaleX(1)"}, {opacity: 0, transform: "rotate(-28deg) scaleX(1.1)"}],
              {duration: 320, easing: "ease-out"}).onfinish = () => e.remove();
  }
  function rand(farbe){
    const e = ebene(); if (!e) return;
    e.style.boxShadow = `inset 0 0 120px ${farbe}`;
    e.animate([{opacity: 1}, {opacity: 0}], {duration: 450, easing: "ease-out"}).onfinish = () => e.remove();
  }
  // Granaten (27.10.2026): Rosis Granate fliegt im Bogen von Duc zum Gegner und platzt am Koerper. Einschlag (Duc 27.10. abends,
  // "richtig Animationen, vor allem beim Impact"): Hitstop -> Gegner blitzt weiss -> Kamera-Stoss -> echte EmberGen-/LiquiGen-
  // Bildfolge (fx/, werkzeuge/eden_rise/granaten_fx.py) -> Druckwelle, die den Hintergrund verzerrt -> Rueckstoss -> Nachwirkung.
  // info = {zustand, id, von (Duc-Sprite)}; WURF_MS = Splint-Vorlauf + Flug + Hitstop, der Kampfbildschirm zeigt Zahl und Treffer erst danach.
  // WURF_VOR: erst klickt der Splint, dann fliegt sie (Duc 28.10.: Klick frueher, dann erst werfen)
  const WURF_VOR = 350, FLUG_MS = 760, HALT_MS = 90, WURF_MS = WURF_VOR + FLUG_MS + HALT_MS;
  const FX = "/plugins/eden-combat/fx/";
  // freigestellte Granaten fuer den Flug (28.10.2026, werkzeuge/eden_rise/granaten_freistellen.py) - das Item-Bild hat Stoff dahinter
  const WURF_BILDER = ["grenade_fire", "grenade_water", "grenade_shock", "grenade_flash", "grenade_concussion", "grenade_shrapnel", "grenade_sleep"];
  let fx = null, fxLaeuft = null;
  function fxLaden(){                                          // Bildboegen einmal vorladen, damit der erste Knall nicht ruckelt
    if (!fxLaeuft) fxLaeuft = fetch(FX + "fx.json").then(r => r.json()).then(m => {
      fx = m; for (const n of Object.keys(m)){ const i = new Image(); i.src = FX + n + ".webp"; }
      for (const g of WURF_BILDER){ const i = new Image(); i.src = FX + "wurf_" + g + ".webp"; }
    }).catch(() => { fxLaeuft = null; });
    return fxLaeuft;
  }
  // 28.10.2026: nicht mehr beim Spielstart (7,6 MB ohne Kampf) - eden-combat.js ruft vorladen() beim Kampfbeginn
  // eine Bildfolge an Punkt p abspielen. o: breite, ms, warte, blend, filter, deck, dreh, boden (p = Fusspunkt), aus (Ausblendanteil), wachsen, ab (Anteil der Bilder vorn ueberspringen),
  // kopf (senkrecht spiegeln: die LiquiGen-Fontaene ist ein Strahl von oben, gespiegelt bricht sie aus dem Boden), flach (senkrecht stauchen: Ring liegt am Boden)
  function flip(e, name, p, o = {}){
    const m = fx && fx[name]; if (!m) return;
    const b = o.breite || m.w, h = b * m.h / m.w, d = document.createElement("div");
    d.style.cssText = `position:absolute;left:${p.x - b / 2}px;top:${p.y - (o.boden ? h * .9 : h / 2)}px;width:${b}px;height:${h}px;visibility:hidden;` +
      `background:url(${FX}${name}.webp) 0 0/${m.spalten * 100}% ${m.zeilen * 100}% no-repeat;mix-blend-mode:${o.blend || "normal"};` +
      `filter:${o.filter || "none"};transform-origin:50% ${o.boden && !o.kopf ? "90%" : "50%"}`;
    e.appendChild(d);
    const t0 = performance.now() + (o.warte || 0), ms = o.ms || 900, deck = o.deck ?? 1;
    const schritt = () => {
      if (!d.isConnected) return;
      const t = (performance.now() - t0) / ms;
      if (t >= 1){ d.remove(); return; }
      if (t >= 0){
        const f = Math.min(m.bilder - 1, Math.floor(((o.ab || 0) + t * (1 - (o.ab || 0))) * m.bilder));
        d.style.visibility = "visible";
        d.style.backgroundPosition = `${m.spalten > 1 ? f % m.spalten / (m.spalten - 1) * 100 : 0}% ${m.zeilen > 1 ? Math.floor(f / m.spalten) / (m.zeilen - 1) * 100 : 0}%`;
        d.style.opacity = deck * (o.aus ? Math.min(1, (1 - t) / o.aus) : 1);
        const w = o.wachsen ? 1 + (o.wachsen - 1) * (1 - Math.pow(1 - t, 3)) : 1;
        d.style.transform = `translateY(${-(o.steigen || 0) * t}px) rotate(${o.dreh || 0}deg) scale(${w},${(o.kopf ? -w : w) * (o.flach || 1)})`;
      }
      requestAnimationFrame(schritt);
    };
    requestAnimationFrame(schritt);
  }
  // Splitter, Glut, Gischt: Striche, die ihrer Flugbahn folgen (keine Punktwolken). g = Schwerkraft in px/s²
  function striche(e, p, {n, farbe, kern = "#fff", weite, laenge = 26, dicke = 3, g = 900, ms = 700, oben = 0, kegel = 360, richtung = 0}){
    for (let i = 0; i < n; i++){
      const w = (richtung + (Math.random() - .5) * kegel) * Math.PI / 180 - oben * Math.PI / 2 * Math.random();
      const v = weite * (.55 + Math.random() * .6) / (ms / 1000), vx = Math.cos(w) * v, vy = Math.sin(w) * v;
      const dauer = ms * (.7 + Math.random() * .5), l = laenge * (.6 + Math.random() * .8), d = document.createElement("div");
      d.style.cssText = `position:absolute;left:${p.x}px;top:${p.y}px;width:${l}px;height:${dicke}px;margin:${-dicke / 2}px 0 0 ${-l}px;` +
        `border-radius:${dicke}px;background:linear-gradient(90deg,transparent,${farbe} 55%,${kern});box-shadow:0 0 8px ${farbe};transform-origin:100% 50%`;
      e.appendChild(d);
      d.animate([0, .2, .4, .6, .8, 1].map(t => {
        const s = t * dauer / 1000, x = vx * s, y = vy * s + g * s * s / 2, r = Math.atan2(vy + g * s, vx) * 180 / Math.PI;
        return {transform: `translate(${x}px,${y}px) rotate(${r}deg) scaleX(${1 - t * .5})`, opacity: t < .7 ? 1 : (1 - t) / .3, offset: t};
      }), {duration: dauer, easing: "linear", fill: "forwards"});
    }
  }
  // Druckwelle: ein Ring, durch den der Hintergrund verschwimmt und aufhellt
  function welle(e, p, groesse, ms, farbe){
    const d = document.createElement("div");
    d.style.cssText = `position:absolute;left:${p.x - 50}px;top:${p.y - 50}px;width:100px;height:100px;border-radius:50%;` +
      `backdrop-filter:blur(5px) brightness(1.35);-webkit-backdrop-filter:blur(5px) brightness(1.35);` +
      `-webkit-mask:radial-gradient(circle,transparent 52%,#000 62%,#000 68%,transparent 76%);mask:radial-gradient(circle,transparent 52%,#000 62%,#000 68%,transparent 76%);` +
      `box-shadow:0 0 0 2px ${farbe || "rgba(255,255,255,.18)"} inset`;
    e.appendChild(d);
    d.animate([{transform: "scale(.15)", opacity: 1}, {transform: `scale(${groesse / 100})`, opacity: 0}], {duration: ms, easing: "cubic-bezier(.15,.75,.35,1)", fill: "forwards"});
  }
  function blende(e, farbe, staerke, ms, z){                  // Vollbild-Blitz in der Farbe des Elements
    const d = document.createElement("div");
    d.style.cssText = `position:absolute;inset:0;background:${farbe};mix-blend-mode:screen;z-index:${z || 0}`;
    e.appendChild(d);
    d.animate([{opacity: staerke}, {opacity: 0}], {duration: ms, easing: "cubic-bezier(.1,.8,.3,1)", fill: "forwards"});
  }
  function fleck(e, boden, farbe, breite, ms, blend){         // Brandfleck / Naesse am Boden unter dem Gegner
    const d = document.createElement("div");
    d.style.cssText = `position:absolute;left:${boden.x - breite / 2}px;top:${boden.y - breite * .1}px;width:${breite}px;height:${breite * .2}px;` +
      `border-radius:50%;background:radial-gradient(ellipse,${farbe},transparent 70%);mix-blend-mode:${blend || "multiply"}`;
    e.appendChild(d);
    d.animate([{opacity: 0}, {opacity: 1, offset: .08}, {opacity: 1, offset: .5}, {opacity: 0}], {duration: ms, fill: "forwards"});
  }
  function kamera(p, staerke, ms, extra){                      // Zoom-Stoss zum Einschlag hin, dann abklingendes Wackeln
    const app = document.getElementById("app"); if (!app) return;
    const o = `${p.x}px ${p.y}px`, s = staerke;
    app.animate([0, 1, -.8, .6, -.4, .2, 0].map((x, i) => ({transformOrigin: o, offset: i / 6,
      transform: `translate(${x * 10 * s}px,${-x * 6 * s}px) scale(${1 + (i === 1 ? .06 : i === 2 ? .03 : i === 3 ? .015 : 0) * s})`,
      ...(extra ? {filter: i === 1 ? extra : "none"} : {})})), {duration: ms, easing: "ease-out"});
  }
  function getroffen(el, rueck, ms){                           // Gegner blitzt weiss auf und wird zurueckgestossen
    if (!el || !el.animate) return;
    el.animate([{filter: "brightness(1)"}, {filter: "brightness(3.2) saturate(0)", offset: .1}, {filter: "brightness(1.6) saturate(.6)", offset: .3},
                {filter: "brightness(1)"}], {duration: 300});
    el.animate([{transform: "translate(0,0)"}, {transform: `translate(${rueck}px,-4px) rotate(${rueck / 10}deg)`, offset: .16},
                {transform: `translate(${rueck * .3}px,0) rotate(0deg)`, offset: .55}, {transform: "translate(0,0)"}],
               {duration: ms, easing: "cubic-bezier(.2,.8,.3,1)", composite: "add"});
  }
  function wolke(e, b, k){                                     // weiche blaue Rauchballen statt Bildfolge (deren Kanten sahen zerrissen aus): erst flach am Boden, dann steigt die Wolke und bleibt stehen
    for (let i = 0; i < 30; i++){
      const boden = i < 12, g = Math.min(1.25, Math.max(1, k)), r = (boden ? 150 + Math.random() * 90 : 100 + Math.random() * 120) * g;   // nicht an k allein: Die liegende Pose ist flach, die Wolke soll trotzdem das ganze Tier verhuellen
      const dx = (Math.random() - .5) * (boden ? 640 : 420) * g, dy = -(boden ? Math.random() * 40 : 40 + Math.random() * 240) * g, hell = Math.random() < .35;
      const d = document.createElement("div");
      d.style.cssText = `position:absolute;left:${b.x - r}px;top:${b.y - 30 - r}px;width:${2 * r}px;height:${2 * r}px;border-radius:50%;opacity:0;filter:blur(14px);` +
        `background:radial-gradient(circle,${hell ? "rgba(178,208,250,.4)" : "rgba(96,148,235,.4)"},${hell ? "rgba(130,175,240,.18)" : "rgba(70,115,215,.2)"} 48%,transparent 72%)`;
      e.appendChild(d);
      const flach = boden ? " scaleY(.5)" : "";
      d.animate([{transform: `translate(0,0) scale(.4)${flach}`, opacity: 0}, {opacity: .9, offset: .16},
                 {transform: `translate(${dx}px,${dy}px) scale(1.5)${flach}`, opacity: .78, offset: .55},
                 {transform: `translate(${dx * 1.15}px,${dy * 1.25}px) scale(1.9)${flach}`, opacity: 0}],
                {duration: 3000 + Math.random() * 1300, delay: i * 30, easing: "ease-out", fill: "forwards"});
    }
  }
  function knall(ziel, el, zustand){
    const e = ebene(); if (!e) return;
    if (el && !el.isConnected) el = document.querySelector("#mitte .kampf .gsprite") || el;   // der Kampf hat waehrend des Flugs neu gezeichnet
    const r = el && el.getBoundingClientRect ? el.getBoundingClientRect() : null;
    // Effekte wachsen mit dem sichtbaren Tier, ohne Obergrenze (Duc 28.10.: der Loewe sah im Vollbild mickrig aus)
    const k = Math.max(.6, (el && el.getBoundingClientRect ? koerper(el).h : KOERPER_BASIS) / KOERPER_BASIS);
    const boden = el ? mitte(el, .97) : {x: ziel.x, y: ziel.y + 120 * k};
    setTimeout(() => e.remove(), zustand === "schlaf" ? 5200 : 3200);
    if (zustand === "schlaf"){                                 // Schlafgranate (Duc 01.11.2026): kein Knall, eine blaue Wolke kriecht ueber den Boden und huellt das Tier ein
      wolke(e, boden, k);
      setTimeout(() => document.dispatchEvent(new CustomEvent("eden-nebel-wirkt")), 1700);   // jetzt verhuellt sie das Tier, eden-combat.js laesst es einschlafen
      if (el && el.animate) el.animate([{filter: "none"}, {filter: "brightness(.72) saturate(.65)", offset: .5}, {filter: "brightness(.85) saturate(.8)"}], {duration: 3200});
    } else if (zustand === "brennend"){
      blende(e, "rgba(255,150,60,1)", .5, 260);
      flip(e, "flare", ziel, {breite: 420 * k, ms: 240, blend: "screen", filter: "sepia(1) saturate(4) hue-rotate(-15deg)", aus: .8});
      // Duc 28.10.: Explosion muss von unten kommen - der Luft-Feuerball zog von links nach rechts, nur noch die Bodenkuppel
      flip(e, "bodenexplosion", boden, {breite: 560 * k, ms: 1800, boden: true, aus: .35});
      welle(e, ziel, 520 * k, 520, "rgba(255,160,80,.35)");
      striche(e, ziel, {n: 18, farbe: "rgba(255,140,40,.95)", kern: "#ffe9b0", weite: 190 * k, laenge: 22, dicke: 3, g: 1100, ms: 900, oben: 1});
      flip(e, "brand", boden, {breite: 170 * k, ms: 1500, warte: 700, boden: true, blend: "screen", deck: .7, aus: .35});
      fleck(e, boden, "rgba(25,12,6,.7)", 230 * k, 2800);
      kamera(ziel, 1, 460); getroffen(el, 30, 620);
    } else if (zustand === "nass"){
      blende(e, "rgba(110,180,255,1)", .35, 240);
      // Ducs LiquiGen-Wasserball 28.10.: platzt am Boden und breitet sich als Kuppel aus (vorher Fontaene aus dem Boden)
      flip(e, "wasserball", boden, {breite: 900 * k, ms: 1500, boden: true, deck: .85, filter: "brightness(1.15)", aus: .35});
      welle(e, ziel, 480 * k, 480, "rgba(150,200,255,.4)");
      welle(e, ziel, 300 * k, 380);
      striche(e, ziel, {n: 24, farbe: "rgba(170,215,255,.9)", kern: "#f2faff", weite: 210 * k, laenge: 30, dicke: 2.5, g: 1500, ms: 850, oben: 1.2});
      fleck(e, boden, "rgba(120,190,255,.35)", 260 * k, 2600, "screen");
      kamera(ziel, .6, 400); getroffen(el, 22, 560);
    } else if (zustand === "strom"){
      const fl = document.createElement("div");
      fl.style.cssText = "position:absolute;inset:0;background:#f4f0c8;mix-blend-mode:screen";
      e.appendChild(fl);
      fl.animate([.55, 0, .4, 0, .3, 0, .15, 0].map(o => ({opacity: o})), {duration: 520, fill: "forwards"});
      for (const [w, ms] of [[-55, 0], [15, 70], [75, 140], [-120, 200]])
        flip(e, "strom", ziel, {breite: 260 * k, ms: 620, warte: ms, dreh: w, blend: "screen", filter: "hue-rotate(-25deg) brightness(1.3)", aus: .4});
      flip(e, "flare", ziel, {breite: 320 * k, ms: 300, blend: "screen", filter: "sepia(1) saturate(3) hue-rotate(10deg)", aus: .7});
      welle(e, ziel, 380 * k, 420, "rgba(255,240,120,.4)");
      striche(e, ziel, {n: 16, farbe: "rgba(255,235,110,.95)", weite: 150 * k, laenge: 18, dicke: 2, g: 300, ms: 420});
      if (el && el.animate) el.animate([1, 0, 1, 0, 1, 0, 1].map(v => ({filter: v ? "brightness(2.6) contrast(1.6) saturate(0)" : "brightness(.55) contrast(1.4)"})),
                                       {duration: 560, easing: "steps(7)"});
      kamera(ziel, .5, 360); getroffen(el, 16, 480);
    } else if (zustand === "geblendet"){
      flip(e, "flare", ziel, {breite: 900 * k, ms: 520, blend: "screen", aus: .6});
      const w = document.createElement("div");                // erst 0,3 s komplett weiss, dann langsam zurueck
      w.style.cssText = "position:absolute;inset:0;background:#fffdf6;z-index:40";
      e.appendChild(w);
      w.animate([{opacity: 0}, {opacity: 1, offset: .04}, {opacity: 1, offset: .2}, {opacity: .35, offset: .55}, {opacity: 0}],
                {duration: 1700, easing: "ease-out", fill: "forwards"});
      const app = document.getElementById("app");
      if (app) app.animate([{filter: "brightness(1.8) saturate(.3) blur(2px)"}, {filter: "brightness(1.3) saturate(.6) blur(1px)", offset: .5}, {filter: "none"}],
                           {duration: 2200, delay: 300, easing: "ease-out"});
      welle(e, ziel, 700 * k, 600);
      getroffen(el, 10, 420);
    } else if (zustand === "erschuettert"){
      blende(e, "rgba(255,245,225,1)", .4, 200);
      flip(e, "rauchring", ziel, {breite: 700 * k, ms: 900, deck: .85, filter: "sepia(.35) brightness(2.6)", aus: .5});   // JangaFX 28.10.
      flip(e, "rauchring", boden, {breite: 820 * k, ms: 1100, flach: .35, deck: .9, filter: "sepia(.35) brightness(2.4)", aus: .45});
      welle(e, ziel, 760 * k, 640, "rgba(230,215,190,.35)");
      setTimeout(() => welle(e, ziel, 520 * k, 520), 110);
      flip(e, "bodenexplosion", boden, {breite: 440 * k, ms: 1500, warte: 60, ab: .45, boden: true, deck: .7, wachsen: 1.2, filter: "saturate(0) sepia(.25) brightness(1.15)", aus: .5});
      striche(e, boden, {n: 14, farbe: "rgba(120,100,80,.9)", kern: "#cbb89a", weite: 170 * k, laenge: 14, dicke: 4, g: 1600, ms: 800, oben: 1, kegel: 120, richtung: -90});
      kamera(ziel, 1.8, 700, "blur(3px) saturate(.35)"); getroffen(el, 40, 760);
    } else {                                                   // blutend: Splitter
      blende(e, "rgba(255,240,220,1)", .45, 220);
      flip(e, "flare", ziel, {breite: 360 * k, ms: 220, blend: "screen", aus: .8});
      // Duc 28.10.: alter Rauchpilz bleibt, aber gedreht, damit er nach oben qualmt statt nach rechts wegzuziehen
      flip(e, "druckstoss", {x: ziel.x - 40 * k, y: ziel.y - 10 * k}, {breite: 360 * k, ms: 1200, deck: .85, dreh: -40, steigen: 60 * k, aus: .35});
      welle(e, ziel, 560 * k, 480, "rgba(255,255,255,.3)");
      striche(e, ziel, {n: 30, farbe: "rgba(205,212,222,.95)", kern: "#ffffff", weite: 330 * k, laenge: 38, dicke: 2.5, g: 250, ms: 520});
      if (r){                                                  // Schnittspuren am Gegner (auf dem sichtbaren Koerper)
        const kb = koerper(el);
        [[-24, 0], [18, 70], [-8, 140]].forEach(([w, ms], i) => {
          const s = document.createElement("div"), y = kb.y + kb.h * (.38 + i * .14), x = kb.x + kb.w * .5;
          s.style.cssText = `position:absolute;left:${x - 70 * k}px;top:${y}px;width:${140 * k}px;height:3px;border-radius:var(--r-fein);` +
            `background:linear-gradient(90deg,transparent,rgba(220,40,40,.95),transparent);transform:rotate(${w}deg) scaleX(0)`;
          e.appendChild(s);
          s.animate([{transform: `rotate(${w}deg) scaleX(0)`, opacity: 1}, {transform: `rotate(${w}deg) scaleX(1)`, opacity: 1, offset: .25}, {transform: `rotate(${w}deg) scaleX(1)`, opacity: 0}],
                    {duration: 650, delay: 90 + ms, fill: "forwards"});
        });
      }
      kamera(ziel, 1.1, 480); getroffen(el, 30, 620);
    }
  }
  function granate(anker, info){ setTimeout(() => flug(anker, info), WURF_VOR); }
  function flug(anker, info){
    const e = ebene(); if (!e) return;
    fxLaden();
    const ziel = mitte(anker, 0.6), von = info.von ? mitte(info.von, 0.45) : {x: ziel.x - 320, y: ziel.y};   // Sprites sind hoch: Koerper, nicht Luft
    const vonBoden = info.von ? mitte(info.von, .97) : {x: von.x, y: von.y + 150}, zielBoden = anker ? mitte(anker, .97) : {x: ziel.x, y: ziel.y + 150};
    const dx = ziel.x - von.x, dy = ziel.y - von.y;                // hoher Bogen (Duc 28.10.), oben nicht aus dem Bild
    const hoch = Math.max(60, Math.min(260 + Math.abs(dx) * .25, von.y + dy / 2 - 40));
    const schatten = document.createElement("div");           // Schatten am Boden zeigt, wohin sie fliegt
    schatten.style.cssText = `position:absolute;left:${vonBoden.x - 22}px;top:${vonBoden.y - 6}px;width:44px;height:12px;border-radius:50%;background:radial-gradient(ellipse,rgba(0,0,0,.55),transparent 70%)`;
    e.appendChild(schatten);
    schatten.animate([0, .5, 1].map(t => ({transform: `translate(${(zielBoden.x - vonBoden.x) * t}px,${(zielBoden.y - vonBoden.y) * t}px) scale(${1 - Math.sin(t * Math.PI) * .45})`,
      opacity: .4 + t * .5})), {duration: FLUG_MS, easing: "linear", fill: "forwards"});
    const bahn = Array.from({length: 17}, (_, i) => i / 16).map(t => ({   // Parabel: x linear, y mit Scheitel ueber der Mitte, dreht sich ueberschlagend
      transform: `translate(${dx * t}px,${dy * t - hoch * 4 * t * (1 - t)}px) rotate(${t * 900}deg) scale(${1 + Math.sin(t * Math.PI) * .3 - t * .25})`, offset: t}));
    const frei = WURF_BILDER.includes(info.id), bild = frei ? FX + "wurf_" + info.id + ".webp" : "/itembild/" + encodeURIComponent(info.id || "");
    let d = null;
    [.12, .22, .38, 1].forEach((deck, i, alle) => {            // Nachzieher = Bewegungsunschaerfe
      const img = document.createElement("img"); img.src = bild; img.alt = "";
      img.style.cssText = `position:absolute;left:${von.x}px;top:${von.y}px;width:80px;height:80px;margin:-40px;object-fit:contain;opacity:${deck};` +
        `filter:drop-shadow(0 4px 8px rgba(0,0,0,.6))${i < alle.length - 1 ? " blur(1.5px)" : ""}`;
      e.appendChild(img);
      const a = img.animate(bahn, {duration: FLUG_MS, delay: (alle.length - 1 - i) * 28, easing: "linear", fill: "forwards"});
      if (i === alle.length - 1){ d = img; a.onfinish = einschlag; } else a.onfinish = () => img.remove();
    });
    function einschlag(){                                      // Hitstop: alles haelt kurz an, die Granate glueht am Koerper
      schatten.remove();
      d.animate([{filter: "brightness(1)"}, {filter: "brightness(4)"}], {duration: HALT_MS, fill: "forwards"});
      flip(e, "flare", ziel, {breite: 140, ms: HALT_MS + 60, blend: "screen"});
      setTimeout(() => { e.remove(); knall(ziel, anker, info.zustand); }, HALT_MS);
    }
  }
  // Eingeschlafen (Duc 01.11.2026): Gruppen aus Z steigen vom Tier auf, bis der Kampf zu ist
  function zzz(){
    const e = ebene(); if (!e) return;
    const sprite = () => document.querySelector("#mitte .kampf .gsprite");
    const ein = (groesse, weg) => {
      const el = sprite(); if (!el) return;
      const r = koerper(el), z = document.createElement("span");
      z.textContent = "Z";
      z.style.cssText = `position:absolute;left:${r.x + r.w * .28}px;top:${r.y + r.h * .1}px;font:700 ${groesse}px var(--f-name);color:rgba(214,230,255,.95);text-shadow:0 2px 10px rgba(30,60,130,.9);opacity:0`;
      e.appendChild(z);
      z.animate([{transform: "translate(0,0) rotate(-8deg) scale(.6)", opacity: 0}, {opacity: 1, offset: .2},
                 {transform: `translate(${weg}px,-130px) rotate(10deg) scale(1.25)`, opacity: 0}], {duration: 2100, easing: "ease-out"}).onfinish = () => z.remove();
    };
    const runde = () => {
      if (!sprite()){ e.remove(); return; }
      [[22, 14, 0], [30, 34, 420], [40, 58, 840], [28, 24, 1500], [36, 46, 1900]].forEach(([g, w, ms]) => setTimeout(ein, ms, g, w));
      setTimeout(runde, 3400);
    };
    setTimeout(runde, 300);                                    // erst wenn das Bild der liegenden Pose geladen ist, sonst stimmt die Hoehe nicht
  }
  // Muendungsfeuer (Duc 01.11.2026): Blitz, Funken und Rauch genau am Lauf. info.x/y = Anteil am Bild (werkzeuge/muendung_messen.py), info.richtung -1 nach links, 1 nach rechts
  function muendung(anker, info){
    const e = ebene(), app = document.getElementById("app"); if (!e || !app || !anker) return;
    const r = anker.getBoundingClientRect(), a = app.getBoundingClientRect(), css = getComputedStyle(anker);
    // Die Bilder stehen mit object-fit:contain im Rahmen, der Punkt bezieht sich auf das Bild, nicht auf den Rahmen
    const nw = anker.naturalWidth || r.width, nh = anker.naturalHeight || r.height, f = css.objectFit === "contain" ? Math.min(r.width / nw, r.height / nh) : r.width / nw;
    const lage = (css.objectPosition || "50% 50%").split(" ").map(x => parseFloat(x) / 100), w = nw * f, h = nh * f, k = Math.max(.7, h / 620);
    const p = {x: r.left - a.left + (r.width - w) * lage[0] + w * info.x, y: r.top - a.top + (r.height - h) * lage[1] + h * info.y}, links = info.richtung < 0;
    setTimeout(() => e.remove(), 1400);
    flip(e, "flare", p, {breite: 300 * k, ms: 130, blend: "screen", filter: "sepia(1) saturate(4) hue-rotate(-15deg)", aus: .7});
    flip(e, "flare", {x: p.x + (links ? -46 : 46) * k, y: p.y}, {breite: 170 * k, ms: 90, blend: "screen", aus: .6});
    striche(e, p, {n: 9, farbe: "rgba(255,190,110,.95)", kern: "#fff4d8", weite: 150 * k, laenge: 20, dicke: 2, g: 200, ms: 260, kegel: 46, richtung: links ? 180 : 0});
    flip(e, "rauchring", {x: p.x + (links ? -28 : 28) * k, y: p.y}, {breite: 210 * k, ms: 1100, deck: .55, steigen: 34 * k, wachsen: 1.5, aus: .6});
    kamera(p, .3, 170);
  }
  const EFFEKTE = {
    granate, muendung,
    zzz,
    parade_perfekt: a => ring(a, "rgba(216,189,134,.95)", 9, 520),
    konter: a => hieb(a, "rgba(243,238,228,.95)"),
    parade_gut: a => ring(a, "rgba(168,213,177,.9)", 6, 420),
    parade_ausweichen: a => ring(a, "rgba(168,213,177,.7)", 5, 380),
    treffer_gegner: a => hieb(a, "rgba(217,161,152,.9)"),
    treffer_duc: () => rand("rgba(217,161,152,.55)"),
    heilung: () => rand("rgba(168,213,177,.45)"),
    fassung: a => ring(a, "rgba(157,185,214,.85)", 5, 420),
  };
  // Spezialangriff als Zwischensequenz (26.10.2026): die freigegebene Labor-Variante laeuft einmal im Vollbild
  // (eden-combat-fx.html), Duc links in seinem Look, der echte Gegner rechts. Leertaste, Esc oder Klick ueberspringt.
  // -> Promise, die nach dem Ende (oder Ueberspringen/Fehler) erfuellt wird - der Kampf wartet darauf.
  let laeuft = null;
  // Kampfklang (26.10.2026): ein AudioContext im Hauptfenster, an/aus und Lautstaerke wie die Effekte (eden-sfx).
  // ton-ablaeufe.js + ton-abspieler.js kommen aus dem Effektlabor; die Zwischensequenz meldet ihre Sequenz-Uhr (tonSync).
  const TON_BASIS = "/plugins/eden-skills/preview/";
  let tonCtx = null, tonMaster = null, tonLaden = null, tonLauf = null;
  const lesen = (k, f) => { try { return localStorage.getItem(k) ?? f; } catch { return f; } };
  function tonBereit(){                                        // im Klick aufrufen: Browser erlauben Ton erst nach einer Geste
    const lautst = Math.max(0, Math.min(1, Number(lesen("eden_sfx_volume", "0.6")) || 0));
    if (lesen("eden_sfx_enabled", "1") !== "1" || !lautst) return null;
    if (!tonCtx){
      const AC = window.AudioContext || window.webkitAudioContext; if (!AC) return null;
      tonCtx = new AC(); tonMaster = tonCtx.createGain(); tonMaster.connect(tonCtx.destination);
    }
    tonMaster.gain.value = lautst;
    if (tonCtx.state === "suspended") tonCtx.resume().catch(() => {});
    return tonCtx;
  }
  function tonSkripte(){
    if (window.EdenAttackSound && window.EDEN_ATTACK_SOUND_CUES && window.EDEN_APPROVED_ANIMATIONS) return Promise.resolve();
    if (!tonLaden) tonLaden = ["freigabe-spezialangriffe.js?v=3", "ton-ablaeufe.js?v=2", "ton-abspieler.js?v=1"].reduce((p, f) => p.then(() =>
      new Promise((ok, bad) => { const s = document.createElement("script"); s.src = TON_BASIS + f; s.onload = ok; s.onerror = bad; document.head.appendChild(s); })),
      Promise.resolve()).catch(e => { tonLaden = null; throw e; });
    return tonLaden;
  }
  function tonStop(){ if (tonLauf) try { tonLauf.handle.stop(); } catch (e) {} tonLauf = null; }
  // Schaden waehrend der Spezialattacke (27.10.2026): der Kampf reicht das Ergebnis herein, die Sequenz-Uhr loest die Zahlen
  // in den Einschlaegen aus (mehrere Einschlaege teilen den Schaden, zuletzt die Summe). Kommt das Ergebnis spaet, gleich zeigen.
  let zahlen = null, zahlBox = null;
  function cutinZahlen(z){ if (laeuft && z) zahlen = {z, plan: null, gezeigt: false}; }
  function zahl(text, art, links, oben, ms){
    if (!zahlBox) return;
    const el = document.createElement("div"); el.className = "kampf-pop kampf-cutin-zahl " + art; el.textContent = text;
    el.style.left = links; el.style.top = oben; zahlBox.appendChild(el); setTimeout(() => el.remove(), ms || 2300);
  }
  function zahlenSync(s){
    if (!zahlen || zahlen.gezeigt || !s || !s.timeline || !s.shown) return;
    const z = zahlen.z, tl = s.timeline;
    if (!zahlen.plan){
      const hits = tl.hits && tl.hits.length ? tl.hits.slice() : [(tl.launch || 0) + .38], n = z.schaden > 1 ? Math.min(hits.length, z.schaden) : 1;
      const teil = Math.floor(z.schaden / n);
      zahlen.plan = hits.slice(0, n).map((t, i) => ({t, schaden: i === n - 1 ? z.schaden - teil * (n - 1) : teil, erst: i === 0, letzt: i === n - 1}));
    }
    for (const p of zahlen.plan){
      if (p.weg || s.time < p.t) continue;
      p.weg = true;
      if (p.schaden) zahl("−" + p.schaden, "schaden " + (z.wirkung || "") + (zahlen.plan.length > 1 ? " teil" : ""), "calc(70% - 60px)", p.letzt ? "30%" : "36%");
      if (p.erst && z.krit) zahl("Critical!", "info", "calc(70% - 60px)", "24%");
      if (p.letzt){
        if (zahlen.plan.length > 1 && z.schaden) setTimeout(() => zahl("−" + z.schaden, "schaden stark", "calc(70% - 60px)", "22%"), 420);
        if (z.fassung) zahl("Composure −" + z.fassung, "fassung", "calc(70% - 60px)", "46%");
        if (z.heil) zahl("+" + z.heil, "heil", "calc(18% - 60px)", "26%");
      }
    }
    if (zahlen.plan.every(p => p.weg)) zahlen.gezeigt = true;
  }
  // pro Bild aus der Zwischensequenz: startet einmal, folgt dann der AudioContext-Uhr; driftet die Sequenz weg, neu ansetzen
  function tonSync(s){
    zahlenSync(s);
    if (!laeuft || !tonCtx || !window.EdenAttackSound || !s || !s.timeline) return;
    if (s.paused || !s.shown){ tonStop(); return; }
    const key = JSON.stringify([s.attack, s.variant, s.mode, s.timeline]);
    if (tonLauf && tonLauf.key === key && Math.abs(tonLauf.offset + (tonCtx.currentTime - tonLauf.at) * tonLauf.speed - s.time) < .13) return;
    tonStop();
    try {
      const at = tonCtx.currentTime, handle = EdenAttackSound.play({attack: s.attack, variant: s.variant, context: tonCtx, destination: tonMaster,
        startAt: at, baseUrl: new URL(TON_BASIS, location.href).href, timeline: s.timeline, mode: s.mode, offset: s.time, speed: s.speed || 1});
      tonLauf = {key, at, offset: s.time, speed: s.speed || 1, handle};
      handle.ready.catch(e => console.warn("cut-in sound:", e));
    } catch (e){ console.warn("cut-in sound:", e); }
  }
  function cutin({effekt, duc, gegner, name, hintergrund}){
    if (laeuft || !effekt || !/^[A-Za-z]+$/.test(effekt)) return Promise.resolve();
    if (tonBereit()) tonSkripte().catch(e => console.warn("cut-in sound:", e));
    // an body, nicht an #app: der Kampfbildschirm zeichnet sich waehrenddessen neu
    return new Promise(fertig => {
      const box = document.createElement("div"), frame = document.createElement("iframe"), tipp = document.createElement("div");
      const titel = document.createElement("div");
      box.className = "kampf-cutin"; tipp.className = "kampf-cutin-tipp"; tipp.textContent = "Space · skip";
      titel.className = "kampf-cutin-titel"; titel.textContent = name || "";
      frame.title = "Special attack"; frame.setAttribute("sandbox", "allow-scripts allow-same-origin");
      const q = new URLSearchParams({angriff: effekt, einmal: "1", duc: duc || ""});
      for (const p of ["idle", "hurt", "guard"]) if (gegner && gegner[p]) q.set(p, gegner[p]);
      if (hintergrund) q.set("bg", hintergrund);                 // Szenenbild statt Laborboden
      frame.src = "/plugins/eden-combat/eden-combat-fx.html?" + q;
      box.append(frame, titel, tipp); document.body.appendChild(box); zahlBox = box; zahlen = null;
      requestAnimationFrame(() => box.classList.add("an"));
      let ende = setTimeout(() => schluss(), 15000);          // Notbremse, falls das Labor nie meldet
      const schluss = () => {
        if (!laeuft) return; laeuft = null; clearTimeout(ende); tonStop();
        window.removeEventListener("message", nachricht); document.removeEventListener("keydown", taste, true);
        const gezeigt = !!(zahlen && zahlen.gezeigt); zahlen = null; zahlBox = null;
        box.classList.add("weg"); setTimeout(() => box.remove(), gezeigt ? 700 : 260); fertig({gezeigt});
      };
      const nachricht = e => {
        if (e.origin !== location.origin || e.source !== frame.contentWindow) return;
        if (e.data && e.data.type === "eden-cutin-ready"){ clearTimeout(ende); box.classList.add("bereit"); ende = setTimeout(schluss, Math.max(1, e.data.dauer) * 1000 + 150); }
        if (e.data && e.data.type === "eden-cutin-fehler"){ console.warn("cut-in:", e.data.text); schluss(); }
      };
      // Solange das Labor laedt, ueberspringt ein Klick nicht aus Versehen die ganze Sequenz (Duc 01.11.2026), Esc geht immer
      const taste = e => { if ((e.code === "Space" && box.classList.contains("bereit")) || e.key === "Escape"){ e.preventDefault(); e.stopImmediatePropagation(); schluss(); } };
      window.addEventListener("message", nachricht); document.addEventListener("keydown", taste, true);
      box.addEventListener("pointerdown", () => { if (box.classList.contains("bereit")) schluss(); });
      laeuft = schluss;
    });
  }
  // Beim Kampfbeginn einmal unsichtbar laden, damit schon die erste Zwischensequenz sofort startet; danach liegt alles im Browser-Cache.
  const vorgeladen = new Set();
  function cutinVorladen({effekt, duc, gegner}){
    if (!effekt || !duc || vorgeladen.has(duc) || laeuft) return;
    vorgeladen.add(duc);
    const frame = document.createElement("iframe");
    frame.setAttribute("sandbox", "allow-scripts allow-same-origin"); frame.setAttribute("aria-hidden", "true"); frame.tabIndex = -1;
    frame.style.cssText = "position:fixed;left:-2000px;top:0;width:640px;height:360px;visibility:hidden;pointer-events:none";
    const q = new URLSearchParams({angriff: effekt, einmal: "1", duc, vorladen: "1"});
    for (const p of ["idle", "hurt", "guard"]) if (gegner && gegner[p]) q.set(p, gegner[p]);
    const weg = () => { window.removeEventListener("message", antwort); clearTimeout(ende); frame.remove(); };
    const antwort = e => { if (e.source === frame.contentWindow && e.data && /^eden-cutin-/.test(e.data.type || "")) weg(); };
    const ende = setTimeout(weg, 30000);
    window.addEventListener("message", antwort);
    frame.src = "/plugins/eden-combat/eden-combat-fx.html?" + q;
    document.body.appendChild(frame);
  }
  // Arcangelo rescue is local to Duc and never opens the cut-in iframe.
  let heilerPromise = null;
  function heilerRettung(anker, info){
    const ctx = tonBereit();                                   // nur der kurze Rettungston, nie die Aufladung
    if (ctx) tonSkripte().then(() => EdenAttackSound.play({attack: "archangel", mode: "rescue", context: ctx, destination: tonMaster,
      variant: ((window.EDEN_APPROVED_ANIMATIONS || {}).choices || {}).archangel?.variant ?? 0,
      baseUrl: new URL(TON_BASIS, location.href).href, startAt: ctx.currentTime}).ready).catch(e => console.warn("rescue sound:", e));
    const starten = () => window.EdenHealer.playRescue(anker, {
      variant: info.variant ?? ((window.EDEN_APPROVED_ANIMATIONS || {}).choices || {}).archangel?.variant ?? 0,
      assetBase: "/plugins/eden-skills/preview/assets/heiler-v1/"
    });
    if (window.EdenHealer) return starten();
    if (!heilerPromise) heilerPromise = new Promise((ok, bad) => {
      const script = document.createElement("script");
      script.src = "/plugins/eden-skills/preview/ablaufprobe/heiler.js?v=2";
      script.onload = ok; script.onerror = bad; document.head.appendChild(script);
    }).catch(error => { heilerPromise = null; throw error; });
    return heilerPromise.then(starten).catch(() => undefined);
  }
  window.EdenCombatEffects = {
    play(name, anker, info = {}){
      if (ruhig()) return;
      if (["archangel_rettung", "arcangelo_rettung"].includes(name) ||
          (["archangel", "arcangelo"].includes(name) || info.effekt === "archangel") && info.phase === "rettung") return heilerRettung(anker, info);
      const f = EFFEKTE[name]; if (f) return f(anker, info);
    },
    namen: [...Object.keys(EFFEKTE), "arcangelo_rettung", "archangel_rettung"],
    cutin, cutinVorladen, get cutinLaeuft(){ return !!laeuft; }, tonSync, cutinZahlen, WURF_MS, WURF_VOR, vorladen: fxLaden,
  };
})();
