import tempfile
import unittest
from pathlib import Path

from tests.test_sets_io import make_portable_fixture
from tools import jtrex_sets_runtime as runtime
from tools.jtrex_sets_admin import JTSetAdminService
from tools.jtrex_sets_io import JTSetStorage


class AdminPowerParameterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.storage = JTSetStorage(root / 'official', root / 'user', root / 'draft')
        source_tmp, _source_root, _manifest, resolve = make_portable_fixture()
        self.source_tmp = source_tmp
        self.addCleanup(source_tmp.cleanup)
        self.service = JTSetAdminService(self.storage, {'trex_vs_steg'})
        self.service.create_from_selection(
            runtime.load_set_manifest(resolve),
            draft_id='params', set_id='user_params', source_kind='official'
        )

    def test_six_parameter_fields_expose_only_approved_bounds_and_defaults(self):
        fields = self.service.power_parameter_fields('params')
        self.assertEqual([field.power_key for field in fields], list(runtime.POWER_KEYS))
        expected = {
            'left_1': ('raw_damage_fraction', 0.25, 0.10, 0.40),
            'left_2': ('heal_fraction', 0.25, 0.10, 0.40),
            'left_3': ('raw_damage_fraction', 0.25, 0.10, 0.40),
            'right_1': ('raw_damage_fraction', 0.25, 0.10, 0.40),
            'right_2': ('raw_damage_fraction', 0.25, 0.10, 0.40),
            'right_3': ('raw_damage_fraction', 1.0 / 3.0, 0.15, 0.50),
        }
        for field in fields:
            with self.subTest(power_key=field.power_key):
                key, default, low, high = expected[field.power_key]
                self.assertEqual(field.parameter, key)
                self.assertEqual(field.value, default)
                self.assertEqual(field.default, default)
                self.assertEqual(field.minimum, low)
                self.assertEqual(field.maximum, high)
                exposed = set(field.__dict__)
                self.assertFalse(exposed & {'mechanism', 'cost', 'energy', 'chrono', 'eos', 'state', 'marker'})

    def test_bounded_edit_is_persisted_and_resumed(self):
        updated = self.service.set_power_parameter('params', 'left_1', 0.40)
        self.assertEqual(updated.value, 0.40)
        reopened = JTSetAdminService(self.storage, {'trex_vs_steg'})
        fields = {field.power_key: field for field in reopened.power_parameter_fields('params')}
        self.assertEqual(fields['left_1'].value, 0.40)
        selection = reopened.validate_complete('params')
        self.assertEqual(selection.power('left_1')['parameters'], {'raw_damage_fraction': 0.40})
        self.assertEqual(selection.power('left_1')['mechanism'], runtime.MECHANISMS['left_1'])

    def test_reset_restores_empty_manifest_parameters_and_canonical_value(self):
        self.service.set_power_parameter('params', 'right_3', 0.50)
        reset = self.service.reset_power_parameter('params', 'right_3')
        self.assertEqual(reset.value, 1.0 / 3.0)
        selection = self.service.validate_complete('params')
        self.assertEqual(selection.power('right_3')['parameters'], {})
        self.assertEqual(selection.power_effect_fraction('right_3'), 1.0 / 3.0)

    def test_invalid_or_unknown_parameter_edit_is_rejected_by_runtime_contract(self):
        bad = (
            ('left_1', 0.09),
            ('right_3', 0.51),
            ('left_2', True),
        )
        for power_key, value in bad:
            with self.subTest(power_key=power_key, value=value):
                with self.assertRaises(runtime.SetContractError):
                    self.service.set_power_parameter('params', power_key, value)
        with self.assertRaises(ValueError):
            self.service.set_power_parameter('params', 'left_9', 0.25)

    def test_export_install_round_trip_preserves_explicit_parameter(self):
        self.service.set_power_parameter('params', 'left_2', 0.35)
        result = self.service.install_revision('params')
        loaded = self.storage.load_user_revision(result.set_id, result.revision)
        self.assertEqual(loaded.power_parameters('left_2'), {'heal_fraction': 0.35})
        self.assertEqual(loaded.power('left_3')['parameters'], {})


if __name__ == '__main__':
    unittest.main()
