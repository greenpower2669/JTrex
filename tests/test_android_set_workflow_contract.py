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

    def test_android_ci_validates_lot03_frozen_session_contract(self):
        source = (ROOT / '.github/workflows/android.yml').read_text()
        runtime_guard = source.split('required_runtime = (', 1)[1].split('for token in required_runtime:', 1)[0]
        main_guard = source.split('required_main = (', 1)[1].split('for token in required_main:', 1)[0]
        for token in (
            'JTSetSessionManager',
            'self.sets = JTSetSessionManager',
            'def on_phase_changed',
            'def select_official_set',
            'def _apply_session_power_identity',
            'startup_intro_set',
        ):
            self.assertIn(token, runtime_guard)
        self.assertNotIn('"load_official_set"', runtime_guard)
        self.assertIn('def jt_apply_power_paths(paths):', main_guard)
        self.assertIn('source=JT_POWER_PATHS', main_guard)
        self.assertIn('main.count("source=JT_POWER_PATHS") != 12', source)

    def test_android_ci_validates_lot06_parameter_contract(self):
        source = (ROOT / '.github/workflows/android.yml').read_text()
        self.assertIn('POWER_PARAMETER_SPECS', source)
        self.assertIn('power_effect_fraction', source)
        self.assertNotIn('parameters are closed in v1', source)
