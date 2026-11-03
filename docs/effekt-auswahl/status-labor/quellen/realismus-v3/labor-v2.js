/* Separate visual lab. No game requests; feedback uses its own localStorage key. */
(() => {
  'use strict';
  const $=s=>document.querySelector(s), specials=new URLSearchParams(location.search).get('kategorie')==='spezialangriffe', reactions=new URLSearchParams(location.search).get('kategorie')==='reaktionen', key=specials?'eden-rise-spezial-labor-v2':reactions?'eden-rise-reaktionen-labor-v1':'eden-rise-status-labor-v1';
  const info={fire:['Brennend','Höher ansetzende, farbige Flammen. Eine weiche warme Kontur bleibt während des Zustands sichtbar.'],water:['Nass','Kräftigere Nässe mit dunklerem Stoff und deutlicheren Reflexen. Eine weiche blaue Kontur bleibt sichtbar.'],quake:['Erschüttert','Höherer, frei driftender Nebel mit weich auslaufenden Rändern. Eine dezente sandfarbene Kontur bleibt sichtbar.'],electric:['Unter Strom','Die bewerteten Entladungen bleiben erhalten. Eine weiche goldene Kontur ist auch zwischen den Impulsen sichtbar.']};
  const reactionInfo={shortCircuit:['Kurzschluss','Nässe und Strom: unregelmäßige, kräftige Entladungen mit einer kurzen Dampffahne.'],mud:['Schlamm','Nässe und Erschütterung: ein zusammenhängender brauner Schwall mit unregelmäßigen, wandernden Ausläufern.'],firestorm:['Feuersturm','Feuer und Strom: gegeneinander ziehende Flammen mit kurzen elektrischen Entladungen.'],steam:['Dampf','Feuer und Nässe: die Flamme erlischt, dichter Dampf steigt auf und verliert sich weich.'],flare:['Ausbrennen','Feuer und Blutung: eine kurze hohe Stichflamme, danach nur noch ein leichter Rauchschleier.']};
  const specialInfo={mistral:['Mistral','Ein seitlicher Windstoß zieht als zusammenhängende Fahne durch die Figur.'],wave:['Ressac','Ein breiter kühler Schwall steigt von unten auf. Materialstudie, noch keine Flüssigkeitssimulation.'],wind:['Libeccio','Ein weicher Windschleier um die Figur; die Kontur begleitet den sichtbaren Zustand.'],tidal:['Lame de Fond','Eine große zusammenhängende Welle füllt den unteren Bildraum und läuft weich aus.'],doubleSlash:['Doppio Gioco','Zwei zeitlich versetzte, breite und texturierte Schnittbewegungen.'],blur:['Sotto Voce','Eine weiche versetzte Silhouette lässt die Figur kurz verschwimmen.'],vendetta:['Vendetta','Eine breite Schnittbewegung mit kurzem rotem Trefferlicht.'],blackSlash:['Omertà','Die Szene dunkelt ab, dann ist eine einzige texturierte Schnittbewegung sichtbar.'],reticle:['Point de Mire','Ruhiges Zielllicht am Oberkörper, anschließend eine matte Kontur.'],calm:['Bonaccia','Ein ruhiger kühler Schleier legt sich über den unteren Bildraum.'],beam:['Phare','Ein weicher warmer Lichtkegel fällt auf die Figur.'],rain:['Pluie d’Étoiles','Drei breite Lichtbahnen mit einem kurzen Nebelimpuls am Boden.']};
  if(reactions){Object.assign(info,reactionInfo);$('#page-title').textContent='Reaktionen im Vergleich';$('#page-intro').textContent='Fünf Kombinationen aus den bewährten Zuständen. Kurzer Auftakt, weiches Auslaufen und eine Kontur während der Reaktion.';$('#effects-nav').replaceChildren(...Object.entries(reactionInfo).map(([id,value])=>{const button=document.createElement('button');button.dataset.state=id;button.textContent=value[0];button.setAttribute('aria-pressed','false');return button}));document.title='Eden Rise · Reaktionen';}
  if(specials){Object.assign(info,specialInfo);$('#page-title').textContent='Spezialangriffe im Vergleich';$('#page-intro').textContent='Zwölf Angriffe als erste Gestaltungsvorschläge mit den freigegebenen Bausteinen.';$('#effects-nav').replaceChildren(...Object.entries(specialInfo).map(([id,value])=>{const b=document.createElement('button');b.dataset.state=id;b.textContent=value[0];return b}));document.title='Eden Rise · Spezialangriffe';}
  document.querySelectorAll('.categories a').forEach(a=>{if((specials?a.href.includes('kategorie=spezialangriffe'):reactions?a.href.includes('kategorie=reaktionen'):!a.href.includes('kategorie=')))a.setAttribute('aria-current','page')});
  let state=specials?'mistral':reactions?'shortCircuit':'fire',paused=matchMedia('(prefers-reduced-motion: reduce)').matches,time=specials?1.55:.7,last=0,feedback={},assetsReady=false;
  try{feedback=JSON.parse(localStorage.getItem(key)||'{}')}catch{}
  const images={},old=$('#old'),fresh=$('#new'),g=fresh.getContext('2d');
  const material=document.createElement('canvas');material.width=600;material.height=560;const m=material.getContext('2d');
  const load=(name,url)=>new Promise((resolve,reject)=>{const i=new Image();i.onload=()=>{images[name]=i;resolve()};i.onerror=()=>reject(new Error('Bild konnte nicht geladen werden: '+url));i.src=url});

  if(specials){
    document.body.classList.add('specials');
    $('#page-intro').textContent='Zwölf Angriffe, jeweils zwei eigene Inszenierungen. Beide Varianten laufen synchron; mit der Zeitleiste kannst du jeden Moment prüfen.';
    document.querySelector('.compare').setAttribute('aria-label','Zwei Varianten im direkten Vergleich');
    document.querySelectorAll('.caption h2')[0].textContent='Variante 1';
    document.querySelectorAll('.caption h2')[1].textContent='Variante 2';
    old.setAttribute('aria-label','Spezialangriff Variante 1');fresh.setAttribute('aria-label','Spezialangriff Variante 2');
    const votes=document.querySelectorAll('[data-vote]');
    votes[0].dataset.vote='variant1';votes[0].textContent='Variante 1 wählen';
    votes[1].dataset.vote='variant2';votes[1].textContent='Variante 2 wählen';
    votes[2].dataset.vote='revise';votes[2].textContent='Beide überarbeiten';
    const controls=document.querySelector('.controls'),replay=document.createElement('button');
    replay.id='replay';replay.textContent='Von vorn';replay.onclick=()=>{time=0;if(assetsReady)render(time)};controls.append(replay);
    const label=document.createElement('label');label.className='timeline';label.textContent='Ablauf ';
    const slider=document.createElement('input');slider.type='range';slider.id='timeline';slider.min='0';slider.max='5.35';slider.step='.01';slider.value='1.55';slider.setAttribute('aria-label','Zeitpunkt des Spezialangriffs');
    slider.oninput=()=>{time=Number(slider.value);paused=true;$('#pause').textContent='Abspielen';if(assetsReady)render(time)};label.append(slider);
    const value=document.createElement('output');value.id='time-value';value.textContent='1.55 s';label.append(value);controls.append(label);
  }

  const clamp=x=>Math.max(0,Math.min(1,x));
  function frame(name,t,x,y,w,h,opacity=1,blend='source-over'){
    const i=images[name],n=Math.floor(t*30)%64,cw=i.width/8,ch=i.height/8;
    g.save();g.globalAlpha=opacity;g.globalCompositeOperation=blend;g.drawImage(i,n%8*cw,Math.floor(n/8)*ch,cw,ch,x,y,w,h);g.restore();
  }
  function figure(ctx,dx=0,dy=0){const i=images.figure,h=475,w=h*i.width/i.height;ctx.drawImage(i,(600-w)/2+dx,32+dy,w,h)}
  // Cache the sprite-shaped halo; it stays visible between effect pulses.
  const contours=new Map();
  function contour(dx=0,dy=0,opacity=1){
    if(!contours.has(state)){
      const tint=document.createElement('canvas');tint.width=600;tint.height=560;
      const c=tint.getContext('2d');figure(c);c.globalCompositeOperation='source-in';
      c.fillStyle=({fire:'#ff9a48',water:'#72c7e2',quake:'#cfbaa0',electric:'#e8cf82',shortCircuit:'#9bd6f2',mud:'#b29b72',firestorm:'#ff9a48',steam:'#c7d9df',flare:'#f29a65',mistral:'#bdcfd4',wave:'#72c7e2',wind:'#c8ddd9',tidal:'#72c7e2',doubleSlash:'#e1cfac',blur:'#9eafba',vendetta:'#ca7564',blackSlash:'#ded1af',reticle:'#d7c69e',calm:'#9bbfc8',beam:'#e7d2a2',rain:'#d7dfeb'})[state];c.fillRect(0,0,600,560);
      const halo=document.createElement('canvas');halo.width=600;halo.height=560;
      const h=halo.getContext('2d');h.filter='blur(11px)';h.globalAlpha=.85;h.drawImage(tint,0,0);
      h.filter='blur(4px)';h.globalAlpha=.55;h.drawImage(tint,0,0);
      h.filter='none';h.globalAlpha=1;h.globalCompositeOperation='destination-out';figure(h);
      contours.set(state,halo);
    }
    g.save();g.globalAlpha=opacity;g.drawImage(contours.get(state),dx,dy);g.restore();
  }
  function background(){const light=$('#background').value==='light';g.fillStyle=light?'#a4a7a3':'#171e24';g.fillRect(0,0,600,560);const grad=g.createRadialGradient(300,280,20,300,300,360);grad.addColorStop(0,light?'#c9c7bd':'#2b353d');grad.addColorStop(1,light?'#8e9593':'#10161d');g.fillStyle=grad;g.fillRect(0,0,600,560);g.fillStyle=light?'#666e6c':'#0c1116';g.fillRect(0,505,600,55);g.save();g.filter='blur(12px)';g.fillStyle='#0007';g.beginPath();g.ellipse(300,506,93,12,0,0,Math.PI*2);g.fill();g.restore()}

  function reaction(t,shown){
    const elapsed=t%3.8,env=Math.sin(Math.PI*clamp(elapsed/2.25));
    const advance=clamp(elapsed/2.25),pulse=Math.exp(-Math.pow((elapsed-.48)/.19,2));
    if(state==='shortCircuit'){
      if(shown){m.clearRect(0,0,600,560);figure(m);m.globalCompositeOperation='source-atop';m.fillStyle=`rgba(94,164,190,${env*.17})`;m.fillRect(0,0,600,560);m.globalCompositeOperation='source-over';g.drawImage(material,0,0)}
      const discharge=env*(.22+.78*Math.pow(Math.max(0,Math.sin(elapsed*29)),4));
      frame('strom',t*1.4,150,110,310,365,discharge,'screen');
      frame('staub',t*.7,170-advance*25,300-advance*85,260+advance*55,190,env*.3);
    }
    if(state==='mud'){
      // Both the wet film and rolling mud use the irregular textured edge.
      // No radial gradient or ellipse limits the visible material.
      m.clearRect(0,0,600,560);const im=images.staub,n=Math.floor(t*25)%64,n2=(n+23)%64;
      m.drawImage(im,n2%8*256,Math.floor(n2/8)*256,256,256,95-advance*30,435,400+advance*70,91);
      m.drawImage(im,n%8*256,Math.floor(n/8)*256,256,256,150-advance*37+Math.sin(t)*13,382-advance*18,310+advance*80,145);
      m.globalCompositeOperation='source-atop';m.fillStyle='#795232e8';m.fillRect(0,0,600,560);m.globalCompositeOperation='source-over';g.save();g.globalAlpha=env*.9;g.drawImage(material,0,0);g.restore();
    }
    if(state==='firestorm'){
      frame('feuer',t*1.18,137+Math.sin(t*5)*28,155,280,330,env*.9);
      frame('feuer',t*1.18+.8,228-Math.sin(t*5)*28,241,190,260,env*.78);
      if(Math.sin(t*22)>.65)frame('strom',t,170,160,270,310,env*.65,'screen');
      frame('staub',t*.6,150,200-advance*90,310,240,env*.17);
    }
    if(state==='steam'){
      frame('feuer',t,205,260,190,225,Math.max(0,1-elapsed*2)*.85);
      frame('staub',t*.65,142-advance*35,290-advance*170,315+advance*80,245+advance*60,env*.79);
      frame('staub',t*.65+.7,212,343-advance*150,195+advance*40,190,env*.35);
    }
    if(state==='flare'){
      frame('feuer',t*1.5,216,385-pulse*180,170,115+pulse*185,Math.min(1,pulse*1.2));
      frame('staub',t*.8,192,315-advance*115,230,190,env*.29);
    }
  }


  function render(t){
    if(specials){
      const settings={figure:$('#figure').checked,light:$('#background').value==='light'};
      window.EdenSpecialFx.render(old,state,t,0,settings);window.EdenSpecialFx.render(fresh,state,t,1,settings);
      if($('#timeline')){$('#timeline').value=String(t%5.4);$('#time-value').textContent=(t%5.4).toFixed(2)+' s'}
      return;
    }
    const q=(t%3.8)/3.8,shown=$('#figure').checked;
    const catalogEffect=window.EDEN_FX_KATALOG.effects.find(e=>e.id===({fire:'C1',water:'C2',quake:'C3',electric:'C4',shortCircuit:'D1',mud:'D2',firestorm:'D3',steam:'D4',flare:'D5',mistral:'E1',wave:'E2',wind:'E3',tidal:'E4',doubleSlash:'E5',blur:'E6',vendetta:'E7',blackSlash:'E8',reticle:'E9',calm:'E10',beam:'E11',rain:'E12'})[state]);
    window.EdenFxPreview.render(old,catalogEffect,1,q,{stage:shown?'figure':'dark',legacy:true});
    background();
    if(state==='fire')frame('feuer',t,185,188,235,280,.85);
    if(shown){g.save();const impulse=state==='quake'?Math.exp(-q*13)*Math.sin(q*110)*7:0;contour(impulse,Math.abs(impulse)*.35,(reactions||specials)?Math.sin(Math.PI*clamp((t%3.8)/2.25)):1);figure(g,impulse,Math.abs(impulse)*.35);g.restore()}
    if(reactions){reaction(t,shown);return;}
    if(state==='fire'){
      frame('feuer',t+.67,210,290,175,205,.8);
      if(shown){m.clearRect(0,0,600,560);figure(m);m.globalCompositeOperation='source-atop';const glow=m.createLinearGradient(0,260,0,505);glow.addColorStop(0,'#ff990000');glow.addColorStop(1,`rgba(255,115,20,${.20+.035*Math.sin(t*8)})`);m.fillStyle=glow;m.fillRect(0,0,600,560);m.globalCompositeOperation='source-over';g.drawImage(material,0,0)}
    }
    if(state==='water'&&shown){
      m.clearRect(0,0,600,560);figure(m);m.globalCompositeOperation='source-atop';const wet=m.createLinearGradient(0,110,0,505);wet.addColorStop(0,'#071b2d00');wet.addColorStop(.28,'#05213399');wet.addColorStop(1,'#05213399');m.fillStyle=wet;m.fillRect(0,0,600,560);
      // Broad connected reflections, clipped by the sprite's alpha; no dots or rings.
      for(let j=0;j<4;j++){const x=250+(j%2)*65+Math.sin(t*.9+j)*8,y=225+Math.floor(j/2)*145; m.save();m.translate(x,y);m.scale(.55,1);const sheen=m.createRadialGradient(0,0,0,0,0,83);sheen.addColorStop(0,'#d7e5eb66');sheen.addColorStop(.3,'#b9d7e540');sheen.addColorStop(1,'#b9d7e500');m.fillStyle=sheen;m.fillRect(-85,-85,170,170);m.restore()}m.globalCompositeOperation='source-over';g.drawImage(material,0,0);
    }
    if(state==='quake'){
      const a=Math.sin(clamp(q*1.5)*Math.PI)*.62;
      frame('staub',t*.75,150-q*58+Math.sin(t*.8)*12,373-q*22,300+q*115,155+q*35,a*.85);
    }
    if(state==='electric'){
      const pulse=Math.sin(t*19)>.45&&Math.sin(t*6.7)>-.25;
      if(pulse){frame('strom',t,175,150,250,310,.82,'screen');if(shown){m.clearRect(0,0,600,560);figure(m);m.globalCompositeOperation='source-atop';m.fillStyle='#aacfff24';m.fillRect(0,0,600,560);m.globalCompositeOperation='source-over';g.drawImage(material,0,0)}}
    }
  }
  function update(){document.querySelectorAll('[data-state]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.state===state)));$('#state-label').textContent=info[state][0];$('#description').textContent=info[state][1];if(specials){const variants=window.EdenSpecialFx.defs[state];document.querySelectorAll('.caption span')[0].textContent=variants[0][0];$('#state-label').textContent=variants[1][0];document.querySelector('.compare article p').textContent=variants[0][1];$('#description').textContent=variants[1][1];}$('#note').value=feedback[state]?.note||'';document.querySelectorAll('[data-vote]').forEach(b=>b.classList.toggle('selected',feedback[state]?.vote===b.dataset.vote));$('#saved').textContent=feedback[state]?'Auf diesem Gerät gespeichert.':''}
  function save(){feedback[state]={...feedback[state],note:$('#note').value};try{localStorage.setItem(key,JSON.stringify(feedback));$('#saved').textContent='Auf diesem Gerät gespeichert.'}catch{$('#saved').textContent='Speichern nicht verfügbar. Bitte Rückmeldung herunterladen.'}}
  document.querySelectorAll('[data-state]').forEach(b=>b.onclick=()=>{state=b.dataset.state;time=specials?1.55:state==='electric'?.4:state==='flare'?.48:['doubleSlash','vendetta','blackSlash'].includes(state)?.47:.7;update();if(assetsReady)render(time)});
  document.querySelectorAll('[data-vote]').forEach(b=>b.onclick=()=>{feedback[state]={...feedback[state],vote:b.dataset.vote};save();update()});$('#note').oninput=save;
  $('#pause').textContent=paused?'Abspielen':'Pause';$('#pause').onclick=()=>{paused=!paused;$('#pause').textContent=paused?'Abspielen':'Pause'};
  $('#background').onchange=$('#figure').onchange=()=>{if(assetsReady)render(time)};
  $('#export').onclick=()=>{const a=document.createElement('a'),url=URL.createObjectURL(new Blob([JSON.stringify({version:specials?2:1,feedback,...(specials?{variants:Object.fromEntries(Object.entries(window.EdenSpecialFx.defs).map(([id,variants])=>[id,variants.map(v=>v[0])]))}:{})},null,2)],{type:'application/json'}));a.href=url;a.download=specials?'eden-spezialangriffe-rueckmeldung.json':reactions?'eden-reaktionen-rueckmeldung.json':'eden-status-rueckmeldung.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)};
  async function init(){
    const catalog=structuredClone(window.EDEN_FX_KATALOG);catalog.statusLabBase='';Object.values(catalog.assets).forEach(a=>a.file='../'+a.file);
    const results=await Promise.all([window.EdenFxPreview.init(catalog),load('figure','assets/figur_idle.webp'),...['feuer','staub','strom'].map(n=>load(n,'assets/'+(n==='staub'?'staub_frei':n)+'.png'))]);
    if(results[0].failed.length)throw new Error('Bisherige Vorschau unvollständig: '+results[0].failed.join(', '));
    if(specials){await Promise.all([load('flow','assets/stroemung.png'),load('flowMask','assets/stroemung_maske.png')]);window.EdenSpecialFx.init(images);}
    assetsReady=true;
    update();function tick(now){if(!paused&&last)time+=Math.min(.05,(now-last)/1000);last=now;render(time);requestAnimationFrame(tick)}requestAnimationFrame(tick);
  }
  init().catch(e=>{$('#error').textContent=e.message});
})();
