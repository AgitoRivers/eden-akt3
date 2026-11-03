/* Local white glare at the target's eyes; isolated visual feedback only. */
(()=>{'use strict';
const C=x=>Math.max(0,Math.min(1,x)),S=x=>{x=C(x);return x*x*(3-2*x)},PI=Math.PI;
function bloom(g,x,y,w,h,alpha){
 if(alpha<.002)return;g.save();g.translate(x,y);g.scale(w,h);g.globalAlpha=C(alpha);
 const light=g.createRadialGradient(0,0,0,0,0,1);light.addColorStop(0,'#fff');light.addColorStop(.16,'#fff');light.addColorStop(.4,'#f6faffad');light.addColorStop(1,'#f6faff00');g.fillStyle=light;g.fillRect(-1,-1,2,2);g.restore();
}
function draw(g,age,x,y,strength=1,variant=0){
 if(age<-.2||age>2.05)return;
 const flash=S((age+.18)/.13)*(1-S((age-.1)/.4)),after=S((age+.03)/.16)*(1-S((age-.55)/1.5));
 g.save();g.globalCompositeOperation='screen';
 bloom(g,x,y,64+flash*27,46+flash*18,flash*.97*strength);
 bloom(g,x,y,117+flash*34,4+flash*3,flash*.9*strength);
 bloom(g,x+Math.sin(age*3)*2,y,37,30,after*.38*strength);
 if(age<.15){const p=S((age+.2)/.35),gap=(1-p)*(variant===1?80:48);bloom(g,x-gap,y-5,17,8,Math.sin(p*PI)*.5*strength);if(variant!==2)bloom(g,x+gap,y+3,17,8,Math.sin(p*PI)*.5*strength)}
 for(let j=0;j<20;j++){
  const seed=((j*71+17)%101)/101,a=age-.03-seed*.14;if(a<0)continue;
  const env=(1-S((a-.25)/1.25))*S(a/.08),angle=j*2.399,r=12+a*(14+seed*22);
  bloom(g,x+Math.cos(angle)*r,y+Math.sin(angle)*r*.55-a*9,1+seed*1.4,1+seed*.7,env*(.16+seed*.36)*strength);
 }g.restore();
}
window.EdenBlindGlare={draw};
})();
