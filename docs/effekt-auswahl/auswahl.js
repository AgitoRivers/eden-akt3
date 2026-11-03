(() => {
  'use strict';
  const D=window.EDEN_FX_KATALOG, Fx=window.EdenFxPreview;
  const $=id=>document.getElementById(id), key='eden-rise-effektauswahl-v1';
  const ids=new Set(D.effects.map(e=>e.id));
  const byId=new Map(D.effects.map(e=>[e.id,e]));
  const subtypes={F1:['Stärkung','Heilung','Schwächung'],F4:['Feuer','Wasser','Erde','Strom'],G2:['Sieg','K.o.','Aufgabe'],J2:['Misslungen','Gut','Meisterhaft'],K4:['Liebt','Mag','Mag nicht'],L2:['Handy','Gag','Bordrat','Duell'],L6:['Mistral','Nachtlicht']};
  let selection={},notes={},subselections={},storageOK=true;
  let selected=D.effects[0],filtered=D.effects,views=[],running=false,started=0,raf=0;
  let motionAllowed=!matchMedia('(prefers-reduced-motion: reduce)').matches;
  let stage='figure',target='gegner',lastFrame=0,toastTimer;
  function safeChoices(obj){
    const out={};if(!obj||typeof obj!=='object'||Array.isArray(obj))return out;
    for(const id of ids){if([1,2,3].includes(obj[id]))out[id]=obj[id];}
    return out;
  }
  function safeNotes(obj){const out={};if(!obj||typeof obj!=='object'||Array.isArray(obj))return out;for(const id of ids)if(typeof obj[id]==='string')out[id]=obj[id].slice(0,3000);return out;}
  function safeSubtypes(obj){const out={};if(!obj||typeof obj!=='object')return out;for(const id of Object.keys(subtypes))if(subtypes[id].includes(obj[id]))out[id]=obj[id];return out;}
  function toast(text){$('toast').textContent=text;$('toast').hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('toast').hidden=true,4200);}
  function restore(){try{const saved=JSON.parse(localStorage.getItem(key)||'{}');selection=safeChoices(saved.selection);notes=safeNotes(saved.notes);subselections=safeSubtypes(saved.subtypes);if(ids.has(saved.current))selected=byId.get(saved.current);}catch{storageOK=false;}}
  function persist(){
    try{localStorage.setItem(key,JSON.stringify({schema:1,version:D.version,selection,notes,subtypes:subselections,current:selected.id,updated:new Date().toISOString()}));storageOK=true;}catch{storageOK=false;}
    $('saveStatus').textContent=storageOK?'Lokal in diesem Browser gespeichert.':'Browser-Speicher nicht verfügbar – bitte Auswahl herunterladen.';
  }
  function updateProgress(){const n=Object.keys(selection).length;$('progress').value=n;$('progressText').textContent=`${n} von ${D.effects.length} gewählt`;}
  function element(tag,cls,text){const el=document.createElement(tag);if(cls)el.className=cls;if(text!==undefined)el.textContent=text;return el;}
  function filter(){
    const q=$('search').value.trim().toLocaleLowerCase('de'),cat=$('category').value;
    filtered=D.effects.filter(e=>(!cat||e.category===cat)&&(!$('onlyOpen').checked||!selection[e.id])&&(!$('onlyMust').checked||e.priority==='M')&&(!q||`${e.id} ${e.name} ${e.description}`.toLocaleLowerCase('de').includes(q)));
    drawList();updatePager();
  }
  function drawList(){
    const list=$('effectList');list.replaceChildren();let prev='';
    for(const e of filtered){
      if(prev!==e.category){prev=e.category;const c=D.categories.find(c=>c.id===prev);list.append(element('div','list-group',`${c.id} · ${c.name}`));}
      const b=element('button','effect-item'+(selected.id===e.id?' active':''));b.type='button';b.dataset.id=e.id;b.setAttribute('aria-current',selected.id===e.id?'true':'false');
      b.append(element('span','item-id',e.id),element('span','item-name',e.name),element('span','item-check',selection[e.id]?'✓':''));
      b.setAttribute('aria-label',`${e.id} ${e.name}${selection[e.id]?', Variante '+selection[e.id]+' gewählt':''}`);b.onclick=()=>selectEffect(e.id);list.append(b);
    }
    if(!filtered.length)list.append(element('p','dim','Keine Effekte für diesen Filter.'));
    $('listCount').textContent=`${filtered.length} von ${D.effects.length} Effekten`;
  }
  function updatePager(){const i=filtered.findIndex(e=>e.id===selected.id);$('position').textContent=i<0?'Außerhalb Filter':`${i+1} / ${filtered.length}`;$('prev').disabled=filtered.length<2;$('next').disabled=filtered.length<2;}
  function settings(){return {stage,target:['A','B','C','D','E','F'].includes(selected.category)?target:selected.id==='G1'?'duc':'kontext',subtype:subselections[selected.id]||(subtypes[selected.id]||[])[0]};}
  function stop(){running=false;cancelAnimationFrame(raf);raf=0;}
  function posters(){for(const v of views)Fx.render(v.canvas,selected,v.index,.43,settings());}
  function play(index=null){
    if(!motionAllowed){posters();toast('Reduzierte Bewegung: Animationen zuerst bewusst freigeben.');return;}
    stop();running=true;started=performance.now();lastFrame=0;
    for(const v of views)v.playing=index===null||index===v.index;
    raf=requestAnimationFrame(tick);
  }
  function tick(now){
    if(!running)return;
    if(document.hidden){stop();return;}
    if(now-lastFrame<1000/30){raf=requestAnimationFrame(tick);return;}lastFrame=now;
    let complete=true;
    for(const view of views){if(!view.playing)continue;const duration=selected.variants[view.index].duration_ms;const elapsed=now-started;const t=Math.min(1,elapsed/duration);Fx.render(view.canvas,selected,view.index,t,settings());if(t<1)complete=false;}
    if(complete){if($('loop').checked){started=now+500;}else{running=false;raf=0;return;}}
    raf=requestAnimationFrame(tick);
  }
  function updateChoices(){
    const choice=selection[selected.id];
    for(const v of views){const chosen=choice===v.index+1;v.article.classList.toggle('chosen',chosen);v.button.textContent=chosen?'✓ Gewählt':`Variante ${v.index+1} wählen`;v.button.setAttribute('aria-pressed',String(chosen));}
    $('decisionText').textContent=choice?`Variante ${choice} · ${selected.variants[choice-1].label}`:'Noch keine Variante gewählt.';
    $('clearChoice').hidden=!choice;
    updateProgress();
  }
  function choose(index){selection[selected.id]=index+1;persist();updateChoices();filter();toast(`${selected.id}: ${selected.variants[index].label} gewählt.`);}
  function renderTechnical(){
    const box=$('technicalContent');box.replaceChildren();
    const sources=[...new Set(selected.variants.flatMap(v=>v.sources))];
    box.append(element('p','',sources.length?'IlluGen-Vorlagenvorschauen: '+sources.join(', '):'Engine-Animationsentwurf aus Linienbögen, Licht, Bewegung und Oberfläche.'));
    box.append(element('p','','Gemeinsame Bausteine werden wiederverwendet. Alle Varianten sind Auswahlentwürfe; Produktions-Exporte stehen aus.'));
    for(const v of selected.variants)box.append(element('p','',`${v.index+1} · ${v.duration_ms} ms · Treffer ${v.hit_ms} ms · ${v.loop?'Zustand mit wiederholbarer Schleife':'einmaliger Impuls'} · Ziel: ${v.target} · Ton separat.`));
    box.append(element('p','','Vor-/Hintergrund, Mischart und Anker werden beim Einbau an die tatsächlich gewählte Darstellung angepasst. Diese Vorschau greift nicht auf die Kampfsteuerung zu.'));
  }
  function selectEffect(id){
    if(!byId.has(id))return;stop();selected=byId.get(id);
    document.body.classList.remove('catalog-open');$('toggleCatalog').setAttribute('aria-expanded','false');
    if(['F4','C9'].includes(id)){target='duc';$('target').value='duc';}
    const cat=D.categories.find(c=>c.id===selected.category);
    $('effectCategory').textContent=cat.name;$('effectId').textContent=selected.id;$('effectName').textContent=selected.name;
    $('effectDescription').textContent=selected.description||'Bewegung, Licht und Oberfläche im Zusammenspiel.';
    $('priority').textContent=({M:'MUSS',S:'SCHÖN',L:'SPÄTER'})[selected.priority];
    $('targetLabel').hidden=!['A','B','C','D','E','F'].includes(selected.category);
    $('note').value=notes[id]||'';
    const sub=$('subtypes');sub.replaceChildren();
    if(subtypes[id]){
      sub.append(element('span','','Ausprägung:'));
      for(const label of subtypes[id]){const b=element('button',label===(settings().subtype)?'active':'',label);b.type='button';b.setAttribute('aria-pressed',String(label===settings().subtype));b.onclick=()=>{subselections[id]=label;persist();selectEffect(id);};sub.append(b);}
    }
    const host=$('variants');host.replaceChildren();views=[];
    for(const variant of selected.variants){
      const article=element('article','variant');
      const top=element('div','variant-top'),title=element('div');title.append(element('p','eyebrow',`VARIANTE 0${variant.index+1}`),element('h3','',variant.label));
      const one=element('button','circle play-one','▶');one.type='button';one.setAttribute('aria-label',`${selected.id} Variante ${variant.index+1} abspielen`);one.onclick=()=>play(variant.index);top.append(title,one);
      const wrap=element('div','canvas-wrap');const canvas=element('canvas');canvas.width=600;canvas.height=460;canvas.setAttribute('aria-label',`${selected.name} – ${variant.label}: animierte Vorschau`);canvas.setAttribute('role','img');
      wrap.append(canvas,element('span','stage-caption','AUSWAHLENTWURF · TESTBÜHNE'));
      const meta=element('div','variant-meta');meta.append(element('p','',variant.description));const pills=element('div','pills');
      pills.append(element('span','pill',`${(variant.duration_ms/1000).toFixed(2).replace('.',',')} s`),element('span','pill',selected.loop?'Auftakt + Schleife':'Einzelimpuls'));meta.append(pills);
      const button=element('button','button choose',`Variante ${variant.index+1} wählen`);button.type='button';button.onclick=()=>choose(variant.index);meta.append(button);
      if(variant.preview_flipbook){const download=element('a','text-button atlas-download','Transparenten Bilderbogen laden');download.href=variant.preview_flipbook.file;download.download=variant.id+'-vorschau.png';meta.append(download);}
      article.append(top,wrap,meta);host.append(article);views.push({article,canvas,button,index:variant.index,playing:false});
    }
    updateChoices();drawList();updatePager();renderTechnical();persist();posters();
  }
  function navigate(dir){if(!filtered.length)return;let i=filtered.findIndex(e=>e.id===selected.id);if(i<0)i=dir>0?-1:0;const next=(i+dir+filtered.length)%filtered.length;selectEffect(filtered[next].id);}
  function nextOpen(){const start=D.effects.findIndex(e=>e.id===selected.id);for(let d=1;d<=D.effects.length;d++){const e=D.effects[(start+d)%D.effects.length];if(!selection[e.id]){if(!filtered.some(f=>f.id===e.id)){$('search').value='';$('category').value='';$('onlyMust').checked=false;filter();}selectEffect(e.id);return;}}toast('Alle 81 Effekte sind gewählt. Du kannst deine Auswahl herunterladen.');}
  function exportSelection(){
    const out={schema:'eden-fx-auswahl/1',catalog_version:D.version,inventory_sha256:D.inventory_sha256,
      exported:new Date().toISOString(),selection,notes,subtypes:subselections,
      status:'Auswahlentwürfe – finale Produktions-Exporte noch ausstehend',
      selected_effects:D.effects.filter(e=>selection[e.id]).map(e=>({id:e.id,name:e.name,variant:e.variants[selection[e.id]-1],note:notes[e.id]||'',subtype:subselections[e.id]||null}))};
    const blob=new Blob([JSON.stringify(out,null,2)+'\n'],{type:'application/json'}),url=URL.createObjectURL(blob),link=document.createElement('a');
    link.href=url;link.download='eden-effektauswahl-'+new Date().toISOString().slice(0,10)+'.json';document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),3000);
    toast(`${Object.keys(selection).length} Entscheidungen als Datei heruntergeladen.`);
  }
  async function importSelection(file){
    if(!file)return;if(file.size>2_000_000){toast('Die Auswahldatei ist zu groß.');return;}
    try{
      const input=JSON.parse(await file.text());
      if(!input||typeof input!=='object'||(input.schema!=='eden-fx-auswahl/1'&&input.schema!==1)||!input.selection||typeof input.selection!=='object')throw Error();
      const choices=safeChoices(input.selection);if(Object.keys(input.selection).some(id=>!ids.has(id)||![1,2,3].includes(input.selection[id])))throw Error();
      try{localStorage.setItem(key+'-vor-import',JSON.stringify({selection,notes,subtypes:subselections}));}catch{}
      selection={...selection,...choices};notes={...notes,...safeNotes(input.notes)};subselections={...subselections,...safeSubtypes(input.subtypes)};
      persist();filter();selectEffect(selected.id);toast(`${Object.keys(choices).length} Entscheidungen importiert. Vorherige Auswahl lokal gesichert.`);
    }catch{toast('Diese Datei ist keine gültige Eden-Effektauswahl. Deine Auswahl bleibt erhalten.');}
    $('importFile').value='';
  }
  restore();
  for(const c of D.categories){const op=document.createElement('option');op.value=c.id;op.textContent=c.id+' · '+c.name;$('category').append(op);}
  for(const id of ['search','category','onlyOpen','onlyMust'])$(id).addEventListener(id==='search'?'input':'change',filter);
  $('playAll').onclick=()=>play();$('prev').onclick=()=>navigate(-1);$('next').onclick=()=>navigate(1);$('nextOpen').onclick=nextOpen;
  $('toggleCatalog').onclick=()=>{const open=document.body.classList.toggle('catalog-open');$('toggleCatalog').setAttribute('aria-expanded',String(open));};
  $('loop').onchange=()=>{if($('loop').checked)play();};
  $('stage').onchange=()=>{stage=$('stage').value;stop();posters();};$('target').onchange=()=>{target=$('target').value;stop();posters();};
  $('note').oninput=()=>{const value=$('note').value;if(value)notes[selected.id]=value;else delete notes[selected.id];persist();};
  $('clearChoice').onclick=()=>{delete selection[selected.id];persist();updateChoices();filter();};
  $('export').onclick=exportSelection;$('import').onclick=()=>$('importFile').click();$('importFile').onchange=e=>importSelection(e.target.files[0]);
  $('about').onclick=()=>$('aboutDialog').showModal();$('closeAbout').onclick=()=>$('aboutDialog').close();
  $('motionNotice').hidden=motionAllowed;$('allowMotion').onclick=()=>{motionAllowed=true;$('motionNotice').hidden=true;play();};
  const media=matchMedia('(prefers-reduced-motion: reduce)');media.addEventListener('change',event=>{if(event.matches){motionAllowed=false;$('motionNotice').hidden=false;stop();posters();}});
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
  document.addEventListener('keydown',event=>{
    if(event.altKey||event.ctrlKey||event.metaKey||$('aboutDialog').open||['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName))return;
    if(['1','2','3'].includes(event.key)){event.preventDefault();choose(Number(event.key)-1);}
    else if(event.key==='ArrowRight'){event.preventDefault();navigate(1);}else if(event.key==='ArrowLeft'){event.preventDefault();navigate(-1);}
  });
  filter();selectEffect(selected.id);
  Fx.init(D).then(result=>{posters();if(result.failed.length){$('saveStatus').textContent='Einige Vorschaubilder fehlen. Ordner vollständig kopieren.';toast(`${result.failed.length} Vorschaubilder konnten nicht geladen werden.`);}});
  // Read-only diagnostics support review without touching the game.
  window.EdenFxAuswahl={snapshot:()=>({effect:selected.id,selection:{...selection},notes:{...notes},subtypes:{...subselections},filtered:filtered.length,variants:views.length,running,storageOK,assets:Fx.stats()}),renderAt:t=>{stop();for(const view of views)Fx.render(view.canvas,selected,view.index,t,settings());}};
})();
