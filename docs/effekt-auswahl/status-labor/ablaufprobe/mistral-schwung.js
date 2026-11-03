/* Wind-up trails are animated soft texture stamps, never stroked circle outlines.
 * Evolving vapor and entrained grit form the air impact. Isolated lab only. */
(()=>{'use strict';
const PI=Math.PI,C=x=>Math.max(0,Math.min(1,x)),S=x=>{x=C(x);return x*x*(3-2*x)};
const ribbon=document.createElement('canvas');ribbon.width=128;ribbon.height=40;
let frame=-1;
function material(A){
 const tick=Math.floor(A.clock*30);if(frame===tick)return;frame=tick;
 const q=ribbon.getContext('2d'),im=q.createImageData(128,40),tm=tick/30;
 for(let y=0;y<40;y++)for(let x=0;x<128;x++){
  const u=(x-64)/64,v=(y-20)/20,n=A.sample(x*2.4-tm*83,y*3.2+tm*29),n2=A.sample(x*4+tm*48,y*5-tm*35),envelope=Math.pow(Math.max(0,1-u*u),1.7)*Math.exp(-v*v*7);
  const a=envelope*S((n*.6+n2*.4-.26)/.5),i=(y*128+x)*4;
  im.data[i]=168+n2*50;im.data[i+1]=193+n2*42;im.data[i+2]=202+n2*40;im.data[i+3]=255*a*.8;
 }q.putImageData(im,0,0);
}
const vapor=document.createElement('canvas'),gust=document.createElement('canvas');
vapor.width=192;vapor.height=192;gust.width=320;gust.height=128;
let vaporFrame=-1;
function airMaterial(A){
 const tick=Math.floor(A.clock*24);if(vaporFrame===tick)return;vaporFrame=tick;
 const tm=tick/24;
 for(const [canvas,wide] of [[vapor,false],[gust,true]]){
  const q=canvas.getContext('2d'),w=canvas.width,h=canvas.height,im=q.createImageData(w,h);
  for(let y=0;y<h;y++)for(let x=0;x<w;x++){
   const u=(x/w-.5)*2,v=(y/h-.5)*2;
   const r=Math.hypot(u,v),angle=Math.atan2(v,u)+tm*1.25+(1-r)*2;
   const sx=wide?x*.66-tm*112:Math.cos(angle)*r*91+100;
   const sy=wide?y*1.15+Math.sin(u*5-tm*6)*14:Math.sin(angle)*r*91+100;
   const warp=A.sample(sx*.53+tm*19,sy*.53-tm*13);
   const n=A.sample(sx*.68+warp*27,sy*.68+tm*12);
   const mid=A.sample(sx*1.55-tm*24,sy*1.55+warp*18);
   const fine=A.sample(sx*3.1+tm*33,sy*3.1-tm*19);
   const edge=wide?Math.pow(Math.max(0,1-u*u),1.5)*Math.exp(-v*v*5):S((1-r+(.5-n)*.22)/.52);
   const density=S((n*.58+mid*.29+fine*.13-.27)/.49);
   const shade=C(.35+n*.42+mid*.23-v*.12),i=(y*w+x)*4;
   im.data[i]=102+shade*111;im.data[i+1]=117+shade*106;im.data[i+2]=123+shade*108;
   im.data[i+3]=255*edge*density*(wide?.8:.68);
  }
  q.putImageData(im,0,0);
 }
}
function air(A,canvas,x,y,w,h,opacity,angle=0){
 if(opacity<.002)return;airMaterial(A);const g=A.g;
 g.save();g.translate(x,y);g.rotate(angle);g.globalAlpha=C(opacity);g.drawImage(canvas,-w/2,-h/2,w,h);g.restore();
}
function winding(A,behind){
 const {t,clock,variant:v,g}=A;if(t<.28||t>1.28)return;material(A);
 const build=S((t-.28)/.78),release=1-S((t-1.1)/.18),phase=clock*4.7+clock*clock*1.35;
 for(let orbit=0;orbit<3;orbit++){
  const spin=orbit===1&&v===2?-1:1,rotation=[-.65,.7,-.1][orbit]+v*.2,rx=[104,89,118][orbit]*(v===1?1.17:1),ry=[63,94,43][orbit];
  for(let j=0;j<29;j++){
   const tail=j/28,angle=phase*spin+orbit*2.2-tail*2.8,depth=Math.sin(angle+rotation),rear=depth<0;if(rear!==behind)continue;
   const uneven=1+.06*Math.sin(angle*3+clock*2+orbit),xx=Math.cos(angle)*rx*uneven,yy=Math.sin(angle)*ry*uneven;
   const x=214+xx*Math.cos(rotation)-yy*Math.sin(rotation),y=301+xx*Math.sin(rotation)+yy*Math.cos(rotation);
   const tangent=Math.atan2(ry*Math.cos(angle),-rx*Math.sin(angle))+rotation;
   const alpha=Math.pow(1-tail,1.4)*build*release*(.46+.12*Math.sin(angle*4+clock*6));
   g.save();g.translate(x,y);g.rotate(tangent);g.globalAlpha=alpha;
   const w=34+tail*14,h=(11+build*9)*(1-tail*.45);g.drawImage(ribbon,-w/2,-h/2,w,h);g.restore();
  }
 }
 if(behind){
  air(A,vapor,214,303,146+build*34,138+build*20,build*release*.76,-clock*.3);
  air(A,gust,205,317,168,78,build*release*.24,clock*.7);
 }
}
function strike(A,behind,lag=0,weight=1){
 const {g,t,clock,age,variant:v}=A,a=age-lag,flight=C((t-1.12-lag)/.38);
 if(t>=1.12+lag&&a<0){
  const x=214+flight*452,y=301-Math.sin(flight*PI)*(v===1?40:12);
  if(!behind){
   const force=Math.pow(Math.sin(flight*PI),.55)*weight;
   air(A,gust,x-62,y,235+flight*105,100+flight*25,force*.92,-.025);
   air(A,vapor,x+12,y,68+flight*58,82+flight*40,force*.66,-clock*2);
   air(A,gust,x-100,y+29,210,44,force*.36,-.13);
  }
 }
 if(a<0||a>1.25)return;
 const fade=1-S((a-.21)/.82);
 if(behind){
  air(A,vapor,678+a*105,306,180+a*270,170+a*230,fade*.68*weight,-a*.8);
  A.mist(clock,688+a*150,326,210+a*290,165+a*120,fade*.22*weight);return;
 }
 air(A,gust,678+a*175,310,240+a*265,108+a*170,fade*.68*weight,-.07-a*.12);
 air(A,gust,667+a*110,418,260+a*330,42+a*50,fade*.37*weight,.04);
 // Fine entrained grit follows the air impulse, without graphic speed lines.
 for(let j=0;j<38;j++){
  const seed=((j*73+19)%101)/101,spread=((j*47)%97)/97-.5;
  const x=673+a*(95+seed*330),y=307+spread*64+a*spread*330+a*a*70;
  const life=fade*(1-S((a-.22-seed*.2)/.55));
  g.save();g.globalAlpha=life*.46;g.fillStyle=j%3?'#9ba7a8':'#d3d9d6';
  g.beginPath();g.ellipse(x,y,.65+seed*1.1,.45+seed*.65,a*3+j,0,PI*2);g.fill();g.restore();
 }
 A.glow(666,298,65,92,'#cfdee66b',Math.exp(-Math.pow((a-.035)/.055,2))*.34*weight);
}
function draw(A,behind){
 winding(A,behind);strike(A,behind,0,A.variant===1?1.12:1);
 if(A.variant===2)strike(A,behind,.22,.7);
}
window.EdenMistralSwing={draw};
})();
