import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class SetPackagingTests(unittest.TestCase):
    def test_buildozer_embeds_json(self):
        text = (ROOT / 'buildozer.spec').read_text()
        line = next(line for line in text.splitlines() if line.startswith('source.include_exts'))
        self.assertIn('json', {part.strip() for part in line.split('=',1)[1].split(',')})

    def test_preparer_uses_manifest_not_manual_media_assets(self):
        source = (ROOT / 'tools/prepare_android.py').read_text()
        self.assertNotIn('MEDIA_ASSETS = {', source)
        self.assertIn('load_official_set', source)
        self.assertIn('selection.assets()', source)

    def test_preparer_packages_set_runtime_and_json(self):
        source = (ROOT / 'tools/prepare_android.py').read_text()
        for token in ('jtrex_sets_runtime.py', 'CATALOG_PATH', 'selection.manifest_path', 'canonical_manifest_sha256'):
            self.assertIn(token, source)

    def test_preparer_reports_set_asset_integrity(self):
        source = (ROOT / 'tools/prepare_android.py').read_text()
        for token in ('canonical_set_id', 'canonical_set_asset_count', 'canonical_set_assets'):
            self.assertIn(token, source)
        self.assertIn('digest(target)', source)
