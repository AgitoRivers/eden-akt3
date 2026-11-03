/* Isolated UI showcase only; never opens the game or writes a save. */
const assert=require('node:assert/strict');
const path=require('node:path');
const fs=require('node:fs');
const vm=require('node:vm');
const {chromium}=require(process.env.EDEN_PLAYWRIGHT_PATH||'playwright');
const url=process.env.EDEN_SKILLS_SHOWCASE_URL||'http://127.0.0.1:8337/status-labor/faehigkeiten/';
// Exercise the menu plugin (Character -> skill tree, Inventory -> weapons) without starting the engine (26.10.2026:
// the old shop/"Du" path in index.html is gone, the pause menu lives in client/plugins/eden-menu).
const menuJs=fs.readFileSync(path.join(__dirname,'../client/plugins/eden-menu/eden-menu.js'),'utf8');
const scope={window:{},document:{addEventListener(){},querySelector:()=>null,querySelectorAll:()=>[]},overlay:'character',beschaeftigt:false,
 PHASE:{nachmittag:'Afternoon'},esc:s=>String(s??''),geld:String,punkte:()=>'',avatar:()=>'',zeichnen(){},senden(){},setTimeout,
 EdenSkills:{html:()=>'<section class="eden-skills">skills</section>'}};
scope.window.EdenSkills=scope.EdenSkills;
vm.createContext(scope);vm.runInContext(menuJs,scope);
const gear={waffe:{id:'bat',label:'Terremoto',schaden:2},ruestung:{id:'jacket_earth',label:'Terra Scura',schutz:3}};
const zMenu={tag:3,tage:8,phase:'nachmittag',persona:{titel:'T',attribute:{charm:3},geheimnis:'',oeffentlich:''},
 handel:{konto:0,inventar_info:[],belegt:0,tasche:[],tasche_plaetze:3},
 kampf_profil:Object.assign({level:2,level_max:9,xp:1,xp_next:5,lp:4,lp_max:4,ausdauer:3,attribute:[],skillpunkte:1,pfade:[],
  waffen:[gear.waffe],ruestungen:[gear.ruestung],chips:{pool:[],stuecke:[]}},gear)};
const EM=scope.window.EdenMenu;
EM.ansicht('skills');
assert.match(EM.html(zMenu,'character'),/em-skillbaum/);assert.match(EM.html(zMenu,'character'),/class="eden-skills"/);
EM.ansicht('overview');assert.doesNotMatch(EM.html(zMenu,'character'),/em-skillbaum/);
assert.match(EM.html(zMenu,'inventory'),/Weapons/);assert.match(EM.html(zMenu,'inventory'),/Terremoto/);
(async()=>{
 const browser=await chromium.launch({headless:true,channel:process.env.EDEN_BROWSER_CHANNEL||'msedge',args:['--disable-gpu']});
 try{
  const page=await browser.newPage({viewport:{width:1600,height:1120}}),errors=[],writes=[];
  page.on('pageerror',e=>errors.push(String(e)));
  page.on('request',r=>{if(r.method()!=='GET')writes.push(r.url())});
  await page.goto(url);await page.waitForSelector('.es-node');
  assert.equal(await page.locator('.es-node').count(),16);
  await page.locator('.eden-skill-art').evaluateAll(images=>Promise.all(images.map(im=>im.decode())));
  assert.equal(await page.locator('.es-detail h4').textContent(),'Omertà');
  assert.equal(await page.locator('.es-learn').isEnabled(),true);
  if(process.env.EDEN_SKILLS_SCREENSHOTS)await page.screenshot({path:path.join(process.env.EDEN_SKILLS_SCREENSHOTS,'faehigkeiten-desktop.png'),fullPage:true});
  for(const tile of await page.locator('.es-node').all()){
   const id=await tile.getAttribute('data-skill-select');
   await tile.click();
   assert.equal(await page.locator('.es-learn').getAttribute('data-skill-learn'),id);
  }
  await page.locator('[data-skill-select="vulcano"]').click();
  assert.equal(await page.locator('.es-learn').isDisabled(),true);
  assert.match(await page.locator('.es-requirement').textContent(),/Furia/);
  await page.locator('[data-skill-select="omerta"]').click();
  await page.locator('.es-learn').click();
  assert.equal(await page.locator('.es-points strong').textContent(),'1');
  assert.match(await page.locator('.es-learn').textContent(),/Already learned/);
  await page.locator('#demo-state').selectOption('spent');
  assert.equal(await page.locator('.es-node.available').count(),0);
  await page.locator('[data-skill-select="scirocco"]').click();
  assert.match(await page.locator('.es-reason').textContent(),/No free skill point/);
  await page.locator('#demo-state').selectOption('beginner');
  assert.equal(await page.locator('.es-node.available').count(),4);
  await page.locator('[data-skill-select="scirocco"]').focus();
  await page.keyboard.press('Enter');
  assert.equal(await page.locator('.es-detail h4').textContent(),'Scirocco');
  assert.equal(await page.locator('[data-skill-select="scirocco"]').evaluate(el=>el===document.activeElement),true);
  assert.deepEqual(writes,[]);assert.deepEqual(errors,[]);
  console.log('PASS: 16 icons, all detail selections, prerequisites, learned state, points exhausted, beginner, PC keyboard focus, no network writes or JS errors.');
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
