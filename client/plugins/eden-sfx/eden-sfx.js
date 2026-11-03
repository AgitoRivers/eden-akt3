// Eden SFX (18.10.2026) - einmalige Sound-Effekte, vorab erzeugt (module/<modul>/sfx, Katalog aus /api/stand).
// Erkennt die meisten Anlaesse selbst am Zustandswechsel (Geld, Vertrauen, Handy, Missionen, Tag, Meldung); der Server
// meldet nur Story-Szenen und Events (V.sfx.hinweis). Wuerfel, Kauf-Art, Vorliebe und abgelehnte Aktionen
// ("nicht_moeglich") ruft index.html ausdruecklich auf.
// Nur Darstellung: aendert nichts am Spielstand und verbraucht keinen Spielzufall.
(() => {
    "use strict";
    const read = (key, fallback) => { try { return localStorage.getItem(key) ?? fallback; } catch { return fallback; } };
    const save = (key, value) => { try { localStorage.setItem(key, value); } catch {} };
    let enabled = read("eden_sfx_enabled", "1") === "1";
    let volume = Math.max(0, Math.min(1, Number(read("eden_sfx_volume", "0.6")) || 0));
    let katalog = {}, unlocked = false, prev = null, letzteAktion = null;
    const zuletzt = {}, laufend = new Set();
    // Klick und Menue-Reiter ohne Verzoegerung (27.10.2026): vorab dekodiert, Start beim Druecken statt beim Loslassen
    const SCHNELL = ["ui_klick", "menue_tab"];
    let ctx = null;
    const puffer = {};
    function vorladen() {
        if (!ctx) { try { ctx = new (window.AudioContext || window.webkitAudioContext)(); } catch { return; } }
        for (const id of SCHNELL) {
            const urls = katalog[id];
            if (!urls || !urls.length || puffer[id]) continue;
            puffer[id] = [];
            urls.forEach(u => fetch(u).then(r => r.arrayBuffer()).then(b => ctx.decodeAudioData(b))
                .then(buf => puffer[id].push(buf)).catch(() => {}));
        }
    }
    function schnell(id) {
        const liste = puffer[id];
        if (!enabled || !unlocked || !ctx || !liste || !liste.length || !volume) return play(id);
        if (ctx.state === "suspended") ctx.resume();
        const src = ctx.createBufferSource(), g = ctx.createGain();
        src.buffer = liste[Math.floor(Math.random() * liste.length)];
        g.gain.value = volume;
        src.connect(g).connect(ctx.destination);
        src.start();
    }

    // opt (03.11.2026, Kampf): {leise: 0..1 Anteil der Lautstaerke, hoehe: Abspieltempo, 1.06 = etwa ein Halbton hoeher}
    function play(id, verzoegerung = 0, opt = null) {
        const urls = katalog[id];
        if (!enabled || !unlocked || !urls || !urls.length || !volume) return;
        if (verzoegerung) { setTimeout(() => play(id, 0, opt), verzoegerung); return; }
        const jetzt = performance.now();
        if (jetzt - (zuletzt[id] || 0) < 150 || laufend.size >= 6) return;    // kein Doppelklick-Stapel
        zuletzt[id] = jetzt;
        const a = new Audio(urls[Math.floor(Math.random() * urls.length)]);
        a.volume = volume * (opt && opt.leise != null ? opt.leise : 1);
        if (opt && opt.hoehe){ a.preservesPitch = false; a.playbackRate = opt.hoehe; }
        laufend.add(a);
        const weg = () => laufend.delete(a);
        a.addEventListener("ended", weg); a.addEventListener("error", weg);
        a.play().catch(weg);
    }
    // Mehrere Anlaesse in einem Zustandswechsel: hoechstens zwei, leicht versetzt, wichtigster zuerst.
    function spielen(liste) {
        liste.filter((id, i) => id && liste.indexOf(id) === i).slice(0, 2).forEach((id, i) => play(id, i * 380));
    }

    function schnappschuss(V) {
        const z = V.z, h = z.handel || {};
        return {
            run: z.id, tag: z.tag, phase: z.phase, konto: h.konto ?? null,
            begehren: Object.fromEntries((z.werte || []).map(w => [w.id, (w.begehren || 0) + (w.b_anteil || 0)])),
            codex: (z.codex || []).length,
            ereignis: z.status === "ereignis" && z.ereignis ? z.tag + "|" + z.phase + "|" + (z.ereignis.titel || z.ereignis.id || "") : null,
            besitz: (h.inventar_info || []).reduce((s, w) => s + (w.n || 1), 0) + (h.tasche || []).length,   // Stapel zaehlen je Stueck
            ungelesen: (z.handy || []).filter(f => !f.gelesen).length,
            vertrauen: Object.fromEntries((z.werte || []).map(w => [w.id, (w.vertrauen || 0) + (w.v_anteil || 0)])),
            jobs: new Set((h.jobs || []).map(j => j.id)),
            ergebnis: z.job_ergebnis ? z.job_ergebnis.nr + "|" + z.job_ergebnis.id : null,
            meldung: (z.meldungen || []).length ? JSON.stringify(z.meldungen[z.meldungen.length - 1]) : null,
            hinweis: (V.sfx && V.sfx.hinweis) || null,
            ev_id: z.ereignis ? z.ereignis.id : null, ev_art: z.ereignis ? z.ereignis.art : null,
            fund: z.ereignis && z.ereignis.fund ? z.ereignis.id : null,
            spur: z.ereignis && z.ereignis.spur ? z.ereignis.spur.stand : null,
            anruf: z.rast_anruf ? z.rast_anruf.id : null,
            auftraege: (z.journal || []).filter(j => j.status === "aktiv").length,
            schritte: (z.journal || []).reduce((n, j) => n + (j.schritte || []).filter(x => x.erledigt).length, 0),
            fertig: (z.journal || []).filter(j => j.status === "fertig").length,
            werkstatt: (w => w ? [...(w.waffen || []), ...(w.ruestungen || [])].reduce((n, x) => n + (x.stufe || 0), 0) : null)((z.kampf_profil || {}).werkstatt),
            waffen: (V.sfx && V.sfx.waffen) || 0,
            ergebnis_zeilen: z.ereignis && z.ereignis.ergebnis ? JSON.stringify(z.ereignis.ergebnis.zeilen || []) : null,
        };
    }

    // Ambience (27.10.2026): eine leise Schleife je Lage (Server: V.sfx.ambience), Ueberblendung 1,5 s
    const amb = {id: null, audio: null};
    function ambience(id) {
        const urls = id && katalog[id];
        if (!enabled || !unlocked) id = null;
        if (id === amb.id) { if (amb.audio) amb.audio.volume = Math.min(1, volume); return; }
        const alt = amb.audio;
        if (alt) { const t0 = performance.now(), v0 = alt.volume;
            const f = () => { const k = Math.min(1, (performance.now() - t0) / 1500); alt.volume = v0 * (1 - k);
                if (k < 1) requestAnimationFrame(f); else alt.pause(); }; f(); }
        amb.id = id; amb.audio = null;
        if (!id || !urls || !urls.length) return;
        const a = new Audio(urls[0]); a.loop = true; a.volume = 0;
        amb.audio = a;
        a.play().then(() => { const t0 = performance.now();
            const f = () => { if (amb.audio !== a) return; const k = Math.min(1, (performance.now() - t0) / 1500);
                a.volume = Math.min(1, volume) * k; if (k < 1) requestAnimationFrame(f); }; f(); }).catch(() => { amb.id = null; });
    }
    let letzteAmb = null;
    function observe(V) {
        katalog = (V && V.sfx && V.sfx.katalog) || katalog;
        vorladen();
        letzteAmb = (V && V.sfx && V.sfx.ambience) || null;
        ambience(letzteAmb);
        if (!V || !V.z) { prev = null; return; }
        const s = schnappschuss(V), p = prev;
        prev = s;
        if (!p || p.run !== s.run) return;                    // erster Blick / anderer Durchlauf: nichts nachholen
        const neu = [];
        // Story-Szene oder Event beginnt (Server-Hinweis), "nach" spielt, wenn die vorige Szene endet.
        const hk = s.hinweis && s.hinweis.key, pk = p.hinweis && p.hinweis.key;
        if (pk && pk !== hk && p.hinweis.nach) neu.push(p.hinweis.nach);
        if (hk && hk !== pk && s.hinweis.id) neu.push(s.hinweis.id);
        else if (s.ev_art === "ort" && s.ev_id !== p.ev_id) neu.push(s.fund && s.fund !== p.fund ? "fund" : "schritte_kies");
        else if (s.ereignis && s.ereignis !== p.ereignis)                                // Events ohne eigenen Story-Ton
            neu.push(s.ev_art === "bordrat" ? "bordrat" : s.ev_art === "handy" ? (V.z.ereignis && V.z.ereignis.anruf_art === "video" && !V.z.ereignis.selfie && !(V.z.phase === "nacht" || /^0[0-5]:\d\d$/.test(V.z.ereignis.titel || "")) ? "anruf_klingeln" : "handy_nachricht") : String(s.ev_id).startsWith("bl_") ? null : (V.z.ereignis && V.z.ereignis.uebergang && !V.z.ereignis.ergebnis ? "szene_bruecke" : "ereignis_jingle"));   // Belagerung: kein Rock-Jingle; mit Zwischenkarte kommt der Jingle erst beim Weiter
        if (s.anruf && s.anruf !== p.anruf) neu.push("anruf_klingeln");
        // In der Grotte ist die Uhr die Ebbe (29.10.2026): dort drueckt die Flut herein statt einer tickenden Uhr
        if (s.spur !== null && p.spur !== null && s.spur < p.spur)
            neu.push(String(letzteAmb || "").startsWith("amb_grotte") ? "flut_steigt" : "spur_uhr");
        if (s.fertig > p.fertig) neu.push("auftrag_siegel");
        else if (s.auftraege > p.auftraege || s.schritte > p.schritte) neu.push("auftrag_feder");
        if (s.waffen > p.waffen) neu.push("neue_waffe");
        if (s.werkstatt !== null && p.werkstatt !== null && s.werkstatt > p.werkstatt) neu.push("werkstatt_fertig");          // Rosis Stueck ueber Nacht fertig
        const text = (s.meldung !== p.meldung ? s.meldung || "" : "") + (s.ergebnis_zeilen !== p.ergebnis_zeilen ? s.ergebnis_zeilen || "" : "");
        if (text.includes("💔")) neu.push("versprechen_gebrochen");
        else if (text.includes("🤝")) neu.push("versprechen");
        if (V.sfx && V.sfx.still) { /* Belagerung (Duc 01.11.2026): keine Tageszeit-Melodien mitten im Krieg */ }
        else if (s.tag > p.tag) neu.push(katalog.tag_karte ? "tag_karte" : katalog.tag_ende ? "tag_ende" : "tag_beginnt");
        else if (s.phase !== p.phase) neu.push(katalog["phase_" + s.phase] ? "phase_" + s.phase : "phase_wechsel");  // je Tageszeit eigene Melodie
        if (s.codex > p.codex) neu.push("hinweis_gefunden");
        if (s.ergebnis && s.ergebnis !== p.ergebnis) neu.push(V.z.job_ergebnis.ok ? "mission_erfolg" : "mission_fehlschlag");
        const aktion = letzteAktion;
        if (s.konto !== null && p.konto !== null && s.konto !== p.konto) {
            if (s.konto > p.konto) neu.push("geld_ein");
            else neu.push(aktion && aktion.aktion === "kaufen" && aktion.daten.laden === "lola" ? "lola_brutzeln" : "geld_aus");
        } else if (aktion && aktion.aktion === "geben" && s.meldung !== p.meldung) neu.push("geschenk");
        else if (aktion && aktion.aktion === "benutzen" && s.meldung !== p.meldung) neu.push("item_benutzen");
        else if (s.besitz > p.besitz) neu.push("item_erhalten");
        if (aktion && aktion.aktion === "kochen" && aktion.daten.fuer === "crew" && s.meldung !== p.meldung) neu.push("glaeser_anstossen");
        let lust = false;
        for (const [pid, b] of Object.entries(s.begehren)) if (pid in p.begehren && b > p.begehren[pid] + 1e-6) lust = true;
        if (lust) neu.push("begehren_plus");
        let rauf = false, runter = false;
        for (const [pid, w] of Object.entries(s.vertrauen)) {
            if (!(pid in p.vertrauen)) continue;
            if (w > p.vertrauen[pid] + 1e-6) rauf = true;
            if (w < p.vertrauen[pid] - 1e-6) runter = true;
        }
        if (rauf) neu.push("vertrauen_plus"); else if (runter) neu.push("vertrauen_minus");
        if ([...s.jobs].some(id => !p.jobs.has(id))) neu.push("mission_neu");
        if (s.ungelesen > p.ungelesen) neu.push(katalog.notification ? "notification" : "handy_nachricht");
        if (!neu.length && s.meldung && s.meldung !== p.meldung) neu.push("ui_meldung");
        if (neu.length) letzteAktion = null;
        spielen(neu);
    }

    // index.html: vor jeder Spieleraktion (Kauf bei Lola brutzelt, Teamessen klingt nach Glaesern).
    function aktion(name, daten) {
        letzteAktion = {aktion: name, daten: daten || {}};
        if (name === "kochen") play("kochen");                // sofort, der Wuerfel kommt danach
    }
    // index.html: rund um EdenDice.play - Rollen sofort, Ergebnis nach der Animation.
    function wurfStart(paket) { if (paket && paket.rolls && paket.rolls.length) play("wuerfel_rollen"); }
    function wurfEnde(paket) {
        const erg = ((paket && paket.rolls) || []).map(r => r.probe && r.probe.ergebnis).filter(Boolean);
        if (!erg.length) return;
        const e = erg.includes("kritisch") ? "kritisch" : erg.includes("patzer") ? "patzer" : erg[erg.length - 1];
        play("wuerfel_" + e);
    }

    // Klick auf Knoepfe (ui_klick ist noch offen: es wechselt zwischen allen Varianten).
    document.addEventListener("pointerdown", e => {
        if (e.button !== 0) return;
        const b = e.target.closest && e.target.closest("button, [role=button]");
        if (!b || b.disabled) return;
        unlocked = true;
        schnell(b.closest(".em-tab, .em-tabs button, .hreiter button") && katalog.menue_tab ? "menue_tab" : "ui_klick");
    }, true);
    const freigeben = () => { const war = unlocked; unlocked = true; if (!war) ambience(letzteAmb); };              // Browser spielen Ton erst nach einer Bedienung
    document.addEventListener("pointerdown", freigeben, {capture: true});
    document.addEventListener("keydown", freigeben, {capture: true});

    // Einstellungen im Menue (wie die Musik): an/aus + Lautstaerke, nur lokal gemerkt.
    const box = document.createElement("div"); box.className = "eden-music eden-sfx";
    box.setAttribute("role", "group"); box.setAttribute("aria-label", "Sound effects");
    const toggle = document.createElement("button"); toggle.type = "button";
    const slider = document.createElement("input"); slider.type = "range";
    slider.min = "0"; slider.max = "1"; slider.step = "0.01"; slider.value = volume;
    slider.setAttribute("aria-label", "Effects volume");
    box.append(toggle, slider); box.hidden = true; document.body.append(box);
    const label = () => { toggle.textContent = enabled ? "Effects on" : "Effects off"; toggle.setAttribute("aria-pressed", String(enabled)); };
    toggle.onclick = () => { enabled = !enabled; save("eden_sfx_enabled", enabled ? "1" : "0"); label(); ambience(letzteAmb); };
    slider.oninput = () => { volume = Number(slider.value); save("eden_sfx_volume", String(volume)); ambience(letzteAmb); };
    slider.onchange = () => play("ui_meldung");               // Probe nach dem Loslassen
    function mountSettings(host) { box.hidden = !host; if (host && box.parentNode !== host) host.append(box); }
    label();

    window.EdenSfx = {observe, play, aktion, wurfStart, wurfEnde, mountSettings};
    window.dispatchEvent(new Event("eden-sfx-ready"));
})();
