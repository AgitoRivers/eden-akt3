/* Exercise approved animations from the skill UI. Isolated lab only, no engine. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {chromium}=require(process.env.EDEN_PLAYWRIGHT_PATH||'playwright');
const approved=JSON.parse(fs.readFileSync(path.join(__dirname,'../docs/effekt-auswahl/status-labor/freigabe-spezialangriffe.json'),'utf8')).choices;
const mapping={mistral:'mistral',ressac:'wave',libeccio:'wind',lame_de_fond:'tidal',doppio_gioco:'doubleSlash',sotto_voce:'blur',vendetta:'vendetta',omerta:'blackSlash',point_de_mire:'reticle',bonaccia:'calm',phare:'beam',pluie_d_etoiles:'rain',scirocco:'scirocco',retour:'retour',furia:'furia',vulcano:'vulcano'};
(async()=>{
 const browser=await chromium.launch({headless:true,channel:process.env.EDEN_BROWSER_CHANNEL||'msedge',args:['--disable-gpu']});
 try{
  const page=await browser.newPage({viewport:{width:1600,height:1120}}),errors=[],writes=[],failed=[];
  page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(r.method()!=='GET')writes.push(r.url())});page.on('response',r=>{if(r.status()>=400)failed.push(r.status()+' '+r.url())});
  await page.goto(process.env.EDEN_SKILLS_SHOWCASE_URL||'http://127.0.0.1:8337/status-labor/faehigkeiten/');
  await page.waitForSelector('.es-node');
  assert.equal(await page.locator('iframe').count(),0,'No animation loads before a click');
  assert.match(await page.locator('.es-build-hint').textContent(),/Omertà/);
  await page.locator('.es-help summary').click();
  assert.match(await page.locator('.es-help').textContent(),/6 skill points/);
  assert.match(await page.locator('.es-point-plan').textContent(),/(?:Level|Lv) 10: 2 points/);
  await page.locator('.es-help summary').click();
  for(const [id,effect] of Object.entries(mapping)){
   await page.locator(`[data-skill-select="${id}"]`).click();
   assert.ok((await page.locator('.es-purpose').textContent()).length>5);
   assert.ok((await page.locator('.es-combo p').textContent()).length>20);
   const before=await page.locator('.es-points strong').textContent();
   await page.locator('[data-skill-preview]').click();
   const frame=await page.locator('.es-preview-dialog iframe').elementHandle().then(el=>el.contentFrame());
   await frame.waitForFunction(()=>Boolean(window.EdenAttackStudy),{},{timeout:30000});
   await page.waitForFunction(()=>document.querySelector('.es-preview-status')?.hidden,{},{timeout:30000});
   const choice=await frame.evaluate(()=>window.EdenAttackStudy.selection());
   assert.deepEqual(choice,{attack:effect,variant:approved[effect].variant});
   assert.equal(await frame.locator('#play').textContent(),'Pause','User-requested preview starts playing');
   if(id==='omerta'){
    await frame.locator('#play').click();
    await frame.evaluate(()=>EdenAttackStudy.render(EdenAttackStudy.timing().contact+.3));
    if(process.env.EDEN_SKILLS_SCREENSHOTS)await page.screenshot({path:path.join(process.env.EDEN_SKILLS_SCREENSHOTS,'faehigkeiten-animation.png')});
   }
   if(id==='vulcano'){
    await frame.evaluate(()=>EdenAttackStudy.render(EdenAttackStudy.duration-.025));
    await frame.waitForFunction(()=>document.querySelector('#play').textContent==='Abspielen');
    const end=await frame.locator('#time').textContent();await page.waitForTimeout(250);
    assert.equal(await frame.locator('#time').textContent(),end,'Player stops instead of looping');
    await frame.locator('#restart').click();
    assert.equal(await frame.locator('#play').textContent(),'Pause');
   }
   if(id==='retour'){
    await frame.locator('#scene').focus();await frame.evaluate(()=>document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true})));
   }else await page.locator('.es-preview-close').click();
   await page.waitForFunction(()=>!document.querySelector('.es-preview-dialog'));
   assert.equal(await page.locator('iframe').count(),0,'Closing unloads the player');
   assert.equal(await page.locator('.es-points strong').textContent(),before,'Preview never spends points');
   assert.equal(await page.locator('[data-skill-preview]').evaluate(el=>el===document.activeElement),true);
  }
  assert.deepEqual(writes,[]);assert.deepEqual(failed,[]);assert.deepEqual(errors,[]);
  console.log('PASS: all 16 approved variants; short explanations, combos, point schedule, build hint; on-demand load, play once, replay, close/unload, Escape, focus restoration, no writes/errors.');
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
