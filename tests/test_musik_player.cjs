const fs = require('node:fs'), vm = require('node:vm'), assert = require('node:assert/strict');
class Element {
 constructor(){this.children=[];this.listeners={};this.textContent='';}
 setAttribute(k,v){this[k]=v;} append(...items){this.children.push(...items);}
 addEventListener(k,fn){(this.listeners[k] ||= []).push(fn);}
 contains(el){return el===this || this.children.includes(el);}
 dispatch(k){for(const fn of this.listeners[k]||[])fn();}
}
const audios=[];
class Audio extends Element {
 constructor(){super();this.volume=1;this.paused=true;this.plays=0;audios.push(this);}
 play(){this.paused=false;this.plays++;return Promise.resolve();}
 pause(){this.paused=true;this.dispatch('pause');}
}
const document = new Element();document.body=new Element();document.createElement=()=>new Element();
let now=0, queue=new Map(),next=0;
const store=new Map();
const context={Audio,document,localStorage:{getItem:k=>store.get(k)??null,setItem:(k,v)=>store.set(k,v)},
 performance:{now:()=>now},requestAnimationFrame:fn=>{queue.set(++next,fn);return next;},cancelAnimationFrame:id=>queue.delete(id),Event:class{},window:{dispatchEvent(){}}};
vm.runInNewContext(fs.readFileSync(__dirname+'/../client/plugins/eden-music/eden-music.js','utf8'),context);
const player=context.window.EdenMusic, box=document.body.children[0],button=box.children[0];
const hint=id=>({stille:false,uebergang_ms:100,track:{id,url:'/musik/audio/'+id,gain:0.6,loop:true}});
const tick=async()=>{await Promise.resolve();now+=1000;const work=[...queue.values()];queue.clear();work.forEach(fn=>fn(now));await Promise.resolve();};
(async()=>{
 assert.equal(box.hidden,true);const settings=new Element();player.mountSettings(settings);assert.equal(box.hidden,false);assert(settings.children.includes(box));player.mountSettings(null);assert.equal(box.hidden,true);
 player.update(hint('one'));assert.equal(audios.reduce((n,a)=>n+a.plays,0),0);
 button.onclick();await tick();let live=audios.find(a=>!a.paused);
 assert(live);assert.equal(live.playbackRate,1);assert.equal(live.loop,false);
 const plays=audios.reduce((n,a)=>n+a.plays,0);player.update(hint('one'));await tick();assert.equal(audios.reduce((n,a)=>n+a.plays,0),plays);
 const normal=live.volume;const voice1=new Audio(),voice2=new Audio();player.registerSpeech(voice1);player.registerSpeech(voice2);
 voice1.dispatch('playing');assert(live.volume<normal);voice2.dispatch('playing');voice1.dispatch('ended');assert(live.volume<normal);voice2.dispatch('error');assert.equal(live.volume,normal);
 const playlist={slot:'deck',stille:false,uebergang_ms:100,playlist:['a','b','c'].map(id=>hint(id).track)};
 player.update(playlist);await tick();await tick();
 const seen=[];
 for(let i=0;i<7;i++){
   const current=audios.slice(0,2).find(a=>!a.paused);seen.push(current.src);
   player.update(playlist);assert.equal(current.src,seen.at(-1));
   current.paused=true;current.dispatch('ended');await tick();await tick();
 }
 assert.equal(new Set(seen.slice(0,3)).size,3);assert.equal(new Set(seen.slice(3,6)).size,3);
 for(let i=1;i<seen.length;i++)assert.notEqual(seen[i],seen[i-1]);
 player.update(hint('single'));await tick();await tick();let single=audios.slice(0,2).find(a=>!a.paused);single.paused=true;single.dispatch('ended');await tick();await tick();assert(audios.slice(0,2).some(a=>!a.paused&&a.src.endsWith('/single')));
 const sting={...hint('sting'),slot:'result',einmalig:true};
 player.update(sting);await tick();await tick();const st=audios.slice(0,2).find(a=>!a.paused);const beforeSting=st.plays;st.paused=true;st.dispatch('ended');await tick();await tick();
 assert(audios.slice(0,2).every(a=>a.paused));player.update(sting);await tick();assert.equal(st.plays,beforeSting);
 player.update(hint('two'));await tick();await tick();assert.equal(audios.slice(0,2).filter(a=>!a.paused).length,1);
 player.update({stille:true,uebergang_ms:0,track:null});await tick();assert(audios.slice(0,2).every(a=>a.paused&&a.volume===0));
 player.update(hint('three'));await tick();button.onclick();await tick();assert(audios.slice(0,2).every(a=>a.paused));assert.equal(store.get('eden_music_enabled'),'0');
 console.log('PASS: browser-player logic: interaction gate, playback, fixed speed, shuffle rounds without repeats, single-track replay, one-shot result without replay, redraw stability, overlapping speech ducking, track transition, blackout, mute persistence.');
})().catch(e=>{console.error(e);process.exitCode=1;});
