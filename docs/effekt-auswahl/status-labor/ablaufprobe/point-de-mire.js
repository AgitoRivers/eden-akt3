/* Isolated target-mark study: light follows the visible figure alpha.
 * No damage, projectiles, UI crosshairs or combat requests. */
(()=>{'use strict';
const PI=Math.PI,C=x=>Math.max(0,Math.min(1,x)),S=x=>{x=C(x);return x*x*(3-2*x)};
const mask=document.createElement('canvas');mask.width=960;mask.height=600;
const grain=document.createElement('canvas');grain.width=grain.height=128;let grainFrame=-1;
function texture(A){
 const tick=Math.floor(A.clock*24);if(tick===grainFrame)return;grainFrame=tick;
 const q=grain.getContext('2d'),im=q.createImageData(128,128),tm=tick/24;
 for(let y=0;y<128;y++)for(let x=0;x<128;x++){
  const u=(x-64)/64,v=(y-64)/64,n=A.sample(x*1.6-tm*22,y*1.6+tm*13),fine=A.sample(x*3.2+tm*17,y*3.2-tm*31);
  const edge=Math.exp(-(u*u*3+v*v*4)),density=S((n*.7+fine*.3-.27)/.55),i=(y*128+x)*4;
  im.data[i]=169+fine*67;im.data[i+1]=219+fine*32;im.data[i+2]=206+fine*43;im.data[i+3]=255*edge*density;
 }q.putImageData(im,0,0);
}
function light(A,x,y,rx,ry,alpha){
 if(alpha<.002)return;const g=A.g;g.save();g.translate(x,y);g.scale(1,ry/rx);g.globalCompositeOperation='screen';g.globalAlpha=C(alpha);
 const grad=g.createRadialGradient(0,0,0,0,0,rx);grad.addColorStop(0,'#e3fff0c9');grad.addColorStop(.13,'#91e1cd80');grad.addColorStop(.5,'#6bbaa632');grad.addColorStop(1,'#6bbaa600');g.fillStyle=grad;g.fillRect(-rx,-rx,rx*2,rx*2);g.restore();
}
function body(A,draw,alpha=1){
 const q=mask.getContext('2d');q.clearRect(0,0,960,600);q.globalCompositeOperation='source-over';q.globalAlpha=1;
 const image=A.images[A.t>.75&&A.age<2.15?'guard':'idle'],h=420,w=h*image.width/image.height;
 draw(q);q.globalCompositeOperation='destination-in';q.drawImage(image,666-w/2,75,w,h);q.globalCompositeOperation='source-over';
 const g=A.g;g.save();g.globalAlpha=alpha;g.globalCompositeOperation='screen';g.drawImage(mask,0,0);g.restore();
}
function scan(A,env){
 const {t,clock,variant:v}=A,progress=S((t-.34)/.88),end=1-S((t-1.17)/.22);
 if(end<.002)return;
 body(A,q=>{
  let gradient;
  if(v===0){const y=115+progress*310;gradient=q.createLinearGradient(0,y-25,0,y+25);}
  if(v===1){const x=575+progress*190;gradient=q.createLinearGradient(x-24,240,x+24,260);}
  if(v===2){const y=130+progress*145;gradient=q.createLinearGradient(0,y-32,0,y+32);}
  gradient.addColorStop(0,'#6eb4aa00');gradient.addColorStop(.38,'#8bd8c366');gradient.addColorStop(.5,'#e4fff1db');gradient.addColorStop(.62,'#8bd8c366');gradient.addColorStop(1,'#6eb4aa00');q.fillStyle=gradient;q.fillRect(0,0,960,600);
  if(v===2){const yy=420-progress*145,second=q.createLinearGradient(0,yy-24,0,yy+24);second.addColorStop(0,'#9cddca00');second.addColorStop(.5,'#d7ffe4bd');second.addColorStop(1,'#9cddca00');q.fillStyle=second;q.fillRect(0,0,960,600);}
 },env*end*.78);
}
function focus(A,env){
 const {g,t,age,clock,variant:v}=A,settle=S((t-.82)/.63),arrival=Math.exp(-Math.pow((age-.04)/.13,2));
 const finalX=[660,678,651][v],finalY=[250,284,265][v];
 const x=finalX+(1-settle)*(v===1?-50:Math.sin(clock*2)*30),y=finalY+(1-settle)*(v===0?65:v===1?25:-45);
 const pulse=.78+.14*Math.sin(clock*3.9)+.08*Math.sin(clock*7.1),strength=env*(.22+settle*.4+arrival*.27);
 texture(A);
 body(A,q=>{
  q.fillStyle='#000';q.fillRect(0,0,960,600);
  q.save();q.translate(x,y);q.rotate(-.4+Math.sin(clock*.6)*.12);q.globalAlpha=.42+arrival*.25;q.drawImage(grain,-52,-70,104,140);q.restore();
  const core=q.createRadialGradient(x,y,0,x,y,32);core.addColorStop(0,'#e9fff2');core.addColorStop(.09,'#caf5ddce');core.addColorStop(.28,'#7bcbb97a');core.addColorStop(1,'#539d8f00');q.fillStyle=core;q.fillRect(x-32,y-32,64,64);
 },strength*pulse);
 light(A,x,y,52+arrival*17,65+arrival*20,strength*.37);
 // A small, soft highlight identifies the lock without a drawn target symbol.
 g.save();g.globalCompositeOperation='screen';g.globalAlpha=env*settle*(.5+arrival*.35)*pulse;g.translate(x,y);g.rotate(-.38);
 const glint=g.createRadialGradient(0,0,0,0,0,12);glint.addColorStop(0,'#f2fff4');glint.addColorStop(.12,'#d9ffe6cb');glint.addColorStop(.42,'#7fd5bb40');glint.addColorStop(1,'#7fd5bb00');g.fillStyle=glint;g.scale(1,.36);g.fillRect(-12,-12,24,24);g.restore();
 for(let j=0;j<20;j++){
  const p=(clock*.38+j*.618)%1,angle=j*2.39996+clock*.2,r=(1-p)*(22+(j%5)*6);
  const opacity=env*settle*Math.sin(p*PI)*.29;
  g.save();g.globalAlpha=opacity;g.fillStyle='#caecdc';g.beginPath();g.arc(x+Math.cos(angle)*r,y+Math.sin(angle)*r*1.35,.45+(j%3)*.18,0,PI*2);g.fill();g.restore();
 }
}
window.EdenPointDeMire={draw(A,behind){
 const env=S((A.t-.28)/.7)*(1-S((A.age-1.5)/.68));if(env<.002)return;
 if(behind){A.mist(A.clock*.5,666,300,200,250,env*.04);return;}
 scan(A,env);focus(A,env);
}};
})();
