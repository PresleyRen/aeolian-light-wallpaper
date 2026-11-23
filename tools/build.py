"""Build self-contained platform/profile folders from one shared runtime."""
import argparse
import html
import json
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROFILES = ['lite-v1', 'snow-v2']
PLATFORMS = ['windows', 'muro']

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', choices=PROFILES+['all'], default='all')
    parser.add_argument('--platform', choices=PLATFORMS+['all'], default='all')
    parser.add_argument('--quality', choices=['eco', 'balanced', 'both'], default='eco')
    parser.add_argument('--mode', choices=['interactive', 'video', 'all'], default='all')
    parser.add_argument('--assets', type=Path, default=ROOT/'assets')
    parser.add_argument('--zip', action='store_true', help='Create independent ZIPs in dist/packages')
    args = parser.parse_args()
    platforms = PLATFORMS if args.platform=='all' else [args.platform]
    profiles = PROFILES if args.version=='all' else [args.version]
    qualities = ['eco','balanced'] if args.quality=='both' else [args.quality]
    assets = args.assets.resolve()
    interactive = args.mode in ['interactive','all']
    native = args.mode in ['video','all']
    formats = {'webm' if p=='windows' else 'mp4' for p in platforms} if interactive else set()
    if native: formats.add('mp4')
    required = {'still.jpg'} | {('eco' if q=='eco' else 'background')+'.'+ext for q in qualities for ext in formats}
    missing = sorted(name for name in required if not (assets/name).is_file())
    if missing: parser.error('Missing local media: '+', '.join(missing)+'. See docs/build.md.')
    built = []
    for platform in platforms:
        ext = 'webm' if platform=='windows' else 'mp4'
        if interactive:
            for profile in profiles:
                dest = ROOT/'dist'/platform/profile
                (dest/'assets').mkdir(parents=True, exist_ok=True)
                for name in ['style.css','app.js']:
                    shutil.copy2(ROOT/'src'/name, dest/name)
                shutil.copy2(ROOT/'src/adapters'/f'{platform}.js', dest/'adapter.js')
                defaults = load(ROOT/'src/defaults.json')
                settings = load(ROOT/'versions'/profile/'profile.json')
                defaults.update(settings['defaults'])
                poster='preview.jpg' if platform=='windows' else 'still.jpg'
                title='Aeolian Light · '+profile+' · '+settings['title']+' · '+('Windows' if platform=='windows' else 'Muro')
                page=(ROOT/'src/index.html').read_text(encoding='utf-8').replace('__TITLE__',html.escape(title)).replace('__POSTER__',poster)
                (dest/'index.html').write_text(page,encoding='utf-8')
                defaults['quality'] = 'eco' if 'eco' in qualities else 'balanced'
                defaults['videoSources'] = {q:'assets/'+('eco' if q=='eco' else 'background')+'.'+ext for q in qualities}
                (dest/'config.js').write_text('// Settings and local videos; see docs/configuration.md.\nwindow.AEOLIAN_CONFIG = '+json.dumps(defaults,ensure_ascii=False,indent=2)+';\n', encoding='utf-8')
                # Remove only known optional media from a previous build of this target.
                for name in ['eco.webm','background.webm','eco.mp4','background.mp4']:
                    p=dest/'assets'/name
                    if p.is_file() and name not in {Path(v).name for v in defaults['videoSources'].values()}: p.unlink()
                for name in [Path(v).name for v in defaults['videoSources'].values()]:
                    shutil.copy2(assets/name, dest/'assets'/name)
                shutil.copy2(assets/'still.jpg',dest/poster)
                # Known generated duplicates from earlier builds; the active poster remains above.
                for name in ['assets/still.jpg','使用说明.md','still.jpg' if platform=='windows' else 'preview.jpg']:
                    duplicate=dest/name
                    if duplicate.is_file():duplicate.unlink()
                if platform=='windows':
                    props = load(ROOT/'src/properties.json')
                    for key,value in defaults.items():
                        if key in props and key!='color': props[key]['value']=value
                    props['particles']['text']='额外雪花数量（默认'+str(defaults['particles'])+'）'
                    props['quality']['options']=[o for o in props['quality']['options'] if o['value'] in qualities]
                    write_json(dest/'project.json',dict(title='Aeolian Light | '+profile+' | '+settings['title'],type='web',file='index.html',preview='preview.jpg',contentrating='Everyone',description='轻量时钟、日期与音乐频谱；请将其他应用获得焦点设为暂停。',general=dict(properties=props,supportsaudioprocessing=True)))
                guide=(ROOT/'docs'/f'{platform}.md').read_text(encoding='utf-8')
                guide=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:m[1]+'：'+(m[2] if m[2].startswith('http') else 'https://github.com/PresleyRen/aeolian-light-wallpaper/blob/main/docs/'+m[2]),guide)
                guide=re.sub(r'^#+\s*|^```.*$', '',guide,flags=re.M).replace('**','').replace('`','')
                (dest/'使用说明.txt').write_text(guide+'\n\n当前版本：'+profile+'，额外雪花：'+str(defaults['particles'])+'，默认特效帧率：'+str(defaults['fps'])+'。\n',encoding='utf-8-sig')
                required_files=['index.html','style.css','app.js','adapter.js','config.js',poster,'使用说明.txt']+list(defaults['videoSources'].values())
                if platform=='windows':required_files.append('project.json')
                built.append((dest,required_files))
        if native:
            for quality in qualities:
                dest=ROOT/'dist'/platform/('video-'+quality)
                dest.mkdir(parents=True,exist_ok=True)
                shutil.copy2(assets/('eco.mp4' if quality=='eco' else 'background.mp4'),dest/'wallpaper.mp4')
                required_files=['wallpaper.mp4','使用说明.txt']
                if platform=='windows':
                    shutil.copy2(assets/'still.jpg',dest/'preview.jpg')
                    write_json(dest/'project.json',dict(title='Aeolian Light | 纯视频 '+quality,type='video',file='wallpaper.mp4',preview='preview.jpg',contentrating='Everyone'))
                    required_files+=['project.json','preview.jpg']
                elif (dest/'preview.jpg').is_file():(dest/'preview.jpg').unlink()
                host='Wallpaper Engine' if platform=='windows' else 'Muro'
                (dest/'使用说明.txt').write_text('纯视频添加教程\n1. 先解压完整ZIP。\n2. 打开'+host+'的壁纸资料库，将wallpaper.mp4拖入或通过添加/导入入口选择此文件。\n3. 选择导入的视频并应用到桌面。\n4. 如需只在桌面时播放，Windows设置“其他应用获得焦点：暂停”；Muro开启Play only on desktop。\n纯视频保留原片动态与原片中的雪花，没有实时时钟、日期、歌名或音乐频谱。\n',encoding='utf-8-sig')
                built.append((dest,required_files))
    for dest,required_files in built:
        if args.zip:
            package=ROOT/'dist/packages'/('-'.join(dest.relative_to(ROOT/'dist').parts)+'.zip')
            package.parent.mkdir(exist_ok=True)
            with zipfile.ZipFile(package,'w') as archive:
                prefix=Path('-'.join(dest.relative_to(ROOT/'dist').parts))
                for name in required_files:
                    f=dest/name
                    archive.write(f,prefix/name,compress_type=zipfile.ZIP_STORED if f.suffix in ['.mp4','.webm','.jpg'] else zipfile.ZIP_DEFLATED)
        print(dest)

if __name__=='__main__': main()
