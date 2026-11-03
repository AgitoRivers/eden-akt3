/* Omerta: body charge, disappearance, two downward cuts, native EmberGen shockwave. */
(()=>{'use strict';
const C=x=>Math.max(0,Math.min(1,x)),S=x=>{x=C(x);return x*x*(3-2*x)},PI=Math.PI;
const random=n=>{const p=Math.sin(n*127.1+91.7)*43758.5453;return p-Math.floor(p)};
const blade=document.createElement('canvas');blade.width=640;blade.height=128;
const material=document.createElement('canvas');material.width=640;material.height=128;let prepared=false;
const hits=()=>[-.16,.18,.5];
function visibility(A){if(A.id!=='blackSlash'||!A.shown)return 1;return 1-S((A.clock-A.launch+.2)/.24)+S((A.clock-A.launch-1.75)/.5)}
function native(A,f,x,y,w,h,alpha,angle=0){
 if(alpha<.002)return;const image=A.images.omertaShock;if(!image)return;
 f=Math.max(0,Math.min(63,Math.floor(f)));const cw=image.width/8,ch=image.height/8,g=A.g;
 g.save();g.globalAlpha=C(alpha);g.translate(x,y);g.rotate(angle);g.drawImage(image,f%8*cw,Math.floor(f/8)*ch,cw,ch,-w/2,-h/2,w,h);g.restore();
}
function prepare(A){
 if(prepared)return;const q=material.getContext('2d'),im=A.images.stahl,b=A.crops.stahl;
 q.drawImage(im,b[0],b[1],b[2]-b[0],b[3]-b[1],40,38,560,52);
 const pixels=q.getImageData(0,0,640,128);for(let k=0;k<pixels.data.length;k+=4){const l=Math.max(pixels.data[k],pixels.data[k+1],pixels.data[k+2])/255;pixels.data[k]=255*l;pixels.data[k+1]=(183+60*l)*l;pixels.data[k+2]=(47+151*l)*l}q.putImageData(pixels,0,0);prepared=true;
}
function sparks(A,x,y,age,inward=false,amount=1){
 const g=A.g;if(amount<.002)return;g.save();g.globalCompositeOperation='screen';
 for(let j=0;j<(inward?100:220);j++){
  const seed=random(j+13),ang=random(j+67)*PI*2,p=inward?(A.clock*(.36+seed*.3)+seed)%1:C(age/(1.1+seed*1.4)),travel=inward?(1-p)*(40+seed*100):(1-Math.exp(-age*3.1))*(35+seed*245);
  const x2=x+Math.cos(ang)*travel,y2=y+Math.sin(ang)*travel*(inward?1.2:.7)+(inward?0:age*age*(18+seed*24));
  const fade=inward?Math.sin(p*PI):1-S((age-.4-seed*.45)/(1+seed*.7)),twinkle=.25+.75*Math.pow(.5+.5*Math.sin(A.clock*(10+seed*12)+j),9);
  g.globalAlpha=amount*fade*(inward?.55:(j%4===0?.9:twinkle*.65));g.fillStyle=j%4?'#e6b953':'#fff4c9';
  const r=.35+seed*(inward?1.1:1.4);g.beginPath();g.ellipse(x2,y2,r,r*.65,ang,0,PI*2);g.fill();
  if(!inward&&age<.42&&j%5===0){g.strokeStyle='#ffdc8f';g.lineWidth=.65;g.beginPath();g.moveTo(x2,y2);g.lineTo(x2-Math.cos(ang)*(4+seed*14)*(1-age/.42),y2-Math.sin(ang)*(4+seed*14)*(1-age/.42));g.stroke()}
 }g.restore();
}
function charge(A){
 const build=S((A.clock-.3)/(A.launch-.65)),fade=1-S((A.clock-A.launch+.18)/.22),env=build*fade;
 if(env>.002){
  native(A,23+(A.clock*10)%9,181,292,190+build*30,310+build*22,env*.48);
  A.glow(180,295,70+build*20,125,'#e8bc633c',env*.6);sparks(A,181,296,0,true,env);
 }
 const vanish=A.clock-(A.launch-.22);if(vanish>=0&&vanish<.65)native(A,2+vanish*47,181,302,245,340,(1-S((vanish-.15)/.5))*.6);
 const back=A.clock-(A.launch+1.65);if(back>=0&&back<.85)native(A,24-back*16,181,312,225,320,(1-S(back/.85))*.3);
}
function cut(A,when,angle,index){
 const p=C((A.age-when+.14)/.24),fade=1-S((A.age-.72)/.52);if(!p||fade<.002)return;
 prepare(A);const q=blade.getContext('2d'),length=[420,470,430][A.variant],left=320-length/2,head=left+p*length;
 q.clearRect(0,0,640,128);q.globalCompositeOperation='source-over';q.drawImage(material,40,0,560,128,left,0,length,128);q.globalCompositeOperation='destination-in';
 const mask=q.createLinearGradient(left-1,0,head+1,0);mask.addColorStop(0,'#fff0');mask.addColorStop(.045,'#ffff');mask.addColorStop(.97,'#ffff');mask.addColorStop(1,'#fff0');q.fillStyle=mask;q.fillRect(left-1,0,head-left+2,128);q.clearRect(head+1,0,640,128);q.globalCompositeOperation='source-over';
 const g=A.g;g.save();g.globalAlpha=fade*(index?.98:.88);g.translate(666,294);g.rotate(angle);g.drawImage(blade,-320,-64);g.restore();
 const flash=Math.exp(-Math.pow((A.age-when)/.045,2));A.glow(666,294,72,90,'#fff0b5',flash*.45);
}
function draw(A,behind){
 const a=A.age-.5,v=A.variant,g=A.g,build=S((A.clock-.35)/(A.launch-.55));
 if(behind){
  const dim=build*(1-S((a-.22)/1.1));if(dim>0){g.save();g.fillStyle=`rgba(2,5,10,${dim*.28})`;g.fillRect(0,0,960,600);g.restore()}
  if(a>=0&&a<1.8)native(A,1+a*23,666,302,[660,770,600][v],[610,490,670][v],.24*(1-S((a-1)/.7)),v===1?.12:0);
  return;
 }
 charge(A);
 const angles=v===1?[.52,2.62]:v===2?[.98,2.16]:[.76,2.38];cut(A,-.16,angles[0],0);cut(A,.18,angles[1],1);
 if(a>=0&&a<2.5){
  native(A,1+a*23,666,302,[660,770,600][v],[610,490,670][v],.98*(1-S((a-1.1)/.8)),v===1?.12:0);
  A.glow(666,300,170,155,'#ffe7a1',Math.exp(-Math.pow((a-.045)/.065,2))*.5);
  sparks(A,666,305,a,false,S(a/.035));
 }
}
window.EdenOmerta={draw,visibility,hits};
})();
