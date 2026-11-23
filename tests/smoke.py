"""Check every generated interactive platform/profile in a real browser."""
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root',type=Path,default=Path('dist'))
parser.add_argument('--chrome',action='store_true',help='Use installed Google Chrome')
parser.add_argument('--browser',choices=['chromium','webkit'],default='chromium')
args=parser.parse_args()
with sync_playwright() as p:
    engine=getattr(p,args.browser)
    browser=engine.launch(headless=True,**({'channel':'chrome'} if args.chrome and args.browser=='chromium' else {}))
    for platform in (['muro'] if args.browser=='webkit' else ['windows','muro']):
        for profile in ['lite-v1','snow-v2']:
            page=browser.new_page(viewport={'width':1920,'height':1080},device_scale_factor=2)
            errors=[];network=[]
            page.on('pageerror',lambda error:errors.append(str(error)))
            page.on('request',lambda request:network.append(request.url) if request.url.startswith(('http:','https:')) else None)
            page.add_init_script('''window.wallpaperRegisterAudioListener=fn=>window.pushAudio=fn;
                window.snowFills=0;const fill=CanvasRenderingContext2D.prototype.fill;
                CanvasRenderingContext2D.prototype.fill=function(...args){if(this.canvas.id==='snow')window.snowFills++;return fill.apply(this,args)};''')
            page.goto((args.root/platform/profile/'index.html').resolve().as_uri(),wait_until='domcontentloaded')
            page.wait_for_function('window.Aeolian && document.querySelector("video").readyState>=2')
            expected=0 if profile=='lite-v1' else 24
            assert page.evaluate('Aeolian.diagnostics().config.particles')==expected
            assert page.evaluate('Aeolian.diagnostics().config.quality')=='eco'
            if expected:
                a=page.evaluate('Aeolian.diagnostics().draws');f=page.evaluate('snowFills')
                page.wait_for_timeout(500)
                d=page.evaluate('Aeolian.diagnostics().draws')-a
                assert d>0 and page.evaluate('snowFills')-f<=3*(d+1),'snow must use at most three fill batches'
            else:assert page.evaluate('Aeolian.diagnostics().canvas.slice(2)')==[1,1]
            page.evaluate('Aeolian.apply({particles:0,spectrum:false})')
            page.wait_for_timeout(150)
            assert page.evaluate('Aeolian.diagnostics().canvas')==[1,1,1,1],'disabled canvases must release backing stores'
            assert not page.evaluate('Aeolian.acceptsAudio()')
            page.evaluate('Aeolian.apply({spectrum:true})')
            page.wait_for_timeout(150)
            assert page.evaluate('Aeolian.diagnostics().canvas.slice(0,2)')==[640,320]
            a=page.evaluate('Aeolian.diagnostics().draws')
            page.evaluate('Aeolian.apply({fps:12}); Aeolian.apply({fps:12})')
            page.wait_for_timeout(200)
            assert page.evaluate('Aeolian.diagnostics().draws')==a,'unchanged settings must not redraw'
            if platform=='windows':
                send='pushAudio(new Array(128).fill(0))'
                pause='wallpaperPropertyListener.setPaused(true)'
                resume='wallpaperPropertyListener.setPaused(false)'
                active='pushAudio(new Array(128).fill(.4))'
            else:
                send='dispatchEvent(new CustomEvent("muro:audio",{detail:{bands:new Array(64).fill(0)}}))'
                pause='dispatchEvent(new CustomEvent("muro:pause"))'
                resume='dispatchEvent(new CustomEvent("muro:resume"))'
                active='dispatchEvent(new CustomEvent("muro:audio",{detail:{bands:new Array(64).fill(.4)}}))'
            page.evaluate('window.quiet=setInterval(()=>{'+send+'},33)')
            before=page.evaluate('Aeolian.diagnostics().ringDraws');page.wait_for_timeout(600)
            assert page.evaluate('Aeolian.diagnostics().ringDraws')==before,'silent callbacks must not redraw'
            page.evaluate('clearInterval(quiet)');page.evaluate(active)
            page.wait_for_function('Math.max(...Aeolian.diagnostics().bands)>.05')
            page.evaluate(resume)
            assert page.evaluate('Math.max(...Aeolian.diagnostics().bands)>.05'),'duplicate resume must preserve active audio'
            page.wait_for_function('Math.max(...Aeolian.diagnostics().bands)<.0011',timeout=5000)
            page.evaluate('Aeolian.apply({particles:24})');page.evaluate(active);page.evaluate(pause)
            before=page.evaluate('Aeolian.diagnostics().draws');page.wait_for_timeout(400)
            state=page.evaluate('Aeolian.diagnostics()')
            assert state['draws']==before and state['video']['paused']
            assert not state['scheduled'] and not state['audioScheduled']
            page.evaluate(active)
            assert page.evaluate('Aeolian.diagnostics().draws')==before
            page.evaluate(resume);page.wait_for_function('!Aeolian.diagnostics().video.paused')
            page.evaluate('Aeolian.apply({hour24:true,englishDate:false})')
            assert page.locator('#period').inner_text()=='' and '年' in page.locator('#date').inner_text()
            for width,height in [(1440,900),(3440,1440),(1080,1920)]:
                page.set_viewport_size({'width':width,'height':height});page.wait_for_timeout(80)
                assert page.evaluate('document.documentElement.scrollWidth===innerWidth && document.documentElement.scrollHeight===innerHeight')
            assert not errors,errors
            assert not network,network
            page.close();print(platform+'/'+profile+': PASS',flush=True)
    browser.close()
