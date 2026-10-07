import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from tests.test_sets_io import make_portable_fixture
from tests.test_sets_media_session import Root, load_media_runtime
from jtrex_sets_runtime import load_set_manifest


class PowerParameterUIContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.runtime = load_media_runtime(Path(__file__).resolve().parents[1])
        app = SimpleNamespace(root=Root(), user_data_dir=self.tmp.name)
        self.media = self.runtime.JTMediaController(app)
        self.media._intro_done = True
        self.media.on_phase_changed('MENU')
        source_tmp, source_root, manifest, resolve = make_portable_fixture()
        self.source_tmp = source_tmp
        self.addCleanup(source_tmp.cleanup)
        source = load_set_manifest(resolve)
        self.media._set_admin.create_from_selection(
            source, draft_id='params-ui', set_id='params_ui', source_kind='official'
        )
        self.media._admin_enabled = True
        self.media.workshop_resume_draft('params-ui')

    @staticmethod
    def texts(widget):
        result = []
        stack = [widget]
        while stack:
            current = stack.pop()
            text = getattr(current, 'text', '')
            if text:
                result.append(text)
            stack.extend(getattr(current, 'children', ()))
        return result

    def test_editor_exposes_admin_only_power_parameter_action(self):
        popup = self.media._workshop_open_editor('params-ui')
        texts = self.texts(popup.content)
        self.assertIn('PARAMÈTRES POUVOIRS', texts)
        self.assertNotIn('COÛTS POUVOIRS', texts)
        self.assertNotIn('JALONS POUVOIRS', texts)

    def test_parameter_popup_has_six_readable_bounded_rows_without_gameplay_controls(self):
        popup = self.media._workshop_power_parameters_dialog()
        texts = self.texts(popup.content)
        fields = self.media.workshop_power_parameter_fields()
        self.assertEqual(len(fields), 6)
        for field in fields:
            self.assertTrue(any(field.label in text for text in texts))
        joined = '\n'.join(texts).lower()
        for forbidden in ('coût', 'cost', 'jalon', 'marker', 'mechanism', 'mécanisme', 'chrono', 'eos'):
            self.assertNotIn(forbidden, joined)
        self.assertGreaterEqual(texts.count('−1 %'), 6)
        self.assertGreaterEqual(texts.count('+1 %'), 6)
        self.assertGreaterEqual(texts.count('DÉFAUT'), 6)

    def test_adjustment_is_one_percent_clamped_and_reset_restores_canonical_default(self):
        self.media.workshop_set_power_parameter('left_1', 0.39)
        field = self.media._workshop_adjust_power_parameter('left_1', +0.01)
        self.assertAlmostEqual(field.value, 0.40)
        field = self.media._workshop_adjust_power_parameter('left_1', +0.01)
        self.assertAlmostEqual(field.value, 0.40)
        for _ in range(40):
            field = self.media._workshop_adjust_power_parameter('left_1', -0.01)
        self.assertAlmostEqual(field.value, 0.10)
        field = self.media.workshop_reset_power_parameter('left_1')
        self.assertAlmostEqual(field.value, 0.25)

        self.media.workshop_set_power_parameter('right_3', 0.49)
        field = self.media._workshop_adjust_power_parameter('right_3', +0.01)
        self.assertAlmostEqual(field.value, 0.50)
        field = self.media._workshop_adjust_power_parameter('right_3', +0.01)
        self.assertAlmostEqual(field.value, 0.50)
        field = self.media.workshop_reset_power_parameter('right_3')
        self.assertAlmostEqual(field.value, 1.0 / 3.0)

    def test_parameter_scroll_content_is_tall_enough_for_all_six_rows(self):
        base_widget = self.runtime.Widget if hasattr(self.runtime, 'Widget') else None

        class SmallBox(base_widget):
            def __init__(self, *args, **kwargs):
                height = kwargs.get('height', 100)
                super().__init__(*args, **kwargs)
                self.size = (self.size[0], height)

        self.runtime.BoxLayout = SmallBox
        popup = self.media._workshop_power_parameters_dialog()
        stack = [popup.content]
        candidates = []
        while stack:
            current = stack.pop()
            if len(getattr(current, 'children', ())) >= 12:
                candidates.append(current)
            stack.extend(getattr(current, 'children', ()))
        self.assertTrue(candidates)
        self.assertGreaterEqual(max(item.height for item in candidates), 700)

    def test_parameter_dialog_remains_menu_and_admin_only(self):
        self.media._admin_enabled = False
        with self.assertRaisesRegex(Exception, 'admin'):
            self.media._workshop_power_parameters_dialog()
        self.media._admin_enabled = True
        self.media.on_phase_changed('ROUND_INTRO')
        with self.assertRaisesRegex(Exception, 'menu'):
            self.media._workshop_power_parameters_dialog()


if __name__ == '__main__':
    unittest.main()
