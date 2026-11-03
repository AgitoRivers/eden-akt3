/* Continuous water rises and forms a shield. No splash textures or spray particles. */
(()=>{'use strict';
const PI=Math.PI,C=x=>Math.max(0,Math.min(1,x)),S=x=>{x=C(x);return x*x*(3-2*x)};
const surface=document.createElement('canvas');surface.width=224;surface.height=320;let frame=-1;
function material(A){
 const tick=Math.floor(A.clock*24);if(frame===tick)return;frame=tick;
 const build=S((A.t-.3)/.8),tm=tick/24,q=surface.getContext('2d'),im=q.createImageData(224,320);
 for(let y=0;y<320;y++)for(let x=0;x<224;x++){
  const u=(x-112)/112,v=(y-160)/160,n=A.sample(x*.78-tm*27,y*.82+tm*40),fine=A.sample(x*1.8+n*18+tm*19,y*1.7-tm*35);
  const nx=A.sample(x*.78-tm*27+3,y*.82+tm*40)-n,ny=A.sample(x*.78-tm*27,y*.82+tm*40+3)-n;
  const yy=y/320,cap=yy<.19?Math.sqrt(Math.max(0,1-Math.pow((yy-.19)/.19,2))):1;
  const width=yy<.19?cap*.95:yy<.62?.95-(yy-.19)*.24:.847*Math.pow(Math.max(0,(1-yy)/.38),.72);
  const relative=Math.abs(u+(n-.5)*.015)/Math.max(.008,width),head=1-build,filled=S((yy-head+.035)/.065);
  const r=Math.min(1,relative),edge=(1-S((relative-.91)/.09))*filled*S(yy/.025)*(1-S((yy-.98)/.02));if(edge<=0)continue;
  const z=Math.sqrt(Math.max(0,1-r*r)),fresnel=Math.pow(C(r),7),rim=Math.exp(-Math.pow((r-.9-(n-.5)*.055)/.037,2));
  const light=C(.35-u*.22-v*.2+nx*.95-ny*.6),crease=Math.pow(C(.5+nx*2-ny*1.5),5)*(.3+fine*.7);
  const reflection=Math.exp(-Math.pow((u+.43+(n-.5)*.08)/.075,2))*S((v+.7)/.35)*(1-S((v-.25)/.45));
  const meniscus=Math.exp(-Math.pow((yy-head-.008)/.017,2))*(1-S((build-.91)/.09)),caustic=Math.pow(Math.max(0,Math.sin(u*11+v*3+tm*2.3+n*3)),10)*(.25+fine*.75),sparkle=crease*(.08+fresnel*.32),i=(y*224+x)*4;
  im.data[i]=61+light*104+rim*24+reflection*50+caustic*42+meniscus*45;im.data[i+1]=125+light*81+rim*22+reflection*40+caustic*36+meniscus*38;im.data[i+2]=145+light*76+rim*20+reflection*35+caustic*32+meniscus*32;
  im.data[i+3]=255*edge*(.11+z*.1+fresnel*.12+rim*(.035+n*.1)*S((fine-.18)/.5)+sparkle*.17+reflection*.21+caustic*.16+meniscus*.32);
 }q.putImageData(im,0,0);
}
window.EdenBonacciaShield={draw(A,behind){
 const {g,t,clock,age,variant:v}=A,build=S((t-.3)/.8),fade=1-S((age-.85)/.95),env=build*fade;
 if(env<.002)return;
 const x=v===1?748:694,y=282,w=v===1?180:v===2?318:292,h=v===1?422:438,angle=v===1?-.15:v===2?Math.sin(clock*.7)*.055:-.035;
 if(behind)return;
 material(A);g.save();g.translate(x,y);g.rotate(angle);g.globalAlpha=env;
 g.drawImage(surface,-w/2,-h/2,w,h);
 g.restore();
}};
})();
