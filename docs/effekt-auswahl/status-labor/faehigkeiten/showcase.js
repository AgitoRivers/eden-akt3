/* Local snapshots calculated in an isolated copy by the real engine functions. */
(()=>{'use strict';
const source=window.EDEN_SKILL_DEMO;let current;
const clone=value=>JSON.parse(JSON.stringify(value));
function draw(){document.querySelector('#skill-mount').innerHTML=EdenSkills.html({kampf_profil:current})}
function reset(){current=clone(source.profiles[source.scenarios[document.querySelector('#demo-state').value]]);draw();document.querySelector('#demo-message').textContent='UI-Vorschau mit Beispieldaten. Dein Spielstand bleibt unberührt.'}
window.senden=(action,{id})=>{
 if(action!=='skill_lernen')return;
 const skills=current.pfade.flatMap(p=>p.skills),selected=skills.find(s=>s.id===id);
 if(!selected||selected.gelernt||selected.grund||current.skillpunkte<1)return;
 const learned=skills.filter(s=>s.gelernt).map(s=>s.id);learned.push(id);
 const next=source.profiles[current.level+':'+learned.sort().join(',')];if(!next)return;
 current=clone(next);draw();document.querySelector('#demo-message').textContent=selected.label+' in der Vorschau gelernt. Nur die Beispieldaten wurden verändert.';
};
document.querySelector('#demo-state').addEventListener('change',reset);document.querySelector('#demo-reset').addEventListener('click',reset);reset();
})();
