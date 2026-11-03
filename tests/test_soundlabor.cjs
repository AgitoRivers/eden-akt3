/* Read-only browser checks of all 124 locally generated sound alternatives. */
const assert=require('node:assert/strict');
const {chromium}=require(process.env.EDEN_PLAYWRIGHT_PATH||'C:/Users/DucNg/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'msedge',args:['--disable-gpu']});
 try{
  const page=await browser.newPage({viewport:{width:1600,height:1000}}),errors=[],bad=[],writes=[];
  page.on('pageerror',e=>errors.push(String(e)));page.on('response',r=>{if(r.status()>=400)bad.push(r.status()+' '+r.url())});page.on('request',r=>{if(r.method()!=='GET')writes.push(r.url())});
  await page.goto('http://127.0.0.1:8337/status-labor/soundlabor/archiv.html');await page.waitForFunction(()=>!!window.EdenSoundLab);
  assert.deepEqual(await page.evaluate(()=>{const s=window.EdenSoundLab.inspect();return {items:s.items,takes:s.takes,playing:s.playing}}),{items:31,takes:124,playing:false});
  assert.equal(await page.locator('.family').count(),7);assert.equal(await page.locator('.take').count(),124);
  const decoded=await page.evaluate(async()=>{
   const data=await (await fetch('katalog.json')).json(),context=new AudioContext(),items=data.groups.flatMap(g=>g.items),takes=items.flatMap(i=>i.variants),ids=new Set(),attacks=new Set(items.flatMap(i=>i.attacks));
   for(let i=0;i<takes.length;i+=6)await Promise.all(takes.slice(i,i+6).map(async t=>{if(t.status!=='ready')throw Error('Missing '+t.generation_id);if(ids.has(t.generation_id))throw Error('Duplicate take');ids.add(t.generation_id);const r=await fetch(t.file);if(!r.ok)throw Error('Missing audio');const audio=await context.decodeAudioData(await r.arrayBuffer());if(audio.duration<.2)throw Error('Empty audio');}));
   await context.close();return {takes:ids.size,attacks:attacks.size,credits:data.actual_credits};
  });assert.equal(decoded.takes,124);assert.equal(decoded.attacks,16);
  await page.getByRole('button',{name:/Klinge & Schatten/}).click();assert.equal(await page.locator('.sound-item').count(),4);
  await page.getByRole('button',{name:'Schwerer Klingenschnitt · A vorhören',exact:true}).click();await page.waitForFunction(()=>window.EdenSoundLab.inspect().playing);
  await page.getByRole('button',{name:'Schwerer Klingenschnitt · B vorhören',exact:true}).click();await page.waitForFunction(()=>window.EdenSoundLab.inspect().current?.letter==='B');
  await page.getByRole('button',{name:'■ Stopp',exact:true}).click();assert.equal(await page.evaluate(()=>window.EdenSoundLab.inspect().playing),false);
  await page.getByRole('radio',{name:'Schwerer Klingenschnitt · Variante B wählen',exact:true}).check();
  await page.getByRole('textbox',{name:'Notiz zu Schwerer Klingenschnitt',exact:true}).fill('Satt genug, etwas kürzer.');await page.waitForTimeout(300);
  await page.reload();await page.waitForFunction(()=>!!window.EdenSoundLab);assert.equal(await page.getByRole('radio',{name:'Schwerer Klingenschnitt · Variante B wählen',exact:true}).isChecked(),true);assert.equal(await page.getByRole('textbox',{name:'Notiz zu Schwerer Klingenschnitt',exact:true}).inputValue(),'Satt genug, etwas kürzer.');
  await page.getByRole('checkbox',{name:'Nur ohne Favorit',exact:true}).check();assert.equal(await page.locator('[data-item="blade_slash"]').count(),0);await page.getByRole('checkbox',{name:'Nur ohne Favorit',exact:true}).uncheck();
  const row=page.locator('[data-item="shadow_charge"]');await row.getByRole('button',{name:'Keine passt',exact:true}).click();assert.equal(await page.locator('[data-item="shadow_charge"] .feedback-state').textContent(),'Neue Varianten');
  const download=page.waitForEvent('download');await page.getByRole('button',{name:'Auswahl sichern ↓',exact:true}).click();const file=await (await download).path();const fs=require('node:fs');const saved=JSON.parse(fs.readFileSync(file,'utf8'));assert.equal(saved.choices.blade_slash.variant,'B');assert.ok(saved.choices.blade_slash.generation_id);assert.equal(saved.choices.shadow_charge.reject,true);
  await page.locator('#search').fill('Phare');assert.equal(await page.locator('.sound-item').count(),1);assert.match(await page.locator('.sound-item h3').textContent(),/Aufblenden/);await page.locator('#search').fill('');
  for(const viewport of [{width:1366,height:768},{width:1600,height:1000}]){await page.setViewportSize(viewport);assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,'No horizontal page overflow')}
  await page.evaluate(()=>localStorage.removeItem('eden-soundlabor-v1'));await page.reload();await page.waitForFunction(()=>!!window.EdenSoundLab);
  await page.locator('#import-file').setInputFiles(file);await page.waitForFunction(()=>document.querySelector('#progress').textContent.includes('1 / 31'));
  assert.equal(await page.getByRole('radio',{name:'Schwerer Klingenschnitt · Variante B wählen',exact:true}).isChecked(),true);assert.equal(await page.locator('[data-item="shadow_charge"] .feedback-state').textContent(),'Neue Varianten');
  // Clear only this isolated headless browser's test choices before the screenshot.
  await page.evaluate(()=>localStorage.removeItem('eden-soundlabor-v1'));await page.reload();await page.waitForFunction(()=>!!window.EdenSoundLab);
  await page.getByRole('button',{name:/Klinge & Schatten/}).click();await page.screenshot({path:'C:/Users/DucNg/Documents/Codex/2026-10-17/hel/work/status-labor/sound-bank/soundlabor.png'});
  assert.deepEqual(errors,[]);assert.deepEqual(bad,[]);assert.deepEqual(writes,[]);console.log('PASS: 31 components, 124 distinct decoded takes, all 16 attacks covered; categories, playback, mute, favorites/notes persistence, rejection, open filter, search, JSON export, PC layout; no errors or writes. Credits:',decoded.credits);
 }finally{await browser.close()}
})().catch(error=>{console.error(error);process.exitCode=1});
