/* Separate visual lab. No game requests; feedback uses its own localStorage key. */
(() => {
  'use strict';
  const $=s=>document.querySelector(s), specials=new URLSearchParams(location.search).get('kategorie')==='spezialangriffe', reactions=new URLSearchParams(location.search).get('kategorie')==='reaktionen', key=specials?'eden-rise-spezial-labor-v3':reactions?'eden-rise-reaktionen-labor-v1':'eden-rise-status-labor-v1';
  const info={fire:['Brennend','Höher ansetzende, farbige Flammen. Eine weiche warme Kontur bleibt während des Zustands sichtbar.'],water:['Nass','Ein kräftiger Splash am Körper, danach nasser Stoff und dezente bewegte Glanzreflexe. Schutzpose und weiche blaue Kontur bleiben erhalten.'],quake:['Erschüttert','Schutzpose und anhaltendes Rütteln, dazu dichte, überlappende Stein-Ausbrüche mit hohen Sprüngen über rund dreieinhalb Sekunden. Ohne festen Bodenriss oder Nebel – für unterschiedliche Schauplätze.'],electric:['Unter Strom','Die bewerteten Entladungen bleiben erhalten. Eine weiche goldene Kontur ist auch zwischen den Impulsen sichtbar.']};
  const reactionInfo={shortCircuit:['Kurzschluss','Nässe und Strom: unregelmäßige, kräftige Entladungen mit einer kurzen Dampffahne.'],mud:['Schlamm','Nässe und Erschütterung: kräftige braune Erdklumpen-Ausbrüche, nasser Körperfilm und ein frei auslaufender Schlammfuß.'],firestorm:['Feuersturm','Feuer und Strom: gegeneinander ziehende Flammen mit kurzen elektrischen Entladungen.'],steam:['Dampf','Feuer und Nässe: die Flamme erlischt, dichter Dampf steigt auf und verliert sich weich.'],flare:['Ausbrennen','Feuer und Blutung: eine kurze hohe Stichflamme, danach nur noch ein leichter Rauchschleier.']};
  const specialInfo={mistral:['Mistral','Ein seitlicher Windstoß zieht als zusammenhängende Fahne durch die Figur.'],wave:['Ressac','Drei Wasserformen aus echten LiquiGen-Bildfolgen: Stoß, Ausbruch und Kombination.'],wind:['Libeccio','Ein weicher Windschleier um die Figur; die Kontur begleitet den sichtbaren Zustand.'],tidal:['Lame de Fond','Drei kräftige Wasserangriffe aus neuen LiquiGen-Exporten.'],doubleSlash:['Doppio Gioco','Zwei zeitlich versetzte, breite und texturierte Schnittbewegungen.'],blur:['Sotto Voce','Eine weiche versetzte Silhouette lässt die Figur kurz verschwimmen.'],vendetta:['Vendetta','Eine breite Schnittbewegung mit kurzem rotem Trefferlicht.'],blackSlash:['Omertà','Die Szene dunkelt ab, dann ist eine einzige texturierte Schnittbewegung sichtbar.'],reticle:['Point de Mire','Ruhiges Zielllicht am Oberkörper, anschließend eine matte Kontur.'],calm:['Bonaccia','Ein ruhiger kühler Schleier legt sich über den unteren Bildraum.'],beam:['Phare','Ein weicher warmer Lichtkegel fällt auf die Figur.'],rain:['Pluie d’Étoiles','Drei breite Lichtbahnen mit einem kurzen Nebelimpuls am Boden.']};
  if(reactions){Object.assign(info,reactionInfo);$('#page-title').textContent='Reaktionen im Vergleich';$('#page-intro').textContent='Fünf Kombinationen aus den bewährten Zuständen. Kurzer Auftakt, weiches Auslaufen und eine Kontur während der Reaktion.';$('#effects-nav').replaceChildren(...Object.entries(reactionInfo).map(([id,value])=>{const button=document.createElement('button');button.dataset.state=id;button.textContent=value[0];button.setAttribute('aria-pressed','false');return button}));document.title='Eden Rise · Reaktionen';}
  if(specials){Object.assign(info,specialInfo);$('#page-title').textContent='Spezialangriffe im Vergleich';$('#page-intro').textContent='Zwölf Angriffe als erste Gestaltungsvorschläge mit den freigegebenen Bausteinen.';$('#effects-nav').replaceChildren(...Object.entries(specialInfo).map(([id,value])=>{const b=document.createElement('button');b.dataset.state=id;b.textContent=value[0];return b}));document.title='Eden Rise · Spezialangriffe';}
  document.querySelectorAll('.categories a').forEach(a=>{const url=new URL(a.href);if(url.pathname.endsWith('/status-labor/')&&(url.searchParams.get('kategorie')||'')===(specials?'spezialangriffe':reactions?'reaktionen':''))a.setAttribute('aria-current','page')});
  let state=specials?'mistral':reactions?'shortCircuit':'fire',paused=matchMedia('(prefers-reduced-motion: reduce)').matches,time=specials?1.55:.7,last=0,feedback={},assetsReady=false;
  try{feedback=JSON.parse(localStorage.getItem(key)||'{}')}catch{}
  const images={},old=$('#old'),fresh=$('#new'),g=fresh.getContext('2d');
  const material=document.createElement('canvas');material.width=600;material.height=560;const m=material.getContext('2d');
  const load=(name,url)=>new Promise((resolve,reject)=>{const i=new Image();i.onload=()=>{images[name]=i;resolve()};i.onerror=()=>reject(new Error('Bild konnte nicht geladen werden: '+url));i.src=url});

  let third;
  if(specials){
    document.body.classList.add('specials');
    const article=document.querySelector('.compare article').cloneNode(true);
    third=article.querySelector('canvas');third.id='third';third.setAttribute('aria-label','Spezialangriff Variante 3');
    article.querySelector('h2').textContent='Variante 3';article.querySelector('.caption span').id='state-label-3';article.querySelector('p').id='description-3';document.querySelector('.compare').append(article);
    $('#page-intro').textContent='Zwölf Angriffe mit je drei unterschiedlichen Varianten. Feine Klingenspuren und natürliche Bildmaterialien. Alle Varianten laufen synchron; die Zeitleiste zeigt jeden Moment.';
    document.querySelector('.compare').setAttribute('aria-label','Drei Varianten im direkten Vergleich');
    document.querySelectorAll('.caption h2')[0].textContent='Variante 1';
    document.querySelectorAll('.caption h2')[1].textContent='Variante 2';
    old.setAttribute('aria-label','Spezialangriff Variante 1');fresh.setAttribute('aria-label','Spezialangriff Variante 2');
    const votes=document.querySelectorAll('[data-vote]');
    votes[0].dataset.vote='variant1';votes[0].textContent='Variante 1 wählen';
    votes[1].dataset.vote='variant2';votes[1].textContent='Variante 2 wählen';
    votes[2].dataset.vote='revise';votes[2].textContent='Alle überarbeiten';const vote3=document.createElement('button');vote3.dataset.vote='variant3';vote3.textContent='Variante 3 wählen';votes[2].before(vote3);
    const rules=document.createElement('section');rules.className='feedback';rules.setAttribute('aria-label','Bedeutung und Spielwirkung');
    const type=document.createElement('h2');type.id='attack-type';const effect=document.createElement('p');effect.id='attack-rule';
    const source=document.createElement('small');source.textContent='Spielwirkung laut Kampfplan und Balancingstand; diese Vorschau löst keinen Kampf aus.';rules.append(type,effect,source);document.querySelector('.compare').after(rules);
    const controls=document.querySelector('.controls'),replay=document.createElement('button');
    replay.id='replay';replay.textContent='Von vorn';replay.onclick=()=>{time=0;if(assetsReady)render(time)};controls.append(replay);
    const label=document.createElement('label');label.className='timeline';label.textContent='Ablauf ';
    const slider=document.createElement('input');slider.type='range';slider.id='timeline';slider.min='0';slider.max='5.35';slider.step='.01';slider.value='1.55';slider.setAttribute('aria-label','Zeitpunkt des Spezialangriffs');
    slider.oninput=()=>{time=Number(slider.value);paused=true;$('#pause').textContent='Abspielen';if(assetsReady)render(time)};label.append(slider);
    const value=document.createElement('output');value.id='time-value';value.textContent='1.55 s';label.append(value);controls.append(label);
  }

  if(!specials){
    const figureLabel=document.createElement('label');figureLabel.textContent='Vergleichsfigur ';const picker=document.createElement('select');picker.id='preview-figure';picker.setAttribute('aria-label','Vergleichsfigur');figureLabel.append(picker);document.querySelector('.controls').prepend(figureLabel);
    const hint=document.createElement('p');hint.textContent='Die Figurenauswahl gilt für den neuen Entwurf. Links bleibt die bisherige Referenz.';hint.style.cssText='color:#aab1b3;font-size:12px';document.querySelector('.compare').before(hint);
    const controls=document.querySelector('.controls'),replay=document.createElement('button');replay.id='replay';replay.textContent='Von vorn';replay.onclick=()=>{time=0;if(assetsReady)render(time)};controls.append(replay);
    const label=document.createElement('label');label.className='timeline';label.textContent='Ablauf ';
    const slider=document.createElement('input');slider.id='timeline';slider.type='range';slider.min='0';slider.max='4.15';slider.step='.01';slider.value='.7';slider.setAttribute('aria-label','Zeitpunkt des Zustands oder der Reaktion');
    slider.oninput=()=>{time=Number(slider.value);paused=true;$('#pause').textContent='Abspielen';if(assetsReady)render(time)};label.append(slider);
    const value=document.createElement('output');value.id='time-value';label.append(value);controls.append(label);
    const tempo=document.createElement('label');tempo.textContent='Tempo ';const speed=document.createElement('select');speed.id='lab-speed';for(const [value,text] of [['1','Normal'],['0.4','Zeitlupe']]){const o=document.createElement('option');o.value=value;o.textContent=text;speed.append(o)}tempo.append(speed);controls.append(tempo);
    const phase=document.createElement('p');phase.id='pose-phase';phase.setAttribute('aria-live','off');controls.after(phase);
    $('#page-intro').textContent=reactions?'Fünf Reaktionen mit länger sichtbarer Trefferpose, passendem Körperlicht und weicher Erholung.':'Vier Zustände mit passender Figurenreaktion, lebendigen Materialschichten und einer weichen Kontur während der Wirkung.';
  }
  function render(t){
    if(specials){
      const settings={figure:$('#figure').checked,light:$('#background').value==='light'};
      window.EdenSpecialFx.render(old,state,t,0,settings);window.EdenSpecialFx.render(fresh,state,t,1,settings);window.EdenSpecialFx.render(third,state,t,2,settings);
      $('#timeline').value=String(t%5.4);$('#time-value').textContent=(t%5.4).toFixed(2)+' s';return;
    }
    const ids={fire:'C1',water:'C2',quake:'C3',electric:'C4',shortCircuit:'D1',mud:'D2',firestorm:'D3',steam:'D4',flare:'D5'};
    const shown=$('#figure').checked,effect=window.EDEN_FX_KATALOG.effects.find(e=>e.id===ids[state]);
    window.EdenFxPreview.render(old,effect,1,(t%3.8)/3.8,{stage:shown?'figure':'dark',legacy:true});
    const result=window.EdenStateFx.render(fresh,state,t,{figure:shown,light:$('#background').value==='light'}),elapsed=t%4.2;
    $('#timeline').value=String(elapsed);$('#time-value').textContent=elapsed.toFixed(2)+' s';
    $('#pose-phase').textContent=elapsed<.28?'Auftakt':result.weight>.95?(['water','quake'].includes(state)?'Schutzreaktion':'Trefferreaktion'):result.weight>.01?'Weiche Erholung':reactions?'Ausklang':'Zustand aktiv';
  }
  function update(){document.querySelectorAll('[data-state]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.state===state)));$('#state-label').textContent=info[state][0];$('#description').textContent=info[state][1];if(specials){const variants=window.EdenSpecialFx.defs[state];document.querySelectorAll('.caption span')[0].textContent=variants[0][0];$('#state-label').textContent=variants[1][0];document.querySelector('.compare article p').textContent=variants[0][1];$('#description').textContent=variants[1][1];$('#state-label-3').textContent=variants[2][0];$('#description-3').textContent=variants[2][1];const rule=window.EdenAttackRules[state];$('#attack-type').textContent=rule.type+' · ab Stufe '+rule.level+' · '+rule.cost+' Ausdauer';$('#attack-rule').textContent=rule.effect;}$('#note').value=feedback[state]?.note||'';document.querySelectorAll('[data-vote]').forEach(b=>b.classList.toggle('selected',feedback[state]?.vote===b.dataset.vote));$('#saved').textContent=feedback[state]?'Auf diesem Gerät gespeichert.':''}
  function save(){feedback[state]={...feedback[state],note:$('#note').value};try{localStorage.setItem(key,JSON.stringify(feedback));$('#saved').textContent='Auf diesem Gerät gespeichert.'}catch{$('#saved').textContent='Speichern nicht verfügbar. Bitte Rückmeldung herunterladen.'}}
  document.querySelectorAll('[data-state]').forEach(b=>b.onclick=()=>{state=b.dataset.state;time=specials?1.55:state==='electric'?.53:state==='flare'?.48:['doubleSlash','vendetta','blackSlash'].includes(state)?.47:.7;update();if(assetsReady)render(time)});
  document.querySelectorAll('[data-vote]').forEach(b=>b.onclick=()=>{feedback[state]={...feedback[state],vote:b.dataset.vote};save();update()});$('#note').oninput=save;
  $('#pause').textContent=paused?'Abspielen':'Pause';$('#pause').onclick=()=>{paused=!paused;$('#pause').textContent=paused?'Abspielen':'Pause'};
  $('#background').onchange=$('#figure').onchange=()=>{if(assetsReady)render(time)};
  $('#export').onclick=()=>{const a=document.createElement('a'),url=URL.createObjectURL(new Blob([JSON.stringify({version:specials?3:1,feedback,...(specials?{variants:Object.fromEntries(Object.entries(window.EdenSpecialFx.defs).map(([id,variants])=>[id,variants.map(v=>v[0])]))}:{})},null,2)],{type:'application/json'}));a.href=url;a.download=specials?'eden-spezialangriffe-rueckmeldung.json':reactions?'eden-reaktionen-rueckmeldung.json':'eden-status-rueckmeldung.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)};
  async function init(){
    const catalog=structuredClone(window.EDEN_FX_KATALOG);catalog.statusLabBase='';Object.values(catalog.assets).forEach(a=>a.file='../'+a.file);
    const results=await Promise.all([window.EdenFxPreview.init(catalog),load('figure','assets/figur_idle.webp'),...(!specials?[load('hurt','assets/figur_hurt.webp'),load('guard','assets/figur_guard.webp'),load('bodenbruch','assets/bodenbruch-real-v1.png'),load('wetSplash','ablaufprobe/spritzwasser-natuerlich.png')]:[]),...['feuer','staub','strom'].map(n=>load(n,'assets/'+(n==='staub'?'staub_frei':n)+'.png'))]);
    if(results[0].failed.length)throw new Error('Bisherige Vorschau unvollständig: '+results[0].failed.join(', '));
    if(specials){await Promise.all([load('stahl','assets/realismus-v3/stahl-gerade.png'),load('stahlrot','assets/realismus-v3/stahl-vendetta-rot.png'),load('stahlviolett','assets/realismus-v3/stahl-doppio-violett-v1.png'),load('liquigenWater','assets/liquigen-welle.png?v=1'),load('licht','assets/realismus-v3/licht.png'),load('glint','assets/realismus-v3/kenney-flare_01.png'),load('trace','assets/realismus-v3/kenney-trace_04.png'),load('druckstoss','assets/druckstoss.png'),load('waterJet','assets/native-v6/wasserstoss.png'),load('waterColumn','assets/native-v6/ausbruch.png?v=2'),load('impactNative','assets/native-v6/treffer.png')]);window.EdenSpecialFx.init(images);}
    if(!specials)await window.EdenFigurePicker.mount($('#preview-figure'),{base:'assets/',onChange(set){images.figure=set.idle;images.hurt=set.hurt;images.guard=set.guard;window.EdenStateFx.init(images);if(assetsReady)render(time)}});
    if(!specials){window.EdenStateFx.init(images);window.EdenStateLab={render(value){time=value;render(value)},get state(){return state},duration:4.2};}
    assetsReady=true;
    update();function tick(now){if(!paused&&last)time+=Math.min(.05,(now-last)/1000)*Number($('#lab-speed')?.value||1);last=now;render(time);requestAnimationFrame(tick)}requestAnimationFrame(tick);
  }
  init().catch(e=>{$('#error').textContent=e.message});
})();
