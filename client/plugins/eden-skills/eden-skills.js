/* Presentation only. Learning, prerequisites and forecasts come from the engine. UI text English (25.10.2026). */
(()=>{'use strict';
const base=new URL('icons/',document.currentScript.src).href,artBase=new URL('paths/',document.currentScript.src).href;
const icons={mistral:'mistral',ressac:'wave',libeccio:'wind',lame_de_fond:'tidal',doppio_gioco:'doubleSlash',sotto_voce:'blur',vendetta:'vendetta',omerta:'blackSlash',point_de_mire:'reticle',bonaccia:'calm',phare:'beam',pluie_d_etoiles:'rain',scirocco:'scirocco',retour:'retour',furia:'furia',vulcano:'vulcano',elicriso:'balm',ponente:'westWind',risveglio:'awaken',arcangelo:'archangel'};
const guide=window.EdenSkillGuide?.skills||{};
const paths={K:{color:'#94bfc8',short:'Wind & Water',mark:'I',pos:'center 42%'},L:{color:'#c2a0e5',short:'Cunning & Precision',mark:'II',pos:'center'},W:{color:'#80c8ba',short:'Focus & Control',mark:'III',pos:'center 30%'},M:{color:'#ec9270',short:'Embers & Release',mark:'IV',pos:'center 20%'},H:{color:'#9fd6a6',short:'Herbs & Grace',mark:'V',pos:'center 62%'}};
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let selected='omerta',detailTab='effect',latest=null,mastered=null,fresh=new Set();
// A path is mastered when all its skills are learned. The moment (glow, sound) plays once, when it happens in this session.
function mastery(p){
 const now=new Set(p.pfade.filter(pf=>pf.skills.length&&pf.skills.every(s=>s.gelernt)).map(pf=>pf.id));
 if(mastered){const neu=[...now].filter(id=>!mastered.has(id));if(neu.length){neu.forEach(id=>fresh.add(id));setTimeout(()=>{if(window.EdenSfx)try{EdenSfx.play('mission_erfolg')}catch(e){}},350);setTimeout(()=>{neu.forEach(id=>fresh.delete(id))},4000);}}
 mastered=now;return now;
}
function numbers(s,p){
 if(!s.zahlen?.length)return '';const b=p.zahlen_basis||{};
 return `<div class="es-numbers"><h5>With you right now</h5><ul>${s.zahlen.map(z=>`<li>${esc(z)}</li>`).join('')}</ul><small>${b.waffe?`${esc(b.waffe)} · Strength ${esc(b.staerke)} · Perception ${esc(b.wahrnehmung)} · ${esc(b.lp_max)} max HP. `:''}Against an unarmoured enemy, without crits.</small></div>`;
}
const busy=()=>typeof beschaeftigt!=='undefined'&&beschaeftigt;
const state=s=>s.gelernt?'learned':s.grund?'locked':'available';
const status=s=>s.gelernt?'Learned':s.grund?'Locked':'Ready';
function iconHtml(id,cls=''){return icons[id]?`<img class="eden-skill-art ${esc(cls)}" src="${base+icons[id]}.png" alt="" width="305" height="305" draggable="false">`:''}
function progressionHelp(p){
 const schedule=(p.skillpunkte_plan||[]).map(x=>`Lv ${esc(x.level)}: ${esc(x.punkte)} point${x.punkte===1?'':'s'}`).join(' · ');
 return `<details class="es-help"><summary>Points & rules <span aria-hidden="true">?</span></summary><div class="es-help-card"><section><h5>Skill points</h5><p>${p.skillpunkte_gesamt!=null?`<b>${esc(p.skillpunkte_gesamt)} skill points</b> in total up to level ${esc(p.level_max)}. `:''}Every skill costs one point.</p><p class="es-point-plan">${schedule}</p></section><section><h5>Progression</h5><p>Each path runs from left to right. A higher skill needs the one before it on the same path. You can spread your points across several paths.</p></section><section><h5>Main path</h5><p>The path with the most learned skills decides which attribute grows and which path traits apply. What learning changes is shown above the learn button. Your equipped weapon stays the same.</p></section><section><h5>Codes & ties</h5><p>${p.pfade.map(pf=>`<b>${esc(pf.id)}</b> = ${esc(pf.name)}`).join(' · ')}. The number is the path tier.</p>${p.hauptpfad_prioritaet?.length?`<p>On a tie: ${p.hauptpfad_prioritaet.map(esc).join(' → ')}.</p>`:''}</section></div></details>`;
}
function learningImpact(s){
 const f=s.lernfolgen;if(!f||s.gelernt||s.grund)return '';
 const heading=f.changed?(f.before?.name?`${esc(f.before.name)} → ${esc(f.after.name)}`:`First main path: ${esc(f.after.name)}`):`Main path stays ${esc(f.after.name)}`;
 return `<div class="es-learning-impact ${f.changed?'is-change':''}"><strong>${f.changed?'Main path: ':''}${heading}</strong>${f.attributes?.length?`<p>${f.attributes.map(a=>`${esc(a.label)} <b>${esc(a.before)} → ${esc(a.after)}</b>`).join(' · ')}</p>`:''}${f.changed?`<p>${esc(f.after.summary||f.after.traits?.join(' ')||'')}</p>${f.tie?'<small>The new main path wins the tie.</small>':''}`:''}</div>`;
}
function html(z){
 latest=z;const p=z?.kampf_profil;
 if(!p)return '<p class="leer">This adventure has no skill paths.</p>';
 const all=p.pfade.flatMap(pf=>pf.skills.map(s=>({...s,path:pf})));
 const s=all.find(s=>s.id===selected)||all.find(s=>!s.gelernt&&!s.grund)||all[0];
 if(!s)return '<p class="leer">No skills yet.</p>';
 selected=s.id;const theme=paths[s.path.id]||paths.K,tip=guide[s.id];
 const previous=s.path.skills.filter(x=>x.stufe<s.stufe).sort((a,b)=>b.stufe-a.stufe)[0];
 const progress=p.level>=p.level_max?100:Math.max(0,Math.min(100,100*p.xp/Math.max(1,p.xp_next)));
 const tabs=[['effect','Effect'],['combo','Combos'],['path','Path']],done=mastery(p);
 return `<section class="eden-skills" aria-label="Skill tree" style="--skill-accent:${theme.color}">
 <div class="es-commandbar"><h3>Skills</h3><div class="es-progress"><span>LEVEL <b>${esc(p.level)}</b><small>/ ${esc(p.level_max)}</small></span><div class="es-xp" role="progressbar" aria-label="Experience to the next level" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${Math.round(progress)}"><i style="width:${progress}%"></i></div><span class="es-experience">${p.level>=p.level_max?'Max level':`${esc(p.xp)} / ${esc(p.xp_next)} XP`}</span><span class="es-main">Main path <b>${esc(p.hauptpfad||'Not yet')}</b></span></div><div class="es-points"><strong>${esc(p.skillpunkte)}</strong><span>skill point${p.skillpunkte===1?'':'s'} free</span></div>${progressionHelp(p)}</div>
 <div class="es-layout"><div class="es-tree" aria-label="Skill paths"><div class="es-board-caption"><span>FIVE PATHS · YOUR FIGHTING STYLE</span><span>Opener <i aria-hidden="true">→</i> Finisher</span></div><div class="es-columns">${p.pfade.map(pf=>{
  const t=paths[pf.id]||paths.K,learned=pf.skills.filter(n=>n.gelernt).length,full=done.has(pf.id);
  return `<section class="es-path ${pf.id===s.path.id?'is-active':''} ${full?'is-mastered':''} ${fresh.has(pf.id)?'just-mastered':''}" data-skill-row="${esc(pf.id)}" style="--path-color:${t.color};--path-art:url('${artBase+esc(pf.id)}.png');--art-pos:${t.pos}" aria-label="${esc(pf.name)}${full?', mastered':''}"><header class="es-path-heading"><span class="es-path-number">${t.mark}</span><h4>${esc(pf.name)}</h4><p>${esc(pf.attribut_label)}</p>${full?'<small class="es-mastered">'+uiIc('quality','imtext')+' Mastered</small>':`<small>${learned} / ${pf.skills.length} learned</small>`}</header><div class="es-nodes">${[...pf.skills].sort((a,b)=>a.stufe-b.stufe).map(n=>`<button type="button" class="es-node ${state(n)} ${n.id===selected?'is-selected':''}" data-skill-select="${esc(n.id)}" aria-pressed="${n.id===selected}" aria-label="${esc(n.label)}, path tier ${esc(n.stufe)}, ${status(n)}${n.zahl?', '+esc(n.zahl):''}"><span class="es-node-image">${iconHtml(n.id)}<span class="es-node-state" aria-hidden="true">${n.gelernt?uiIc('done','imtext'):n.grund?'·':'+'}</span></span><span class="es-node-label"><strong>${esc(n.label)}</strong></span></button>`).join('')}</div></section>`;
 }).join('')}</div><div class="es-legend"><span><i class="learned"></i> Learned</span><span><i class="available"></i> Ready</span><span><i class="locked"></i> Locked</span><small>← → ↑ ↓ select · Enter confirm</small></div></div>
 <aside class="es-detail" aria-label="Selected skill"><div class="es-detail-scroll"><div class="es-detail-top"><span>${esc(s.path.name)} · ${esc(s.path.id)}${esc(s.stufe)}</span><span class="es-status ${state(s)}">${status(s)}</span></div><div class="es-detail-identity"><div class="es-hero">${iconHtml(s.id)}</div><div class="es-detail-title"><small>${s.stufe===9?'FINISHER':'SPECIAL ATTACK'}</small><h4>${esc(s.label)}</h4>${tip?`<p class="es-purpose">${esc(tip.short)}</p>`:''}<div class="es-cost"><b>${esc(s.kosten)}</b> stamina <span>·</span> ${esc(s.path.attribut_label)}</div></div></div>
 <div class="es-detail-tabs" role="tablist" aria-label="Skill information">${tabs.map(([id,label])=>`<button type="button" role="tab" id="es-tab-${id}" aria-controls="es-panel-${id}" aria-selected="${detailTab===id}" data-skill-tab="${id}">${label}</button>`).join('')}</div><div class="es-detail-panels">
 <section class="es-info-panel" id="es-panel-effect" role="tabpanel" aria-labelledby="es-tab-effect" ${detailTab!=='effect'?'hidden':''}><div class="es-effect"><h5>Effect</h5><p>${esc(s.text)}</p></div>${numbers(s,p)}<div class="es-requirement"><h5>${s.gelernt?'Unlocked':'Requirement'}</h5><p>${previous?`${esc(previous.label)} on the same path`:'Opener of this path'}${!s.gelernt?' · 1 free skill point':''}</p>${s.grund&&!s.gelernt?`<p class="es-reason">${esc(s.grund)}</p>`:''}</div></section>
 <section class="es-info-panel" id="es-panel-combo" role="tabpanel" aria-labelledby="es-tab-combo" ${detailTab!=='combo'?'hidden':''}><div class="es-combo"><h5>Combos</h5><p>${esc(tip?.combo||'There is no combo tip for this skill yet.')}</p></div>${p.hinweis&&s.path.id==='L'?`<aside class="es-build-hint"><strong>Your fighting style</strong><span>${esc(p.hinweis)}</span></aside>`:''}</section>
 <section class="es-info-panel" id="es-panel-path" role="tabpanel" aria-labelledby="es-tab-path" ${detailTab!=='path'?'hidden':''}><h5>Your main path</h5><p><b>${esc(p.hauptpfad_info?.name||'Not yet')}</b></p><p>${esc(p.hauptpfad_info?.traits?.join(' ')||'Your first learned skill sets your first main path.')}</p><p>The path with the most learned skills wins. What this choice changes is shown below, before you learn it.</p>${p.hauptpfad_prioritaet?.length?`<p class="es-tie-rule">Tie: ${p.hauptpfad_prioritaet.map(esc).join(' → ')}.</p>`:''}</section></div></div>
 <div class="es-actions">${learningImpact(s)}<div class="es-action-buttons">${icons[s.id]&&window.EdenSkillPreview?`<button type="button" class="es-preview-button" data-skill-preview="${esc(s.id)}">▶ Animation</button>`:''}<button type="button" class="es-learn" data-skill-learn="${esc(s.id)}" ${s.gelernt||s.grund||busy()?'disabled':''}>${s.gelernt?uiIc('done','imtext')+' Already learned':s.grund?'Not available yet':'Learn · 1 point'}</button></div><p class="es-footer-note">${s.gelernt?'Already part of your fighting style.':'Learning uses one skill point.'}</p></div></aside></div></section>`;
}
function replace(root,focusAttr,focusValue){
 const holder=document.createElement('div');holder.innerHTML=html(latest);const next=holder.firstElementChild;root.replaceWith(next);
 for(const el of next.querySelectorAll(`[${focusAttr}]`))if(el.getAttribute(focusAttr)===focusValue){el.focus({preventScroll:true});break;}
}
document.addEventListener('click',event=>{
 const button=event.target.closest('button[data-skill-select],button[data-skill-learn],button[data-skill-preview],button[data-skill-tab]');
 if(!event.target.closest('.es-help'))document.querySelectorAll('.eden-skills .es-help[open]').forEach(el=>el.open=false);
 const root=button?.closest('.eden-skills');if(!root||!latest)return;
 const all=latest.kampf_profil.pfade.flatMap(p=>p.skills);
 if(button.hasAttribute('data-skill-preview')){const id=button.dataset.skillPreview,s=all.find(s=>s.id===id);if(s&&window.EdenSkillPreview)EdenSkillPreview.open({effect:icons[id],name:s.label,trigger:button});return;}
 if(button.hasAttribute('data-skill-learn')){const id=button.dataset.skillLearn,s=all.find(s=>s.id===id);if(!s||s.gelernt||s.grund||busy()||button.disabled)return;if(window.EdenSfx)try{EdenSfx.play('level_up')}catch(e){}if(typeof senden==='function')senden('skill_lernen',{id},'Learning skill …');return;}
 if(button.hasAttribute('data-skill-tab')){detailTab=button.dataset.skillTab;replace(root,'data-skill-tab',detailTab);return;}
 selected=button.dataset.skillSelect;detailTab='effect';replace(root,'data-skill-select',selected);
});
// Darueberfahren zeigt die Details sofort: im Baum stehen nur Bild und Name (Duc 31.10.2026)
document.addEventListener('mouseover',event=>{
 const node=event.target.closest?.('.eden-skills [data-skill-select]');if(!node||!latest||node.dataset.skillSelect===selected)return;
 selected=node.dataset.skillSelect;detailTab='effect';replace(node.closest('.eden-skills'),'data-skill-select',selected);
});
document.addEventListener('keydown',event=>{
 const node=event.target.closest('.eden-skills [data-skill-select]');if(!node||!latest)return;
 const offsets={ArrowLeft:[0,-1],ArrowRight:[0,1],ArrowUp:[-1,0],ArrowDown:[1,0]},offset=offsets[event.key];if(!offset)return;
 const rows=latest.kampf_profil.pfade.map(p=>[...p.skills].sort((a,b)=>a.stufe-b.stufe));
 const row=rows.findIndex(r=>r.some(s=>s.id===node.dataset.skillSelect)),col=rows[row].findIndex(s=>s.id===node.dataset.skillSelect);
 const target=rows[Math.max(0,Math.min(rows.length-1,row+offset[0]))]?.[Math.max(0,Math.min(rows[row].length-1,col+offset[1]))];if(!target)return;
 event.preventDefault();event.stopPropagation();selected=target.id;detailTab='effect';replace(node.closest('.eden-skills'),'data-skill-select',selected);
});
window.EdenSkills={html,iconHtml,icons};
})();
