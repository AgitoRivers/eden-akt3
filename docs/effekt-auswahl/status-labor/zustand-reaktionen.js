/* Shared state/reaction preview; never calls the game. */
(()=>{'use strict';
const C=x=>Math.max(0,Math.min(1,x)),S=x=>{x=C(x);return x*x*(3-2*x)},PI=Math.PI;
const pulse=(t,c,w)=>Math.exp(-Math.pow((t-c)/w,2));
const span=(t,a,b,fade=.6)=>S((t-a)/.16)*(1-S((t-b)/fade));
const colors={fire:'#ff9a48',water:'#72c7e2',quake:'#cfbaa0',electric:'#e8cf82',shortCircuit:'#9bd6f2',mud:'#b29b72',firestorm:'#ff9a48',steam:'#c7d9df',flare:'#f29a65'};
const reactionIds=['shortCircuit','mud','firestorm','steam','flare'];
const poses=document.createElement('canvas');poses.width=1200;poses.height=1120;const pg=poses.getContext('2d');pg.scale(2,2);
const cell=document.createElement('canvas');cell.width=cell.height=256;const cg=cell.getContext('2d');
let images;const halos=new Map();
function body(g,pose,alpha=1,x=0,y=0){const i=images[pose],h=475,w=h*i.width/i.height;g.save();g.globalAlpha=alpha;g.drawImage(i,300-w/2+x,32+y,w,h);g.restore()}
function halo(g,id,pose,alpha,x,y){
 if(alpha<.002)return;const key=id+pose;
 if(!halos.has(key)){
  const c=document.createElement('canvas');c.width=600;c.height=560;const q=c.getContext('2d');body(q,pose);q.globalCompositeOperation='source-in';q.fillStyle=colors[id];q.fillRect(0,0,600,560);
  const out=document.createElement('canvas');out.width=600;out.height=560;const h=out.getContext('2d');h.filter='blur(9px)';h.drawImage(c,0,0);h.filter='none';h.globalCompositeOperation='destination-out';body(h,pose);halos.set(key,out);
 }g.save();g.globalAlpha=alpha;g.drawImage(halos.get(key),x,y);g.restore();
}
function frame(g,name,time,x,y,w,h,a=1,tint=null,angle=0){
 if(a<.003)return;const i=images[name],f=((Math.floor(time*30)%64)+64)%64;
 cg.clearRect(0,0,256,256);cg.globalCompositeOperation='source-over';cg.drawImage(i,f%8*256,Math.floor(f/8)*256,256,256,0,0,256,256);
 if(tint){cg.globalCompositeOperation='source-atop';cg.fillStyle=tint;cg.fillRect(0,0,256,256);cg.globalCompositeOperation='source-over'}
 g.save();g.globalAlpha=C(a);if(name==='strom')g.globalCompositeOperation='screen';g.translate(x+w/2,y+h/2);g.rotate(angle);g.drawImage(cell,-w/2,-h/2,w,h);g.restore();
}
function wetFrame(g,name,f,x,y,w,h,alpha=1){
 if(alpha<.003)return;const i=images[name];f=Math.max(0,Math.min(63,Math.floor(f)));
 g.save();g.globalAlpha=C(alpha);g.drawImage(i,f%8*256,Math.floor(f/8)*256,256,256,x,y,w,h);g.restore();
}
function stage(g,light){
 const bg=g.createRadialGradient(300,270,30,300,280,410);bg.addColorStop(0,light?'#c9c7bd':'#2b353d');bg.addColorStop(1,light?'#8e9593':'#10161d');g.fillStyle=bg;g.fillRect(0,0,600,560);
 const floor=g.createLinearGradient(0,460,0,560);floor.addColorStop(0,'#111b2000');floor.addColorStop(1,light?'#4e595a99':'#071017aa');g.fillStyle=floor;g.fillRect(0,460,600,100);
 g.save();g.filter='blur(10px)';g.fillStyle='#0007';g.beginPath();g.ellipse(300,507,89,11,0,0,PI*2);g.fill();g.restore();
}
const stoneChips=new Map();
function chipImage(index,mud){
 const key=index+String(mud);if(stoneChips.has(key))return stoneChips.get(key);
 const crops=[[568,216,602,234],[1760,380,1794,400],[1446,544,1478,566],[1506,488,1536,506],[1718,328,1742,344]],b=crops[index];
 const c=document.createElement('canvas');c.width=b[2]-b[0];c.height=b[3]-b[1];const q=c.getContext('2d');q.drawImage(images.bodenbruch,b[0],b[1],c.width,c.height,0,0,c.width,c.height);
 if(mud){q.globalCompositeOperation='source-atop';q.fillStyle='#945b2dc4';q.fillRect(0,0,c.width,c.height)}
 stoneChips.set(key,c);return c;
}
const scatter=seed=>{const n=Math.sin(seed*127.1+31.7)*43758.5453;return n-Math.floor(n)};
function stoneSpray(g,t,mud=false,front=false){
 // Seven dense bursts with depth, broad trajectories, tumbling and a small grounded bounce.
 const perBurst=22,bursts=7;
 for(let burst=0;burst<bursts;burst++)for(let j=0;j<perBurst;j++){
  const seed=burst*97+j*13+11,foreground=scatter(seed+1)>.58;if(foreground!==front)continue;
  const launch=.24+burst*.34+scatter(seed+2)*.14,age=t-launch,life=1.02+scatter(seed+3)*.3;if(age<0||age>life)continue;
  const side=scatter(seed+4)<.5?-1:1,vx=side*(45+scatter(seed+5)*120),vy=145+scatter(seed+6)*235;
  const gravity=260,land=vy/gravity,after=Math.max(0,age-land),bounceVy=vy*.19;
  const height=age<land?-vy*age+gravity*age*age:after<bounceVy/gravity?-bounceVy*after+gravity*after*after:0;
  const travel=age<land?age:land+after*.18;
  const depth=foreground?1:.84,x=300+side*(12+scatter(seed+7)*38)+vx*travel*depth,y=foreground?505:494;
  const large=j%7===0,w=(large?14+scatter(seed+8)*8:4+scatter(seed+8)*8)*depth;
  const im=chipImage((j+burst)%5,mud),h=w*im.height/im.width;
  const alpha=S(age/.035)*(1-S((age-(life-.34))/.34))*(large?.92:.78);
  g.save();g.globalAlpha=alpha;g.translate(x,y+height);g.rotate(scatter(seed+9)*PI*2+Math.min(age,land)*side*(4+scatter(seed+10)*8));
  // Squash changes with tumble, retaining connected photographic material rather than round dots.
  g.scale(1,.65+.35*Math.abs(Math.cos(age*8+seed)));g.drawImage(im,-w/2,-h/2,w,h);g.restore();
 }
}
function poseAt(id,t){
 const events=id==='shortCircuit'?[.23,.8,1.3]:id==='firestorm'?[.28,.95]:[.28];
 const latest=events.filter(e=>e<=t).at(-1),age=latest===undefined?-1:t-latest;
 const hold=reactionIds.includes(id)?1.15:2.55;
 const weight=age<0?0:S(age/.08)*(1-S((age-hold)/(reactionIds.includes(id)?.42:.5)));
 return {pose:['water','quake'].includes(id)?'guard':'hurt',weight,age};
}
function render(canvas,id,time,settings={}){
 if(canvas.width!==1200||canvas.height!==1120){canvas.width=1200;canvas.height=1120}
 const g=canvas.getContext('2d'),t=((time%4.2)+4.2)%4.2,isReaction=reactionIds.includes(id),env=isReaction?span(t,.12,2.75,.85):1;
 const {pose,weight,age}=poseAt(id,t),recoil=age>=0?Math.sin(Math.min(1,age/.12)*PI/2)*Math.exp(-age*6)*4:0;
 const dx=id==='quake'?span(t,.22,2.7,.55)*(Math.sin(t*53)*3.7+Math.sin(t*91)*1.3):recoil,dy=Math.abs(dx)*.18,shown=settings.figure!==false;
 const discharge=(.2+.8*Math.pow(Math.max(0,Math.sin(t*27)+.3*Math.sin(t*53)),3))*(.5+.5*Math.pow(Math.sin(t*4.2),2));
 g.save();g.setTransform(2,0,0,2,0,0);g.clearRect(0,0,600,560);stage(g,settings.light);
 if(id==='fire'||id==='firestorm')window.EdenOrganicBurn.draw({g,image:images.oilFire,time,x:300+dx,foot:507+dy,scale:1.12,intensity:id==='fire'?1:env,seed:2},true);
 if(id==='quake'||id==='mud')stoneSpray(g,t,id==='mud',false);
 if(id==='steam')frame(g,'staub',t*.65,150-t*9,300-t*22,300+t*15,225,env*.36);
 if(shown){
  halo(g,id,'figure',env*.62*(1-weight),dx,dy);halo(g,id,pose,env*.62*weight,dx,dy);
  pg.clearRect(0,0,600,560);body(pg,'figure',1-weight,dx,dy);body(pg,pose,weight,dx,dy);
  pg.globalCompositeOperation='source-atop';
  const hot=['fire','firestorm','flare'].includes(id),wet=['water','shortCircuit','mud'].includes(id);
  if(wet){const film=pg.createLinearGradient(0,125,0,505);film.addColorStop(0,'#07213700');film.addColorStop(.45,id==='mud'?`rgba(67,46,27,${env*.38})`:`rgba(5,29,44,${env*(id==='water'?.56:.42)})`);film.addColorStop(1,id==='mud'?`rgba(67,46,27,${env*.48})`:`rgba(5,29,44,${env*(id==='water'?.6:.48)})`);pg.fillStyle=film;pg.fillRect(0,0,600,560);}
  const lamp=pg.createLinearGradient(180,230,370,505);
  const strength=hot?(id==='flare'?pulse(t,.48,.24)*.3:env*(.16+.04*Math.sin(t*9))):id==='electric'||id==='shortCircuit'?env*C(discharge)*.27:0;
  lamp.addColorStop(0,'#c3dcf000');lamp.addColorStop(1,hot?`rgba(255,139,52,${strength})`:`rgba(179,213,245,${strength})`);pg.fillStyle=lamp;pg.fillRect(0,0,600,560);
  if(wet){
   for(let j=0;j<3;j++){
    const x=250+j*43+Math.sin(t*1.4+j)*10,y=215+j*67+Math.sin(t*.9+j)*15;
    pg.save();pg.translate(x,y);pg.rotate(-.18+Math.sin(t+j)*.08);pg.scale(.35,1);
    const sheen=pg.createRadialGradient(0,0,0,0,0,80);sheen.addColorStop(0,`rgba(193,219,229,${env*(id==='mud'?.11:id==='water'?.26:.23)})`);sheen.addColorStop(1,'#bed7e400');pg.fillStyle=sheen;pg.fillRect(-82,-82,164,164);pg.restore();
   }
  }
  pg.globalCompositeOperation='source-over';g.drawImage(poses,0,0,600,560);
 }
 if(id==='fire'){
  window.EdenOrganicBurn.draw({g,image:images.oilFire,time,x:300+dx,foot:507+dy,scale:1.12,intensity:1,seed:2},false);
  frame(g,'staub',t*.5,190,285-t%2.1*27,230,190,.085);
 }
 if(id==='water'){
  const wash=span(t,.16,.76,.6);
  wetFrame(g,'wetSplash',14+C((t-.16)/1.2)*49,95,180,410,265,wash*.58);
 }
 if(id==='quake')stoneSpray(g,t,false,true);
 if(id==='electric')frame(g,'strom',t*1.15,165,140,270,325,C(discharge)*.86,'#d5e4ff1c');
 if(id==='shortCircuit'){
  frame(g,'strom',t*1.4,150,110,310,365,env*(.18+C(discharge)*.82));
  frame(g,'staub',t*.65,170-t*8,330-t*27,270+t*10,190,env*.31,'#b4cfda45');
 }
 if(id==='mud'){
  frame(g,'staub',t*.82+.7,100-t*7,440,390+t*12,78,env*.46,'#775237ed');
  frame(g,'staub',t*.9,165+Math.sin(t)*13,392-t*5,290+t*16,133,env*.5,'#856342e6');
  stoneSpray(g,t,true,true);
 }
 if(id==='firestorm'){
  window.EdenOrganicBurn.draw({g,image:images.oilFire,time,x:300+dx,foot:507+dy,scale:1.12,intensity:env,seed:2},false);
  frame(g,'strom',t*1.25,160,145,280,330,env*C(discharge)*.68);
  frame(g,'staub',t*.6,150,245-t*24,310,220,env*.15);
 }
 if(id==='steam'){
  frame(g,'feuer',t,210,280,180,210,(1-S(t/.62))*.77);
  frame(g,'staub',t*.65,135-t*13,310-t*38,325+t*18,245+t*12,env*.64);
  frame(g,'staub',t*.65+.75,215,370-t*34,205+t*9,185,env*.28);
 }
 if(id==='flare'){
  const flash=pulse(t,.48,.21);
  frame(g,'feuer',t*1.5,210,285-flash*80,180,165+flash*100,C(flash*1.1));
  frame(g,'staub',t*.7,190,345-t*30,235,185,span(t,.52,2.65,.7)*.28);
 }
 g.restore();return {pose,weight,age};
}
window.EdenStateFx={init(value){images=value;halos.clear()},render,poseAt,duration:4.2};
})();
