import json
import tempfile
import unittest
from pathlib import Path
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from jtrex_sets_runtime import load_set_manifest
from tests.runtime_harness import Clock, Video
from tests.test_sets_io import make_portable_fixture
from tests.test_sets_media_session import Root, load_media_runtime



class WorkshopUIContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.runtime = load_media_runtime(ROOT)
        self.root = Root()
        app = SimpleNamespace(root=self.root, user_data_dir=self.tmp.name)
        self.media = self.runtime.JTMediaController(app)
        self.media._intro_done = True
        self.media.on_phase_changed('MENU')

    def test_twenty_taps_keep_diagnostic_and_only_admin_exposes_workshop(self):
        self.assertFalse(any(getattr(child, 'text', '') == 'ATELIER SETS' for child in self.root.children))
        window = self.runtime.Window
        touch = SimpleNamespace(x=window.width * .95, y=window.height * .05)
        for _ in range(20):
            self.media._on_admin_trigger(window, touch)
        self.assertTrue(self.media._admin_enabled)
        Clock.events[-1].callback(0)
        self.assertIsNotNone(self.media._admin_popup)
        self.assertEqual(self.media._admin_workshop_button.text, 'ATELIER SETS')
        self.assertGreaterEqual(self.media._admin_workshop_button.height, 58)

    def test_mobile_set_selector_is_compact_scrollable_and_admin_edit_is_discreet(self):
        self.assertTrue(self.media._set_button.text.startswith('SET v'))
        self.assertLessEqual(self.media._set_button.height, 40)
        self.assertTrue(self.media._set_edit_button.disabled)
        self.media._open_set_selector()
        self.assertIsNotNone(self.media._set_selector_scroll)
        self.assertGreaterEqual(len(self.media._set_option_buttons), 1)
        self.media._set_selector_closed()
        self.media._admin_enabled = True
        self.media._set_selector_visible(True)
        self.assertFalse(self.media._set_edit_button.disabled)
        self.assertEqual(self.media._set_edit_button.text, 'MOD')
        self.assertLessEqual(self.media._set_edit_button.height, 40)
        group_left = self.media._set_button.x
        group_right = self.media._set_edit_button.x + self.media._set_edit_button.width
        self.assertAlmostEqual((group_left + group_right) / 2.0, self.root.width / 2.0, delta=2.0)

    def test_workshop_is_menu_only_and_uses_large_readable_actions(self):
        with self.assertRaisesRegex(Exception, 'admin'):
            self.media._open_workshop()
        self.media._admin_enabled = True
        self.media._open_workshop()
        self.assertIsNotNone(self.media._workshop_menu_scroll)
        expected = {
            'CREER DEPUIS LE SET ACTUEL', 'REPRENDRE UN BROUILLON',
            'MODIFIER LE SET UTILISATEUR', 'IMPORTER UN ZIP', 'FERMER',
        }
        self.assertTrue(expected.issubset({button.text for button in self.media._workshop_buttons.values()}))
        self.assertTrue(all(button.height >= 44 for button in self.media._workshop_buttons.values()))
        self.media.on_phase_changed('ROUND_INTRO')
        with self.assertRaisesRegex(Exception, 'menu'):
            self.media._open_workshop()

    def test_assistant_resume_progress_preview_candidate_keep_accept_previous_and_validate(self):
        source_tmp, source_root, manifest, resolve = make_portable_fixture()
        self.addCleanup(source_tmp.cleanup)
        source = load_set_manifest(resolve)
        self.media._set_admin.create_from_selection(
            source, draft_id='ui-draft', set_id='ui_dinos', source_kind='official'
        )
        self.media._admin_enabled = True
        state = self.media.workshop_resume_draft('ui-draft')
        self.assertEqual(state.role_index, 0)
        self.media._workshop_open_editor('ui-draft')
        self.assertIsNotNone(self.media._workshop_editor_scroll)
        self.assertIsNotNone(self.media._workshop_progress_label)
        self.assertIn('ÉTAPE 1/', self.media._workshop_progress_label.text)
        self.media._workshop_editor_popup = None
        self.media._workshop_editor_label = None
        self.media._workshop_editor_scroll = None
        self.media._workshop_progress_label = None
        for _ in range(3):
            self.media.workshop_keep_and_next()
        info = self.media.workshop_current_role_info()
        self.assertEqual(info['role'].asset_type, 'video')
        self.assertEqual(info['progress'], (4, len(self.media._set_admin.roles('ui-draft'))))
        current = self.media.workshop_preview_current()
        self.assertTrue(current.opened)
        self.media._workshop_preview_current_action()
        self.assertIsNotNone(self.media._workshop_preview_popup)
        self.assertGreaterEqual(self.media._workshop_preview_popup.size_hint[0], 0.9)
        player = self.media._set_preview.current_player
        self.assertIsNotNone(player)
        self.assertEqual(player.state, 'playing')
        player.texture = SimpleNamespace(size=(640, 360))
        player.callbacks['on_frame'](player)
        self.media._workshop_preview_event.callback(0)
        self.assertNotEqual(self.media._workshop_preview_label.text, 'Aperçu fermé')
        self.assertIn('640x360', self.media._workshop_preview_label.text)
        self.assertIs(self.media._workshop_preview_surface._preview.texture, player.texture)
        candidate = Path(self.tmp.name) / 'replacement.mp4'
        candidate.write_bytes(b'replacement-video')
        staged = self.media.workshop_stage_candidate(candidate)
        self.assertTrue(Path(staged).is_file())
        replacement = self.media.workshop_preview_candidate()
        self.assertTrue(replacement.opened)
        old_index = self.media._set_admin.open_draft('ui-draft').role_index
        self.media.workshop_accept_and_next()
        self.assertEqual(self.media._set_admin.open_draft('ui-draft').role_index, old_index + 1)
        self.media.workshop_previous()
        self.assertEqual(self.media._set_admin.open_draft('ui-draft').role_index, old_index)
        verified = self.media.workshop_validate()
        self.assertEqual(verified.set_id, 'ui_dinos')

    def test_right_selection_dinosaur_is_bounded_in_generated_screen_up(self):
        generated = ROOT / 'app' / 'main.py'
        if not generated.is_file():
            self.skipTest('generated Android main.py is produced by the CI preparation step')
        source = generated.read_text(encoding='utf-8')
        self.assertIn('_jt_jb_render_pos=', source)
        self.assertIn('if indexa==0:', source)
        self.assertIn('_jt_jb_min_x=self.x+self.width+_jt_jb_safety-self.jb.size[0]', source)
        self.assertIn(
            'self.jb.pos=(max(_jt_jb_render_pos[0],_jt_jb_min_x),_jt_jb_render_pos[1])',
            source,
        )
        runtime_source = (ROOT / 'tools' / 'jtrex_media_runtime.py').read_text(encoding='utf-8')
        self.assertNotIn('_guard_menu_right_dinosaur_crop', runtime_source)
        self.assertNotIn('_menu_right_dino_event', runtime_source)

    def test_identity_dialog_exposes_all_six_power_labels(self):
        source = (ROOT / 'tools/jtrex_media_runtime.py').read_text(encoding='utf-8')
        self.assertIn('for power_key in POWER_KEYS', source)
        self.assertIn('power_labels=power_labels', source)
        for key in ('left_1', 'left_2', 'left_3', 'right_1', 'right_2', 'right_3'):
            self.assertIn(key, self.runtime.POWER_KEYS)

    def test_export_action_uses_android_create_document_and_async_egress(self):
        source = (ROOT / 'tools/jtrex_media_runtime.py').read_text(encoding='utf-8')
        self.assertIn('self._set_picker.create(', source)
        self.assertIn('self._set_egress.export(', source)


if __name__ == '__main__':
    unittest.main()
