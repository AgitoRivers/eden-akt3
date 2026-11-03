/* Transparent moving water shield. Existing native liquid detail, no damage. */
(()=>{'use strict';
const PI=Math.PI,C=x=>Math.max(0,Math.min(1,x)),S=x=>{x=C(x);return x*x*(3-2*x)};
const surface=document.createElement('canvas');surface.width=224;surface.height=320;let frame=-1;
function material(A){
 const tick=Math.floor(A.clock*24);if(frame===tick)return;frame=tick;
 const tm=tick/24,q=surface.getContext('2d'),im=q.createImageData(224,320);
 for(let y=0;y<320;y++)for(let x=0;x<224;x++){
  const u=(x-112)/112,v=(y-160)/160,n=A.sample(x*.78-tm*27,y*.82+tm*40),fine=A.sample(x*1.8+n*18+tm*19,y*1.7-tm*35);
  const nx=A.sample(x*.78-tm*27+3,y*.82+tm*40)-n,ny=A.sample(x*.78-tm*27,y*.82+tm*40+3)-n;
  const r=Math.hypot(u,v)+(n-.5)*.026,edge=1-S((r-.935)/.065);if(edge<=0)continue;
  const z=Math.sqrt(Math.max(0,1-r*r)),fresnel=Math.pow(C(r),7),rim=Math.exp(-Math.pow((r-.9-(n-.5)*.055)/.037,2));
  const light=C(.35-u*.22-v*.2+nx*.95-ny*.6),crease=Math.pow(C(.5+nx*2-ny*1.5),5)*(.3+fine*.7);
  const reflection=Math.exp(-Math.pow((u+.43+(n-.5)*.08)/.075,2))*S((v+.7)/.35)*(1-S((v-.25)/.45));
  const caustic=Math.pow(Math.max(0,Math.sin(u*17+v*4+tm*2.3+n*3)),12)*(.25+fine*.75),sparkle=crease*(.08+fresnel*.32),i=(y*224+x)*4;
  im.data[i]=70+light*96+rim*24+reflection*50+caustic*42;im.data[i+1]=126+light*78+rim*22+reflection*40+caustic*36;im.data[i+2]=144+light*73+rim*20+reflection*35+caustic*32;
  im.data[i+3]=255*edge*(.065+z*.075+fresnel*.13+rim*(.04+n*.12)*S((fine-.18)/.5)+sparkle*.17+reflection*.17+caustic*.14);
 }q.putImageData(im,0,0);
}
window.EdenBonacciaShield={draw(A,behind){
 const {g,t,clock,age,variant:v}=A,build=S((t-.3)/.8),fade=1-S((age-.85)/.95),env=build*fade;
 if(env<.002)return;
 const x=v===1?748:694,y=282,w=v===1?180:v===2?318:292,h=v===1?422:438,angle=v===1?-.15:v===2?Math.sin(clock*.7)*.055:-.035;
 if(behind){A.mist(clock*.6,675,490,290,38,env*.08);return;}
 material(A);g.save();g.translate(x,y);g.rotate(angle);g.globalAlpha=env;
 g.drawImage(surface,-w/2,-h/2,w,h);
 // Low-opacity native LiquiGen detail moves inside the curved protective surface.
 g.save();g.beginPath();g.ellipse(0,0,w*.455,h*.46,0,0,PI*2);g.clip();
 A.sheet('jet',Math.floor(clock*27)%64,0,5,w*.96,h*.98,env*.28,.12);
 if(v===2)A.sheet('jet',Math.floor(clock*25+23)%64,-28,-32,w*.7,h*.7,env*.1,-.38);
 g.restore();
 // Small beads skim the liquid edge instead of forming a solid neon outline.
 for(let j=0;j<54;j++){
  const phase=j*2.399+clock*(.25+(j%3)*.06),radius=.91+.025*Math.sin(clock*3+j),xx=Math.cos(phase)*w*.5*radius,yy=Math.sin(phase)*h*.5*radius;
  const opacity=env*(.2+.25*Math.sin(j*8+clock*5)**2);
  g.save();g.globalAlpha=opacity;g.fillStyle=j%5?'#a8d6db':'#e0f4f2';g.beginPath();g.ellipse(xx,yy,.5+(j%3)*.3,.7+(j%4)*.4,phase,0,PI*2);g.fill();g.restore();
 }
 g.restore();
 // Grounded runoff, kept small and continuously animated.
 A.sheet('jet',Math.floor(clock*24+18)%64,x,490,w*1.08,55,env*.2,.02);
}};
})();
