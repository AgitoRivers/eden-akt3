/* DucErdeSaebel: pose choreography for the isolated effect lab.
 * Uses prepared copies only. Source PNGs and combat scripts are never modified. */
(()=>{'use strict';
const S=x=>{x=Math.max(0,Math.min(1,x));return x*x*(3-2*x)};
const poses=['idle','windup','attack','heavy_windup','heavy_attack','guard','hurt'],images={};
let anchors;
const heavy=new Set(['mistral','vendetta','blackSlash','tidal','scirocco','retour','furia','vulcano']);
const casting=new Set(['reticle','beam','rain']),self=new Set(['wind','calm','balm','westWind','awaken','archangel']);
function schedule(A){
 const {id,launch,hitOffsets,variant:v}=A,events=[];
 const add=(at,pose,blend=.085)=>events.push({at,pose,blend});
 add(0,'idle',0);
 if(id==='archangel'&&window.EdenHealer?.phase==='rettung'){add(0,'hurt',0);add(.12,'guard',.06);add(.55,'idle',.1);return events;}
 if(self.has(id)){add(.16,'guard',.13);add(launch+1.55,'idle',.17);return events;}
 if(id==='scirocco'){add(.16,'guard',.13);add(launch+.72,'idle',.18);return events;}
 if(window.EdenBerserker.supports(id)&&window.EdenBerserker.modeFor(id)==='charge'){add(.16,id==='furia'?'idle':'guard',.13);return events;}
 if(casting.has(id)){
  add(.16,'guard',.13);
  // Raised hand casts and holds the effect; no unrelated sword swing.
  add(launch+(id==='rain'?Math.max(...hitOffsets)+.75:1.4),'idle',.18);return events;
 }
 const wind=heavy.has(id)?'heavy_windup':'windup',hit=heavy.has(id)?'heavy_attack':'attack';
 add(.16,wind,.12);
 if(id==='retour'){add(launch-.99,'hurt',.065);add(launch-.49,wind,.12);}
 const first=launch+.38+hitOffsets[0];
 const release=id==='doubleSlash'||id==='vendetta'?first-.21:launch-.12;
 add(release,hit,.07);
 if(id==='doubleSlash'){
  add(first+.025,'windup',.045);add(launch+.38+hitOffsets[1]-.21,'heavy_attack',.055);
 }else if(id==='vendetta'){
  add(first+.045,'windup',.05);add(launch+.38+hitOffsets[1]-.21,'heavy_attack',.055);
 }
 if(id==='vulcano')for(let k=1;k<hitOffsets.length;k++){const contact=launch+.38+hitOffsets[k];add(contact-.39,wind,.065);add(contact-.21,hit,.065);}
 const last=launch+.38+Math.max(...hitOffsets);
 add(Math.max(release+.42,last+.23),'idle',.15);
 return events.sort((a,b)=>a.at-b.at);
}
function state(A){
 const events=schedule(A);let index=0;
 for(let i=1;i<events.length;i++)if(A.clock>=events[i].at)index=i;
 const current=events[index],previous=events[Math.max(0,index-1)],mix=current.blend?S((A.clock-current.at)/current.blend):1;
 return {pose:current.pose,from:previous.pose,mix,at:current.at};
}
function draw(A){
 const {g,clock,id,launch,age}=A,st=state(A);
 const swinging=['attack','heavy_attack'].includes(st.pose);
 const reach=swinging?Math.sin(Math.min(1,(clock-st.at)/.25)*Math.PI)*9:0;
 const preAge=clock-(launch-.95),stagger=id==='retour'&&A.shown&&A.previewMode!=='charge'&&preAge>0?Math.sin(preAge*29)*Math.exp(-preAge*6)*8:0;
 const x=180+reach+stagger,foot=495,visibility=window.EdenOmerta.visibility(A);
 g.save();g.globalAlpha=.5*visibility;g.fillStyle='#000';g.filter='blur(8px)';g.beginPath();g.ellipse(x,500,76,12,0,0,Math.PI*2);g.fill();g.restore();
 const paint=(pose,opacity)=>{
  if(opacity<.002)return;const image=images[pose],anchor=anchors[pose],scale=anchor.scale??.34,center=anchor.center_x??image.width/2;
  g.save();g.globalAlpha=opacity*visibility;g.translate(x,foot);if(anchor.mirror===true||(anchor.mirror===undefined&&pose==='guard'))g.scale(-1,1);g.drawImage(image,-center*scale,-anchor.foot*scale,image.width*scale,image.height*scale);if(A.shown&&(id==='doubleSlash'||id==='vendetta'))window.EdenDoppioCharge.draw(A,{pose,image,anchor,scale});if(A.shown&&id==='balm')window.EdenHealer.drawBody(A,{pose,image,anchor,scale});g.restore();
 };
 paint(st.from,1-st.mix);paint(st.pose,st.mix);
 // Low-amplitude breathing/gesture is carried by the pose; feet do not bob.
 // Draw a small local casting reflection without painting an artificial weapon.
 if(A.shown&&(casting.has(id)||self.has(id))){
  const env=S((clock-.45)/.5)*(1-S((age-1.1)/.6));
  A.glow(215,282,36,65,id==='beam'?'#f0db9b37':id==='rain'?'#93beef29':'#bdd9d72a',env*.12);
 }
 return st;
}
// Atomically swap a complete pose set; never reorient the already mirrored sources.
let catalog=null,assetBase='',activeSet=null,loadRevision=0;
async function loadSet(id){
 const item=catalog.sets.find(s=>s.id===id);if(!item)throw Error('Unbekanntes Duc-Set.');
 const revision=++loadRevision,prefix=assetBase+item.directory;
 const metadata=await fetch(prefix+'posen.json').then(r=>{if(!r.ok)throw Error('Duc-Posendaten fehlen.');return r.json()});
 const pairs=await Promise.all(poses.map(pose=>new Promise((resolve,reject)=>{const image=new Image();image.onload=()=>resolve([pose,image]);image.onerror=()=>reject(Error('Duc-Pose fehlt: '+pose));image.src=prefix+pose+'.webp'})));
 if(revision!==loadRevision)return false;
 anchors=metadata;Object.assign(images,Object.fromEntries(pairs));activeSet=item;
 document.dispatchEvent(new CustomEvent('eden-duc-sprite-changed',{detail:{id:item.id}}));return true;
}
async function load(base){
 assetBase=base;catalog=await fetch(base+'duc-varianten-v1/katalog.json').then(r=>{if(!r.ok)throw Error('Duc-Spritekatalog fehlt.');return r.json()});
 const look=document.querySelector('#player-look'),weapon=document.querySelector('#player-weapon');
 let initial='DucErdeSword';try{const saved=localStorage.getItem('eden-fx-duc-set-v1');if(catalog.sets.some(s=>s.id===saved))initial=saved}catch{}
 const selected=catalog.sets.find(s=>s.id===initial)||catalog.sets[0];
 if(look&&weapon){
  look.replaceChildren(...Object.entries(catalog.looks).map(([value,label])=>{const o=document.createElement('option');o.value=value;o.textContent=label;return o}));
  weapon.replaceChildren(...Object.entries(catalog.weapons).map(([value,label])=>{const o=document.createElement('option');o.value=value;o.textContent=label;return o}));
  look.value=selected.look;weapon.value=selected.weapon;
  async function apply(){
   const target=catalog.sets.find(s=>s.look===look.value&&s.weapon===weapon.value);if(!target)return;
   look.disabled=weapon.disabled=true;
   try{if(await loadSet(target.id))try{localStorage.setItem('eden-fx-duc-set-v1',target.id)}catch{}}
   catch(error){if(activeSet){look.value=activeSet.look;weapon.value=activeSet.weapon}const message=document.querySelector('#error');if(message)message.textContent=error.message}
   finally{look.disabled=weapon.disabled=false}
  }
  look.addEventListener('change',apply);weapon.addEventListener('change',apply);
 }
 await loadSet(selected.id);
}
window.EdenDucActor={state,schedule,load,loadSet,selection(){return activeSet?{id:activeSet.id,look:activeSet.look,weapon:activeSet.weapon,poses:[...poses]}:null},draw};

})();
