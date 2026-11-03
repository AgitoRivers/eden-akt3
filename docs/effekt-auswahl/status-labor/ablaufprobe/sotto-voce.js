/* Isolated sound-pressure study; no damage or combat-rule changes. */
(()=>{'use strict';
const PI=Math.PI,C=x=>Math.max(0,Math.min(1,x)),S=x=>{x=C(x);return x*x*(3-2*x)};
const orb=document.createElement('canvas');orb.width=orb.height=224;let frame=-1;
function voice(t){return .52+.23*Math.sin(t*18)+.15*Math.sin(t*31+.8)+.1*Math.sin(t*9.4);}
function material(A){
 const tick=Math.floor(A.clock*30);if(frame===tick)return;frame=tick;
 const tm=tick/30,q=orb.getContext('2d'),im=q.createImageData(224,224),amplitude=voice(tm);
 for(let y=0;y<224;y++)for(let x=0;x<224;x++){
  const u=(x-112)/112,v=(y-112)/112,r=Math.hypot(u,v),theta=Math.atan2(v,u),i=(y*224+x)*4;
  if(r>1.03)continue;
  const n=A.sample(x*.8-tm*34,y*.8+tm*21),d=A.sample(x*2+n*14+tm*16,y*2-tm*29);
  const depth=Math.sqrt(Math.max(0,1-r*r)),warped=r+(n-.5)*.028+Math.sin(theta*3+tm*3)*.007;
  const shell=Math.exp(-Math.pow((warped-.77)/.074,2));
  const pressure=Math.pow(Math.max(0,Math.sin((u*.48+v*.27+depth*.82)*24-tm*16+(n-.5)*1.5)),5)*(1-S((r-.56)/.41))*(.45+d*.55);
  const cloud=S((n*.7+d*.3-.4)/.48)*(1-S((r-.45)/.49));
  const light=C(.55-u*.26-v*.31),envelope=1-S((r-.88)/.12);
  const highlight=Math.exp(-((u+.29)*(u+.29)+(v+.4)*(v+.4))/.075);
  const alpha=(shell*(.12+light*.22)*(.65+d*.35)+pressure*(.08+amplitude*.12)+cloud*.2+depth*light*.075+highlight*.13)*envelope;
  im.data[i]=179+light*65;im.data[i+1]=188+light*61;im.data[i+2]=190+light*60;im.data[i+3]=255*alpha;
 }q.putImageData(im,0,0);
}
function sphere(A,x,y,r,a,stretch=1){
 if(a<.002)return;material(A);const g=A.g;
 g.save();g.translate(x,y);g.globalAlpha=C(a);g.drawImage(orb,-r*stretch,-r,r*2*stretch,r*2);g.restore();
}
function reflection(A,x,y,r,a){
 const g=A.g;g.save();g.translate(x,y);g.scale(1,.2);const grad=g.createRadialGradient(0,0,0,0,0,r);grad.addColorStop(0,`rgba(201,221,224,${a})`);grad.addColorStop(1,'rgba(201,221,224,0)');g.fillStyle=grad;g.fillRect(-r,-r,r*2,r*2);g.restore();
}
function ghost(A,dx,alpha){
 const i=A.images.guard,h=420,w=h*i.width/i.height,g=A.g;
 g.save();g.globalAlpha=alpha;g.filter='blur(1.3px)';g.drawImage(i,666-w/2+dx,75,w,h);g.restore();
}
function charge(A,behind){
 const {g,t,clock,variant:v}=A;if(t<.28||t>1.18)return;
 const build=S((t-.28)/.76),release=1-S((t-1.1)/.08),env=build*release;
 if(behind){A.mist(clock*.7,214,304,110+build*80,100+build*65,env*.075);reflection(A,214,493,80+build*45,env*.13);return;}
 const beat=voice(clock),r=22+build*(v===2?51:40)+beat*3;
 sphere(A,214,300,r,env*.96,v===2?1.08:1);
 // Small airborne grains converge into the pressure field, rather than magic glyphs.
 for(let j=0;j<28;j++){
  const p=(clock*(.45+(j%4)*.05)+j*.618)%1,angle=j*2.399+clock*.45,d=r*.5+(1-p)*(75-r*.3);
  const x=214+Math.cos(angle)*d,y=300+Math.sin(angle)*d*.84;
  g.save();g.globalAlpha=env*Math.sin(p*PI)*.28;g.fillStyle='#d7e3e4';g.beginPath();g.arc(x,y,.45+(j%3)*.2,0,PI*2);g.fill();g.restore();
 }
}
function release(A,behind,lag=0,weight=1){
 const {t,age,clock,variant:v,g}=A,a=age-lag,flight=C((t-1.12-lag)/.38);
 if(t>=1.12+lag&&a<0&&!behind){
  const x=214+flight*452,y=300-Math.sin(flight*PI)*(v===1?17:4),r=(v===2?64:53)*weight;
  sphere(A,x,y,r,(1-S((flight-.94)/.06))*.98,1.12+flight*.25);
  for(let j=1;j<=3;j++){const tail=C(flight-j*.065);sphere(A,214+tail*452,300,r*(.76-j*.1),Math.sin(flight*PI)*(.11-j*.022),.7);}
 }
 if(a<0||a>1.65)return;
 const fade=1-S((a-.16)/1.3),shock=S(a/.055)*(1-S((a-.25)/.42));
 if(behind){
  sphere(A,666,295,(68+a*(v===2?245:185))*weight,shock*.48,v===2?1.3:.78);
  A.mist(clock,670+a*60,308,180+a*200,160+a*100,fade*.11*weight);
  ghost(A,Math.sin(clock*83)*5,fade*.12*weight);ghost(A,-Math.sin(clock*83)*7,fade*.08*weight);
  return;
 }
 sphere(A,666+a*22,295,(60+a*135)*weight,shock*.25,.65);
 reflection(A,666,493,120+a*70,fade*.11*weight);
 // Fleeting pressure shimmer crosses the body; no damaging explosion or Hurt.
 const flash=Math.exp(-Math.pow((a-.045)/.07,2));
 A.glow(666,295,62,100,'#dae4e64a',flash*.2*weight);
}
window.EdenSottoVoce={draw(A,behind){charge(A,behind);release(A,behind,0,A.variant===2?1.12:1);if(A.variant===1)release(A,behind,.18,.65)}};
})();
