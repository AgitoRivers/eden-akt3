/* Eden Rise dice effects. Procedural background only; no changes to dice artwork. */
class EdenDiceEffects {
  constructor(canvas, stage, anchor, options = {}) {
    this.canvas=canvas;this.stage=stage;this.anchor=anchor;this.ctx=canvas.getContext('2d');
    this.options=Object.assign({intensity:1,duration:5600},options);
    this.motion=matchMedia('(prefers-reduced-motion: reduce)');
    this.kind=null;this.frame=0;this.started=0;this.age=0;this.running=false;this.canvas.dataset.state='idle';
    this.resizeObserver=new ResizeObserver(()=>{this.resize();if(this.kind)this.paint(this.age);});
    this.resizeObserver.observe(stage);
    this.onMotion=()=>{if(this.motion.matches)this.stop();};
    this.motion.addEventListener('change',this.onMotion);
    this.resize();
  }
  resize(){
    const box=this.stage.getBoundingClientRect(),center=this.anchor.getBoundingClientRect();
    this.w=box.width;this.h=box.height;this.cx=center.left-box.left+center.width/2;this.cy=center.top-box.top+center.height/2;
    const dpr=Math.min(devicePixelRatio||1,2);this.canvas.width=Math.round(this.w*dpr);this.canvas.height=Math.round(this.h*dpr);this.ctx.setTransform(dpr,0,0,dpr,0,0);
  }
  clear(){this.ctx.clearRect(0,0,this.w,this.h);}
  stop(){cancelAnimationFrame(this.frame);this.running=false;this.kind=null;this.clear();this.canvas.dataset.state='idle';}
  play(kind){
    this.stop();if(this.motion.matches||this.options.intensity===0)return;
    this.kind=kind==='20'?'sun':'fire';this.canvas.dataset.state='running';this.canvas.dataset.effect=this.kind;
    let seed=kind==='20'?523:917;
    const random=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};
    this.particles=Array.from({length:82},()=>({x:random(),y:random(),size:.8+random()*2.4,delay:random()*1.1,life:2.3+random()*2.5,angle:random()*Math.PI*2,drift:(random()-.5)*100}));
    this.running=true;this.started=performance.now();this.age=0;
    const tick=(now)=>{this.age=now-this.started;if(!this.canvas.isConnected){this.destroy();return;}if(this.age>this.options.duration){this.stop();return;}this.paint(this.age);this.frame=requestAnimationFrame(tick);};
    this.frame=requestAnimationFrame(tick);
  }
  glow(x,y,r,inner,outer){const c=this.ctx,g=c.createRadialGradient(x,y,0,x,y,r);g.addColorStop(0,inner);g.addColorStop(1,outer);c.fillStyle=g;c.fillRect(x-r,y-r,r*2,r*2);}
  paint(age){
    this.clear();if(!this.kind||this.motion.matches)return;
    const seconds=age/1000,c=this.ctx;
    const fade=Math.min(1,seconds/.22)*Math.min(1,(this.options.duration-age)/1250);
    c.save();c.globalAlpha=Math.max(0,fade)*this.options.intensity;
    if(this.kind==='sun')this.sun(seconds);else this.fire(seconds);
    c.restore();
  }
  sun(t){
    const c=this.ctx,x=this.cx,y=this.cy,r=Math.min(this.w*.66,390);
    this.glow(x,y,r,'rgba(249,176,67,.35)','rgba(249,176,67,0)');
    c.save();c.translate(x,y);c.rotate(t*.045);
    const g=c.createRadialGradient(0,0,65,0,0,r);g.addColorStop(0,'rgba(255,217,143,.03)');g.addColorStop(.5,'rgba(255,204,112,.15)');g.addColorStop(1,'rgba(255,184,65,0)');c.fillStyle=g;c.filter='blur(2px)';
    for(let i=0;i<26;i++){const a=i*Math.PI*2/26,w=i%2?.025:.058,length=r*(i%3?.83:1);c.beginPath();c.moveTo(Math.cos(a-w)*75,Math.sin(a-w)*75);c.lineTo(Math.cos(a-w)*length,Math.sin(a-w)*length);c.lineTo(Math.cos(a+w)*length,Math.sin(a+w)*length);c.lineTo(Math.cos(a+w)*75,Math.sin(a+w)*75);c.closePath();c.fill();}
    c.restore();
    if(t<1.15){c.save();c.globalAlpha*=Math.max(0,1-t/1.15)*.55;c.strokeStyle='#e8b96a';c.lineWidth=1.4;c.beginPath();c.ellipse(x,y+110,75+t*190,17+t*42,0,0,Math.PI*2);c.stroke();c.restore();}
    for(const p of this.particles){const time=t-p.delay;if(time<0||time>p.life)continue;const progress=time/p.life;const distance=90+progress*(105+p.y*130);const px=x+Math.cos(p.angle)*distance,py=y+Math.sin(p.angle)*distance-progress*60;
      c.save();c.globalAlpha*=Math.sin(progress*Math.PI)*.85;c.fillStyle='#ffe8a4';c.beginPath();c.arc(px,py,p.size*(1-progress*.6),0,Math.PI*2);c.fill();
      if(p.size>2.3){c.strokeStyle='#ffdf8c';c.lineWidth=.8;c.beginPath();c.moveTo(px-4,py);c.lineTo(px+4,py);c.moveTo(px,py-4);c.lineTo(px,py+4);c.stroke();}c.restore();}
  }
  fire(t){
    const c=this.ctx,x=this.cx,y=this.cy,spread=Math.min(205,this.w*.39),base=y+130;
    this.glow(x,base,Math.min(this.w*.6,340),'rgba(232,64,9,.36)','rgba(130,29,8,0)');
    for(let i=0;i<9;i++){const side=i%2?-1:1,px=x+side*(100+i*12)+Math.sin(t*.8+i)*17,py=y+20-i*19-t*12,r=37+i*5;this.glow(px,py,r,'rgba(107,92,84,.16)','rgba(56,45,40,0)');}
    for(let i=0;i<19;i++){
      const px=x-spread+2*spread*i/18,width=13+(i%4)*5;
      const height=90+Math.sin(i*2.8+t*2.5)*22+Math.abs((i-9)/9)*80;
      const sway=Math.sin(t*2.4+i*1.7)*19;
      const g=c.createLinearGradient(0,base,0,base-height);g.addColorStop(0,'rgba(179,37,6,0)');g.addColorStop(.38,'rgba(248,90,9,.3)');g.addColorStop(.7,'rgba(255,157,27,.38)');g.addColorStop(1,'rgba(255,212,94,0)');c.fillStyle=g;
      c.save();c.shadowColor='rgba(255,101,14,.25)';c.shadowBlur=14;c.beginPath();c.moveTo(px-width,base);c.bezierCurveTo(px-width*1.8,base-height*.32,px+width*1.1,base-height*.5,px+sway-width*.4,base-height*.73);c.bezierCurveTo(px+sway-width,base-height*.86,px+sway-width*.1,base-height*.92,px+sway,base-height);c.bezierCurveTo(px+sway+width*.6,base-height*.66,px-width*.5,base-height*.53,px+width*.55,base-height*.3);c.bezierCurveTo(px+width*1.3,base-height*.16,px+width*.6,base-height*.1,px+width,base);c.closePath();c.fill();c.restore();
    }
    for(const p of this.particles){const time=t-p.delay;if(time<0||time>p.life)continue;const progress=time/p.life,px=x+(p.x-.5)*spread*2+Math.sin(progress*5+p.angle)*16+p.drift*progress,py=base-progress*(210+p.y*150);
      c.save();c.globalAlpha*=Math.sin(progress*Math.PI)*.95;c.strokeStyle=p.size>2?'#ffd688':'#f78c35';c.lineWidth=p.size*.65;c.beginPath();c.moveTo(px,py);c.lineTo(px-p.drift*.015,py+3+p.y*5);c.stroke();c.fillStyle='#ffe0a3';c.beginPath();c.arc(px,py,p.size*.55,0,Math.PI*2);c.fill();c.restore();
    }
  }
  destroy(){this.stop();this.resizeObserver.disconnect();this.motion.removeEventListener('change',this.onMotion);}
}
