/* Two native EmberGen sequences; separate charge/release choreography for the isolated lab. */
(()=>{'use strict';
const C=x=>Math.max(0,Math.min(1,x)),S=x=>{x=C(x);return x*x*(3-2*x)},PI=Math.PI,ids=new Set(['scirocco','retour','furia','vulcano']);
const end=(a,d)=>a<0?0:S(a/.035)*(1-S((a-d*.55)/(d*.45))),tm=A=>A.animationClock??A.clock;
let stacks=3,mode='full';
function frame(A,name,f){const i=A.images[name],w=i.width/8,h=i.height/8,n=Math.max(0,Math.min(63,Math.floor(f)));return {i,w,h,x:n%8*w,y:Math.floor(n/8)*h};}
function native(A,name,f,x,y,w,h,a=1,angle=0){
 if(a<.002)return;const b=frame(A,name,f),g=A.g;g.save();g.globalAlpha=C(a);g.translate(x,y);g.rotate(angle);g.drawImage(b.i,b.x,b.y,b.w,b.h,-w/2,-h/2,w,h);g.restore();
}
function ball(A,x,y,r,a=1,phase=0,stretch=1){native(A,'emberBall',(tm(A)*26+phase*11)%64,x,y,r*2*stretch,r*1.9,a,phase*.15);}
function sparks(A,x,y,a=1,spread=1,inward=false,phase=0){
 const g=A.g;if(a<.002)return;g.save();g.globalCompositeOperation='screen';
 for(let j=0;j<86;j++){
  const seed=Math.sin(j*12.9898+phase*17)*43758.5453,p=(tm(A)*.62+seed-Math.floor(seed))%1,ang=j*2.399+Math.sin(j*7.3)*.8+phase,q=inward?1-p:p;
  const xx=x+Math.cos(ang)*(15+q*100)*spread,yy=y+Math.sin(ang)*65*spread-(inward?0:p*p*130*spread);
  g.globalAlpha=a*Math.sin(p*PI)*(.35+j%4*.13);g.fillStyle=j%5?'#ff9c38':'#fff2bf';g.beginPath();g.ellipse(xx,yy,.7+j%3*.32,1.1+j%4*.4,ang,0,2*PI);g.fill();
 }g.restore();
}
// A continuous ribbon samples moving flame detail; no drawn outline or steel stripe.
function ribbon(A,path,start,stop,width,alpha,phase=0,side=null){
 if(stop<=start||alpha<.002)return;const g=A.g,b=frame(A,'emberBall',(tm(A)*27+phase*13)%64),n=Math.max(10,Math.ceil((stop-start)*72));
 g.save();g.globalAlpha=alpha;
 for(let j=0;j<n;j++){
  const u=start+(stop-start)*j/n,v=start+(stop-start)*(j+1)/n,p=path(u),q=path(v);
  if(side!==null&&p[2]!==undefined&&((p[2]>=0)!==side))continue;
  const dx=q[0]-p[0],dy=q[1]-p[1],len=Math.hypot(dx,dy),taper=Math.sin(PI*(j+.5)/n)**.45;
  g.save();g.translate(p[0],p[1]);g.rotate(Math.atan2(dy,dx));
  const moving=frame(A,'emberBall',(tm(A)*27+phase*13+j*3.7)%64),thick=width*taper*(.9+.16*Math.sin(j*2.3+tm(A)*4));
  g.globalAlpha=alpha*.63;
  g.drawImage(moving.i,moving.x,moving.y,moving.w,moving.h,-len*1.4,-thick/2,len*3.9,thick);g.restore();
 }g.restore();
}
function blast(A,a,index=0,scale=1,shape=0){
 const env=end(a,1.38);if(!env)return;
 const w=(shape===1?550:shape===2?320:400)*scale,h=(shape===1?300:shape===2?570:410)*scale;
 native(A,'emberBlast',Math.min(63,6+a*43),670,300,w,h,env*.96);
 A.glow(666,300,145*scale,160*scale,'#ff9d3845',Math.exp(-Math.pow((a-.04)/.085,2))*.72);
 sparks(A,666,310,env*.85,1.1*scale,false,index*.7);
}
function fireSlash(A,a,index=0,weight=1){
 const p=(a+.13)/.29;if(p<=0||p>=1.65)return;
 const angles=A.variant===0?[.23,-.32,.39,-.4,.1]:A.variant===1?[-.64,.58,-.42,.36,-.6]:[.84,-.85,.12,.64,-.58],ang=angles[index%5],flip=index%2?-1:1;
 const path=u=>{const x=(u-.5)*405*weight*flip,y=Math.sin(u*PI)*5;return [666+x*Math.cos(ang)-y*Math.sin(ang),294+x*Math.sin(ang)+y*Math.cos(ang)];};
 const head=C(p),tail=Math.max(0,head-.77);ribbon(A,path,tail,head,32*weight,(1-S((a-.1)/.27))*.94,index);
}
function bodyCharge(A,amount,kind='charge'){
 const v=A.variant,t=tm(A),env=amount*S((A.clock-.2)/.3);if(env<.002)return;
 A.glow(181,298,80+env*30,128,kind==='rage'?'#da582a3d':'#dd622e36',env*.85);
 // One coherent torso field; persistent rage uses rising flames instead of repeated orbs.
 if(kind==='rage'){
  native(A,'fire',8+(t*24)%48,154,355,123,315,env*.45);
  native(A,'fire',8+(t*24+21)%48,211,386,95,235,env*.35);
 }else native(A,'emberBall',(t*24)%64,182,291,120,210,env*.21);
 sparks(A,180,307,env,.83,v!==1,v*.8);
 if(v===1)ribbon(A,u=>{const a=u*PI*2+t*1.9;return [180+Math.cos(a)*65,310+Math.sin(a)*84];},0,.89,14,env*.45,1);
 if(v===2){ball(A,151,300,16+env*10,env*.42,2);ball(A,210,302,16+env*10,env*.42,3);}
}
function sciroccoCharge(A){
 if(A.age>=-.26)return;const v=A.variant,build=S((A.clock-.25)/Math.max(.4,A.launch-.5)),env=S((A.clock-.2)/.24)*(1-S((A.age+.38)/.14));
 const r=(v===1?71:v===2?48:57)*(.14+.86*build),x=224,y=v===1?235:270;
 ball(A,x,y,r,env,0);sparks(A,x,y,env*.9,.9,true,v);
 A.glow(x,y,r*1.35,r*1.35,'#ffb43b45',env*.5);
}
function sciroccoRelease(A){
 const v=A.variant,p=A.flight;
 if(p>0&&p<1){
  const pos=u=>[224+u*442,(v===1?235:270)+(300-(v===1?235:270))*u];
  ribbon(A,pos,Math.max(0,p-.28),p,v===1?43:27,.58,v);
  const xy=pos(p);ball(A,xy[0],xy[1],v===1?70:v===2?43:55,.98,v,p>.3?1.1:1);
 }
 blast(A,A.age,0,v===1?1.17:v===2?.95:1,v);
 if(A.age>=.2)native(A,'fire',8+(tm(A)*21)%48,668,389,150,215,end(A.age-.15,1.8)*.4);
}
function incoming(A){
 if(A.previewMode!=='full')return;const a=A.clock-(A.launch-.95),env=end(a,.65);if(!env)return;
 native(A,'impact',C(a/.6)*63,180,300,190,170,env*.57);A.glow(180,295,85,130,'#fb76564d',env);
}
function storm(A,behind){
 const v=A.variant,t=tm(A),build=S((A.clock-.25)/Math.max(.6,A.launch-.4)),last=Math.max(...A.hitOffsets),env=build*(1-S((A.age-last-.12)/.7));
 if(env<.003)return;
 const growth=.25+.75*build,spin=t*(v===1?-2.6:2.1),width=(28+build*35)*(.8+stacks*.055);
 if(behind){
  if(v===0)native(A,'emberBall',(t*23)%64,666,317,280*growth,395*growth,env*.41);
  if(v===1)for(let k=0;k<2;k++)native(A,'emberBall',(t*23+k*23)%64,666+(k?1:-1)*106*growth,320,195*growth,365*growth,env*.43,k?.2:-.2);
  if(v===2)native(A,'emberBall',(t*23)%64,666,155+(1-build)*170,320*growth,150*growth,env*.55);
 }
 const count=v===1?36:32;
 for(let j=0;j<count;j++){
  const u=j/(count-1),a=spin+u*PI*(v===1?5.8:5),depth=Math.sin(a);
  if((depth>=0)===behind)continue;
  let x,y,w,h;
  if(v===0){const radius=(62+u*65)*growth;x=666+Math.cos(a)*radius;y=480-u*365*growth;w=(150+u*78)*growth;h=w*1.04;}
  else if(v===1){const sign=j%2?1:-1;x=666+sign*(130-u*45)*growth+Math.cos(a)*46;y=478-u*350*growth;w=(150+u*72)*growth;h=w*1.1;}
  else{x=666+Math.cos(a)*(140-u*62)*growth;y=150+(1-build)*170+Math.sin(a)*49+u*70;w=(112+u*34)*growth;h=w*.9;}
  native(A,'emberBall',(t*25+j*7.3)%64,x,y,w,h,env*(behind?.43:.65),Math.sin(a)*.28);
 }
 if(!behind){sparks(A,666,385,env,1.45,false,v);A.glow(666,475,210,40,'#df702b35',env*.75);}
}
function whip(A){
 const a=A.age,p=C((a+.43)/.43);if(a<-.43||a>.58)return;
 const v=A.variant,travel=u=>{
  const wave=Math.sin(u*PI)*(v===0?Math.sin(u*PI*2-a*7)*65:v===1?-155*Math.sin(u*PI):Math.sin(u*PI*3-a*7)*86);
  return [210+456*u,300+wave*(1-S((a+.04)/.42))];
 };
 const tail=Math.max(0,p-(a>0?.92:.77));ribbon(A,travel,tail,p,38+v*6,(1-S((a-.09)/.49))*.95,v);
 if(a>=0){blast(A,a,0,.75,v===1?2:0);sparks(A,666,300,end(a,.9),1.15);}
}
function charge(A,behind=false){
 if(A.id==='vulcano'){storm(A,behind);if(!behind)bodyCharge(A,S((A.clock-.25)/1.8)*(1-S((A.age+.15)/.25)));return;}
 if(behind)return;
 if(A.id==='scirocco'){sciroccoCharge(A);return;}
 if(A.id==='retour'){bodyCharge(A,S((A.clock-.2)/1.9)*(1-S((A.age+.1)/.35)));incoming(A);return;}
 if(A.id==='furia')bodyCharge(A,S((A.clock-.15)/.7)*(1-S((A.age-1.8)/.8)),'rage');
}
function release(A){
 if(A.previewMode==='charge')return;
 if(A.id==='scirocco'){sciroccoRelease(A);return;}
 if(A.id==='retour'){fireSlash(A,A.age,0,1.1);blast(A,A.age,0,1.04,A.variant);return;}
 if(A.id==='furia'){whip(A);return;}
 A.hitOffsets.forEach((h,j)=>{fireSlash(A,A.age-h,j,1.1);blast(A,A.age-h,j,j===0?1.23:.78+j*.045,A.variant);});
}
function draw(A,behind){
 charge(A,behind);if(behind)return;release(A);
 const caption=A.id==='scirocco'&&A.age>=0?'Ungedeckt · Gegner +1 Brandstufe':A.id==='retour'?'Phase 1: Funkenladung halten · Phase 2: Konter entladen':A.id==='furia'?'Brennzustand: 3 Runden · Angriff: Feuerpeitsche':A.id==='vulcano'&&A.age>Math.max(...A.hitOffsets)+.25?'Brandstufen entladen · danach 1 Runde aussetzen':'';
 if(caption&&A.clock>.2){const g=A.g;g.save();g.font='13px system-ui';g.textAlign='center';g.fillStyle='#e8ba88';g.fillText(caption,480,566);g.restore();}
}
window.EdenBerserker={draw,drawCharge:charge,drawRelease:release,supports:id=>ids.has(id),modeFor:id=>ids.has(id)?mode:'full',get mode(){return mode},set mode(v){mode=['charge','release'].includes(v)?v:'full'},get stacks(){return stacks},set stacks(n){stacks=Math.max(1,Math.min(5,Math.round(n)))},hits(){return Array.from({length:stacks},(_,i)=>i*.48)}};
})();
