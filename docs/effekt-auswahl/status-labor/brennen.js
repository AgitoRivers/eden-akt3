/* Native Oil Fire body layers shared by the isolated status and attack previews. */
(()=>{'use strict';
const C=x=>Math.max(0,Math.min(1,x)),S=x=>{x=C(x);return x*x*(3-2*x)},PI=Math.PI;
function frame(g,image,n,w,h,alpha){
 if(alpha<.002)return;const cw=image.width/8,ch=image.height/8;n=Math.max(0,Math.min(63,n));
 g.globalAlpha=alpha;g.drawImage(image,n%8*cw,Math.floor(n/8)*ch,cw,ch,-w/2,-h,w,h);
}
function patch(g,image,time,x,foot,w,h,alpha,phase){
 if(alpha<.002)return;const p=((time*27+phase)%56+56)%56,n=Math.floor(p),fraction=p-n,join=S((p-48)/8);
 g.save();g.translate(x,foot);
 frame(g,image,8+n,w,h,alpha*(1-fraction)*(1-join));frame(g,image,Math.min(63,9+n),w,h,alpha*fraction*(1-join));
 if(join>0){frame(g,image,n-48,w,h,alpha*(1-fraction)*join);frame(g,image,n-47,w,h,alpha*fraction*join)}g.restore();
}
function draw({g,image,time,x=666,foot=495,scale=1,intensity=1,seed=0},behind=false){
 if(!image||intensity<.003)return;const strength=C(intensity),t=time+seed*.37;
 // Separate anchored fire pockets share native flow, with different phases and heights.
 const pockets=behind?[[-39,-2,122,305,.69,8],[43,-25,106,267,.66,31]]:[[-25,-7,104,160,.74,0],[38,-104,79,177,.63,21],[-38,-205,68,145,.5,43]];
 for(const [dx,dy,w,h,alpha,phase] of pockets){const breath=.93+.07*Math.sin(t*1.6+phase*.17)+.035*Math.sin(t*3.3+phase);patch(g,image,t*(phase===31?.92:1),x+dx*scale,foot+dy*scale,w*scale,h*scale,alpha*strength*breath,phase)}
 if(behind){
  g.save();g.globalAlpha=strength*.19;g.translate(x,foot-115*scale);g.scale(1,1.45);const light=g.createRadialGradient(0,0,0,0,0,104*scale);light.addColorStop(0,'#ff8d2b85');light.addColorStop(.45,'#c74a2030');light.addColorStop(1,'#b43b1500');g.fillStyle=light;g.fillRect(-105*scale,-105*scale,210*scale,210*scale);g.restore();return;
 }
 g.save();g.globalCompositeOperation='screen';
 for(let j=0;j<62;j++){
  const p=((t*(.31+j%7*.019)+j*.618)%1+1)%1,noise=Math.sin(j*127.1)*43758.5453,random=noise-Math.floor(noise),side=(random-.5)*120*scale;
  const xx=x+side+Math.sin(p*5+j)*p*13*scale,yy=foot-(25+p*(230+random*100))*scale,a=Math.sin(p*PI)*strength*(.2+random*.55);
  g.globalAlpha=a;g.fillStyle=j%6?'#f5943b':'#fff0bd';g.beginPath();g.ellipse(xx,yy,(.4+random*.75)*scale,(.6+random)*scale,.2,0,PI*2);g.fill();
 }g.restore();
}
window.EdenOrganicBurn={draw};
})();
