import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class AndroidSetWorkflowContract(unittest.TestCase):
    def test_android_ci_validates_manifest_driven_runtime(self):
        source = (ROOT / '.github/workflows/android.yml').read_text()
        self.assertIn('assets/sets/catalog.json', source)
        self.assertIn('jtrex_sets_runtime.py', source)
        self.assertIn('SCENE_SPECS', source)
        self.assertIn('canonical_set_asset_count', source)
