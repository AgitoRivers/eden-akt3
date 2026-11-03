"""Existing-image preparation only: catalog integrity, source hashes, transparent complete sets."""
import hashlib
import json
from pathlib import Path
import unittest
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'docs/effekt-auswahl/status-labor/assets'
CATALOG=json.loads((ASSETS/'duc-varianten-v1/katalog.json').read_text(encoding='utf-8'))

class DucSprites(unittest.TestCase):
    def test_all_looks_weapons_and_poses_are_complete(self):
        self.assertEqual(len(CATALOG['sets']),26)   # 25 Duc-Looks x Waffen + Maxwell mit Steel Mop (1da54f2e)
        self.assertEqual(len({(s['look'],s['weapon']) for s in CATALOG['sets']}),26)   # 25 Duc-Looks x Waffen + Maxwell mit Steel Mop (1da54f2e)
        for item in CATALOG['sets']:
            folder=ASSETS/item['directory']
            anchors=json.loads((folder/'posen.json').read_text(encoding='utf-8'))
            self.assertEqual(len(item['poses']),13)
            for pose in item['poses']:
                self.assertFalse(anchors[pose]['mirror'])
                with Image.open(folder/(pose+'.webp')) as im:
                    self.assertEqual(im.size,(1170,1000) if item['look']!='Maxwell' else (1053,900));self.assertEqual(im.mode,'RGBA')   # Maxwell kleiner (1da54f2e)
                    self.assertEqual(im.getchannel('A').getextrema(),(0,255))
            for pose in ('idle','hurt','guard'):
                self.assertTrue((folder/('gegner_'+pose+'.webp')).is_file())

    def test_source_files_match_recorded_hashes(self):
        self.assertTrue(CATALOG['sourceUnmodified'])
        for item in CATALOG['sets']:
            for pose in item['sourcePoses']:
                self.assertEqual(hashlib.sha256(Path(pose['source']).read_bytes()).hexdigest(),pose['sha256'])

if __name__=='__main__':unittest.main()
