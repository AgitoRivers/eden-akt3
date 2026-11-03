/* Danzels Auftraege (Duc 30.10.2026, Wiki systeme/schneider.md): Bestellungen und Massstuecke im Laden Le Theatre Rouge.
   Liest z.schneider, sendet schneider_bringen {id}. Keine Aktion, keine Phase. */
window.EdenSchneider = (function(){
  const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}[c]));
  const karte = a => {
    const mat = a.material.map(m => `<span class="sn-mat${m.hat >= m.n ? " da" : ""}">${esc(m.label)} ${m.hat}/${m.n}</span>`).join("");
    const preis = a.lohn ? `<span class="sn-preis">Pays ${a.lohn} €</span>` : a.geld ? `<span class="sn-preis">Costs ${a.geld} €</span>` : "";
    const knopf = a.status === "laeuft" ? `<span class="sn-tisch">On the table. Ready tomorrow.</span>`
      : `<button class="mini" type="button" ${a.geht ? "" : "disabled"} onclick="EdenSchneider.bringen('${esc(a.id)}')">Bring the materials</button>`;
    return `<div class="sn-karte"><b>${esc(a.label)}</b><small>${esc(a.kunde)}</small><p>${esc(a.text)}</p>
      <div class="sn-zeile">${mat}${preis}</div><div class="sn-zeile">${knopf}</div></div>`;
  };
  function html(z){
    const s = z.schneider;
    if (!s) return `<p class="leer">Danzel has nothing for you yet.</p>`;
    const dorf = s.auftraege.length ? s.auftraege.map(karte).join("") : `<p class="leer">Nobody in the village has ordered anything right now.</p>`;
    const rest = s.muster_je - (s.fertig % s.muster_je);
    const fuss = s.muster > 0 ? `You have ${s.muster} pattern${s.muster === 1 ? "" : "s"} to use.`
      : `${rest} more finished order${rest === 1 ? "" : "s"} and Danzel will have a new pattern for you.`;
    const mass = s.massstuecke.length ? `<h3 class="orte-kopf">Made to measure</h3>${s.massstuecke.map(karte).join("")}` : "";
    return `<div class="sn-liste">${dorf}<p class="sn-fuss">${esc(fuss)}</p>${mass}</div>`;
  }
  return {html, bringen: id => senden("schneider_bringen", {id}, "…")};
})();
