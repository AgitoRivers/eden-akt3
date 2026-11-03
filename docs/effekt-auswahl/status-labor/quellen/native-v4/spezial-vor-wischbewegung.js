/* 36 effect variants. Water uses the actual LiquiGen export; generated steel/light are static materials.
 * Kenney CC0 glints and tracks; original IlluGen smoke atlas is retained.
 * No game API, no character data, no sound and no live saves. */
(() => {
  'use strict';
  const clamp=x=>Math.max(0,Math.min(1,x)),PI=Math.PI;
  const smooth=x=>{x=clamp(x);return x*x*(3-2*x)};
  const hit=(t,c,w=.08)=>Math.exp(-Math.pow((t-c)/w,2));
  const envelope=(t,a,b)=>smooth((t-a)/.3)*(1-smooth((t-b)/.7));
  const defs={
    mistral:[['Seitenstoß','Ein trockener Luftstoß zieht seitlich durch die Szene und wirbelt Bodennebel auf.'],['Fallböe','Eine schräge Böe drückt von oben in die Szene und zieht am Boden weiter.'],['Doppelböe','Zwei versetzte Luftstöße kommen aus entgegengesetzten Richtungen.']],
    wave:[['Brandung','Ein niedriger Wasserschwall läuft seitlich gegen die Figur und verliert an Kraft.'],['Auflauf','Das Wasser drückt von unten hoch und sinkt weich zurück.'],['Gegenströmung','Zwei unterschiedlich starke Wasserschübe treffen zeitversetzt aufeinander.']],
    wind:[['Aufwind','Weicher Dunst hebt sich hinter und seitlich der Figur.'],['Umlauf','Zwei zusammenhängende Luftfahnen ziehen vor und hinter der Figur vorbei.'],['Windwechsel','Ein trockener Stoß wird von einer sanften Gegenströmung abgelöst.']],
    tidal:[['Flutstoß','Eine schwere, detaillierte Wassermasse schiebt sich quer durch den unteren Bildraum.'],['Flutaufbau','Wasser steigt hinter der Figur an und bricht vor ihr herunter.'],['Doppelte Brandung','Eine erste breite Flut wird von einem schnelleren zweiten Brecher eingeholt.']],
    doubleSlash:[['Feiner Kreuzschnitt','Zwei kurze, schmale Stahlwischer kreuzen sich mit klar getrennten Treffern.'],['Finte und Rückhand','Ein knapper erster Wischer wird von einer flachen Rückhand beantwortet.'],['Auf- und Abwärtsschnitt','Eine aufsteigende Klingenspur geht in einen präzisen Abwärtsschnitt über.']],
    blur:[['Seitlicher Wechsel','Ein schwaches Nachbild löst sich seitlich; die Silhouette tritt zurück in den Fokus.'],['Schleiertritt','Dünner Dunst zieht durch die Figur, die kurz im Hintergrund verschwindet.'],['Versetztes Echo','Zwei sehr dezente Nachbilder lösen sich nacheinander in entgegengesetzte Richtungen.']],
    vendetta:[['Gezielter Schnitt','Ein einzelner feiner Abwärtsschnitt mit einem kurzen warmen Trefferimpuls.'],['Verzögerte Antwort','Ein kurzer Ansatz geht in eine tiefere, waagerechte Rückhand über.'],['Steiler Schnitt','Ein rascher, nahezu senkrechter Stahlwischer mit knappem Staubnachlauf.']],
    blackSlash:[['Kurze Dunkelheit','Das Licht fällt kurz ab; eine schmale silbrige Spur wird sichtbar.'],['Verdeckte Rückhand','Ein dünner Schatten zieht durch das Bild, gefolgt von einer flachen Klingenspur.'],['Stiller Schnitt','Die Szene bleibt lesbar, nur der Treffermoment dunkelt kurz ab.']],
    reticle:[['Präziser Schuss','Ein feiner seitlicher Schusswischer und ein kleiner, kurzer Trefferreflex.'],['Schräger Treffer','Der Schuss kommt von schräg oben und hinterlässt einen knappen Druckschweif.'],['Durchschuss','Eine schmale Spur läuft durch das Ziel und klingt dahinter aus.']],
    calm:[['Ruhiges Wasser','Eine flache Strömung beruhigt sich; ein kühler Schleier bleibt kurz zurück.'],['Windstille','Zwei seitliche Nebelfahnen lösen sich auf und geben die Figur frei.'],['Tiefe Ruhe','Das Bild entsättigt sich sanft; Bodendunst hebt und senkt sich langsam.']],
    beam:[['Suchlicht','Ein weicher fotografischer Lichtstrahl schwenkt über die Figur.'],['Lichtspalt','Ein schmales, strukturiertes Tageslicht fällt nahezu senkrecht in die Szene.'],['Gegenlicht','Zwei schwächere Lichtquellen wechseln sich als sanftes Gegenlicht ab.']],
    rain:[['Drei Einschläge','Drei schlanke Lichtspuren treffen nacheinander ein und lösen kleine Druckfahnen aus.'],['Versetzter Lichtfall','Drei schräg einfallende Lichtbahnen treffen mit unterschiedlicher Länge und Verzögerung.'],['Gemeinsamer Treffer','Drei feine Bahnen bündeln sich zu einem kurzen, weich auslaufenden Lichtimpuls.']]
  };
  let images,crops;
  const canvas=()=>{const c=document.createElement('canvas');c.width=600;c.height=560;return c};
  const smokeCache=new Map(),haloCache=new Map();
  const fluidLayer=document.createElement("canvas");fluidLayer.width=640;fluidLayer.height=320;
  const lightLayer=canvas();
  const makeGradient=(g,colors,y0=0,y1=560)=>{const p=g.createLinearGradient(0,y0,0,y1);colors.forEach((c,i)=>p.addColorStop(i/(colors.length-1),c));return p};
  function figure(g,x=0,y=0,alpha=1,filter='none'){
    const i=images.figure,w=475*i.width/i.height;g.save();g.globalAlpha=clamp(alpha);g.filter=filter;g.drawImage(i,300-w/2+x,32+y,w,475);g.restore();
  }
  function halo(g,color,a){
    if(!haloCache.has(color)){const c=canvas(),x=c.getContext('2d');figure(x);x.globalCompositeOperation='source-in';x.fillStyle=color;x.fillRect(0,0,600,560);const h=canvas(),z=h.getContext('2d');z.filter='blur(10px)';z.drawImage(c,0,0);z.filter='none';z.globalCompositeOperation='destination-out';figure(z);haloCache.set(color,h)}
    g.save();g.globalAlpha=clamp(a);g.drawImage(haloCache.get(color),0,0);g.restore();
  }
  function photo(g,name,x,y,w,h,a=1,angle=0,flip=false){
    if(a<.003||w<=0||h<=0)return;
    const i=images[name],b=crops[name]||[0,0,i.width,i.height];
    g.save();g.globalAlpha=clamp(a);g.translate(x+w/2,y+h/2);g.rotate(angle);if(flip)g.scale(-1,1);
    g.drawImage(i,b[0],b[1],b[2]-b[0],b[3]-b[1],-w/2,-h/2,w,h);g.restore();
  }
  function smoke(g,t,x,y,w,h,a=.5,tint=null,angle=0){
    if(a<.003)return;
    const f=Math.floor(Math.max(t,0)*30)%64,key=f+String(tint);
    if(!smokeCache.has(key)){const c=document.createElement('canvas');c.width=c.height=256;const q=c.getContext('2d');q.drawImage(images.staub,f%8*256,Math.floor(f/8)*256,256,256,0,0,256,256);if(tint){q.globalCompositeOperation='source-atop';q.fillStyle=tint;q.fillRect(0,0,256,256)}if(smokeCache.size>96)smokeCache.delete(smokeCache.keys().next().value);smokeCache.set(key,c)}
    g.save();g.globalAlpha=clamp(a);g.translate(x+w/2,y+h/2);g.rotate(angle);g.drawImage(smokeCache.get(key),-w/2,-h/2,w,h);g.restore();
  }
  function steel(g,t,when,angle,x=300,y=270,length=255,thickness=8){
    length*=1.32; thickness*=1.40;
    const p=hit(t,when,.115),d=(t-when)*110;
    photo(g,'stahl',x-length/2+d,y-thickness/2,length,thickness,p*.88,angle);
  }
  function glint(g,t,when,x,y,scale=1){const a=hit(t,when,.09);photo(g,'glint',x-22*scale,y-17*scale,44*scale,34*scale,a*.3);}
  // Actual LiquiGen image sequence: 32 isolated water frames, 8 columns, 4 rows.
  // Source camera detail is limited. Frame interpolation avoids hard 16 fps steps.
  function water(g,t,x,y,w,h,a=1,flip=false){
    if(a<.003)return;
    const i=images.liquigenWater,phase=clamp((t-.5)/2)*31;
    const f=Math.floor(phase),next=Math.min(31,f+1),blend=phase-f;
    const q=fluidLayer.getContext('2d');q.clearRect(0,0,640,320);
    q.globalAlpha=1;q.globalCompositeOperation='source-over';
    q.drawImage(i,f%8*128,Math.floor(f/8)*96,128,96,0,0,640,320);
    // Add premultiplied frames, including alpha, for a true cross-fade.
    if(blend>0){
      q.globalCompositeOperation='destination-in';q.fillStyle=`rgba(255,255,255,${1-blend})`;q.fillRect(0,0,640,320);
      q.globalCompositeOperation='lighter';q.globalAlpha=blend;
      q.drawImage(i,next%8*128,Math.floor(next/8)*96,128,96,0,0,640,320);
    }
    q.globalCompositeOperation='source-over';q.globalAlpha=1;
    g.save();g.globalAlpha=clamp(a);g.translate(x+(flip?w:0),y);if(flip)g.scale(-1,1);
    g.drawImage(fluidLayer,0,0,w,h);g.restore();
    smoke(g,t*.85,x-w*.03,y+h*.2,w*.68,h*.6,a*.18,'#b7d6e76b',-.08);
    smoke(g,t*.85+.9,x+w*.3,y+h*.38,w*.74,h*.48,a*.22,'#b2d8e678',.07);
  }
  function burst(g,t,when,x,y,w,h,a=.5,angle=0){
    const age=(t-when)/1.55;if(age<0||age>=1)return;
    const f=Math.min(15,Math.floor(age*16)),i=images.druckstoss;
    g.save();g.globalAlpha=clamp(a*smooth(age*12)*(1-smooth((age-.62)/.38)));
    g.translate(x+w/2,y+h/2);g.rotate(angle);g.drawImage(i,f%4*512,Math.floor(f/4)*512,512,512,-w/2,-h/2,w,h);g.restore();
  }
  function light(g,t,x,y,w,h,a=1,angle=0){
    // Two independent layers: photographic shaft and moving volumetric density.
    photo(g,'licht',x,y,w,h,a*.72,angle);
    g.save();g.globalCompositeOperation='screen';
    smoke(g,t*.65,x-w*.5,y+h*.36,w*1.7,h*.6,a*.26,'#d6d3bb50',angle);
    g.restore();
  }
  function stage(g,lightBackground){g.fillStyle=makeGradient(g,lightBackground?['#a3adae','#bbc1b8','#697878']:['#101924','#27343d','#111b25']);g.fillRect(0,0,600,560);g.fillStyle=makeGradient(g,['#0d182000','#0b111d70'],425,560);g.fillRect(0,425,600,135);g.save();g.filter='blur(11px)';g.fillStyle='#0006';g.beginPath();g.ellipse(300,505,96,10,0,0,PI*2);g.fill();g.restore()}
  function render(c,id,time,v,settings={}){
    const g=c.getContext('2d'),t=time%5.4,env=envelope(t,.5,2.6),p=smooth((t-.7)/1.4),impact=hit(t,1.55,.15),shown=settings.figure!==false;
    const cool=['mistral','wave','wind','tidal','calm'].includes(id),color=cool?'#b3cdd3':'#d5d0c4';
    g.save();g.clearRect(0,0,600,560);stage(g,settings.light);
    // Small recoil at contact; avoid exaggerated camera movement and bloom.
    g.translate(Math.sin(t*67)*impact*1.8,Math.cos(t*59)*impact*.7);
    if(id==='tidal'&&v===1)water(g,t,45,420-p*175,510,180+p*70,env*.8);
    if(id==='wind')smoke(g,t,140,320-p*180,330,250,env*.22,null,v===1?.4:0);
    if(shown){halo(g,color,env*.32);figure(g,id==='blur'?Math.sin(t*2)*env*12:impact*2,0,id==='blur'?1-env*.48:1,id==='calm'?'saturate(.3)':'none')}
    switch(id){
      case 'mistral':{
        burst(g,t,[.7,.85,.65][v],v===1?210:70,v===1?180:305,v===1?250:420,v===1?290:160,.45,v===1?.55:0);
        if(v===0){smoke(g,t,-240+p*540,300,480,170,env*.65);smoke(g,t+.6,-90+p*220,415,400,95,env*.42,'#c8baa740');}
        if(v===1){smoke(g,t,80+p*190,80+p*280,250,310,env*.65,null,-.6);smoke(g,t+.5,140,414,400,100,impact*.5,'#bfb3a650');}
        if(v===2){smoke(g,t,-130+p*390,285,350,160,envelope(t,.55,1.45)*.6);smoke(g,t+.7,450-p*270,350,310,130,envelope(t,1.3,2.8)*.5);}
        break;}
      case 'wave':{
        if(v===0)water(g,t,-90+p*280,385,430,145,env*.9);
        if(v===1)water(g,t,150,485-Math.sin(p*PI)*170,330,105+Math.sin(p*PI)*95,env*.85);
        if(v===2){water(g,t,-100+p*280,402,360,125,envelope(t,.6,1.6)*.8);water(g,t+.7,410-p*230,370,380,160,envelope(t,1.3,2.8)*.88,true);}
        break;}
      case 'wind':{
        burst(g,t,.78,150,250,300,225,.16,[0,-.3,.3][v]);
        if(v===0){smoke(g,t,120,380-p*230,190,260,env*.38,null,-.2);smoke(g,t+.5,300,320-p*210,190,270,env*.3,null,.2);}
        if(v===1){smoke(g,t,40+p*180,170,320,230,env*.35,null,-.3);smoke(g,t+.9,320-p*100,300,300,170,env*.4,null,.25);}
        if(v===2){smoke(g,t,-80+p*300,320,380,170,envelope(t,.6,1.6)*.48);smoke(g,t+.5,420-p*240,260-p*80,300,230,envelope(t,1.35,2.8)*.36);}
        break;}
      case 'tidal':{
        if(v===0){water(g,t,-220+p*380,290,690,270,env*.95);smoke(g,t,10,355,550,160,env*.19);}
        if(v===1)water(g,t+.3,55,185+p*160,560,260-p*50,envelope(t,1,2.8)*.95,true);
        if(v===2){water(g,t,-170+p*330,340,600,210,envelope(t,.55,1.6)*.86);water(g,t+.8,-320+p*420,270,730,280,envelope(t,1.1,2.9)*.94);}
        break;}
      case 'doubleSlash':{
        if(v===0){steel(g,t,1.27,.5,300,250,270,8);steel(g,t,1.55,-.48,300,290,270,8);}
        if(v===1){steel(g,t,1.22,-.16,310,235,165,6);steel(g,t,1.55,.12,290,292,280,7);}
        if(v===2){steel(g,t,1.27,-.68,300,287,235,8);steel(g,t,1.55,1.04,310,253,210,7);smoke(g,t,240,260,130,80,hit(t,1.7,.3)*.15);}
        burst(g,t,1.52,235,245,180,135,.32);
        glint(g,t,1.55,303,278,.6);break;}
      case 'blur':{
        if(v===0&&shown){figure(g,-35*env,0,env*.18,'blur(3px)');smoke(g,t,140,190,270,290,env*.16,'#10213280');}
        if(v===1){smoke(g,t,185,120+p*180,250,360,env*.28,'#20314390');if(shown)figure(g,18*(1-p),0,smooth((t-1.8)/.7)*.3);}
        if(v===2&&shown){figure(g,-27*env,-3,envelope(t,.6,1.5)*.19,'blur(2px)');figure(g,34*env,2,envelope(t,1.2,2.5)*.16,'blur(3px)');}
        break;}
      case 'vendetta':{
        if(v===0)steel(g,t,1.55,.84,300,278,265,8);
        if(v===1){steel(g,t,1.22,-.3,300,245,160,5);steel(g,t,1.55,.08,310,315,240,7);}
        if(v===2){steel(g,t,1.55,1.27,300,265,230,7);smoke(g,t,230,305,180,110,hit(t,1.8,.3)*.18,'#84756830');}
        burst(g,t,1.52,235,250,180,130,.34);
        glint(g,t,1.55,303,279,.65);break;}
      case 'blackSlash':{
        g.fillStyle=`rgba(0,3,8,${hit(t,1.45,v===0?.32:v===1?.48:.15)*(v===2?.24:.65)})`;g.fillRect(0,0,600,560);
        steel(g,t,1.55,[.12,-.36,.95][v],300,270,[240,290,195][v],[6,6,5][v]);
        if(v===1)smoke(g,t,125,200,350,200,hit(t,1.4,.4)*.19,'#12202e90');
        break;}
      case 'reticle':{
        const angle=[-.1,.55,-.22][v],w=[185,150,310][v];
        photo(g,'trace',300-w/2,264,w,5,hit(t,1.52,.055)*.7,angle);
        glint(g,t,1.55,300,270,.8);
        burst(g,t,1.52,255,245,170,110,.42,angle);
        smoke(g,t,v===2?305:250,v===1?260:240,v===2?210:130,90,hit(t,1.72,.28)*.3);
        break;}
      case 'calm':{
        if(v===0)water(g,t,50,450,500,65,env*.34);
        if(v===1){smoke(g,t,-60-p*130,290,270,230,env*.27);smoke(g,t+.6,390+p*80,310,280,200,env*.25);}
        if(v===2){smoke(g,t,95,415-Math.sin(p*PI)*45,440,115,env*.28);g.fillStyle=`rgba(138,170,178,${env*.045})`;g.fillRect(0,0,600,560);}
        break;}
      case 'beam':{
        if(v===0)light(g,t,70+p*220,-100,220,670,env*.48,-.25+p*.35);
        if(v===1)light(g,t,235,-60,150,630,env*.48,.035);
        if(v===2){light(g,t,70,-90,200,660,envelope(t,.6,1.6)*.33,.24);light(g,t,325,-90,200,660,envelope(t,1.25,2.8)*.37,-.24);}
        break;}
      case 'rain':{
        const xs=v===2?[200,300,400]:v===1?[190,370,270]:[180,300,420];
        for(let j=0;j<3;j++){
          const when=v===2?1.55:1.05+j*.5,a=hit(t,when,v===2?.13:.18),x=xs[j];
          light(g,t+j,x-38,-50,76,550,a*.52,v===1?.26:v===2?(j-1)*.18:-.1);
          burst(g,t,when,x-125,375,250,160,.5);
          smoke(g,t+j,x-105,395,210,115,hit(t,when+.17,.29)*.28);
          photo(g,'glint',x-17,465,34,25,a*.12);
        }break;}
    }
    g.restore();
  }
  window.EdenSpecialFx={defs,render,duration:5.4,init(value){images=value;crops=Object.fromEntries(window.EDEN_REALISM_SOURCES.generated.map(r=>[r.name,r.crop]));}};
})();
