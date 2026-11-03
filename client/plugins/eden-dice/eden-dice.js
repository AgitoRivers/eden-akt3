/* Eden Dice 1.0.0. Display only: never generates a random result or applies game effects. */
(function(global){
 'use strict';
 const scriptURL=document.currentScript&&document.currentScript.src;
 const options=Object.assign({assetBase:scriptURL?new URL('assets/',scriptURL).href:'/plugins/eden-dice/assets/',compactMs:800,largeMs:1950},global.EdenDiceOptions||{});
 const motion=matchMedia('(prefers-reduced-motion: reduce)');
 const cache=new Map(),seen=new Set();let chain=Promise.resolve(),active=null,generation=0;
 const labels={charm:'Charm',empathy:'Empathy',perception:'Perception',cunning:'Cunning',courage:'Courage',strength:'Strength'};
 const names={erfolg:'Success',fehlschlag:'Failure',kritisch:'Critical success',patzer:'Critical failure'};
 const asset=name=>new URL(name,new URL(options.assetBase.endsWith('/')?options.assetBase:options.assetBase+'/',document.baseURI)).href;
 function normalise(p){
   if(!p||!Number.isInteger(p.wurf)||p.wurf<1||p.wurf>20||!Number.isFinite(p.sg)||!Number.isFinite(p.summe))throw new TypeError('Invalid dice check');
   const dice=Array.isArray(p.wuerfe)&&p.wuerfe.length?p.wuerfe:[p.wurf];
   if(dice.length>2||dice.some(n=>!Number.isInteger(n)||n<1||n>20)||Math.max(...dice)!==p.wurf)throw new TypeError('Invalid advantage dice');
   const bonuses=Array.isArray(p.boni)?p.boni:[];
   if(bonuses.some(b=>!Array.isArray(b)||!Number.isFinite(b[1])))throw new TypeError('Invalid bonuses');
   return {wurf:p.wurf,wuerfe:dice.slice(),sg:p.sg,summe:p.summe,boni:bonuses.map(b=>[String(b[0]),b[1]]),attribut:String(p.attribut||''),ergebnis:String(p.ergebnis||'')};
 }
 function load(name){
   if(cache.has(name))return cache.get(name);
   const promise=new Promise(resolve=>{const image=new Image();let done=false;const finish=value=>{if(done)return;done=true;clearTimeout(timer);image.onload=image.onerror=null;resolve(value);};const timer=setTimeout(()=>finish(null),1800);image.onload=()=>finish(image);image.onerror=()=>finish(null);image.src=asset(name);});cache.set(name,promise);return promise;
 }
 function filename(value){return value===1?'critical-failure.webp':value===20?'critical-success.webp':'d20_'+value+'.webp';}
 function paint(canvas,value,image,frame=17,rolling=false){
   const c=canvas.getContext('2d'),size=canvas.width;c.clearRect(0,0,size,size);
   if(image){if(rolling||value!==1&&value!==20){const cols=rolling?8:5,cell=image.width/cols;c.drawImage(image,frame%cols*cell,Math.floor(frame/cols)*cell,cell,cell,0,0,size,size);}else c.drawImage(image,0,0,size,size);}
   else{c.fillStyle=getComputedStyle(canvas).color||'#f3eee4';c.font='500 '+Math.round(size*.38)+'px monospace';c.textAlign='center';c.textBaseline='middle';c.fillText(rolling?'…':String(value),size/2,size/2);}
 }
 function element(tag,className,text){const node=document.createElement(tag);if(className)node.className=className;if(text!==undefined)node.textContent=text;return node;}
 function remember(id){seen.add(id);if(seen.size>1000)seen.delete(seen.values().next().value);}
 function build(probe,large,title,target){
   const wrap=element('div',large?'eden-dice-layer':'eden-dice-card');let content=wrap,stage=wrap;
   const skip=element('button','ed-skip','Skip');skip.type='button';
   if(large){wrap.setAttribute('role','dialog');wrap.setAttribute('aria-modal','true');wrap.setAttribute('aria-label','Dice check');content=element('div','ed-sheet');wrap.append(content);const head=element('header');head.append(element('h2','',title||'Dice check'),skip);stage=element('div','ed-stage');content.append(head,stage);stage.append(element('span','ed-label',(labels[probe.attribut]||probe.attribut)+' · DC '+probe.sg));}
   else{wrap.setAttribute('role','group');wrap.setAttribute('aria-label','Dice check');}
   const dice=element('div','ed-dice'),canvases=probe.wuerfe.map(()=>{const canvas=element('canvas','ed-die');canvas.width=canvas.height=512;canvas.setAttribute('role','img');canvas.setAttribute('aria-label','Rolling the D20');dice.append(canvas);return canvas;});
   if(probe.wuerfe.length===2){stage.classList.add('ed-advantage');wrap.classList.add('ed-advantage');}
   const values=element('div','ed-values');if(!large)values.append(element('span','ed-label',(labels[probe.attribut]||probe.attribut)+' check · DC '+probe.sg));
   const equation=element('span','ed-equation','The die falls …'),outcome=element('span','ed-outcome','');outcome.setAttribute('aria-live','polite');values.append(equation,outcome);stage.append(dice,values);if(!large)stage.append(skip);
   let layer=wrap;
   if(large){const fx=element('canvas','ed-fx');fx.setAttribute('aria-hidden','true');stage.prepend(fx);document.body.append(wrap);}
   else if(target&&target.isConnected){target.append(wrap);if(target.id==='verlauf')target.scrollTop=target.scrollHeight;}
   else{layer=element('div','eden-dice-layer ed-floating');layer.append(wrap);document.body.append(layer);}
   return {wrap,layer,stage,dice,canvases,equation,outcome,skip};
 }
 async function one(record,policy,target){
   const p=normalise(record.probe),large=record.modus==='gross'||policy.kritisch_gross!==false&&(p.wurf===1||p.wurf===20);
   const ui=build(p,large,record.titel,target),previous=document.activeElement,app=document.getElementById('app'),inertBefore=app&&app.inert;
   if(large&&app)app.inert=true;
   if(large)ui.skip.focus({preventScroll:true});
   let effect=null,raf=0,done=false;
   const owner={skip:()=>{}};active=owner;
   try{
     return await new Promise(resolve=>{
       const finish=status=>{if(done)return;done=true;cancelAnimationFrame(raf);resolve({status,id:record.id});};owner.skip=()=>finish('skipped');ui.skip.addEventListener('click',owner.skip);
       const onKey=e=>{if(e.key==='Escape'||large&&(e.key==='Enter'||e.key===' ')){e.preventDefault();e.stopImmediatePropagation();owner.skip();}else if(large&&e.key==='Tab'){e.preventDefault();ui.skip.focus();}};
       const onMotion=()=>{if(motion.matches)owner.skip();};
       document.addEventListener('keydown',onKey,true);motion.addEventListener('change',onMotion);
       owner.clean=()=>{document.removeEventListener('keydown',onKey,true);motion.removeEventListener('change',onMotion);};
       Promise.all([load('single-roll.webp'),...p.wuerfe.map(n=>load(filename(n)))]).then(images=>{
         if(done)return;
         const reveal=()=>{const index=p.wuerfe.indexOf(p.wurf);ui.canvases.forEach((canvas,i)=>{paint(canvas,p.wuerfe[i],images[i+1]);canvas.setAttribute('aria-label','W20: '+p.wuerfe[i]+(p.wuerfe.length>1?(i===index?', gewertet':', verworfen'):''));if(p.wuerfe.length>1)canvas.classList.add(i===index?'ed-chosen':'ed-discarded');});
           const bonus=p.boni.map(([name,n])=>(n>=0?'+':'−')+Math.abs(n)+' '+name).join(' ');ui.equation.textContent=(p.wuerfe.length>1?p.wuerfe.join(' / ')+' → '+p.wurf:String(p.wurf))+' '+bonus+' = '+p.summe;
           ui.outcome.textContent=names[p.ergebnis]||p.ergebnis;ui.wrap.classList.toggle('ed-failure',p.ergebnis==='patzer'||p.ergebnis==='fehlschlag');
         };
         if(motion.matches){reveal();finish('reduced-motion');return;}
         const start=performance.now(),duration=large?options.largeMs:options.compactMs;let revealed=false;
         const tick=now=>{if(done)return;if(!ui.wrap.isConnected){finish('detached');return;}const t=(now-start)/duration;
           if(t<.78)ui.canvases.forEach((canvas,i)=>paint(canvas,p.wuerfe[i],images[0],Math.min(60,Math.floor(t/.78*61)+(i?5:0))%61,true));
           else if(!revealed){revealed=true;reveal();if(large&&policy.effekte!==false&&(p.wurf===1||p.wurf===20)&&typeof EdenDiceEffects!=='undefined'){effect=new EdenDiceEffects(ui.stage.querySelector('.ed-fx'),ui.stage,ui.dice,{duration:1600,intensity:.85});effect.play(String(p.wurf));}}
           if(t<1)raf=requestAnimationFrame(tick);else if(effect){ui.skip.textContent='Weiter';raf=requestAnimationFrame(function linger(){if(done)return;if(!effect.running){finish('completed');return;}raf=requestAnimationFrame(linger);});}else finish('completed');
         };raf=requestAnimationFrame(tick);
       }).catch(()=>finish('fallback'));
     });
   }finally{if(owner.clean)owner.clean();if(effect)effect.destroy();ui.layer.remove();if(large&&app)app.inert=inertBefore;if(large&&previous&&previous.isConnected)previous.focus({preventScroll:true});if(active===owner)active=null;}
 }
 function play(packet,opts={}){
   if(!packet||!Array.isArray(packet.rolls))return Promise.resolve([]);
   const todo=packet.rolls.filter(r=>r&&typeof r.id==='string'&&!seen.has(r.id));todo.forEach(r=>remember(r.id));const gen=generation;
   const run=async()=>{const result=[];for(const record of todo){if(gen!==generation)break;try{result.push(await one(record,packet.policy||{},opts.target));}catch(error){console.warn('[EdenDice] Anzeige übersprungen:',error.message);result.push({status:'invalid',id:record.id});}}return result;};
   const next=chain.then(run,run);chain=next.catch(()=>{});return next;
 }
 function cancel(){generation++;if(active)active.skip();}
 function enhance(root=document){
   root.querySelectorAll('.wurf > .w').forEach(old=>{const value=Number(old.textContent.trim());if(!Number.isInteger(value)||value<1||value>20)return;const canvas=element('canvas','eden-dice-static');canvas.width=canvas.height=256;canvas.setAttribute('role','img');canvas.setAttribute('aria-label','W20: '+value);old.replaceWith(canvas);canvas.parentElement.classList.add('ed-enhanced');paint(canvas,value,null);load(filename(value)).then(image=>{if(canvas.isConnected)paint(canvas,value,image);});});
 }
 global.EdenDice={version:'1.0.0',play,cancel,enhance,normalise,options};
})(window);
