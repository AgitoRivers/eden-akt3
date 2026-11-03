/* Berserker visual studies. Existing animated fire and steel materials; no battle rules executed. */
(()=>{'use strict';
const C=x=>Math.max(0,Math.min(1,x)),S=x=>{x=C(x);return x*x*(3-2*x)},PI=Math.PI;
const blade=document.createElement('canvas');blade.width=640;blade.height=120;
const end=(a,d)=>a<0?0:S(a/.045)*(1-S((a-d*.55)/(d*.45)));
let stacks=3;
function flame(A,x,foot,w,h,alpha,phase=0){
 if(alpha<.002)return;
 A.sheet('fire',8+((A.clock*23+phase*13)%48),x,foot-h/2,w,h,alpha);
}
function embers(A,x,y,alpha,scale=1,phase=0){
 const g=A.g;if(alpha<.002)return;
 g.save();g.globalCompositeOperation='screen';
 for(let j=0;j<48;j++){
  const p=((A.clock*.65+j*.618+phase)%1),a=j*2.399+phase;
  const xx=x+Math.cos(a)*(18+p*80)*scale,yy=y+Math.sin(a)*30*scale-p*145*scale;
  g.globalAlpha=alpha*Math.sin(p*PI)*(.4+(j%3)*.16);g.fillStyle=j%4?'#fa9f46':'#fff3ce';
  g.beginPath();g.ellipse(xx,yy,.7+(j%3)*.4,1.2+(j%4)*.45,-a,0,PI*2);g.fill();
 }g.restore();
}
function slash(A,offset,index=0,weight=1){
 const a=A.age-offset,p=(a+.15)/.28;if(p<=0||p>=1.65)return;
 const g=A.g,q=blade.getContext('2d'),image=A.images.stahl,b=A.crops.stahl;
 const length=405*weight,height=20*weight,head=110+p*length,tail=length*.75;
 q.clearRect(0,0,640,120);q.globalCompositeOperation='source-over';q.globalAlpha=1;
 q.drawImage(image,b[0],b[1],b[2]-b[0],b[3]-b[1],head-tail,60-height/2,tail,height);
 q.globalCompositeOperation='source-atop';q.fillStyle=A.variant===1?'#ea5a20':'#ffc870';q.globalAlpha=.72;q.fillRect(0,0,640,120);
 q.globalAlpha=1;q.globalCompositeOperation='destination-in';const mask=q.createLinearGradient(head-tail,0,head,0);
 mask.addColorStop(0,'#fff0');mask.addColorStop(.43,'#fffb');mask.addColorStop(.9,'#ffff');mask.addColorStop(1,'#fff0');q.fillStyle=mask;q.fillRect(0,0,640,120);q.globalCompositeOperation='source-over';
 const angles=A.variant===0?[.2,-.26,.35,-.38,.1]:A.variant===1?[-.65,.58,-.42,.35,-.6]:[.82,-.85,.1,.64,-.58];
 g.save();g.translate(666,280+(index%2)*25);g.rotate(angles[index%5]);if(index%2)g.scale(-1,1);g.globalAlpha=1-S((a-.08)/.24);g.drawImage(blade,-320,-60);g.restore();
}
function impact(A,offset,index=0,weight=1){
 const a=A.age-offset,env=end(a,.85);if(!env)return;
 const g=A.g;g.save();g.filter='sepia(1) saturate(2.8)';
 A.sheet('impact',C(a/.72)*63,670+a*36,298,260*weight,195*weight,env*.8);
 g.restore();
 flame(A,671,405,175*weight,240*weight,env*.77,index);
 A.glow(666,295,110*weight,135*weight,'#ff9a384f',Math.exp(-Math.pow((a-.035)/.08,2))*.8);
 embers(A,666,310,env,.95*weight,index*.7);
}
function incoming(A){
 const when=A.launch-.95,a=A.clock-when,env=end(a,.65);
 if(a>-.35&&a<.1){
  const p=C((a+.35)/.4),g=A.g,i=A.images.stahl,b=A.crops.stahl;
  g.save();g.globalAlpha=Math.sin(p*PI)*.55;g.translate(650-p*470,290);g.rotate(-.12);g.drawImage(i,b[0],b[1],b[2]-b[0],b[3]-b[1],-65,-7,130,14);g.restore();
 }
 if(env){A.glow(180,295,83,125,'#fa674f65',env*.7);A.sheet('impact',C(a/.6)*63,180,300,190,170,env*.6);}
 flame(A,180,488,120,220,S((a+.02)/.2)*(1-S((A.age-.65)/.9))*.5,1);
}
function draw(A,behind){
 if(behind)return;
 const {id,age,clock,variant:v}=A,g=A.g,charge=S((clock-.3)/Math.max(.3,A.launch-.3))*(1-S((age+.2)/.4));
 if(id==='retour')incoming(A);
 const rage=id==='furia'?S((clock-.3)/.32)*(1-S((age-1.05)/.9)):0;
 const strength=id==='vulcano'?1.05:id==='scirocco'?.58:id==='retour'?.8:.7;
 flame(A,180,493,125+v*18,220+v*22,(charge*strength+rage*.48)*.63,v);
 embers(A,180,325,charge*.75+rage*.6,1,v*.4);
 if(id==='retour'&&A.flight>0&&A.flight<1){
  const x=215+A.flight*440;
  flame(A,x,354,100+A.flight*35,160,.75,2);
  embers(A,x,300,.5,.55);
 }
 const hits=A.hitOffsets;
 hits.forEach((offset,index)=>{slash(A,offset,index,id==='vulcano'?1.06:id==='retour'?1.03:1);impact(A,offset,index,id==='vulcano'?.85+index*.1:1);});
 if(age>=0&&id!=='vulcano')flame(A,668,493,140,240,S(age/.12)*(1-S((age-1.35)/.7))*.44,v+3);
 if(id==='vulcano'){
  const remaining=hits.filter(h=>age<h+.16).length,env=S((clock-.3)/1)*(1-S((age-Math.max(...hits)-.3)/.8));
  flame(A,668,493,165,200+remaining*27,env*(.24+remaining*.09),1);
  if(age>Math.max(...hits)+.15){const rest=end(age-Math.max(...hits)-.15,.9);embers(A,666,350,rest,.8);}
 }
 // A quiet caption explains the price; these are visual states, never live combat mutations.
 const caption=id==='scirocco'&&age>=0?'Ungedeckt · Gegner +1 Brandstufe':id==='retour'&&clock>A.launch-.95?'Voller Gegentreffer · Duc +1 Brandstufe':id==='furia'&&clock>.35?'Flammenrausch · Duc brennt · kein Verteidigen':id==='vulcano'&&age>Math.max(...hits)+.25?'Brandstufen verbraucht · danach 1 Runde aussetzen':'';
 if(caption){g.save();g.font='13px system-ui';g.textAlign='center';g.fillStyle='#e8b67e';g.fillText(caption,480,565);g.restore();}
}
window.EdenBerserker={draw,get stacks(){return stacks},set stacks(n){stacks=Math.max(1,Math.min(5,Math.round(n)))},hits(){return Array.from({length:stacks},(_,i)=>i*.48)}};
})();
