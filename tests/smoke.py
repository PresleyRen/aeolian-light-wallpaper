"""Integration regressions for snow-v2 with actual browser rendering."""
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root', type=Path, default=Path('dist/snow-v2'))
parser.add_argument('--chrome', action='store_true', help='Use installed Google Chrome')
args = parser.parse_args()
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, **({'channel': 'chrome'} if args.chrome else {}))
    for platform in ['windows', 'muro']:
        page = browser.new_page()
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.add_init_script('window.wallpaperRegisterAudioListener=fn=>window.pushAudio=fn')
        page.goto((args.root/platform/'index.html').resolve().as_uri())
        page.wait_for_function('window.Aeolian && document.querySelector("video").readyState>=2')
        assert page.evaluate('Aeolian.diagnostics().config.particles') == 24
        a = page.evaluate('Aeolian.diagnostics().draws')
        page.wait_for_timeout(500)
        assert page.evaluate('Aeolian.diagnostics().draws') > a, 'snow must animate'
        page.evaluate('Aeolian.apply({particles:0})')
        page.wait_for_timeout(200)
        if platform == 'windows':
            send = 'pushAudio(new Array(128).fill(0))'
            pause = 'wallpaperPropertyListener.setPaused(true)'
            resume = 'wallpaperPropertyListener.setPaused(false)'
            active = 'pushAudio(new Array(128).fill(.4))'
        else:
            send = 'dispatchEvent(new CustomEvent("muro:audio",{detail:{bands:new Array(64).fill(0)}}))'
            pause = 'dispatchEvent(new CustomEvent("muro:pause"))'
            resume = 'dispatchEvent(new CustomEvent("muro:resume"))'
            active = 'dispatchEvent(new CustomEvent("muro:audio",{detail:{bands:new Array(64).fill(.4)}}))'
        page.evaluate('window.quiet=setInterval(()=>{'+send+'},33)')
        before = page.evaluate('Aeolian.diagnostics().ringDraws')
        page.wait_for_timeout(600)
        assert page.evaluate('Aeolian.diagnostics().ringDraws') == before, 'silent callbacks must not redraw'
        page.evaluate('clearInterval(quiet)')
        page.evaluate(active)
        page.wait_for_function('Math.max(...Aeolian.diagnostics().bands)>.05')
        page.wait_for_function('Math.max(...Aeolian.diagnostics().bands)<.0011', timeout=5000)
        page.evaluate('Aeolian.apply({particles:24})')
        page.evaluate(active)
        page.evaluate(pause)
        before = page.evaluate('Aeolian.diagnostics().draws')
        page.wait_for_timeout(400)
        state = page.evaluate('Aeolian.diagnostics()')
        assert state['draws'] == before and state['video']['paused']
        assert not state['scheduled'] and not state['audioScheduled']
        page.evaluate(active)  # ignored while an app is focused
        assert page.evaluate('Aeolian.diagnostics().draws') == before
        page.evaluate(resume)
        page.wait_for_function('!Aeolian.diagnostics().video.paused')
        assert not errors, errors
        page.close()
        print(platform+': snow, silence, expiry, pause/resume PASS')
    browser.close()
