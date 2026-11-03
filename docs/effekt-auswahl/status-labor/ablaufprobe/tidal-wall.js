/* Lame de Fond: native LiquiGen wave sequence, isolated stage only. */
(()=>{'use strict';
const C=x=>Math.max(0,Math.min(1,x)),S=x=>{x=C(x);return x*x*(3-2*x)},PI=Math.PI;
// 64 newly simulated LiquiGen frames. No generated still or mesh deformation.
const material=document.createElement('canvas');material.width=1024;material.height=640;
function wall(A){
 const {g,t,age}=A;if(t<.28||age>1.2)return;
 const rise=S((t-.3)/.8),flight=S((t-1.12)/.38),f=t<1.12?rise*25:t<1.5?25+flight*20:45+C(age/1.05)*18;
 const a=S((t-.28)/.18)*(1-S((age-.45)/.75)),i=A.images.tidalNative,q=material.getContext('2d'),n=Math.floor(f),blend=f-n;
 q.clearRect(0,0,1024,640);q.globalCompositeOperation='source-over';q.globalAlpha=1-blend;q.drawImage(i,n%8*1024,Math.floor(n/8)*640,1024,640,0,0,1024,640);
 if(blend>0){const next=Math.min(63,n+1);q.globalCompositeOperation='lighter';q.globalAlpha=blend;q.drawImage(i,next%8*1024,Math.floor(next/8)*640,1024,640,0,0,1024,640);}q.globalAlpha=1;q.globalCompositeOperation='source-over';
 // The captured wave moves across the frame itself; only mirror its travel direction.
 const height=390+rise*460;
 g.save();g.globalAlpha=a*.96;g.translate(1160,665);g.scale(-1,1);g.drawImage(material,0,-height,1360,height);g.restore();
}
function draw(A,behind){
 const {g,t,age,clock}=A,build=S((t-.3)/.75);
 if(behind){
  if(t>.3&&age<.4){
   // Three low streams gather inward; no hard circular ground boundary.
   const fade=(1-S(Math.max(0,age)/.4))*build;
   for(let j=0;j<3;j++)A.sheet('jet',18+((clock*19+j*11)%30),275+j*67,493+j*2,170,45,fade*.34,[-.06,.01,.06][j]);
  }
  wall(A);return;
 }
 if(age<-.02||age>1.85)return;
 const a=Math.max(0,age),burst=S(a/.085)*(1-S((a-.45)/.85));
 // A broad, animated impact with the native water motion; no rigid floor decal.
 // Immediate body impact, followed by a separate, lower sheet of spray.
 const blast=S(a/.035)*(1-S((a-.2)/.78)),f=27+C(a/.95)*36;
 A.sheet('jet',f,683+a*52,297,560+a*90,410+a*30,blast*.98,.04);
 const shoulder=S((a-.035)/.07)*(1-S((a-.22)/.61));
 A.sheet('jet',32+C(a/.85)*31,687+a*90,260,345+a*65,300,shoulder*.68,-.78);
 const floorBlast=S((a-.09)/.11)*(1-S((a-.48)/.8));
 A.sheet('jet',29+C(a/1.25)*34,535+a*75,485,1080+a*80,185,floorBlast*.78,.09,true);
 A.mist(clock,550+a*85,390,960+a*120,260,burst*.15);
 // Fine droplets follow ballistic paths; thin highlights, no drawn streak outlines.
 for(let i=0;i<104;i++){
  const n=(Math.sin(i*91.73)*43758.5)%1+.5,speed=90+Math.abs(n)*195,angle=i*2.399;
  const life=1-S((a-(.26+(i%7)*.04))/.55);if(a>1.2||life<.002)continue;
  const px=666+Math.cos(angle)*speed*a*1.7+a*60,py=299+Math.sin(angle)*speed*a-a*100+a*a*210;
  g.save();g.globalAlpha=life*S(a/.035)*.66;g.translate(px,py);g.rotate(angle);g.fillStyle='#c9e6ec';g.beginPath();g.ellipse(0,0,1.2+(i%4)*.5,.8,0,0,PI*2);g.fill();g.restore();
 }
}
window.EdenTidalWall={draw};
})();
