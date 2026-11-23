"""Prepare local-only media; no downloads of artwork or videos."""
import argparse
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', required=True, type=Path)
parser.add_argument('--ffmpeg', default=None)
args = parser.parse_args()
source = args.source.resolve()
if not source.is_file():
    parser.error('Source video does not exist')
ffmpeg = args.ffmpeg or shutil.which('ffmpeg')
if not ffmpeg:
    try:
        import imageio_ffmpeg
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        parser.error('Install FFmpeg or imageio-ffmpeg first')
out = ROOT/'assets'
out.mkdir(exist_ok=True)

def run(options, target):
    subprocess.run([ffmpeg, '-y', '-hide_banner', '-loglevel', 'warning', '-i', str(source),
                    '-map', '0:v:0']+options+['-an', str(out/target)], check=True)

# Transcode rather than relabel arbitrary inputs. Both WebMs are VP9 profile 0.
for name, filt, quality in [('background.webm', 'fps=30000/1001', '30'),
                             ('eco.webm', 'scale=1280:720:flags=lanczos,fps=24', '33')]:
    run(['-vf', filt, '-c:v', 'libvpx-vp9', '-crf', quality, '-b:v', '0',
         '-deadline', 'good', '-cpu-used', '4', '-row-mt', '1', '-pix_fmt', 'yuv420p'], name)
for name, filt, quality in [('background.mp4', 'fps=30000/1001', '21'),
                             ('eco.mp4', 'scale=1280:720:flags=lanczos,fps=24', '22')]:
    run(['-vf', filt, '-c:v', 'libx264', '-crf', quality, '-preset', 'fast',
         '-pix_fmt', 'yuv420p', '-movflags', '+faststart'], name)
subprocess.run([ffmpeg, '-y', '-hide_banner', '-loglevel', 'error', '-i', str(source),
                '-frames:v', '1', '-q:v', '3', str(out/'still.jpg')], check=True)
print('Prepared local assets in', out)
