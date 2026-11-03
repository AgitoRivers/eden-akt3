/* Phare and Pluie d'Etoiles: isolated visual study. No combat execution.
 * Moving volumetric light, existing native impact material and ballistic motes. */
(()=>{'use strict';
const PI=Math.PI,C=x=>Math.max(0,Math.min(1,x)),S=x=>{x=C(x);return x*x*(3-2*x)},mix=(a,b,p)=>a+(b-a)*p;
const cone=document.createElement('canvas');cone.width=192;cone.height=384;
let coneFrame=-1,blueImpact;
const debris=document.createElement('canvas');debris.width=200;debris.height=160;let debrisFrame=-1;
const hash=n=>{const q=Math.sin(n*127.1+311.7)*43758.5453;return q-Math.floor(q)};
const events=v=>v===0?[0,.27,.72]:v===1?[0,.23,.5]:[-.035,0,.035];
function mote(g,x,y,r,alpha,color){
 if(alpha<.002)return;g.save();g.globalAlpha=C(alpha);g.fillStyle=color;g.beginPath();g.ellipse(x,y,r,r*.72,0,0,PI*2);g.fill();g.restore();
}
function coneMaterial(A){
 const frame=Math.floor(A.clock*24);if(frame===coneFrame)return;coneFrame=frame;
 const q=cone.getContext('2d'),im=q.createImageData(192,384),tm=frame/24;
 for(let y=0;y<384;y++)for(let x=0;x<192;x++){
  const v=y/384,u=(x-96)/96,width=.11+v*.87;
  const warp=A.sample(x*.65+tm*7,y*.43-tm*20);
  const n=A.sample(x*.81+warp*17,y*.62-tm*33),detail=A.sample(x*2.3-tm*15,y*1.5+tm*12);
  const side=Math.exp(-Math.pow(Math.abs(u)/width,3)*3.1),foot=1-S((v-.86)/.14);
  const streak=.56+.44*A.sample(x*.27+tm*2,y*.035+warp*5);
  const a=side*foot*S(v/.08)*(.3+n*.48+detail*.12)*streak;
  const i=(y*192+x)*4;im.data[i]=255;im.data[i+1]=215+detail*25;im.data[i+2]=153+detail*54;im.data[i+3]=255*a*.83;
 }q.putImageData(im,0,0);
}
function shaft(A,x,width,opacity,angle=0){
 if(opacity<.002)return;coneMaterial(A);const g=A.g;
 g.save();g.globalCompositeOperation='screen';g.globalAlpha=C(opacity);g.translate(x,-95);g.rotate(angle);g.drawImage(cone,-width/2,0,width,620);g.restore();
}
function phare(A,behind){
 const {g,t,age,clock,variant:v}=A;
 const build=S((t-.28)/.76),fade=1-S((age-1.05)/1.15),env=build*fade;
 if(env<.002)return;
 const settle=S((t-.65)/.64),sweep=(1-settle)*(.34*Math.sin(clock*2.25)+.2);
 if(behind){
  g.save();g.fillStyle=`rgba(0,4,9,${env*.36})`;g.fillRect(0,0,960,600);g.restore();
  A.mist(clock*.55,666,295,470,385,env*.13);
  if(v===0){shaft(A,666,350,env*.96,sweep);shaft(A,666,115,env*.42,sweep);}
  if(v===1){
   const opening=(1-settle)*110;
   shaft(A,666-opening,150,env*.8,-.12*(1-settle));shaft(A,666+opening,150,env*.8,.12*(1-settle));shaft(A,666,260,env*settle*.55);
  }
  if(v===2){for(let j=-2;j<=2;j++)shaft(A,666+j*19,200,env*(j===0?.5:.28),j*(.07+.06*settle));}
  A.glow(666,492,190,31,'#f6d498ae',env*.62);
  A.glow(666,250,135,260,'#fbe4b333',env*.24);
 }else{
  shaft(A,666,v===1?185:250,env*.16,v===0?sweep:0);
  for(let j=0;j<64;j++){
   const seed=((j*71+17)%101)/101,phase=(clock*(.08+seed*.045)+j*.618)%1;
   const x=666+Math.sin(j*8.73)* (35+seed*115)+Math.sin(clock+j)*8,y=492-phase*420;
   const a=Math.sin(phase*PI)*env*(.22+seed*.35);
   mote(g,x,y,.55+seed*1.05,a,'#fff1c8');
  }
 }
}
function impactMaterial(A){
 if(blueImpact)return;
 const i=A.images.impact;blueImpact=document.createElement('canvas');blueImpact.width=i.width;blueImpact.height=i.height;
 const q=blueImpact.getContext('2d');q.drawImage(i,0,0);q.globalCompositeOperation='source-atop';q.fillStyle='rgba(48,117,235,.68)';q.fillRect(0,0,i.width,i.height);q.globalCompositeOperation='source-over';
}
function dustMaterial(A){
 const frame=Math.floor(A.clock*24);if(frame===debrisFrame)return;debrisFrame=frame;
 const tm=frame/24,q=debris.getContext('2d'),im=q.createImageData(200,160);
 for(let y=0;y<160;y++)for(let x=0;x<200;x++){
  const u=(x-100)/100,v=(y-80)/80,n=A.sample(x*.85-tm*29,y*.9+tm*18),d=A.sample(x*2.4+n*19+tm*35,y*2.1-tm*26);
  const r=Math.hypot(u,v),edge=S((1-r+(n-.5)*.38)/.55),density=S((n*.68+d*.32-.3)/.46),i=(y*200+x)*4;
  im.data[i]=86+d*101;im.data[i+1]=135+d*93;im.data[i+2]=184+d*65;im.data[i+3]=edge*density*210;
 }q.putImageData(im,0,0);
}
function dust(A,x,y,w,h,a,angle){
 dustMaterial(A);const g=A.g;g.save();g.translate(x,y);g.rotate(angle);g.globalAlpha=C(a);g.drawImage(debris,-w/2,-h/2,w,h);g.restore();
}
function nativeBurst(A,a,x,y,strength,behind){
 if(a<0||a>1.15)return;impactMaterial(A);
 const f=Math.min(63,Math.floor(a*72)),fade=1-S((a-.16)/.85),size=(145+S(a/.3)*115)*strength,g=A.g;
 g.save();g.globalAlpha=fade*(behind?.26:.1);g.translate(x,y);g.rotate(-.2);g.drawImage(blueImpact,f%8*256,Math.floor(f/8)*256,256,256,-size/2,-size*.44,size,size*.88);g.restore();
 if(behind){
  dust(A,x+a*49,y-a*35,(145+a*270)*strength,(120+a*225)*strength,fade*.77,-a*.55);
  A.glow(x,y,135*strength,125*strength,'#387cdb74',Math.exp(-a*7)*.7);return;
 }
 dust(A,x+a*90,y+24,(165+a*240)*strength,(68+a*65)*strength,fade*.48,-.24);
 A.glow(x,y,55*strength,65*strength,'#e4f4ffdb',Math.exp(-Math.pow((a-.025)/.046,2))*.8);
 A.mist(A.clock*.8+a,x+a*40,y+35,210+a*160,110+a*80,fade*.12*strength);
 for(let j=0;j<62;j++){
  const seed=hash(j+2),angle=hash(j+89)*PI*2,velocity=35+hash(j+41)*260;
  const px=x+Math.cos(angle)*velocity*a,py=y+Math.sin(angle)*velocity*a+a*a*145;
  const alpha=(1-S((a-.1-seed*.15)/(.3+seed*.45)))*(.4+seed*.5);
  if(alpha<.002)continue;
  const r=(.35+seed*.85)*strength;
  mote(g,px,py,r,alpha,j%4?'#aed4ff':'#f2f8ff');
 }
}
function projectile(A,j,when,behind){
 const {g,age,variant:v}=A,a=age-when;
 const tx=[647,684,666][j],ty=[273,322,292][j];
 const sx=v===1?[340,880,440][j]:v===2?[430,665,895][j]:[555,740,645][j],sy=-45;
 const strength=v===0?[.74,.91,1.3][j]:v===1?[.9,.9,1.1][j]:.9;
 if(a>=-.34&&a<0&&!behind){
  const p=S((a+.34)/.34),x=mix(sx,tx,p),y=mix(sy,ty,p),dx=tx-sx,dy=ty-sy,angle=Math.atan2(dy,dx);
  const len=35+60*p,alpha=S((a+.34)/.065);
  g.save();g.translate(x,y);g.rotate(angle);g.globalCompositeOperation='screen';g.globalAlpha=alpha;
  const trail=g.createLinearGradient(-len,0,4,0);trail.addColorStop(0,'#295dcc00');trail.addColorStop(.58,'#559bea70');trail.addColorStop(.94,'#c7e7ffd9');trail.addColorStop(1,'#fff');g.fillStyle=trail;
  g.beginPath();g.moveTo(-len,0);g.quadraticCurveTo(-len*.2,-8,4,0);g.quadraticCurveTo(-len*.2,8,-len,0);g.fill();g.restore();
  A.glow(x,y,27,32,'#82bdffb0',alpha*.7);mote(g,x,y,3,alpha,'#f3faff');
 }
 nativeBurst(A,a,tx,ty,strength,behind);
}
function rain(A,behind){
 const {g,t,clock,variant:v,age}=A,build=S((t-.3)/.8),pre=build*(1-S((t-1.04)/.15));
 if(behind&&pre>.001){
  g.save();g.fillStyle=`rgba(1,6,22,${pre*.24})`;g.fillRect(0,0,960,600);g.restore();
  A.mist(clock*.45,666,50,420,130,pre*.13);
  for(let j=0;j<3;j++){
   const x=[555,740,645][j],y=45+Math.sin(clock*1.6+j)*9;
   A.glow(x,y,35+build*12,25+build*11,'#6fa9ff9e',pre*(.45+j*.08));
   mote(g,x,y,1+build*1.7,pre,'#e6f4ff');
   for(let k=0;k<9;k++){const p=(clock*.6+k/9)%1,angle=k*2.4+clock;const r=(1-p)*36;mote(g,x+Math.cos(angle)*r,y+Math.sin(angle)*r*.55,.6,pre*p*.6,'#a6ccff');}
  }
 }
 for(let j=0;j<3;j++)projectile(A,j,events(v)[j],behind);
 if(!behind&&age>=0&&age<1.8){const fade=1-S((age-.5)/1.3);A.glow(666,492,155,22,'#507fce55',fade*.25);}
}
window.EdenLightStars={draw(A,behind){if(A.id==='beam')phare(A,behind);else rain(A,behind)},hits:events};
})();
