// Muro InteractiveBridge API: offline, no Spotify token or network service.
window.addEventListener('muro:audio',event => window.Aeolian.audio(event.detail?.bands));
window.addEventListener('muro:pause',() => window.Aeolian.pause(true));
window.addEventListener('muro:resume',() => window.Aeolian.pause(false));
if (window.muro?.paused) window.Aeolian.pause(true);
