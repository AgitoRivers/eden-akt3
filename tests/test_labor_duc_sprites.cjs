/* Public lab assets and preference changes only, never an engine request. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {chromium}=require(process.env.EDEN_PLAYWRIGHT_PATH||'playwright');
const catalog=JSON.parse(fs.readFileSync(path.join(__dirname,'../docs/effekt-auswahl/status-labor/assets/duc-varianten-v1/katalog.json'),'utf8'));
(async()=>{
 const browser=await chromium.launch({headless:true,channel:process.env.EDEN_BROWSER_CHANNEL||'msedge',args:['--disable-gpu']});
 try{
  const page=await browser.newPage({viewport:{width:1600,height:1000}}),errors=[],failed=[],writes=[];
  page.on('pageerror',e=>errors.push(String(e)));page.on('response',r=>{if(r.status()>=400)failed.push(r.status()+' '+r.url())});page.on('request',r=>{if(r.method()!=='GET')writes.push(r.url())});
  await page.goto('http://127.0.0.1:8337/status-labor/ablaufprobe/?angriff=doubleSlash&variante=0');
  await page.waitForFunction(()=>Boolean(window.EdenAttackStudy),{},{timeout:30000});
  assert.equal(await page.locator('#player-look option').count(),5);assert.equal(await page.locator('#player-weapon option').count(),5);assert.equal(await page.locator('#preview-figure option').count(),27);
  for(const item of catalog.sets){
   await page.locator('#player-look').selectOption(item.look);await page.waitForFunction(()=>!document.querySelector('#player-weapon').disabled);
   await page.locator('#player-weapon').selectOption(item.weapon);
   await page.waitForFunction(id=>window.EdenDucActor.selection()?.id===id,item.id);
   const selected=await page.evaluate(()=>EdenDucActor.selection());assert.equal(selected.poses.length,7);
   const effect=await page.evaluate(()=>{const t=EdenAttackStudy.timing();EdenAttackStudy.render(t.contact);return EdenAttackStudy.actor(t.contact).pose});assert.ok(['attack','heavy_attack','windup','heavy_windup'].includes(effect));
  }
  for(const item of catalog.sets){await page.locator('#preview-figure').selectOption('duc:'+item.id);await page.waitForFunction(()=>!document.querySelector('#preview-figure').disabled);assert.equal(await page.locator('#error').textContent(),'')}
  await page.locator('#player-look').selectOption('Wasser');await page.waitForFunction(()=>!document.querySelector('#player-weapon').disabled);await page.locator('#player-weapon').selectOption('Gun');await page.waitForFunction(()=>EdenDucActor.selection()?.id==='DucWasserGun');
  await page.locator('#preview-figure').selectOption('vergleich');await page.waitForFunction(()=>!document.querySelector('#preview-figure').disabled);await page.evaluate(()=>EdenAttackStudy.render(.8));
  if(process.env.EDEN_SKILLS_SCREENSHOTS)await page.screenshot({path:path.join(process.env.EDEN_SKILLS_SCREENSHOTS,'duc-neue-sprites.png')});
  await page.reload();await page.waitForFunction(()=>Boolean(window.EdenAttackStudy),{},{timeout:30000});assert.equal(await page.evaluate(()=>EdenDucActor.selection().id),'DucWasserGun');
  await page.goto('http://127.0.0.1:8337/status-labor/?kategorie=reaktionen');await page.waitForSelector('#preview-figure option[value="duc:DucCyberSword"]',{state:'attached'});
  await page.locator('#preview-figure').selectOption('duc:DucCyberSword');await page.waitForFunction(()=>!document.querySelector('#preview-figure').disabled);assert.equal(await page.locator('#error').textContent(),'');
  assert.deepEqual(errors,[]);assert.deepEqual(failed,[]);assert.deepEqual(writes,[]);
  console.log('PASS: all 25 left-player sets, 25 comparison sets, seven-pose loads, persisted selection, reaction lab, no writes or load/JS errors.');
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
