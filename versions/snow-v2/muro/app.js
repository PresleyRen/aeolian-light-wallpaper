/* Aeolian Light: native video + one small spectrum canvas; no frameworks. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const cfg = Object.assign({}, window.AEOLIAN_CONFIG);
  const video = $('background'), ring = $('spectrum'), snow = $('snow');
  const rc = ring.getContext('2d'), sc = snow.getContext('2d');
  const bands = new Float32Array(64), smooth = new Float32Array(64);
  const clamp = (v,a,b) => Math.min(b,Math.max(a,v));
  const finite = v => Number.isFinite(Number(v)) ? Number(v) : 0;
  let paused = false, hostPaused = false, timer = 0, frame = 0, clockTimer = 0;
  let lastDraw = 0, lastAudio = -Infinity, ringDirty = true, nodes = [], mediaTitle = '', mediaArtist = '';
  let draws = 0, ringDraws = 0, generalFps = 30;
  let audioTimer = 0, audioDeadline = 0;
  const spokes = Array.from({length:64}, (_,i) => {
    const a = Math.PI * i / 63;
    return {x:Math.cos(a),y:Math.sin(a)};
  });
  function updateClock() {
    clearTimeout(clockTimer);
    if (paused) return;
    const now = new Date(), h = now.getHours();
    const text = String(cfg.hour24 ? h : (h % 12 || 12)).padStart(2,'0') + ':' +
      String(now.getMinutes()).padStart(2,'0') + (cfg.seconds ? ':'+String(now.getSeconds()).padStart(2,'0') : '');
    if ($('digits').textContent !== text) $('digits').textContent = text;
    $('period').textContent = cfg.hour24 ? '' : h < 12 ? 'AM' : 'PM';
    const day = cfg.englishDate
      ? now.getDate() + ' ' + ['January','February','March','April','May','June','July','August','September','October','November','December'][now.getMonth()] + ' ' + now.getFullYear()
      : now.getFullYear()+'年'+(now.getMonth()+1)+'月'+now.getDate()+'日';
    if ($('date').textContent !== day) $('date').textContent = day;
    if (cfg.clock || cfg.date) {
      const interval = cfg.seconds ? 1000 : 60000;
      clockTimer = setTimeout(updateClock, interval - Date.now() % interval + 20);
    }
  }
  function updateMedia() {
    $('title').textContent = cfg.media && mediaTitle ? mediaTitle : cfg.caption;
    $('artist').textContent = cfg.media && mediaTitle ? mediaArtist : cfg.captionArtist;
    $('track').hidden = !$('title').textContent && !$('artist').textContent;
  }
  function play() {
    if (!paused) video.play().catch(() => { /* The poster stays visible if autoplay is blocked. */ });
  }
  function selectVideo() {
    const src = cfg.quality === 'eco' ? 'assets/eco.mp4' : 'assets/background.mp4';
    if (video.getAttribute('src') !== src) {
      video.src = src;
      video.load();
      play();
    }
  }
  function resize() {
    // Fixed logical ring and a capped snow backing store, independent of Retina/4K DPR.
    ring.width = 640; ring.height = 320;
    const ratio = Math.min(1, 640 / innerWidth, 360 / innerHeight);
    snow.width = Math.max(1,Math.round(innerWidth*ratio));
    snow.height = Math.max(1,Math.round(innerHeight*ratio));
    nodes = Array.from({length:cfg.particles}, () => ({
      x:Math.random()*snow.width,y:Math.random()*snow.height,
      r:.5+Math.random()*.8,v:6+Math.random()*11,alpha:.2+Math.random()*.4
    }));
    ringDirty = true;
    wake();
  }
  function apply(patch) {
    const previous = {...cfg};
    Object.assign(cfg,patch);
    cfg.fps = clamp(finite(cfg.fps),10,30);
    cfg.particles = Math.round(clamp(finite(cfg.particles),0,80));
    cfg.dim = clamp(finite(cfg.dim),0,.6);
    cfg.sensitivity = clamp(finite(cfg.sensitivity),.1,5);
    cfg.hudScale = clamp(finite(cfg.hudScale),.5,1.5);
    cfg.hudX = clamp(finite(cfg.hudX),0,100); cfg.hudY = clamp(finite(cfg.hudY),0,100);
    const root = document.documentElement.style;
    root.setProperty('--ink',cfg.color);
    root.setProperty('--hud-x',cfg.hudX+'%'); root.setProperty('--hud-y',cfg.hudY+'%');
    root.setProperty('--hud-scale',cfg.hudScale);
    $('shade').style.opacity = cfg.dim;
    $('time').hidden = !cfg.clock; $('date').hidden = !cfg.date;
    ring.hidden = !cfg.spectrum; snow.hidden = !cfg.particles;
    if (!cfg.spectrum) { bands.fill(0); smooth.fill(0); clearTimeout(audioTimer); audioTimer=0; }
    updateMedia(); updateClock(); selectVideo();
    if (previous.particles !== cfg.particles || !ring.width || !snow.width) resize();
    ringDirty = true;
    wake();
  }
  function expireAudio() {
    audioTimer = 0;
    if (paused || !cfg.spectrum) return;
    const remaining = audioDeadline - performance.now();
    if (remaining > 0) {
      audioTimer = setTimeout(expireAudio,remaining + 10);
      return;
    }
    bands.fill(0); ringDirty = true; wake();
  }
  function audio(input) {
    if (paused || !cfg.spectrum || !input) return;
    let changed = false, active = false;
    for (let i=0;i<64;i++) {
      const value = clamp(finite(input[i]),0,1);
      // Silence and sub-pixel differences must not wake a static visualizer.
      const next = value < .002 ? 0 : value;
      if (Math.abs(bands[i]-next) > .002) changed = true;
      if (next) active = true;
      bands[i] = next;
    }
    lastAudio = performance.now();
    if (active) {
      audioDeadline = lastAudio + 450;
      if (!audioTimer) audioTimer = setTimeout(expireAudio,460);
    }
    if (changed) { ringDirty = true; wake(); }
  }
  function drawRing(now,dt) {
    if (!cfg.spectrum) return false;
    if (now-lastAudio > 450) bands.fill(0);
    let moving = false;
    let changed = ringDirty;
    for (let i=0;i<64;i++) {
      const target = clamp(bands[i]*cfg.sensitivity,0,1);
      // Time-based smoothing behaves consistently at 12, 24 and 30fps.
      const blend = 1-Math.exp(-dt*(target>smooth[i]?18:7));
      const before = smooth[i];
      smooth[i] += (target-smooth[i])*blend;
      if (Math.abs(target-smooth[i]) < .001) smooth[i] = target;
      if (before !== smooth[i]) changed = true;
      if (Math.abs(target-smooth[i]) >= .001) moving = true;
    }
    if (!changed) return moving;
    rc.clearRect(0,0,640,320);
    rc.strokeStyle = cfg.color; rc.globalAlpha=.68; rc.lineWidth=1.6;
    rc.beginPath(); rc.arc(320,0,240,0,Math.PI); rc.stroke();
    rc.globalAlpha=.86; rc.lineWidth=2;
    rc.beginPath();
    spokes.forEach((s,i) => {
      const base=242, len=4 + (i%8===0?12:0) + smooth[i]*46;
      rc.moveTo(320+s.x*base,s.y*base);
      rc.lineTo(320+s.x*(base+len),s.y*(base+len));
    });
    rc.stroke(); rc.globalAlpha=1;
    ringDirty=false; ringDraws++;
    return moving;
  }
  function drawSnow(dt) {
    if (!cfg.particles) return;
    sc.clearRect(0,0,snow.width,snow.height);
    sc.fillStyle=cfg.color;
    for (const n of nodes) {
      n.y += n.v*dt; n.x += 2*dt;
      if (n.y>snow.height+2) { n.y=-2; n.x=Math.random()*snow.width; }
      if (n.x>snow.width+2) n.x=-2;
      sc.globalAlpha=n.alpha;
      sc.beginPath(); sc.arc(n.x,n.y,n.r,0,Math.PI*2); sc.fill();
    }
    sc.globalAlpha=1;
  }
  function render(now) {
    frame=0;
    if (paused) return;
    const dt = lastDraw ? Math.max(0,(now-lastDraw)/1000) : 1/cfg.fps;
    lastDraw=now;
    const moving=drawRing(now,dt);
    drawSnow(Math.min(.15,dt)); draws++;
    if (cfg.particles || (cfg.spectrum && moving)) wake();
  }
  function wake() {
    if (paused || timer || frame) return;
    const fps=Math.min(cfg.fps,generalFps,cfg.quality==='eco'?12:30);
    const delay=Math.max(0,1000/fps-(performance.now()-lastDraw));
    timer=setTimeout(() => { timer=0; frame=requestAnimationFrame(render); },delay);
  }
  function pause(value) {
    hostPaused=Boolean(value); syncPause();
  }
  function syncPause() {
    paused=hostPaused || document.hidden;
    clearTimeout(timer); timer=0; cancelAnimationFrame(frame); frame=0;
    clearTimeout(clockTimer); clockTimer=0;
    clearTimeout(audioTimer); audioTimer=0;
    if (paused) video.pause();
    else { lastDraw=0; lastAudio=-Infinity; bands.fill(0); smooth.fill(0); ringDirty=true; updateClock(); play(); wake(); }
  }
  addEventListener('resize',resize);
  document.addEventListener('visibilitychange',syncPause);
  video.addEventListener('loadeddata',() => { if (paused) video.pause(); else play(); });
  window.Aeolian = {
    apply,audio,pause,
    generalFps(value) { generalFps=clamp(finite(value),1,30); },
    media(title,artist) { mediaTitle=String(title||''); mediaArtist=String(artist||''); updateMedia(); },
    diagnostics() { return {paused,draws,ringDraws,scheduled:Boolean(timer||frame),audioScheduled:Boolean(audioTimer),config:{...cfg},video:{paused:video.paused,width:video.videoWidth,height:video.videoHeight,error:video.error?.code||0},canvas:[ring.width,ring.height,snow.width,snow.height],bands:Array.from(smooth)}; }
  };
  resize();
  apply({});
  syncPause();
})();
