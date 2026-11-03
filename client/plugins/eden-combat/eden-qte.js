/* Parade-Probe als eigener Baustein (Duc 03.11.2026, "Lesen statt rechnen"). Nur Zeit und Darstellung, keine Regeln.
   Ablauf wie in Sekiro / Clair Obscur: erst holt der Gegner aus und leuchtet (1 s, Perle = parieren, Blau = ausweichen),
   dann die Probe. Parieren ist eine Leiste (der Marker laeuft auf die Zone), Ausweichen bewusst eine andere Probe: ein Kreis
   zieht sich auf den Zielring zusammen (Duc 03.11.2026). Der Kampf (eden-combat.js) und der Showcase
   (docs/abnahme/kampf_lesen/) nutzen denselben Code.

   EdenQTE.start(host, spec, hooks) -> {druck(), ausweichen(), stop()}
     spec  {art: "parieren" | "ausweichen" | "wahl", lauf (ms bis zum Schlag), ziel (Lage der Zone in %),
            fenster {gut, perf} (ms, ganze Breite), finte {art, ...} | null, bekannt (Finte schon erlebt: leichte Markierung),
            name, tell (ms, nur Showcase-Zeitlupe)}
     hooks {tell(an), schlag(i, letzter), finte(), halten(), treffer(i), ende(ergebnis)}
            ergebnis: perfekt | gut | ausweichen | verfehlt; treffer(i): Schlag i einer Kette pariert (nicht der letzte)
   Rueckmeldung (Duc 03.11.2026, "satter, ermutigend"): Kettentreffer pulsen hell, die perfekte Parade laesst vom Kern
   einen Ring aufplatzen, ein Fehler sagt leise "Too early" / "Too late", die Serie perfekter Paraden steht als Punkte
   daneben (spec.serie / spec.serie_max). Ring und Hinweis liegen fixiert ueber der Seite, damit sie das Ende ueberleben.
   Finten (Daten je Absicht in kaempfe.json, immer gleich, damit man sie lernt; nur auf der Leiste):
     zoegern    {bei, halt}      Marker bleibt bei bei*ziel halt ms stehen (hooks.halten: Taunt / Knurren), dann der Schlag
     taeuschung {bei, zurueck}   Marker laeuft bis bei*ziel, der Gegner zuckt, der Marker springt auf zurueck*ziel zurueck
                                 (weiter vorn, nie an den Anfang); der Kampf kuendigt sie im Tell mit einem Klang an
     kette      {abstaende}      2-4 Schlaege hintereinander; die ersten brauchen nur "gut", nur der letzte hat die
                                 perfekte Zone und entscheidet das Ergebnis. Der erste Schlag kommt nie vor ERSTER_MIN. */
(function(global){
  "use strict";
  const TELL = 1000;                   // Duc 03.11.2026: 1 s Leuchten, damit man es auch bei einem Ruckler sieht
  const AUSWEICH_FAKTOR = 1.5;         // Ausweichen ist leichter als Parieren: Fenster = 1,5 x gutes Paradefenster
  const AUSWEICH_TEMPO = 0.6;          // der Kreis ist deutlich schneller als die Leiste (Duc 03.11.2026: 0,8 war zu leicht), Fenster gleich
  const ERSTER_MIN = 900;              // Kette: der erste Schlag fruehestens nach 900 ms (Ruckler am Anfang auf langsamen PCs)
  const reduziert = () => global.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Zeitplan des Markers: Stuecke {t0, t1, x0, x1} und die Schlaege {t, x}
  function plan(spec){
    const Z = Math.max(55, Math.min(85, spec.ziel || 75)), L = spec.lauf || 1500, f = spec.finte || {};
    let v = Z / L;
    const st = [], schlaege = [];
    if (f.art === "zoegern"){
      const b = f.bei || 0.7, h = f.halt || 500;
      st.push({t0: 0, t1: b * L, x0: 0, x1: b * Z}, {t0: b * L, t1: b * L + h, x0: b * Z, x1: b * Z, halt: true},
              {t0: b * L + h, t1: L + h, x0: b * Z, x1: Z});
      schlaege.push({t: L + h, x: Z});
    } else if (f.art === "taeuschung"){
      const b = f.bei || 0.8, r = Math.min(f.zurueck || 0.55, b - 0.1), tf = b * L;
      st.push({t0: 0, t1: tf, x0: 0, x1: b * Z, finte: true}, {t0: tf, t1: tf + (1 - r) * L, x0: r * Z, x1: Z});
      schlaege.push({t: tf + (1 - r) * L, x: Z});
    } else if (f.art === "kette"){
      const ab = (f.abstaende || [450]).slice(0, 3), summe = ab.reduce((a, b) => a + b, 0);
      const erster = Math.max(L - summe, ERSTER_MIN * L / 1500, ERSTER_MIN), ende = erster + summe;
      v = Math.min(Z / L, 92 / ende);                       // die letzte Zone bleibt auf der Leiste
      st.push({t0: 0, t1: ende, x0: 0, x1: ende * v});
      let t = erster;
      schlaege.push({t, x: t * v});
      ab.forEach(a => { t += a; schlaege.push({t, x: t * v}); });
    } else {
      st.push({t0: 0, t1: L, x0: 0, x1: Z});
      schlaege.push({t: L, x: Z});
    }
    return {Z, L, v, st, schlaege, ende: schlaege[schlaege.length - 1].t};
  }
  function lage(p, t){
    for (const s of p.st) if (t <= s.t1) return s.t1 === s.t0 ? s.x0 : s.x0 + (s.x1 - s.x0) * Math.max(0, t - s.t0) / (s.t1 - s.t0);
    return p.schlaege[p.schlaege.length - 1].x + (t - p.ende) * p.v;
  }

  // Kreis: Radius in px, schrumpft linear und trifft beim Schlag genau den Zielring
  const R_ZIEL = 46, R_START = 150;
  const radius = (t, L) => R_ZIEL + (R_START - R_ZIEL) * (1 - t / L);

  function start(host, spec, hooks){
    hooks = hooks || {};
    const art = spec.art || "parieren", kreis = art !== "parieren";
    const p = kreis ? plan({ziel: spec.ziel, lauf: (spec.lauf || 1500) * AUSWEICH_TEMPO}) : plan(spec);
    const fe = spec.fenster || {gut: 211, perf: 87};
    const dodgeW = fe.gut * AUSWEICH_FAKTOR;               // ganze Breite in ms
    const letzte = p.schlaege.length - 1;
    const zone = (x, ms, kl) => `<i class="${kl}" style="left:${x - ms * p.v / 2}%;width:${ms * p.v}%"></i>`;
    const ring = (ms, kl) => { const a = radius(-ms / 2, p.L), b = radius(ms / 2, p.L);   // Band zwischen zwei Radien
      return `<i class="${kl}" style="width:${2 * a}px;height:${2 * a}px;border-width:${a - b}px"></i>`; };
    const probe = kreis
      ? `<div class="qte-kreis">${ring(dodgeW, "k-aus")}${art === "wahl" ? ring(fe.perf, "k-perf") : ""}<i class="k-ziel"></i><b class="k-lauf"></b></div>`
      : `<div class="qte-leiste">${hinweis()}${p.schlaege.map((s, i) => zone(s.x, fe.gut, "z-gut") + (i === letzte ? zone(s.x, fe.perf, "z-perf") : "")).join("")}<b class="qte-marker"></b></div>`;
    // Ab dem zweiten Mal (Duc 03.11.2026): eine leichte Markierung, wo der Strich stehen bleibt bzw. wo der Gegner zuckt
    function hinweis(){
      const s = spec.bekannt && p.st.find(x => x.halt || x.finte);
      return s ? `<i class="z-hinweis" style="left:${s.halt ? s.x0 : s.x1}%"></i>` : "";
    }
    const serie = spec.serie_max ? `<span class="qte-serie" title="Perfect parries in a row">${Array.from({length: spec.serie_max},
      (_, i) => `<i class="${i < (spec.serie || 0) ? "an" : ""}"></i>`).join("")}</span>` : "";
    const tasten = (art === "wahl" ? `<span class="taste">D</span> dodge <span class="taste">Space</span> parry`
      : art === "ausweichen" ? `<span class="taste">D</span> dodge` : `<span class="taste">Space</span> parry`) + serie;
    const el = document.createElement("div");
    el.className = "qte qte-" + art;
    el.innerHTML = `<div class="qte-name">${spec.name ? String(spec.name).replace(/[&<>"]/g, "") : ""}</div>${probe}<div class="qte-tasten">${tasten}</div>`;
    host.appendChild(el);
    const marker = el.querySelector(".qte-marker, .k-lauf"), timer = [];
    let raf = 0, t0 = null, offen = 0, fertig = false, frueh = false;
    const zeit = () => performance.now() - t0;
    // Ring und Hinweis liegen fixiert ueber der Seite: das Probe-Fenster verschwindet mit dem Ende, sie nicht
    function oben(kl, quelle, text, ms){
      if (!quelle) return;
      const r = quelle.getBoundingClientRect(), d = document.createElement("div");
      d.className = kl; if (text) d.textContent = text;
      d.style.left = (r.left + r.width / 2) + "px"; d.style.top = (text ? r.bottom + 30 : r.top + r.height / 2) + "px";
      document.body.appendChild(d); setTimeout(() => d.remove(), ms);
    }
    function ende(erg){
      if (fertig) return; fertig = true;
      timer.forEach(clearTimeout); cancelAnimationFrame(raf);
      if (erg === "perfekt"){
        oben("qte-burst", el.querySelector(".z-perf, .k-perf, .k-ziel"), "", 450);
        const punkt = el.querySelector(".qte-serie i:not(.an)"); if (punkt) punkt.classList.add("an", "neu");
      } else if (erg === "verfehlt" && !kreis) oben("qte-zeitpunkt", el.querySelector(".qte-leiste"), frueh ? "Too early" : "Too late", 1100);
      if (hooks.tell) hooks.tell(false);
      if (hooks.ende) hooks.ende(erg);
    }
    function werten(erg){                                 // ein Schlag ist entschieden; in der Kette zaehlt der letzte
      if (erg === "verfehlt") return ende("verfehlt");
      if (offen < letzte){                                // Kettentreffer: die Zone pulst hell, ein leiser Klang (hooks.treffer)
        el.querySelectorAll(".qte-leiste .z-gut")[offen]?.classList.add("getroffen");
        if (hooks.treffer) hooks.treffer(offen);
      }
      if (offen++ >= letzte) ende(erg);
    }
    function malen(){
      if (fertig) return;
      const t = zeit();
      if (kreis){ const r = Math.max(8, radius(t, p.L)); marker.style.width = marker.style.height = 2 * r + "px";
        marker.style.opacity = t > p.L ? Math.max(0, 1 - (t - p.L) / 250) : 1; }
      else marker.style.left = Math.min(100, lage(p, t)) + "%";
      raf = requestAnimationFrame(malen);
    }
    if (hooks.tell) hooks.tell(true);
    el.classList.add("tell");
    timer.push(setTimeout(() => {
      el.classList.remove("tell"); el.classList.add("los");
      t0 = performance.now();
      raf = requestAnimationFrame(malen);
      p.st.filter(s => s.finte).forEach(s => timer.push(setTimeout(() => { if (!fertig && hooks.finte) hooks.finte(); }, s.t1)));
      p.st.filter(s => s.halt).forEach(s => timer.push(setTimeout(() => { if (!fertig && hooks.halten) hooks.halten(); }, s.t0)));
      p.schlaege.forEach((s, i) => {
        timer.push(setTimeout(() => { if (!fertig && hooks.schlag) hooks.schlag(i, i === letzte); }, s.t));
        const spaet = (kreis ? dodgeW : fe.gut) / 2 + 80;
        timer.push(setTimeout(() => { if (!fertig && offen === i) ende("verfehlt"); }, s.t + spaet));
      });
    }, (spec.tell || TELL) * (reduziert() ? 0.5 : 1)));
    return {
      druck(){                                           // Leertaste / Klick: parieren (im Kreis nur der perfekte Ring)
        if (t0 === null || fertig || art === "ausweichen") return;
        const roh = zeit() - p.schlaege[offen].t, dt = Math.abs(roh);
        frueh = roh < 0;
        if (kreis) return werten(dt <= fe.perf / 2 ? "perfekt" : "verfehlt");
        werten(dt <= fe.perf / 2 && offen === letzte ? "perfekt" : dt <= fe.gut / 2 ? "gut" : "verfehlt");
      },
      ausweichen(){                                      // D: ausweichen (Kreis)
        if (t0 === null || fertig || !kreis) return;
        werten(Math.abs(zeit() - p.schlaege[offen].t) <= dodgeW / 2 ? "ausweichen" : "verfehlt");
      },
      stop(){ fertig = true; timer.forEach(clearTimeout); cancelAnimationFrame(raf); el.remove(); },
      plan: p, el
    };
  }
  global.EdenQTE = {start, plan, TELL, AUSWEICH_FAKTOR, AUSWEICH_TEMPO, ERSTER_MIN};
})(window);
