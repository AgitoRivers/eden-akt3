/* Warm Corsican self effects. No combat rules, damage or enemy pose changes. */
(()=>{'use strict';
 const PI=Math.PI,C=x=>Math.max(0,Math.min(1,x)),S=x=>{x=C(x);return x*x*(3-2*x)},mix=(a,b,p)=>a+(b-a)*p;
 const defs={
  balm:{name:'Elicriso',kind:'self',variants:[['Verdant charge','Sage-green energy gathers against Duc’s body, threaded with fine gold. It opens into a warm healing pulse.'],['Twin currents','Two green-gold currents converge at the chest, building a close body charge before the healing pulse.'],['Amber pulse','A denser amber core grows inside a deep green body aura, then softly releases its stored light.']]},
  westWind:{name:'Ponente',kind:'self',variants:[['Mild west wind','One broad soft current circles Duc with slow myrtle leaves. Three quiet pulses suggest its continuing healing. No storm.'],['Sheltering breeze','Two gentle currents rise around Duc and settle at his shoulders, with small leaves and a long soft afterglow.'],['Myrtle passage','A mild diagonal breeze passes Duc from the west. Three calm waves of sage light return along the body.']]},
  awaken:{name:'Risveglio',kind:'self',variants:[['Morning from above','Warm dawn light descends from above onto Duc and settles around his body. Bright, still and restorative.'],['Twin rays','Two soft curtains of morning light fall from above Duc’s shoulders and gently open around him.'],['Descending veil','A narrow ivory-sage light descends from above, widening into a calm restorative veil. No explosion.']]},
  archangel:{name:'Arcangelo',kind:'self',variants:[['Guardian of light','Gold-ivory wings slowly open behind Duc and settle into a protective glow. The separate rescue is short and local to Duc.'],['Sheltering wings','More closely folded light wings curve protectively around Duc. The rescue opens them once above a warm golden ground pulse.'],['Church dawn','Vertical morning light reveals high guardian wings, with sage edges and a restrained golden root. No angel figure or fireworks.']]}
 };
 const launches={balm:2.4,westWind:2.8,awaken:3.1,archangel:3.6},durations={balm:4.9,westWind:6.3,awaken:5.7,archangel:5.9};
 const ids=new Set(Object.keys(defs)),cache=new Map();let images={},phase='aufladen';
 function load(base){
  const url=new URL(base,document.baseURI).href;
  if(!cache.has(url))cache.set(url,Promise.all(['oil','leaf','dawn','wings'].map(name=>new Promise((ok,bad)=>{const i=new Image();i.onload=()=>{
   // A soft runtime material mask prevents an atlas cell edge from becoming a visible rectangle.
   const canvas=document.createElement('canvas');canvas.width=i.width;canvas.height=i.height;const g=canvas.getContext('2d');g.drawImage(i,0,0);g.globalCompositeOperation='destination-in';
   g.save();g.translate(i.width/2,i.height/2);g.scale(i.width/2,i.height/2);const mask=g.createRadialGradient(0,0,.64,0,0,1.05);mask.addColorStop(0,'#fff');mask.addColorStop(1,'#fff0');g.fillStyle=mask;g.fillRect(-1,-1,2,2);g.restore();ok([name,canvas]);};i.onerror=()=>bad(Error('Healer material missing: '+name));i.src=new URL(name+'.png',url).href}))).then(pairs=>{images=Object.fromEntries(pairs);return images}));
  return cache.get(url);
 }
 function sprite(g,name,x,y,w,h,alpha=1,angle=0){const i=images[name];if(!i||alpha<.001)return;g.save();g.globalAlpha=C(alpha);g.translate(x,y);g.rotate(angle);g.drawImage(i,-w/2,-h/2,w,h);g.restore()}
 function glow(g,x,y,w,h,color,alpha){if(alpha<.001)return;g.save();g.globalAlpha=C(alpha);g.translate(x,y);g.scale(w,h);const grad=g.createRadialGradient(0,0,0,0,0,1);grad.addColorStop(0,color);grad.addColorStop(.25,color);grad.addColorStop(1,'#fff0');g.fillStyle=grad;g.fillRect(-1,-1,2,2);g.restore()}
 function envelope(t,start,end,rise=.3,fall=.65){return S((t-start)/rise)*(1-S((t-end+fall)/fall))}
 function motes(g,t,cx,y,amount,alpha,color,spread=120){
  for(let j=0;j<amount;j++){const seed=(Math.sin(j*39.7)*1321)%1,p=((t*.22+j*.618)%1+1)%1,x=cx+Math.sin(j*2.4+t*.32)*spread*(.35+Math.abs(seed)*.65),yy=y-p*220+Math.sin(j+t)*8;
   glow(g,x,yy,1.1+j%3*.25,1.2+j%3*.35,color,alpha*Math.sin(p*PI)*.6);
  }
 }
 function leaf(g,t,cx,y,n,alpha,style){
  for(let j=0;j<n;j++){const p=((t*.36+j*.381)%1+1)%1,a=p*PI*2*(style===1?1.35:1)+j*.7,x=cx+Math.sin(a)*(style===2?145:95),yy=y+(style===1?-p*160+Math.sin(a)*45:Math.cos(a)*80)-35;
   const w=12+(j%3)*5;sprite(g,'leaf',x,yy,w,w*.68,alpha*(.5+.5*Math.sin(p*PI)),a*.55+Math.sin(t+j)*.2);
  }
 }
 function gauze(g,t,cx,y,w,alpha,style){
  // Layered moving painted material; no hard outline or fixed circular boundary.
  for(let j=0;j<3;j++){const a=Math.sin(t*.8+j)*.13+(style===2?-.3:0),dx=Math.sin(t*.6+j*2.1)*30;
   sprite(g,'dawn',cx+dx,y+j*30,w*(1-j*.09),62+j*12,alpha*(.65-j*.13),PI/2+a);
  }
 }
 function wings(g,t,cx,y,w,h,alpha,spread=1){
  const i=images.wings;if(!i||alpha<.001)return;
  for(const side of [-1,1]){g.save();g.globalAlpha=C(alpha);g.translate(cx,y);g.rotate(side*(.11*(1-spread)+Math.sin(t*1.2)*.012));g.scale(spread,1);
   g.drawImage(i,side<0?0:i.width/2,0,i.width/2,i.height,side<0?-w/2:0,-h/2,w/2,h);g.restore()}
 }
 function drawRescue(g,t,{cx=666,foot=495,variant=0,scale=1,reduced=false,behind=false}={}){
  if(t<0||t>=1.25)return;const fade=envelope(t,0,1.25,.08,.5),open=S(t/.35),clock=reduced?.35:t;
  g.save();g.translate(cx,foot);g.scale(scale,scale);
  if(behind){
   glow(g,0,-170,160,235,'#a7dcb0',fade*.18);wings(g,clock,0,-184,[410,350,435][variant],330,fade*.86,.60+.40*open);
   sprite(g,'dawn',0,-210,300,530,fade*.23,variant===2?.04:0);
  }else{
   const pulse=Math.exp(-Math.pow((t-.16)/.12,2));glow(g,0,-12,145,25,'#e8ce82',fade*.42);glow(g,0,-150,70,130,'#fff5d4',pulse*.20);
   gauze(g,clock*1.1,0,-35,290,fade*.18,variant);motes(g,clock,0,-25,reduced?0:28,fade*.65,'#f4dba0',105);
  }
  g.restore();
 }
 const chargeTexture=document.createElement('canvas');chargeTexture.width=144;chargeTexture.height=192;let chargeFrame='';
 function bodyPower(A){const at=A.launch+.38;return S((A.clock-.2)/(at-.2))*(1-S((A.clock-at)/.75))}
 function drawBody(A,{image,anchor,scale}){
  if(A.id!=='balm')return;const power=bodyPower(A);if(power<.002)return;const tick=A.variant+':'+Math.floor(A.clock*24);
  if(chargeFrame!==tick){chargeFrame=tick;const q=chargeTexture.getContext('2d'),im=q.createImageData(144,192);
   for(let y=0;y<192;y++)for(let x=0;x<144;x++){const u=(x-72)/72,v=(y-96)/96,warp=A.sample(x*.7-A.clock*16,y*.8+A.clock*12),n=A.sample(x*.92+warp*19,y*.9+A.clock*36),fine=A.sample(x*2.3+A.clock*21,y*2-A.clock*29),edge=Math.exp(-Math.pow(u+(n-.5)*.18,2)*3.6-v*v*2.7),gold=S((fine-.58)/.35),i=(y*144+x)*4;
    im.data[i]=mix(58+fine*70,247,gold);im.data[i+1]=mix(137+fine*100,211,gold);im.data[i+2]=mix(92+fine*45,115,gold);im.data[i+3]=edge*S((n*.7+fine*.3-.25)/.6)*220;
   }q.putImageData(im,0,0)
  }
  const g=A.g,cy=-anchor.foot*scale+image.height*scale*.405;g.save();g.globalAlpha*=power*.95;g.drawImage(chargeTexture,-82,cy-115,164,230);g.restore();
 }
 function draw(A,behind){
  const {g,id,variant:v,clock,launch}=A,cx=666,end=durations[id],warm=envelope(clock,.18,end,.55,.85),heal=S((clock-launch+.12)/.5),fade=1-S((clock-end+.9)/.9);
  if(id==='archangel'&&phase==='rettung'){drawRescue(g,A.animationClock,{cx,variant:v,behind});return}
  if(!warm)return;
  if(id==='balm'){
   const power=bodyPower(A),pulse=Math.exp(-Math.pow((clock-launch-.38)/.22,2));
   if(behind){glow(g,cx,342,108+v*9,170,'#71c78d',power*.37);glow(g,cx+12,325,64,110,'#eccd79',power*(v===2?.22:.12));sprite(g,'dawn',cx,340,180,330,power*.14);return}
   for(let j=0;j<(v===1?60:44);j++){const p=(clock*.47+j*.618)%1,angle=j*2.399+clock*.25,rx=18+(1-p)*(v===1?100:85),ry=22+(1-p)*100;
    const x=cx+Math.cos(angle)*rx,y=332+Math.sin(angle)*ry;glow(g,x,y,.9+j%3*.22,1.3+j%4*.3,j%3?'#b2e4a1':'#f4d988',power*Math.sin(p*PI)*.74)
   }
   if(v===1){gauze(g,clock,cx-30,315,110,power*.22,2);gauze(g,clock+1,cx+30,370,110,power*.22,0)}
   glow(g,cx,340,65+pulse*70,110+pulse*80,'#c1e7aa',pulse*.25);motes(g,clock,cx,455,18,warm*heal*.34,'#e8d595',70);return;
  }
  if(id==='westWind'){
   const pulse=Array.from({length:3},(_,j)=>Math.exp(-Math.pow((clock-(launch+.38+j*.78))/.34,2))).reduce((a,b)=>a+b,0);
   if(behind){glow(g,cx,380,145,190,'#9fd6a6',warm*.13+pulse*.055);gauze(g,clock,cx,345,v===1?275:310,warm*.25,v);return}
   leaf(g,clock,cx,v===1?485:385,[24,45,24][v],warm*.85,v);gauze(g,clock+2,cx,420,280,warm*.17,v);
   motes(g,clock,cx,465,16,warm*.35,'#dcebd1',100);return;
  }
  if(id==='awaken'){
   const breath=S((clock-.5)/(launch-.5)),open=S((clock-launch+.1)/.65),level=warm*(.22+open*.65);
   if(behind){
    if(v===1){for(const side of [-1,1])sprite(g,'dawn',cx+side*(32+open*40),155+open*65,190,650,level*.60,side*.09)}
    else sprite(g,'dawn',cx,145+open*90,v===2?155+open*155:330,670,level*.70,0);
    glow(g,cx,135+open*180,105+open*45,235,'#c1e6bf',level*.17);return;
   }
   glow(g,cx+12,330,44+open*44,75+open*55,'#fff4cc',Math.sin(C((clock-launch+.4)/1.25)*PI)*fade*.24);
   motes(g,clock*.65,cx,490,34,warm*open*.55,'#f3e7c6',105);
   if(v===2)gauze(g,clock*.45,cx,344,190+breath*95,warm*.26,0);return;
  }
  if(id==='archangel'){
   const unfold=S((clock-.4)/(launch-.4)),hold=warm*(.2+.8*unfold),width=[410,355,440][v];
   if(behind){wings(g,clock,cx,302,width,350,hold*.83,.25+.75*unfold);if(v===2)sprite(g,'dawn',cx,275,320,555,hold*.48);glow(g,cx,340,140,205,'#b7dcae',hold*.13);return}
   glow(g,cx,488,100+unfold*45,18,'#e9d49b',hold*.26);motes(g,clock*.65,cx,470,22,hold*.40,'#f4dfa5',100);gauze(g,clock*.3,cx,400,240,hold*.13,0);
  }
 }
 function playRescue(anchor,{variant=0,assetBase='/plugins/eden-skills/preview/assets/heiler-v1/'}={}){
  const app=document.getElementById('app');if(!app)return {stop(){},duration:1.25};variant=Math.max(0,Math.min(2,Number(variant)||0));
  const canvas=document.createElement('canvas'),rect=app.getBoundingClientRect(),r=anchor?.getBoundingClientRect()||rect,dpr=Math.min(2,window.devicePixelRatio||1);
  canvas.width=Math.ceil(rect.width*dpr);canvas.height=Math.ceil(rect.height*dpr);canvas.dataset.edenHealerRescue='';canvas.style.cssText='position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:34';app.append(canvas);
  const g=canvas.getContext('2d'),cx=r.left-rect.left+r.width/2,foot=r.top-rect.top+r.height*.92,scale=Math.max(.35,Math.min(1.5,r.height/420));g.setTransform(dpr,0,0,dpr,0,0);
  const reduced=window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;let frame=0,stopped=false,start=performance.now();
  function stop(){if(stopped)return;stopped=true;cancelAnimationFrame(frame);canvas.remove()}
  const timer=setTimeout(stop,1250);
  load(assetBase).then(()=>{if(stopped)return;function tick(now){const t=(now-start)/1000;if(stopped||t>=1.25||anchor&&!anchor.isConnected){clearTimeout(timer);stop();return}g.clearRect(0,0,rect.width,rect.height);const at=reduced?.35:t;drawRescue(g,at,{cx,foot,scale,variant,reduced,behind:true});drawRescue(g,at,{cx,foot,scale,variant,reduced,behind:false});frame=requestAnimationFrame(tick)}frame=requestAnimationFrame(tick)}).catch(()=>{clearTimeout(timer);stop()});
  return {stop(){clearTimeout(timer);stop()},duration:1.25};
 }
 window.EdenHealer={defs,launches,supports:id=>ids.has(id),duration:id=>id==='archangel'&&phase==='rettung'?1.25:durations[id],modeFor:id=>id==='archangel'&&phase==='rettung'?'rescue':'full',get phase(){return phase},set phase(p){phase=p==='rettung'?'rettung':'aufladen'},load,draw,drawBody,drawRescue,playRescue};
})();
