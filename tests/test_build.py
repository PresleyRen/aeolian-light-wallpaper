"""Packaging regressions: independent formats, valid quality options, no stale media."""
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPO=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('wallpaper_build',REPO/'tools/build.py')
build=importlib.util.module_from_spec(spec);spec.loader.exec_module(build)

class BuildTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        for name in ['src','versions','docs']:shutil.copytree(REPO/name,self.root/name)
        self.assets=self.root/'assets';self.assets.mkdir()
        # These are packaging fixtures; video decoding is covered separately.
        for name in ['still.jpg','eco.webm','background.webm','eco.mp4','background.mp4']:(self.assets/name).write_bytes(b'fixture')
        self.old_root=build.ROOT;build.ROOT=self.root
    def tearDown(self):
        build.ROOT=self.old_root;self.temp.cleanup()
    def run_build(self,*args):
        with patch.object(sys,'argv',['build.py',*args]):build.main()
    def test_windows_interactive_needs_no_mac_media(self):
        (self.assets/'eco.mp4').unlink();(self.assets/'background.mp4').unlink()
        self.run_build('--platform','windows','--mode','interactive')
        target=self.root/'dist/windows/lite-v1'
        project=json.loads((target/'project.json').read_text(encoding='utf-8'))
        props=project['general']['properties']
        self.assertEqual([v['value'] for v in props['quality']['options']],['eco'])
        self.assertEqual(props['particles']['value'],0)
        self.assertTrue((target/'assets/eco.webm').is_file())
    def test_eco_rebuild_drops_only_optional_media(self):
        self.run_build('--platform','muro','--mode','interactive','--quality','both')
        target=self.root/'dist/muro/snow-v2/assets'
        (target/'custom.txt').write_text('keep',encoding='utf-8')
        self.run_build('--platform','muro','--mode','interactive')
        self.assertFalse((target/'background.mp4').exists())
        self.assertTrue((target/'eco.mp4').exists())
        self.assertTrue((target/'custom.txt').exists())
    def test_native_video_needs_no_webm(self):
        (self.assets/'eco.webm').unlink();(self.assets/'background.webm').unlink()
        self.run_build('--platform','windows','--mode','video')
        target=self.root/'dist/windows/video-eco'
        project=json.loads((target/'project.json').read_text(encoding='utf-8'))
        self.assertEqual(project['type'],'video')
        self.assertFalse((target/'app.js').exists())

if __name__=='__main__':unittest.main()
