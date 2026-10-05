import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'assets/sets/trex_vs_steg/manifest.json'


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


class MediaAssetSizeGuardTests(unittest.TestCase):
    def test_declared_media_sizes_match_repository_assets(self):
        manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
        mismatches = []
        for asset in manifest['assets']:
            relative = asset['path']
            if not relative.startswith('assets/'):
                continue
            path = ROOT / relative
            if not path.is_file():
                mismatches.append((relative, 'missing'))
                continue
            if path.stat().st_size != asset['size']:
                mismatches.append((relative, 'size', asset['size'], path.stat().st_size))
            actual_sha = digest(path)
            if actual_sha != asset['sha256']:
                mismatches.append((relative, 'sha256', asset['sha256'], actual_sha))
        self.assertEqual([], mismatches)


if __name__ == '__main__':
    unittest.main()
