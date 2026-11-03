/* Weapon-independent violet body charge for Doppio Gioco. Preview only. */
(()=>{'use strict';
const S=x=>{x=Math.max(0,Math.min(1,x));return x*x*(3-2*x)},PI=Math.PI;
const vapor=document.createElement('canvas');vapor.width=144;vapor.height=192;let frame=-1;
function energy(A){
 const first=A.launch+.38+A.hitOffsets[0]-.15,second=A.launch+.38+A.hitOffsets[1]-.15,t=A.clock;
 if(t<first)return S((t-.24)/(first-.24))*(.93+.07*Math.sin(t*14));
 if(t<second)return .95-.61*S((t-first)/.1)+.35*S((t-first-.1)/Math.max(.04,second-first-.1));
 return .69*(1-S((t-second)/.13));
}
function material(A){
 const tick=Math.floor(A.clock*24);if(frame===tick)return;frame=tick;
 const q=vapor.getContext('2d'),im=q.createImageData(144,192),tm=tick/24;
 for(let y=0;y<192;y++)for(let x=0;x<144;x++){
  const u=(x-72)/72,v=(y-96)/96,warp=A.sample(x*.8-tm*21,y*.8+tm*14),n=A.sample(x*.92+warp*20,y*.87+tm*41),fine=A.sample(x*2.4+tm*27,y*2.1-tm*39);
  const edge=Math.exp(-Math.pow(u+(n-.5)*.22,2)*3.4-v*v*2.8),density=S((n*.68+fine*.32-.27)/.55),i=(y*144+x)*4;
  im.data[i]=122+fine*75;im.data[i+1]=57+fine*62;im.data[i+2]=190+fine*58;im.data[i+3]=edge*density*214;
 }q.putImageData(im,0,0);
}
window.EdenDoppioCharge={energy,draw(A,{image,anchor,scale}){
 const charge=energy(A);if(charge<.002)return;material(A);
 // Normalized upper-body anchor; there are no blade masks, weapon paths or pose-specific polygons.
 const g=A.g,cx=0,cy=-anchor.foot*scale+image.height*scale*.405;
 g.save();g.globalAlpha*=charge*.78;g.drawImage(vapor,cx-73,cy-100,146,200);g.restore();
 g.save();g.globalCompositeOperation='screen';g.globalAlpha*=charge*.29;
 const glow=g.createRadialGradient(cx,cy,0,cx,cy,88);glow.addColorStop(0,'#b273e86b');glow.addColorStop(.35,'#9246ce4a');glow.addColorStop(1,'#632aa600');g.fillStyle=glow;g.fillRect(cx-88,cy-88,176,176);g.restore();
 // Soft shoulder wisps converge into the chest instead of following equipment.
 for(let j=0;j<32;j++){
  const p=(A.clock*(.47+j%4*.045)+j*.618)%1,angle=j*2.399+A.clock*.35;
  const rx=18+(1-p)*(37+j%3*7),ry=24+(1-p)*65;
  const x=cx+Math.cos(angle)*rx,y=cy+Math.sin(angle)*ry;
  g.save();g.globalAlpha*=charge*Math.sin(p*PI)*.48;g.fillStyle=j%5?'#c296ed':'#e5c9ff';g.beginPath();g.arc(x,y,.4+j%3*.2,0,PI*2);g.fill();g.restore();
 }
}};
})();
