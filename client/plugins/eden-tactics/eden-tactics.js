/* Taktik-Karte der Belagerung (Duc 31.10.2026, E-102). Nur Darstellung, Regeln kommen vom Server (z.taktik, kern/taktik.py).
   Aktionen ueber senden('taktik', {was, ...}): aufstellen, start, szene, szene_alle, bewegen, zurueck, angreifen, warten, runde, neustart, white, schliessen.
   Stil: docs/wiki/systeme/ui_stil.md. Figuren und Plaetze sind eckig und lassen sich ziehen (Duc 31.10.2026), Polish kommt spaeter. */
(function(){
  "use strict";
  const LAUF_MS = 500;
  const KAM = {zoom: null, x: null, y: null, alt: null, pan: null};   // Kamera: Standard ist der ganze Ausschnitt der Welle (zoom null), hineinzoomen geht weiter (Duc 02.11.2026)
  const ROLLE = {schnell: "Fast: beats Ranged", fern: "Ranged: beats Heavy", schwer: "Heavy: beats Fast"};
  const ST = {sel: null, ziel: null, modus: null, hilfe: null, gefahr: false, gelaende: false, cutin: 0, anim: null, tempo: 1, weiter: false, pos: {}, lauf: {}, blick: {}, bannerAus: null};
  const ZUG = {id: null, hilfe: false, x0: 0, y0: 0, aktiv: false, geist: null, feld: null};
  let klickSperre = false;
  const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
  const busy = () => (typeof beschaeftigt !== "undefined" && beschaeftigt);
  const neu = () => { if (typeof zeichnen === "function") zeichnen(); };
  const ART = {stumpf: "Blunt", klinge: "Blade", stange: "Polearm", fern: "Ranged", taser: "Taser"};
  const GUT = {stumpf: "robots", klinge: "people, animals", stange: "reach", fern: "flyers", taser: "stops people, animals"};

  function aktion(was, extra){ if (!busy()) senden("taktik", Object.assign({was}, extra || {}), "…"); }
  const t = () => (typeof V !== "undefined" && V && V.z && V.z.taktik) || null;
  const einheit = (s, id) => s.einheiten.find(e => e.id === id);
  const kuerzel = n => n.replace(/^Mr\. /, "").slice(0, 2);
  const gesicht = url => `<i class="tk-gesicht" style="${url ? `background-image:url('${esc(url)}');${String(url).startsWith("/sprite/") ? ausschnittStil(ausschnittFuer(url)) : ""}` : ""}"></i>`;
  const pos = (s, x, y) => `left:${x * 100 / s.spalten}%;top:${y * 100 / s.zeilen}%;width:${100 / s.spalten}%;height:${100 / s.zeilen}%`;

  const basis = () => Math.min(innerWidth, innerHeight * 1.5);
  const planRand = s => s.phase === "aufstellen" ? 376 : 0;   // Der Schlachtplan liegt links
  function kamFit(s){
    const a = s.ausschnitt;
    return Math.min((innerWidth - planRand(s)) / (a[2] - a[0] + 1), innerHeight / (a[3] - a[1] + 1)) * s.spalten / basis();
  }
  const kamZoom = s => s.phase === "aufstellen" || s.phase === "bestand" || !KAM.zoom ? kamFit(s) : Math.max(kamFit(s), KAM.zoom);
  // Passt der Ausschnitt ins Fenster, steht er in der Mitte, sonst darf die Kamera nicht aus ihm heraus
  function kamAchse(von, bis, c, rand, platz, kam){
    const l = von * c, r = (bis + 1) * c;
    return r - l <= platz ? rand + (platz - (r - l)) / 2 - l : Math.min(rand - l, Math.max(rand + platz - r, kam));
  }
  function kamLage(s){
    const b = basis() * kamZoom(s), c = b / s.spalten, a = s.ausschnitt, rand = planRand(s);
    const x = kamAchse(a[0], a[2], c, rand, innerWidth - rand, KAM.x || 0), y = kamAchse(a[1], a[3], c, 0, innerHeight, KAM.y || 0);
    KAM.x = x; KAM.y = y;
    return {b, x, y};
  }
  const kamStil = s => { const l = kamLage(s); return `width:${l.b}px;left:${l.x}px;top:${l.y}px;`; };
  function kamSetzen(s){
    const w = document.querySelector(".tk-feldwelt");
    if (!w) return;
    const l = kamLage(s);
    w.style.width = l.b + "px"; w.style.left = l.x + "px"; w.style.top = l.y + "px";
  }
  function kamAuf(s, x, y){
    const b = basis() * kamZoom(s), c = b / s.spalten;
    KAM.x = innerWidth / 2 - (x + .5) * c;
    KAM.y = innerHeight / 2 - (y + .5) * c;
  }
  // Nur nachziehen, wenn die Figur nah am Rand oder draussen steht, sonst springt das Bild bei jedem Klick
  function kamBlick(s, e){
    const l = kamLage(s), c = l.b / s.spalten, px = l.x + (e.x + .5) * c, py = l.y + (e.y + .5) * c;
    if (px < innerWidth * .2 || px > innerWidth * .8 || py < innerHeight * .2 || py > innerHeight * .75) kamAuf(s, e.x, e.y);
  }
  function kamZurueck(){
    if (!KAM.alt) return;
    KAM.zoom = KAM.alt.zoom; KAM.x = KAM.alt.x; KAM.y = KAM.alt.y; KAM.alt = null;
    ST.weiter = true;
    neu();
  }
  function ganzeKarte(){
    const s = t();
    if (!s) return;
    KAM.zoom = KAM.zoom ? null : kamFit(s) * 1.5;
    const e = ST.sel && einheit(s, ST.sel);
    if (e) kamAuf(s, e.x, e.y); else if (KAM.zoom) kamAuf(s, 25, 15);
    neu();
  }
  // Das Briefing zeigt, wovon gerade die Rede ist: Die Kamera faehrt hin, ohne Ziel wieder auf den ganzen Ausschnitt (Duc 02.11.2026)
  function kamSzene(s){
    const key = s.szene ? (s.szene_id || "") + "|" + s.szene_rest : null;
    if (key === KAM.szene) return;
    KAM.szene = key;
    const zu = s.szene && s.szene.zu;
    if (!zu && !KAM.szeneZoom) return;
    const von = kamLage(s);
    KAM.szeneZoom = !!zu;
    KAM.zoom = zu ? kamFit(s) * 1.4 : null;
    if (zu) kamAuf(s, zu[0], zu[1]);
    if (matchMedia("(prefers-reduced-motion:reduce)").matches) return;
    setTimeout(() => {
      const w = document.querySelector(".tk-feldwelt");
      if (!w) return;
      const l = kamLage(s), setzen = q => { w.style.width = q.b + "px"; w.style.left = q.x + "px"; w.style.top = q.y + "px"; };
      w.style.transition = "none";
      setzen(von);
      void w.offsetWidth;
      w.style.transition = "left .7s ease,top .7s ease,width .7s ease";
      setzen(l);
      setTimeout(() => { w.style.transition = ""; }, 760);
    }, 0);
  }
  function panStart(ev){
    if (ev.button === 0 || ev.button === 1) KAM.pan = {x0: ev.clientX, y0: ev.clientY, kx: KAM.x, ky: KAM.y, aktiv: false};
  }
  document.addEventListener("wheel", ev => {
    const s = t();
    if (!s || !document.querySelector(".tk-feldwelt") || s.phase === "aufstellen") return;
    ev.preventDefault();
    const l = kamLage(s), wx = (ev.clientX - l.x) / l.b, wy = (ev.clientY - l.y) / (l.b * 2 / 3);
    const fit = kamFit(s), soll = kamZoom(s) * (ev.deltaY < 0 ? 1.15 : 1 / 1.15);
    KAM.zoom = soll <= fit * 1.01 ? null : Math.min(3, soll);
    const nb = basis() * kamZoom(s);
    KAM.x = ev.clientX - wx * nb; KAM.y = ev.clientY - wy * (nb * 2 / 3);
    kamSetzen(s);
  }, {passive: false});
  addEventListener("resize", () => { if (t() && document.querySelector(".tk-feldwelt")) neu(); });

  // Pixel-Figur als Bildstreifen: Beim Stehen atmet sie (stand), beim Ziehen laeuft sie (figur)
  function sprite(e, laeuft, verzug){
    const f = laeuft || !e.figur.stand ? e.figur : e.figur.stand;
    const anim = laeuft === "dauernd" ? `animation:tk-schritte .9s steps(${f.bilder - 1}) infinite;` : laeuft ? `animation:tk-schritte ${LAUF_MS}ms steps(${f.bilder - 1}) 1;animation-delay:-${verzug}ms;` : `animation:tk-schritte 1.4s steps(${f.bilder - 1}) infinite alternate;`;
    return `<span class="tk-sprite ${ST.blick[e.id] === "rechts" ? "rechts" : ""}" style="background-image:url('/taktikbild/${esc(f.bild)}');background-size:${f.bilder * 100}% 100%;height:${f.hoehe}%;aspect-ratio:${f.seite};${anim}"></span>`;
  }
  // Hat sich die Figur bewegt, gleitet sie vom alten Feld herueber. Mehrfaches Zeichnen setzt das Gleiten nicht zurueck.
  function gleiten(e){
    const alt = ST.pos[e.id], jetzt = performance.now();
    ST.pos[e.id] = [e.x, e.y];
    if (alt && (alt[0] !== e.x || alt[1] !== e.y)){
      ST.lauf[e.id] = {dx: (alt[0] - e.x) * 100, dy: (alt[1] - e.y) * 100, ab: jetzt};
      if (alt[0] !== e.x) ST.blick[e.id] = e.x > alt[0] ? "rechts" : "links";
      setTimeout(() => { if (!ZUG.aktiv) neu(); }, LAUF_MS + 30);   // angekommen: wieder die Stand-Bilder
    }
    const l = ST.lauf[e.id];
    if (!l) return null;
    const verzug = Math.round(jetzt - l.ab);
    if (verzug >= LAUF_MS){ delete ST.lauf[e.id]; return null; }
    return {stil: `--dx:${l.dx}%;--dy:${l.dy}%;animation:tk-lauf ${LAUF_MS}ms ease-in-out;animation-delay:-${verzug}ms;`, verzug};
  }

  function figur(s, e){
    const ziel = ST.hilfe ? (s.hilfe.find(h => h.id === ST.hilfe)?.ziele || []).includes(e.id) : ST.modus === "angriff" && ST.sel && (einheit(s, ST.sel)?.ziele || []).some(g => g.id === e.id);
    const kl = ["tk-fig", e.seite, e.boss ? "boss" : "", e.fest ? "fest" : "", e.fertig ? "fertig" : "", ST.sel === e.id ? "wahl" : "", ziel ? "ziel" : "", ZUG.aktiv && !ZUG.hilfe && ZUG.id === e.id ? "zieht" : "", e.haelt ? "haelt" : "", e.getarnt ? "getarnt" : "", e.figur ? "hat-figur" : ""].join(" ");
    const lauf = gleiten(e);
    const lp = e.id === "duc" ? s.duc_lp / Math.max(1, s.duc_lp_max) : e.lp_max ? e.lp / e.lp_max : 1;
    return `<button type="button" class="${kl}" data-id="${e.id}" style="${pos(s, e.x, e.y)};${e.figur ? `z-index:${e.y + 5};` : ""}${lauf ? lauf.stil : ""}" onpointerenter="EdenTactics.ueber('${e.id}')" onpointerleave="EdenTactics.ueber(null)" onpointerdown="EdenTactics.greifen(event,'${e.id}')" onclick="event.stopPropagation();EdenTactics.fig('${e.id}')">
      <span class="tk-marke">${e.figur ? "" : esc(kuerzel(e.name))}</span>${e.figur ? sprite(e, !!lauf, lauf ? lauf.verzug : 0) : ""}${e.id === "duc" && s.duc_waffe ? `<i class="tk-waffe" style="background-image:url('/itembild/${esc(s.duc_waffe.id)}')"></i>` : ""}${e.boss ? "" : `<i class="tk-lp"><b style="width:${Math.round(lp * 100)}%"></b></i>`}${e.seite === "blau" && e.macht ? `<i class="tk-macht ${e.macht >= 100 ? "voll" : ""}"><b style="width:${e.macht}%"></b></i>` : ""}</button>`;
  }

  function felder(s){
    const a = s.ausschnitt, zu = (x, y, b, ho) => b > 0 && ho > 0 ? `<i class="tk-aussen" style="left:${x * 100 / s.spalten}%;top:${y * 100 / s.zeilen}%;width:${b * 100 / s.spalten}%;height:${ho * 100 / s.zeilen}%"></i>` : "";
    let h = zu(0, 0, s.spalten, a[1]) + zu(0, a[3] + 1, s.spalten, s.zeilen - a[3] - 1) + zu(0, a[1], a[0], a[3] - a[1] + 1) + zu(a[2] + 1, a[1], s.spalten - a[2] - 1, a[3] - a[1] + 1);   // Was diese Welle nicht braucht, ist abgedunkelt
    if (ST.gelaende) s.raster.forEach((z, y) => { for (let x = 0; x < z.length; x++) if ("WBST".includes(z[x])) h += `<i class="tk-feld boden-${z[x]}" style="${pos(s, x, y)}"></i>`; });
    if (s.phase === "spieler"){
      const f = einheit(s, ST.sel);
      const quellen = f && f.gefahr ? [f] : ST.gefahr ? s.einheiten.filter(u => u.gefahr) : [];
      const seen = new Set();
      for (const u of quellen) for (const [x, y] of u.gefahr){
        const k = x + "," + y;
        if (!seen.has(k)){ seen.add(k); h += `<i class="tk-feld gefahr" style="${pos(s, x, y)}"></i>`; }
      }
    }
    if (s.phase === "aufstellen"){
      const fronten = {};
      for (const p of s.plaetze){
        h += `<i class="tk-platz ${ST.sel ? "offen" : ""}" style="${pos(s, p.x, p.y)}"></i>`;
        if (!fronten[p.front]){
          fronten[p.front] = 1;
          h += `<span class="tk-front glas" style="left:${p.x * 100 / s.spalten}%;top:${p.y * 100 / s.zeilen}%">${esc(p.front)}</span>`;
        }
      }
    }
    const e = ST.sel && einheit(s, ST.sel);
    if (s.phase === "spieler" && e && e.felder && !ST.modus){
      // Wie Fire Emblem: helle Felder sind Bewegung, rote zeigen, wohin der Trupp von dort aus noch schlagen kann
      const lauf = new Set(e.felder.map(f => f[0] + "," + f[1])), rand = new Set();
      for (const [x, y] of e.felder) for (let dx = -e.reichweite; dx <= e.reichweite; dx++) for (let dy = -(e.reichweite - Math.abs(dx)); dy <= e.reichweite - Math.abs(dx); dy++){
        const k = (x + dx) + "," + (y + dy);
        if ((dx || dy) && x + dx >= 0 && y + dy >= 0 && x + dx < s.spalten && y + dy < s.zeilen && !lauf.has(k)) rand.add(k);
      }
      for (const k of rand){ const [x, y] = k.split(",").map(Number); h += `<i class="tk-feld reich" style="${pos(s, x, y)}"></i>`; }
      for (const [x, y] of e.felder) h += `<i class="tk-feld geh" style="${pos(s, x, y)}"></i>`;
    }
    if (s.phase === "spieler" && e && ST.modus === "angriff") for (const [x, y] of e.reich || []) h += `<i class="tk-feld reich stark" style="${pos(s, x, y)}"></i>`;
    for (const p of s.spaeter || []) h += `<i class="tk-feld spaeter" style="${pos(s, p.x, p.y)}"></i>`;
    for (const [x, y] of s.tueren) h += `<i class="tk-feld tuer" style="${pos(s, x, y)}"></i>`;
    if (!s.barrikade_bild) for (const [x, y] of s.barrikade) h += `<i class="tk-feld barr" style="${pos(s, x, y)}"></i>`;
    return h;
  }

  function absichten(s){
    if (s.phase !== "spieler") return "";
    const nach = {};
    return s.absichten.map(a => {
      const e = einheit(s, a.von);
      if (!e) return "";
      const x1 = (a.von_x + .5) * 100 / s.spalten, y1 = (a.von_y + .5) * 100 / s.zeilen, x2 = (a.x + .5) * 100 / s.spalten, y2 = (a.y + .5) * 100 / s.zeilen;
      nach[a.von] = 1;
      return `<line x1="${x1}" y1="${y1 * 2 / 3}" x2="${x2}" y2="${y2 * 2 / 3}" class="${a.art} ${a.trifft ? "trifft" : ""}"/>`;
    }).join("");
  }
  // Die Barrikade im Norden liegt als Bild auf der Karte, offen nach dem Verrat (Duc 02.11.2026)
  function barrBild(s){
    const b = s.barrikade_bild;
    if (!b) return "";
    const [x0, y0, x1, y1] = b.box;
    return `<img class="tk-barrbild" alt="" src="/taktikbild/${esc(b.datei)}" style="left:${x0 * 100 / s.spalten}%;top:${y0 * 100 / s.zeilen}%;width:${(x1 - x0) * 100 / s.spalten}%;height:${(y1 - y0) * 100 / s.zeilen}%">`;
  }
  // Stimme: Jede gesprochene Zeile hat eine feste Kennung und ist vorab vertont, wie bei den Events (Duc 02.11.2026)
  function sprich(s){
    const zeile = s.phase === "szene" && s.szene ? [s.szene_id, s.szene_rest, s.szene.text].join("|") : null;
    if (zeile !== ST.tonZeile){ ST.tonZeile = zeile; if (zeile && s.szene.ton) ton(s.szene.ton); }   // Ton an der Zeile (Drehbuch Finale)
    const zid = s.phase === "szene" && s.szene && s.szene.zid || null;
    if (zid === ST.gesprochen) return;
    ST.gesprochen = zid;
    if (ST.audio){ ST.audio.pause(); ST.audio = null; }
    if (!zid || typeof STIMME === "undefined" || !STIMME) return;
    const a = new Audio("/api/zeile?id=" + encodeURIComponent(zid));
    ST.audio = typeof mitTempo === "function" ? mitTempo(a) : a;
    ST.audio.play().catch(() => {});
  }
  // Vor der Welle: Wer kommt und wo. Im Briefing leuchtet, wovon die Rede ist, die Zahl sind die Runden bis zur Landung
  function geister(s){
    const zeigt = (s.szene && s.szene.zeigt) || [];
    return (s.feind_start || []).map(f => `<button type="button" class="tk-fig schwarz geist ${f.figur ? "hat-figur" : ""} ${zeigt.includes(f.typ) ? "zeigt" : ""}" style="${pos(s, f.x, f.y)};z-index:${f.y + 5};" onpointerenter="EdenTactics.ueber('${f.id}')" onpointerleave="EdenTactics.ueber(null)" onclick="event.stopPropagation()">
      <span class="tk-marke">${f.figur ? "" : esc(kuerzel(f.name))}</span>${f.figur ? sprite(f) : ""}${f.in ? `<b class="tk-geist-in zahl">${f.in}</b>` : ""}</button>`).join("");
  }
  // Brennende Haeuser und ankommende Boote stehen sichtbar auf der Karte
  function ziele_karte(s){
    if (s.phase !== "spieler") return "";
    const haus = s.haeuser.map(h => `<span class="tk-haus ${h.status}" style="${pos(s, h.x, h.y)}" title="${esc(h.name)}">${h.status === "brennt" ? `${uiIc("burn", "imtext")}<b class="zahl">${h.lunte}</b>` : h.status === "gerettet" ? uiIc("done", "imtext") : "–"}</span>`).join("");
    const boote = (s.barrikaden || []).map(b => `<span class="tk-haus ${b.kaputt ? "brennt" : "gerettet"}" style="${pos(s, b.x, b.y)}" title="${esc(b.name)}${b.kaputt ? " is broken" : " holds"}">${uiIc("guard", "imtext")}</span>`).join("") + s.ankunft.map(a => `<i class="tk-feld ankunft" style="${pos(s, a.x, a.y)}"><b class="zahl">${a.in}</b></i>`).join("");
    return haus + boote;
  }
  // Genauer Schaden je Ziel, das in diesem Gegnerzug getroffen wird
  function treffer(s){
    if (s.phase !== "spieler") return "";
    const je = {};
    for (const a of s.absichten) if (a.trifft) (je[a.an] = je[a.an] || {x: a.x, y: a.y, n: 0}).n += a.schaden;
    return Object.values(je).map(t => `<b class="tk-schaden zahl" style="${pos(s, t.x, t.y)}">-${t.n}</b>`).join("");
  }

  function kopf(s){
    const herzen = Array.from({length: s.kirche_max}, (_, i) => uiIc("guard", i < s.kirche ? "klein" : "klein leer")).join("");
    return `<div class="tk-kopf glas">
      <b class="tk-titel name">${s.art === "manoever" ? "The Manoeuvre" : s.phase === "bestand" ? "The Morning After" : s.welle ? `Wave ${s.welle} of ${s.wellen}` : "Battle Plan"}</b>${s.vorbereitung ? `<span class="tk-wert" title="${esc(s.vorbereitung.zeilen.map(z => z.text).join(" · "))}">Alon <em class="zahl">${s.vorbereitung.prozent} %</em></span>` : ""}${s.runde ? `<span>Round ${s.runde}</span>` : ""}
      <span class="tk-wert">Church ${herzen}<em class="zahl">${s.kirche}/${s.kirche_max}</em></span>
      <span class="tk-wert">Yacht <em class="zahl">${s.yacht}/${s.yacht_max}</em></span>
      <span class="tk-wert">You <em class="zahl">${s.duc_lp}/${s.duc_lp_max}</em></span>
      ${s.haeuser.length ? `<span class="tk-wert">Homes saved <em class="zahl">${s.haeuser.filter(h => h.status === "gerettet").length}/${s.haeuser.length}</em></span>` : ""}
      ${s.ankunft.length ? `<span class="tk-wert">Boats in <em class="zahl">${Math.min(...s.ankunft.map(a => a.in))}</em></span>` : ""}
      ${s.phase === "spieler" ? `<button type="button" class="knopf leise tk-klein ${ST.gefahr ? "an" : ""}" onclick="EdenTactics.schalte('gefahr')">Threat · R</button>` : ""}
      <button type="button" class="knopf leise tk-klein ${ST.gelaende ? "an" : ""}" onclick="EdenTactics.schalte('gelaende')">Terrain · T</button>
      ${s.phase === "aufstellen" ? "" : `<button type="button" class="knopf leise tk-klein ${!KAM.zoom ? "an" : ""}" onclick="EdenTactics.ganzeKarte()">Map · Z</button>
      <button type="button" class="knopf leise tk-klein ${ST.tempo > 1 ? "an" : ""}" onclick="EdenTactics.tempo()">Speed ${ST.tempo}x · F</button>`}
      <span class="tk-gelaendeinfo"></span>
    </div>`;
  }

  // Aufstellung: Seitenleiste links neben den Plaetzen, nichts verdeckt die Karte (Duc 31.10.2026)
  function zeile(k){
    return `<button type="button" class="tk-zeile ${ST.sel === k.id ? "wahl" : ""} ${k.reserve && !k.im_einsatz ? "bank" : ""}" onpointerenter="EdenTactics.info('${k.id}')" onpointerdown="EdenTactics.greifen(event,'${k.id}')" onclick="EdenTactics.fig('${k.id}')">
      ${gesicht(k.sprite)}<span class="tk-zeile-txt"><span><b class="name">${esc(k.name)}</b> <small>${esc(k.kann || "")}</small>${k.reserve ? (k.im_einsatz ? ` <small class="tk-bank" onpointerdown="event.stopPropagation()" onclick="event.stopPropagation();EdenTactics.aktion('bank',{id:'${k.id}'})">Take off the map</small>` : ` <small class="tk-reserve">Not on the map · drag to bring in</small>`) : ""}</span>
      <span class="tk-werte">${k.lp ? `<em>HP ${k.lp}</em><em>ATK ${k.angriff}</em><em>DEF ${k.abwehr}</em>` : "<em>Real fight</em>"}<em>MOV ${k.bewegung}</em>${k.reichweite > 1 ? `<em>RNG ${k.reichweite}</em>` : ""}${k.rolle ? `<em>${ROLLE[k.rolle]}</em>` : ""}${k.art ? `<em>${ART[k.art]}: ${GUT[k.art]}</em>` : ""}</span></span>
    </button>`;
  }
  function kachel(h, wie, extra){
    return `<button type="button" class="tk-kachel ${wie}" onpointerenter="EdenTactics.info('${h.id}')" ${extra || ""}>${gesicht(h.sprite)}<b>${esc(h.name)}</b></button>`;
  }
  const TAKT = {runde: "Once each round · click her in battle", welle: "Once each wave · click in battle", schlacht: "Once in the whole battle · click in battle"};
  function hilfeZeile(h, s, voll){
    const tag = h.fest ? "Always with you" : h.gewaehlt ? "Coming · click to leave her out" : voll ? "No place free" : "Click to bring along";
    const klick = h.fest || (!h.gewaehlt && voll) ? "" : `onclick="EdenTactics.hilfeWahl('${h.id}')"`;
    return `<button type="button" class="tk-zeile tk-hilfe ${h.gewaehlt ? "gewaehlt" : "bank"}" ${klick}>
      ${gesicht(h.sprite)}<span class="tk-zeile-txt"><span><b class="name">${esc(h.name)}</b> <small>${esc(h.kann)}</small> <small class="tk-reserve">${tag}</small></span>
      <span class="tk-htext">${esc(h.text)}</span><span class="tk-werte"><em>${h.takt ? TAKT[h.takt] : "Works by herself, nothing to click"}</em></span>
      ${h.nutzlos ? `<span class="tk-nutzlos">This wave: ${esc(h.nutzlos)}</span>` : ""}</span></button>`;
  }
  function plan(s){
    const wahl = s.hilfe.filter(h => h.gewaehlt), rest = s.hilfe.filter(h => !h.gewaehlt), voll = wahl.length >= s.hilfe_plaetze;
    return `<aside class="tk-plan glas">
      <div class="tk-plan-teile">
        <section><h3>Troops<small>${s.einheiten.filter(e => e.seite === "blau" && !e.fest).length} of ${s.trupps_max} this wave · Drag onto a lit square</small></h3><div class="tk-zeilen">${s.karten.filter(k => !k.fest).map(zeile).join("")}</div></section>
        <section><h3>Support<small>Not on the map. ${wahl.length} of ${s.hilfe_plaetze} coming</small></h3><div class="tk-zeilen">${wahl.concat(rest).map(h => hilfeZeile(h, s, voll)).join("")}</div></section>
        <section><h3>Village guard<small>Stay in the centre</small></h3><div class="tk-hplaetze">${s.karten.filter(k => k.fest).map(k => kachel(k, "wehr", "")).join("")}</div></section>
      </div>
      <p class="tk-detail">${ST.sel ? "Now click a square on the map. Esc cancels." : "Holm's plan is on the map. Two troops on one square swap places."}</p>
      <button type="button" class="knopf" ${busy() ? "disabled" : ""} onclick="EdenTactics.aktion('start')">Begin</button>
    </aside>`;
  }
  // Der Morgen danach (Duc 01.11.2026, kern/belagerung.py): erst die Liste, am Tag das Flicken. Selbst im Ring-Minispiel oder Petrus Trupp gegen mehr Holz.
  function kostenZeile(liste){
    return liste.map(k => `<em class="${k.hast >= k.n ? "" : "fehlt"}">${k.n} ${esc(k.label)}</em>`).join("");
  }
  function bestand(s){
    const b = s.bestand, zeilen = b.offen.map(o => `<section class="tk-bau">
        <b class="name">${esc(o.name)}</b><small>${esc(o.text)}</small>
        ${b.flicken ? `<span class="tk-werte">${kostenZeile(o.kosten)}</span>
        <span class="tk-knopfe"><button type="button" class="knopf" ${o.geht && !busy() ? "" : "disabled"} onclick="EdenTactics.flicken('${o.id}')">Mend it yourself</button>
          <button type="button" class="knopf leise" ${o.crew_geht && !busy() ? "" : "disabled"} title="${esc(o.crew.map(k => k.n + " " + k.label).join(", "))}" onclick="EdenTactics.flickenCrew('${o.id}')">Petru's crew</button></span>` : ""}
      </section>`).join("");
    return `<aside class="tk-plan glas">
      <div class="tk-plan-teile">
        <section><h3>${b.flicken ? "Mending" : "What Broke"}<small>${b.vorrat.timber} Timber · ${b.vorrat.stein} Stone</small></h3>
          <p class="tk-detail">${esc(b.holm)}</p>
          ${b.flicken ? "" : `<p class="tk-detail">The village brings ${b.notration.timber} Timber and ${b.notration.stein} Stone.</p>`}
          ${b.flicken && b.offen.length ? `<p class="tk-detail">You can do ${b.minis_frei} more yourself today. A clean job saves wood.</p>` : ""}
        </section>
        ${zeilen || `<section class="tk-bau"><b class="name">Nothing is broken</b><small>Enjoy it. Nobody will believe you.</small></section>`}
      </div>
      <button type="button" class="knopf" ${busy() ? "disabled" : ""} onclick="EdenTactics.aktion('schliessen')">${b.flicken ? "That will have to do" : "Go to work"}</button>
    </aside>`;
  }
  function hilfeLeiste(s){
    const wahl = s.hilfe.filter(h => h.gewaehlt);
    const zustand = h => h.nutzlos ? "Not this wave" : !h.takt ? "Always on" : h.bereit ? (h.takt === "runde" ? "Each round" : h.takt === "welle" ? "Each wave" : "Once") : "Used";
    return `<div class="tk-hleiste glas">${wahl.map(h => `<button type="button" class="tk-kachel ${h.nutzlos || (h.takt && !h.bereit) ? "aus" : ""} ${ST.hilfe === h.id ? "wahl" : ""}" onclick="EdenTactics.hilfeDruck('${h.id}')">
      ${gesicht(h.sprite)}<b>${esc(h.name)}</b><small>${zustand(h)}</small></button>`).join("")}</div>`;
  }

  function seite(s){
    if (s.phase === "bestand") return bestand(s);
    if (s.phase === "aufstellen"){
      return plan(s);
    }
    if (s.phase === "szene" && s.szene){
      if (s.szene.art === "titel") return `<div class="tk-titelkarte" onclick="EdenTactics.aktion('szene')"><small class="name">${esc(s.szene.ober)}</small><b class="name">${esc(s.szene.text)}</b>${s.szene.ziel ? `<p>${esc(s.szene.ziel)}</p>` : ""}
        <span class="tk-knopfe">${s.szene_rest ? `<button type="button" class="knopf leise" onclick="event.stopPropagation();EdenTactics.aktion('szene_alle')">Skip · Esc</button>` : ""}<button type="button" class="knopf">Continue · Space</button></span></div>`;
      if (s.szene.art === "wahl") return `<div class="tk-szene glas tk-wahl"><p>${esc(s.szene.text)}</p><span class="tk-wahlen">${s.szene.optionen.map((o, i) =>
        `<button type="button" class="knopf" onclick="event.stopPropagation();EdenTactics.aktion('szene_wahl', {i: ${i}})">${esc(o.text)}</button>`).join("")}</span></div>`;   // Ducs Wahl mitten in einer Szene (Drehbuch Finale)
      const links = s.szene.zu && s.szene.zu[0] < (s.ausschnitt[0] + s.ausschnitt[2]) / 2;   // Wer spricht, steht nie vor dem, wovon die Rede ist
      return `${s.szene.sprite ? `<img class="tk-redner ${links ? "rechts" : ""}" src="${esc(s.szene.sprite)}" alt="">` : ""}<div class="tk-szene glas" onclick="EdenTactics.aktion('szene')"><b class="tk-wer name">${s.szene.avatar ? `<img class="tk-avatar" src="${esc(s.szene.avatar)}" alt="">` : ""}${esc(s.szene.wer)}</b><p>${esc(s.szene.text)}</p>
        <span class="tk-knopfe">${s.szene_rest ? `<button type="button" class="knopf leise" onclick="event.stopPropagation();EdenTactics.aktion('szene_alle')">Skip · Esc</button>` : ""}<button type="button" class="knopf">Continue · Space</button></span></div>`;
    }
    if (s.phase === "white_neu") return `<div class="tk-szene glas"><p>Mr. White is still standing. Get up.</p><button type="button" class="knopf" onclick="EdenTactics.aktion('white')">Fight again</button></div>`;
    if (s.phase === "verloren") return `<div class="tk-szene glas"><b class="tk-wer name">The bay has fallen</b><p>Back to the start of this wave.</p><span class="tk-knopfe">${s.rueckspruenge > 0 ? `<button type="button" class="knopf leise" onclick="EdenTactics.rethink()">Rethink last round · ${s.rueckspruenge}</button>` : ""}<button type="button" class="knopf" onclick="EdenTactics.aktion('neustart')">Restart wave</button></span></div>`;
    if (s.phase === "gewonnen") return `<div class="tk-szene glas"><b class="tk-wer name">${s.art === "manoever" ? "Manoeuvre over" : s.welle < s.wellen ? `Wave ${s.welle} of ${s.wellen} held` : "The bay holds"}</b><p>${s.art === "manoever" ? "Two days left." : s.welle < s.wellen ? "It isn't over yet." : "The village is still here."}</p><button type="button" class="knopf" onclick="EdenTactics.aktion('schliessen')">Continue</button></div>`;
    return hilfeLeiste(s) + befehl(s);
  }

  // Aktionsmenue neben der Figur, sobald sie steht: wie in Fire Emblem erst bewegen, dann entscheiden
  function menue(s){
    const e = s.phase === "spieler" && ST.sel && !ST.hilfe && !ST.modus && einheit(s, ST.sel);
    if (!e || e.seite !== "blau" || e.fest || e.fertig || !e.gezogen || ST.lauf[e.id]) return "";
    const ziele = (e.ziele || []).length;
    const retten = (e.retten || []).map(hid => s.haeuser.find(h => h.id === hid)).filter(Boolean);
    const links = e.x > s.spalten - 9, oben = e.y > s.zeilen - 10;
    const stil = `${links ? `right:${(s.spalten - e.x) * 100 / s.spalten}%` : `left:${(e.x + 1.2) * 100 / s.spalten}%`};${oben ? `bottom:${(s.zeilen - e.y - 1) * 100 / s.zeilen}%` : `top:${e.y * 100 / s.zeilen}%`}`;
    return `<div class="tk-menue glas" style="${stil}" onclick="event.stopPropagation()" onpointerdown="event.stopPropagation()">
      <button type="button" class="knopf ${ziele ? "" : "leise"}" ${ziele ? "" : "disabled"} onclick="EdenTactics.modus('angriff')">${ziele ? "Attack" : "No enemy in reach"}</button>
      ${e.power && e.macht >= 100 ? `<button type="button" class="knopf leise" title="${esc(e.power.text)}" onclick="EdenTactics.tun('macht')">${esc(e.power.titel)}</button>` : ""}
      ${retten.map(h => `<button type="button" class="knopf ${ziele ? "leise" : ""}" onclick="EdenTactics.tunRetten('${h.id}')">Rescue · ${esc(h.name)}</button>`).join("")}
      ${(e.loeschen || []).map(hid => s.haeuser.find(h => h.id === hid)).filter(Boolean).map(h => `<button type="button" class="knopf leise" onclick="EdenTactics.tunLoeschen('${h.id}')">Water · ${esc(h.name)}</button>`).join("")}
      <button type="button" class="knopf leise" onclick="EdenTactics.tun('warten')">Wait</button>
      <button type="button" class="knopf leise" onclick="EdenTactics.tun('zurueck')">Back · Esc</button>
    </div>`;
  }

  function befehl(s){
    const h = ST.hilfe && s.hilfe.find(x => x.id === ST.hilfe);
    if (h){
      const knopf = !h.bereit ? "" : h.id === "ligeia" ? `<button type="button" class="knopf" onclick="EdenTactics.hilfeTun()">Sing</button>`
        : h.id === "siri" ? h.ziele.map(f => `<button type="button" class="knopf leise" onclick="EdenTactics.hilfeTun('${f}')">${esc(f)}</button>`).join("") : "";
      const rat = !h.bereit ? "" : h.id === "holm" || h.id === "lola" || h.id === "danzel" ? (h.ziele.length ? "<span>Click a marked troop.</span>" : "<span>No troop needs this right now.</span>") : "";
      return `<div class="tk-befehl glas"><b class="name">${esc(h.kann)}</b><span>${esc(h.text)}</span>${rat}<span class="tk-knopfe">${knopf}<button type="button" class="knopf leise" onclick="EdenTactics.hilfeDruck('${h.id}')">Close</button></span></div>`;
    }
    const e = ST.sel && einheit(s, ST.sel);
    let mitte = `<span>${s.einheiten.some(x => x.seite === "blau" && !x.fest && !x.fertig) ? "Pick a blue troop. Tab goes to the next one." : "All troops have acted. Enter ends the round."}</span>`;
    if (e && e.seite === "blau" && !e.fest && !e.fertig){
      const g = ST.modus === "angriff" && ST.ziel && (e.ziele || []).find(x => x.id === ST.ziel);
      const gn = g && einheit(s, g.id);
      mitte = `<b class="name">${esc(e.name)}</b>`;
      if (g && g.echter_kampf) mitte += `<span>You step in yourself against ${esc(gn.name)}. This opens a real fight.${g.mit ? ` ${esc(g.mit)} strikes first and hurts it.` : ""}</span>`;
      else if (g) mitte += `<span>${esc(gn.name)}: <em class="zahl">${g.schaden}</em> damage${g.mit ? ` · ${esc(g.mit)} joins in <em class="zahl">${g.mit_schaden}</em>` : ""}${g.staerke > 1 ? " · strong, no strike back" : g.staerke < 1 ? " · weak" : ""}${g.betaeubt && g.lp_danach > 0 ? " · it stops for one round" : ""}${g.lp_danach === 0 ? " · defeats it" : ` · ${g.lp_danach} HP left`}${g.zurueck ? ` · strikes back ${g.zurueck}` : ""}</span>`;
      else mitte += `<span>${ST.modus === "angriff" ? "Pick a target in the red fields." : e.gezogen ? "Choose an action." : (e.getarnt ? "Hidden in the forest. " : "") + (e.nur_ziehen ? "Hit and Run: move away, or stay and wait." : "Move to a lit field, or act from here.")}</span>`;
      // Angriff geht immer, auch ohne Bewegung: Wer schon gut steht, schlaegt einfach zu (Duc 01.11.2026)
      if (!ST.modus && !e.gezogen) mitte += `<span class="tk-knopfe"><button type="button" class="knopf ${(e.ziele || []).length ? "" : "leise"}" ${(e.ziele || []).length ? "" : "disabled"} onclick="EdenTactics.modus('angriff')">${(e.ziele || []).length ? "Attack" : "No enemy in reach"}</button><button type="button" class="knopf leise" onclick="EdenTactics.tun('warten')">Wait</button></span>`;
      if (ST.modus === "angriff") mitte += `<span class="tk-knopfe">${g ? `<button type="button" class="knopf" onclick="EdenTactics.angriff()">Attack</button>` : ""}<button type="button" class="knopf leise" onclick="EdenTactics.modus(null)">Back · Esc</button></span>`;
    } else if (e){
      mitte = `<b class="name">${esc(e.name)}</b><span>${e.seite === "blau" ? (e.fest ? "Village guard, holds this spot." : "Already acted.") : `${e.boss ? (s.white_frei ? "Only you can stop him. Attack him now." : "Nobody can touch him yet. Hold the church.") : `HP ${e.lp}/${e.lp_max} · ATK ${e.angriff} · DEF ${e.abwehr} · MOV ${e.bewegung}${e.reichweite > 1 ? ` · RNG ${e.reichweite}` : ""}. The red fields are its reach.`}`}</span>`;
    }
    const offen = s.einheiten.filter(x => x.seite === "blau" && !x.fest && !x.fertig).length;
    const zurueck = s.rethink_frei ? `<button type="button" class="knopf leise" title="Resets every move of this round. It is free until the first attack." onclick="EdenTactics.rethink()">Rethink</button>`
      : s.rueckspruenge > 0 ? `<button type="button" class="knopf leise" title="Goes back to the start of a round." onclick="EdenTactics.rethink()">Rethink · ${s.rueckspruenge}</button>` : "";
    return `<div class="tk-befehl glas">${mitte}${zurueck}<button type="button" class="knopf ${offen ? "leise" : ""}" ${busy() ? "disabled" : ""} onclick="EdenTactics.runde()">End round</button></div>`;
  }

  function schlaege(s){
    const zeilen = (s.letzter_zug || []).slice(-6).map(l => {
      const v = einheit(s, l.von), a = l.an === "kirche" ? {name: "the church"} : l.an === "yacht" ? {name: "the yacht"} : einheit(s, l.an);
      return `<li>${esc(v ? v.name : "A fallen troop")} hits ${esc(a ? a.name : "a target")} <em class="zahl">${l.schaden}</em></li>`;
    }).join("");
    const melde = s.meldung ? `<li>${esc(s.meldung)}</li>` : "";
    return (zeilen || melde) && s.phase === "spieler" ? `<ul class="tk-log glas">${melde}${zeilen}</ul>` : "";
  }

  // Der grosse Moment: einmal gross einblenden, ausserhalb der Karte, damit Neuzeichnen ihn nicht abschneidet
  // Treffer sichtbar machen: Der Angreifer stoesst vor, das Ziel zuckt, die Zahl steigt auf. Laeuft neben dem Zeichnen her.
  function trefferZeigen(s){
    if (ST.anim === null){ ST.anim = s.anim ? s.anim.n : 0; return; }   // nach dem Neuladen nichts wiederholen
    if (!s.anim || s.anim.n === ST.anim) return;
    ST.anim = s.anim.n;
    const ruhig = matchMedia("(prefers-reduced-motion:reduce)").matches;
    const log = s.anim.log.slice(0, 12), schritt = 360 / ST.tempo, vor = Object.keys(ST.lauf).length ? LAUF_MS : 0;
    const alt = ST.ton ? ST.ton.figuren : {}, leben = {};  // Stand vor den Treffern, jeder Treffer zieht davon ab
    for (const l of log){
      const f = alt[l.an], lp = l.an === "duc" ? ST.ton && ST.ton.duc_lp : f && f.lp;
      if (lp == null || leben[l.an]) continue;
      const voll = l.an === "duc" ? s.duc_lp_max : f.lp_max;
      leben[l.an] = {lp, voll};
      const balken = document.querySelector(`.tk-fig[data-id="${l.an}"] .tk-lp b`);   // Bis zum Einschlag zeigt die Leiste noch den alten Wert
      if (balken && voll) balken.style.width = Math.round(lp / voll * 100) + "%";
    }
    log.forEach((l, i) => setTimeout(() => { einTreffer(s, l, ruhig, !log.slice(i + 1).some(x => x.an === l.an)); leisteLaeuft(s, l, leben[l.an], ruhig); }, 60 + i * schritt + vor));
    if (KAM.alt) setTimeout(kamZurueck, vor + log.length * schritt + 500 / ST.tempo);
  }
  // Wie in Fire Emblem: Die Leiste laeuft beim Einschlag vom alten auf den neuen Wert, gross ueber dem Ziel und auf der Figur (Duc 01.11.2026)
  function leisteLaeuft(s, l, stand, ruhig){
    const w = document.querySelector(".tk-feldwelt"), ort = stand && ST.pos[l.an];
    if (!w || !ort || !stand.voll) return;
    const vorher = stand.lp, nachher = Math.max(0, vorher - l.schaden), proz = x => Math.round(x / stand.voll * 100);
    stand.lp = nachher;
    const r = w.getBoundingClientRect(), c = r.width / s.spalten;
    const d = document.createElement("div");
    d.className = "tk-lpzug" + (einheit(s, l.an)?.seite === "schwarz" || !einheit(s, l.an) && l.an[0] === "g" ? " feind" : "");
    d.style.left = (r.left + (ort[0] + .5) * c) + "px";
    d.style.top = (r.top + (ort[1] + 1) * c + 4) + "px";
    d.innerHTML = `<i class="rest" style="width:${proz(vorher)}%"></i><i class="voll" style="width:${proz(vorher)}%"></i><b class="zahl">${vorher}</b>`;
    document.body.appendChild(d);
    const voll = d.querySelector(".voll"), rest = d.querySelector(".rest"), zahl = d.querySelector("b");
    const zaehlen = ms => { const t0 = performance.now(); const u = setInterval(() => { const k = Math.min(1, (performance.now() - t0) / ms); zahl.textContent = Math.round(vorher + (nachher - vorher) * k); if (k >= 1) clearInterval(u); }, 30); };
    const klein = document.querySelector(`.tk-fig[data-id="${l.an}"] .tk-lp b`);
    setTimeout(() => {
      voll.style.width = proz(nachher) + "%";
      if (klein) klein.style.width = proz(nachher) + "%";
      setTimeout(() => { rest.style.width = proz(nachher) + "%"; }, ruhig ? 0 : 260);    // Der helle Rest zeigt, wie viel gerade weg war
      zaehlen(ruhig ? 1 : 420);
    }, 40);
    setTimeout(() => d.remove(), 1200);
  }
  function einTreffer(s, l, ruhig, letzter){
    const w = document.querySelector(".tk-feldwelt");
    if (!w) return;
    const r = w.getBoundingClientRect(), c = r.width / s.spalten;
    const ort = l.an === "kirche" ? s.tueren[0] : l.an === "yacht" ? [41, 15] : ST.pos[l.an];
    if (!ort) return;
    const an = document.querySelector(`.tk-fig[data-id="${l.an}"]`), von = document.querySelector(`.tk-fig[data-id="${l.von}"]`), vp = ST.pos[l.von];
    const schiesst = vp && Math.abs(ort[0] - vp[0]) + Math.abs(ort[1] - vp[1]) > 1;
    ton(trefferTon(s, l, schiesst));
    if (schiesst){                                     // aus der Ferne: ein Schuss fliegt, der Taser zuckt blau
      const x0 = r.left + (vp[0] + .5) * c, y0 = r.top + (vp[1] + .5) * c, x1 = r.left + (ort[0] + .5) * c, y1 = r.top + (ort[1] + .5) * c;
      const lang = Math.hypot(x1 - x0, y1 - y0), winkel = Math.atan2(y1 - y0, x1 - x0) * 180 / Math.PI;
      const sch = document.createElement("i");
      sch.className = "tk-schuss " + (einheit(s, l.von)?.art === "taser" ? "taser" : "");
      sch.style.cssText = `left:${x0}px;top:${y0}px;width:${lang}px;transform:rotate(${winkel}deg)`;
      document.body.appendChild(sch);
      sch.animate([{clipPath: "inset(0 100% 0 0)", opacity: 1}, {clipPath: "inset(0 0 0 0)", opacity: 1, offset: .5}, {clipPath: "inset(0 0 0 100%)", opacity: .8}], {duration: ruhig ? 1 : 240, easing: "linear"}).onfinish = () => sch.remove();
    } else if (!ruhig && von && vp){
      const n = Math.hypot(ort[0] - vp[0], ort[1] - vp[1]) || 1, schub = Math.min(1, n) * .55;
      von.animate([{transform: "none"}, {transform: `translate(${(ort[0] - vp[0]) / n * schub * 100}%,${(ort[1] - vp[1]) / n * schub * 100}%)`}, {transform: "none"}], {duration: 280, easing: "ease-out"});
    }
    if (!ruhig && an) setTimeout(() => an.animate([{transform: "none"}, {transform: "translateX(-14%)"}, {transform: "translateX(14%)"}, {transform: "none"}], {duration: 200}), 120);
    const d = document.createElement("b");
    d.className = "tk-zahl zahl " + (einheit(s, l.an)?.seite === "blau" || l.an === "kirche" || l.an === "yacht" ? "eigen" : "");
    const weg = letzter && l.an !== "kirche" && l.an !== "yacht" && !s.einheiten.some(u => u.id === l.an);   // erst der letzte Treffer wirft um
    d.textContent = "-" + l.schaden + (weg ? " KO" : "");
    if (weg) setTimeout(() => ton("tk_ko"), 140);
    d.style.left = (r.left + (ort[0] + .5) * c) + "px";
    d.style.top = (r.top + ort[1] * c) + "px";
    document.body.appendChild(d);
    setTimeout(() => d.remove(), 950);
  }
  // Toene der Karte (Duc 01.11.2026, E-114): vergleicht den neuen Stand mit dem vorigen, nur Darstellung. Was im Katalog fehlt, bleibt still.
  const ton = id => { if (id && window.EdenSfx) EdenSfx.play(id); };
  const SZENE_TON = {verrat: "tk_gitter", mochi: "tk_loewe", mochi_allein: "tk_loewe", falscher_sieg: "tk_jubel", sieg: "tk_jubel"};
  const SZENE_SCHLUSS = {mochi: "tk_rauch", sieg: "tk_glocke"};
  const HILFE_TON = {lola: "heilung", danzel: "tk_stahlplatte"};
  function trefferTon(s, l, schiesst){
    if (l.an === "kirche") return "tk_kirche";
    const v = einheit(s, l.von), art = v && v.art;
    return l.von === "maxwell" ? "tk_maxwell_schlag" : l.von === "alva" ? "tk_flinte" : l.von === "bibi" ? "tk_granate" : art === "taser" ? "tk_taser" : art === "klinge" ? "tk_klinge" : schiesst ? "gun_shot" : "kampf_treffer";
  }
  function klang(s){
    const jetzt = {phase: s.phase, welle: s.welle, runde: s.runde, szene: s.szene_id || null, rest: s.szene_rest, yacht: s.yacht, cutin: s.cutin ? s.cutin.n : 0,
      haeuser: Object.fromEntries((s.haeuser || []).map(h => [h.id, h.status])), kaputt: (s.barrikaden || []).filter(b => b.kaputt).length,
      bereit: Object.fromEntries((s.hilfe || []).map(h => [h.id, h.bereit])), duc_lp: s.duc_lp, figuren: Object.fromEntries(s.einheiten.map(e => [e.id, e]))};
    const p = ST.ton;
    ST.ton = jetzt;
    if (!p){                                           // nach dem Neuladen nichts nachholen, nur die Glocke zum Titel einer Welle
      if (/^welle_\d$/.test(jetzt.szene || "") && s.szene && s.szene.art === "titel") ton("tk_glocke");
      return;
    }
    if (jetzt.szene && (jetzt.szene !== p.szene)){
      ton(/^welle_\d$/.test(jetzt.szene) ? "tk_glocke" : /^ende_\d$/.test(jetzt.szene) ? "tk_jubel" : SZENE_TON[jetzt.szene]);
    }
    if (jetzt.szene && jetzt.rest === 0 && (jetzt.szene !== p.szene || p.rest > 0) && SZENE_SCHLUSS[jetzt.szene]) ton(SZENE_SCHLUSS[jetzt.szene]);
    if (jetzt.cutin > p.cutin) ton("tk_cutin");
    if (jetzt.kaputt > p.kaputt) ton("tk_holzbruch");
    if (jetzt.yacht === 0 && p.yacht > 0) ton("tk_yacht_sinkt");
    else if (jetzt.yacht < p.yacht) ton("tk_yacht_riss");
    for (const [id, st] of Object.entries(jetzt.haeuser)){
      if (st === "verloren" && p.haeuser[id] !== "verloren") ton("tk_haus_weg");
      if (st === "brennt" && p.haeuser[id] !== "brennt"){ ton("tk_haus_feuer"); ton("tk_haus_schreie"); }
    }
    if (p.phase === "spieler" && s.phase === "spieler")   // Ausserhalb des eigenen Zugs ist niemand bereit, das zaehlt nicht
      for (const [id, war] of Object.entries(p.bereit)) if (war && jetzt.bereit[id] === false && HILFE_TON[id]) ton(HILFE_TON[id]);
    const gleiche = jetzt.welle === p.welle;           // Beim Aufstellen einer neuen Welle laeuft niemand
    for (const e of s.einheiten){
      const a = p.figuren[e.id];
      if (!a){ if (e.typ === "drohne") ton("tk_drohne"); continue; }
      if (!gleiche || (a.x === e.x && a.y === e.y)) continue;
      if (e.typ === "roboter" || e.typ === "roboter_schwer") ton("tk_roboter");   // Kobra und Skorpion stampfen nicht
      else if (e.seite === "blau" && s.phase === "spieler" && jetzt.runde === p.runde) ton("tk_schritte");
    }
    for (const [id, a] of Object.entries(p.figuren)) if (a.typ === "drohne" && !jetzt.figuren[id]) ton("tk_drohne_ab");
    if (jetzt.runde > p.runde && s.phase === "spieler"){   // Dein Zug beginnt, wenn die Treffer des Gegners durch sind
      const n = s.anim ? Math.min(12, s.anim.log.length) : 0;
      setTimeout(() => { ton("tk_zugwechsel"); zugBand(jetzt.runde); }, n * 360 / ST.tempo + LAUF_MS + 300);
    }
  }
  function zugBand(runde){
    const d = document.createElement("div");
    d.className = "tk-cutin";
    d.innerHTML = `<span class="tk-cutin-band glas"><span><b class="name">Round ${runde}</b><em>Your Turn</em></span></span>`;
    document.body.appendChild(d);
    setTimeout(() => d.remove(), 1700);
  }
  function cutin(s){
    if (!s.cutin || s.cutin.n === ST.cutin) return "";
    const neuLaden = ST.cutin === 0;
    ST.cutin = s.cutin.n;
    if (neuLaden && s.phase !== "spieler") return "";
    const k = s.karten.find(x => x.id === s.cutin.id);
    const d = document.createElement("div");
    d.className = "tk-cutin";
    d.innerHTML = `<span class="tk-cutin-band glas">${gesicht(k && k.sprite)}<span><b class="name">${esc(s.cutin.titel)}</b><em>${esc(s.cutin.ruf)}</em></span></span>`;
    document.body.appendChild(d);
    setTimeout(() => d.remove(), 1700);
    return "";
  }
  function html(z){
    const s = z.taktik;
    if (!s) return "";
    setTimeout(() => { trefferZeigen(s); klang(s); }, 0);
    kamSzene(s);
    if (s.phase === "spieler" && ST.phase !== "spieler") ST.weiter = true;   // Spielerzug beginnt: Kamera und Auswahl auf den ersten Trupp
    ST.phase = s.phase;
    sprich(s);
    if (ST.weiter && s.phase === "spieler" && !KAM.alt && !busy()){  // Nach einer Tat steht gleich der naechste Trupp bereit
      ST.weiter = false;
      const treffer = s.anim && ST.anim !== null && s.anim.n !== ST.anim ? Math.min(12, s.anim.log.length) : 0;
      const dran = () => { const q = t(); if (!q || q.phase !== "spieler" || ST.sel) return false; const n = naechster(q); if (n){ ST.sel = n.id; kamAuf(q, n.x, n.y); } return !!n; };
      if (treffer) setTimeout(() => { if (dran()) neu(); }, treffer * 360 / ST.tempo + 700);   // Die Kamera bleibt beim Angreifer, bis die Treffer durch sind (Duc 01.11.2026)
      else dran();
    }
    return `<div class="tk">
      <div class="tk-feldwelt" onclick="EdenTactics.feld(event)" onpointerdown="EdenTactics.panStart(event)" onpointermove="EdenTactics.boden(event)" style="${kamStil(s)}background-image:url('/taktikbild/${esc(s.bild)}')">
        ${barrBild(s)}${felder(s)}<i class="tk-zielfeld"></i><svg class="tk-pfeile" viewBox="0 0 100 66.667" preserveAspectRatio="none">${absichten(s)}</svg>${ziele_karte(s)}${geister(s)}${s.einheiten.map(e => figur(s, e)).join("")}${treffer(s)}${menue(s)}
      </div>
      ${kopf(s)}<div class="tk-info glas" hidden></div>${schlaege(s)}${seite(s)}${cutin(s)}
    </div>`;
  }

  const offen = s => s.einheiten.filter(e => e.seite === "blau" && !e.fest && !e.fertig);
  function naechster(s){
    const o = offen(s);
    if (!o.length) return null;
    const i = o.findIndex(e => e.id === ST.sel);
    return o[(i + 1) % o.length];
  }
  // Infokarte: was man ueber eine Figur wissen muss, solange die Maus darauf steht
  function ueber(id){
    const s = t(), f = document.querySelector(".tk-info");
    if (!s || !f) return;
    const e = id && (einheit(s, id) || (s.feind_start || []).find(q => q.id === id));
    if (!e){ f.hidden = true; return; }
    const lp = e.id === "duc" ? `${s.duc_lp}/${s.duc_lp_max}` : e.boss ? "?" : `${e.lp}/${e.lp_max}`;
    const boden = s.gelaende[s.raster[e.y][e.x]];
    f.innerHTML = `<b class="name">${esc(e.name)}</b>${e.kann ? ` <small>${esc(e.kann)}</small>` : ""}
      <span class="tk-werte"><em>HP ${lp}</em>${e.angriff ? `<em>ATK ${e.angriff}</em>` : ""}<em>DEF ${e.abwehr}</em><em>MOV ${e.bewegung}</em>${e.reichweite > 1 ? `<em>RNG ${e.reichweite}</em>` : ""}</span>
      ${e.rolle ? `<span class="tk-rolle">${ROLLE[e.rolle]}</span>` : ""}
      ${e.text ? `<p>${esc(e.text)}</p>` : ""}${e.id === "duc" && s.duc_waffe ? `<p>Weapon: ${esc(s.duc_waffe.name)}</p>` : ""}${boden && boden.abwehr && !e.fliegt ? `<p>${esc(boden.name)}: +${boden.abwehr} DEF</p>` : ""}${e.haelt ? "<p>Stops for this round.</p>" : ""}`;
    f.hidden = false;
  }
  function fig(id){
    const s = t();
    if (!s || busy()) return;
    if (s.phase === "aufstellen"){ ST.sel = ST.sel === id ? null : id; neu(); return; }
    const e = einheit(s, id);
    if (s.phase !== "spieler" || !e) return;
    if (ST.hilfe){
      const h = s.hilfe.find(x => x.id === ST.hilfe), hid = ST.hilfe;
      if (h && h.ziele.includes(id)){ ST.hilfe = null; aktion("hilfe", {id: hid, ziel: id}); }
      return;
    }
    const sel = ST.sel && einheit(s, ST.sel);
    if (ST.modus === "angriff" && e.seite !== "blau" && sel && (sel.ziele || []).some(g => g.id === id)){
      if (ST.ziel === id){ angriff(); return; }        // zweiter Klick auf dasselbe Ziel greift an
      ST.ziel = id; neu(); return;
    }
    // Zweiter Klick auf den eigenen Trupp: Er bleibt stehen, und das Menue kommt
    if (ST.sel === id && e.seite === "blau" && !e.fest && !e.fertig && !e.gezogen){ ST.modus = null; aktion("bewegen", {id, x: e.x, y: e.y}); return; }
    ST.sel = id; ST.ziel = null; ST.modus = null; kamBlick(s, e); neu();
  }
  // Der naechste Platz bis zwei Felder daneben: die Plaetze sind klein, das Ziehen soll nicht fummelig sein
  function naechsterPlatz(s, x, y){
    let best = null, abst = 3;
    for (const p of s.plaetze){
      const d = Math.abs(p.x - x) + Math.abs(p.y - y);
      if (d < abst){ abst = d; best = p; }
    }
    return best;
  }
  function feld(ev){
    const s = t();
    if (!s || busy()) return;
    const r = ev.currentTarget.getBoundingClientRect();
    const x = Math.floor((ev.clientX - r.left) / r.width * s.spalten), y = Math.floor((ev.clientY - r.top) / r.height * s.zeilen);
    if (s.phase === "aufstellen" && ST.sel){
      const id = ST.sel, p = naechsterPlatz(s, x, y);
      ST.sel = null;
      if (p) aktion("aufstellen", {id, x: p.x, y: p.y}); else neu();
      return;
    }
    const e = ST.sel && einheit(s, ST.sel);
    if (s.phase === "spieler" && e && e.felder && !ST.modus && e.felder.some(f => f[0] === x && f[1] === y)){ ST.ziel = null; aktion("bewegen", {id: ST.sel, x, y}); return; }
    if (ST.modus){ ST.modus = null; ST.ziel = null; neu(); return; }
    ST.ziel = null; neu();
  }
  // Ziehen: Karte oder blaue Figur greifen, auf einen Platz (Aufstellung) oder ein helles Feld (Runde) fallen lassen. Klick bleibt moeglich.
  function greifen(ev, id){
    const s = t();
    if (!s || busy() || ev.button !== 0) return;
    const e = einheit(s, id);
    const darf = s.phase === "aufstellen" ? s.karten.some(k => k.id === id && !k.fest) : s.phase === "spieler" && e && e.seite === "blau" && !e.fest && !e.fertig && !e.gezogen;
    if (darf) ev.stopPropagation();                  // Ziehen der Figur, nicht Schwenken der Karte
    if (darf) Object.assign(ZUG, {id, hilfe: false, x0: ev.clientX, y0: ev.clientY, aktiv: false, feld: null});
  }
  function greifenHilfe(ev, id){
    if (t() && !busy() && ev.button === 0) Object.assign(ZUG, {id, hilfe: true, x0: ev.clientX, y0: ev.clientY, aktiv: false, feld: null});
  }
  function hilfeWahl(id){ aktion("hilfe_wahl", {id}); }
  function flicken(id){ aktion("flicken", {id}); }
  function flickenCrew(id){ aktion("flicken_crew", {id}); }
  function hilfeDruck(id){ ST.hilfe = ST.hilfe === id ? null : id; ST.sel = null; ST.ziel = null; neu(); }
  function hilfeTun(ziel){ const id = ST.hilfe; ST.hilfe = null; aktion("hilfe", {id, ziel}); }
  // Beschreibung der Trupp oder Hilfe, ueber der die Maus steht
  function info(id){
    const s = t(), f = document.querySelector(".tk-detail");
    if (!s || !f || ST.sel) return;
    const k = s.karten.find(x => x.id === id) || s.hilfe.find(x => x.id === id);
    if (k) f.textContent = k.text;
  }
  function zugZiel(s, ev){
    const w = document.querySelector(".tk-feldwelt");
    if (!w) return null;
    const r = w.getBoundingClientRect();
    const x = Math.floor((ev.clientX - r.left) / r.width * s.spalten), y = Math.floor((ev.clientY - r.top) / r.height * s.zeilen);
    if (s.phase === "aufstellen") return naechsterPlatz(s, x, y);
    const e = einheit(s, ZUG.id);
    if (!e || !e.felder) return null;
    return e.felder.some(f => f[0] === x && f[1] === y) ? {x, y} : null;
  }
  document.addEventListener("pointermove", ev => {
    const s = t();
    if (KAM.pan && s){
      const dx = ev.clientX - KAM.pan.x0, dy = ev.clientY - KAM.pan.y0;
      if (!KAM.pan.aktiv && Math.abs(dx) + Math.abs(dy) < 6) return;
      KAM.pan.aktiv = true;
      KAM.x = KAM.pan.kx + dx; KAM.y = KAM.pan.ky + dy;
      kamSetzen(s);
      return;
    }
    if (!ZUG.id || !s) return;
    if (!ZUG.aktiv){
      if (Math.abs(ev.clientX - ZUG.x0) + Math.abs(ev.clientY - ZUG.y0) < 6) return;
      ZUG.aktiv = true;
      if (!ZUG.hilfe){ ST.sel = ZUG.id; ST.ziel = null; }
      neu();
      const w = document.querySelector(".tk-feldwelt"), b = w ? w.getBoundingClientRect().width / s.spalten : 24, e = ZUG.hilfe ? s.hilfe.find(h => h.id === ZUG.id) : einheit(s, ZUG.id) || s.karten.find(k => k.id === ZUG.id);
      ZUG.geist = document.createElement("div");
      ZUG.geist.className = "tk-fig tk-geist blau";
      ZUG.geist.style.width = ZUG.geist.style.height = b + "px";
      ZUG.geist.innerHTML = e.figur ? `<span class="tk-marke"></span>${sprite(e, "dauernd", 0)}` : `<span class="tk-marke">${esc(kuerzel(e.name))}</span>`;
      if (e.figur) ZUG.geist.classList.add("hat-figur");
      document.body.appendChild(ZUG.geist);
    }
    ZUG.geist.style.left = ev.clientX + "px";
    ZUG.geist.style.top = ev.clientY + "px";
    if (ZUG.hilfe){
      const fach = document.querySelector(".tk-plan .tk-hplaetze"), r = fach && fach.getBoundingClientRect();
      ZUG.feld = r && ev.clientX >= r.left && ev.clientX <= r.right && ev.clientY >= r.top && ev.clientY <= r.bottom ? {} : null;
      if (fach) fach.classList.toggle("offen", !!ZUG.feld);
      return;
    }
    ZUG.feld = zugZiel(s, ev);
    const m = document.querySelector(".tk-zielfeld");
    if (m){
      m.style.display = ZUG.feld ? "block" : "none";
      if (ZUG.feld) m.style.cssText += ";" + pos(s, ZUG.feld.x, ZUG.feld.y);
    }
  });
  document.addEventListener("pointerup", () => {
    if (KAM.pan){
      if (KAM.pan.aktiv){ klickSperre = true; setTimeout(() => { klickSperre = false; }, 0); }
      KAM.pan = null;
    }
    if (!ZUG.id) return;
    const s = t(), id = ZUG.id, f = ZUG.feld, war = ZUG.aktiv, hilfe = ZUG.hilfe;
    if (ZUG.geist) ZUG.geist.remove();
    Object.assign(ZUG, {id: null, hilfe: false, aktiv: false, geist: null, feld: null});
    if (!war || !s) return;
    klickSperre = true;                               // der Klick, den der Browser nach dem Ziehen ausloest, zaehlt nicht
    setTimeout(() => { klickSperre = false; }, 0);
    if (hilfe){ if (f) hilfeWahl(id); else neu(); return; }
    if (f) ST.pos[id] = [f.x, f.y];                  // abgelegt: Sie steht schon dort, nichts gleitet mehr
    if (s.phase === "aufstellen") ST.sel = null;
    if (f) aktion(s.phase === "aufstellen" ? "aufstellen" : "bewegen", {id, x: f.x, y: f.y}); else neu();
  });
  document.addEventListener("click", ev => { if (klickSperre){ ev.stopPropagation(); ev.preventDefault(); } }, true);

  function tunRetten(haus){ const id = ST.sel; ST.ziel = null; ST.sel = null; ST.modus = null; ST.weiter = true; aktion("retten", {id, haus}); }
  function tunLoeschen(haus){ const id = ST.sel; ST.ziel = null; ST.sel = null; ST.modus = null; ST.weiter = true; aktion("loeschen", {id, haus}); }
  // Der Gegnerzug laeuft ueber die ganze Karte: kurz herauszoomen, danach zurueck zum naechsten Trupp
  function runde(){
    const s = t();
    if (!s || busy()) return;
    ST.sel = null; ST.ziel = null; ST.modus = null;
    if (KAM.zoom) KAM.alt = {zoom: KAM.zoom, x: KAM.x, y: KAM.y};
    KAM.zoom = null;
    ton("tk_zugwechsel");
    aktion("runde");
    setTimeout(kamZurueck, 6000);                    // falls nichts zu zeigen war, etwa bei einer Szene oder Niederlage
  }
  function tempo(){ ST.tempo = ST.tempo === 1 ? 2 : ST.tempo === 2 ? 4 : 1; neu(); }
  function modus(m){ ST.modus = m; ST.ziel = null; neu(); }
  function rethink(){ ST.sel = null; ST.ziel = null; ST.modus = null; aktion("rueck"); }
  function schalte(was){ ST[was] = !ST[was]; neu(); }
  // Was das Feld unter der Maus bedeutet, immer sichtbar im Kopf
  function boden(ev){
    const s = t(), f = document.querySelector(".tk-gelaendeinfo");
    if (!s || !f) return;
    const r = ev.currentTarget.getBoundingClientRect();
    const x = Math.floor((ev.clientX - r.left) / r.width * s.spalten), y = Math.floor((ev.clientY - r.top) / r.height * s.zeilen);
    const g = s.raster[y] && s.gelaende[s.raster[y][x]];
    f.textContent = g ? `${g.name}: ${g.text}` : "";
  }
  function angriff(){ const id = ST.sel, ziel = ST.ziel; ST.ziel = null; ST.modus = null; ST.sel = null; ST.weiter = true; aktion("angreifen", {id, ziel}); }
  function tun(was){ const id = ST.sel; ST.ziel = null; ST.modus = null; if (was === "warten" || was === "macht"){ ST.sel = null; ST.weiter = true; } aktion(was, {id}); }
  // Esc geht immer einen Schritt zurueck: Ziel, Angriffsmodus, Bewegung, Auswahl
  function zurueckSchritt(s){
    const e = ST.sel && einheit(s, ST.sel);
    if (ST.hilfe) ST.hilfe = null;
    else if (ST.ziel) ST.ziel = null;
    else if (ST.modus) ST.modus = null;
    else if (e && e.seite === "blau" && e.gezogen && !e.fertig){ aktion("zurueck", {id: e.id}); return; }
    else ST.sel = null;
    neu();
  }

  document.addEventListener("keydown", ev => {
    const s = t();
    if (!s || typeof V === "undefined" || V.z.status !== "taktik" || busy()) return;
    if (s.phase === "szene" && s.szene && s.szene.art === "wahl" && ev.key !== "Escape") return;   // bei einer Wahl zaehlt nur der Klick
    if ((ev.key === " " || ev.key === "Enter") && s.phase === "szene"){ ev.preventDefault(); aktion("szene"); }
    else if (ev.key === "Escape" && s.phase === "szene"){ ev.stopPropagation(); aktion("szene_alle"); }
    else if (ev.key === "Escape"){ ev.stopPropagation(); zurueckSchritt(s); }
    else if (ev.key === "r" || ev.key === "R") schalte("gefahr");
    else if (ev.key === "t" || ev.key === "T") schalte("gelaende");
    else if (ev.key === "z" || ev.key === "Z") ganzeKarte();
    else if (ev.key === "f" || ev.key === "F") tempo();
    else if (s.phase === "spieler" && ev.key === "Tab"){
      ev.preventDefault();
      const n = naechster(s);
      if (n){ ST.sel = n.id; ST.ziel = null; ST.modus = null; kamBlick(s, n); neu(); }
    }
    else if (s.phase === "spieler" && ev.key === "Enter" && !offen(s).length){ ev.preventDefault(); runde(); }
    else if (s.phase === "spieler" && ev.key.startsWith("Arrow")){
      ev.preventDefault();
      const d = 80;
      if (ev.key === "ArrowLeft") KAM.x += d; else if (ev.key === "ArrowRight") KAM.x -= d; else if (ev.key === "ArrowUp") KAM.y += d; else KAM.y -= d;
      kamSetzen(s);
    }
  }, true);                                         // zuerst: Andere Tastenregeln im Spiel fangen R sonst ab

  window.EdenTactics = {flicken, flickenCrew, html, fig, feld, greifen, greifenHilfe, tunRetten, tunLoeschen, modus, rethink, runde, tempo, ganzeKarte, panStart, ueber, schalte, boden, hilfeWahl, hilfeDruck, hilfeTun, info, aktion, angriff, tun, _st: ST};
  try { if (typeof V !== "undefined" && V && V.z && V.z.status === "taktik") zeichnen(); } catch (e) {}
})();
