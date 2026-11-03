/* Requires Playwright and installed Edge: PLAYWRIGHT_MODULE can point to an existing module. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const base=path.resolve(__dirname,'../client/plugins/eden-dice');
const harness='<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="/eden-dice.css"><style>:root{color-scheme:dark;--ink:#07080b;--perle:#f3eee4;--akz:#d8bd86}body{background:#07080b;color:#f3eee4;font:15px/1.5 sans-serif;padding:20px}#target{max-width:600px}.wurf{display:flex;gap:12px;align-items:center}</style><script defer src="/eden-dice-effects.js"></script><script defer src="/eden-dice.js"></script><div id="app"><button id="origin">Start</button><div id="target"></div><div class="wurf"><span class="w">16</span><span>16 + 2 = 18</span></div></div></html>';
const server=http.createServer((req,res)=>{if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(harness);return;}const file=path.resolve(base,'.'+decodeURIComponent(req.url.split('?')[0]));if(!file.startsWith(base+path.sep)||!fs.existsSync(file)){res.writeHead(404);res.end();return;}res.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':file.endsWith('.css')?'text/css':'image/webp');res.end(fs.readFileSync(file));});
function probe(wurf=16,bonus=2,rolls=[wurf]){return {wurf,wuerfe:rolls,sg:12,summe:wurf+bonus,boni:[['Cunning',bonus]],attribut:'cunning',ergebnis:wurf===20?'kritisch':wurf===1?'patzer':wurf+bonus>=12?'erfolg':'fehlschlag'};}
(async()=>{
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const url='http://127.0.0.1:'+server.address().port;
 const browser=await chromium.launch({channel:'msedge',headless:true});let checks=0;
 try{
 const page=await browser.newPage({viewport:{width:736,height:900}}),errors=[];page.on('pageerror',e=>errors.push(e.message));await page.goto(url);await page.waitForFunction(()=>window.EdenDice);
 const packet=(id,p,modus='kompakt',policy={})=>({rolls:[{id,probe:p,modus,titel:'Testprobe'}],policy});
 const play=pack=>page.evaluate(pack=>EdenDice.play(pack,{target:document.getElementById('target')}),pack);
 const first=play(packet('normal',probe(16,4)));await page.waitForSelector('.eden-dice-card');assert.equal(await page.locator('.ed-sheet').count(),0);assert.equal((await first)[0].status,'completed');checks++;
 assert.deepEqual(await play(packet('normal',probe(16,4))),[]);checks++;
 const natural=play(packet('advantage',probe(20,2,[1,20])));await page.waitForSelector('.ed-sheet');assert.equal(await page.locator('#app').evaluate(e=>e.inert),true);await page.waitForSelector('.ed-chosen');assert.match(await page.locator('.ed-chosen').getAttribute('aria-label'),/20, gewertet/);assert.match(await page.locator('.ed-discarded').getAttribute('aria-label'),/1, verworfen/);assert.equal(await page.locator('.ed-fx').getAttribute('data-effect'),'sun');await page.keyboard.press('Escape');assert.equal((await natural)[0].status,'skipped');assert.equal(await page.locator('#app').evaluate(e=>e.inert),false);checks++;
 const fail=play(packet('fail',probe(1,15)));await page.waitForSelector('.ed-sheet');await page.waitForFunction(()=>document.querySelector('.ed-outcome')?.textContent==='Kritischer Fehlschlag');assert.equal(await page.locator('.ed-fx').getAttribute('data-effect'),'fire');await page.locator('.ed-skip').click();await fail;checks++;
 const important=play(packet('important',probe(9,1),'gross'));await page.waitForSelector('.ed-sheet');await page.locator('.ed-skip').click();await important;checks++;
 await page.emulateMedia({reducedMotion:'reduce'});assert.equal((await play(packet('reduced',probe(20))))[0].status,'reduced-motion');checks++;
 assert.equal((await play(packet('invalid',{wurf:200})))[0].status,'invalid');assert.equal(await page.locator('.eden-dice-layer').count(),0);checks++;
 await page.evaluate(()=>{EdenDice.options.assetBase='/missing/';});assert.equal((await play(packet('missing',probe(14))))[0].status,'reduced-motion');checks++;
 await page.evaluate(()=>{EdenDice.enhance(document);EdenDice.enhance(document);});assert.equal(await page.locator('.eden-dice-static').count(),1);checks++;
 await page.setViewportSize({width:320,height:900});await page.emulateMedia({reducedMotion:'no-preference'});const mobile=play(packet('mobile',probe(20,2,[4,20])));await page.waitForSelector('.ed-sheet');assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);await page.locator('.ed-skip').click();await mobile;checks++;
 const pending=play(packet('cancel',probe(13)));await page.waitForSelector('.eden-dice-card');await page.evaluate(()=>EdenDice.cancel());assert.equal((await pending)[0].status,'skipped');checks++;
 assert.deepEqual(errors,[]);checks++;console.log('PASS:',checks,'browser checks: normal, natural criticals, advantage, skip, dedup, reduction, invalid/missing assets, enhancement, mobile, cancellation, runtime.');
 }finally{await browser.close();await new Promise(resolve=>server.close(resolve));}
})().catch(error=>{console.error(error);server.close();process.exitCode=1;});
