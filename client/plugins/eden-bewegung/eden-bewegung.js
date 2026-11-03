/* Eden: Bewegung und Uebergaenge (Duc 02.11.2026, docs/wiki/systeme/ui_stil.md Abschnitt 2b).
   Vier Mikro-Interaktionen im Stil der Buehnenkarten, alles ohne Eingriff in die Spiellogik:
   1. Stufe steigt: kurze Karte oben mit Ring, Pop und Klang (Vertrauen/Begehren je Figur).
   2. Wert steigt im Gespraech: Pille mit Zahl ("+2 Trust") steigt an der Figur auf und fliegt zur Beziehungskarte.
   3. Antwort gewaehlt: die Wahl bleibt kurz stehen und leuchtet, die anderen blenden aus, dann erst wird gesendet.
   4. Gefuehl wechselt: der Sprite blendet in 150 ms ueber statt hart zu springen.
   Bei "weniger Bewegung" (prefers-reduced-motion) gibt es nur die Information, ohne Animation. */
(function () {
  "use strict";
  const still = () => !!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
  let vorher = null, lauf = null;

  function schnappschuss(z) {
    const out = {};
    (z.werte || []).forEach(w => { out[w.id] = {name: w.name, vertrauen: w.vertrauen, begehren: w.begehren, va: w.v_anteil, ba: w.b_anteil, vp: w.v_punkte, bp: w.b_punkte}; });
    // Figuren auf der Buehne bringen ihre Punkte selbst mit, auch ohne Romanze (Jana, Megan ...)
    if (z.status === "szene" && z.szene) z.szene.buehne.forEach(f => { out[f.id] = Object.assign({name: f.name}, out[f.id], {vp: f.v_punkte, bp: f.b_punkte}); });
    return out;
  }

  // Trust = Smiley in Blau, Desire = Herz in Rot (--begehren, Duc 03.11.2026), wie die Punkte der Beziehungskarte (Duc 02.11.2026: keine technischen Etiketten)
  const IC = {vertrauen: "mood-good", begehren: "love"};
  const SATZ = {vertrauen: "trusts you more", begehren: "wants you more"};
  const icon = (achse, klasse) => window.EdenUI ? EdenUI.icon(IC[achse], klasse) : "";

  // 1. Stufe steigt
  function stufenKarte(name, achse, stufe) {
    let ebene = document.getElementById("bew-stufen");
    if (!ebene) { ebene = document.createElement("div"); ebene.id = "bew-stufen"; document.body.appendChild(ebene); }
    const k = document.createElement("div");
    k.className = "bew-stufe glas " + (achse === "begehren" ? "b" : "v");
    const punkte = [1, 2, 3, 4, 5].map(n => `<u class="${n < stufe ? "an" : n === stufe ? "an neu" : ""}"></u>`).join("");
    k.innerHTML = `<span class="bew-ring">${icon(achse, "")}</span><span class="bew-text"><b>${name}</b>`
      + `<span>${SATZ[achse]}</span><span class="bew-punkte">${punkte}</span></span>`;
    ebene.appendChild(k);
    if (window.EdenSfx) EdenSfx.play("level_up");
    setTimeout(() => k.classList.add("geht"), still() ? 2200 : 2800);
    setTimeout(() => k.remove(), 3400);
  }

  // 2. Wert steigt im Gespraech (UX-Paket 03.11.2026: mit Zahl). Die Pille steigt an der Figur auf und zeigt "+2 Trust",
  //    bleibt kurz stehen und fliegt dann zur Beziehungskarte. Weniger Bewegung: sie steht still an der Figur und blendet aus.
  function pilleFliegt(pid, achse, delta) {
    const fig = document.getElementById("fig-" + pid), ziel = document.getElementById("relkarte");
    if (!fig) return;
    const a = fig.getBoundingClientRect(), b = ziel ? ziel.getBoundingClientRect() : null;
    if (!a.width) return;
    const p = document.createElement("div");
    p.className = "bew-pille glas " + (achse === "begehren" ? "b" : "v") + (still() || !b || !b.width ? " still" : "");
    p.innerHTML = icon(achse, "") + `<b>${delta > 0 ? "+" + delta : "+"}</b><span>${achse === "begehren" ? "Desire" : "Trust"}</span>`;
    const x0 = a.left + a.width * 0.72, y0 = a.top + a.height * 0.3;     // neben dem Kopf, nie ueber dem Gesicht
    p.style.left = x0 + "px"; p.style.top = y0 + "px";
    if (b && b.width) {
      p.style.setProperty("--dx", (b.left + b.width / 2 - x0) + "px");
      p.style.setProperty("--dy", (b.top + b.height / 2 - y0) + "px");
    }
    document.body.appendChild(p);
    setTimeout(() => {
      p.remove();
      if (ziel && !p.classList.contains("still")) { ziel.classList.remove("bew-puls"); void ziel.offsetWidth; ziel.classList.add("bew-puls"); }
    }, 1900);
  }

  function observe(V) {
    const z = V && V.z;
    if (!z || !z.werte) { vorher = null; return; }
    const jetzt = schnappschuss(z), alt = vorher, gleicherLauf = lauf === z.id;
    vorher = jetzt; lauf = z.id;
    if (!alt || !gleicherLauf) return;
    const buehne = new Set(z.status === "szene" && z.szene ? z.szene.buehne.map(f => f.id) : []);
    Object.entries(jetzt).forEach(([pid, w]) => {
      const v = alt[pid];
      if (!v) return;
      [["vertrauen", "va", "vp"], ["begehren", "ba", "bp"]].forEach(([achse, anteil, pkt]) => {
        const delta = w[pkt] != null && v[pkt] != null ? w[pkt] - v[pkt] : 0;
        if (w[achse] != null && w[achse] > v[achse]) stufenKarte(w.name, achse, w[achse]);
        else if (buehne.has(pid) && (delta > 0 || (w[achse] != null && w[achse] === v[achse] && (w[anteil] || 0) > (v[anteil] || 0))))
          pilleFliegt(pid, achse, delta);
      });
    });
  }

  // 3. Antwort gewaehlt: Klick abfangen, Wahl zeigen, dann den echten Klick ausloesen
  const WAHL = ".wahlb, #chips .chip, .ev-opt, .option";
  document.addEventListener("click", ev => {
    const knopf = ev.target.closest && ev.target.closest(WAHL);
    if (!knopf || knopf.disabled || knopf.dataset.bewOk || still()) return;
    if (knopf.closest("#chips") && !knopf.closest("#chips").querySelector(".chip:nth-child(2)")) return;   // nur "Ideas": nichts zu waehlen
    ev.preventDefault(); ev.stopImmediatePropagation();
    const gruppe = knopf.parentElement;
    gruppe.classList.add("bew-gewaehlt");
    knopf.classList.add("bew-wahl");
    setTimeout(() => { knopf.dataset.bewOk = "1"; knopf.click(); delete knopf.dataset.bewOk; gruppe.classList.remove("bew-gewaehlt"); knopf.classList.remove("bew-wahl"); }, 260);
  }, true);

  // 4. Gefuehl wechselt: altes Bild als Geist darueber, der ausblendet
  function figurBeobachten() {
    const box = document.getElementById("figuren");
    if (!box) return;
    new MutationObserver(liste => liste.forEach(m => {
      const img = m.target;
      if (m.attributeName !== "src" || !m.oldValue || m.oldValue === img.getAttribute("src") || still() || img.classList.contains("weg")) return;
      const geist = img.cloneNode(false);
      geist.removeAttribute("id");
      geist.src = m.oldValue;
      geist.classList.add("bew-geist");
      img.parentElement.appendChild(geist);
      requestAnimationFrame(() => requestAnimationFrame(() => geist.classList.add("aus")));
      setTimeout(() => geist.remove(), 260);
    })).observe(box, {subtree: true, attributes: true, attributeFilter: ["src"], attributeOldValue: true});
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", figurBeobachten); else figurBeobachten();

  window.EdenBewegung = {observe};
})();
