/* Purple charge attached to the actual sabre pose, not a floating effect.
 * Native-pixel blade masks retain the photographed metal texture. */
(()=>{'use strict';
const S=x=>{x=Math.max(0,Math.min(1,x));return x*x*(3-2*x)},PI=Math.PI,cache={};
const shapes={
 windup:[[654,624],[695,546],[745,440],[782,327],[810,178],[818,225],[810,312],[788,401],[752,493],[712,575],[678,640]],
 attack:[[549,620],[639,614],[729,585],[834,533],[806,575],[741,612],[654,636],[550,651]],
 heavy_attack:[[758,705],[780,714],[739,810],[674,905],[582,989],[477,1037],[526,990],[608,915],[688,814]]
};
const axes={windup:[[666,627],[768,430],[811,190]],attack:[[552,634],[722,621],[827,542]],heavy_attack:[[770,714],[700,911],[486,1030]]};
function energy(A){
 const first=A.launch+.38+A.hitOffsets[0]-.15,second=A.launch+.38+A.hitOffsets[1]-.15,t=A.clock;
 if(t<first)return S((t-.24)/(first-.24))*(.93+.07*Math.sin(t*14));
 if(t<second)return .95-.61*S((t-first)/.1)+.35*S((t-first-.1)/Math.max(.04,second-first-.1));
 return .69*(1-S((t-second)/.13));
}
function material(pose,image){
 if(cache[pose])return cache[pose];const points=shapes[pose];if(!points)return null;
 const c=document.createElement('canvas');c.width=image.width;c.height=image.height;const q=c.getContext('2d');
 q.beginPath();points.forEach(([x,y],j)=>j?q.lineTo(x,y):q.moveTo(x,y));q.closePath();
 q.save();q.shadowColor='#8b36e5';q.shadowBlur=24;q.fillStyle='#9a48e0a8';q.fill();q.restore();
 q.save();q.clip();q.drawImage(image,0,0);q.globalCompositeOperation='source-atop';
 const color=q.createLinearGradient(480,1000,810,180);color.addColorStop(0,'#5a1e8d91');color.addColorStop(.5,'#9e4de9ac');color.addColorStop(1,'#d0a4ff9c');q.fillStyle=color;q.fillRect(0,0,c.width,c.height);q.restore();
 cache[pose]=c;return c;
}
function point(pose,t){const [p,c,e]=axes[pose],a=1-t;return [a*a*p[0]+2*a*t*c[0]+t*t*e[0],a*a*p[1]+2*a*t*c[1]+t*t*e[1]];}
window.EdenDoppioCharge={energy,draw(A,{pose,image,anchor,scale}){
 const charge=energy(A),layer=material(pose,image);if(!layer||charge<.002)return;
 const g=A.g;g.save();g.globalAlpha*=charge*.86;g.drawImage(layer,-image.width*scale/2,-anchor.foot*scale,image.width*scale,image.height*scale);g.restore();
 // Converging specks and travelling glints use the same pose coordinates as the blade.
 for(let j=0;j<23;j++){
  const progress=(A.clock*(.55+j%3*.08)+j*.618)%1,along=(j*.381966)%1,[sx,sy]=point(pose,along);
  const angle=j*2.399+A.clock*.7,d=(1-progress)*(18+(j%5)*5),x=sx+Math.cos(angle)*d,y=sy+Math.sin(angle)*d;
  g.save();g.globalAlpha*=charge*Math.sin(progress*PI)*.55;g.fillStyle=j%5?'#c497ee':'#e1c6ff';
  g.beginPath();g.arc(-image.width*scale/2+x*scale,-anchor.foot*scale+y*scale,.38+j%3*.18,0,PI*2);g.fill();g.restore();
 }
 const p=(A.clock*.74)%1,[x,y]=point(pose,p);
 g.save();g.globalAlpha*=charge*.37;g.translate(-image.width*scale/2+x*scale,-anchor.foot*scale+y*scale);
 const light=g.createRadialGradient(0,0,0,0,0,11);light.addColorStop(0,'#e8ceffbb');light.addColorStop(.25,'#b873ec70');light.addColorStop(1,'#8b40dc00');g.fillStyle=light;g.fillRect(-11,-11,22,22);g.restore();
}};
})();
