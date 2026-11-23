"""Sample page metrics: video-only is still a web page, not native host playback."""
import json,time,argparse
from pathlib import Path
R=Path(__file__).resolve().parent.parent
from playwright.sync_api import sync_playwright
parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=R/'dist/windows/snow-v2');parser.add_argument('--out',type=Path,default=R/'performance.json');parser.add_argument('--seconds',type=float,default=3);parser.add_argument('--chrome',action='store_true',help='Use installed Google Chrome')
a=parser.parse_args();rows=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,**({'channel':'chrome'} if a.chrome else {}))
 for case in ['video-only','snow-silent','snow-music','paused']:
  for repeat in range(3):
   page=browser.new_page(viewport={'width':1920,'height':1080},device_scale_factor=2)
   page.add_init_script('window.wallpaperRegisterAudioListener=fn=>window.sendAudio=fn')
   page.goto((a.root/'index.html').resolve().as_uri());page.wait_for_function('window.Aeolian && document.querySelector("video").readyState>=2')
   if case=='video-only':page.evaluate('Aeolian.apply({particles:0,spectrum:false})')
   if case=='snow-music':page.evaluate('window.pump=setInterval(()=>sendAudio(Array.from({length:128},(_,i)=>.4+.3*Math.sin(performance.now()/250+i/8))),33)')
   if case=='paused':page.evaluate('Aeolian.pause(true)')
   page.wait_for_timeout(500)
   cdp=page.context.new_cdp_session(page);cdp.send('Performance.enable')
   metrics=lambda:{x['name']:x['value'] for x in cdp.send('Performance.getMetrics')['metrics']}
   start=metrics();d0=page.evaluate('Aeolian.diagnostics()');t=time.perf_counter();page.wait_for_timeout(a.seconds*1000);elapsed=time.perf_counter()-t;end=metrics();d=page.evaluate('Aeolian.diagnostics()')
   row={'case':case,'repeat':repeat,'seconds':round(elapsed,3),'scriptMs':round((end['ScriptDuration']-start['ScriptDuration'])*1000,3),'taskMs':round((end['TaskDuration']-start['TaskDuration'])*1000,3),'jsHeapMiB':round(end['JSHeapUsedSize']/1048576,3),'draws':d['draws']-d0['draws'],'ringDraws':d['ringDraws']-d0['ringDraws'],'canvasPixels':sum(d['canvas'][i]*d['canvas'][i+1] for i in [0,2])}
   rows.append(row);print(json.dumps(row),flush=True);page.close()
 browser.close()
a.out.write_text(json.dumps({'browser':'Chromium headless; CDP main renderer metrics, not total process memory or GPU utilization','rows':rows},indent=2),encoding='utf-8')
