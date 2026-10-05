import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class OrbMediaManifestCanon(unittest.TestCase):
    def test_beach_loop_is_guarded_by_canonical_set_manifest(self):
        manifest = json.loads((ROOT / 'assets/sets/trex_vs_steg/manifest.json').read_text(encoding='utf-8'))
        assets = {entry['id']: entry for entry in manifest['assets']}
        asset = assets[manifest['media']['orbs_background']]
        self.assertEqual(asset['path'], 'assets/combat/StegTrexPlageVideoenboucledesorbes.mp4')
        self.assertEqual(asset['size'], 9848376)
        self.assertEqual(asset['sha256'], '71b1abe5498d7e9f5dfd61cccede099759c49ec0a82324e8dd76b8c054dccd9d')

    def test_legacy_wait_media_is_retired_from_active_candidate(self):
        legacy = ROOT / 'assets/combat/StegVsTrexvaetviensremolacebisorigune.mp4'
        self.assertFalse(legacy.exists())
        runtime = (ROOT / 'tools/jtrex_media_runtime.py').read_text(encoding='utf-8')
        manifest = (ROOT / 'assets/sets/trex_vs_steg/manifest.json').read_text(encoding='utf-8')
        self.assertNotIn('StegVsTrexvaetviensremolace', runtime)
        self.assertNotIn('StegVsTrexvaetviensremolace', manifest)


if __name__ == '__main__':
    unittest.main()
