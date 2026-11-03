/* DOM-free cut-in audio. The host owns the AudioContext, destination and sequence clock. */
((root)=>{'use strict';
 const contextCaches=new WeakMap();
 function catalog(){if(!root.EDEN_ATTACK_SOUND_CUES)throw Error('EDEN_ATTACK_SOUND_CUES missing');return root.EDEN_ATTACK_SOUND_CUES}
 function resolve({attack,variant=0,timeline,mode='full'}={}){
  const def=catalog().attacks[attack];if(!def)throw Error('Unknown attack: '+attack);
  const lane=def.variants[variant];if(!lane)throw Error('Unknown variant: '+variant);
  if(mode==='rescue'){
   if(!lane.rescue)throw Error('No rescue phase for '+attack);
   return {attack,variant,mode,duration:lane.rescue.duration,events:lane.rescue.events.map(e=>({...e}))};
  }
  const t=timeline||lane,launch=t.launch,hits=t.hits,fullDuration=t.duration;
  if(!Number.isFinite(launch)||!Array.isArray(hits)||!hits.length||!hits.every(Number.isFinite)||!Number.isFinite(fullDuration))throw Error('Invalid sequence timing');
  const events=[];
  for(const cue of lane.events){
   if(mode==='charge'&&cue.phase!=='charge')continue;if(mode==='release'&&cue.phase==='charge')continue;
   if(cue.anchor==='hit'&&cue.hit_index>=hits.length)continue;
   const hitIndex=cue.hit_index===-1?hits.length-1:cue.hit_index;
   let offset=cue.anchor==='launch'?launch+cue.delta:cue.anchor==='hit'?hits[hitIndex]+cue.delta:cue.offset;
   if(mode==='release')offset-=launch-.25;
   const endTime=mode==='charge'?7:mode==='release'?fullDuration-launch+.25:fullDuration;
   const span=cue.until==='launch'?launch-.04-offset:cue.until==='end'?endTime-offset:cue.duration;
   events.push({...cue,offset:Math.max(0,offset),duration:span===undefined?undefined:Math.max(.02,span)});
  }
  // Vulcano's hit count follows the chosen brand stacks, including stacks 4 and 5.
  if(attack==='vulcano'&&mode!=='charge'&&hits.length>lane.hits.length){
   const sample=lane.events.filter(e=>e.anchor==='hit'&&e.hit_index===0&&e.phase==='hit');
   for(let i=lane.hits.length;i<hits.length;i++)for(const e of sample)events.push({...e,hit_index:i,offset:hits[i]+e.delta-(mode==='release'?launch-.25:0)});
  }
  return {attack,variant,mode,duration:mode==='charge'?7:mode==='release'?fullDuration-launch+.25:fullDuration,events:events.sort((a,b)=>a.offset-b.offset)};
 }
 function buffer(context,url){
  let cache=contextCaches.get(context);if(!cache){cache=new Map();contextCaches.set(context,cache)}
  if(!cache.has(url)){const pending=fetch(url).then(r=>{if(!r.ok)throw Error('Audio HTTP '+r.status);return r.arrayBuffer()}).then(b=>context.decodeAudioData(b));cache.set(url,pending);pending.catch(()=>cache.delete(url))}
  return cache.get(url);
 }
 function assetUrl(id,baseUrl){const entry=catalog().sounds[id];if(!entry)throw Error('Unknown sound: '+id);if(!baseUrl)throw Error('baseUrl required: URL of status-labor/ or preview/');return new URL(entry.file,baseUrl).href}
 function preload({context,baseUrl,attack,variant=0,timeline,mode='full'}={}){
  if(!context)throw Error('Host AudioContext required');const plan=resolve({attack,variant,timeline,mode});
  return Promise.all([...new Set(plan.events.map(e=>e.sound_id))].map(id=>buffer(context,assetUrl(id,baseUrl))));
 }
 function play({attack,variant=0,context,destination,startAt,baseUrl,timeline,mode='full',offset=0,speed=1}={}){
  if(!context||!destination)throw Error('Host context and destination required');
  if(!Number.isFinite(speed)||speed<=0||!Number.isFinite(offset)||offset<0)throw Error('Invalid speed/offset');
  if(destination.context&&destination.context!==context)throw Error('Destination belongs to another context');
  const plan=resolve({attack,variant,timeline,mode}),when=startAt??context.currentTime;
  if(!Number.isFinite(when))throw Error('Invalid startAt');
  let stopped=false;const active=new Set(),bus=context.createGain();bus.gain.value=.8;bus.connect(destination);
  function stop(){if(stopped)return;stopped=true;const now=context.currentTime;bus.gain.cancelScheduledValues(now);bus.gain.setValueAtTime(bus.gain.value,now);bus.gain.linearRampToValueAtTime(0,now+.025);for(const source of active)try{source.stop(now+.035)}catch(_){}if(!active.size)bus.disconnect()}
  const ready=Promise.all(plan.events.map(async cue=>({cue,data:await buffer(context,assetUrl(cue.sound_id,baseUrl))}))).then(loaded=>{
   if(stopped)return;
   const now=context.currentTime,sequenceNow=offset+Math.max(0,now-when)*speed;
   if(sequenceNow>=plan.duration){stop();return}
   for(const {cue,data} of loaded){
    const span=Math.min(cue.duration??data.duration,plan.duration-cue.offset,data.duration),elapsed=Math.max(0,sequenceNow-cue.offset);
    if(span<=0||elapsed>=span)continue;
    const source=context.createBufferSource(),gain=context.createGain();source.buffer=data;source.playbackRate.value=speed;
    const at=Math.max(now,when+(cue.offset-offset)/speed),remaining=(span-elapsed)/speed,end=at+remaining,fade=Math.min(.07,remaining/3);
    gain.gain.setValueAtTime(0,at);gain.gain.linearRampToValueAtTime(cue.gain,at+Math.min(.006,remaining/4));gain.gain.setValueAtTime(cue.gain,Math.max(at+Math.min(.006,remaining/4),end-fade));gain.gain.linearRampToValueAtTime(0,end);
    source.connect(gain);gain.connect(bus);active.add(source);
    source.onended=()=>{active.delete(source);source.disconnect();gain.disconnect();if(!active.size)bus.disconnect()};
    source.start(at,elapsed,span-elapsed);
   }
   if(!active.size)bus.disconnect();
  }).catch(error=>{stop();throw error});
  ready.catch(()=>{}); // Host may observe ready; never leak an unhandled rejection on skip.
  return {stop,ready,inspect:()=>({attack,variant,stopped,active:active.size,startAt:when,duration:plan.duration})};
 }
 root.EdenAttackSound=Object.freeze({resolve,preload,play});
})(globalThis);
