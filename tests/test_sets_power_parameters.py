import copy
import json
import math
import tempfile
import unittest
from pathlib import Path

from tools import jtrex_sets_runtime as runtime

ROOT = Path(__file__).resolve().parents[1]


class SetPowerParameterContractTests(unittest.TestCase):
    def _canonical_manifest(self):
        return json.loads(
            (ROOT / 'assets/sets/trex_vs_steg/manifest.json').read_text(encoding='utf-8')
        )

    def _load_manifest(self, mutate=None):
        manifest = self._canonical_manifest()
        if mutate is not None:
            mutate(manifest)
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        root = Path(td.name)
        path = root / 'manifest.json'
        path.write_text(json.dumps(manifest, allow_nan=True), encoding='utf-8')

        def resolve(relative):
            candidate = root / relative
            return str(candidate) if candidate.is_file() else None

        return runtime.load_set_manifest(resolve)

    def test_empty_parameters_normalize_to_canonical_defaults(self):
        selection = self._load_manifest()
        expected = {
            'left_1': ('raw_damage_fraction', 0.25),
            'left_2': ('heal_fraction', 0.25),
            'left_3': ('raw_damage_fraction', 0.25),
            'right_1': ('raw_damage_fraction', 0.25),
            'right_2': ('raw_damage_fraction', 0.25),
            'right_3': ('raw_damage_fraction', 1.0 / 3.0),
        }
        for power_key, (field, value) in expected.items():
            with self.subTest(power_key=power_key):
                self.assertEqual(selection.power(power_key)['parameters'], {})
                self.assertEqual(selection.power_parameters(power_key), {field: value})
                self.assertEqual(selection.power_effect_fraction(power_key), value)

    def test_each_power_accepts_its_inclusive_min_and_max(self):
        bounds = {
            'left_1': ('raw_damage_fraction', 0.10, 0.40),
            'left_2': ('heal_fraction', 0.10, 0.40),
            'left_3': ('raw_damage_fraction', 0.10, 0.40),
            'right_1': ('raw_damage_fraction', 0.10, 0.40),
            'right_2': ('raw_damage_fraction', 0.10, 0.40),
            'right_3': ('raw_damage_fraction', 0.15, 0.50),
        }
        for power_key, (field, low, high) in bounds.items():
            for value in (low, high):
                with self.subTest(power_key=power_key, value=value):
                    selection = self._load_manifest(
                        lambda m, key=power_key, name=field, v=value:
                        m['powers'][key].__setitem__('parameters', {name: v})
                    )
                    self.assertEqual(selection.power_parameters(power_key), {field: value})
                    self.assertEqual(selection.power_effect_fraction(power_key), value)

    def test_wrong_parameter_key_is_rejected_per_slot(self):
        with self.assertRaises(runtime.SetContractError):
            self._load_manifest(
                lambda m: m['powers']['left_2'].__setitem__(
                    'parameters', {'raw_damage_fraction': 0.25}
                )
            )

    def test_non_finite_bool_and_out_of_range_parameters_are_rejected(self):
        bad_cases = (
            ('left_1', 'raw_damage_fraction', True),
            ('left_1', 'raw_damage_fraction', float('nan')),
            ('left_1', 'raw_damage_fraction', float('inf')),
            ('left_1', 'raw_damage_fraction', 0.099999),
            ('left_1', 'raw_damage_fraction', 0.400001),
            ('right_3', 'raw_damage_fraction', 0.149999),
            ('right_3', 'raw_damage_fraction', 0.500001),
        )
        for power_key, field, value in bad_cases:
            with self.subTest(power_key=power_key, value=value):
                with self.assertRaises(runtime.SetContractError):
                    self._load_manifest(
                        lambda m, key=power_key, name=field, v=value:
                        m['powers'][key].__setitem__('parameters', {name: v})
                    )

    def test_multiple_or_unknown_parameter_fields_are_rejected(self):
        cases = (
            {'raw_damage_fraction': 0.25, 'cost': 1},
            {'formula': 'pvd/2'},
        )
        for params in cases:
            with self.subTest(params=params):
                with self.assertRaises(runtime.SetContractError):
                    self._load_manifest(
                        lambda m, p=copy.deepcopy(params):
                        m['powers']['left_1'].__setitem__('parameters', p)
                    )


if __name__ == '__main__':
    unittest.main()
