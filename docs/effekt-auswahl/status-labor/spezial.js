/* Individually choreographed 2D VFX studies. No game API, simulations or sound. */
(() => {
  'use strict';
  const PI=Math.PI,TAU=PI*2,clamp=x=>Math.max(0,Math.min(1,x));
  const smooth=x=>{x=clamp(x);return x*x*(3-2*x)};
  const bell=(t,c,w)=>Math.exp(-Math.pow((t-c)/w,2));
  const range=(t,a,b)=>smooth((t-a)/.25)*(1-smooth((t-b)/.55));
  const defs={
    mistral:[['Druckfront','Eine breite Druckfront trifft seitlich, wirft Staub auf und reißt in langen Fahnen weiter.'],['Fallwind','Ein schräger Fallwind schlägt von oben ein und bricht am Boden auseinander.']],
    wave:[['Brandungsfaust','Ein aufrollender Brecher schlägt über der Figur zusammen.'],['Rückstrom','Zwei schwere Wasserschübe treffen versetzt von beiden Seiten.']],
    wind:[['Wirbelsäule','Breite Luftbänder schrauben sich vor und hinter der Figur nach oben.'],['Sichelwind','Zwei große, gegensinnig laufende Windsicheln schließen sich um die Figur.']],
    tidal:[['Der Brecher','Eine hohe Flut baut sich auf und rollt quer über das ganze Kampffeld.'],['Flutwand','Das Wasser hebt sich hinter der Figur und stürzt als breite Wand nach vorne.']],
    doubleSlash:[['Kreuzschnitt','Zwei große Schnittbögen kreuzen sich mit zwei getrennten Treffermomenten.'],['Finte und Rückhand','Eine enge Finte geht in eine breite, tiefe Rückhand über.']],
    blur:[['Schattenwechsel','Zwei Nachbilder lösen sich seitlich ab; die echte Silhouette kehrt versetzt zurück.'],['Schleiertritt','Die Figur zerfließt in einem dunklen Schleier und erscheint im Gegenwind neu.']],
    vendetta:[['Rote Schneide','Ein schwerer, roter Abwärtsschnitt zieht einen dunklen Nachhall hinter sich her.'],['Zorn und Echo','Ein aufsteigender Schnitt kehrt als verzögerte zweite Schneide zurück.']],
    blackSlash:[['Licht aus','Die Szene verstummt im Dunkel. Ein einzelner heller Schnitt zerreißt die schwarze Fläche.'],['Schwarzer Vorhang','Ein dunkler Schleier schließt sich um die Figur und wird von innen aufgebrochen.']],
    reticle:[['Tunnelblick','Die Umgebung verdunkelt sich; ein präziser Schuss läuft auf einen einzigen Fokus zu.'],['Durchschlag','Ein langer Schuss zieht durch die Figur und hinterlässt einen aufgefächerten Druckschweif.']],
    calm:[['Totenstille','Die Farben weichen, das Wasser glättet sich. Eine tiefe Druckwelle bricht die Ruhe.'],['Auge des Sturms','Zwei gegenläufige Strömungen halten die Mitte frei, bevor ein einzelner ruhiger Impuls entsteht.']],
    beam:[['Leuchtturm','Ein breiter Suchscheinwerfer schwenkt über das Feld und hält die Figur im Licht fest.'],['Sonnenbruch','Ein schmaler Lichtspalt öffnet sich zu einem mächtigen, strukturierten Strahlenfächer.']],
    rain:[['Drei Sternenlanzen','Drei schwere Lichtlanzen schlagen nacheinander ein und werfen Druckfahnen auf.'],['Himmelsfall','Drei Bahnen sammeln sich über der Figur und entladen sich als ein gemeinsamer Lichtsturz.']]
  };
  let images,patternImage,patternMask;
  const tiles=new Map(),halos=new Map();
  const make=()=>{const c=document.createElement('canvas');c.width=600;c.height=560;return c};
  const material=make(),mg=material.getContext('2d');
  function gradient(g,colors,x0=0,y0=0,x1=0,y1=560){const p=g.createLinearGradient(x0,y0,x1,y1);colors.forEach((c,i)=>p.addColorStop(i/(colors.length-1),c));return p}
  function glow(g,x,y,r,color,a=1){g.save();g.globalAlpha=clamp(a);const p=g.createRadialGradient(x,y,0,x,y,r);p.addColorStop(0,color);p.addColorStop(1,color.slice(0,7)+'00');g.fillStyle=p;g.fillRect(x-r,y-r,r*2,r*2);g.restore()}
  function figure(g,x=0,y=0,a=1,filter='none'){if(!images.figure)return;const i=images.figure,w=475*i.width/i.height;g.save();g.globalAlpha=clamp(a);g.filter=filter;g.drawImage(i,300-w/2+x,32+y,w,475);g.restore()}
  function halo(g,color,a=1,x=0,y=0){
    if(!halos.has(color)){const c=make(),q=c.getContext('2d');figure(q);q.globalCompositeOperation='source-in';q.fillStyle=color;q.fillRect(0,0,600,560);const h=make(),z=h.getContext('2d');z.filter='blur(12px)';z.drawImage(c,0,0);z.filter='none';z.globalCompositeOperation='destination-out';figure(z);halos.set(color,h)}
    g.save();g.globalAlpha=clamp(a);g.drawImage(halos.get(color),x,y);g.restore();
  }
  function tile(t,color){
    const f=Math.floor(Math.max(0,t)*30)%64,key=f+color;
    if(tiles.has(key))return tiles.get(key);
    const c=document.createElement('canvas');c.width=c.height=256;const q=c.getContext('2d');
    q.drawImage(images.staub,f%8*256,Math.floor(f/8)*256,256,256,0,0,256,256);
    if(color){q.globalCompositeOperation='source-atop';q.fillStyle=color;q.fillRect(0,0,256,256)}
    if(tiles.size>128)tiles.delete(tiles.keys().next().value);tiles.set(key,c);return c;
  }
  function plume(g,t,x,y,w,h,a,color='#aabac490',angle=0){if(a<.004)return;g.save();g.globalAlpha=clamp(a);g.translate(x+w/2,y+h/2);g.rotate(angle);g.drawImage(tile(t,color),-w/2,-h/2,w,h);g.restore()}
  // Two independently scrolling material layers, retaining middle values.
  // Inspired by the public JangaFX Diablo 3 method; this is a Canvas adaptation.
  function flowTexture(g,t,a=.3){
    if(!patternImage)return;g.save();g.globalAlpha=a;g.globalCompositeOperation='multiply';
    const p=g.createPattern(patternImage,'repeat');g.translate(-(t*29)%256,-(t*17)%256);g.fillStyle=p;g.fillRect(-300,-300,1400,1400);
    g.translate((t*12)%256,(t*6)%256);g.scale(2,2);g.globalAlpha=a*.7;g.fillStyle=p;g.fillRect(-300,-300,900,900);g.restore();
    if(patternMask){g.save();g.globalCompositeOperation='destination-in';g.translate(-(t*24)%256,-(t*15)%256);g.fillStyle=g.createPattern(patternMask,'repeat');g.fillRect(-800,-800,2200,2200);g.restore()}
  }
  function ribbon(g,t,points,width,colors,a=1,rough=.1){
    if(a<.004)return;
    const samples=[];
    for(let i=0;i<=48;i++){
      const u=i/48,v=1-u;
      const x=v*v*v*points[0][0]+3*v*v*u*points[1][0]+3*v*u*u*points[2][0]+u*u*u*points[3][0];
      const y=v*v*v*points[0][1]+3*v*v*u*points[1][1]+3*v*u*u*points[2][1]+u*u*u*points[3][1];
      const dx=3*v*v*(points[1][0]-points[0][0])+6*v*u*(points[2][0]-points[1][0])+3*u*u*(points[3][0]-points[2][0]);
      const dy=3*v*v*(points[1][1]-points[0][1])+6*v*u*(points[2][1]-points[1][1])+3*u*u*(points[3][1]-points[2][1]);
      const length=Math.hypot(dx,dy)||1,w=width*Math.pow(Math.sin(PI*u),.7)*(1+rough*Math.sin(u*51+t*5)+rough*.5*Math.sin(u*97-t*3));
      samples.push([x,y,-dy/length*w,dx/length*w]);
    }
    mg.clearRect(0,0,600,560);mg.save();mg.beginPath();samples.forEach((p,i)=>i?mg.lineTo(p[0]+p[2],p[1]+p[3]):mg.moveTo(p[0]+p[2],p[1]+p[3]));samples.slice().reverse().forEach(p=>mg.lineTo(p[0]-p[2]*.4,p[1]-p[3]*.4));mg.closePath();mg.clip();
    mg.fillStyle=gradient(mg,colors,0,120,550,470);mg.fillRect(0,0,600,560);flowTexture(mg,t,.5);mg.restore();
    g.save();g.globalAlpha=clamp(a);g.filter='blur(1.2px)';g.shadowColor=colors[1];g.shadowBlur=15;g.drawImage(material,0,0);g.shadowBlur=0;g.restore();
  }
  function wave(g,t,x,height,width,a=1,flip=false){
    if(a<.004)return;
    mg.clearRect(0,0,600,560);mg.save();mg.translate(x,490);if(flip)mg.scale(-1,1);
    mg.beginPath();mg.moveTo(-width*.65,40);mg.bezierCurveTo(-width*.43,-height*.14,-width*.30,-height*.84,width*.02,-height);
    mg.bezierCurveTo(width*.23,-height*1.12,width*.42,-height*.86,width*.31,-height*.64);
    mg.bezierCurveTo(width*.19,-height*.57,width*.23,-height*.26,width*.39,-height*.13);
    mg.bezierCurveTo(width*.49,-height*.05,width*.52,5,width*.65,35);mg.closePath();mg.clip();
    mg.fillStyle=gradient(mg,['#d1f2eee8','#449faedc','#164c65e0','#102c4700'],0,-height,0,70);mg.fillRect(-width,-height*1.3,width*2,height*1.5+100);
    mg.translate(-x,-490);flowTexture(mg,t,.32);plume(mg,t,x-width*.65,440-height,width*1.2,height*.8,.8,'#d1e9ed80');mg.restore();
    g.save();g.globalAlpha=clamp(a);g.filter='blur(.9px)';g.drawImage(material,0,0);g.restore();
    plume(g,t+.2,x-width*.28,450-height,width*.78,height*.5,a*.8,'#e0eff0b0',flip?.2:-.2);
    plume(g,t+.35,x-width*.65,453,width*1.3,100,a*.8,'#d4e8eaa0');
  }
  function dust(g,t,hit,a=1){plume(g,t,95-hit*60,365-hit*30,400+hit*120,170,a,'#b9aa9390');}
  function flash(g,t,center,color='#e7f4ff',strength=.3){glow(g,300,280,450,color,bell(t,center,.1)*strength)}
  function shaft(g,t,top,bottom,width,a,color='#f4dfb5',lean=0){
    if(a<.004)return;
    const dx=bottom[0]-top[0],dy=bottom[1]-top[1],len=Math.hypot(dx,dy),nx=-dy/len,ny=dx/len;
    mg.clearRect(0,0,600,560);mg.save();mg.translate(top[0],top[1]);mg.rotate(Math.atan2(dy,dx)-PI/2);mg.beginPath();mg.moveTo(-width*.2,0);mg.lineTo(width*.2,0);mg.lineTo(width,len);mg.lineTo(-width,len);mg.closePath();mg.clip();
    mg.fillStyle=gradient(mg,[color+'00',color+'e0',color+'00'],-width,0,width,0);mg.fillRect(-width,0,width*2,len);flowTexture(mg,t,.45);mg.restore();
    g.save();g.globalAlpha=clamp(a);g.filter='blur(4px)';g.drawImage(material,0,0);g.restore();glow(g,bottom[0],bottom[1],width*2,color,a*.5);
  }
  function stage(g,light){
    g.fillStyle=gradient(g,light?['#858d8f','#adb3ac','#687979']:['#0a121e','#233344','#101b27']);g.fillRect(0,0,600,560);
    glow(g,305,270,380,light?'#b8c9c4':'#345568',.38);g.fillStyle=gradient(g,['#101a2500','#0b121de8'],0,430,0,560);g.fillRect(0,430,600,130);
    g.save();g.filter='blur(11px)';g.fillStyle='#0007';g.beginPath();g.ellipse(300,502,103,11,0,0,TAU);g.fill();g.restore();
  }
  function render(canvas,id,time,variant,settings={}){
    const g=canvas.getContext('2d'),t=time%5.4,v=variant,hit=bell(t,1.52,.19),env=range(t,.45,2.7),fall=smooth((t-1.2)/1.5);
    const shown=settings.figure!==false,light=settings.light;
    const warm=['doubleSlash','vendetta','blackSlash','reticle','beam','rain'].includes(id);
    const color=id==='vendetta'?'#cc7264':warm?'#f3d7a3':'#9ad6e7';
    g.save();g.clearRect(0,0,600,560);stage(g,light);
    g.translate(Math.sin(t*71)*hit*(v?5:3),Math.cos(t*61)*hit*2);
    // Anticipation, local light, then the main gesture and its residue.
    glow(g,300,320,260,color,bell(t,.75,.4)*.13);
    if(id==='wind'){
      for(let j=0;j<3;j++){const y=465-j*116-fall*60,shift=Math.sin(t*4+j)*65;
        ribbon(g,t+j,[[80,y],[140,y-135],[430+shift,y+125],[530,y-70]],v?18:29,['#b5e4ed00','#b0d5de90','#f4fdffcc'],env*.48,.2)}
    }
    if(id==='tidal'&&v===1)wave(g,t,340,340*smooth((t-.3)/1),540,env*.75,true);
    if(id==='blur'&&shown){
      for(let j=3;j>0;j--){figure(g,(v?1:-1)*j*(40+fall*25),-j*4,env*(.24-j*.04),'blur(3px) saturate(.25)');}
    }
    if(shown){halo(g,color,.35+env*.4);figure(g,id==='blur'?Math.sin(t*3)*env*45:hit*7,0,id==='blur'?1-env*.7:1,id==='calm'?'saturate(.15)':'none')}
    switch(id){
      case 'mistral':{
        const sweep=-280+smooth((t-.65)/1.25)*1000;
        if(!v){plume(g,t,sweep-340,130,420,350,env*.9,'#d1e1e6a0',-.3);for(let j=0;j<3;j++)ribbon(g,t+j,[[-80,250+j*90],[150,120+j*60],[360,360+j*40],[700,160+j*100]],24-j*4,['#8eabb500','#c6dfe6ad','#f5ffffb0'],env*.6,.24);dust(g,t,hit,env*.8);}
        else{plume(g,t,110,70+fall*225,370,390,env*.85,'#c4dae8b0',-.7);ribbon(g,t,[[35,-100],[110,180],[350,350],[610,525]],55,['#a1c9da00','#c6e0e6c0','#ecfcffc0'],env,.18);dust(g,t,hit,env);}
        break;}
      case 'wave':{
        if(!v)wave(g,t,80+fall*350,250*env,360,env);
        else{wave(g,t,140+fall*130,190,320,range(t,.45,1.8));wave(g,t+.6,470-fall*130,265,350,range(t,1.15,2.8),true)}
        flash(g,t,1.5,'#b9eff3',.18);break;}
      case 'wind':{
        if(!v){for(let j=0;j<3;j++){const y=425-j*115+Math.sin(t*3+j)*25;ribbon(g,t+j,[[45,y],[180,y+100],[440,y-170],[560,y-50]],25,['#8fc1cd00','#c3e0e6af','#e9fdffc0'],env*.85,.21)}plume(g,t,180,60,250,440,env*.32,'#bcdde480');}
        else{ribbon(g,t,[[70,480],[530,500],[550,55],[260,65]],43,['#76b1bd00','#cee5e8bc','#efffffd0'],env,.16);ribbon(g,t+.8,[[530,470],[30,420],[130,30],[340,110]],35,['#8ab6bd00','#adcfdac0','#f1ffffc0'],env*.85,.17);}
        break;}
      case 'tidal':{
        if(!v){wave(g,t,-80+fall*620,390,650,env);plume(g,t,10,30+fall*290,590,350,env*.4,'#def0eea0');}
        else{const crash=range(t,1.1,2.6);wave(g,t+.4,300,420*(1-fall*.35),640,crash);plume(g,t,20,170+fall*150,600,320,crash*.75,'#d0edf3ad');}
        flash(g,t,1.52,'#d3f6f8',.2);break;}
      case 'doubleSlash':{
        const a=bell(t,1.3,.25),b=bell(t,1.8,.29);
        ribbon(g,t,v?[[70,340],[180,100],[470,140],[520,330]]:[[30,95],[130,195],[410,325],[570,455]],v?28:37,['#86725300','#d8d4c9c0','#ffffe9f0'],a,.16);
        ribbon(g,t+.4,v?[[590,440],[340,500],[140,290],[30,160]]:[[560,90],[430,200],[180,330],[20,470]],v?58:42,['#a2927800','#eddfc8d0','#fff7d5f0'],b,.13);
        plume(g,t,150,200,330,220,(a+b)*.24,'#d6d1bfa0');flash(g,t,1.8,'#fff3d0',.17);break;}
      case 'blur':{
        if(!v){plume(g,t,60-fall*80,160,520+fall*100,330,env*.68,'#2b3d5bd0');ribbon(g,t,[[20,380],[180,260],[420,440],[620,165]],42,['#16202d00','#6e93a060','#c6e1e690'],env*.5,.3);if(shown&&t>1.55)figure(g,35*(1-fall),0,smooth((t-1.55)/.8));}
        else{plume(g,t,160,40+fall*280,300,500-fall*180,env*.9,'#172b42e0',-.3);if(shown){figure(g,-85*(1-fall),-20,env*.25,'blur(4px)');halo(g,'#9dcfd4',bell(t,2.2,.5));}}
        break;}
      case 'vendetta':{
        const a=bell(t,v?1.25:1.55,.3),b=v?bell(t,1.95,.32):0;
        ribbon(g,t,v?[[40,470],[150,370],[365,130],[565,90]]:[[110,15],[170,150],[430,360],[505,540]],v?46:62,['#3c132000','#9b3d39c0','#ffb397e0'],a,.2);
        if(v)ribbon(g,t+.6,[[550,145],[430,220],[180,450],[30,490]],33,['#41111d00','#aa4b4dcc','#ffd1ade0'],b,.15);
        plume(g,t,160,180,350,310,(a+b)*.38,'#682b35a0');flash(g,t,v?1.95:1.55,'#e49578',.19);break;}
      case 'blackSlash':{
        g.save();g.fillStyle=`rgba(2,5,12,${env*.94})`;g.fillRect(-30,-30,660,620);g.restore();
        if(!v){ribbon(g,t,[[-70,410],[90,360],[435,150],[650,150]],35,['#413c4000','#bcb9afd0','#fff6daff'],bell(t,1.6,.24),.15);}
        else{plume(g,t,0,30,600,520,env*.75,'#030711f0');ribbon(g,t,[[210,-60],[250,170],[370,350],[390,620]],50,['#363f5000','#a2c9d9cc','#f4fdffe8'],bell(t,1.5,.38),.28);}
        flash(g,t,1.6,'#f0eddb',.13);break;}
      case 'reticle':{
        g.save();const focus=g.createRadialGradient(300,225,50,300,225,290);focus.addColorStop(0,'#06101c00');focus.addColorStop(1,`rgba(0,4,13,${env*.82})`);g.fillStyle=focus;g.fillRect(0,0,600,560);g.restore();
        glow(g,300,228,75,'#ffd8a4',bell(t,.9,.4)*.45);
        if(!v){ribbon(g,t,[[20,345],[150,300],[270,240],[305,225]],16,['#64524900','#dfbf8be0','#fff6dcff'],bell(t,1.5,.19),.08);plume(g,t,230,170,240,140,bell(t,1.7,.35),'#d2c4a4a0');}
        else{ribbon(g,t,[[-40,320],[155,275],[380,235],[650,185]],24,['#6c6e6800','#b3d7d9e0','#f2fffff0'],bell(t,1.52,.28),.12);plume(g,t,310,145,320,230,bell(t,1.8,.45),'#beced7a0',-.3);}
        flash(g,t,1.52,'#fff0cf',.22);break;}
      case 'calm':{
        g.save();g.globalAlpha=env*.22;g.fillStyle='#b2d5da';g.fillRect(0,0,600,560);g.restore();
        if(!v){ribbon(g,t,[[-60,470],[130,445],[460,490],[670,455]],10+hit*24,['#739eac00','#b6d9e6b0','#eefcffb0'],env,.05);plume(g,t,50,395,520,110,env*.3,'#c9e3ed80');glow(g,300,440,230,'#bedee7',hit*.4);}
        else{plume(g,t,-140+fall*90,100,360,420,env*.62,'#c1d6db90');plume(g,t+.8,400-fall*80,80,360,440,env*.62,'#a7cad790');ribbon(g,t,[[40,495],[160,465],[430,495],[580,470]],18,['#a1bac900','#d0e9e9b0','#f1ffff90'],env*.8,.08);}
        break;}
      case 'beam':{
        if(!v){const end=120+smooth((t-.3)/1.6)*390;shaft(g,t,[85,-60],[end,510],105,env,'#f9dfa5');shaft(g,t+.6,[85,-60],[end+28,510],26,env*.65,'#fff3d5');plume(g,t,110,120,400,370,env*.25,'#e6cfac60');}
        else{for(let j=0;j<5;j++)shaft(g,t+j*.3,[300,-50],[70+j*115,520],24+j%2*14,env*(.45+hit*.2),'#e8e2bf');shaft(g,t,[300,-30],[300,500],60,env*.75,'#fff0c9');}
        flash(g,t,1.52,'#fff2d5',.17);break;}
      case 'rain':{
        if(!v){for(let j=0;j<3;j++){const a=bell(t,1.05+j*.4,.32),x=185+j*115;shaft(g,t+j,[x-180,-70],[x,485],32,a,'#d7e9ff');plume(g,t+j,x-140,352,280,180,a*.85,'#c0d5e8ad');}}
        else{for(let j=0;j<3;j++)shaft(g,t+j,[30+j*270,-60],[300,220],18,range(t,.35,1.55),'#bfd9f4');shaft(g,t,[300,140],[300,510],125,bell(t,1.8,.46),'#e5f3ff');plume(g,t,10,285,580,280,bell(t,2,.5),'#ccdfeac0');}
        break;}
    }
    // Brief letterbox and a single local impact emphasize scale without strobing.
    const bars=env*17;g.fillStyle='#030711b0';g.fillRect(-20,0,640,bars);g.fillRect(-20,560-bars,640,bars);
    g.restore();
  }
  window.EdenSpecialFx={defs,render,init(value){images=value;patternImage=value.flow;patternMask=value.flowMask;},duration:5.4};
})();
