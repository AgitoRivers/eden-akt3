/* Separate visual lab. No game requests; feedback uses its own localStorage key. */
(() => {
  'use strict';
  const $=s=>document.querySelector(s), reactions=new URLSearchParams(location.search).get('kategorie')==='reaktionen', key=reactions?'eden-rise-reaktionen-labor-v1':'eden-rise-status-labor-v1';
  const info={fire:['Brennend','Höher ansetzende, farbige Flammen. Eine weiche warme Kontur bleibt während des Zustands sichtbar.'],water:['Nass','Kräftigere Nässe mit dunklerem Stoff und deutlicheren Reflexen. Eine weiche blaue Kontur bleibt sichtbar.'],quake:['Erschüttert','Höherer, frei driftender Nebel mit weich auslaufenden Rändern. Eine dezente sandfarbene Kontur bleibt sichtbar.'],electric:['Unter Strom','Die bewerteten Entladungen bleiben erhalten. Eine weiche goldene Kontur ist auch zwischen den Impulsen sichtbar.']};
  const reactionInfo={shortCircuit:['Kurzschluss','Nässe und Strom: unregelmäßige, kräftige Entladungen mit einer kurzen Dampffahne.'],mud:['Schlamm','Nässe und Erschütterung: ein zusammenhängender brauner Schwall, der am Boden weich ausläuft.'],firestorm:['Feuersturm','Feuer und Strom: gegeneinander ziehende Flammen mit kurzen elektrischen Entladungen.'],steam:['Dampf','Feuer und Nässe: die Flamme erlischt, dichter Dampf steigt auf und verliert sich weich.'],flare:['Ausbrennen','Feuer und Blutung: eine kurze hohe Stichflamme, danach nur noch ein leichter Rauchschleier.']};
  if(reactions){Object.assign(info,reactionInfo);$('#page-title').textContent='Reaktionen im Vergleich';$('#page-intro').textContent='Fünf Kombinationen aus den bewährten Zuständen. Kurzer Auftakt, weiches Auslaufen und eine Kontur während der Reaktion.';$('#effects-nav').replaceChildren(...Object.entries(reactionInfo).map(([id,value])=>{const button=document.createElement('button');button.dataset.state=id;button.textContent=value[0];button.setAttribute('aria-pressed','false');return button}));document.title='Eden Rise · Reaktionen';}
  document.querySelectorAll('.categories a').forEach(a=>{if(a.href.includes('kategorie=reaktionen')===reactions)a.setAttribute('aria-current','page')});
  let state=reactions?'shortCircuit':'fire',paused=matchMedia('(prefers-reduced-motion: reduce)').matches,time=.7,last=0,feedback={};
  try{feedback=JSON.parse(localStorage.getItem(key)||'{}')}catch{}
  const images={},old=$('#old'),fresh=$('#new'),g=fresh.getContext('2d');
  const material=document.createElement('canvas');material.width=600;material.height=560;const m=material.getContext('2d');
  const load=(name,url)=>new Promise((resolve,reject)=>{const i=new Image();i.onload=()=>{images[name]=i;resolve()};i.onerror=()=>reject(new Error('Bild konnte nicht geladen werden: '+url));i.src=url});
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
      c.fillStyle=({fire:'#ff9a48',water:'#72c7e2',quake:'#cfbaa0',electric:'#e8cf82',shortCircuit:'#9bd6f2',mud:'#b29b72',firestorm:'#ff9a48',steam:'#c7d9df',flare:'#f29a65'})[state];c.fillRect(0,0,600,560);
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
      // A cohesive wet ground film, with transparent edges, rather than drops.
      m.clearRect(0,0,600,560);m.save();m.translate(300,473);m.scale(1,.22);
      const film=m.createRadialGradient(0,0,12,0,0,165);film.addColorStop(0,'#634329dc');film.addColorStop(.55,'#77533abd');film.addColorStop(1,'#533c2b00');m.fillStyle=film;m.fillRect(-170,-170,340,340);m.restore();g.save();g.globalAlpha=env;g.drawImage(material,0,0);g.restore();
      // Recolour one coherent rolling volume; preserve the original opacity.
      m.clearRect(0,0,600,560);const im=images.staub,n=Math.floor(t*25)%64;
      m.drawImage(im,n%8*256,Math.floor(n/8)*256,256,256,130-advance*25,388-advance*12,335+advance*55,130);
      m.globalCompositeOperation='source-atop';m.fillStyle='#795232ce';m.fillRect(0,0,600,560);m.globalCompositeOperation='source-over';g.save();g.globalAlpha=env*.82;g.drawImage(material,0,0);g.restore();
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
    const q=(t%3.8)/3.8,shown=$('#figure').checked;
    const catalogEffect=window.EDEN_FX_KATALOG.effects.find(e=>e.id===({fire:'C1',water:'C2',quake:'C3',electric:'C4',shortCircuit:'D1',mud:'D2',firestorm:'D3',steam:'D4',flare:'D5'})[state]);
    window.EdenFxPreview.render(old,catalogEffect,1,q,{stage:shown?'figure':'dark'});
    background();
    if(state==='fire')frame('feuer',t,185,188,235,280,.85);
    if(shown){g.save();const impulse=state==='quake'?Math.exp(-q*13)*Math.sin(q*110)*7:0;contour(impulse,Math.abs(impulse)*.35,reactions?Math.sin(Math.PI*clamp((t%3.8)/2.25)):1);figure(g,impulse,Math.abs(impulse)*.35);g.restore()}
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
  function update(){document.querySelectorAll('[data-state]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.state===state)));$('#state-label').textContent=info[state][0];$('#description').textContent=info[state][1];$('#note').value=feedback[state]?.note||'';document.querySelectorAll('[data-vote]').forEach(b=>b.classList.toggle('selected',feedback[state]?.vote===b.dataset.vote));$('#saved').textContent=feedback[state]?'Auf diesem Gerät gespeichert.':''}
  function save(){feedback[state]={...feedback[state],note:$('#note').value};try{localStorage.setItem(key,JSON.stringify(feedback));$('#saved').textContent='Auf diesem Gerät gespeichert.'}catch{$('#saved').textContent='Speichern nicht verfügbar. Bitte Rückmeldung herunterladen.'}}
  document.querySelectorAll('[data-state]').forEach(b=>b.onclick=()=>{state=b.dataset.state;time=state==='electric'?.4:state==='flare'?.48:.7;update();if(images.figure)render(time)});
  document.querySelectorAll('[data-vote]').forEach(b=>b.onclick=()=>{feedback[state]={...feedback[state],vote:b.dataset.vote};save();update()});$('#note').oninput=save;
  $('#pause').textContent=paused?'Abspielen':'Pause';$('#pause').onclick=()=>{paused=!paused;$('#pause').textContent=paused?'Abspielen':'Pause'};
  $('#background').onchange=$('#figure').onchange=()=>{if(images.figure)render(time)};
  $('#export').onclick=()=>{const a=document.createElement('a'),url=URL.createObjectURL(new Blob([JSON.stringify({version:1,feedback},null,2)],{type:'application/json'}));a.href=url;a.download=reactions?'eden-reaktionen-rueckmeldung.json':'eden-status-rueckmeldung.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)};
  async function init(){
    const catalog=structuredClone(window.EDEN_FX_KATALOG);Object.values(catalog.assets).forEach(a=>a.file='../'+a.file);
    const results=await Promise.all([window.EdenFxPreview.init(catalog),load('figure','assets/figur_idle.webp'),...['feuer','staub','strom'].map(n=>load(n,'assets/'+n+'.png'))]);
    if(results[0].failed.length)throw new Error('Bisherige Vorschau unvollständig: '+results[0].failed.join(', '));
    update();function tick(now){if(!paused&&last)time+=Math.min(.05,(now-last)/1000);last=now;render(time);requestAnimationFrame(tick)}requestAnimationFrame(tick);
  }
  init().catch(e=>{$('#error').textContent=e.message});
})();
