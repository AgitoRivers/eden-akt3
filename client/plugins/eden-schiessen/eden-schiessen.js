/* Holm's Bet. Presentation only; results and the prizes belong to kern/schiessen.py.
   Three rounds against one opponent, the total decides. Coordinates use a 1000 x 560 range, independent of device pixel ratio. */
window.EdenSchiessen = (() => {
  'use strict';
  const W = 1000, H = 560, MAG = 10, RELOAD = 2, ZIELE = ['flasche', 'flasche2', 'flasche3', 'ton', 'drohne', 'moewe', 'granate'];
  const GRANATE_R = 9, GRANATE_DY = 46;     // the grenade hangs below the gull, the hit zone is small on purpose
  const ROUND_KINDS = [['bottle'], ['bottle', 'clay'], ['clay', 'clay', 'drone']];
  const GULLS = [1, 1, 2], STREAK_SHOW = 3, STREAK_STEP = 5;
  const TEXT = Object.freeze({
    title: "Holm's Bet", start: 'Take your shot', again: 'Again', leave: 'Back to deck',
    aim: 'Aim with the mouse. Left-click to fire. Wind pushes the shot in the arrow’s direction: aim against it.',
    aimCalm: 'Aim with the mouse. Left-click to fire. No wind tonight, the shot goes where you point.',
    ammo: 'Ten cartridges, two barrels. R or right-click reloads in two seconds, and targets don’t wait. Reload yourself in the five-second break.',
    gullrule: 'A gull costs you a hit. Hit the grenade under the gull and your opponent is blind for five seconds.',
    gullonly: 'A gull costs you a hit.',
    relaxed: 'Relaxed aim · no wind, two seconds more each round', relaxedCalm: 'Relaxed aim · two seconds more each round', saving: 'Checking the score…',
    retry: 'Send score again', failed: 'The score did not reach the deck. Try sending it again.',
    gull: ['That one wasn’t in the bet, Frankfurt.', 'Leave the gulls alone.', 'Bottles, Frankfurt. Not birds.'],
    reload: 'Reloading', empty: 'Empty. R to reload.', paused: 'Round paused', resume: 'Back to the bet',
  });
  const game = () => typeof V !== 'undefined' && V ? V.z || {} : {};
  const busy = () => typeof beschaeftigt !== 'undefined' && beschaeftigt;
  const send = (action, data = {}) => typeof senden === 'function' ? senden(action, data, '…') : Promise.reject(new Error('No engine'));
  const rand = (a, b) => a + Math.random() * (b - a);
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const FARBEN = {};     // canvas colours come from the same tokens as the page
  const col = n => FARBEN[n] || (FARBEN[n] = getComputedStyle(document.documentElement).getPropertyValue('--' + n).trim());
  const SPRITES = {};
  ZIELE.forEach(n => { const i = new Image(); i.onload = () => { SPRITES[n] = i; }; i.src = `/plugins/eden-schiessen/${n}.webp`; });
  let relaxed = false, folgt = false;
  try { relaxed = localStorage.getItem('eden_schiessen_leicht') === '1'; } catch (_) {}
  let S = null, lastFocus = null;
  const el = q => S?.box.querySelector(q);
  // Missing sound IDs are deliberately silent. No generated or unrelated sounds.
  function sound(id) {
    if (typeof V !== 'undefined' && V?.sfx?.katalog?.[id] && window.EdenSfx) EdenSfx.play(id);
  }
  function kreis(z) {
    if (!z || z.status !== 'wahl' || z.holm_wette !== true || !window.EdenAngeln) return '';
    return `<div class="es-kreis-wrap">${EdenAngeln.kreisKnopf({bild:'/bg/yacht_foredeck_sunrise.png',
      lab: "Holm's Bet <kbd>G</kbd>", aria: TEXT.title, titel: 'Meet Holm on the foredeck · costs no time',
      klick:'EdenSchiessen.oeffnen()'})}</div>`;
  }
  function oeffnen() { if (game().status === 'wahl' && game().holm_wette && !busy()) return send('schiessen_start'); }
  function card(html) {
    el('.es-card').innerHTML = html;
    el('.es-card').hidden = !html;
    if (html) el('.es-card button')?.focus({preventScroll:true});
  }
  const canRelax = () => S.data.relaxed_erlaubt;
  const roundTime = () => S.data.dauer + (S.easy ? S.data.relaxed_plus_s : 0);
  function relaxBox() {
    return canRelax() ? `<label><input type="checkbox" data-es="easy" ${relaxed ? 'checked' : ''}> ${S.data.wind ? TEXT.relaxed : TEXT.relaxedCalm}</label>` : '';
  }
  function instructions() {
    S.phase = 'ready';
    const a = S.data, n = a.gegner.name;
    card(`<small>FOREDECK · DUSK</small><h1>${TEXT.title}</h1>
      <p class="es-lead">Three rounds against ${n}. Most hits after three wins.</p>
      <div class="es-rule-grid"><div><b>${a.dauer} seconds a round · ${a.ziele} targets</b><p>${a.wind ? TEXT.aim : TEXT.aimCalm}</p></div>
      <div><b>Reload at the right moment</b><p>${TEXT.ammo}</p></div></div>
      <p class="es-target-key">${n} hits ${a.bot.join(' · ')} in rounds 1 · 2 · 3</p><p class="es-fine">${a.granate.length ? TEXT.gullrule : TEXT.gullonly}</p>
      ${relaxBox()}<button class="es-primary" data-es="start">${TEXT.start}</button><small>No time passes. Losing costs nothing.</small>`);
  }
  function mount(a) {
    lastFocus = document.activeElement;
    const box = document.createElement('section');
    box.id = 'schiessen'; box.setAttribute('role','dialog'); box.setAttribute('aria-modal','true');
    box.setAttribute('aria-label', TEXT.title);
    const av = typeof meinAvatar === 'function' ? meinAvatar() : '<span class="av ich">D</span>';
    const gegner = typeof avatar === 'function' ? avatar(a.gegner.avatare.neutral) : '';
    Object.values(a.gegner.avatare).forEach(u => { if (u) new Image().src = u; });
    box.innerHTML = `<div class="es-backdrop"></div><header class="es-header">
      <div class="es-player"><div class="es-face">${av}</div><div class="es-who"><small>YOU</small><div class="es-rounds" data-rounds="you"></div></div><b class="es-total" data-score="you">0</b></div>
      <div class="es-mid"><small class="es-round-label">ROUND 1 OF 3</small><div class="es-clock" aria-label="Seconds remaining">${a.dauer}</div></div>
      <div class="es-player es-other"><b class="es-total" data-score="holm">0</b><div class="es-who"><small>${a.gegner.name.toUpperCase()}</small><div class="es-rounds" data-rounds="holm"></div></div><div class="es-face">${gegner}<span class="es-blind" hidden></span></div></div>
      <button class="es-button" data-es="exit"><kbd>Esc</kbd> Back to deck</button></header>
      <div class="es-range"><canvas aria-label="Shooting range: bottles, clays, drones and protected gulls"></canvas>
      <div class="es-wind"><span class="es-wind-arrow">${window.EdenUI ? EdenUI.icon('wind') : ''}</span><div><small>WIND</small><b>Read the wind</b></div><span class="es-wind-bars"></span></div>
      <div class="es-callout" role="status" aria-live="polite"></div>
      <div class="es-break" hidden></div>
      <div class="es-card" role="region" aria-label="Round instructions and result"></div></div>
      <footer class="es-footer"><div class="es-ammo"><small>GEMELLI</small><div class="es-cartridges"></div><span class="es-barrels"></span></div>
      <div class="es-reload"><button class="es-button" data-es="reload"><kbd>R</kbd> Reload</button><span class="es-reload-track"><i></i></span></div>
      <div class="es-spare"></div><div class="es-streak"></div>
      <p>LEFT-CLICK <span>Fire</span> · RIGHT-CLICK <span>Reload</span><br><small>Read the wind. Aim against it.</small></p></footer>`;
    document.getElementById('app').appendChild(box);
    S = {box, data:a, phase:'ready', raf:0, previous:0, time:0, round:0, you:[0,0,0], bot:[0,0,0], botDone:[false,false,false],
      ammo:MAG, barrels:2, reloading:0, cycle:0, cooldown:0, targets:[], particles:[], marks:[], pointer:{x:500,y:280,in:false},
      wind:0, nextWind:0, plan:[], botPlan:[], blind:0, flash:0, breakLeft:0, streak:0, glow:0, mood:'neutral', moodUntil:0, callsUntil:0, submitted:false, exitRequested:false, easy:relaxed};
    box.querySelector('.es-backdrop').style.backgroundImage = `url("${encodeURI(a.bild).replace(/"/g,'%22')}")`;
    box.querySelector('.es-wind').hidden = !a.wind;
    S.canvas = box.querySelector('canvas'); S.ctx = S.canvas.getContext('2d');
    S.canvas.width = W * Math.min(devicePixelRatio || 1,2); S.canvas.height = H * Math.min(devicePixelRatio || 1,2);
    S.ctx.scale(S.canvas.width / W, S.canvas.height / H);
    const fit = () => {
      if (!S || S.box !== box) return;
      const r=box.querySelector('.es-range').getBoundingClientRect();
      const scale=Math.min(r.width/W,r.height/H);
      S.canvas.style.width=`${W*scale}px`; S.canvas.style.height=`${H*scale}px`;
      box.style.setProperty('--es-field-width',`${W*scale}px`);
    };
    S.resize=new ResizeObserver(fit); S.resize.observe(box.querySelector('.es-range')); fit();
    S.scenery=new Image(); S.scenery.src=a.bild;
    box.addEventListener('click', e => {
      const action = e.target.closest('[data-es]')?.dataset.es;
      if (action === 'start') begin();
      if (action === 'exit') exit();
      if (action === 'reload') reload();
      if (action === 'retry') submit();
      if (action === 'resume') resume();
    });
    box.querySelector('canvas').addEventListener('pointermove', e => {
      const r = S.canvas.getBoundingClientRect();
      S.pointer = {x:(e.clientX-r.left)*W/r.width, y:(e.clientY-r.top)*H/r.height,in:true};
    });
    S.canvas.addEventListener('pointerleave', () => { if (S) S.pointer.in = false; });
    S.canvas.addEventListener('pointerdown', e => {
      if (e.button !== 0) return;
      const r = S.canvas.getBoundingClientRect();
      S.pointer = {x:(e.clientX-r.left)*W/r.width,y:(e.clientY-r.top)*H/r.height,in:true};
      shoot();
    });
    box.addEventListener('contextmenu', e => { e.preventDefault(); reload(); });
    box.addEventListener('change', e => {
      if (e.target.dataset.es !== 'easy') return;
      relaxed = e.target.checked;
      try { localStorage.setItem('eden_schiessen_leicht', relaxed ? '1' : '0'); } catch (_) {}
    });
    if (a.letztes) { S.phase = 'result'; result(a.letztes, false); }
    else instructions();
    hud(); draw();
    S.raf = requestAnimationFrame(frame);
  }
  function begin() {
    if (!S || !['ready','result'].includes(S.phase) || busy()) return;
    if (S.data.letztes?.sieg && S.data.gegner.id !== 'holm') return;
    Object.assign(S,{round:0, you:[0,0,0], bot:[0,0,0], botDone:[false,false,false], ammo:MAG, barrels:2, reloading:0, cycle:0, cooldown:0,
      particles:[], marks:[], streak:0, glow:0, mood:'neutral', moodUntil:0, easy:canRelax() && relaxed, submitted:false, exitRequested:false, awaitingAttempt:S.data.versuche + 1});
    card(''); startBreak(true);
  }
  function chooseWind() {
    S.nextWind = S.easy || !S.data.wind ? 0 : (Math.random() < .5 ? -1 : 1)*rand(15,42);
    el('.es-wind').hidden = !S.data.wind;
    const strength = !S.nextWind ? 0 : Math.min(3,1+Math.floor((Math.abs(S.nextWind)-15)/9));
    el('.es-wind b').textContent = !S.nextWind ? 'Calm' : `${S.nextWind > 0 ? 'Right' : 'Left'} · ${['','light','steady','strong'][strength]}`;
    el('.es-wind-arrow').style.transform = S.nextWind < 0 ? 'rotate(180deg)' : 'none';
    el('.es-wind-arrow').style.opacity = S.nextWind ? 1 : .3;
    el('.es-wind-bars').innerHTML = [1,2,3].map(i => `<i class="${i<=strength?'an':''}"></i>`).join('');
    el('.es-wind').classList.add('es-wind-changed');
  }
  // The break comes before every round: the next wind shows, and reloading stays the player's job.
  function startBreak(first) {
    S.phase='break'; S.breakLeft=first ? 3 : S.data.pause_s; S.targets=[]; S.time=0; S.previous=0; S.blind=0;
    chooseWind(); breakText();
  }
  function breakText() {
    const b=el('.es-break'); b.hidden=false;
    const need=S.data.bot[S.round];
    b.innerHTML=`<small>ROUND ${S.round+1} OF 3</small><b>${Math.ceil(S.breakLeft)}</b><p>${S.data.gegner.name} hits ${need}. ${S.ammo<MAG?'<kbd>R</kbd> Reload now.':'Rifle is full.'}</p>`;
  }
  function startRound() {
    el('.es-break').hidden=true; el('.es-wind').classList.remove('es-wind-changed');
    S.phase='playing'; S.wind=S.nextWind; S.time=0; S.previous=0; S.targets=[]; S.blind=0;
    const d=roundTime(), kinds=ROUND_KINDS[S.round], n=S.data.ziele, plan=[];
    for (let i=0;i<n;i++) plan.push({at:(i+.2)*d/n+rand(-.08,.08), type:kinds[Math.floor(i/n*kinds.length)]});
    for (let i=0;i<GULLS[S.round];i++) plan.push({at:rand(1.5,d-2), type:'gull'});
    if (S.data.granate.includes(S.round)) plan.push({at:rand(2.5,d-4), type:'flash'});
    S.plan=plan.sort((a,b)=>a.at-b.at);
    const m=S.data.bot[S.round];
    // Holm starts fast and slows as the stitches pull; the others keep an even pace.
    const curve=S.data.gegner.id==='holm' ? 1.5 : 1;
    S.botPlan=Array.from({length:m},(_,i)=>({at:d*.96*(1-Math.pow(1-(i+1)/(m+1),curve))+rand(-.12,.12), x:rand(120,880), y:rand(130,280)}));
    hud();
  }
  function call(text, seconds=2) { el('.es-callout').textContent = text; S.callsUntil = S.time+seconds; }
  function spawn(type) {
    const dir = Math.random()<.5 ? 1 : -1;
    const t = {type, age:0, seed:rand(0,6.28), dir, x:dir>0 ? -40 : 1040, y:0, r:0};
    if (type === 'bottle') Object.assign(t,{x:rand(80,920),y:rand(370,440),vx:dir*rand(40,70),r:20,life:3.2,look:['flasche','flasche2','flasche3'][Math.floor(Math.random()*3)]});
    if (type === 'clay') Object.assign(t,{x:dir>0?rand(-40,150):rand(850,1040),y:rand(335,380),vx:dir*rand(135,180),vy:rand(-146,-112),r:24,life:3});
    if (type === 'drone') Object.assign(t,{x:dir>0?rand(-40,100):rand(900,1040),y:rand(110,230),vx:dir*rand(172,210),r:19,life:3.4});
    if (type === 'gull') Object.assign(t,{y:rand(160,295),vx:dir*rand(135,180),r:28,life:7.5});
    if (type === 'flash') Object.assign(t,{y:rand(120,230),vx:dir*rand(150,175),r:24,life:7});
    t.y0 = t.y;
    S.targets.push(t);
  }
  function position(t) {
    if (t.type==='bottle') return {x:t.x,y:t.y0+Math.sin(t.age*2+t.seed)*5+Math.max(0,t.age-t.life+.5)*60};
    if (t.type==='clay') return {x:t.x,y:t.y0+t.vy*t.age+37*t.age*t.age};
    const gull=t.type==='gull'||t.type==='flash';
    return {x:t.x,y:t.y0+Math.sin(t.age*(gull?2:4)+t.seed)*(gull?14:7)};
  }
  function reload() {
    if (!S || !['playing','break'].includes(S.phase) || S.reloading || S.ammo===MAG) return;
    S.reloading=RELOAD; sound('gun_reload'); hud();
  }
  function shoot() {
    if (!S || S.phase!=='playing' || S.reloading || S.cycle || S.cooldown || !S.pointer.in) return;
    if (!S.ammo) { call(TEXT.empty,1.2); return; }
    S.ammo--; S.barrels--; S.cooldown=.12;
    if (!S.barrels) S.cycle=.4;
    const x=S.pointer.x+S.wind, y=S.pointer.y;
    sound('gun_shot');
    S.marks.push({x,y,life:.48,hit:false});
    const zone=S.data.trefferzone;
    const flash=S.targets.find(t=>{
      if (t.type!=='flash') return false;
      const p=position(t);
      return Math.hypot(x-p.x,y-(p.y+GRANATE_DY))<=GRANATE_R*zone;
    });
    if (flash) { blind(flash); streakUp(x,y); hud(); return; }
    const hits = S.targets.filter(t => {
      const p=position(t), gull=t.type==='gull'||t.type==='flash';
      const dx=(x-p.x)/(gull?1.2:1), dy=(y-p.y)/(t.type==='bottle'?1.35:t.type==='flash'?.65:1);
      return Math.hypot(dx,dy) <= t.r*zone;
    });
    const target=hits.find(t=>t.type==='gull'||t.type==='flash') || hits[hits.length-1];
    if (target) {
      S.targets.splice(S.targets.indexOf(target),1);
      const gull=target.type==='gull'||target.type==='flash';
      S.you[S.round]=Math.max(0,S.you[S.round]+(gull?-1:1));
      S.marks[S.marks.length-1].hit=true;
      const look=gull?'gull':target.type;
      burst(x,y,look==='bottle'?col('gut'):look==='gull'?col('perle'):look==='drone'?col('schlecht'):col('akz'),gull?-1:1,look);
      sound({bottle:'schiessen_flasche',clay:'schiessen_ton',drone:'schiessen_drohne',gull:'schiessen_moewe'}[look]);
      if (gull) { S.streak=0; call(TEXT.gull[Math.floor(Math.random()*TEXT.gull.length)],2.2); }
      else streakUp(x,y);
    } else S.streak=0;
    hud();
  }
  // A streak changes the feel, never the score.
  function streakUp(x,y) {
    S.streak++;
    if (S.streak<STREAK_SHOW) return;
    S.glow=Math.min(1,S.glow+.5);
    S.particles.push({x,y:y-26,colour:col('akz'),text:`${S.streak} in a row`,label:true,life:.9,total:.9});
    if (S.streak%STREAK_STEP) return;
    S.glow=1;
    sound('fund');
    if (reduced.matches) return;
    for (let i=0;i<26;i++) S.particles.push({x,y,colour:i%2?col('rede'):col('akz'),vx:rand(-260,260),vy:rand(-260,60),shape:'spark',life:rand(.4,.8),total:.8});
  }
  function blind(t) {
    S.targets.splice(S.targets.indexOf(t),1);
    S.blind=S.data.blend_s; S.flash=.5;
    S.marks[S.marks.length-1].hit=true;
    sound('schiessen_blend');
    call(`${S.data.gegner.name} is blind for ${S.data.blend_s} seconds.`,2.4);
  }
  function burst(x,y,colour,points,type='holm') {
    S.particles.push({x,y,colour,points,label:true,life:.85,total:.85});
    S.marks.push({x,y,life:type==='bottle'?.7:.45,total:type==='bottle'?.7:.45,effect:type});
    if (reduced.matches) return;
    for (let i=0;i<(type==='drone'?22:14);i++) {
      const spark=type==='drone';
      S.particles.push({x,y,colour:spark?(i%2?col('rede'):col('schlecht')):type==='bottle' && i%2?col('akz2'):colour,
        vx:rand(spark?-230:-130,spark?230:130),vy:rand(-180,40),
        shape:spark?'spark':type==='clay'?'clay':'chip',
        life:rand(.3,.7),total:.7});
    }
  }
  const sum = a => a.reduce((x,y)=>x+y,0);
  function hud() {
    const roundsHtml=(list,who)=>list.map((v,i)=>{
      const open=i>S.round || (i===S.round && S.phase!=='playing' && !S.botDone[i]);
      const live=i===S.round && S.phase==='playing';
      const won=S.botDone[i] && (who==='you' ? S.you[i]>S.bot[i] : S.bot[i]>S.you[i]);
      return `<i class="${live?'live':''} ${won?'won':''}">${open?'·':v}</i>`;
    }).join('');
    el('[data-rounds="you"]').innerHTML=roundsHtml(S.you,'you');
    el('[data-rounds="holm"]').innerHTML=roundsHtml(S.bot,'holm');
    el('[data-score="you"]').textContent=sum(S.you);
    el('[data-score="holm"]').textContent=sum(S.bot);
    const left=S.phase==='playing' ? Math.max(0,Math.ceil(roundTime()-S.time)) : S.phase==='break' ? Math.ceil(S.breakLeft) : '–';
    el('.es-clock').textContent=left;
    el('.es-clock').classList.toggle('es-urgent',S.phase==='playing' && left<=3);
    el('.es-round-label').textContent=S.phase==='break' ? 'BREAK' : `ROUND ${Math.min(S.round+1,3)} OF 3`;
    el('.es-cartridges').innerHTML=Array.from({length:MAG},(_,i)=>`<i class="${i<S.ammo?'loaded':'spent'}"></i>`).join('');
    el('.es-cartridges').setAttribute('aria-label',`${S.ammo} of 10 cartridges`);
    el('.es-barrels').textContent=S.reloading ? `${TEXT.reload} ${S.reloading.toFixed(1)}s` : !S.ammo ? TEXT.empty : S.cycle ? 'Cycling…' : `${S.barrels} / 2 barrels`;
    el('.es-ammo').classList.toggle('es-ammo-low',S.ammo<=2 && ['playing','break'].includes(S.phase));
    el('[data-es="reload"]').disabled=!['playing','break'].includes(S.phase) || !!S.reloading || S.ammo===MAG;
    el('.es-reload-track i').style.width=S.reloading ? `${(1-S.reloading/RELOAD)*100}%` : '0%';
    // How many cartridges may still miss in this round before a reload is forced.
    const toBeat=S.data.bot[S.round]+1-S.you[S.round], spare=S.ammo-Math.max(0,toBeat);
    el('.es-spare').innerHTML=S.phase==='playing' ? (toBeat<=0 ? `<b class="ok">Ahead of ${S.data.gegner.name}</b>` : spare>=0 ? `<b>${spare}</b> to spare` : `<b class="bad">Reload</b> needed`) : '';
    const blind=el('.es-blind'); blind.hidden=!(S.blind>0); if (S.blind>0) blind.textContent=Math.ceil(S.blind);
    const st=el('.es-streak'); st.textContent=S.streak>=STREAK_SHOW ? `${S.streak} in a row` : ''; st.classList.toggle('hot',S.streak>=STREAK_STEP);
    mood();
  }
  // The opponent's face follows the score; blindness shows at once, the rest changes no more than every 1.2 s.
  function setMood(m) {
    if (m===S.mood) return;
    S.mood=m; S.moodUntil=performance.now()+1200;
    const u=S.data.gegner.avatare[m], av=el('.es-other .av');
    if (u && av) av.style.backgroundImage=`url('${u}')`;
    el('.es-other .es-face').classList.toggle('es-blinded',m==='blind');
  }
  function mood() {
    if (!['playing','break'].includes(S.phase)) return;
    const y=sum(S.you), b=sum(S.bot);
    if (S.blind>0) return setMood('blind');
    if (performance.now()<S.moodUntil) return;
    setMood(b>y+1?'vorn':y>b+1?'hinten':'neutral');
  }
  function endRound() {
    S.botDone[S.round]=true;
    if (S.round>=2) { S.phase='sending'; S.targets=[]; submit(); return; }
    S.round++;
    startBreak(false);
  }
  function frame(now) {
    if (!S) return;
    const dt=S.previous ? Math.max(0,(now-S.previous)/1000) : 0;
    S.previous=now;
    S.flash=Math.max(0,S.flash-dt);
    if (S.phase==='playing' || S.phase==='break') {
      if (S.reloading) { S.reloading=Math.max(0,S.reloading-dt); if (!S.reloading) {S.ammo=MAG;S.barrels=2;S.cycle=0;} }
      if (S.cycle) { S.cycle=Math.max(0,S.cycle-dt); if (!S.cycle) S.barrels=Math.min(2,S.ammo); }
      S.cooldown=Math.max(0,S.cooldown-dt);
    }
    if (S.phase==='break') {
      S.breakLeft=Math.max(0,S.breakLeft-dt);
      breakText();
      if (!S.breakLeft) startRound();
      hud();
    }
    if (S.phase==='playing') {
      S.time=Math.min(roundTime(),S.time+dt);
      S.blind=Math.max(0,S.blind-dt);
      S.glow=Math.max(0,S.glow-dt*.8);
      while (S.plan.length && S.time>=S.plan[0].at) spawn(S.plan.shift().type);
      while (S.botPlan.length && S.time>=S.botPlan[0].at) {
        const shot=S.botPlan.shift();
        if (S.blind>0) continue;
        S.bot[S.round]++;
        burst(shot.x,shot.y,col('akz'),0);
      }
      S.targets.forEach(t=>{t.age+=dt;t.x+=t.vx*dt;});
      S.targets=S.targets.filter(t=>t.age<t.life && t.x>-80 && t.x<1080 && position(t).y<510);
      S.marks.forEach(m=>m.life-=dt);S.marks=S.marks.filter(m=>m.life>0);
      S.particles.forEach(p=>{p.life-=dt;if(p.label)p.y-=dt*27;else{p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=dt*250;}});
      S.particles=S.particles.filter(p=>p.life>0);
      if (S.time>S.callsUntil) el('.es-callout').textContent='';
      if (S.time>=roundTime()) endRound();
      hud();
    }
    draw(); S.raf=requestAnimationFrame(frame);
  }
  async function submit() {
    if (!S || S.submitted || busy()) return;
    const session=S;
    S.submitted=true; S.phase='sending'; hud();
    card(`<small>THREE ROUNDS DONE</small><h2>${TEXT.saving}</h2><p>You ${sum(S.you)} · ${S.data.gegner.name} ${sum(S.bot)}</p>`);
    const runden=S.you.map((du,i)=>({du,bot:S.bot[i]}));
    try { await send('schiessen_ergebnis',{runden,leicht:S.easy}); } catch (_) {}
    if (S!==session) return;
    const a=game().schiessen;
    if (a && a.versuche===S.awaitingAttempt && a.letztes) {
      S.data=a;S.phase='result';result(a.letztes,true);
      if (S.exitRequested) exit();
    } else {
      S.submitted=false; S.phase='send-failed'; S.exitRequested=false;
      card(`<h2>${TEXT.failed}</h2><button class="es-primary" data-es="retry">${TEXT.retry}</button>`);
    }
  }
  function result(r,speak) {
    S.you=r.runden.map(x=>x.du); S.bot=r.runden.map(x=>x.bot); S.botDone=[true,true,true]; S.round=2; hud(); S.moodUntil=0; setMood(r.sieg?'hinten':'vorn');
    const a=S.data, holm=a.gegner.id==='holm', zeile=r.sieg?0:1, more=!r.sieg || holm;
    const gifts=(r.geschenke||[]).map(g=>`<li>Round ${g.runde}: <b>${g.name}</b></li>`).join('');
    const line=(r.geschenke||[]).length ? a.texte[r.geschenke.at(-1).runde+1] : a.texte[zeile];
    card(`<small>${r.sieg?'YOU WIN':'ROUND COMPLETE'} · ${a.gegner.name.toUpperCase()}</small><h2>${line}</h2>
      <div class="es-result-score">${r.du}<span>YOU / ${a.gegner.name.toUpperCase()}</span>${r.bot}</div>
      <p class="es-result-rounds">${r.runden.map((x,i)=>`<span class="${x.du>x.bot?'won':''}">R${i+1} ${x.du}:${x.bot}</span>`).join('')}</p>
      ${gifts?`<ul class="es-gifts">${gifts}</ul>`:''}
      ${more?`${relaxBox()}<button class="es-primary" data-es="start">${TEXT.again}</button>`:''}
      <button class="${more?'es-button':'es-primary'}" data-es="exit">${a.gegner.id==='wolff'&&r.sieg?'Meet Holm':a.weiter?'Next shooter':TEXT.leave}</button>`);
    if (speak && typeof festeZeileSprich==='function') {
      LADEN.gehoert=null;
      festeZeileSprich((r.geschenke||[]).length ? r.geschenke.at(-1).zeile : `${a.worte}#z${zeile}`);
    }
  }
  async function exit() {
    if (!S) return;
    if (S.phase==='sending' || busy()) { S.exitRequested=true; return; }
    if (S.phase==='exiting') return;
    S.phase='exiting';
    const next=S.data.weiter;
    await send('schiessen_ende');
    if (S && game().status==='schiessen') { S.phase='ready';instructions(); }
    else if (next && game().status==='wahl') oeffnen();
  }
  function pause() {
    if (!S || S.phase!=='playing') return;
    S.phase='paused';
    card(`<h2>${TEXT.paused}</h2><p>The sea can wait.</p><button class="es-primary" data-es="resume">${TEXT.resume}</button>`);
  }
  function resume() { if (S?.phase==='paused') {S.phase='playing';S.previous=0;card('');} }
  document.addEventListener('visibilitychange',()=>{if(document.hidden)pause();});
  window.addEventListener('blur',pause);
  document.addEventListener('keydown',e=>{
    if (!S || e.ctrlKey || e.altKey || e.metaKey) return;
    if (e.key==='Tab') {
      const buttons=[...S.box.querySelectorAll('button:not(:disabled),input')].filter(b=>b.getClientRects().length);
      if (!buttons.length) return;
      if (e.shiftKey && document.activeElement===buttons[0]) {e.preventDefault();buttons.at(-1).focus();}
      else if (!e.shiftKey && document.activeElement===buttons.at(-1)) {e.preventDefault();buttons[0].focus();}
      e.stopImmediatePropagation();return;
    }
    e.stopImmediatePropagation();
    if(e.key==='Escape'){e.preventDefault();exit();}
    else if(e.key.toLowerCase()==='r'){e.preventDefault();if(!e.repeat)reload();}
  },true);
  function draw() {
    if (!S) return;
    const c=S.ctx; c.clearRect(0,0,W,H);
    // An open-water viewport sits inside the foredeck photograph. The foreground furniture
    // stays outside this viewport, so floating targets cannot appear to stand on the deck.
    const sky=c.createLinearGradient(0,0,0,H);
    sky.addColorStop(0,'#3f455c');sky.addColorStop(.48,'#a98d7b');
    sky.addColorStop(.49,'#425c68');sky.addColorStop(1,'#142e3e');
    c.fillStyle=sky;c.fillRect(0,0,W,H);
    if (S.scenery.complete && S.scenery.naturalWidth) {
      const iw=S.scenery.naturalWidth,ih=S.scenery.naturalHeight;
      // Reuse clear sky and water from the supplied foredeck photo, avoiding the rail and mast.
      c.drawImage(S.scenery,0,0,iw*.6,ih*.31,0,0,W,273);
      c.drawImage(S.scenery,0,ih*.325,iw*.28,ih*.055,0,273,W,H-273);
      const dusk=c.createLinearGradient(0,0,0,H);
      dusk.addColorStop(0,'rgba(20,28,52,.62)');dusk.addColorStop(.48,'rgba(32,38,59,.48)');
      dusk.addColorStop(.49,'rgba(17,48,64,.58)');dusk.addColorStop(1,'rgba(8,29,46,.78)');
      c.fillStyle=dusk;c.fillRect(0,0,W,H);
    }
    c.fillStyle='rgba(224,193,151,.12)';c.fillRect(0,272,W,2);
    c.lineWidth=1;
    for(let j=0;j<19;j++) {c.beginPath();c.strokeStyle=`rgba(159,196,199,${.04+j*.004})`;
      for(let x=0;x<=W;x+=10){const y=285+j*14+Math.sin(x/(45+j*2)+S.time*.7+j)*(1+j*.14);x?c.lineTo(x,y):c.moveTo(x,y);}c.stroke();}
    S.targets.forEach(t=>drawTarget(c,t));
    const hs=S.botPlan[0];
    if (S.phase==='playing' && hs && hs.at-S.time<.5 && S.blind<=0) {
      c.save();c.translate(hs.x,hs.y);c.strokeStyle=col('akz');c.globalAlpha=.7;c.lineWidth=1.5;
      c.beginPath();c.ellipse(0,0,16,7,0,0,7);c.stroke();c.font='10px sans-serif';c.fillStyle=col('rede');c.textAlign='center';c.fillText(S.data.gegner.name.toUpperCase(),0,-17);c.restore();
    }
    S.particles.forEach(p=>{c.save();c.globalAlpha=clamp(p.life/p.total,0,1);c.fillStyle=p.colour;
      if(p.label){c.font='bold 26px sans-serif';c.textAlign='center';c.shadowColor=col('ink');c.shadowBlur=5;c.font=p.text?'bold 19px sans-serif':c.font;c.fillText(p.text||(p.points>0?'+'+p.points:p.points<0?'−1':''),p.x,p.y);}
      else{c.translate(p.x,p.y);c.rotate(p.life*4);
        if(p.shape==='spark'){c.fillRect(-1,-1,12,1.5);}
        else{c.beginPath();c.moveTo(-3,-3);c.lineTo(4,-1);c.lineTo(1,4);c.closePath();c.fill();}
      }c.restore();});
    S.marks.forEach(m=>{c.save();c.globalAlpha=clamp(m.life/(m.total||.48),0,1);c.strokeStyle=m.hit?col('rede'):col('perle');c.lineWidth=2;c.beginPath();
      if(m.effect){
        const age=1-m.life/m.total;
        if(m.effect==='bottle'){c.strokeStyle=col('akz2');c.ellipse(m.x,m.y+20,12+age*45,3+age*10,0,0,7);c.stroke();}
        if(m.effect==='drone'){c.fillStyle=col('rede');c.beginPath();c.arc(m.x,m.y,12*(1-age),0,7);c.fill();}
        c.restore();return;
      }
      const r=7+(1-m.life/.48)*10;c.arc(m.x,m.y,r,0,7);c.moveTo(m.x-4,m.y-4);c.lineTo(m.x+4,m.y+4);c.stroke();c.restore();});
    if(S.glow>0){c.save();c.globalAlpha=S.glow*.7;c.strokeStyle=col('akz');c.lineWidth=7;c.shadowColor=col('akz');c.shadowBlur=24;c.strokeRect(3,3,W-6,H-6);c.restore();}
    if(S.flash>0){c.save();c.globalAlpha=clamp(S.flash*1.6,0,.85);c.fillStyle=col('perle');c.fillRect(0,0,W,H);c.restore();}
    if(S.phase==='playing' && S.pointer.in){const {x,y}=S.pointer;c.save();c.translate(x,y);c.strokeStyle=S.reloading?col('akz2'):col('perle');c.lineWidth=1.4;
      c.shadowColor=col('ink');c.shadowBlur=4;c.beginPath();c.arc(0,0,11,0,7);c.moveTo(-19,0);c.lineTo(-5,0);c.moveTo(5,0);c.lineTo(19,0);c.moveTo(0,-19);c.lineTo(0,-5);c.moveTo(0,5);c.lineTo(0,19);c.stroke();c.restore();}
  }
  function sprite(c,name,size) {       // size = the longer side, so a tall bottle and a wide gull both fit their hit zone
    const i=SPRITES[name];
    if (!i) return;
    const k=size/Math.max(i.naturalWidth,i.naturalHeight), w=i.naturalWidth*k, h=i.naturalHeight*k;
    c.drawImage(i,-w/2,-h/2,w,h);
  }
  function drawTarget(c,t) {
    const p=position(t);c.save();c.translate(p.x,p.y);
    c.shadowColor='rgba(0,0,0,.7)';c.shadowBlur=5;
    if(t.type==='bottle') {
      c.rotate(Math.sin(t.age*1.5+t.seed)*.15);
      sprite(c,t.look,74);
      c.strokeStyle='rgba(203,234,229,.45)';c.beginPath();c.ellipse(0,32,24,4,0,0,7);c.stroke();
    } else if(t.type==='clay') {
      c.rotate(t.age*2*t.dir);
      sprite(c,'ton',56);
    } else if(t.type==='drone') {
      sprite(c,'drohne',96);
    } else {
      if(t.type==='flash') {     // the grenade blinks so it can be found
        c.save();c.translate(0,GRANATE_DY);
        c.strokeStyle=col('perle');c.lineWidth=1.5;c.beginPath();c.moveTo(0,-GRANATE_DY+6);c.lineTo(0,-10);c.stroke();
        sprite(c,'granate',32);
        c.globalAlpha=.45+.45*Math.sin(t.age*12);c.fillStyle=col('rede');c.shadowColor=col('rede');c.shadowBlur=14;c.beginPath();c.arc(0,0,3.5,0,7);c.fill();
        c.restore();
      }
      c.scale(t.dir,1);
      sprite(c,'moewe',84);
    }c.restore();
  }
  function update(z) {
    const a=z?.status==='schiessen' && z.schiessen;
    document.body.classList.toggle('schiessen-modus',!!a);
    if (!a) {
      if(S){cancelAnimationFrame(S.raf);S.resize.disconnect();S.box.remove();S=null; if(lastFocus?.isConnected)lastFocus.focus({preventScroll:true});}
      // The scene with a new opponent is over: the round starts by itself.
      if (z?.status==='wahl' && z.holm_wette_folgt && !folgt && !busy()) { folgt=true; setTimeout(()=>{folgt=false;oeffnen();},0); }
      return;
    }
    if(!S) mount(a); else S.data=a;
  }
  return {update,kreis,oeffnen};
})();
