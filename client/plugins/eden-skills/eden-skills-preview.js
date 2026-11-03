/* On-demand, read-only playback of the approved effect-lab variant. */
(()=>{'use strict';
const script=document.currentScript;
const root=new URL(script.dataset.previewRoot||'preview/',script.dataset.previewRoot?document.baseURI:script.src);
let modal=null;
function close(){if(!modal)return;const {dialog,frame,trigger,timer}=modal;clearTimeout(timer);modal=null;frame.src='about:blank';dialog.close();dialog.remove();if(trigger?.isConnected)trigger.focus({preventScroll:true})}
function open({effect,name,trigger}){
 if(!effect||!/^[A-Za-z]+$/.test(effect))return;
 close();
 const dialog=document.createElement('dialog');dialog.className='es-preview-dialog';dialog.setAttribute('aria-labelledby','es-preview-title');
 const header=document.createElement('header'),title=document.createElement('h2'),button=document.createElement('button');title.id='es-preview-title';title.textContent=name+' · Animation';button.type='button';button.className='es-preview-close';button.textContent='Close';button.onclick=close;header.append(title,button);
 const status=document.createElement('p');status.className='es-preview-status';status.setAttribute('role','status');status.textContent='Loading animation …';
 const frame=document.createElement('iframe');frame.title='Animation preview: '+name;frame.setAttribute('sandbox','allow-scripts allow-same-origin');frame.setAttribute('allow','autoplay');
 const footer=document.createElement('p');footer.className='es-preview-note';footer.textContent='Approved animation · uses no stamina and takes no turn.';
 dialog.append(header,status,frame,footer);document.body.append(dialog);
 const target=new URL('ablaufprobe/skill-preview.html',root);target.searchParams.set('angriff',effect);target.searchParams.set('einmal','1');
 const timer=setTimeout(()=>{if(modal?.dialog===dialog)status.textContent='This is taking longer than usual. You can close the preview and open it again.'},30000);
 modal={dialog,frame,trigger,status,effect,timer};
 dialog.addEventListener('cancel',event=>{event.preventDefault();close()});dialog.addEventListener('click',event=>{if(event.target===dialog){const b=dialog.getBoundingClientRect();if(event.clientX<b.left||event.clientX>b.right||event.clientY<b.top||event.clientY>b.bottom)close()}});
 dialog.addEventListener('keydown',event=>{if(event.key==='Escape'){event.preventDefault();event.stopPropagation();close()}});
 dialog.showModal();frame.src=target.href;button.focus();
}
window.addEventListener('message',event=>{
 if(!modal||event.origin!==location.origin||event.source!==modal.frame.contentWindow)return;
 if(event.data?.type==='eden-skill-preview-close'){close();return}
 if(event.data?.attack!==modal.effect)return;
 if(event.data?.type==='eden-skill-preview-ready'){clearTimeout(modal.timer);modal.status.textContent='';modal.status.hidden=true}
 if(event.data?.type==='eden-skill-preview-error'){clearTimeout(modal.timer);modal.status.hidden=false;modal.status.textContent='The animation could not be loaded. Please close the preview and try again.'}
});
window.EdenSkillPreview={open,close};
})();
