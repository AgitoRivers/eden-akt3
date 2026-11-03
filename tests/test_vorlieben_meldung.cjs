// Lavendel-Meldung "Preference discovered" (Spieltest Duc 29.10.2026): nie in Szene/Kampf/Expedition, mehrere = EINE Meldung.
const fs = require('node:fs'), vm = require('node:vm'), assert = require('node:assert/strict');
const html = fs.readFileSync(__dirname + '/../client/index.html', 'utf8');
const von = html.indexOf('const VMQ = []'), bis = html.indexOf('function vmOeffnen');
assert(von > 0 && bis > von, 'Meldungs-Code in index.html gefunden');
const box = {innerHTML: ''}, posts = [], timer = [];
const ctx = {
  $: () => box, esc: s => String(s), uiIc: () => '', V: {z: null}, window: {},
  fetch: (url, o) => { posts.push([url, JSON.parse(o.body)]); return Promise.resolve(); },
  setTimeout: fn => { timer.push(fn); return timer.length; }, clearTimeout: () => {}, Date,
};
vm.runInNewContext(html.slice(von, bis) + '\nthis.vmPruefen = vmPruefen; this.vmZu = vmZu; this.vm = () => VM_AKTIV;', ctx);
const e = (figur, item) => ({figur, item, name: figur[0].toUpperCase() + figur.slice(1), label: item, reaktion: 'mag'});
const stand = (status, neu, extra) => Object.assign({status, vorlieben: {neu}}, extra || {});

// 1) Mitten in einer Szene: nichts zeigen, nichts als gemeldet markieren
let z = stand('szene', [e('lola', 'cannoli'), e('alva', 'rum'), e('petru', 'tools')]);
ctx.V.z = z; ctx.vmPruefen(z);
assert.equal(ctx.vm(), null); assert.equal(box.innerHTML, ''); assert.equal(posts.length, 0);
// Kampf und laufende Expedition ebenso
for (const s of [stand('kampf', z.vorlieben.neu), stand('wahl', z.vorlieben.neu, {expedition: {id: 'grotte'}})]) {
  ctx.V.z = s; ctx.vmPruefen(s); assert.equal(ctx.vm(), null, s.status);
}
// 2) Danach (Wahl, keine Expedition): EINE gebuendelte Meldung, alle drei gemeldet
z = stand('wahl', z.vorlieben.neu); ctx.V.z = z; ctx.vmPruefen(z);
assert.equal(ctx.vm().buendel.length, 3);
assert.match(box.innerHTML, /3 new preferences/); assert.match(box.innerHTML, /Lola, Alva and Petru/);
assert.equal(posts.length, 1); assert.deepEqual(posts[0][1].schluessel, ['lola|cannoli', 'alva|rum', 'petru|tools']);
ctx.vmZu(); assert.equal(timer.length, 1);           // nur der Schliess-Timer, keine Folgemeldung
// 3) Einzelne neue Vorliebe: die gewohnte Einzelmeldung
z = stand('kabine', [e('lola', 'cannoli'), e('megan', 'tea')]); ctx.V.z = z; ctx.vmPruefen(z);
assert.equal(ctx.vm().figur, 'megan'); assert.match(box.innerHTML, /Preference discovered/); assert.match(box.innerHTML, /Megan likes tea/);
console.log('OK Vorlieben-Meldung: wartet bis nach Szene/Kampf/Expedition, buendelt mehrere');
