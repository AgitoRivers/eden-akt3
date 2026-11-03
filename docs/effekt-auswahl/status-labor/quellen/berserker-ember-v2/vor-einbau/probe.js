/* Isolated visual study. No game requests, no saves, no audio. */
(()=>{'use strict';
const $=s=>document.querySelector(s),c=$('#scene'),g=c.getContext('2d'),W=960,H=600,PI=Math.PI;
const clamp=x=>Math.max(0,Math.min(1,x)),smooth=x=>{x=clamp(x);return x*x*(3-2*x)},mix=(a,b,p)=>a+(b-a)*p;
const pulse=(t,c,w)=>Math.exp(-Math.pow((t-c)/w,2)),endFade=(t,a,b)=>smooth((t-a)/.12)*(1-smooth((t-b)/.7));
const library=window.EdenAttackLibrary;let attack='wave',variant=0,crops={};
const images={},load=(name,file)=>new Promise((resolve,reject)=>{const i=new Image();i.onload=()=>{images[name]=i;resolve()};i.onerror=()=>reject(Error('Bild fehlt: '+file));i.src=file});
const layer=document.createElement('canvas');layer.width=W;layer.height=H;const q=layer.getContext('2d');
const flow=document.createElement('canvas');flow.width=256;flow.height=128;const fg=flow.getContext('2d'),pixels=fg.createImageData(256,128);
const orb=document.createElement('canvas');orb.width=orb.height=256;const og=orb.getContext('2d'),op=og.createImageData(256,256);
// Twice the presentation resolution, including the moving water material.
c.width=W*2;c.height=H*2;g.setTransform(2,0,0,2,0,0);
let environment;
let noise,flowFrame=-1,paused=true,time=1.6,last=0,ready=false;
const floor=document.createElement('canvas');floor.width=W;floor.height=H;
function ground(){
 const x=floor.getContext('2d');let grad=x.createLinearGradient(0,0,0,H);grad.addColorStop(0,'#11191d');grad.addColorStop(.58,'#293135');grad.addColorStop(1,'#333c3d');x.fillStyle=grad;x.fillRect(0,0,W,H);
 // A quiet perspective floor anchors movement and contact without competing with the attack.
 for(let row=0;row<9;row++){
  const p0=row/9,p1=(row+1)/9,y0=330+270*p0*p0,y1=330+270*p1*p1;
  const span0=130+1100*p0,span1=130+1100*p1;
  for(let col=-7;col<8;col++){
   const seed=(Math.sin(row*91+col*47)*43758.5453)%1,v=Math.round(40+Math.abs(seed)*9+row*.8);
   x.beginPath();x.moveTo(470+col*span0/7,y0);x.lineTo(470+(col+1)*span0/7,y0);x.lineTo(470+(col+1)*span1/7,y1);x.lineTo(470+col*span1/7,y1);x.closePath();x.fillStyle=`rgb(${v-5},${v+1},${v+1})`;x.fill();x.strokeStyle='#121b1b45';x.lineWidth=1;x.stroke();
  }
 }
 const v=x.createRadialGradient(540,310,120,480,300,640);v.addColorStop(0,'#0000');v.addColorStop(1,'#020609d9');x.fillStyle=v;x.fillRect(0,0,W,H);
}
function glow(x,y,rx,ry,color,a){if(a<.002)return;g.save();g.translate(x,y);g.scale(1,ry/rx);const r=g.createRadialGradient(0,0,0,0,0,rx);r.addColorStop(0,color);r.addColorStop(.28,color);r.addColorStop(1,'#78d6ee00');g.globalAlpha=clamp(a);g.fillStyle=r;g.fillRect(-rx,-rx,rx*2,rx*2);g.restore()}
function sheet(name,f,x,y,w,h,a=1,angle=0,flip=false){
 if(a<.002)return;f=Math.max(0,Math.min(63,Math.floor(f)));const i=images[name];
 g.save();g.globalAlpha=clamp(a);g.translate(x,y);g.rotate(angle);if(flip)g.scale(1,-1);
 g.drawImage(i,f%8*256,Math.floor(f/8)*256,256,256,-w/2,-h/2,w,h);g.restore();
}
function mist(t,x,y,w,h,a){const f=Math.floor(t*27)%64;sheet('mist',f,x,y,w,h,a)}
function flowMaterial(t){
 const f=Math.floor(t*30);if(f===flowFrame)return;flowFrame=f;
 const sample=(x,y)=>noise[((y&255)*256+(x&255))*4]/255;
 for(let y=0;y<128;y++)for(let x=0;x<256;x++){
  // Independently scrolling octave masks, following JangaFX's documented D3 study.
  const n1=sample(Math.floor(x*.8-t*58),Math.floor(y*1.5+t*11));
  const n2=sample(Math.floor(x*1.6-t*116+71),Math.floor(y*3-t*7));
  const n3=sample(Math.floor(x*3.2-t*232+139),Math.floor(y*6+t*14));
  const value=clamp((n1*n2*n3*4-.18)*2.5+.2);
  const u=(x-142)/128,v=(y-64)/49;
  const shape=Math.exp(-(u*u*1.3+v*v*2.5));const edge=smooth((1-Math.abs(v))/.4)*smooth(x/38)*smooth((255-x)/46);
  const idx=(y*256+x)*4;pixels.data[idx]=148+value*75;pixels.data[idx+1]=188+value*55;pixels.data[idx+2]=204+value*47;pixels.data[idx+3]=Math.round(255*value*shape*edge*.8);
 }
 fg.putImageData(pixels,0,0);
}
function stream(t,x,y,w,h,a,angle=0){g.save();g.translate(x,y);g.rotate(angle);g.globalAlpha=clamp(a);g.drawImage(flow,-w/2,-h/2,w,h);g.restore()}
function waterSample(x,y){
 const ix=Math.floor(x),iy=Math.floor(y),fx=x-ix,fy=y-iy;
 const at=(xx,yy)=>noise[(((yy&255)*256)+(xx&255))*4]/255;
 return mix(mix(at(ix,iy),at(ix+1,iy),fx),mix(at(ix,iy+1),at(ix+1,iy+1),fx),fy);
}
function waterOrb(t,x,y,r,a=1,stretch=1){
 // Flowing surface normals, environmental refraction and broad reflections.
 // No luminous crack pattern: transparent water carries the moving detail.
 for(let py=0;py<256;py++)for(let px=0;px<256;px++){
  const u=(px-127.5)/119,v=(py-127.5)/119,angle=Math.atan2(v,u);
  const edgeRadius=1+Math.sin(angle*5+t*4)*.028+Math.sin(angle*9-t*3)*.018;
  const d=Math.hypot(u,v)/edgeRadius,idx=(py*256+px)*4;
  if(d>=1){op.data[idx+3]=0;continue;}
  const z=Math.sqrt(1-d*d);
  const sx=(Math.atan2(u,z)/PI+.5)*224+t*20;
  const sy=(Math.asin(Math.max(-1,Math.min(1,v)))/PI+.5)*224-t*17;
  const n=waterSample(sx+Math.sin(sy*.035+t)*13,sy);
  const detail=waterSample(sx*2.8-t*31+n*19,sy*2.8+t*13);
  const dx=waterSample(sx+1.8,sy)-waterSample(sx-1.8,sy);
  const dy=waterSample(sx,sy+1.8)-waterSample(sx,sy-1.8);
  let nx=u+dx*3.2+(detail-.5)*.18,ny=v+dy*3.2,nz=z;
  const len=Math.hypot(nx,ny,nz);nx/=len;ny/=len;nz/=len;
  const fresnel=.02+.98*Math.pow(1-z,5);
  const highlight=Math.pow(Math.max(0,-nx*.36-ny*.48+nz*.8),48);
  const reflection=Math.pow(Math.max(0,-nx*.7+ny*.12+nz*.7),18);
  const ripple=Math.pow(Math.max(0,detail-.43)*1.65,3)*(.3+z*.7);
  const ex=Math.max(0,Math.min(W-1,Math.round(x+u*r*.56+dx*27)));
  const ey=Math.max(0,Math.min(H-1,Math.round(y+v*r*.56+dy*27)));
  const e=(ey*W+ex)*4;
  // Connected, advected foam patches instead of isolated white dots.
  const foam=smooth((detail*.62+n*.38-.44)/.27)*smooth((d-.18)/.7);
  const light=highlight*139+reflection*(64+fresnel*46)+ripple*62;
  op.data[idx]=mix(environment[e]*.87+light+9+fresnel*47,216,foam*.84);
  op.data[idx+1]=mix(environment[e+1]*.95+light+8+fresnel*59,233,foam*.84);
  op.data[idx+2]=mix(environment[e+2]+light+13+fresnel*63,238,foam*.84);
  op.data[idx+3]=Math.round(255*smooth((1-d)/.035)*Math.min(1,.7+fresnel*.2+highlight*.1+foam*.23));
 }
 og.putImageData(op,0,0);g.save();g.globalAlpha=clamp(a);g.translate(x,y);g.imageSmoothingQuality='high';g.drawImage(orb,-r*stretch,-r,r*2*stretch,r*2);g.restore();
}
function splashContact(age){
 if(age<0||age>=1.3)return;
 const fade=1-smooth((age-.43)/.87);
 const f=14+49*Math.pow(Math.min(1,age/1.2),.78);
 // Native liquid motion only: never translate the complete image downward.
 sheet('jet',f,666,299,415,300,fade*.96,.04);
 const aerosol=smooth(age/.14)*(1-smooth((age-.25)/.65));
 g.save();g.filter='blur(2px)';
 sheet('jet',f,666,299,428,308,aerosol*.1,.04);g.restore();
}
function target(t,on,kind='hurt',water=true){
 const events=library.hits(attack,variant),first=1.5+events[0];
 const latest=events.filter(e=>t>=1.5+e).at(-1)??events[0];
 const age=t-first,lastAge=t-1.5-latest;
 const hitWeight=attack==='doubleSlash'?(latest===events[0]?.72:1.3):attack==='rain'?(variant===0?[.72,.95,1.38][Math.max(0,events.indexOf(latest))]:variant===2?1.18:1):1;
 const recoil=on&&kind==='hurt'&&lastAge>0?Math.sin(Math.min(1,lastAge/.14)*PI/2)*Math.exp(-lastAge*3.8)*hitWeight:0;
 const hold=['vendetta','blackSlash','tidal','rain','scirocco','retour','furia','vulcano'].includes(attack)?1.75:1.25,recoverTime=['vendetta','blackSlash','tidal','rain','scirocco','retour','furia','vulcano'].includes(attack)?.5:.4;
 const hurt=on&&kind==='hurt'&&age>=0&&lastAge<hold+recoverTime,recovery=smooth((lastAge-hold)/recoverTime),guard=on&&t>.75&&(['guard','evade'].includes(kind)?age<(attack==='reticle'?2.15:1.65):kind==='hurt'&&t<first);
 const i=images[hurt?'hurt':guard?'guard':'idle'];const h=420,w=h*i.width/i.height;
 const evade=on&&kind==='evade'?(t<1.5?smooth((t-1.12)/.38):1-smooth(age/1.2)):0;
 const shudder=on&&attack==='blur'&&age>=0&&age<1.65?(Math.sin(t*105)*2.2+Math.sin(t*157)*.85)*(1-smooth((age-.55)/1.1)):on&&attack==='mistral'&&age>.12&&age<2.05?(Math.sin(t*77)*1.5+Math.sin(t*113)*.65)*(1-smooth((age-1.45)/.6)):0;
 const x=666+shudder+recoil*(attack==='mistral'?(variant===1?54:44):attack==='tidal'&&variant===0?61:attack==='blackSlash'?43:attack==='vendetta'?33:attack==='doubleSlash'?27:attack==='rain'?35:21)+evade*(variant===1?22:-24),y=495;
 g.save();g.globalAlpha=.55;g.fillStyle='#000';g.filter='blur(9px)';g.beginPath();g.ellipse(x,499,80,13,0,0,PI*2);g.fill();g.restore();
 q.clearRect(0,0,W,H);q.save();q.translate(x,y);q.rotate(recoil*(attack==='mistral'?.085:attack==='tidal'&&variant===0?.11:attack==='blackSlash'?.105:attack==='vendetta'?.085:attack==='rain'?.078:.055));q.globalAlpha=1-evade*.6;
 if(hurt){
  q.globalAlpha=1-recovery;q.drawImage(i,-w/2,-h,w,h);
  q.globalAlpha=recovery;q.drawImage(images.idle,-w/2,-h,w,h);
 }else q.drawImage(i,-w/2,-h,w,h);
 q.restore();
 if(on){
  const flash=kind==='hurt'?pulse(lastAge,.03,.085)*(water?1:['vendetta','doubleSlash','blackSlash'].includes(attack)?.05:.18):0,wet=water?endFade(t,1.5,2.4):0;
  q.globalCompositeOperation='source-atop';q.fillStyle=`rgba(8,43,55,${wet*.27})`;q.fillRect(0,0,W,H);
  const r=q.createRadialGradient(635,285,0,635,285,210);r.addColorStop(0,`rgba(206,243,251,${flash*.9})`);r.addColorStop(.35,`rgba(106,192,217,${flash*.4})`);r.addColorStop(1,'#83c7dc00');q.fillStyle=r;q.fillRect(0,0,W,H);
  if(kind==='calm'||kind==='guard'){
   const strength=(t<1.5?smooth((t-.3)/.72):1-smooth((age-.3)/1.4))*(attack==='beam'?.17:.045);
   const sheen=q.createLinearGradient(520,100,790,450);sheen.addColorStop(0,attack==='beam'?`rgba(236,212,165,${strength})`:`rgba(170,210,217,${strength})`);sheen.addColorStop(1,'#b5c9d000');q.fillStyle=sheen;q.fillRect(0,0,W,H);
  }
  if(attack==='blackSlash'){
    const a=pulse(lastAge,.035,.12)*.48;const gold=q.createRadialGradient(666,299,0,666,299,185);gold.addColorStop(0,`rgba(255,189,73,${a})`);gold.addColorStop(1,'#d9a24400');q.fillStyle=gold;q.fillRect(0,0,W,H);
   }
   if(attack==='doubleSlash'){
    const a=pulse(lastAge,.035,.09)*.31*hitWeight;
    const violet=q.createRadialGradient(666,latest<0?270:299,0,666,latest<0?270:299,145);violet.addColorStop(0,`rgba(151,83,211,${a})`);violet.addColorStop(1,'#793db000');q.fillStyle=violet;q.fillRect(0,0,W,H);
   }
   if(attack==='rain'){
    const a=pulse(lastAge,.04,.1)*.4*hitWeight;const blue=q.createRadialGradient(666,290,0,666,290,190);blue.addColorStop(0,`rgba(116,181,255,${a})`);blue.addColorStop(1,'#427fca00');q.fillStyle=blue;q.fillRect(0,0,W,H);
   }
   if(attack==='vendetta'){
   const a=pulse(lastAge,.035,.075)*.23;
   const red=q.createRadialGradient(666,295,0,666,295,120);red.addColorStop(0,`rgba(192,47,37,${a})`);red.addColorStop(1,'#b02d2400');q.fillStyle=red;q.fillRect(0,0,W,H);
  }
  q.globalCompositeOperation='source-over';
 }
 g.drawImage(layer,0,0);
}
const LOOP=5.45,LAUNCH=3.12;
const launchTime=()=>library.launches[attack];
const duration=()=>LOOP+(launchTime()-LAUNCH)+Math.max(0,...library.hits(attack,variant))+(['vendetta','blackSlash','tidal','rain','beam','scirocco','retour','furia','vulcano'].includes(attack)?.6:0);
function render(value){
 if(!ready)return;const total=duration(),launch=launchTime(),clock=((value%total)+total)%total;
 // Stretch preparation only; flight, contact and aftermath retain their timing.
 const t=clock<=.3?clock:clock<launch?.3+(clock-.3)*(.82/(launch-.3)):clock-(launch-1.12);
 const on=$('#effects').checked,reference=attack==='wave'&&variant===0,kind=library.defs[attack].kind,charge=endFade(t,.3,.95),flight=clamp((t-1.12)/.38),age=t-1.5;
 flowMaterial(clock);g.save();g.clearRect(0,0,W,H);
 const impactEvents=library.hits(attack,variant),recentHit=impactEvents.filter(e=>age>=e).at(-1),shakeAge=['doubleSlash','mistral','rain','vulcano'].includes(attack)?(recentHit===undefined?-1:age-recentHit):age;
 const shake=on&&kind==='hurt'&&shakeAge>0?Math.exp(-shakeAge*(attack==='tidal'&&variant===0?12:attack==='blackSlash'?13:attack==='vendetta'?16:21))*(attack==='rain'?(variant===0?(recentHit===impactEvents[2]?7:3.6):variant===2?6:4.5):attack==='mistral'?6:attack==='tidal'&&variant===0?8.2:attack==='blackSlash'?7.5:attack==='vendetta'?5.2:attack==='doubleSlash'?(recentHit===impactEvents[0]?2.8:5.4):3.2):0;g.translate(Math.sin(t*107)*shake,Math.cos(t*91)*shake*.5);g.drawImage(floor,0,0);
 mist(t*.4,610,330,700,110,.05);
 const A={g,images,crops,id:attack,variant,t,clock,age,flight,launch,hitOffsets:impactEvents,shown:on,sample:waterSample,glow,mist,sheet,stream,waterOrb,splashContact};
 const selfEffect=attack==='wind'||attack==='calm';
 const drawEffect=behind=>{g.save();if(selfEffect)g.translate(-486,0);library.draw(A,behind);g.restore()};
 if(on&&reference){
  glow(210,475,230,40,'#73b5c350',charge*.6);
  glow(666,493,260,48,'#a0d7e967',pulse(t,1.56,.13)*.75);
 }
 window.EdenDucActor.draw(A);
 if(on&&!reference)drawEffect(true);
 target(t,on&&!selfEffect,kind,attack==='wave'||attack==='tidal');
 if(on&&reference){
  if(t<1.12){
   const build=smooth((t-.3)/.72);
   waterOrb(clock,220,300,18+build*31,smooth((t-.3)/.2)*.95);
   mist(t,206,342,160,105,build*.09);
  }
  if(t>=1.12&&t<1.5){
   const x=mix(220,656,flight),y=300-Math.sin(flight*PI)*30;
   for(let j=4;j>=1;j--){const p=Math.max(0,flight-j*.045);stream(t-j*.025,mix(220,656,p),300-Math.sin(p*PI)*30,80,22,.025+(4-j)*.02,-.02);}
   stream(t,x-48,y,115,32,.38,-.02);waterOrb(clock,x,y,49-flight*7,.98,1.06);
   glow(x,y,84,40,'#c0e1e34d',.28);
  }
  splashContact(age);
  if(age>=0&&age<1.65){
   const a=1-smooth((age-.7)/.95);
   mist(t,710,430,380,170,a*.065);
   glow(655,290,100,130,'#dcf7fb',pulse(t,1.525,.032)*.25);
  }
 }
 if(on&&!reference)drawEffect(false);
 g.restore();$('#timeline').value=String(clock);$('#time').textContent=clock.toFixed(2)+' s';
 const phase=t+1e-9<1.12?0:t+1e-9<1.5?1:t+1e-9<1.9?2:3;document.querySelectorAll('[data-phase]').forEach(e=>e.setAttribute('aria-current',String(Number(e.dataset.phase)===phase)));
}
const attackSelect=$('#attack');
for(const [id,def] of Object.entries(library.defs)){const option=document.createElement('option');option.value=id;option.textContent=def.name;attackSelect.append(option)}
const params=new URLSearchParams(location.search);if(library.defs[params.get('angriff')])attack=params.get('angriff');
if(['0','1','2'].includes(params.get('variante')))variant=Number(params.get('variante'));
function refreshSelection(){
 $('#burn-control').hidden=attack!=='vulcano';
 const def=library.defs[attack];attackSelect.value=attack;$('#timeline').max=(duration()-.01).toFixed(2);
 document.querySelector('h1').textContent=def.name+' · '+def.variants[variant][0];
 document.title='Eden Rise · '+def.name;$('#attack-description').textContent=def.variants[variant][1];
 const rule=window.EdenAttackRules[attack];$('#attack-type').textContent=rule.type+' · ab Stufe '+rule.level+' · '+rule.cost+' Ausdauer';$('#attack-rule').textContent=rule.effect;
 $('#scene').setAttribute('aria-label',def.name+' – '+def.variants[variant][0]);
 document.querySelectorAll('[data-variant]').forEach(b=>{const n=Number(b.dataset.variant);b.textContent=(n+1)+' · '+def.variants[n][0];b.setAttribute('aria-pressed',String(n===variant))});
 const labels=def.kind==='hurt'?['01 · Vorbereitung','02 · Angriff','03 · Kontakt','04 · Ausklang']:['01 · Vorbereitung','02 · Entfaltung','03 · Wirkung','04 · Ausklang'];
 document.querySelectorAll('[data-phase]').forEach((e,i)=>e.textContent=labels[i]);
}
function selectionChanged(){time=0;paused=false;$('#play').textContent='Pause';refreshSelection();if(ready)render(time)}
attackSelect.onchange=()=>{attack=attackSelect.value;selectionChanged()};
document.querySelectorAll('[data-variant]').forEach(b=>b.onclick=()=>{variant=Number(b.dataset.variant);selectionChanged()});
$('#burn-stacks').onchange=e=>{window.EdenBerserker.stacks=Number(e.target.value);selectionChanged()};
refreshSelection();
$('#play').onclick=()=>{paused=!paused;$('#play').textContent=paused?'Abspielen':'Pause'};
$('#restart').onclick=()=>{time=0;render(time)};$('#timeline').oninput=e=>{time=Number(e.target.value);render(time)};$('#effects').onchange=()=>render(time);
async function init(){
 await Promise.all([load('fire','../assets/feuer.png'),load('idle','../assets/figur_idle.webp'),load('guard','../assets/figur_guard.webp'),load('hurt','../assets/figur_hurt.webp'),load('jet','spritzwasser-natuerlich.png'),load('tidalNative','../assets/lame-liquigen-1024-v7.png'),load('shieldNative','../assets/bonaccia-liquigen-v3.png'),load('column','../assets/native-v6/ausbruch.png?v=2'),load('impact','../assets/native-v6/treffer.png'),load('mist','../assets/staub_frei.png'),load('noise','../assets/stroemung.png'),load('stahl','../assets/realismus-v3/stahl-gerade.png'),load('stahlrot','../assets/realismus-v3/stahl-vendetta-rot.png'),load('stahlviolett','../assets/realismus-v3/stahl-doppio-violett-v1.png'),load('licht','../assets/realismus-v3/licht.png'),load('glint','../assets/realismus-v3/kenney-flare_01.png'),load('trace','../assets/realismus-v3/kenney-trace_04.png')]);
 await window.EdenDucActor.load('../assets/');
 await window.EdenFigurePicker.mount($('#preview-figure'),{base:'../assets/',onChange(set){images.idle=set.idle;images.hurt=set.hurt;images.guard=set.guard;if(ready)render(time)}});
 const n=document.createElement('canvas');n.width=n.height=256;const nx=n.getContext('2d',{willReadFrequently:true});nx.drawImage(images.noise,0,0);noise=nx.getImageData(0,0,256,256).data;
 crops=Object.fromEntries(window.EDEN_REALISM_SOURCES.generated.map(r=>[r.name,r.crop]));
 ground();environment=floor.getContext('2d').getImageData(0,0,W,H).data;ready=true;window.EdenAttackStudy={render(t){time=t;render(t)},get duration(){return duration()},timing(){return {launch:launchTime(),contact:launchTime()+.38}},selection(){return {attack,variant}},actor(t){const launch=launchTime();return window.EdenDucActor.state({id:attack,variant,clock:t,launch,hitOffsets:library.hits(attack,variant)})}};render(time);
 function tick(now){if(!paused&&last)time+=Math.min(.05,(now-last)/1000)*Number($('#speed').value);last=now;if(!paused)render(time);requestAnimationFrame(tick)}requestAnimationFrame(tick);
}
init().catch(e=>{$('#error').textContent=e.message});
})();
