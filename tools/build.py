"""Build either preserved source version with locally prepared media."""
import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--version', choices=['lite-v1', 'snow-v2'], default='snow-v2')
parser.add_argument('--assets', type=Path, default=ROOT/'assets')
args = parser.parse_args()
assets = args.assets.resolve()
required = ['background.webm', 'eco.webm', 'background.mp4', 'eco.mp4', 'still.jpg']
missing = [name for name in required if not (assets/name).is_file()]
if missing:
    parser.error('Missing local media: '+', '.join(missing)+'. Run tools/prepare_media.py first.')

for platform in ['windows', 'muro']:
    source = ROOT/'versions'/args.version/platform
    dest = ROOT/'dist'/args.version/platform
    shutil.copytree(source, dest, dirs_exist_ok=True)
    selected = ['background.webm', 'eco.webm'] if platform == 'windows' else ['background.mp4', 'eco.mp4']
    for name in selected+['still.jpg']:
        shutil.copy2(assets/name, dest/'assets'/name)
    shutil.copy2(assets/'still.jpg', dest/'preview.jpg')
    if platform == 'muro':
        shutil.copy2(assets/'still.jpg', dest/'still.jpg')
    else:
        project_path = dest/'project.json'
        project = json.loads(project_path.read_text(encoding='utf-8'))
        project['title'] = 'Aeolian Light | '+args.version
        project_path.write_text(json.dumps(project, ensure_ascii=False, indent=2), encoding='utf-8')
    print(dest)
