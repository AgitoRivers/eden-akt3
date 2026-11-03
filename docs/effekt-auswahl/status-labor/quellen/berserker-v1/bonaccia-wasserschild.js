/* Native LiquiGen water, with a separate 2D gathering choreography. Lab only. */
(()=>{'use strict';
const C=x=>Math.max(0,Math.min(1,x)),S=x=>{x=C(x);return x*x*(3-2*x)};
const surface=document.createElement('canvas');
function water(A,f){
 const image=A.images.shieldNative,w=image.width/8,h=image.height/8;
 if(surface.width!==w||surface.height!==h){surface.width=w;surface.height=h;}
 const q=surface.getContext('2d'),n=Math.floor(f),blend=f-n;
 q.clearRect(0,0,w,h);q.globalCompositeOperation='source-over';q.globalAlpha=1-blend;
 q.drawImage(image,n%8*w,Math.floor(n/8)*h,w,h,0,0,w,h);
 if(blend>0){const k=Math.min(63,n+1);q.globalCompositeOperation='lighter';q.globalAlpha=blend;q.drawImage(image,k%8*w,Math.floor(k/8)*h,w,h,0,0,w,h);}
 q.globalAlpha=1;q.globalCompositeOperation='source-over';return {q,w,h};
}
window.EdenBonacciaShield={draw(A,behind){
 if(behind)return;
 const {g,clock,age,variant:v}=A,build=S((clock-.3)/1.9),fade=1-S((age-.85)/.95);
 if(clock<=.3||fade<.002)return;
 const f=18+C((clock-.3)/3.15)*45,{w,h}=water(A,f);
 const x=v===1?748:694,y=282,dw=v===1?195:v===2?332:302,dh=422,angle=v===1?-.13:v===2?.025*Math.sin(clock*.7):-.025;
 // Keep the water nucleus at the shield centre; expand equally in every direction.
 g.save();g.translate(x,y);g.rotate(angle);g.globalAlpha=fade*.68*S((clock-.3)/.2);
 const spread=.045+.955*build,rw=dw*spread,rh=dh*spread;
 g.drawImage(surface,-rw/2,-rh/2,rw,rh);
 // Rounded drops gather inward rather than spraying outward. Same native water material.
 if(build<.998)for(let j=0;j<14;j++){
  const p=C((clock-.3-j*.065)/1.3);if(p<=0||p>=1)continue;
  const side=j%2?1:-1,a=j*2.399963,endX=Math.cos(a)*dw*.16*build,endY=Math.sin(a)*dh*.16*build;
  const px=Math.cos(a)*dw*.6*(1-S(p))+endX*S(p),py=Math.sin(a)*dh*.47*(1-S(p))+endY*S(p);
  const rx=5+(j%4)*1.3,ry=rx*(1.15+Math.sin(p*Math.PI)*.75);
  g.save();g.translate(px,py);g.rotate(side*(.2+p*.4));g.globalAlpha=fade*S(p/.13)*(1-S((p-.76)/.24))*.86;
  g.beginPath();g.ellipse(0,0,rx,ry,0,0,Math.PI*2);g.clip();
  g.drawImage(surface,w*.27,h*.18,w*.4,h*.34,-rx,-ry,rx*2,ry*2);
  const shine=g.createRadialGradient(-rx*.4,-ry*.35,.2,0,0,ry);
  shine.addColorStop(0,'#edffffda');shine.addColorStop(.18,'#d6f6ff90');shine.addColorStop(.48,'#39748718');shine.addColorStop(.85,'#102c4660');shine.addColorStop(1,'#bde9f8a0');g.fillStyle=shine;g.fillRect(-rx,-ry,rx*2,ry*2);g.restore();
 }
 g.restore();
}};
})();
