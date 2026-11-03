/* Level-up ceremony (Duc 28.10.2026): full screen after every fight with a level up, Maxwell's training included.
   Beat 1 the moment (level, HP counting up, points), beat 2 the attribute point, beat 3 the skill tree with a burn-in
   per learned skill, main path banner and mastery. Presentation only: the actions stay attribut_steigern, skill_lernen
   and kampf_schliessen. Animations play once per state change; a plain re-render shows the final picture. UI English. */
(()=>{'use strict';
const artBase=new URL('paths/',document.currentScript.src).href;
const PATHS={K:{color:'#94bfc8',mark:'I',pos:'center 42%'},L:{color:'#c2a0e5',mark:'II',pos:'center'},W:{color:'#80c8ba',mark:'III',pos:'center 30%'},M:{color:'#ec9270',mark:'IV',pos:'center 20%'},H:{color:'#9fd6a6',mark:'V',pos:'center 62%'}};
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const busy=()=>typeof beschaeftigt!=='undefined'&&beschaeftigt;
const sfx=(id,ms)=>{if(window.EdenSfx)try{EdenSfx.play(id,ms||0)}catch(e){}};
const still=()=>window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
const INTRO_MS=2100,FINALE_MS=3200;
// key = fight + new level; snap = what the last render showed, so the next state can tell what just changed
let S={key:null,intro:false,introBis:0,snap:null,sig:'',fx:null,echo:null,sel:null,baum:false,last:null,timer:null};

function snapshot(pr){
 const skills=pr.pfade.flatMap(p=>p.skills);
 return {attrs:Object.fromEntries(pr.attribute.map(a=>[a.id,a.wert])),learned:skills.filter(s=>s.gelernt).map(s=>s.id),
  zahl:Object.fromEntries(skills.map(s=>[s.id,s.zahl||''])),main:pr.hauptpfad||'',
  mastered:pr.pfade.filter(p=>p.skills.length&&p.skills.every(s=>s.gelernt)).map(p=>p.id)};
}
function diff(a,b,pr){
 const fx={},echo=[],skills=pr.pfade.flatMap(p=>p.skills.map(s=>({...s,pfad:p})));
 const att=pr.attribute.find(x=>b.attrs[x.id]>(a.attrs[x.id]||0));
 if(att){fx.attr=att.id;echo.push(`<b>${esc(att.label)}</b> ${esc(a.attrs[att.id])} → ${esc(b.attrs[att.id])}`);}
 const neu=skills.find(s=>s.gelernt&&!a.learned.includes(s.id));
 if(neu){fx.learn=neu.id;fx.path=neu.pfad.id;echo.push(`<b>${esc(neu.label)}</b> burned in`);}
 else skills.filter(s=>s.zahl&&a.zahl[s.id]&&s.zahl!==a.zahl[s.id]).slice(0,3)
  .forEach(s=>echo.push(`${esc(s.label)} ${esc(a.zahl[s.id])} → <b>${esc(s.zahl)}</b>`));
 if(b.main&&b.main!==a.main)fx.main={vorher:a.main,nachher:b.main};
 const m=b.mastered.find(id=>!a.mastered.includes(id));if(m)fx.master=m;
 return {fx,echo};
}
const gained=(pr,auf)=>(pr.skillpunkte_plan||[]).filter(x=>x.level>auf.von&&x.level<=auf.auf).reduce((n,x)=>n+x.punkte,0);
const icon=id=>window.EdenSkills?EdenSkills.iconHtml(id):'';

function held(pr,auf,finale){
 const proLv=auf.auf>auf.von?auf.lp/(auf.auf-auf.von):5,cap=pr.lp_max+proLv*Math.max(0,pr.level_max-pr.level);
 const alt=pr.lp_max-auf.lp,sp=gained(pr,auf);
 return `<section class="lvl-held"><div class="lvl-glanz" aria-hidden="true"></div>
  <small class="lvl-ueber">${finale?'Max level':'Level up'}</small>
  <div class="lvl-zahl"><span>LEVEL</span><b>${esc(auf.auf)}</b></div>
  <div class="lvl-gewinne">
   <div class="lvl-hp"><span>Max HP</span><div class="lvl-bar"><i class="neu" style="width:${(100*pr.lp_max/cap).toFixed(1)}%"></i><i class="alt" style="width:${(100*alt/cap).toFixed(1)}%"></i></div><b data-lvl-zaehl="${alt}:${pr.lp_max}">${esc(pr.lp_max)}</b><em>+${esc(auf.lp)}</em></div>
   <div class="lvl-chips">${auf.ausdauer?`<span class="lvl-chip">+${esc(auf.ausdauer)} stamina</span>`:''}<span class="lvl-chip">+${auf.auf-auf.von} attribute point${auf.auf-auf.von>1?'s':''}</span>${sp?`<span class="lvl-chip gold">+${sp} skill point${sp>1?'s':''}</span>`:''}</div>
  </div>${finale?'<p class="lvl-unter">The peak of your fighting style.</p>':''}</section>`;
}
function attrStufe(pr,fx){
 const ap=pr.attributpunkte||0,traegt=id=>pr.pfade.filter(p=>p.attribut===id).map(p=>p.name);
 return `<div class="lvl-schritt"><h3>Where do you grow? <small>${ap} attribute point${ap>1?'s':''}</small></h3>
 <div class="lvl-attr">${pr.attribute.map((a,i)=>{const max=a.max||5,voll=a.wert>=max,pf=traegt(a.id);
  return `<button type="button" class="lvl-a ${fx&&fx.attr===a.id?'zuendet':''}" data-lvl-attr="${esc(a.id)}" ${busy()||voll?'disabled':''}>
   <span class="lvl-a-kopf"><b>${esc(a.label)}</b><span class="lvl-a-wert">${esc(a.wert)}${voll?'':` <i>→ ${a.wert+1}</i>`}</span></span>
   <span class="lvl-pips">${Array.from({length:max},(_,j)=>`<i class="${j<a.wert?'an':''} ${!voll&&j===a.wert?'naechst':''}"></i>`).join('')}</span>
   <span class="lvl-a-wirk">${esc(a.wirkung||'')}</span>
   ${pf.length?`<span class="lvl-a-pfad">Powers the ${pf.map(esc).join(' & ')} path</span>`:''}<span class="lvl-taste">${i+1}</span></button>`;}).join('')}</div></div>`;
}
function detail(s,pr){
 const tier=s.stufe===9?'Finisher':'Special attack',f=s.lernfolgen;
 const folgen=f&&!s.gelernt&&!s.grund?`<div class="lvl-folgen ${f.changed?'wechsel':''}"><b>${f.changed?(f.before&&f.before.name?`Main path: ${esc(f.before.name)} → ${esc(f.after.name)}`:`First main path: ${esc(f.after.name)}`):`Main path stays ${esc(f.after.name)}`}</b>${f.attributes&&f.attributes.length?`<span>${f.attributes.map(a=>`${esc(a.label)} ${esc(a.before)} → ${esc(a.after)}`).join(' · ')}</span>`:''}</div>`:'';
 const pv=window.EdenSkillPreview&&window.EdenSkills&&EdenSkills.icons&&EdenSkills.icons[s.id];
 return `<aside class="lvl-detail" style="--pc:${(PATHS[s.pfad.id]||PATHS.K).color}">
  <div class="lvl-d-kopf"><div class="lvl-d-icon">${icon(s.id)}</div><div><small>${esc(s.pfad.name)} · ${esc(s.pfad.id)}${esc(s.stufe)} · ${tier}</small><h4>${esc(s.label)}</h4><span class="lvl-kosten"><b>${esc(s.kosten)}</b> stamina</span></div></div>
  <p class="lvl-d-text">${esc(s.text)}</p>
  ${s.zahlen&&s.zahlen.length?`<ul class="lvl-d-zahlen">${s.zahlen.map(z=>`<li>${esc(z)}</li>`).join('')}</ul>`:''}
  ${s.grund&&!s.gelernt?`<p class="lvl-d-grund">${esc(s.grund)}</p>`:''}${folgen}
  <div class="lvl-d-knoepfe">${pv?`<button type="button" class="lvl-zweit" data-lvl-preview="${esc(s.id)}">▶ Animation</button>`:''}
   <button type="button" class="lvl-lernen" data-lvl-learn="${esc(s.id)}" ${s.gelernt||s.grund||!pr.skillpunkte||busy()?'disabled':''}>${s.gelernt?uiIc('done','imtext')+' Learned':s.grund?'Not available yet':!pr.skillpunkte?'No skill point left':'Burn in · 1 point'}</button></div></aside>`;
}
function baumStufe(pr,fx){
 const all=pr.pfade.flatMap(p=>p.skills.map(s=>({...s,pfad:p})));
 const frei=all.filter(s=>!s.gelernt&&!s.grund),main=pr.pfade.find(p=>p.name===pr.hauptpfad);
 let s=all.find(x=>x.id===S.sel)||(fx&&fx.learn&&all.find(x=>x.id===fx.learn))||frei.find(x=>main&&x.pfad.id===main.id)||frei[0]||all[0];
 S.sel=s.id;
 const n=pr.skillpunkte;
 const rows=pr.pfade.map(p=>{const t=PATHS[p.id]||PATHS.K,sk=[...p.skills].sort((a,b)=>a.stufe-b.stufe),gel=sk.filter(x=>x.gelernt).length,voll=sk.length&&gel===sk.length;
  return `<section class="lvl-pfad ${main&&main.id===p.id?'haupt':''} ${voll?'meister':''} ${fx&&fx.master===p.id?'wird-meister':''} ${fx&&fx.path===p.id?'glueht':''}" style="--pc:${t.color};--art:url('${artBase+esc(p.id)}.png');--pos:${t.pos}">
   <header><span class="lvl-mark">${t.mark}</span><b>${esc(p.name)}</b><small>${esc(p.attribut_label)}</small><em>${voll?uiIc('quality','imtext')+' Mastered':`${gel} / ${sk.length}`}</em></header>
   <div class="lvl-knoten-reihe">${sk.map((x,i)=>`${i?`<i class="lvl-kante ${x.gelernt?'an':''} ${fx&&fx.learn===x.id?'brennt':''}" aria-hidden="true"></i>`:''}<button type="button" class="lvl-knoten ${x.gelernt?'k-gelernt':x.grund?'k-zu':'k-frei'} ${x.id===s.id?'k-sel':''} ${fx&&fx.learn===x.id?'brennt':''}" data-lvl-sel="${esc(x.id)}" aria-pressed="${x.id===s.id}" aria-label="${esc(x.label)}, ${x.gelernt?'learned':x.grund?'locked':'ready'}">
     <span class="lvl-k-bild">${icon(x.id)}</span><span class="lvl-k-name">${esc(x.label)}</span><span class="lvl-k-zahl">${esc(x.zahl||(p.id+x.stufe))}</span></button>`).join('')}</div></section>`;}).join('');
 // Mastery (Duc 28.10.2026): IlluGen preset shield_gradient as a golden ring over the row, unclipped, with the piano hit
 const mi=fx&&fx.master?pr.pfade.findIndex(p=>p.id===fx.master):-1;
 const schild=mi>=0?`<i class="lvl-schild" style="top:${((mi+.5)*100/pr.pfade.length).toFixed(1)}%" aria-hidden="true"></i>`:'';
 return `<div class="lvl-schritt baum"><h3>${n?`${n} skill point${n>1?'s':''} – burn in a special attack`:'Your fighting style'}${pr.hauptpfad?`<small>Main path ${esc(pr.hauptpfad)}</small>`:''}</h3>
  ${fx&&fx.main?`<div class="lvl-banner"><small>Main path</small><b>${esc(fx.main.nachher)}</b>${pr.hauptpfad_info&&pr.hauptpfad_info.traits?`<span>${esc(pr.hauptpfad_info.traits.join(' '))}</span>`:''}</div>`:''}
  ${fx&&fx.master?`<div class="lvl-banner meister"><b>${uiIc('quality','imtext')} ${esc((pr.pfade.find(p=>p.id===fx.master)||{}).name)} mastered</b></div>`:''}
  <div class="lvl-baum"><div class="lvl-pfade">${rows}${schild}</div>${detail(s,pr)}</div>
  ${pr.hinweis&&n?`<p class="lvl-hinweis">${esc(pr.hinweis)}</p>`:''}</div>`;
}

function html(z,k,o){
 const pr=z.kampf_profil,e=k.ergebnis,auf=e.aufstieg,key=k.id+':'+auf.auf,finale=auf.auf>=pr.level_max;
 S.last={z,k,o};
 if(S.key!==key){clearTimeout(S.timer);S={key,intro:false,introBis:0,snap:null,sig:'',fx:null,echo:null,sel:null,baum:false,last:{z,k,o},timer:null};}
 const now=snapshot(pr),sig=JSON.stringify(now);
 if(S.snap&&sig!==S.sig){const d=diff(S.snap,now,pr);S.fx=d.fx;if(d.echo.length)S.echo=d.echo;}else S.fx=null;
 S.snap=now;S.sig=sig;
 let intro=false;
 if(!S.intro){S.intro=true;intro=!still();S.introBis=Date.now()+(finale?FINALE_MS:INTRO_MS);sfx('level_up',600);if(finale)sfx('mission_erfolg',1700);}
 else if(Date.now()<S.introBis)intro=true;              // a re-render during the intro keeps the intro running
 const fx=S.fx;
 if(fx&&fx.learn)sfx('chip_einrasten',380);
 if(fx&&fx.master)sfx('skill_gemeistert',800);           // Duc 28.10.2026: Cinematic Piano Hit, lands with the light wave
 const ap=pr.attributpunkte||0;
 if(!ap&&(pr.skillpunkte>0||gained(pr,auf)))S.baum=true;
 const schritt=ap>0?2:S.baum?3:4,stepNeu=S.schritt!==schritt;S.schritt=schritt;
 const offen=ap>0||pr.skillpunkte>0;
 const zeilen=(e.zeilen||[]).filter(t=>!/^Level \d+!/.test(t));
 const stufen=[['Level',1],['Attribute',2],['Skill',3]].filter(x=>x[1]!==3||S.baum);
 const buehne=schritt===2?attrStufe(pr,fx):schritt===3?baumStufe(pr,fx)
  :`<div class="lvl-schritt fertig"><h3>You're stronger now.</h3><p>The next skill point comes at level ${esc(((pr.skillpunkte_plan||[]).find(x=>x.level>pr.level)||{}).level||pr.level_max)}.</p></div>`;
 if(intro){setTimeout(zaehlen,0);clearTimeout(S.timer);S.timer=setTimeout(ende,Math.max(0,S.introBis-Date.now()));}
 return `<div class="lvl ${intro?'lvl-intro':''} ${finale?'lvl-finale':''} ${schritt===3?'lvl-mit-baum':''}" data-lvl role="dialog" aria-modal="true" aria-label="Level ${esc(auf.auf)}" style="--intro:${finale?FINALE_MS:INTRO_MS}ms">
 <div class="lvl-grund" aria-hidden="true"></div><div class="lvl-strahlen" aria-hidden="true"></div><div class="lvl-funken" aria-hidden="true">${'<i></i>'.repeat(finale?28:16)}</div>
 <div class="lvl-rahmen">
  <header class="lvl-kopf"><div class="lvl-ergebnis"><b>${esc(o.titel)}</b><span>${esc(e.text)}</span>${zeilen.length?`<span class="lvl-folgen-z">${zeilen.map(t=>`<i>${esc(t)}</i>`).join('')}</span>`:''}</div>
   <ol class="lvl-schritte">${stufen.map(([t,n])=>`<li class="${n<schritt?'fertig':n===schritt?'an':''}">${t}</li>`).join('')}</ol></header>
  ${held(pr,auf,finale)}
  <section class="lvl-buehne ${stepNeu?'neu':''}">${S.echo?`<div class="lvl-echo ${fx?'neu':''}">${S.echo.join('<span>·</span>')}</div>`:''}${buehne}</section>
  <footer class="lvl-fuss"><span>Duc ${uiIc('hp','imtext')} ${esc(pr.lp)}/${esc(pr.lp_max)} · ${esc(k.runde)} rounds${offen?' · Points you don\'t spend now wait for you in the Character menu.':''}</span>
   <button type="button" class="lvl-weiter ${offen?'':'bereit'}" data-lvl-weiter ${busy()?'disabled':''}>${offen?'Later · Continue':'Continue'}</button></footer>
 </div>${intro?'<p class="lvl-skip">Space · skip</p>':''}</div>`;
}
// HP counts up during the intro
function zaehlen(){
 const el=document.querySelector('.lvl.lvl-intro [data-lvl-zaehl]');if(!el)return;
 const [a,b]=el.dataset.lvlZaehl.split(':').map(Number),t0=performance.now()+700,dauer=900;
 const tick=t=>{if(!el.isConnected)return;const p=Math.max(0,Math.min(1,(t-t0)/dauer));el.textContent=Math.round(a+(b-a)*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(tick);};
 el.textContent=a;requestAnimationFrame(tick);
}
// intro over (timer) or skipped (Space/click): drop the class, the base rules are the final picture
function ende(){const el=document.querySelector('.lvl.lvl-intro');if(!el)return;el.classList.remove('lvl-intro');el.querySelector('.lvl-skip')?.remove();const z=el.querySelector('[data-lvl-zaehl]');if(z)z.textContent=z.dataset.lvlZaehl.split(':')[1];}
function skip(){S.introBis=0;clearTimeout(S.timer);ende();}
function neuZeichnen(attr,val){
 const el=document.querySelector('[data-lvl]');if(!el||!S.last)return;
 const h=document.createElement('div');h.innerHTML=html(S.last.z,S.last.k,S.last.o);const nx=h.firstElementChild;el.replaceWith(nx);
 if(attr)for(const b of nx.querySelectorAll(`[${attr}]`))if(b.getAttribute(attr)===val){b.focus({preventScroll:true});break;}
}
document.addEventListener('click',ev=>{
 const root=ev.target.closest('[data-lvl]');if(!root)return;
 if(root.classList.contains('lvl-intro')){ev.preventDefault();ev.stopPropagation();skip();return;}
 const b=ev.target.closest('button');if(!b||b.disabled||busy())return;
 const send=(a,d)=>{if(typeof senden==='function')senden(a,d,'…');};
 if(b.dataset.lvlAttr){sfx('level_up');send('attribut_steigern',{id:b.dataset.lvlAttr});}
 else if(b.dataset.lvlLearn){send('skill_lernen',{id:b.dataset.lvlLearn});}
 else if(b.dataset.lvlSel){S.sel=b.dataset.lvlSel;neuZeichnen('data-lvl-sel',S.sel);}
 else if(b.dataset.lvlPreview){const id=b.dataset.lvlPreview,s=S.last.z.kampf_profil.pfade.flatMap(p=>p.skills).find(x=>x.id===id);
  if(s&&window.EdenSkillPreview)EdenSkillPreview.open({effect:EdenSkills.icons[id],name:s.label,trigger:b});}
 else if(b.hasAttribute('data-lvl-weiter'))send('kampf_schliessen',{});
},true);
document.addEventListener('keydown',ev=>{
 const root=document.querySelector('[data-lvl]');if(!root||/INPUT|TEXTAREA/.test(ev.target.tagName||'')||document.querySelector('dialog[open]'))return;
 if(root.classList.contains('lvl-intro')){if(ev.code==='Space'||ev.key==='Enter'||ev.key==='Escape'){ev.preventDefault();ev.stopImmediatePropagation();skip();}return;}
 const n=parseInt(ev.key,10),tiles=root.querySelectorAll('[data-lvl-attr]');
 if(n&&tiles[n-1]&&!tiles[n-1].disabled){ev.preventDefault();ev.stopImmediatePropagation();tiles[n-1].click();return;}
 const sel=ev.target.closest&&ev.target.closest('[data-lvl-sel]'),off={ArrowLeft:[0,-1],ArrowRight:[0,1],ArrowUp:[-1,0],ArrowDown:[1,0]}[ev.key];
 if(sel&&off){const rows=S.last.z.kampf_profil.pfade.map(p=>[...p.skills].sort((a,b)=>a.stufe-b.stufe).map(s=>s.id));
  const r=rows.findIndex(x=>x.includes(sel.dataset.lvlSel)),c=rows[r].indexOf(sel.dataset.lvlSel);
  const t=rows[Math.max(0,Math.min(rows.length-1,r+off[0]))][Math.max(0,Math.min(3,c+off[1]))];
  if(t){ev.preventDefault();ev.stopImmediatePropagation();S.sel=t;neuZeichnen('data-lvl-sel',t);}}
},true);
window.EdenLevelUp={html,skip,_s:()=>S};
})();
