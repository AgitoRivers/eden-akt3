/* Standalone review renderer. No game imports, network calls, saves or combat rules. */
(() => {
  'use strict';
  const PI=Math.PI, TAU=2*PI;
  const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
  const ease=x=>1-Math.pow(1-clamp(x),3);
  const smooth=x=>{x=clamp(x);return x*x*(3-2*x);};
  const pulse=t=>Math.sin(PI*clamp(t));
  const C={gold:'#d8bd86',pearl:'#f3eee4',rose:'#d9a198',sage:'#a8d5b1',blue:'#9db9d6',water:'#80b9c3',fire:'#ef9b60',earth:'#b49c80',gray:'#a5a8b2',lavender:'#B7A4D6',dodge:'#8ec5ff'};
  const images=new Map(), frames=new Map();
  let assets={}, ready=false;
  function load(src){return new Promise(resolve=>{const im=new Image();im.onload=()=>{images.set(src,im);resolve(true);};im.onerror=()=>resolve(false);im.src=src;});}
  async function init(catalog){assets=catalog.assets;const paths=[...Object.values(assets).map(a=>a.file),...['idle','hurt','windup','guard','weakened'].map(p=>'assets/figur_'+p+'.webp')];const loaded=await Promise.all(paths.map(load));ready=true;return {total:paths.length,failed:paths.filter((p,i)=>!loaded[i])};}
  function coloredFrame(name,t,color){
    const a=assets[name];if(!a)return null;const im=images.get(a.file);if(!im)return null;
    const f=a.frames===1?0:Math.min(a.frames-1,Math.floor(clamp(t,0,.999)*a.frames));
    const key=name+':'+f+':'+color;if(frames.has(key))return frames.get(key);
    const fw=im.width/a.columns,fh=im.height/a.rows;
    const out=document.createElement('canvas');out.width=fw;out.height=fh;const g=out.getContext('2d');
    g.drawImage(im,(f%a.columns)*fw,Math.floor(f/a.columns)*fh,fw,fh,0,0,fw,fh);
    g.globalCompositeOperation='source-in';g.fillStyle=color;g.fillRect(0,0,fw,fh);
    if(frames.size>=96)frames.delete(frames.keys().next().value);frames.set(key,out);return out;
  }
  function tex(g,name,t,x,y,w,h,color,alpha=1,angle=0){const im=coloredFrame(name,t,color);if(!im)return;g.save();g.translate(x,y);g.rotate(angle);g.globalAlpha=clamp(alpha);g.drawImage(im,-w/2,-h/2,w,h);g.restore();}
  function glow(g,x,y,r,color,a=.25){g.save();g.globalAlpha=clamp(a);const gr=g.createRadialGradient(x,y,0,x,y,r);gr.addColorStop(0,color);gr.addColorStop(1,color+'00');g.fillStyle=gr;g.fillRect(x-r,y-r,r*2,r*2);g.restore();}
  function stroke(g,path,color,width=3,a=1,blur=7){g.save();g.globalAlpha=clamp(a);g.strokeStyle=color;g.lineWidth=width;g.lineCap='round';g.lineJoin='round';g.shadowColor=color;g.shadowBlur=blur;g.beginPath();path(g);g.stroke();g.restore();}
  function ring(g,x,y,r,color,a,stretch=.45,start=0,end=TAU,width=2){stroke(g,p=>p.ellipse(x,y,r,r*stretch,0,start,end),color,width,a,8);}
  function ribbon(g,pts,color,width,a){stroke(g,p=>{p.moveTo(...pts[0]);p.bezierCurveTo(...pts[1],...pts[2],...pts[3]);},color,width,a,width*2);}
  function heart(g,x,y,s,color,a){stroke(g,p=>{p.moveTo(x,y+s*.35);p.bezierCurveTo(x-s,y-s*.24,x-s*.55,y-s*.85,x,y-s*.3);p.bezierCurveTo(x+s*.55,y-s*.85,x+s,y-s*.24,x,y+s*.35);},color,2,a,9);}
  function rounded(g,x,y,w,h,r){g.beginPath();g.roundRect(x,y,w,h,r);}
  function panel(g,x,y,w,h){g.fillStyle='rgba(9,11,15,.8)';g.strokeStyle='rgba(216,189,134,.4)';g.lineWidth=1;rounded(g,x,y,w,h,14);g.fill();g.stroke();}
  function label(g,text,x,y,color,size=17,a=1){g.save();g.globalAlpha=clamp(a);g.font=`bold ${size}px 'Bricolage Grotesque','Segoe UI',sans-serif`;g.textAlign='center';g.textBaseline='middle';g.fillStyle=color;g.shadowColor='#000';g.shadowBlur=9;g.fillText(text,x,y);g.restore();}
  function edge(g,w,h,color,a){g.save();g.globalAlpha=clamp(a);let gr=g.createLinearGradient(0,0,w*.18,0);gr.addColorStop(0,color+'aa');gr.addColorStop(1,color+'00');g.fillStyle=gr;g.fillRect(0,0,w*.18,h);gr=g.createLinearGradient(w,0,w*.82,0);gr.addColorStop(0,color+'aa');gr.addColorStop(1,color+'00');g.fillStyle=gr;g.fillRect(w*.82,0,w*.18,h);g.restore();}
  function poseFor(e,t){if(['exhausted','weakened','reticle'].includes(e.kind))return 'weakened';if(['windup','heavyWindup'].includes(e.kind))return 'windup';if(e.kind==='shield')return 'guard';if(['impact','slash','stab','doubleSlash','tint','counter','vendetta'].includes(e.kind)&&t>.32&&t<.68)return 'hurt';return 'idle';}
  function drawFigure(g,e,t,w,h,mode,v,settings){
    if(mode!=='figure')return;
    const im=images.get('assets/figur_'+poseFor(e,t)+'.webp')||images.get('assets/figur_idle.webp');if(!im)return;
    if(settings.target==='duc'){
      const pw=w*.52,ph=h*.70,x=(w-pw)/2,y=h*.16;panel(g,x,y,pw,ph);
      g.save();rounded(g,x+8,y+8,pw-16,ph*.65,9);g.clip();g.drawImage(im,90,25,380,480,x+8,y+8,pw-16,ph*.65);g.restore();
      label(g,'Duc',w*.5,y+ph*.76,C.gold,15);g.fillStyle='#a8d5b1';rounded(g,x+15,y+ph*.87,pw-30,5,3);g.fill();return;
    }
    if(e.category==='J'){
      const y=h*.64;g.fillStyle='#28292e';rounded(g,w*.29,y,w*.42,h*.13,10);g.fill();stroke(g,p=>p.ellipse(w*.5,y,w*.21,h*.035,0,0,TAU),'#82858b',2,.75,0);stroke(g,p=>{p.moveTo(w*.70,y+5);p.lineTo(w*.84,y-5);},'#82858b',7,.7,0);return;
    }
    if(e.category==='H'){
      for(let i=0;i<3;i++)ribbon(g,[[0,h*(.65+i*.09)],[w*.3,h*(.59+i*.09)],[w*.7,h*(.72+i*.09)],[w,h*(.66+i*.09)]],C.water,1,.18);
      stroke(g,p=>{p.moveTo(w*.16,h*.65);p.quadraticCurveTo(w*.32,h*.28,w*.53,h*.61);},C.pearl,1,.42,0);return;
    }
    if(['I2','I3','J6','L4','L5','L2'].includes(e.id)){
      panel(g,w*.25,h*.31,w*.50,h*.40);label(g,e.id==='L4'?'BATTERIE':e.id==='L2'?'EDEN':e.id==='L5'?'CALA D’ORSU':'TASCHE',w*.5,h*.42,C.gold,13);
      label(g,e.id==='L4'?'12 %':e.id==='I3'?'6 / 6':'—',w*.5,h*.56,C.pearl,22);return;
    }
    const isPortrait=e.category==='K';
    if(isPortrait){g.save();rounded(g,w*.30,h*.17,w*.40,h*.65,28);g.clip();g.drawImage(im,95,25,365,520,w*.3,h*.17,w*.4,h*.65);g.restore();return;}
    const fh=h*.88,fw=fh*im.width/im.height;
    let x=w*.5-fw*.5,y=h*.07;
    if(['damage','impact','critical','quake'].includes(e.kind)&&t>.32&&t<.60)x+=Math.sin(t*88)*(v+1)*1.5*(1-clamp((t-.32)/.28));
    if(['exhausted','weakened'].includes(e.kind))y+=smooth(t)*h*.02;
    g.save();if(e.kind==='blur')g.globalAlpha=.55+.45*(1-pulse(t));if(e.kind==='calm')g.filter='saturate(.35)';g.drawImage(im,x,y,fw,fh);g.restore();
  }
  function base(g,w,h,mode){
    if(mode==='light'){g.fillStyle='#d4d0c9';g.fillRect(0,0,w,h);return;}
    let gr=g.createLinearGradient(0,0,w,h);gr.addColorStop(0,'#0c1019');gr.addColorStop(.55,'#151b26');gr.addColorStop(1,'#0a0d12');g.fillStyle=gr;g.fillRect(0,0,w,h);
    gr=g.createRadialGradient(w*.5,h*.72,0,w*.5,h*.72,w*.6);gr.addColorStop(0,'rgba(80,85,98,.15)');gr.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=gr;g.fillRect(0,0,w,h);
    g.strokeStyle='rgba(216,189,134,.12)';g.lineWidth=1;g.beginPath();g.moveTo(0,h*.87);g.lineTo(w,h*.87);g.stroke();
  }
  function drawFx(g,e,v,t,w,h,settings,behind=false){
    let kind=e.kind;const sub=settings.subtype;
    if(kind==='element')kind=({Feuer:'fire',Wasser:'water',Erde:'quake',Strom:'electric'})[sub]||'fire';
    let color=C[e.palette]||C.gold;
    if(e.kind==='gift')color=sub==='Mag nicht'?C.blue:sub==='Mag'?C.gold:C.rose;
    if(e.kind==='cooking')color=sub==='Misslungen'?C.rose:sub==='Gut'?C.sage:C.gold;
    if(e.kind==='buff')color=sub==='Schwächung'?C.gray:C.sage;
    const env=pulse(t),q=ease((t-.10)/.72),hit=clamp((t-.28)/.24),fade=1-smooth((t-.65)/.35),a=env*(.65+v*.13),x=w*.5,y=h*.57,s=w*(.53+v*.12);
    const loopWave=.68+.22*Math.sin(t*TAU);
    g.save();
    // Every source sprite is a softened alpha mask. No dotted emitter is used.
    // A shared framing change also distinguishes restrained UI-only variants.
    g.translate(x,y);g.scale([.83,1,1.12][v],[.91,1,1.04][v]);g.translate(-x,-y);
    function slash(angle=0,offset=0,alpha=1){
      const z=clamp((t-offset-.12)/.62);if(z<=0||z>=1)return;
      const which=v===0?'sword_slash_3D':'swipe_dissolve';
      tex(g,which,.12+z*.72,x+(z-.5)*w*.14,y,s*(v===0?1.1:1.0),s*(v===0?.62:.9),color,pulse(z)*alpha,angle+(v===2?-.35:.2));
      if(v>0)ribbon(g,[[w*.29,h*.72],[w*.35,h*.52],[w*.56,h*.36],[w*.76,h*.41]],color,1.5,pulse(z)*.42);
    }
    function impact(){
      const z=clamp((t-.17)/.75);if(z<=0)return;
      ring(g,x,h*.68,w*(.06+z*(.25+v*.06)),color,pulse(z),.30+v*.06,0,TAU,2+v);
      if(v>0)ring(g,x,h*.68,w*(.03+z*.23),color,pulse(z)*.4,.29,PI*.1,PI*1.8,1);
      if(v===2)tex(g,'painted_style_golden_shockwave',0,x,y,s*.75,s*.75,color,pulse(z)*.38);
      glow(g,x,y,w*.18,color,Math.max(0,1-Math.abs(t-.32)*16)*.35);
    }
    function fire(){
      const n=v===0?2:v===1?3:4;
      for(let i=0;i<n;i++){const z=n===1?0:(i/(n-1)-.5);tex(g,'stylized_flame_flipbook',(t*.85+i*.16)%1,x+z*w*.24,h*(.73-Math.abs(z)*.08),w*(.24+v*.025),h*(.45+v*.06),color,loopWave*(.68-Math.abs(z)*.18));}
      if(v===2)glow(g,x,h*.75,w*.28,color,.16*env);
    }
    function water(muddy=false){
      const z=clamp((t-.08)/.82);const col=muddy?C.earth:color;
      tex(g,'waterfall_3D_2',.08+z*.84,x,h*(.84-z*(v===2?.38:.22)),s*(.75+z*.3),h*(.18+v*.08),col,pulse(z)*.8,v===0?PI/2:v===1?-.35:.45);
      ring(g,x,h*.83,w*(.08+z*.3),col,pulse(z)*.75,.2,0,TAU,2);
      if(v>0)ribbon(g,[[w*.2,h*.83],[w*.36,h*(.4+z*.2)],[w*.68,h*.50],[w*.83,h*.77]],col,4,pulse(z)*.7);
    }
    function electric(big=false){
      const name=v===0?'electric_arc_4':v===1?'lightning_sheet':'erosion_based_lightning';
      tex(g,name,(t*.9)%1,x+w*.09*Math.sin(t*6),y,w*(big?.5:.3),h*.66,color,env*.82,(v-1)*.12);
      if(v>0)tex(g,'electric_arc_4',(t*.8+.3)%1,x-w*.13,y+h*.07,w*.18,h*.39,color,env*.5,-.7);
      if(big)ring(g,x,h*.81,w*(.1+.25*q),C.water,env*.65,.3,0,TAU,2);
    }
    function smoke(steam=false){
      for(let i=0;i<1+v;i++){
        tex(g,'stylized_smoke_trail',(.15+t*.75+i*.13)%1,x+(i-v*.5)*w*.13,h*(.73-t*.25),w*(.25+v*.035),h*(steam?.65:.45),color,env*.35,(i-v*.5)*.15);
      }
      if(steam)ribbon(g,[[x-w*.1,h*.7],[x-w*.18,h*.5],[x+w*.14,h*.5],[x+w*.04,h*.25]],color,2,env*.35);
    }
    function aura(){
      tex(g,'shield_gradient',0,x,h*.62,w*(.46+v*.10),h*(.70+v*.07),color,a*.50);
      if(v>0)ring(g,x,h*.83,w*(.20+v*.035),color,env*.75,.24,0,TAU,1.5);
      if(v===2)ribbon(g,[[w*.24,h*.83],[w*.18,h*.54],[w*.32,h*.27],[w*.43,h*.3]],color,2,env*.6);
    }
    function wind(){
      tex(g,'swipe_dissolve',.18+q*.55,x,h*.72,s*1.1,h*.35,color,env*.65,(v-1)*.15);
      if(v>0)ribbon(g,[[w*.13,h*.75],[w*.36,h*.33],[w*.64,h*.94],[w*.88,h*.44]],color,2,env*.65);
    }
    if(behind){
      if(['fire','firestorm','flare'].includes(kind))fire();
      if(['wind','mistral','weather'].includes(kind))wind();
      if(['shield','heal','buff','trust','desire','milestone','rareFind','rareCatch','find','level','romance'].includes(kind))aura();
      g.restore();return;
    }
    switch(kind){
      case 'slash':slash(-.25);break;
      case 'impact':impact();break;
      case 'stab':{
        const z=clamp((t-.12)/.65);stroke(g,p=>{p.moveTo(w*(.24+z*.15),h*.70);p.lineTo(w*(.45+z*.16),h*.47);},color,3+v,pulse(z),11);
        if(v>0)tex(g,'lense_flare',.3,x,y,w*.44,h*.3,color,Math.max(0,1-Math.abs(t-.38)*9)*.65);break;}
      case 'thrust':wind();stroke(g,p=>{p.moveTo(w*.17,h*.64);p.lineTo(w*(.25+q*.57),h*.53);},color,2+v,a,12);break;
      case 'shot':{
        const z=clamp((t-.12)/.55);tex(g,'lense_flare',.3,w*.2,h*.68,w*.28,h*.26,color,Math.max(0,1-Math.abs(t-.18)*22)*.9);
        stroke(g,p=>{p.moveTo(w*.25,h*.65);p.lineTo(w*(.25+q*.35),h*(.65-q*.15));},color,2,Math.max(0,1-Math.abs(t-.32)*10),10);if(t>.25)impact();break;}
      case 'critical':impact();slash(-.1);break;
      case 'counter':ring(g,x,y,w*.2,color,Math.max(0,1-t*3),.85);slash(.35,.17);break;
      case 'doubleSlash':slash(-.3,0);slash(.45,.23,.9);break;
      case 'vendetta':slash(-.3);stroke(g,p=>{p.moveTo(w*.41,h*.49);p.lineTo(w*.58,h*.69);},C.rose,3+v,env*.8,4);break;
      case 'blackSlash':g.fillStyle=`rgba(0,0,0,${env*.9})`;g.fillRect(0,0,w,h);slash(-.25,.08);break;
      case 'tint':glow(g,x,y,w*.22,color,Math.max(0,1-Math.abs(t-.34)*18)*.55);stroke(g,p=>{p.moveTo(w*.39,h*.44);p.lineTo(w*.62,h*.66);},color,1+v,a*.6);break;
      case 'windup':case 'heavyWindup':{
        const grow=kind==='heavyWindup'?1.25:1;
        stroke(g,p=>{p.moveTo(w*.65,h*.77);p.bezierCurveTo(w*.73,h*.57,w*.67,h*.37,w*.59,h*.31);},color,2+v,env*.8*grow,12);
        if(v>0)ring(g,x,h*.83,w*.25*grow,color,a*.6,.25,PI*.15,PI*1.85,2);
        if(v===2)ribbon(g,[[w*.23,h*.78],[w*.24,h*.6],[w*.32,h*.42],[w*.38,h*.38]],color,1.5,env*.45);break;}
      case 'parry':case 'parrySoft':{
        const z=clamp((t-.13)/.76);ring(g,x,y,w*(.05+z*(kind==='parrySoft'?.20:.29)),color,pulse(z),.83,-.3,TAU-.55,2+v);
        if(v>0)ring(g,x,y,w*(.06+z*.21),color,pulse(z)*.5,.83,PI*.25,PI*1.7,1);
        if(kind==='parry')for(let i=0;i<v+1;i++){const an=-.6+i*.65;stroke(g,p=>{p.moveTo(x+Math.cos(an)*w*.16,y+Math.sin(an)*h*.18);p.lineTo(x+Math.cos(an)*w*(.18+z*.13),y+Math.sin(an)*h*(.20+z*.10));},color,2,pulse(z),6);}break;}
      case 'dodge':wind();edge(g,w,h,color,a*.3);break;
      case 'damage':edge(g,w,h,color,env*.65);if(v>0)stroke(g,p=>{p.moveTo(w*.3,h*.74);p.lineTo(w*.66,h*.45);},color,3,env*.5);break;
      case 'shield':aura();break;
      case 'fire':break;
      case 'water':case 'wave':case 'catch':case 'escape':water();break;
      case 'tidal':water();if(v>0){g.save();g.translate(w*.15,-h*.12);water();g.restore();}break;
      case 'quake':case 'mistral':{
        impact();for(let i=0;i<2+v;i++){const dx=(i-(1+v)*.5)*w*.12;stroke(g,p=>{p.moveTo(x+dx,h*.83);p.lineTo(x+dx+w*.04,h*.88);p.lineTo(x+dx-w*.02,h*.92);},color,1.5,env*.7,1);}break;}
      case 'electric':electric();break;
      case 'bleed':{
        const alpha=(.62+.22*Math.sin(t*TAU))*env;stroke(g,p=>{p.moveTo(w*.42,h*.48);p.lineTo(w*.59,h*.68);},color,3+v,alpha,4);if(v===2)stroke(g,p=>{p.moveTo(w*.45,h*.48);p.lineTo(w*.61,h*.66);},color,1,alpha*.5,2);break;}
      case 'exhausted':case 'weakened':smoke();ring(g,x,h*.85,w*.20,color,a*.35,.22,0,PI*1.6,1);break;
      case 'blind':g.save();g.globalAlpha=env*.22;g.fillStyle=color;g.fillRect(w*.32,h*.17,w*.37,h*.13);g.restore();edge(g,w,h,color,a*.25);break;
      case 'vulnerable':edge(g,w,h,color,(.30+.18*Math.sin(t*TAU*2))*env);break;
      case 'stun':{
        const an=t*TAU;ring(g,x,h*.19,w*.12,color,env*.6,.25);const sx=x+Math.cos(an)*w*.12,sy=h*.19+Math.sin(an)*h*.035;
        stroke(g,p=>{for(let i=0;i<10;i++){const r=i%2?4:9;const a=-PI/2+i*PI/5;const xx=sx+Math.cos(a)*r,yy=sy+Math.sin(a)*r;if(i===0)p.moveTo(xx,yy);else p.lineTo(xx,yy);}p.closePath();},color,1.4,env,5);break;}
      case 'shortCircuit':electric(true);break;
      case 'mud':case 'slime':water(true);break;
      case 'firestorm':electric();tex(g,'swipe_dissolve',t,x,h*.67,s,s*.8,color,env*.8,t*PI);break;
      case 'steam':case 'sizzle':smoke(true);break;
      case 'flare':tex(g,'stylized_flame_flipbook',t,x,h*.65,w*.36,h*.64,color,env);break;
      case 'wind':break;
      case 'blur':for(let i=0;i<2+v;i++)ribbon(g,[[w*.25,h*(.40+i*.11)],[w*.38,h*(.37+i*.11)],[w*.62,h*(.46+i*.11)],[w*.75,h*(.42+i*.11)]],color,3,env*.22);break;
      case 'reticle':{
        const r=w*(.16+(1-q)*.12);ring(g,x,y,r,color,env,.9,-.15,PI*.85,1.7);ring(g,x,y,r,color,env,.9,PI*.95,PI*1.85,1.7);
        for(let i=0;i<4;i++){const an=i*PI/2;stroke(g,p=>{p.moveTo(x+Math.cos(an)*r*.8,y+Math.sin(an)*r*.8);p.lineTo(x+Math.cos(an)*r*1.2,y+Math.sin(an)*r*1.2);},color,1.5,env,2);}break;}
      case 'calm':ring(g,x,h*.76,w*(.06+q*.33),color,env,.17,0,TAU,1);if(v>0)ring(g,x,h*.76,w*(.03+q*.23),color,env*.4,.17);break;
      case 'beam':{
        const z=.5+Math.sin(t*PI)*.14;g.save();g.globalAlpha=env*.24;const gr=g.createLinearGradient(w*.1,h*.4,w*.9,h*.2);gr.addColorStop(0,color+'00');gr.addColorStop(.6,color);gr.addColorStop(1,color+'00');g.fillStyle=gr;g.beginPath();g.moveTo(w*.12,h*.65);g.lineTo(w*.95,h*(z-.30));g.lineTo(w*.95,h*(z+.03));g.closePath();g.fill();g.restore();break;}
      case 'rain':for(let i=0;i<3;i++){const z=clamp((t-i*.13)/.6);const xx=w*(.34+i*.16);stroke(g,p=>{p.moveTo(xx,h*(.12+z*.28));p.lineTo(xx-w*.055,h*(.28+z*.40));},color,2+v,pulse(z),12);}break;
      case 'dodgeOnly':ring(g,x,y,w*(.17+.08*q),C.dodge,env,.95,0,TAU,2+v);break;
      case 'buff':case 'heal':case 'trust':case 'find':aura();break;
      case 'victory':{
        if(sub==='K.o.'){edge(g,w,h,C.rose,env*.3);label(g,'K.o.',x,h*.36,C.rose,25,env);}else if(sub==='Aufgabe'){label(g,'Aufgabe',x,h*.36,C.gold,24,env);ring(g,x,h*.78,w*.22,C.gold,env,.3);}else aura();break;}
      case 'wake':case 'return':{
        const black=Math.sin(PI*clamp(t*1.45));g.fillStyle=`rgba(0,0,0,${Math.max(0,black)*.94})`;g.fillRect(0,0,w,h);if(t>.5)glow(g,x,h*.25,w*.65,C.gold,(t-.5)*.55);break;}
      case 'level':case 'milestone':{
        for(let i=0;i<1+v;i++){const xx=x+(i-v*.5)*w*.10;const gr=g.createLinearGradient(0,h*.2,0,h*.9);gr.addColorStop(0,color+'00');gr.addColorStop(.55,color+'aa');gr.addColorStop(1,color+'00');g.save();g.globalAlpha=env*.4;g.fillStyle=gr;g.fillRect(xx-w*.016,h*.2,w*.032,h*.7);g.restore();}ring(g,x,h*.83,w*(.12+q*.2),color,env,.23);break;}
      case 'day':{
        const gr=g.createLinearGradient(0,0,w,h);gr.addColorStop(0,'#e2b77600');gr.addColorStop(.5,'#e2b77677');gr.addColorStop(1,'#e2b77600');g.save();g.globalAlpha=env*.55;g.translate((q-.5)*w,0);g.fillStyle=gr;g.fillRect(0,0,w,h);g.restore();stroke(g,p=>p.arc(x,h*.67,w*.13,PI,TAU),color,3,env,8);break;}
      case 'cast':{
        const z=q;stroke(g,p=>{p.moveTo(w*.15,h*.70);p.quadraticCurveTo(w*.40,h*(.05+z*.28),w*(.2+z*.55),h*(.3+z*.4));},color,1.5,env,1);if(t>.5)ring(g,w*.75,h*.7,w*(t-.5)*.25,color,fade,.19);break;}
      case 'bite':{
        const yy=h*.65+Math.sin(t*TAU*2)*4;stroke(g,p=>{p.moveTo(x,yy-12);p.lineTo(x,yy+9);},C.rose,3,env,1);ring(g,x,h*.68,w*(.03+q*.17),color,env,.25,0,TAU,1.5);break;}
      case 'rareCatch':water();aura();break;
      case 'pickup':{
        const xx=w*(.32+q*.34),yy=h*(.72-.32*Math.sin(q*PI));panel(g,w*.62,h*.65,w*.15,h*.14);stroke(g,p=>{p.moveTo(xx-8,yy);p.lineTo(xx,yy-10);p.lineTo(xx+8,yy);p.lineTo(xx,yy+10);p.closePath();},color,2,env,8);break;}
      case 'full':edge(g,w,h,color,env*.25);label(g,'6 / 6',x,h*.58,color,26,env);break;
      case 'rareFind':aura();ring(g,x,h*.65,w*(.1+q*.22),color,env,.7,0,TAU,2);break;
      case 'elite':{
        edge(g,w,h,'#07080b',env*.75);g.save();g.strokeStyle=color;g.lineWidth=2;g.globalAlpha=env;g.beginPath();g.moveTo(x-w*.08,h*.35);g.bezierCurveTo(x-w*.14,h*.21,x+w*.14,h*.21,x+w*.08,h*.35);g.lineTo(x+w*.035,h*.40);g.lineTo(x-w*.035,h*.40);g.closePath();g.stroke();g.beginPath();g.moveTo(x-w*.025,h*.40);g.lineTo(x-w*.025,h*.44);g.moveTo(x+w*.025,h*.40);g.lineTo(x+w*.025,h*.44);g.stroke();g.restore();break;}
      case 'cooking':aura();if(sub==='Misslungen')smoke();break;
      case 'favorite':case 'desire':case 'gift':heart(g,x,h*(.57-q*.13),w*(.08+v*.015),color,env);if(v>0)aura();break;
      case 'upgrade':{
        stroke(g,p=>{p.moveTo(w*.38,h*.76);p.lineTo(w*.61,h*.32);},color,5,env,11);for(let i=0;i<1+v;i++)ribbon(g,[[w*.47,h*.54],[w*.50,h*.43],[w*.62,h*.45],[w*.68,h*.36]],color,1.5,env*.7);break;}
      case 'trade':ring(g,x+(q-.5)*w*.22,h*(.51-.10*Math.sin(q*PI)),w*.045,color,env,1,0,TAU,2);break;
      case 'cool':edge(g,w,h,C.blue,env*.35);ring(g,x,h*(.64+q*.16),w*.21,C.blue,env*.45,.3);break;
      case 'romance':glow(g,x,h*.60,w*.55,color,env*.18);ribbon(g,[[w*.10,h*.87],[w*.25,h*.60],[w*.73,h*.97],[w*.90,h*.64]],color,2,env*.40);break;
      case 'blush':glow(g,w*.45,h*.41,w*.06,color,env*.3);glow(g,w*.55,h*.41,w*.06,color,env*.3);break;
      case 'event':{
        const yy=h*(.95-.54*smooth(t/.5));panel(g,w*.22,yy,w*.56,h*.27);label(g,sub||'Handy',x,yy+h*.08,C.gold,14,env);label(g,'Neuer Moment',x,yy+h*.18,C.pearl,11,env);break;}
      case 'warning':edge(g,w,h,color,env*.3);label(g,'12 %',x,h*.56,color,27,env);break;
      case 'reputation':ring(g,x,y,w*(.1+q*.16),color,env,.9,0,TAU,1.5);break;
      case 'weather':
        if(sub==='Nachtlicht'){for(let i=0;i<3;i++){const xx=w*(.2+i*.3);stroke(g,p=>{p.moveTo(xx,h*.14);p.lineTo(xx,h*.22);},C.gold,3,env*.5,12);}}else wind();break;
    }
    // Large lettering is part of the preview composition, never an input blocker.
    let text=e.title;
    if(['gift','cooking','victory'].includes(e.kind))text=sub||text;
    if(text&&t>.13&&t<.94&&!['event','full','warning','victory'].includes(kind)){
      label(g,text,x,h*.12,color,v===2?20:17,pulse(clamp((t-.13)/.81))*.9);
    }
    g.restore();
  }
  function render(canvas,e,index,t,settings={}){
    const g=canvas.getContext('2d'),w=canvas.width,h=canvas.height;
    if(!ready){g.fillStyle='#10131b';g.fillRect(0,0,w,h);label(g,'Vorschau wird geladen',w*.5,h*.5,C.gold,15);return;}
    t=clamp(t);const mode=settings.stage||'figure';
    g.clearRect(0,0,w,h);base(g,w,h,mode);
    drawFx(g,e,index,t,w,h,settings,true);drawFigure(g,e,t,w,h,mode,index,settings);
    drawFx(g,e,index,t,w,h,settings,false);
  }
  function renderLayer(canvas,e,index,t,settings={}){
    const g=canvas.getContext('2d'),w=canvas.width,h=canvas.height;g.clearRect(0,0,w,h);
    if(!ready)return;
    drawFx(g,e,index,clamp(t),w,h,settings,true);drawFx(g,e,index,clamp(t),w,h,settings,false);
  }
  window.EdenFxPreview={init,render,renderLayer,palette:C,stats:()=>({ready,images:images.size,frames:frames.size})};
})();
