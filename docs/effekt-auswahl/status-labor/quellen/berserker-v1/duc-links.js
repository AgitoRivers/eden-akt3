/* DucErdeSaebel: pose choreography for the isolated effect lab.
 * Uses prepared copies only. Source PNGs and combat scripts are never modified. */
(()=>{'use strict';
const S=x=>{x=Math.max(0,Math.min(1,x));return x*x*(3-2*x)};
const poses=['idle','windup','attack','heavy_windup','heavy_attack','guard'],images={};
let anchors;
const heavy=new Set(['mistral','vendetta','blackSlash','tidal']);
const casting=new Set(['reticle','beam','rain']),self=new Set(['wind','calm']);
function schedule(A){
 const {id,launch,hitOffsets,variant:v}=A,events=[];
 const add=(at,pose,blend=.085)=>events.push({at,pose,blend});
 add(0,'idle',0);
 if(self.has(id)){add(.16,'guard',.13);add(launch+1.55,'idle',.17);return events;}
 if(casting.has(id)){
  add(.16,'guard',.13);
  // Raised hand casts and holds the effect; no unrelated sword swing.
  add(launch+(id==='rain'?Math.max(...hitOffsets)+.75:1.4),'idle',.18);return events;
 }
 const wind=heavy.has(id)?'heavy_windup':'windup',hit=heavy.has(id)?'heavy_attack':'attack';
 add(.16,wind,.12);
 const first=launch+.38+hitOffsets[0];
 const release=id==='doubleSlash'||id==='vendetta'?first-.21:launch-.12;
 add(release,hit,.07);
 if(id==='doubleSlash'){
  add(first+.025,'windup',.045);add(launch+.38+hitOffsets[1]-.21,'heavy_attack',.055);
 }else if(id==='vendetta'&&v===1){
  add(first+.045,'windup',.05);add(launch+.38+hitOffsets[1]-.21,'heavy_attack',.055);
 }
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
 const {g,clock,id,launch,age}=A,st=state(A),scale=.34;
 const swinging=['attack','heavy_attack'].includes(st.pose);
 const reach=swinging?Math.sin(Math.min(1,(clock-st.at)/.25)*Math.PI)*9:0;
 const x=180+reach,foot=495;
 g.save();g.globalAlpha=.5;g.fillStyle='#000';g.filter='blur(8px)';g.beginPath();g.ellipse(x,500,76,12,0,0,Math.PI*2);g.fill();g.restore();
 const paint=(pose,opacity)=>{
  if(opacity<.002)return;const image=images[pose],anchor=anchors[pose];
  g.save();g.globalAlpha=opacity;g.translate(x,foot);if(pose==='guard')g.scale(-1,1);g.drawImage(image,-image.width*scale/2,-anchor.foot*scale,image.width*scale,image.height*scale);if(A.shown&&(id==='doubleSlash'||id==='vendetta'))window.EdenDoppioCharge.draw(A,{pose,image,anchor,scale});g.restore();
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
window.EdenDucActor={state,schedule,async load(base){
 anchors=await fetch(base+'duc-links/posen.json?v=1').then(r=>{if(!r.ok)throw Error('Duc-Posendaten fehlen.');return r.json()});
 await Promise.all(poses.map(p=>new Promise((resolve,reject)=>{const image=new Image();image.onload=()=>{images[p]=image;resolve()};image.onerror=()=>reject(Error('Duc-Pose fehlt: '+p));image.src=base+'duc-links/'+p+'.webp?v=1'})));
},draw};
})();
