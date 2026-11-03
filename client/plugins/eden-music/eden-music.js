(() => {
    "use strict";
    const read = (key, fallback) => { try { return localStorage.getItem(key) ?? fallback; } catch { return fallback; } };
    const save = (key, value) => { try { localStorage.setItem(key, value); } catch {} };
    const channels = [new Audio(), new Audio()];
    const speech = new Set(), registered = new WeakSet();
    let enabled = read("eden_music_enabled", "1") === "1";
    let volume = Math.max(0, Math.min(1, Number(read("eden_music_volume", "0.35")) || 0));
    let target = null, currentId = null, active = 0, revision = 0, unlocked = false;
    let playlist = [], poolKey = "", bag = [], oneShot = false;
    let weights = [0, 0], gains = [1, 1], fade = null;
    const box = document.createElement("div"); box.className = "eden-music";
    box.setAttribute("role", "group"); box.setAttribute("aria-label", "Background music");
    const toggle = document.createElement("button"); toggle.type = "button";
    const slider = document.createElement("input"); slider.type = "range";
    slider.min = "0"; slider.max = "1"; slider.step = "0.01"; slider.value = volume;
    slider.setAttribute("aria-label", "Music volume");
    const credits = document.createElement("a"); credits.href = "/musik/credits";
    credits.target = "_blank"; credits.rel = "noopener"; credits.textContent = "Music & credits";
    box.append(toggle, slider, credits); box.hidden = true; document.body.append(box);
    function label(error = false) {
        toggle.textContent = error ? "Start music" : enabled ? "Music on" : "Music off";
        toggle.setAttribute("aria-pressed", String(enabled));
        box.title = target?.title || "Music for this scene";
    }
    function levels() {
        const duck = speech.size ? 0.28 : 1;
        channels.forEach((audio, i) => { audio.volume = Math.max(0, Math.min(1, weights[i] * gains[i] * volume * duck)); });
    }
    function transition(nextWeights, ms) {
        if (fade) cancelAnimationFrame(fade);
        const from = [...weights], start = performance.now();
        const frame = now => {
            const p = ms ? Math.min(1, (now - start) / ms) : 1;
            weights = from.map((v, i) => v + (nextWeights[i] - v) * p); levels();
            if (p < 1) fade = requestAnimationFrame(frame);
            else { fade = null; channels.forEach((audio, i) => { if (!weights[i]) audio.pause(); }); }
        };
        frame(start);
    }
    async function synchronize(ms = 1800) {
        if (!enabled || !target) {
            revision++; currentId = null; transition([0, 0], ms); label(); return;
        }
        if (target.id === currentId) { label(); return; }
        if (!unlocked) { label(true); return; }
        const ticket = ++revision, next = 1 - active, audio = channels[next], track = target;
        audio.pause(); audio.src = track.url; audio.loop = false;
        audio.playbackRate = audio.defaultPlaybackRate = 1;
        weights[next] = 0; gains[next] = track.gain ?? 1; levels();
        try {
            await audio.play();
            if (ticket !== revision) return;
            active = next; currentId = track.id;
            transition(next === 0 ? [1, 0] : [0, 1], ms); label();
        } catch {
            if (ticket === revision) { currentId = null; label(true); }
        }
    }
    function pickNext() {
        if (!bag.length) {
            bag = [...playlist];
            for (let i = bag.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [bag[i], bag[j]] = [bag[j], bag[i]];
            }
            if (bag.length > 1 && bag[0].id === currentId) {
                [bag[0], bag[1]] = [bag[1], bag[0]];
            }
        }
        target = bag.shift() || null;
    }
    channels.forEach((audio, index) => audio.addEventListener("ended", () => {
        if (index !== active || !enabled || !playlist.length || !currentId) return;
        if (oneShot) { target = null; currentId = null; transition([0, 0], 300); return; }
        pickNext(); currentId = null; synchronize(900);
    }));
    let serverHint = null, override = null;    // override: kurzer Vorrang-Track, z. B. Gestaendnis in der Anhoerung
    function update(hint) { serverHint = hint; apply(override || hint); }
    function vorrang(hint) { override = hint || null; apply(override || serverHint); }
    function apply(hint) {
        const next = hint && !hint.stille ? (hint.playlist?.length ? hint.playlist : hint.track ? [hint.track] : []) : [];
        const key = next.length ? `${hint.slot || ""}|${next.map(track => track.id).sort().join("|")}` : "";
        if (key === poolKey) {
            if (!next.length && hint?.uebergang_ms === 0) synchronize(0);
            return;
        }
        poolKey = key; playlist = next; bag = []; oneShot = Boolean(hint?.einmalig);
        pickNext();
        synchronize(hint?.uebergang_ms ?? 1800);
    }
    function registerSpeech(audio) {
        if (registered.has(audio)) return audio;
        registered.add(audio);
        audio.addEventListener("playing", () => { speech.add(audio); levels(); });
        for (const event of ["pause", "ended", "error", "emptied"]) {
            audio.addEventListener(event, () => { speech.delete(audio); levels(); });
        }
        return audio;
    }
    document.addEventListener("pointerdown", event => {
        if (!unlocked && !box.contains(event.target)) { unlocked = true; synchronize(); }
    }, {capture: true});
    document.addEventListener("keydown", () => {
        if (!unlocked) { unlocked = true; synchronize(); }
    }, {capture: true});
    toggle.onclick = () => {
        unlocked = true;
        if (toggle.textContent === "Start music") enabled = true;
        else enabled = !enabled;
        save("eden_music_enabled", enabled ? "1" : "0"); synchronize(300);
    };
    slider.oninput = () => { volume = Number(slider.value); save("eden_music_volume", String(volume)); levels(); };
    function mountSettings(host) {
        box.hidden = !host;
        if (host) host.append(box);
    }
    window.EdenMusic = {update, vorrang, registerSpeech, mountSettings}; label();
    window.dispatchEvent(new Event("eden-music-ready"));
})();
