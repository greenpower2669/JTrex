import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tests'))

from jtrex_sets_runtime import POWER_KEYS, load_official_set
from runtime_harness import Harness
from tests.test_sets_media_session import build_media, make_two_set_root


def load_preparer():
    spec = importlib.util.spec_from_file_location('prep_lot06', ROOT / 'tools/prepare_android.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def repo_resolve(relative):
    path = ROOT / relative
    return str(path) if path.is_file() else None


def values(overrides=None):
    table = {1: 0.25, 2: 0.25, 3: 0.25, 4: 0.25, 5: 0.25, 6: 1.0 / 3.0}
    table.update(overrides or {})
    return table


def trigger_power_impact(harness, state, marker):
    harness.state(state)
    harness.frame()
    harness.ns['anim1'] = marker - 1
    harness.ns['anim1vv'] = 1
    harness.root.mc1(.03)
    harness.root.mc1(.03)


class PowerParameterIntegrationTests(unittest.TestCase):
    def test_preparer_builds_normalized_six_slot_effect_table(self):
        prep = load_preparer()
        selection = load_official_set(repo_resolve)
        self.assertEqual(prep.build_power_parameter_table(selection), values())

    def test_rewriter_changes_only_the_six_historical_power_effect_writes(self):
        prep = load_preparer()
        source = '''\n\t\tif anim1==181:\n\t\t\tdegd+=pvd/4\n\t\tif anim1==182:\n\t\t\tdegg-=pvg/4\n\t\tif anim1==183:\n\t\t\tdegd+=pvd/4\n\t\tif anim1==184:\n\t\t\tdegg+=pvg/4\n\t\tif anim1==185:\n\t\t\tdegg+=pvg/4\n\t\tif anim1==186:\n\t\t\tdegg+=pvg/3\nother=pvg/4\n'''
        rewritten = prep.rewrite_power_effects(source)
        for slot in range(1, 7):
            self.assertIn(f'JT_POWER_EFFECT_FRACTIONS[{slot}]', rewritten)
        self.assertNotIn('degd+=pvd/4', rewritten)
        self.assertNotIn('degg-=pvg/4', rewritten)
        self.assertNotIn('degg+=pvg/3', rewritten)
        self.assertIn('other=pvg/4', rewritten)
        self.assertIn('if anim1==181:', rewritten)
        self.assertIn('if anim1==186:', rewritten)

    def test_media_applies_frozen_session_parameters_and_next_session_resets(self):
        tmp, root, alt_id = make_two_set_root()
        self.addCleanup(tmp.cleanup)
        manifest_path = root / f'assets/sets/{alt_id}/manifest.json'
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        manifest['powers']['left_1']['parameters'] = {'raw_damage_fraction': 0.40}
        manifest['powers']['right_3']['parameters'] = {'raw_damage_fraction': 0.50}
        manifest_path.write_text(json.dumps(manifest), encoding='utf-8')

        media, _ = build_media(root)
        media._intro_done = True
        applied = []
        media._engine = {
            'jt_apply_power_paths': lambda table: None,
            'jt_apply_power_parameters': lambda table: applied.append(dict(table)),
        }
        media.on_phase_changed('MENU')
        media.select_official_set(alt_id)
        media.on_phase_changed('ROUND_INTRO')
        self.assertEqual(applied[-1], values({1: 0.40, 6: 0.50}))

        media.on_phase_changed('MENU')
        media.select_official_set('trex_vs_steg')
        media.on_phase_changed('ROUND_INTRO')
        self.assertEqual(applied[-1], values())

    def test_generated_engine_custom_attack_preserves_historical_energy_and_smoothing(self):
        h = Harness()
        self.assertIn('jt_apply_power_parameters', h.ns)
        h.start_round()
        h.ns['jt_apply_power_parameters'](values({1: 0.40}))
        h.ns.update(stamg=0.0, stamd=0.0, degg=0.0, degd=0.0, degg0=0.0, degd0=0.0)
        trigger_power_impact(h, 21, 181)
        self.assertEqual(h.ns['degd'], 150_000_000.0)
        self.assertEqual(h.ns['degg'], 0.0)
        self.assertEqual(h.ns['stamg'], 50.0)
        self.assertEqual(h.ns['stamd'], 20.0)

    def test_generated_engine_lifestream_custom_fraction_caps_and_adds_no_energy(self):
        h = Harness()
        self.assertIn('jt_apply_power_parameters', h.ns)
        h.start_round()
        h.ns['jt_apply_power_parameters'](values({2: 0.40}))
        h.ns.update(
            stamg=0.0, stamd=0.0,
            degg=100_000_000.0, degg0=100_000_000.0,
            degd=0.0, degd0=0.0,
        )
        trigger_power_impact(h, 22, 182)
        self.assertEqual(h.ns['degg'], -100_000_000.0)
        self.assertEqual(h.ns['stamg'], 0.0)
        self.assertEqual(h.ns['stamd'], 0.0)
        h.root.affpv(.5)
        self.assertEqual(h.ns['degg'], 0.0)

    def test_generated_engine_meteor_default_is_exact_historical_third(self):
        h = Harness()
        self.assertIn('jt_apply_power_parameters', h.ns)
        h.start_round()
        h.ns['jt_apply_power_parameters'](values())
        h.ns.update(stamg=0.0, stamd=0.0, degg=0.0, degd=0.0, degg0=0.0, degd0=0.0)
        trigger_power_impact(h, 26, 186)
        self.assertEqual(h.ns['degg'], 125_000_000.0)
        self.assertEqual(h.ns['stamg'], (500_000_000.0 / 3.0) / 10_000_000.0)
        self.assertEqual(h.ns['stamd'], (500_000_000.0 / 3.0) / 4_000_000.0)


if __name__ == '__main__':
    unittest.main()
