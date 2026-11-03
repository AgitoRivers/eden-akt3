/* Desktop board: no scrolling, complete effects, real forecasts, keyboard navigation. */
const assert=require('node:assert/strict');
const path=require('node:path');
const {chromium}=require(process.env.EDEN_PLAYWRIGHT_PATH||'playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,channel:process.env.EDEN_BROWSER_CHANNEL||'msedge',args:['--disable-gpu']});
 try{
  const page=await browser.newPage({viewport:{width:1600,height:900}}),errors=[],writes=[];
  page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(r.method()!=='GET')writes.push(r.url())});
  await page.goto(process.env.EDEN_SKILLS_SHOWCASE_URL||'http://127.0.0.1:8337/status-labor/faehigkeiten/');await page.waitForSelector('.es-node');
  async function fits(label){
   const result=await page.evaluate(()=>{
    const problems=[],bounds=el=>{const b=el.getBoundingClientRect();return {left:b.left,top:b.top,right:b.right,bottom:b.bottom,width:b.width,height:b.height}},inside=(a,b)=>a.left>=b.left-1&&a.right<=b.right+1&&a.top>=b.top-1&&a.bottom<=b.bottom+1;
    if(document.documentElement.scrollWidth>innerWidth||document.documentElement.scrollHeight>innerHeight)problems.push('page overflows');
    const board=bounds(document.querySelector('.es-columns'));
    for(const node of document.querySelectorAll('.es-node'))if(!inside(bounds(node),board))problems.push('node outside board: '+node.dataset.skillSelect);
    for(const selector of ['.es-tree','.es-detail','.es-detail-panels']){const el=document.querySelector(selector);if(el.scrollHeight>el.clientHeight+2)problems.push(selector+' overflow '+el.scrollHeight+'/'+el.clientHeight)}
    const panel=document.querySelector('.es-info-panel:not([hidden])'),area=document.querySelector('.es-detail-panels');if(!inside(bounds(panel),bounds(area)))problems.push('active information panel overflows');
    const learn=bounds(document.querySelector('.es-learn'));if(learn.bottom>innerHeight||learn.top<0)problems.push('action outside screen');
    return problems;
   });
   if(result.length&&process.env.EDEN_SKILLS_SCREENSHOTS)await page.screenshot({path:path.join(process.env.EDEN_SKILLS_SCREENSHOTS,'board-layout-failure.png')});
   assert.deepEqual(result,[],label);
  }
  for(const [width,height] of [[1280,720],[1366,768],[1600,900],[1920,1080]]){
   await page.setViewportSize({width,height});
   for(const node of await page.locator('.es-node').all()){
    const id=await node.getAttribute('data-skill-select');await node.click();
    await fits(`${width}x${height}: ${id}`);
   }
   await page.locator('#demo-state').selectOption('crossroads');await page.locator('[data-skill-select="scirocco"]').click();
   await fits(`${width}x${height}: main-path change`);
   const forecast=await page.locator('.es-learning-impact').textContent();assert.match(forecast,/Fighter → Berserker/);assert.match(forecast,/Strength.*5 → 2/);assert.match(forecast,/Courage.*2 → 5/);
   for(const tab of ['effect','combo','path']){await page.locator(`[data-skill-tab="${tab}"]`).click();await fits(`${width}x${height}: ${tab} tab`)}
   await page.locator('#demo-state').selectOption('experienced');
  }
  await page.setViewportSize({width:1280,height:720});
  for(const node of await page.locator('.es-node').all()){
   await node.click();
   for(const tab of ['combo','path']){await page.locator(`[data-skill-tab="${tab}"]`).click();await fits('720p supplemental information')}
  }
  await page.locator('[data-skill-select="mistral"]').click();await page.keyboard.press('ArrowRight');assert.equal(await page.locator('.es-learn').getAttribute('data-skill-learn'),'ressac');
  await page.keyboard.press('ArrowDown');assert.equal(await page.locator('.es-learn').getAttribute('data-skill-learn'),'sotto_voce');
  assert.equal(await page.locator('[data-skill-select="sotto_voce"]').evaluate(el=>el===document.activeElement),true);
  await page.locator('#demo-state').selectOption('crossroads');await page.locator('[data-skill-select="scirocco"]').click();await page.locator('.es-learn').click();assert.equal(await page.locator('.es-main b').textContent(),'Berserker');assert.equal(await page.locator('.es-points strong').textContent(),'0');
  await page.locator('#demo-state').selectOption('experienced');await page.locator('[data-skill-select="omerta"]').click();await page.setViewportSize({width:1600,height:900});
  await page.locator('.es-help summary').click();assert.match(await page.locator('.es-help-card').textContent(),/Berserker → Fighter → Smuggler → Marksman/);await page.locator('.es-help summary').click();
  if(process.env.EDEN_SKILLS_SCREENSHOTS){await page.screenshot({path:path.join(process.env.EDEN_SKILLS_SCREENSHOTS,'faehigkeiten-board.png')});await page.setViewportSize({width:1280,height:720});await page.screenshot({path:path.join(process.env.EDEN_SKILLS_SCREENSHOTS,'faehigkeiten-board-720p.png')})}
  assert.deepEqual(errors,[]);assert.deepEqual(writes,[]);
  console.log('PASS: all 16 skills and main-path changes at four PC resolutions without scrolling; complete detail tabs, keyboard arrows, point use, no network writes/errors.');
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
