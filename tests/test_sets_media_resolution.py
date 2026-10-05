import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tests'))
from runtime_harness import Harness


class SetMediaResolutionTests(unittest.TestCase):
    def test_scene_specs_are_engine_policy_without_file_paths(self):
        h = Harness()
        specs = h.runtime.SCENE_SPECS
        self.assertIn('zero-win', specs)
        self.assertTrue(all('file' not in spec for spec in specs.values()))
        self.assertTrue(any(spec.get('play_to_end') for spec in specs.values()))

    def test_intro_paths_come_from_selection(self):
        h = Harness()
        self.assertEqual(h.media.selection.intro_paths(), (
            'assets/intro/JTrexintro1.mp4',
            'assets/intro/JTrexintro2.mp4',
            'assets/intro/JTrexintro3.mp4',
        ))

    def test_all_canonical_states_resolve_same_paths(self):
        h = Harness()
        expected = {
            1:'assets/combat/StegTrexPlageVideoenboucledesorbes.mp4',
            2:'assets/combat/Chargestegtrexchargerougebleucorrected.mp4',
            5:'assets/combat/Stegtrexegalitechargeboutonjaune.mp4',
            -7:'assets/combat/Zerowinstegtrexsurleschargedejaugejauneetbleuetrouge.mp4',
            8:'assets/combat/Stegtrexresultstegwin.mp4', 9:'assets/combat/Stegtrexresulttrexwin.mp4',
            10:'assets/finishing/steg-finishing-trex.mp4', 11:'assets/finishing/trex-finishing-steg.mp4',
            21:'assets/powers/stsf-sanctuary-force.mp4', 22:'assets/powers/stls-lifestream.mp4',
            23:'assets/powers/stta-tornado-attack.mp4', 24:'assets/powers/trfs-fire-storm.mp4',
            25:'assets/powers/trph-phoenix-attack.mp4', 26:'assets/powers/trma-meteor-attack.mp4',
        }
        for state, path in expected.items():
            key = h.media._key_for_state(state)
            self.assertEqual(h.media._scene_config(key)['file'], path)

    def test_phase_runtime_no_longer_mutates_global_scene_catalog(self):
        source = (ROOT / 'tools/jtrex_phase_runtime.py').read_text()
        self.assertNotIn('_install_zero_win_scene', source)
        self.assertNotIn('__globals__["SCENES"]', source)

    def test_controllers_have_independent_selection_objects(self):
        h1, h2 = Harness(), Harness()
        self.assertIsNot(h1.media.selection, h2.media.selection)
        self.assertEqual(h1.runtime.SCENE_SPECS, h2.runtime.SCENE_SPECS)
