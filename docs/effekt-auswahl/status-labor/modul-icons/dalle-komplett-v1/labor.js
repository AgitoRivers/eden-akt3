'use strict';
let catalog,mode='chips',selected=null;
const $=s=>document.querySelector(s);
const tierLabels={bronze:'Bronze',silver:'Silber',gold:'Gold'};
const extraLabels={element:'Element · allgemein',abwehr:'Resistenz · allgemein',zustand_welle:'Welle · Reserve',zustand:'Zustand · allgemein'};
function cat(id){return catalog.categories.find(c=>c.id===id)}
function showDetail(item){
 selected=item.id+'-'+item.level;
 const category=cat(item.category),img=$('#detail-image');img.hidden=false;img.src=item.file;img.alt=item.label;
 $('#detail-meta').textContent=(item.group==='waffe'?'WAFFENMODUL':'JACKENMODUL')+' · '+tierLabels[item.tier];
 $('#detail-name').textContent=item.label;
 $('#detail-category').textContent=(category?.label||item.category)+' · Stufe '+item.level+' · '+item.level+'/3 Leuchten';
 $('#detail-effect').textContent=item.effect||'Kategoriezeichen zur Orientierung. Kein zusätzlicher Spielgegenstand.';
 $('.detail').style.setProperty('--category',category?.color||'#b697db');
 const link=$('#detail-download');link.href=item.file;link.download=item.file.split('/').pop();
 document.querySelectorAll('.card').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.key===selected)));
}
function data(){
 if(mode==='chips')return catalog.chips.map(c=>({id:c.id,label:c.label,file:c.file,level:c.stufe,tier:c.tier,group:c.gruppe,category:c.kategorie,effect:c.text}));
 if(mode==='categories')return catalog.categories.map(c=>({...c,category:c.id}));
 return catalog.art.filter(a=>a.source.endsWith('kategorie-zusatz.png')).map(a=>({id:a.family,label:extraLabels[a.family],file:a.file,level:a.level,tier:a.tier,group:a.family==='abwehr'?'jacke':'waffe',category:a.family==='zustand_welle'?'zustand':a.family,effect:a.family==='zustand_welle'?'Gestaltungsreserve: Wellenzeichen. Aktuell keinem Spielmodul zugeordnet.':'Allgemeines Kategoriezeichen. Die Spielmodule stehen unter „Alle 72 Module“.'}));
}
function render(){
 const grid=$('#grid');grid.replaceChildren();grid.classList.toggle('sheets',mode==='sheets');
 $('.filters').hidden=mode==='sheets';$('#empty').hidden=true;
 if(mode==='sheets'){
  for(const s of catalog.sources){const card=document.createElement('article');card.className='sheet';const img=document.createElement('img');img.src='raster/'+s.id+'.png';img.alt=s.id;img.width=256;img.height=192;const title=document.createElement('h3');title.textContent=s.id.replaceAll('-',' ');card.append(img,title);for(const [file,label] of [['raster/'+s.id+'.png','64-px-Raster ↓'],[s.file,'Master ↓']]){const a=document.createElement('a');a.href=file;a.download='';a.textContent=label;a.style.marginRight='16px';card.append(a)}grid.append(card)}
  $('#count').textContent='7 Raster · je vier Familien × drei Stufen';return;
 }
 const search=$('#search').value.trim().toLocaleLowerCase('de'),group=$('#group').value,level=$('#level').value;
 const list=data().filter(c=>(group==='all'||c.group===group)&&(level==='all'||String(c.level)===level)&&(!search||(c.label+' '+c.category+' '+(cat(c.category)?.label||'')).toLocaleLowerCase('de').includes(search)));
 $('#count').textContent=list.length+' Icons · Zielgröße 64 × 64 px';$('#empty').hidden=!!list.length;
 for(const c of list){const b=document.createElement('button');b.className='card';b.dataset.key=c.id+'-'+c.level;b.setAttribute('aria-pressed',String(b.dataset.key===selected));const img=document.createElement('img');img.src=c.file;img.alt='';img.width=64;img.height=64;const title=document.createElement('strong');title.textContent=c.label;const tier=document.createElement('small');tier.textContent=tierLabels[c.tier]+' · '+c.level+'/3';b.append(img,title,tier);b.onclick=()=>showDetail(c);grid.append(b)}
 if(list.length&&!list.some(c=>c.id+'-'+c.level===selected))showDetail(list[0]);
}
document.querySelectorAll('[data-mode]').forEach(b=>b.onclick=()=>{mode=b.dataset.mode;document.querySelectorAll('[data-mode]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));render()});
for(const id of ['group','level'])$('#'+id).onchange=render;
$('#search').oninput=render;
$('#size').onchange=e=>document.documentElement.style.setProperty('--icon-size',e.target.value+'px');
fetch('katalog.json').then(r=>{if(!r.ok)throw Error(r.status);return r.json()}).then(c=>{catalog=c;render()}).catch(e=>{$('#count').textContent='Katalog konnte nicht geladen werden: '+e.message});
