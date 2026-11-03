/* Shared attack choreography for the isolated lab. Existing material sources only. */
(()=>{'use strict';
const PI=Math.PI,C=x=>Math.max(0,Math.min(1,x)),S=x=>{x=C(x);return x*x*(3-2*x)},mix=(a,b,p)=>a+(b-a)*p;
const pulse=(t,c,w)=>Math.exp(-Math.pow((t-c)/w,2));
const life=(a,d=1.4)=>a<0||a>d?0:S(a/.08)*(1-S((a-d*.45)/(d*.55)));
const defs={
 mistral:{name:'Mistral',kind:'hurt',variants:[['Wilder Schwung','Drei unterbrochene Windbahnen kreisen beim Ausholen, beschleunigen und entladen sich als harter Schlag. Hurt und Rückstoß gehen in kurzes erschüttertes Rütteln über.'],['Schweres Ausholen','Breitere kreisende Luftbahnen sammeln Schwung für einen kräftigeren Einzelhieb.'],['Gegenschwung','Eine gegenläufige Windbahn führt in zwei versetzte Drucktreffer.']]},
 wave:{name:'Ressac',kind:'hurt',variants:[['Wasserlanze · Referenz','Die abgestimmte Wasserkugel mit Gischt, kurzem Flug und länger sichtbarer Trefferpose.'],['Wasserhammer','Ein schwerer, flacherer Wasserkörper schießt in einem niedrigen Bogen zum Ziel.'],['Zwillingsstoß','Zwei kleinere Wasserkugeln treffen mit kurzem Abstand aus verschiedenen Höhen.']]},
 wind:{name:'Libeccio',kind:'guard',variants:[['Zwei Nebeltrichter','Zwei schmale Tornados stehen seitlich der Figur und lösen sich weich auf.'],['Umlaufender Tornado','Ein kleiner Wirbel zieht vor und hinter der Figur entlang.'],['Sich öffnende Wirbel','Zwei schmale Trichter entstehen nah am Körper und wandern auseinander.']]},
 tidal:{name:'Lame de Fond',kind:'hurt',variants:[['Brechende Wasserwand','Bodennahe Strömungen sammeln sich zu einer hohen Wasserwand. Die überhängende Krone kippt über den Gegner und zerfällt in bewegliche Gischt; kräftiger Rückstoß und lange Hurt-Reaktion.'],['Steigender Brecher','Eine bodennahe Wassermasse steigt im Flug an und trifft von unten.'],['Doppelte Kaskade','Ein erster Druckstoß wird von einem kleineren, höher liegenden Schub eingeholt.']]},
 doubleSlash:{name:'Doppio Gioco',kind:'hurt',variants:[['Kreuzschnitt','Zwei lange violette Klingenspuren kreuzen sich als gerichtete Wischer. Jeder Treffer löst Hurt und einen eigenen Rückstoß aus; der zweite setzt kräftiger nach.'],['Finte und Rückhand','Ein kurzer erster Wischer kündigt die tiefere, kräftige Rückhand an.'],['Auf und ab','Eine steigende Klinge geht in einen steilen Abwärtsschnitt über.']]},
 blur:{name:'Sotto Voce',kind:'evade',variants:[['Seitlicher Wechsel','Die Figur löst sich seitlich aus ihrer alten Silhouette und tritt wieder hervor.'],['Schleiertritt','Ein dünner Schleier verbirgt die Bewegung; ein versetztes Nachbild bleibt zurück.'],['Doppeltes Echo','Zwei kurze, entgegengesetzte Nachbilder laufen mit zeitlichem Abstand aus.']]},
 vendetta:{name:'Vendetta',kind:'hurt',variants:[['Roter Diagonalschnitt','Eine längere, flachere karminrote Klingenspur trifft hart; deutlicher Rückstoß, Hurt und ein kurzer roter Kontaktreflex.'],['Verzögerte Rückhand','Ein knapper Ansatz wird von einer tieferen Rückhand abgelöst.'],['Steiler Hieb','Ein fast senkrechter Schnitt trifft einmal und klingt ohne zusätzliche Explosion aus.']]},
 blackSlash:{name:'Omertà',kind:'hurt',variants:[['Goldener Durchbruch','Goldenergie verdichtet sich lange, schießt zum Gegner und entlädt sich als flacher, explosiver Schnitt mit Funken und kräftiger Hurt-Reaktion.'],['Schwere Gold-Rückhand','Eine tiefer geladene Energie trifft als diagonale Rückhand. Der goldene Einschlag bricht breit auseinander.'],['Urteil von oben','Eine kompakte Goldladung entlädt sich in einem steilen Schnitt mit heißem Kern und auseinanderstiebenden Partikeln.']]},
 reticle:{name:'Point de Mire',kind:'guard',variants:[['Ruhiger Fokus','Ein schmaler kühler Reflex markiert die Schwachstelle; das Ziel nimmt eine Schutzpose ein.'],['Wandernder Fokus','Ein feiner Lichtreflex wandert seitlich über das Ziel und legt seine Schwäche offen.'],['Schwäche offenlegen','Zwei dezente Reflexe betonen die Markierung; keine Flugspur und kein Schadenseinschlag.']]},
 calm:{name:'Bonaccia',kind:'guard',variants:[['Glatte Strömung','Bodennaher Wasserdunst wird ruhiger; ein kühler Reflex zieht über den Körper.'],['Windstille','Zwei Luftfahnen weichen auseinander und geben die Figur frei.'],['Tiefe Ruhe','Ein langsamer Schleier sinkt zurück; Licht und Farbe beruhigen sich gemeinsam.']]},
 beam:{name:'Phare',kind:'guard',variants:[['Leuchtfeuer','Ein wandernder, volumetrischer Lichtkegel streift die Figur und hält kurz inne.'],['Lichtspalt','Ein schmaler Lichtschacht öffnet sich von oben und fällt über Körper und Boden.'],['Gegenlicht','Zwei unterschiedlich warme Lichtquellen lösen einander hinter der Figur ab.']]},
 rain:{name:'Pluie d’Étoiles',kind:'hurt',variants:[['Sternfolge','Drei kurze Lichtfälle treffen nacheinander; jeder Kontakt bleibt örtlich begrenzt.'],['Schräger Sternfall','Drei schräg fallende Lichtspuren schlagen versetzt um die Figur ein.'],['Bündelung','Drei schmale Bahnen laufen gleichzeitig am Körper zusammen.']]}
};
const bladeLayer=document.createElement('canvas');bladeLayer.width=512;bladeLayer.height=128;
const lightLayer=document.createElement('canvas');lightLayer.width=200;lightLayer.height=600;
function photo(A,name,x,y,w,h,a=1,angle=0){
 if(a<.002)return;const i=A.images[name],b=A.crops[name]||[0,0,i.width,i.height],g=A.g;
 g.save();g.globalAlpha=C(a);g.translate(x,y);g.rotate(angle);g.drawImage(i,...[b[0],b[1],b[2]-b[0],b[3]-b[1]],-w/2,-h/2,w,h);g.restore();
}
function blade(A,when,angle,length=265,height=35,reverse=false){
 length*=1.3;height*=.62;
 const p=(A.age-when+.15)/.32;if(p<=0||p>=1.65)return;
 const material=A.id==='blackSlash'?'stahlgold':A.id==='vendetta'?'stahlrot':A.id==='doubleSlash'?'stahlviolett':'stahl';
 const q=bladeLayer.getContext('2d'),i=A.images[material],b=A.crops[material];
 q.clearRect(0,0,512,128);q.globalCompositeOperation='source-over';
 const head=256-length/2+p*length,trail=length*.65;
 q.drawImage(i,b[0],b[1],b[2]-b[0],b[3]-b[1],head-trail,64-height/2,trail,height);
 q.globalCompositeOperation='destination-in';const m=q.createLinearGradient(256-length/2,0,256+length/2,0);
 m.addColorStop(0,'#fff0');m.addColorStop(.07,'#ffff');m.addColorStop(.93,'#ffff');m.addColorStop(1,'#fff0');q.fillStyle=m;q.fillRect(0,0,512,128);q.globalCompositeOperation='source-over';
 const g=A.g;g.save();g.translate(666,when<0?270:299);g.rotate(angle);if(reverse)g.scale(-1,1);g.globalAlpha=.92;g.drawImage(bladeLayer,-256,-64);g.restore();
}
function contact(A,when=0,warm=false,weight=1){
 const a=A.age-when;if(a<0||a>1)return;
 A.glow(666,296,54,64,A.id==='vendetta'?'#b94b405c':A.id==='doubleSlash'?'#ac77d880':warm?'#d4b49e70':'#c2dbe570',pulse(a,.025,.04)*.28*weight);
 A.mist(A.clock+when,664+a*18,320,130+a*55,100,life(a,.85)*.12*weight);
 photo(A,'glint',666,297,28,19,pulse(a,.025,.035)*.2*weight);
}
function shaft(A,x,y,w,h,a,angle=0){
 if(a<.003)return;
 const q=lightLayer.getContext('2d'),i=A.images.licht,b=A.crops.licht;
 q.clearRect(0,0,200,600);q.globalCompositeOperation='source-over';
 q.drawImage(i,b[0],b[1],b[2]-b[0],b[3]-b[1],0,0,200,600);
 q.globalCompositeOperation='destination-in';const m=q.createLinearGradient(0,0,200,0);
 m.addColorStop(0,'#fff0');m.addColorStop(.24,'#fff9');m.addColorStop(.5,'#ffff');m.addColorStop(.76,'#fff9');m.addColorStop(1,'#fff0');q.fillStyle=m;q.fillRect(0,0,200,600);q.globalCompositeOperation='source-over';
 const g=A.g;g.save();g.globalAlpha=C(a);g.translate(x,y);g.rotate(angle);g.globalCompositeOperation='screen';g.drawImage(lightLayer,-w/2,-h/2,w,h);g.restore();
 A.mist(A.clock*.8,x,y+h*.18,w*1.4,h*.27,a*.13);
}
function ghost(A,dx,a){
 if(!A.shown||a<.002)return;const i=A.images.idle,h=420,w=h*i.width/i.height,g=A.g;
 g.save();g.globalAlpha=a;g.filter='blur(2px)';g.drawImage(i,666-w/2+dx,75,w,h);g.restore();
}
function waterAttack(A){
 const heavy=A.id==='tidal',v=A.variant,build=S((A.t-.3)/.72),f=A.flight;
 const size=heavy?62:47,startY=v===1?385:300;
 if(A.t<1.12){
  A.waterOrb(A.clock,220,startY,18+build*(size-18),S((A.t-.3)/.2)*.96,v===1?1.18:1);
  if(v===2)A.waterOrb(A.clock+.31,155,370,12+build*20,S((A.t-.5)/.25)*.9);
 }
 const project=(p,y,r,lag=0)=>{
  const progress=C((A.t-1.12-lag)/.38);if(A.t<1.12+lag||A.t>=1.5+lag)return;
  const x=mix(220,656,progress),yy=mix(y,299,progress)-Math.sin(progress*PI)*(heavy?40:25);
  A.stream(A.clock,x-50,yy,120,35,.32,-.04);A.waterOrb(A.clock+lag,x,yy,r,.98,v===1?1.18:1.05);
 };
 project(f,startY,size,0);if(v===2)project(f,370,size*.62,.18);
 A.splashContact(A.age);if(v===2&&A.age>.18){const g=A.g;g.save();g.translate(70,-45);g.translate(666,299);g.scale(.67,.67);g.translate(-666,-299);A.splashContact(A.age-.18);g.restore();}
}
const vortexCache=new Map();
function tornado(A,x,foot,w,h,a,seed=0,lean=0,profile='slim'){
 if(a<.003)return;
 const tick=Math.floor((A.clock+seed)*30),key=String(tick)+profile;
 if(!vortexCache.has(key)){
  const c=document.createElement('canvas');c.width=192;c.height=320;
  const q=c.getContext('2d'),im=q.createImageData(192,320),tm=tick/30;
  for(let py=0;py<320;py++){
   const height=1-py/319;
   const wide=profile==='wide';
   const radius=wide?12+52*Math.pow(height,.62)+6*Math.sin(height*PI):8+47*Math.pow(height,.72);
   const axis=96+Math.sin(height*3.6+tm*1.8)*height*12;
   const vertical=S(height/.055)*(1-S((height-.81)/.19));
   for(let px=0;px<192;px++){
    const u=(px-axis)/radius,d=Math.abs(u),i=(py*192+px)*4;if(d>=1)continue;
    const z=Math.sqrt(1-u*u),angle=Math.atan2(u,z);
    // Advect density around a tapered volume, with soft helical variations.
    const sx=angle*57-tm*89+height*83,sy=height*212-tm*31;
    const n=A.sample(sx,sy),n2=A.sample(sx*2.3+37,sy*1.6-tm*19);
    const cloud=S((n*.62+n2*.38-.22)/.65);
    const twist=.6+.4*Math.sin(angle*2.1+height*(wide?32:43)-tm*(wide?9.5:12)+n2*2.5);
    const edge=S((1-d)/.32),density=(.24+.76*cloud)*twist*edge*vertical;
    const light=110+z*33-u*18+n2*24;
    im.data[i]=light*.93;im.data[i+1]=light*.98;im.data[i+2]=light;
    im.data[i+3]=Math.round(255*density*.9);
   }
  }
  q.putImageData(im,0,0);if(vortexCache.size>10)vortexCache.delete(vortexCache.keys().next().value);vortexCache.set(key,c);
 }
 const g=A.g;g.save();g.globalAlpha=C(a);g.translate(x,foot);g.rotate(lean);g.drawImage(vortexCache.get(key),-w/2,-h,w,h);g.restore();
}

// Gold materials retain the existing raster microstructure and native simulation alpha.
function goldMaterial(A){
 if(A.images.stahlgold)return;
 for(const [key,source] of [['stahlgold','stahl'],['impactGold','impact'],['glintGold','glint']]){
  const i=A.images[source],c=document.createElement('canvas');c.width=i.width;c.height=i.height;
  const q=c.getContext('2d');q.drawImage(i,0,0);q.globalCompositeOperation='source-atop';q.globalAlpha=.44;q.fillStyle='#e8ad38';q.fillRect(0,0,c.width,c.height);q.globalAlpha=1;q.globalCompositeOperation='source-over';A.images[key]=c;
 }
 A.crops.stahlgold=A.crops.stahl;
}
const energyVolume=document.createElement('canvas');energyVolume.width=energyVolume.height=128;
function goldCharge(A){
 const {g,t,clock,variant:v}=A;if(t<.3||t>=1.5)return;
 const build=S((t-.3)/.78),flight=S((t-1.12)/.38),x=220+flight*436,y=[300,345,350][v]+(299-[300,345,350][v])*flight;
 const radius=(17+build*25)*(1-flight*.45),q=energyVolume.getContext('2d'),im=q.createImageData(128,128);
 for(let py=0;py<128;py++)for(let px=0;px<128;px++){
  const dx=(px-64)/60,dy=(py-64)/60,dist=Math.hypot(dx,dy),n=A.sample(px*2.3+clock*35,py*2.1-clock*51),n2=A.sample(px*4-clock*26,py*3.7+clock*22),edge=1-S((dist-(.43+n*.18))/.35);
  const density=edge*(.25+.75*n2)*build,i=(py*128+px)*4,hot=Math.pow(Math.max(0,1-dist),2);
  im.data[i]=255;im.data[i+1]=135+hot*115+n2*28;im.data[i+2]=30+hot*180;im.data[i+3]=255*C(density);
 }
 q.putImageData(im,0,0);g.save();g.globalCompositeOperation='screen';g.drawImage(energyVolume,x-radius,y-radius,radius*2,radius*2);g.restore();
 A.glow(x,y,radius*2.4,radius*2.1,'#eab65c80',build*.3);
 const gather=t<1.12?build:1-flight;
 for(let i=0;i<32;i++){
  const p=(clock*.62+i*.618)%1,angle=i*2.399+clock*.55,r=(1-p)*(75+22*Math.sin(i*7));
  photo(A,'glint',x+Math.cos(angle)*r,y+Math.sin(angle)*r*.72,2+p*4,2+p*4,Math.sin(p*PI)*gather*.68);
 }
 A.mist(clock,x,y+14,radius*3,radius*2.2,build*.10);
}
function goldRelease(A,behind){
 const a=A.age,v=A.variant,g=A.g;
 if(!behind)blade(A,-.08,[.12,-.42,1.04][v],[320,300,285][v],v===2?43:39,v===1);
 if(a<0||a>1.5)return;
 if(behind){A.glow(666,299,165,180,'#d69b3d90',pulse(a,.045,.085)*.65);return;}
 // Native EmberGen impact: rapidly expanding first frames, then particles dissipate.
 const size=95+S(a/.25)*[275,295,320][v];
 A.sheet('impactGold',Math.min(63,a*62),666,299,size,size*.83,life(a,1.12)*.95,[.12,-.25,.5][v]);
 A.glow(666,299,66,83,'#fff0cb',pulse(a,.028,.032)*.62);
 for(let i=0;i<84;i++){
  const seed=Math.sin(i*127.1+v*73.7)*43758.5453,n=seed-Math.floor(seed),angle=i*2.399+v*.7,speed=90+n*235,travel=1-Math.exp(-a*3.8),x=666+Math.cos(angle)*speed*travel,y=299+Math.sin(angle)*speed*.65*travel+a*a*70;
  const fade=life(a,.6+n*.65)*(i%4===0?.8:.45),w=i%4===0?10:4;
  photo(A,'glintGold',x,y,w*(1+a*2),w*.55,fade,angle);
 }
 A.mist(A.clock,680+a*27,320,160+a*190,130+a*90,life(a,1.3)*.16);
}

function draw(A,behind){
 const {g,id,variant:v,age,clock,t}=A,build=S((t-.3)/.72),fade=life(age,1.65),pre=t<1.12?build:0;
 if(id==='tidal'&&v===0){window.EdenTidalWall.draw(A,behind);return;}
 if(id==='blackSlash'){goldMaterial(A);if(!behind)goldCharge(A);goldRelease(A,behind);return;}
 if(id==='wave'||id==='tidal'){if(!behind)waterAttack(A);return;}
 if(id==='mistral'){window.EdenMistralSwing.draw(A,behind);return;}
 if(id==='wind'){
  const env=t<1.5?build*.8:fade;
  if(v===0&&behind){tornado(A,604,494,102,255,env*.86);tornado(A,757,493,87,215,env*.73,.65,.045);}
  if(v===1){
   const phase=clock*2.8,x=675+Math.cos(phase)*78,isRear=Math.sin(phase)<0;
   if(behind===isRear)tornado(A,x,493+Math.sin(phase)*6,110,244,env*.88,.3);
  }
  if(v===2&&behind){
   const open=S((t-.8)/1.4);
   tornado(A,642-open*81,494,95,242,env*.82,.2,-.035);
   tornado(A,699+open*84,494,91,224,env*.78,.85,.035);
  }
  if(!behind)A.mist(clock,666,493,245,32,env*.07);
  return;
 }
 if(id==='doubleSlash'||id==='vendetta'||id==='blackSlash'){
  if(behind){
   if(id==='blackSlash')A.mist(clock,535+S((t-1.1)/.4)*130,285,320,220,(pre*.16+fade*.15));
   return;
  }
  if(id==='doubleSlash'){
   if(v===0){blade(A,-.23,.48,260,32);blade(A,.06,-.52,270,36,true);}
   if(v===1){blade(A,-.27,-.14,155,24);blade(A,.06,.12,280,38,true);}
   if(v===2){blade(A,-.23,-.72,230,34);blade(A,.06,1.08,215,37);}
   contact(A,v===1?-.27:-.23,false,.8);contact(A,.06,false,1.3);
  }
  if(id==='vendetta'){
   if(v===0)blade(A,0,.84,265,39);
   if(v===1){blade(A,-.24,-.3,150,22);blade(A,.08,.08,250,39,true);}
   if(v===2)blade(A,0,1.27,230,39);
   contact(A,v===1?.08:0,true,1);
  }
return;
 }
 if(id==='blur'){
  const env=t<1.5?build:fade;
  if(behind){
   if(v===0)ghost(A,-52*S((t-1.12)/.6),env*.23);
   if(v===1){ghost(A,35,env*.15);A.mist(clock,655,320,235,310,env*.23);}
   if(v===2){ghost(A,-43,life(age+.22,1.25)*.21);ghost(A,48,life(age-.12,1.2)*.18);}
  }else A.mist(clock*.8,665,480,245,58,env*.13);
  return;
 }
 if(id==='reticle'){
  if(behind)return;
  const env=t<1.5?build*.8:fade;
  const x=v===1?640+Math.sin(clock*1.6)*30:666;
  photo(A,'licht',x,292,42,205,env*.2,v===1?-.14:.04);
  if(v===2)photo(A,'licht',692,310,28,160,env*.12,-.18);
  A.glow(x,285,39,62,'#b6ccd63b',env*.17);
  A.mist(clock*.65,638,330,120,170,env*.065);return;
 }
 if(id==='calm'){
  const env=t<1.5?build*.85:fade;
  if(behind){
   if(v===0){A.stream(clock*.5,665,489,390,40,env*.16);A.mist(clock*.5,666,470,370,75,env*.15);}
   if(v===1){A.mist(clock*.65,600-env*150,350,240,200,env*.27);A.mist(clock*.65+.5,730+env*125,360,220,190,env*.24);}
   if(v===2)A.mist(clock*.45,666,470-env*50,390,120,env*.24);
  }else A.glow(666,360,110,195,'#a5cbdc22',env*.14);
  return;
 }
 if(id==='beam'){
  const env=t<1.5?build*.8:fade;
  if(behind){
   if(v===0)shaft(A,610+Math.sin(clock*.9)*65,240,155,610,env*.64,-.13);
   if(v===1)shaft(A,666,240,100,620,env*.72,.035);
   if(v===2){shaft(A,582,240,135,610,env*(.32+.14*Math.sin(clock*1.4)),.22);shaft(A,745,240,150,610,env*(.35-.14*Math.sin(clock*1.4)),-.22);}
  }else A.glow(666,494,140,23,'#dac7a84d',env*.3);
  return;
 }
 if(id==='rain'&&!behind){
  if(t<1.12){A.mist(clock*.5,666,80,350,100,pre*.15);A.glow(665,70,90,26,'#cdd7e540',pre*.18);}
  for(let j=0;j<3;j++){
   const when=v===2?0:j*.23,x=v===2?666:[596,686,746][j],a=age-when;
   if(a>=-.13&&a<.1){const p=C((a+.13)/.18),angle=v===1?.28:(v===2?(j-1)*.15:0);shaft(A,x,40+p*150,35,330,pulse(a,-.01,.07)*.75,angle);}
   const strength=pulse(a,.025,.04);
   A.glow(x,301,45,67,'#d5dbea65',strength*.25);
   A.mist(clock+j,x,320+Math.max(0,a)*28,120,85,life(a,.85)*.17);
  }
 }
}
function hits(id,v){
 if(id==='doubleSlash')return v===1?[-.27,.06]:[-.23,.06];
 if(id==='vendetta'&&v===1)return [-.24,.08];
 if(id==='mistral'&&v===2)return [0,.22];
 if((id==='wave'||id==='tidal')&&v===2)return [0,.18];
 if(id==='rain'&&v!==2)return [0,.23,.46];
 return [0];
}
const launches={mistral:2.25,wave:3.12,wind:2.6,tidal:3.12,doubleSlash:1.65,blur:1.8,vendetta:2,blackSlash:2.9,reticle:2.4,calm:2.9,beam:3,rain:2.65};
window.EdenAttackLibrary={defs,draw,hits,launches};
})();
