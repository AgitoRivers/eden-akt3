/* Player controls only. No learning, choice persistence or engine actions. */
(()=>{'use strict';
const attack=new URLSearchParams(location.search).get('angriff');
const notify=type=>{if(parent!==window)parent.postMessage({type,attack},location.origin)};
const error=document.querySelector('#error');
new MutationObserver(()=>{if(error.textContent.trim())notify('eden-skill-preview-error')}).observe(error,{childList:true,subtree:true,characterData:true});
document.addEventListener('eden-preview-ready',()=>{
 const selection=window.EdenAttackStudy.selection(),choice=window.EDEN_APPROVED_ANIMATIONS?.choices[selection.attack];
 const caption=document.createElement('p');caption.className='preview-caption';caption.textContent=choice?'Freigegeben: '+choice.name+' · '+choice.variantName:'Animationsvorschau';document.querySelector('main').append(caption);
 const restart=document.querySelector('#restart'),play=document.querySelector('#play'),nativeRestart=restart.onclick,nativePlay=play.onclick;
 restart.onclick=()=>{nativeRestart();if(play.textContent==='Abspielen')nativePlay()};
 play.onclick=()=>{if(play.textContent==='Abspielen'&&Number(document.querySelector('#timeline').value)>=Number(document.querySelector('#timeline').max)-.1)nativeRestart();nativePlay()};
 notify('eden-skill-preview-ready');
});
document.addEventListener('visibilitychange',()=>{if(document.hidden&&document.querySelector('#play').textContent==='Pause')document.querySelector('#play').click()});
document.addEventListener('keydown',event=>{if(event.key==='Escape'){event.preventDefault();notify('eden-skill-preview-close')}});
})();
