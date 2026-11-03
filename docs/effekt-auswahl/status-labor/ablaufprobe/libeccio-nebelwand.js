/* Rough, advected fog wall for Libeccio variant 0. Preview only.
 * Coordinates use the existing self-effect translation to Duc on the left. */
(()=>{'use strict';
const C=x=>Math.max(0,Math.min(1,x)),S=x=>{x=C(x);return x*x*(3-2*x)};
const wall=document.createElement('canvas');wall.width=256;wall.height=320;let frame=-1;
function material(A){
 const tick=Math.floor(A.clock*24);if(tick===frame)return;frame=tick;
 const tm=tick/24,q=wall.getContext('2d'),im=q.createImageData(256,320);
 for(let y=0;y<320;y++)for(let x=0;x<256;x++){
  const u=(x-128)/128,v=y/320;
  const warp=A.sample(x*.45-tm*12,y*.44+tm*19),coarse=A.sample(x*.36+warp*35-tm*19,y*.42-tm*23);
  const mid=A.sample(x*.91+coarse*27-tm*31,y*.82+warp*19-tm*38),fine=A.sample(x*2.2+tm*23,y*2.1-tm*43);
  const wobble=Math.sin(v*8+tm*1.9)*.08+(coarse-.5)*.16;
  const width=.5+.2*Math.sin(v*5.4+1.3)+.15*warp;
  const side=1-S((Math.abs(u+wobble)-width*.58)/(.33+coarse*.15));
  const cap=S((v-.025+(coarse-.5)*.12)/.22),foot=1-S((v-.87)/.13);
  const density=S((coarse*.54+mid*.34+fine*.12-.26)/.52);
  const light=C(.35+mid*.3+fine*.12-u*.16-v*.07),i=(y*256+x)*4;
  im.data[i]=105+light*111;im.data[i+1]=119+light*107;im.data[i+2]=121+light*106;
  im.data[i+3]=255*side*cap*foot*density*.88;
 }q.putImageData(im,0,0);
}
window.EdenLibeccioFog={draw(A,behind){
 if(!behind)return;
 const {g,t,age,clock}=A,build=S((t-.28)/.65),fade=1-S((age-.9)/.95),env=build*fade;
 if(env<.002)return;material(A);
 // Broad irregular column, softly rising into place, never a rectangular curtain.
 const lift=1-S((t-.3)/.85),height=425+build*55;
 g.save();g.globalAlpha=env*.93;g.drawImage(wall,666-207,43+lift*105,414,height);g.restore();
 // Independently moving native fog breaks up the surface and broadens the base.
 A.mist(clock*.77,585+Math.sin(clock*.7)*12,345,185,280,env*.19);
 A.mist(clock*.63+.9,745+Math.sin(clock*.8)*10,278,210,310,env*.17);
 A.mist(clock*.61,657,470,390,92,env*.26);
}};
})();
