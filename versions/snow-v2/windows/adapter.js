// Wallpaper Engine integration. Register immediately, once, outside onload.
window.wallpaperPropertyListener = {
  applyUserProperties(properties) {
    const patch = {};
    for (const key of ['fps','clock','date','hour24','seconds','englishDate','spectrum','sensitivity','particles','dim','hudX','hudY','hudScale','media','caption','captionArtist']) {
      if (properties[key]) patch[key] = properties[key].value;
    }
    if (properties.quality) patch.quality = properties.quality.value;
    if (properties.color) {
      const values=String(properties.color.value).split(' ').map(v=>Math.round(Math.min(1,Math.max(0,Number(v)||0))*255));
      if (values.length===3) patch.color='rgb('+values.join(',')+')';
    }
    window.Aeolian.apply(patch);
  },
  applyGeneralProperties(properties) { if (properties.fps !== undefined) window.Aeolian.generalFps(properties.fps); },
  setPaused(isPaused) { window.Aeolian.pause(isPaused); }
};
if (typeof window.wallpaperRegisterAudioListener === 'function') {
  const mono=new Float32Array(64);
  window.wallpaperRegisterAudioListener(values => {
    const state=window.Aeolian;
    // The core ignores host audio while paused; reuse the same mono buffer.
    for(let i=0;i<64;i++) mono[i]=((values[i]||0)+(values[i+64]||0))*.5;
    state.audio(mono);
  });
}
if (typeof window.wallpaperRegisterMediaPropertiesListener === 'function') {
  window.wallpaperRegisterMediaPropertiesListener(event => window.Aeolian.media(event.title,event.artist));
}
if (typeof window.wallpaperRegisterMediaStatusListener === 'function') {
  window.wallpaperRegisterMediaStatusListener(event => { if (!event.enabled) window.Aeolian.media('',''); });
}
