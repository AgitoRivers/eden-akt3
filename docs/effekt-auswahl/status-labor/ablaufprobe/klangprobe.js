/* Laboratory controls only. ton-abspieler.js remains DOM-free and usable in the game parent. */
(()=>{'use strict';
 const host=document.createElement('section');host.className='sound-study';host.setAttribute('aria-label','Klangprobe');
 host.innerHTML='<button type="button" id="sound-toggle" aria-pressed="false">Ton aktivieren</button><label>Lautstärke <input id="sound-volume" type="range" min="0" max="100" value="65" aria-label="Sound-Lautstärke"></label><label>Klangfassung <select id="sound-version" aria-label="Klangfassung"><option value="approved">Bisherige Mischung</option><option value="library">Bibliotheksprobe</option></select></label><span id="sound-status" role="status">20 Spezialattacken · Heiler-Ton als Entwurf · Ton aus</span>';
 document.querySelector('.controls').after(host);
 const style=document.createElement('style');style.textContent='.sound-study{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin:10px 0 16px;padding:12px;border:1px solid #4b535a;border-radius:9px;background:#182126}.sound-study label{font-size:13px}.sound-study input{width:110px}.sound-study span{font-size:12px;color:#b9c8ca}.sound-study button[aria-pressed=true]{border-color:#d8bd82;color:#f5dca8}';document.head.append(style);
 const toggle=host.querySelector('#sound-toggle'),volume=host.querySelector('#sound-volume'),status=host.querySelector('#sound-status'),baseUrl=new URL('../',location.href).href;
 let context,master,enabled=false,handle=null,last=null,active=null,serial=0,starts=0;
 const baseline=window.EDEN_ATTACK_SOUND_CUES,version=host.querySelector('#sound-version');let trialPromise=null,switching=false,versionRequest=0;
 async function changeVersion(){const request=++versionRequest;switching=true;stop();status.textContent='Klangfassung wird geladen …';try{if(version.value==='library'){if(!trialPromise)trialPromise=fetch(new URL('ton-bibliothek-v1.json',baseUrl)).then(r=>{if(!r.ok)throw Error(r.status);return r.json()});const trial=await trialPromise;if(request!==versionRequest)return;window.EDEN_ATTACK_SOUND_CUES={...baseline,sounds:{...baseline.sounds,...trial.sounds},attacks:{...baseline.attacks,...trial.attacks}}}else window.EDEN_ATTACK_SOUND_CUES=baseline;if(request!==versionRequest)return;switching=false;stop();status.textContent=version.value==='library'?'Bibliotheksprobe · noch nicht freigegeben':'Bisherige Mischung';if(last)document.querySelector('#restart').click()}catch(_){if(request!==versionRequest)return;trialPromise=null;switching=false;version.value='approved';window.EDEN_ATTACK_SOUND_CUES=baseline;status.textContent='Bibliotheksprobe nicht verfügbar · bisherige Mischung bleibt aktiv'}}
 version.onchange=changeVersion;
 function stop(){serial++;handle?.stop();handle=null;active=null}
 function sync(s){
  last=s;if(switching||!enabled||!context)return;
  if(s.paused||!s.shown||document.hidden){stop();status.textContent=s.paused?'Ton bereit · pausiert':'Ton aus · Effekte oder Seite ausgeblendet';return}
  const timeline=window.EdenAttackStudy?.soundTimeline();if(!timeline)return;
  const key=JSON.stringify([s.attack,s.variant,s.mode,timeline]);
  if(active){const expected=active.offset+(context.currentTime-active.at)*active.speed;if(active.key===key&&active.speed===s.speed&&Math.abs(expected-s.time)<.13)return}
  stop();const run=serial;
  try{
   const at=context.currentTime;
   handle=window.EdenAttackSound.play({attack:s.attack,variant:s.variant,context,destination:master,startAt:at,baseUrl,timeline,mode:s.mode,offset:s.time,speed:s.speed});
   active={key,at,offset:s.time,speed:s.speed};starts++;status.textContent=(version.value==='library'?'PROBE · ':'Ton läuft · ')+window.EDEN_ATTACK_SOUND_CUES.attacks[s.attack].name;
   handle.ready.catch(()=>{if(run!==serial)return;stop();status.textContent='Ton konnte nicht geladen werden · erneut aktivieren'});
  }catch(_){stop();status.textContent='Ton nicht verfügbar'}
 }
 toggle.addEventListener('click',async()=>{
  enabled=!enabled;toggle.setAttribute('aria-pressed',String(enabled));toggle.textContent=enabled?'Ton an':'Ton aktivieren';stop();
  if(!enabled){status.textContent='Ton aus';return}
  const run=serial;
  try{
   if(!context){context=new AudioContext();master=context.createGain();master.gain.value=Number(volume.value)/100;master.connect(context.destination)}
   await context.resume();if(!last)return;
   const s={...last};status.textContent='Bestätigte Sounds werden geladen …';
   await window.EdenAttackSound.preload({attack:s.attack,variant:s.variant,context,baseUrl,timeline:window.EdenAttackStudy?.soundTimeline(),mode:s.mode});
   if(!enabled||serial!==run)return;
   document.querySelector('#restart').click();if(document.querySelector('#play').textContent==='Abspielen')document.querySelector('#play').click();
  }catch(_){if(serial!==run)return;enabled=false;stop();toggle.setAttribute('aria-pressed','false');toggle.textContent='Ton aktivieren';status.textContent='Ton konnte nicht geladen werden'}
 });
 volume.addEventListener('input',()=>{if(master)master.gain.setTargetAtTime(Number(volume.value)/100,context.currentTime,.025)});
 document.addEventListener('visibilitychange',()=>{if(document.hidden)stop()});
 window.addEventListener('pagehide',()=>{enabled=false;stop();context?.close()});
 window.EdenAttackAudio={sync,inspect:()=>({version:version.value,switching,enabled,playing:!!handle&&!handle.inspect().stopped,starts,contextState:context?.state??'not-created',active:handle?.inspect()??null})};
 if(new URLSearchParams(location.search).get('klang')==='bibliothek-v1'){version.value='library';changeVersion()}
})();
