/* Gathering at rest sites (Duc 28.10.2026). The engine (kern/abbau.py) decides what stands there and books the yield; this
   plugin plays the swing: a ring closes in on the golden target ring around the notch - hit Space when they meet (like the ring
   parry in combat). Old tools need three good blows per tree or rock, better ones one, the tempered ones none: one swing and it
   comes down. Perfect last blow = +1. A tree falls, a rock splits. A cork oak stays standing: its bark drops on the second-to-last blow.
   Also: the source chips on a rest frame (wood / stone / water, with "back in N days" when empty) and Petru's tool panel.
   Sends: abbau_start {art}, abbau_schlag {ergebnis}, abbau_ende, angeln_start {ort}, petru_kaufen {werkzeug},
   petru_fisch {fisch, alle} (Petru buys fish from the first catch, 28.10.2026), petru_koeder {koeder, look} and
   petru_koeder_look {koeder, look} (baits, 30.10.2026).
   The overlay keeps its own state; redraws of the game never restart a swing. */
window.EdenAbbau = (function(){
  const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}[c]));
  const merk = {lesen(k, d){ try { return localStorage.getItem(k) ?? d; } catch(e){ return d; } }, schreiben(k, v){ try { localStorage.setItem(k, v); } catch(e){} }};
  const uiIc = (id, klasse) => window.EdenUI ? EdenUI.icon(id, klasse) : "";
  const ROH_ICON = {timber: "timber", slate: "slate", granite: "granite", steel: "steel", cork: "cork", iron: "iron", feather: "feather", cloth: "cloth", wool: "wool", leather: "leather", coral: "coral"};
  const rohIc = id => ROH_ICON[id] ? uiIc(ROH_ICON[id], "imtext") : "";
  const ART = {
    holz: {icon: "axe", titel: "Work the trees", ding: ["tree", "trees"], taste: "C", schlag: "abbau_axt", fertig: "abbau_baum_faellt"},
    stein: {icon: "pick", titel: "Break rocks", ding: ["rock", "rocks"], taste: "M", schlag: "abbau_hacke", fertig: "abbau_stein_bricht"},
    wasser: {icon: "fish", titel: "Fish", ding: ["cast", "casts"], taste: "F"},
    bau: {icon: "guard", titel: "Mending", ding: ["job", "jobs"], taste: "", schlag: "tk_hammer", fertig: "tk_bretter"},   // Belagerung, kern/belagerung.py (Duc 01.11.2026)
  };
  const BLOWS = n => n === 0 ? "one swing and it's down" : n === 1 ? "one good blow each" : `${n} good blows each`;
  let S = null;              // running session: {phase, raf, timer, t0, dauer, nr, treffer}

  const spiel = () => (typeof V !== "undefined" && V && V.z) || {};
  const sfx = id => { if (window.EdenSfx && EdenSfx.play) { try { EdenSfx.play(id); } catch(e){} } };
  const send = (aktion, daten) => (typeof senden === "function" ? senden(aktion, daten || {}, "…") : Promise.resolve());
  const besetzt = () => typeof beschaeftigt !== "undefined" && beschaeftigt;
  const $ = sel => document.querySelector("#abbau " + sel);

  // ---------------------------------------------------------------- source circles on a rest frame (eden-expedition)
  // Duc 30.10.2026: like the fishing circle. What is there can be clicked; what is gone stays as a grey circle.
  function quellenHtml(e){
    const qs = (e && e.quellen) || [];
    if (!qs.length || e.ergebnis || !window.EdenAngeln) return "";
    return `<div class="eb-kreise exp-hud" aria-label="What you can gather here">${qs.map(q => {
      const a = ART[q.art], leer = !q.rest, zu = !!q.fehlt, voll = !leer && !zu && !!q.voll, geht = !leer && !zu && !voll;
      const zeile = zu ? `needs ${q.fehlt === "Axe" ? "an axe" : "a pickaxe"} · Petru`
        : leer ? `back in ${q.in_tagen} day${q.in_tagen === 1 ? "" : "s"}` : voll ? "bag full" : "";
      const was = q.art === "wasser" ? `${a.titel} · ${q.wasser === "meer" ? "sea" : "fresh water"}` : a.titel;
      const klick = q.art === "wasser" ? `senden('angeln_start',{ort:'${esc(q.platz)}'},'You fetch the rod …')` : `senden('abbau_start',{art:'${q.art}'},'…')`;
      return EdenAngeln.kreisKnopf({bild: q.bild, zahl: q.rest, zu: !geht || besetzt(), klick, aria: a.titel,
        lab: zeile ? esc(zeile) : `${esc(a.titel)} <kbd>${a.taste}</kbd>`,
        titel: leer ? "Empty for now. It grows back." : zu ? "Petru sells tools from day 2." : voll ? "No room in your bag. Make room first (I)."
          : `${was} · ${q.rest} ${q.rest === 1 ? a.ding[0] : a.ding[1]} left${q.werkzeug ? " · " + q.werkzeug.label : ""}`});
    }).join("")}</div>`;
  }
  function quelleTaste(k){
    const z = spiel(), e = z.ereignis;
    if (!e || !e.quellen || e.ergebnis || z.rast_anruf || besetzt()) return false;
    const q = e.quellen.find(x => ART[x.art].taste === k.toUpperCase());
    if (!q || !q.rest || q.fehlt || q.voll) return false;
    if (q.art === "wasser") send("angeln_start", {ort: q.platz}); else send("abbau_start", {art: q.art});
    return true;
  }

  // ---------------------------------------------------------------- overlay
  function geruest(a){
    const box = document.createElement("div");
    box.id = "abbau";
    box.className = "art-" + a.art;
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-label", ART[a.art].titel);
    box.innerHTML = `
      <div class="eb-hinter" style="${a.bild ? `background-image:url('${esc(a.bild)}')` : ""}"></div>
      <div class="eb-vignette"></div>
      <header class="eb-kopf glas">
        <div class="eb-ort"><small>${ART[a.art].titel}${a.bau ? "" : " · rest site"}</small><b>${esc(a.label)}</b></div>
        <div class="eb-knotenreihe" aria-label="Trees and rocks here"></div>
        <div class="eb-beute" aria-label="Gathered so far"></div>
        <div class="eb-werkzeug" title="${esc(a.werkzeug.label)}">${a.werkzeug.bild ? `<img src="${esc(a.werkzeug.bild)}" alt="">` : ""}<span><b>${esc(a.werkzeug.label)}</b><small>${a.bau ? "" : `Level ${a.werkzeug.stufe} · `}${BLOWS(a.direkt ? 0 : a.noetig)}</small></span></div>
        <button type="button" class="eb-knopf" data-eb="ende"><kbd>Esc</kbd> ${a.bau ? "Stop, and get your materials back" : "Back to the fire"}</button>
      </header>
      <section class="eb-buehne" aria-hidden="true">
        <div class="eb-staub"></div>
        <div class="eb-ziel">
          <div class="eb-ring"><div class="eb-gut"></div><div class="eb-zielring"></div><div class="eb-lauf"></div></div>
          <div class="eb-ruf"></div>
          <div class="eb-pips"></div>
        </div>
      </section>
      <div class="eb-unten glas" aria-live="polite" hidden></div>
      <div class="eb-karte glas" hidden></div>`;
    box.addEventListener("pointerdown", e => {
      const b = e.target.closest("[data-eb]");
      if (b){ e.stopPropagation(); aktion(b.dataset.eb); return; }
      if (e.target.closest(".eb-buehne")) taste();
    });
    document.getElementById("app").appendChild(box);
    return box;
  }

  function kopf(a){
    const reihe = a.knoten.map((k, i) => {
      const g = a.geschafft[i];
      const kl = g ? "fertig" + (g.perfekt ? " perfekt" : "") : i === a.nr ? "jetzt" : "offen";
      return `<span class="eb-kn ${kl}" title="${esc(k.label)}">${g ? uiIc(a.art === "holz" ? "timber" : "slate", "imtext") : ""}</span>`;
    }).join("");
    $(".eb-knotenreihe").innerHTML = reihe;
    const summe = {};
    a.geschafft.forEach(g => g.ertrag.forEach(r => { summe[r.id] = (summe[r.id] || 0) + r.n; }));
    const ids = a.art === "holz" ? ["timber", "cork"] : a.art === "bau" ? ["timber", "slate"] : ["slate", "granite"];
    $(".eb-beute").innerHTML = ids.map(id => {
      const r = (a.rohstoffe || []).find(x => x.id === id) || {label: id, n: 0};
      return `<span class="eb-roh${summe[id] ? " neu" : ""}"><i>${rohIc(id)}</i><b>${r.n}</b> ${esc(r.label)}${summe[id] ? `<em>+${summe[id]}</em>` : ""}</span>`;
    }).join("");
  }

  function unten(html){ const u = $(".eb-unten"); if (u){ u.innerHTML = html; u.hidden = !html; } }
  function karte(html, klasse){
    const k = $(".eb-karte");
    k.className = "eb-karte glas " + (klasse || "");
    k.innerHTML = html;
    k.hidden = !html;
  }

  // the tree or rock on stage; the notch (where the ring sits) is on the trunk for trees, in the middle for rocks
  function knotenZeigen(a, rein){
    const k = a.knoten[a.nr], b = $(".eb-buehne");
    b.querySelectorAll(".eb-sprite").forEach(x => x.remove());
    if (!k) return;
    if (a.art === "bau"){                              // Noch kein Bild: Mit jedem guten Schlag sitzt ein Brett mehr (Bilder kommen spaeter)
      const w = document.createElement("div");
      w.className = "eb-sprite eb-bauwerk " + a.typ;
      w.innerHTML = Array.from({length: a.noetig}, (_, i) => `<i class="${i < a.treffer ? "an" : ""}"></i>`).join("");
      b.insertBefore(w, b.firstChild);
      $(".eb-ziel").dataset.art = a.art;
      $(".eb-pips").innerHTML = Array.from({length: a.noetig}, (_, i) => `<i class="${i < a.treffer ? "voll" : ""}"></i>`).join("");
      return;
    }
    if (k.sprite_nach){ new Image().src = k.sprite_nach; new Image().src = k.sprite_rinde; }
    const img = document.createElement("img");
    img.className = "eb-sprite " + (a.art === "holz" ? "baum" : "fels") + (rein ? " rein" : "");
    img.src = k.sprite;
    img.alt = k.label;
    b.insertBefore(img, b.firstChild);
    $(".eb-ziel").dataset.art = a.art;
    $(".eb-pips").innerHTML = a.direkt ? "" : Array.from({length: a.noetig}, (_, i) => `<i class="${i < a.treffer ? "voll" : ""}"></i>`).join("");
  }

  function startKarte(a){
    const rest = a.knoten.length - a.nr, ding = ART[a.art].ding;
    const neu = merk.lesen("eden_abbau_tutorial", "0") !== "1";
    S.phase = "start";
    ringAus();
    if (a.bau) karte(`<small>Mending</small><b>${esc(a.label)}</b>
      <p>A ring closes in on the <span class="gold">golden ring</span>. Hit <kbd>Space</kbd> the moment they meet. Three good blows finish the job, and each perfect blow saves wood.</p>
      <button type="button" class="eb-gross" data-eb="los"><kbd>Space</kbd> Start</button>`, "start");
    else karte(`<small>${esc(a.label)}</small><b>${rest} ${rest === 1 ? ding[0] : ding[1]} to ${a.art === "holz" ? "fell" : "break"}</b>
      <p>${esc(a.werkzeug.label)}: ${BLOWS(a.direkt ? 0 : a.noetig)}.</p>
      ${neu && !a.direkt ? `<p class="eb-hilfe">A ring closes in on the <span class="gold">golden ring</span> around the notch. Hit <kbd>Space</kbd>
        the moment they meet. Spot on is a <b>perfect</b> blow, and a perfect last blow gives one extra piece.</p>` : ""}
      <button type="button" class="eb-gross" data-eb="los"><kbd>Space</kbd> ${a.direkt ? "Swing" : "Start"}</button>`, "start");
  }

  // ---------------------------------------------------------------- the ring
  const R_ZIEL = 92;                  // px diameter of the golden target ring
  function ringAus(){ cancelAnimationFrame(S && S.raf); const r = $(".eb-ring"); if (r) r.classList.remove("an"); }
  function ringStart(a){
    if (!S) return;
    karte("");
    if (a.direkt){
      S.phase = "direkt";
      unten(`<kbd>Space</kbd> Swing`);
      ringAus();
      return;
    }
    S.phase = "ring";
    const r = a.ring, z = $(".eb-ring");
    S.dauer = r.dauer * 1000 * Math.pow(r.schneller, a.treffer);
    S.t0 = performance.now() + 220;
    const gutPx = R_ZIEL * (1 + 2.2 * (r.gut_ms / S.dauer)), perfPx = R_ZIEL * (1 + 2.2 * (r.perfekt_ms / S.dauer));
    z.style.setProperty("--ziel", R_ZIEL + "px");
    z.querySelector(".eb-gut").style.width = z.querySelector(".eb-gut").style.height = gutPx + "px";
    z.querySelector(".eb-zielring").style.setProperty("--perf", (perfPx - R_ZIEL) / 2 + "px");
    z.classList.add("an");
    unten(`<kbd>Space</kbd> when the rings meet`);
    const lauf = z.querySelector(".eb-lauf");
    lauf.style.width = lauf.style.height = R_ZIEL * 3.2 + "px";      // never start from the last ring's size
    lauf.style.opacity = 0;
    const schritt = now => {
      if (!S || S.phase !== "ring") return;
      const t = (now - S.t0) / S.dauer, q = Math.max(0, Math.min(1.25, t));
      const g = R_ZIEL * (1 + 2.2 * (1 - Math.min(q, 1))) * (q > 1 ? 1 - (q - 1) * 0.6 : 1);
      lauf.style.width = lauf.style.height = g + "px";
      lauf.style.opacity = q > 1 ? Math.max(0, 1 - (q - 1) * 4) : Math.min(1, t * 4 + 0.2);
      if (t >= 1.25){ verpasst(a); return; }
      S.raf = requestAnimationFrame(schritt);
    };
    S.raf = requestAnimationFrame(schritt);
  }
  // the ring ran out without a swing: not a blow (nothing is sent); after two in a row the game waits for the player
  function verpasst(a){
    cancelAnimationFrame(S.raf);
    S.verpasst = (S.verpasst || 0) + 1;
    ruf("Too slow", "daneben");
    if (S.verpasst >= 2){
      S.phase = "pause";
      ringAus();
      unten(`<kbd>Space</kbd> Ready when you are`);
      return;
    }
    S.phase = "melden";
    setTimeout(() => { if (S && S.phase === "melden") ringStart(a); }, 520);
  }
  function bewerten(){
    const a = spiel().abbau, d = Math.abs(performance.now() - (S.t0 + S.dauer));
    return d <= a.ring.perfekt_ms ? "perfekt" : d <= a.ring.gut_ms ? "gut" : "daneben";
  }

  // ---------------------------------------------------------------- one blow
  function ruf(text, klasse){
    const r = $(".eb-ruf");
    r.className = "eb-ruf " + klasse;
    r.textContent = text;
    void r.offsetWidth;
    r.classList.add("an");
  }
  function spaene(art, viele){
    const b = $(".eb-buehne"), ziel = $(".eb-ziel").getBoundingClientRect(), bb = b.getBoundingClientRect();
    for (let i = 0; i < (viele ? 16 : 8); i++){
      const p = document.createElement("i");
      p.className = "eb-span " + art;
      const w = (Math.random() - 0.5) * Math.PI * 1.4 - Math.PI / 2, v = 60 + Math.random() * (viele ? 150 : 90);
      p.style.left = (ziel.left - bb.left + ziel.width / 2) + "px";
      p.style.top = (ziel.top - bb.top + ziel.height / 2) + "px";
      p.style.setProperty("--dx", Math.cos(w) * v + (art === "holz" ? 40 : 0) + "px");
      p.style.setProperty("--dy", Math.sin(w) * v + "px");
      p.style.setProperty("--rot", (Math.random() * 720 - 360) + "deg");
      b.appendChild(p);
      setTimeout(() => p.remove(), 900);
    }
  }
  function wackeln(perfekt){
    const sp = $(".eb-sprite");
    if (sp){ sp.classList.remove("hieb"); void sp.offsetWidth; sp.classList.add("hieb"); }
    if (perfekt){ const box = document.getElementById("abbau"); box.classList.remove("beben"); void box.offsetWidth; box.classList.add("beben"); }
  }
  // Cork oak (Duc 30.10.2026): the bark comes off in one piece and collapses at the foot of the tree. Only the bark.
  function rindeFaellt(kn){
    const sp = $(".eb-sprite");
    if (!sp) return;
    const r = sp.cloneNode();
    r.classList.remove("hieb", "rein");
    r.classList.add("eb-rinde");
    r.src = kn.sprite_rinde;
    sp.src = kn.sprite_nach;
    sp.after(r);
    setTimeout(() => sfx("abbau_rinde_faellt"), 90);
    setTimeout(() => r.remove(), 1200);
  }
  async function schlag(ergebnis){
    const a = spiel().abbau;
    if (!a || !S || S.phase === "melden") return;
    cancelAnimationFrame(S.raf);
    S.phase = "melden";
    S.verpasst = 0;
    const art = a.art;
    if (ergebnis === "daneben"){
      sfx("abbau_daneben");
      ruf("Glancing blow", "daneben");
      $(".eb-ring").classList.add("fehl");
      setTimeout(() => { const r = $(".eb-ring"); if (r) r.classList.remove("fehl"); }, 300);
    } else {
      sfx(ART[art].schlag);
      ruf(ergebnis === "perfekt" ? "Perfect!" : "Good", ergebnis);
      spaene(art, ergebnis === "perfekt");
      wackeln(ergebnis === "perfekt");
      const pip = $(".eb-pips").children[a.treffer];
      if (pip) pip.classList.add("voll");
      const brett = document.querySelectorAll("#abbau .eb-bauwerk i")[a.treffer];
      if (brett) brett.classList.add("an");
    }
    if (merk.lesen("eden_abbau_tutorial", "0") !== "1") merk.schreiben("eden_abbau_tutorial", "1");
    const vorher = a.nr;
    await send("abbau_schlag", {ergebnis});
    const n = spiel().abbau;
    if (!n || !S) return;
    kopf(n);
    if (n.nr > vorher){ await fallen(n, n.geschafft[n.geschafft.length - 1]); return; }
    setTimeout(() => { if (S && S.phase === "melden") ringStart(n); }, ergebnis === "daneben" ? 520 : 380);
  }
  function fallen(a, e){
    return new Promise(fertig => {
      S.phase = "faellt";
      ringAus();
      unten("");
      const sp = $(".eb-sprite"), b = $(".eb-buehne");
      const korn = a.knoten[a.nr - 1], kork = !!(korn && korn.sprite_rinde);
      if (!kork) setTimeout(() => sfx(ART[a.art].fertig), 120);
      if (kork){
        rindeFaellt(korn);                                 // on the last blow, together with the yield (Duc 30.10.2026)
        if (sp) sp.classList.add("steht");                 // the tree stays; we simply move on to the next one
      } else if (a.art === "bau"){
        // das Bauwerk steht und bleibt stehen
      } else if (a.art === "holz"){
        if (sp) sp.classList.add("faellt");
      } else if (sp){                       // the rock splits: two halves of the same picture drift apart
        ["links", "rechts"].forEach(seite => {
          const h = sp.cloneNode();
          h.className = "eb-sprite fels haelfte " + seite;
          b.appendChild(h);
        });
        sp.remove();
      }
      const staub = $(".eb-staub");
      if (!kork){ staub.classList.remove("an"); void staub.offsetWidth; staub.classList.add("an", a.art); }
      const beute = document.createElement("div");
      beute.className = "eb-beutezug";
      beute.innerHTML = `${e.ertrag.map(r => `<span><i>${rohIc(r.id)}</i>+${r.n} ${esc(r.label)}</span>`).join("")}${e.perfekt ? `<small>Clean finish · +1</small>` : ""}${(e.liegen || []).length ? `<small class="eb-liegen">${uiIc("backpack", "imtext")} Bag full · ${e.liegen.map(r => `${r.n} ${esc(r.label)}`).join(", ")} left behind</small>` : ""}`;
      b.appendChild(beute);
      setTimeout(() => {
        beute.remove();
        b.querySelectorAll(".haelfte").forEach(x => x.remove());
        if (!S) return fertig();
        if (a.nr >= a.knoten.length || a.voll){ endeKarte(a); return fertig(); }      // bag full: stop here (stacking 28.10.2026)
        knotenZeigen(a, true);
        setTimeout(() => { if (S) ringStart(a); fertig(); }, 420);
      }, 1500);
    });
  }
  function endeKarte(a){
    S.phase = "ende";
    ringAus();
    unten("");
    $(".eb-pips").innerHTML = "";
    const summe = {};
    a.geschafft.forEach(g => g.ertrag.forEach(r => { summe[r.label] = (summe[r.label] || 0) + r.n; }));
    const perf = a.geschafft.filter(g => g.perfekt).length, rest = a.knoten.length - a.nr;
    const voll = a.voll && rest > 0;
    if (a.bau) karte(`<small>Mending</small><b>${esc(a.label)} is mended</b>
      <div class="eb-summe">${Object.entries(summe).map(([l, n]) => `<span>+${n} ${esc(l)}</span>`).join("")}</div>
      <button type="button" class="eb-gross" data-eb="ende"><kbd>Space</kbd> Back to the list</button>`, "ende");
    else karte(`<small>${esc(a.label)}</small><b>${voll ? "Your bag is full" : a.art === "holz" ? "That's all the trees here" : "Nothing left to break"}</b>
      <div class="eb-summe">${Object.entries(summe).map(([l, n]) => `<span>+${n} ${esc(l)}</span>`).join("")}</div>
      <p>${perf ? `${perf} clean finish${perf > 1 ? "es" : ""}. ` : ""}${voll ? `${rest} ${rest === 1 ? ART[a.art].ding[0] : ART[a.art].ding[1]} still here. Make room and come back.` : "It grows back in a few days."}</p>
      <button type="button" class="eb-gross" data-eb="ende"><kbd>Space</kbd> Back to the fire</button>`, "ende");
  }

  // ---------------------------------------------------------------- input
  function taste(){
    const a = spiel().abbau;
    if (!a || !S || besetzt()) return;
    if (S.phase === "start" || S.phase === "pause"){ S.verpasst = 0; return ringStart(a); }
    if (S.phase === "ring") return schlag(bewerten());
    if (S.phase === "direkt") return schlag("perfekt");
    if (S.phase === "ende") return aktion("ende");
  }
  function aktion(k){
    if (k === "los") return taste();
    if (k === "ende"){
      if (!S || S.phase === "faellt" || besetzt()) return;
      cancelAnimationFrame(S.raf);
      S.phase = "weg";
      send("abbau_ende");
    }
  }
  window.addEventListener("keydown", e => {
    if (e.target && e.target.closest && e.target.closest("input, textarea")) return;
    if (document.getElementById("abbau")){
      if (e.key === " " || e.key === "Enter"){ e.preventDefault(); e.stopImmediatePropagation(); if (!e.repeat) taste(); }
      else if (e.key === "Escape"){ e.preventDefault(); e.stopImmediatePropagation(); aktion("ende"); }
      return;
    }
    if (document.getElementById("angeln") || !document.querySelector(".exp")) return;
    if (/^[cmf]$/i.test(e.key) && !e.ctrlKey && !e.altKey && !e.metaKey && quelleTaste(e.key)){ e.preventDefault(); e.stopImmediatePropagation(); }
  }, true);

  // ---------------------------------------------------------------- sync with the game
  function update(z){
    const a = z && z.status === "abbau" && z.abbau;
    document.body.classList.toggle("abbau-modus", !!a);
    let box = document.getElementById("abbau");
    if (!a){
      if (box) box.remove();
      if (S){ cancelAnimationFrame(S.raf); clearTimeout(S.timer); }
      S = null;
      return;
    }
    if (!box){
      box = geruest(a);
      S = {phase: "start", raf: 0, timer: 0};
      kopf(a);
      knotenZeigen(a, false);
      if (a.nr >= a.knoten.length) endeKarte(a); else startKarte(a);
    }
  }

  // ---------------------------------------------------------------- Petru's workshop: tools
  function kostenHtml(n, konto){
    const teile = [`<span class="${konto >= n.geld ? "ok" : "fehlt"}">${n.geld} €</span>`]
      .concat(n.rohstoffe.map(r => `<span class="${r.hast >= r.n ? "ok" : "fehlt"}">${rohIc(r.id)} ${r.n} ${esc(r.label)} <small>(${r.hast})</small></span>`))
      .concat(n.fisch ? [`<span class="${n.fisch.hast ? "ok" : "fehlt"}">${uiIc("fish", "imtext")} a ${esc(n.fisch.label)} <small>${n.fisch.hast ? "in your pantry" : "catch one"}</small></span>`] : []);
    return `<div class="eb-kosten">${teile.join("")}</div>`;
  }
  function petruHtml(z){
    const ws = z.werkzeuge || [], konto = (z.handel || {}).konto ?? 0;
    if (!ws.length) return `<p class="leer">Petru's tools are still on the wall.</p>`;
    return `<p class="leer" style="margin:0 0 10px">An axe for wood, a pickaxe for stone. You'll find both at the rest sites on your expeditions. Better tools take fewer blows.</p>
      <div class="eb-werkzeuge">${ws.map(w => {
        const j = w.jetzt, n = w.naechste;
        return `<section class="eb-wz">
          <header>${j ? `<img src="${esc(j.bild)}" alt="">` : `<span class="eb-wz-leer">${uiIc(w.art === "holz" ? "axe" : "pick", "imtext")}</span>`}
            <div><b>${esc(w.label)}</b><small>${j ? `Level ${w.stufe} · ${esc(j.label)} · ${BLOWS(j.treffer)}` : "You don't have one yet"}</small></div>
            <span class="eb-stufen">${[1, 2, 3].map(i => `<i class="${i <= w.stufe ? "an" : ""}"></i>`).join("")}</span></header>
          ${n ? `<div class="eb-naechste"><img src="${esc(n.bild)}" alt=""><div>
              <small>${w.stufe ? "Upgrade to level " + n.stufe : "Buy"} · ${BLOWS(n.treffer)}</small><b>${esc(n.label)}</b><p>${esc(n.text)}</p>
              ${kostenHtml(n, konto)}
              ${n.gesperrt ? `<p class="eb-gesperrt">${uiIc("locked", "imtext")} ${esc(n.gesperrt)}</p>` : ""}
              <button class="mini" type="button" ${n.geht && !besetzt() ? "" : "disabled"} onclick="EdenAbbau.kaufen('${esc(w.id)}')">${w.stufe ? "Upgrade" : "Buy"} · ${n.geld} €</button>
            </div></div>` : `<p class="eb-max">The best there is. Petru nods at it once, which says everything.</p>`}
        </section>`;
      }).join("")}</div>`;
  }
  function kaufen(wid){
    send("petru_kaufen", {werkzeug: wid}).then(() => {
      const z = spiel();
      if (z.petru_zeile && typeof LADEN !== "undefined"){ LADEN.stimmung = z.petru_zeile; if (typeof zeichnen === "function") zeichnen(); }
    });
  }

  // ---------------------------------------------------------------- Petru buys fish (28.10.2026): from the first catch
  const SELTEN = ["", "common", "uncommon", "rare"];
  function fischHtml(z){
    const fs = z.petru_fische || [];
    const kopf = `<p class="leer" style="margin:0 0 10px">Petru pays by how rare a fish is, not how pretty. The first time you bring him a kind, he tells you about it.</p>`;
    if (!fs.length) return kopf + `<p class="leer">Nothing in your pantry he'd buy. Go fishing.</p>`;
    return kopf + `<div class="eb-fische">${fs.map(f => `<div class="eb-fisch">
        <img src="${esc(f.bild)}" alt=""><div><b>${esc(f.label)}</b>
        <small>${SELTEN[f.stufe] || ""} · ×${f.n} in your pantry${f.neu ? ` · <span class="eb-neu">he hasn't seen one from you yet</span>` : ""}</small></div>
        <span class="eb-preis">${f.preis} € each</span>
        <button class="mini" type="button" ${besetzt() ? "disabled" : ""} onclick="EdenAbbau.fischVerkaufen('${esc(f.id)}', false)">Sell 1</button>
        ${f.n > 1 ? `<button class="mini" type="button" ${besetzt() ? "disabled" : ""} onclick="EdenAbbau.fischVerkaufen('${esc(f.id)}', true)">All · ${f.preis * f.n} €</button>` : ""}
      </div>`).join("")}</div>`;
  }
  function fischVerkaufen(fid, alle){
    send("petru_fisch", {fisch: fid, alle: !!alle}).then(() => {
      const z = spiel();
      if (z.petru_zeile && typeof LADEN !== "undefined"){ LADEN.stimmung = z.petru_zeile; if (typeof zeichnen === "function") zeichnen(); }
    });
  }

  // ---------------------------------------------------------------- Petru's baits (30.10.2026): permanent, 3 levels, 2 looks each
  // Before building, a click on a look picks it; once built, the look can be switched any time. The best bait you own is used.
  const KOEDER_WAHL = {};                                   // look picked before building: {baitId: lookId}
  function koederHtml(z){
    const ks = z.petru_koeder || [], konto = (z.handel || {}).konto ?? 0;
    if (!ks.length) return `<p class="leer">Petru's bait tin is empty.</p>`;
    return `<p class="leer" style="margin:0 0 10px">Baits are never used up. The best one you own is on the line, and each comes in two looks you can swap whenever you like.
        Gull feathers come from gulls you beat, and now and then from the rocks by the sea.</p>
      <div class="eb-werkzeuge">${ks.map(k => {
        const wahl = k.gebaut ? k.look : (KOEDER_WAHL[k.id] || k.looks[0].id);
        return `<section class="eb-wz eb-koeder${k.aktiv ? " aktiv" : ""}">
          <header><img src="${esc(k.looks.find(l => l.id === wahl).bild)}" alt="" style="object-fit:contain">
            <div><b>${esc(k.label)}</b><small>Level ${k.stufe}${k.aktiv ? " · on your line" : k.gebaut ? " · built" : ""}</small></div>
            <span class="eb-stufen">${[1, 2, 3].map(i => `<i class="${i <= k.stufe ? "an" : ""}"></i>`).join("")}</span></header>
          <p class="eb-text">${esc(k.text)}</p>
          <ul class="eb-wirkung">${k.wirkung.map(t => `<li>${esc(t)}</li>`).join("")}</ul>
          <div class="eb-looks" role="radiogroup" aria-label="Look">${k.looks.map(l => `<button type="button" class="eb-look${l.id === wahl ? " an" : ""}" role="radio" aria-checked="${l.id === wahl}"
              ${besetzt() ? "disabled" : ""} onclick="EdenAbbau.koederLook('${esc(k.id)}', '${esc(l.id)}', ${k.gebaut})"><img src="${esc(l.bild)}" alt=""><small>${esc(l.label)}</small></button>`).join("")}</div>
          ${k.gebaut ? "" : `${kostenHtml({geld: k.geld, rohstoffe: k.rohstoffe, fisch: null}, konto)}
            <button class="mini" type="button" ${k.geht && !besetzt() ? "" : "disabled"} onclick="EdenAbbau.koederBauen('${esc(k.id)}')">Build · ${k.geld} €</button>`}
        </section>`;
      }).join("")}</div>`;
  }
  function koederNeuZeichnen(){
    const z = spiel();
    if (z.petru_zeile && typeof LADEN !== "undefined") LADEN.stimmung = z.petru_zeile;
    if (typeof zeichnen === "function") zeichnen();
  }
  function koederBauen(kid){
    send("petru_koeder", {koeder: kid, look: KOEDER_WAHL[kid] || null}).then(koederNeuZeichnen);
  }
  function koederLook(kid, look, gebaut){
    if (!gebaut){ KOEDER_WAHL[kid] = look; if (typeof zeichnen === "function") zeichnen(); return; }
    send("petru_koeder_look", {koeder: kid, look}).then(() => { if (typeof zeichnen === "function") zeichnen(); });
  }

  // The client may have drawn the rest frame before this (defer) script arrived: draw once more, like eden-expedition does.
  setTimeout(() => {
    const z = spiel();
    if ((z.status === "abbau" || (z.ereignis && z.ereignis.rast)) && typeof zeichnen === "function") zeichnen();
  }, 0);
  return {update, quellenHtml, petruHtml, kaufen, fischHtml, fischVerkaufen, koederHtml, koederBauen, koederLook, _st: () => S};
})();
