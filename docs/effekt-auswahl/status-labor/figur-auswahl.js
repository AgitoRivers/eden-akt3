/* Shared lab comparison picker. Full sets load before they replace the visible figure. */
window.EdenFigurePicker={async mount(select,{base,onChange}){
 const catalog=await fetch(base+'duc-varianten-v1/katalog.json').then(r=>{if(!r.ok)throw Error('Spritekatalog fehlt.');return r.json()});
 const options=new Map([['vergleich',{label:'Anzugfigur · Vergleich',prefix:'vergleich_',version:'?v=2'}],['bisher',{label:'Dieb · bisherige Figur',prefix:'figur_',version:''}]]);
 select.replaceChildren();
 for(const [value,item] of options){const o=document.createElement('option');o.value=value;o.textContent=item.label;select.append(o)}
 for(const [look,label] of Object.entries(catalog.looks)){
  const group=document.createElement('optgroup');group.label='Duc · '+label;
  for(const item of catalog.sets.filter(s=>s.look===look)){
   const value='duc:'+item.id;options.set(value,{label:item.label,prefix:item.directory+'gegner_',version:''});const o=document.createElement('option');o.value=value;o.textContent=catalog.weapons[item.weapon];group.append(o);
  }select.append(group);
 }
 let selected='vergleich',revision=0;try{const saved=localStorage.getItem('eden-fx-preview-figure');if(options.has(saved))selected=saved}catch{}select.value=selected;
 async function apply(persist){
  const requested=select.value,ticket=++revision,item=options.get(requested);if(!item)return;
  select.disabled=true;
  try{
   const pairs=await Promise.all(['idle','hurt','guard'].map(pose=>new Promise((resolve,reject)=>{const image=new Image();image.onload=()=>resolve([pose,image]);image.onerror=()=>reject(Error('Vorschaupose konnte nicht geladen werden.'));image.src=base+item.prefix+pose+'.webp'+item.version})));
   if(ticket!==revision)return;selected=requested;onChange(Object.fromEntries(pairs));
   if(persist)try{localStorage.setItem('eden-fx-preview-figure',selected)}catch{}
  }catch(error){if(ticket===revision)select.value=selected;throw error}
  finally{if(ticket===revision)select.disabled=false}
 }
 select.onchange=()=>apply(true).catch(error=>{const message=document.querySelector('#error');if(message)message.textContent=error.message});
 await apply(false);
}};
