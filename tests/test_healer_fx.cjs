const assert=require('node:assert/strict'),path=require('node:path');
const{chromium}=require(process.env.EDEN_PLAYWRIGHT_PATH||'playwright');
(async()=>{const b=await chromium.launch({headless:true,channel:'msedge',args:['--disable-gpu']});const p=await b.newPage({viewport:{width:1500,height:1000}}),errors=[];
 await p.emulateMedia({reducedMotion:'no-preference'});p.on('pageerror',e=>errors.push(e.message));p.on('response',r=>{if(r.status()>=400)errors.push(r.status()+' '+r.url())});
 // Emulate only the game's existing read-only preview prefix; never start the engine.
 await p.route('**/plugins/eden-skills/preview/**',route=>route.continue({url:route.request().url().replace('/plugins/eden-skills/preview/','/status-labor/')}));
 await p.addInitScript(()=>{window.__readyCount=0;document.addEventListener('eden-preview-ready',()=>window.__readyCount++)});
 for(const id of ['balm','westWind','awaken','archangel'])for(const variant of [0,1,2]){
  await p.goto('http://127.0.0.1:8337/status-labor/ablaufprobe/?angriff='+id+'&variante='+variant+'&einmal=1');await p.waitForFunction(()=>window.EdenAttackStudy);
  await p.locator('#choice-others').check();await p.locator('[data-variant="'+variant+'"]').click();
  assert.deepEqual(await p.evaluate(()=>EdenAttackStudy.selection()),{attack:id,variant});assert.equal(await p.evaluate(()=>window.__readyCount),1);
  assert.equal(await p.locator('.variants [data-variant]:visible').count(),3,'Unapproved healer drafts expose all three variants');
  const result=await p.evaluate(()=>{if(document.querySelector('#play').textContent==='Pause')document.querySelector('#play').click();const t=EdenAttackStudy.soundTimeline().hits[0]+.15;EdenAttackStudy.render(t);const c=document.querySelector('#scene'),g=c.getContext('2d');document.querySelector('#effects').checked=false;EdenAttackStudy.render(t);const off=g.getImageData(1080,70,700,950).data.slice();document.querySelector('#effects').checked=true;EdenAttackStudy.render(t);const on=g.getImageData(1080,70,700,950).data;let diff=0;for(let i=0;i<off.length;i++)if(off[i]!==on[i])diff++;return{enemyChangedPixels:diff,pose:EdenAttackStudy.actor(t).pose,duration:EdenAttackStudy.duration}});
  assert.equal(result.enemyChangedPixels,0,id+' does not affect enemy');assert(!['attack','heavy_attack'].includes(result.pose));assert(result.duration>4);
 }
 await p.goto('http://127.0.0.1:8337/status-labor/ablaufprobe/?angriff=archangel&phase=rettung&einmal=1');await p.waitForFunction(()=>window.EdenAttackStudy);assert.equal(await p.evaluate(()=>EdenAttackStudy.duration),1.25);
 await p.evaluate(()=>{const app=document.createElement('div');app.id='app';app.style.cssText='position:relative;width:500px;height:450px';const duc=document.createElement('div');duc.id='rescue-anchor';duc.style.cssText='position:absolute;left:180px;top:100px;width:120px;height:300px';app.append(duc);document.body.append(app)});
 await p.addScriptTag({path:path.join(__dirname,'../client/plugins/eden-combat/eden-combat-effects.js')});
 await p.evaluate(()=>EdenCombatEffects.play('arcangelo_rettung',document.querySelector('#rescue-anchor'),{variant:1}));assert.equal(await p.locator('[data-eden-healer-rescue]').count(),1);assert.equal(await p.locator('[data-eden-healer-rescue]').evaluate(e=>getComputedStyle(e).pointerEvents),'none');assert.equal(await p.locator('iframe').count(),0);
 await p.waitForTimeout(1400);assert.equal(await p.locator('[data-eden-healer-rescue]').count(),0);
 await p.emulateMedia({reducedMotion:'reduce'});await p.evaluate(()=>EdenCombatEffects.play('archangel',document.querySelector('#rescue-anchor'),{phase:'rettung'}));assert.equal(await p.locator('[data-eden-healer-rescue]').count(),0);
 assert.deepEqual(errors,[]);await b.close();console.log(JSON.stringify({healerSkills:4,variants:12,enemyPixels:'unchanged',noAttackPoses:true,rescueDuration:1.25,noIframe:true,cleanup:'ok',reducedMotion:'ok',errors}));
})().catch(e=>{console.error(e);process.exit(1)});
