/* Wind-up trails are animated soft texture stamps, never stroked circle outlines.
 * The impact reuses the existing native EmberGen export. Isolated lab only. */
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
 A.mist(clock,214,313,175,180,build*release*.07);
}
function strike(A,behind,lag=0,weight=1){
 const {g,t,clock,age,variant:v}=A,a=age-lag,flight=C((t-1.12-lag)/.38);
 if(t>=1.12+lag&&a<0){
  const x=214+flight*452,y=301-Math.sin(flight*PI)*(v===1?40:12);
  if(!behind){A.stream(clock,x-42,y,175+flight*65,52,Math.sin(flight*PI)*.62*weight,-.025);A.mist(clock,x,y,75+flight*45,85,Math.sin(flight*PI)*.3*weight);}
 }
 if(a<0||a>1.25)return;
 const fade=1-S((a-.21)/.82),f=Math.min(63,a*68);
 if(behind){A.sheet('impact',f,671,314,285*weight,208*weight,fade*.52);return;}
 A.sheet('impact',f,675,309,230*weight,172*weight,fade*.26);
 A.mist(clock,680+a*80,304,200+a*190,170+a*65,fade*.15*weight);
 A.glow(666,298,65,92,'#cfdee66b',Math.exp(-Math.pow((a-.035)/.055,2))*.34*weight);
}
function draw(A,behind){
 winding(A,behind);strike(A,behind,0,A.variant===1?1.12:1);
 if(A.variant===2)strike(A,behind,.22,.7);
}
window.EdenMistralSwing={draw};
})();
