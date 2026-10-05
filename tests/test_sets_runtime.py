import copy
import json
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))


class SetRuntimeContractTests(unittest.TestCase):
    def _runtime(self):
        import jtrex_sets_runtime as runtime
        return runtime

    def _repo_resolve(self, relative):
        path = ROOT / relative
        return str(path) if path.is_file() else None

    def _canonical(self):
        return json.loads((ROOT / 'assets/sets/trex_vs_steg/manifest.json').read_text())

    def _temp_selection(self, mutate):
        runtime = self._runtime()
        manifest = self._canonical()
        mutate(manifest)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'assets/sets/trex_vs_steg').mkdir(parents=True)
            (root / 'assets/sets/catalog.json').write_text(json.dumps({
                'format_version': 1,
                'sets': [{'set_id': 'trex_vs_steg', 'manifest': 'assets/sets/trex_vs_steg/manifest.json'}],
            }))
            (root / 'assets/sets/trex_vs_steg/manifest.json').write_text(json.dumps(manifest))
            def resolve(relative):
                path = root / relative
                return str(path) if path.is_file() else None
            return runtime.load_official_set(resolve)

    def test_canonical_catalog_contract_and_sides(self):
        runtime = self._runtime()
        selection = runtime.load_official_set(self._repo_resolve)
        self.assertEqual(selection.set_id, 'trex_vs_steg')
        self.assertEqual(selection.format_version, 1)
        self.assertEqual(selection.engine_contract, 'jtrex-combat-v1')
        self.assertEqual(selection.dinosaurs()['left']['id'], 'st')
        self.assertEqual(selection.dinosaurs()['right']['id'], 'tr')

    def test_canonical_media_roles_resolve(self):
        selection = self._runtime().load_official_set(self._repo_resolve)
        self.assertEqual(len(selection.intro_paths()), 3)
        self.assertEqual(selection.media_path('orbs_background'), 'assets/combat/StegTrexPlageVideoenboucledesorbes.mp4')
        self.assertEqual(selection.media_path('verdict_draw'), 'assets/combat/Zerowinstegtrexsurleschargedejaugejauneetbleuetrouge.mp4')

    def test_canonical_six_powers_and_closed_parameters(self):
        selection = self._runtime().load_official_set(self._repo_resolve)
        keys = ('left_1','left_2','left_3','right_1','right_2','right_3')
        for key in keys:
            self.assertEqual(selection.power(key)['parameters'], {})
        self.assertEqual(selection.power_media_path('left_1'), 'assets/powers/stsf-sanctuary-force.mp4')
        self.assertEqual(selection.power_media_path('right_3'), 'assets/powers/trma-meteor-attack.mp4')

    def test_missing_referenced_asset_is_rejected(self):
        runtime = self._runtime()
        with self.assertRaises(runtime.SetContractError):
            self._temp_selection(lambda m: m['media'].__setitem__('orbs_background', 'missing-id'))

    def test_unknown_media_role_is_rejected(self):
        runtime = self._runtime()
        with self.assertRaises(runtime.SetContractError):
            self._temp_selection(lambda m: m['media'].__setitem__('surprise_scene', m['media']['orbs_background']))

    def test_unknown_power_role_is_rejected(self):
        runtime = self._runtime()
        with self.assertRaises(runtime.SetContractError):
            self._temp_selection(lambda m: m['powers'].__setitem__('left_4', copy.deepcopy(m['powers']['left_1'])))

    def test_asset_paths_are_confined(self):
        runtime = self._runtime()
        bad = ('/tmp/x.mp4', '../x.mp4', 'dir\\x.mp4', 'https://example.test/x.mp4')
        for value in bad:
            with self.subTest(value=value):
                with self.assertRaises(runtime.SetContractError):
                    self._temp_selection(lambda m, v=value: m['assets'][0].__setitem__('path', v))

    def test_gameplay_policy_fields_are_rejected(self):
        runtime = self._runtime()
        for field in ('loop', 'play_to_end', 'states'):
            with self.subTest(field=field):
                with self.assertRaises(runtime.SetContractError):
                    self._temp_selection(lambda m, f=field: m['powers']['left_1'].__setitem__(f, True))
