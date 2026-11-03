/* DOM-free player contract, timing anchors, cancellation, cache and latest approvals. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'..'),lab=path.join(root,'docs/effekt-auswahl/status-labor');
let fetches=0,fail=false,delay=null;
const sandbox={URL,fetch:async()=>{fetches++;if(delay)await delay;if(fail)return{ok:false,status:404};return{ok:true,arrayBuffer:async()=>new ArrayBuffer(8)}}};vm.createContext(sandbox);
for(const file of ['ton-ablaeufe.js','ton-abspieler.js'])vm.runInContext(fs.readFileSync(path.join(lab,file),'utf8'),sandbox);
const api=sandbox.EdenAttackSound,data=sandbox.EDEN_ATTACK_SOUND_CUES;
function ctx(){const c={currentTime:10,starts:[],stops:[],decode:0};c.createGain=()=>({context:c,connect(){},disconnect(){},gain:{value:1,cancelScheduledValues(){},setValueAtTime(){},linearRampToValueAtTime(){},setTargetAtTime(){}}});c.createBufferSource=()=>({connect(){},disconnect(){},playbackRate:{value:1},start(...args){c.starts.push(args)},stop(t){c.stops.push(t)}});c.decodeAudioData=async()=>{c.decode++;return{duration:12}};return c}
(async()=>{
 assert.equal(Object.keys(data.attacks).length,20);
 for(const [id,a]of Object.entries(data.attacks))for(const [v,l]of Object.entries(a.variants)){
  const plan=api.resolve({attack:id,variant:Number(v)});assert(plan.events.length>0);assert(plan.events.every(e=>e.offset>=0&&e.offset<plan.duration));
  for(const e of l.events)if(e.anchor==='hit')assert(Math.abs(e.offset-(l.hits[e.hit_index===-1?l.hits.length-1:e.hit_index]+e.delta))<1e-5);
 }
 for(const id of ['doubleSlash','vendetta'])for(const v of [0,1,2])assert.deepEqual(Array.from(api.resolve({attack:id,variant:v}).events.filter(e=>e.sound_id.startsWith('compact_hit_')),e=>e.sound_id),['compact_hit_A','compact_hit_D']);
 for(const id of ['scirocco','retour','furia','vulcano'])assert(api.resolve({attack:id}).events.some(e=>e.sound_id==='afterburn'));
 for(const id of ['wind','calm','reticle','beam','balm','westWind','awaken','archangel'])assert(!api.resolve({attack:id}).events.some(e=>['heavy_hit','compact_hit_A','compact_hit_D'].includes(e.sound_id)));
 const rescue=api.resolve({attack:'archangel',mode:'rescue'});assert.equal(rescue.duration,1.25);assert(rescue.events.every(e=>e.sound_id!=='guardian_unfold'&&e.offset<1.25));
 const l=data.attacks.mistral.variants[0],moved={launch:l.launch+.7,hits:l.hits.map(h=>h+.7),duration:l.duration+.7};
 const first=api.resolve({attack:'mistral'}).events.find(e=>e.sound_id==='compact_hit_A'),next=api.resolve({attack:'mistral',timeline:moved}).events.find(e=>e.sound_id==='compact_hit_A');assert(Math.abs(next.offset-first.offset-.7)<1e-6);
 const vul=api.resolve({attack:'vulcano',timeline:{launch:3.8,hits:[4.18,4.66,5.14,5.62,6.1],duration:9.65}});assert.equal(vul.events.filter(e=>e.sound_id==='heavy_hit').length,5);assert(Math.abs(vul.events.find(e=>e.sound_id==='afterburn').offset-6.22)<1e-6);
 assert(api.resolve({attack:'furia',mode:'charge'}).events.every(e=>e.phase==='charge'));assert(api.resolve({attack:'furia',mode:'release'}).events.every(e=>e.phase!=='charge'));
 const c=ctx(),baseUrl='http://localhost/preview/';await api.preload({context:c,baseUrl,attack:'mistral'});const count=c.decode;await api.preload({context:c,baseUrl,attack:'mistral'});assert.equal(c.decode,count);
 const h=api.play({attack:'mistral',context:c,destination:c.createGain(),baseUrl,startAt:11});await h.ready;assert(c.starts.length>0);assert(c.starts.every(x=>x[0]>=11));h.stop();assert(c.stops.every(t=>t<=10.04));h.stop();
 let release;delay=new Promise(r=>release=r);const c2=ctx(),stopped=api.play({attack:'mistral',context:c2,destination:c2.createGain(),baseUrl});stopped.stop();release();await stopped.ready;assert.equal(c2.starts.length,0);delay=null;
 const c3=ctx();c3.currentTime=100;const expired=api.play({attack:'mistral',context:c3,destination:c3.createGain(),baseUrl,startAt:1});await expired.ready;assert.equal(c3.starts.length,0);
 fail=true;const c4=ctx(),broken=api.play({attack:'mistral',context:c4,destination:c4.createGain(),baseUrl});await assert.rejects(broken.ready,/404/);assert(broken.inspect().stopped);fail=false;
 const allow=JSON.parse(fs.readFileSync(path.join(root,'client/plugins/eden-skills/preview-files.json'),'utf8'));
 for(const [id,s]of Object.entries(data.sounds)){assert(allow.includes(s.file));const bytes=fs.readFileSync(path.join(lab,s.file));assert.equal(require('node:crypto').createHash('sha256').update(bytes).digest('hex'),s.sha256)}
 for(const f of ['ton-ablaeufe.js','ton-abspieler.js'])assert(allow.includes(f));
 console.log(JSON.stringify({attacks:20,variants:60,sounds:Object.keys(data.sounds).length,timing:'anchored',cache:'ok',stopBeforeDecode:'ok',skipFade:'ok',missingAudio:'handled',vulcanoStacks5:'ok',rescue:'1.25s',DOMRequired:false}));
})().catch(e=>{console.error(e);process.exit(1)});
