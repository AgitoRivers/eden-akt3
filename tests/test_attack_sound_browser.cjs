/* Run only against the isolated lab on 8337. No engine or saves. */
const assert=require('node:assert/strict'),path=require('node:path');
const {chromium}=require(process.env.EDEN_PLAYWRIGHT_PATH||'playwright');
(async()=>{
 const b=await chromium.launch({headless:true,channel:'msedge',args:['--disable-gpu']});const p=await b.newPage({viewport:{width:1600,height:1000}}),errors=[],bad=[];
 p.on('pageerror',e=>errors.push(e.message));p.on('response',r=>{if(r.status()>=400)bad.push(r.status()+' '+r.url())});
 await p.addInitScript(()=>{window.__readyCount=0;document.addEventListener('eden-preview-ready',()=>window.__readyCount++)});
 await p.goto('http://127.0.0.1:8337/status-labor/ablaufprobe/?angriff=mistral&einmal=1');await p.waitForFunction(()=>window.EdenAttackStudy);
 assert.equal(await p.evaluate(()=>window.__readyCount),1);assert.equal((await p.evaluate(()=>EdenAttackStudy.selection())).attack,'mistral');assert((await p.evaluate(()=>EdenAttackStudy.duration))>4);
 await p.locator('#sound-toggle').click();await p.waitForFunction(()=>EdenAttackAudio.inspect().enabled&&EdenAttackAudio.inspect().starts>0);
 await p.locator('#play').click();assert.equal((await p.evaluate(()=>EdenAttackAudio.inspect())).playing,false);
 await p.locator('#play').click();await p.waitForFunction(()=>EdenAttackAudio.inspect().playing);
 await p.locator('#speed').selectOption('0.4');await p.locator('#restart').click();await p.waitForTimeout(60);
 await p.locator('#sound-toggle').click();assert.equal((await p.evaluate(()=>EdenAttackAudio.inspect())).playing,false);
 const report=await p.evaluate(async()=>{
  const results=[];
  for(const [attack,a]of Object.entries(EDEN_ATTACK_SOUND_CUES.attacks)){
   const variant=window.EDEN_APPROVED_ANIMATIONS.choices[attack].variant??0,lane=a.variants[variant],context=new OfflineAudioContext(2,Math.ceil(lane.duration*48000),48000);
   const handle=EdenAttackSound.play({attack,variant,context,destination:context.destination,startAt:0,baseUrl:new URL('../',location.href).href});
   await handle.ready;const rendered=await context.startRendering();let peak=0,energy=0;
   for(let ch=0;ch<2;ch++)for(const v of rendered.getChannelData(ch)){peak=Math.max(peak,Math.abs(v));energy+=v*v}
   results.push({attack,peak,energy});
  }
  return results;
 });
 assert.equal(report.length,20);assert(report.every(r=>r.energy>0));assert(report.every(r=>r.peak<.99),JSON.stringify(report.filter(r=>r.peak>=.99)));
 const approved=await p.evaluate(()=>Object.fromEntries(Object.entries(EDEN_APPROVED_ANIMATIONS.choices).map(([k,v])=>[k,v.variant??0])));
 for(const [attack,variant]of Object.entries(approved)){
  await p.goto('http://127.0.0.1:8337/status-labor/ablaufprobe/?angriff='+attack+'&einmal=1');await p.waitForFunction(()=>window.EdenAttackStudy);
  assert.deepEqual(await p.evaluate(()=>EdenAttackStudy.selection()),{attack,variant});assert.equal(await p.evaluate(()=>window.__readyCount),1);
  const contract=await p.evaluate(()=>({duration:EdenAttackStudy.duration,hook:typeof EdenFigurePicker.mount,duc:localStorage.getItem('eden-fx-duc-set-v1')}));assert(contract.duration>0);assert.equal(contract.hook,'function');
  await p.evaluate(()=>EdenAttackStudy.render(EdenAttackStudy.soundTimeline().hits[0]+.05));
 }
 assert.deepEqual(errors,[]);assert.deepEqual(bad,[]);await b.close();console.log(JSON.stringify({attacksRendered:20,animationEntries:20,mistralPlayback:'ok',pauseResume:'ok',speed:'ok',stop:'ok',readyEvent:'preserved',maxSamplePeak:Math.max(...report.map(r=>r.peak)),errors,bad}));
})().catch(e=>{console.error(e);process.exit(1)});
