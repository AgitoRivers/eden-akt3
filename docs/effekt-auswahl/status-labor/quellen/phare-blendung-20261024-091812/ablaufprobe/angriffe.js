/* Shared attack choreography for the isolated lab. Existing material sources only. */
(()=>{'use strict';
const PI=Math.PI,C=x=>Math.max(0,Math.min(1,x)),S=x=>{x=C(x);return x*x*(3-2*x)},mix=(a,b,p)=>a+(b-a)*p;
const pulse=(t,c,w)=>Math.exp(-Math.pow((t-c)/w,2));
const life=(a,d=1.4)=>a<0||a>d?0:S(a/.08)*(1-S((a-d*.45)/(d*.55)));
const defs={
 scirocco:{name:'Scirocco',kind:'hurt',variants:[['Verdichteter Feuerball','Eine native EmberGen-Feuerkugel lädt sich vor Ducs Oberkörper auf. Sie wird gerade geschleudert und platzt am Gegner mit Flammen, Rauch und Funken. Ein Treffer.'],['Schwerer Feuerball','Eine größere, schwerere Feuerkugel lädt höher und fliegt geradlinig ins Ziel. Breite explosive Entladung.'],['Konzentrierter Feuerkern','Ein kleinerer, konzentrierter Feuerkern wird geradlinig ins Ziel geschleudert und entlädt sich als hohe Flammensäule am Ziel.']]},
 retour:{name:'Retour de Flamme',kind:'hurt',variants:[['Funkenladung und Konter','Phase 1: Energie mit einziehenden Funken am Körper laden und halten. Phase 2: ein gerichteter Feuer-Slash mit explosivem Impact. Im kompletten Ablauf nimmt Duc vor dem Konter einen Treffer mit eigener Hurt-Pose.'],['Kreisende Racheglut','Die Ladung kreist mit Funken am Oberkörper. Beim Konter entlädt sie sich als diagonale Flammenrückhand mit breiter Explosion.'],['Verdichtete Racheglut','Zwei kleine Glutkerne sammeln sich am Körper. Beim Konter werden sie zu einem steilen Feuer-Slash und einem hohen explosiven Einschlag.']]},
 furia:{name:'Furia',kind:'hurt',variants:[['Züngelnde Feuerpeitsche','Phase 1: Duc brennt als anhaltender Zustand für 3 Runden. Phase 2: Eine bewegliche Feuerpeitsche schnellt vom Körper zum Gegner und schlägt mit einem feurigen Impact ein. Ein Treffer je Angriff.'],['Überkopf-Geißel','Eine breite Feuerpeitsche holt hoch über dem Kampf aus und schnellt dann ins Ziel. Der Brennzustand bleibt an Duc.'],['Schlangenflamme','Eine geschwungene Feuerpeitsche zieht in einer S-Bahn zum Gegner. Nach dem Einschlag bleibt die geschwungene Form erhalten und verblasst. Die native Feuerbewegung läuft dabei weiter.']]},
 vulcano:{name:'Vulcano',kind:'hurt',variants:[['Aufsteigender Feuersturm','Eine wachsende Feuerspirale umschließt das Ziel. Der Sturm entlädt sich als große native Explosion mit einzelnen Feuer-Slashes. Genau ein Treffer je gewählter Brandstufe.'],['Gegenläufige Flammenfronten','Zwei breite gegenläufige Feuerbahnen verdichten sich um den Gegner. Eine seitlich auseinanderbrechende Explosion trägt die kreuzenden Feuer-Slashes.'],['Glühende Sturmkrone','Über dem Gegner baut sich eine doppelte rotierende Sturmkrone auf. Sie entlädt sich als hoher Explosionsstoß mit steilen Feuer-Slashes.']]},
 mistral:{name:'Mistral',kind:'hurt',variants:[['Wilder Schwung','Drei unterbrochene Windbahnen kreisen beim Ausholen, beschleunigen und entladen sich als harter Schlag. Hurt und Rückstoß gehen in kurzes erschüttertes Rütteln über.'],['Schweres Ausholen','Breitere kreisende Luftbahnen sammeln Schwung für einen kräftigeren Einzelhieb.'],['Gegenschwung','Eine gegenläufige Windbahn führt in zwei versetzte Drucktreffer.']]},
 wave:{name:'Ressac',kind:'hurt',variants:[['Wasserlanze · Referenz','Die abgestimmte Wasserkugel mit Gischt, kurzem Flug und länger sichtbarer Trefferpose.'],['Wasserhammer','Ein schwerer, flacherer Wasserkörper schießt in einem niedrigen Bogen zum Ziel.'],['Zwillingsstoß','Zwei kleinere Wasserkugeln treffen mit kurzem Abstand aus verschiedenen Höhen.']]},
 wind:{name:'Libeccio',kind:'guard',variants:[['Grobe Nebelwand','Breite, unregelmäßige Nebelschwaden bauen sich links VOR Duc zu einer bewegten Wand auf. Die Figur bleibt teilweise sichtbar; bodennaher Dunst läuft weich aus. Der Gegner bleibt unberührt.'],['Umlaufender Tornado','Ein kleiner Wirbel zieht vor und hinter der Figur entlang.'],['Sich öffnende Wirbel','Zwei schmale Trichter entstehen nah am Körper und wandern auseinander.']]},
 tidal:{name:'Lame de Fond',kind:'hurt',variants:[['Brechende Wasserwand','Bodennahe Strömungen sammeln sich zu einer hohen Wasserwand. Die überhängende Krone kippt über den Gegner und zerfällt in bewegliche Gischt; kräftiger Rückstoß und lange Hurt-Reaktion.'],['Steigender Brecher','Eine bodennahe Wassermasse steigt im Flug an und trifft von unten.'],['Doppelte Kaskade','Ein erster Druckstoß wird von einem kleineren, höher liegenden Schub eingeholt.']]},
 doubleSlash:{name:'Doppio Gioco',kind:'hurt',variants:[['Kreuzschnitt','Violette Energie sammelt sich waffenunabhängig an Oberkörper und Schultern. Der erste Wischer entlädt einen Teil, die Restladung verdichtet sich zur kräftigeren Rückhand. Zwei lange violette Klingenspuren kreuzen sich als gerichtete Wischer. Jeder Treffer löst Hurt und einen eigenen Rückstoß aus; der zweite setzt kräftiger nach.'],['Finte und Rückhand','Die violette Körperladung entlädt einen kurzen ersten Wischer; die verbleibende Energie lädt für die tiefere, kräftige Rückhand nach.'],['Auf und ab','Violette Körperladung bleibt durch Vorbereitung und Rückholbewegung sichtbar. Eine steigende Klinge geht in einen steilen Abwärtsschnitt über.']]},
 blur:{name:'Sotto Voce',kind:'evade',variants:[['Verdichtete Stimme','Eine perlmuttgraue Schallkugel lädt sich links pulsierend auf und entlädt sich zum Ziel. Feine Druckwellen laufen aus; die Figur vibriert mit versetzten Nachbildern. Visuelle Studie, unveränderte Abtauchen-Regel.'],['Doppeltes Echo','Die erste Schallentladung wird von einem kleineren Echo eingeholt. Zwei Resonanzimpulse lassen die Silhouette nachschwingen.'],['Tiefe Resonanz','Eine breitere, langsam pulsierende Kugel bündelt die Stimme und öffnet sich am Ziel zu einer schweren, weich auslaufenden Druckwelle.']]},
 vendetta:{name:'Vendetta',kind:'hurt',variants:[['Rotes Sieges-V','Die kräftige rote Körperladung entlädt sich in zwei gerichteten Schnitten. Erst links oben zur unteren Spitze, dann rechts oben zur selben Spitze: ein deutliches V mit zwei sichtbaren Trefferreaktionen.'],['Breites Rache-V','Zwei weiter geöffnete rote Schnitte bilden nach der Funkenladung ein breites V. Der zweite Hieb setzt mit kräftigerem Rückstoß nach.'],['Steiles Glut-V','Zwei steilere karminrote Schnitte treffen sich unten zu einem schmaleren V. Die Klingenspuren bleiben kurz gemeinsam sichtbar, während der Gegner zurückweicht.']]},
 blackSlash:{name:'Omertà',kind:'hurt',variants:[['Pakt der Stille','Duc lädt eine Goldaura und verschwindet. Zwei Schnitte schlagen von oben links und oben rechts ein. Nach dem zweiten entlädt sich die Ladung als echte goldene Smoke Shockwave mit Funken und glitzerndem Goldstaub. Duc kehrt im Rauch zurück.'],['Goldener Hinterhalt','Goldaura, Verschwinden, zwei breitere Schnitte von oben und eine flache, weit auseinanderbrechende Rauch-Druckwelle. Funken und Goldstaub bleiben kurz im Raum.'],['Goldenes Urteil','Duc verschwindet in der Goldaura. Zwei steile Schnitte schlagen ein, danach entfaltet sich eine hohe goldene Rauch-Druckwelle. Im auslaufenden Glitzer kehrt Duc zurück.']]},
 reticle:{name:'Point de Mire',kind:'guard',variants:[['Präziser Fokus','Ein kühler, mintweißer Reflex tastet die Figur von oben nach unten ab und bündelt sich an einer Schwachstelle. Eine dezente, bewegte Markierung bleibt am Körper. Kein Schaden und keine Hurt-Pose.'],['Seitliche Erfassung','Ein schräger Lichtreflex wandert seitlich über die Silhouette und rastet am Oberkörper ein. Die Markierung pulsiert ruhig weiter.'],['Doppelte Analyse','Zwei Reflexe nähern sich von oben und unten, legen die Schwachstelle frei und verdichten sich zu einem lokalen Lichtakzent.']]},
 calm:{name:'Bonaccia',kind:'guard',variants:[['Wasserschutzschild','Eine echte LiquiGen-Wasserfläche wächst links vor Duc zum gewölbten Schild. Kleine Tropfen sammeln sich nach innen; bewegte Wasserfalten bleiben sichtbar. Kein Splash, keine Gegnerreaktion.'],['Vorgezogener Wasserbogen','Die simulierte Wasserfläche bildet einen schmaleren, nach vorn geneigten Schild rechts vor Duc. Tropfen ziehen in die Schutzfläche ein.'],['Strömende Wasserlinse','Breitere Wasserlinse mit bewegter LiquiGen-Oberfläche und leicht wechselnder Neigung. Tropfen sammeln sich zum Schutzschild.']]},
 beam:{name:'Phare',kind:'guard',variants:[['Suchscheinwerfer','Elfenbein und Gold: Ein wandernder Lichtkegel findet das Ziel, bündelt sich und hält es im Leuchtfeuer. Bewegter Dunst und goldener Staub machen das Licht räumlich sichtbar. Kein direkter Schaden.'],['Lichtbruch','Getrennte goldene Lichtspalten öffnen sich seitlich und verschmelzen zu einem kräftigen Leuchtfeuer am Ziel.'],['Gegenlicht','Ein aufgefächerter Lichtschein erhebt sich hinter der Silhouette; warme Reflexe und schwebender Staub bleiben kurz zurück.']]},
 rain:{name:'Pluie d’Étoiles',kind:'hurt',variants:[['Dreifacher Fall','Saphirblau und Silber: Drei geladene Lichtpunkte schlagen nacheinander ein. Der dritte Treffer detoniert als große silberblaue Explosion. Danach bleibt feiner, glitzernder Eisstaub zurück; jeder Kontakt löst Hurt und Rückstoß aus.'],['Schräger Sternenschauer','Drei kurze, heiße Geschosse treffen aus wechselnden Winkeln mit versetzter Hurt-Reaktion und auseinanderstiebenden Silberpartikeln.'],['Konvergenz','Drei Bahnen bündeln sich nahezu gleichzeitig am Ziel. Ein kompakter blauer Einschlag zerfällt in drei überlagerte Ausbrüche. Weiterhin drei einzelne Treffer.']]}
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
function vendettaArm(A,when,angle,length,height,x,y,reverse=false){
 const age=A.age-when,p=C((age+.15)/.27),alpha=1-S((A.age-hits(A.id,A.variant)[1]-.12-.8)/.6);if(!p||alpha<.002)return;
 const q=bladeLayer.getContext('2d'),i=A.images.stahlrot,b=A.crops.stahlrot,left=256-length/2,head=left+length*p;
 q.clearRect(0,0,512,128);q.globalCompositeOperation='source-over';q.drawImage(i,b[0],b[1],b[2]-b[0],b[3]-b[1],left,64-height/2,length,height);
 q.globalCompositeOperation='destination-in';const mask=q.createLinearGradient(left-1,0,head+1,0);mask.addColorStop(0,'#fff0');mask.addColorStop(.06,'#ffff');mask.addColorStop(.94,'#ffff');mask.addColorStop(1,'#fff0');q.fillStyle=mask;q.fillRect(left-1,0,head-left+2,128);q.clearRect(head+1,0,512,128);q.globalCompositeOperation='source-over';
 const g=A.g;g.save();g.translate(x,y);g.rotate(angle);if(reverse)g.scale(-1,1);g.globalAlpha=.94*alpha;g.drawImage(bladeLayer,-256,-64);g.restore();
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

function draw(A,behind){
 const {g,id,variant:v,age,clock,t}=A,build=S((t-.3)/.72),fade=life(age,1.65),pre=t<1.12?build:0;
 if(['scirocco','retour','furia','vulcano'].includes(id)){window.EdenBerserker.draw(A,behind);return;}
 if(id==='tidal'&&v===0){window.EdenTidalWall.draw(A,behind);return;}
 if(id==='blackSlash'){window.EdenOmerta.draw(A,behind);return;}
 if(id==='wave'||id==='tidal'){if(!behind)waterAttack(A);return;}
 if(id==='mistral'){window.EdenMistralSwing.draw(A,behind);return;}
 if(id==='wind'&&v===0){window.EdenLibeccioFog.draw(A,behind);return;}
 if(id==='wind'){
  const env=t<1.5?build*.8:fade;
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
   const times=hits(id,v),angle=[.85,.67,1.05][v],length=[305,330,300][v];
   vendettaArm(A,times[0],angle,length,29,666-Math.cos(angle)*length/2,380-Math.sin(angle)*length/2);
   vendettaArm(A,times[1],-angle,length,32,666+Math.cos(angle)*length/2,380-Math.sin(angle)*length/2,true);
   contact(A,times[0],true,.9);contact(A,times[1],true,1.3);
  }
return;
 }
 if(id==='blur'){window.EdenSottoVoce.draw(A,behind);return;}
 if(id==='reticle'){window.EdenPointDeMire.draw(A,behind);return;}
 if(id==='calm'){window.EdenBonacciaShield.draw(A,behind);return;}
 if(id==='beam'||id==='rain'){window.EdenLightStars.draw(A,behind);return;}
}
function hits(id,v){
 if(id==='vulcano')return window.EdenBerserker.hits();
 if(id==='blackSlash')return window.EdenOmerta.hits();
 if(id==='doubleSlash')return v===1?[-.27,.06]:[-.23,.06];
 if(id==='vendetta')return v===1?[-.24,.12]:v===2?[-.12,.14]:[-.16,.1];
 if(id==='mistral'&&v===2)return [0,.22];
 if((id==='wave'||id==='tidal')&&v===2)return [0,.18];
 if(id==='rain')return window.EdenLightStars.hits(v);
 return [0];
}
const launches={scirocco:3.1,retour:3.6,furia:2.0,vulcano:3.8,mistral:2.25,wave:3.12,wind:2.6,tidal:3.12,doubleSlash:2.85,blur:2.65,vendetta:3.25,blackSlash:3.4,reticle:2.4,calm:2.9,beam:3,rain:2.65};
window.EdenAttackLibrary={defs,draw,hits,launches};
})();
