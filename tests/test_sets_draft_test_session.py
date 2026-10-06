import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from tests.test_sets_io import make_portable_fixture
from tests.test_sets_media_session import build_media, make_two_set_root
from tests.runtime_harness import Clock, Video
from tools import jtrex_sets_runtime as runtime


class TemporarySessionManagerTests(unittest.TestCase):
    def setUp(self):
        self.catalog_tmp, self.catalog_root, self.alt_id = make_two_set_root()
        self.addCleanup(self.catalog_tmp.cleanup)
        self.state_path = self.catalog_root / 'selection.json'
        self.manager = runtime.JTSetSessionManager(
            lambda relative: str(self.catalog_root / relative) if (self.catalog_root / relative).is_file() else None,
            self.state_path,
        )
        draft_tmp, draft_root, manifest, resolve = make_portable_fixture()
        self.draft_tmp = draft_tmp
        self.addCleanup(draft_tmp.cleanup)
        manifest['set_id'] = 'draft_test'
        manifest['display_name'] = 'Draft Test'
        (draft_root / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
        self.draft_root = draft_root
        self.draft = runtime.load_set_manifest(resolve)

    def test_temporary_session_is_verified_frozen_and_never_persists(self):
        selected_before = self.manager.selected_set.set_id
        persisted_before = json.loads(self.state_path.read_text(encoding='utf-8'))

        session = self.manager.begin_temporary_session(self.draft)

        self.assertEqual(session.set_id, 'draft_test')
        self.assertTrue(self.manager.session_active)
        self.assertTrue(self.manager.session_temporary)
        self.assertEqual(self.manager.runtime_set.set_id, 'draft_test')
        self.assertEqual(self.manager.selected_set.set_id, selected_before)
        self.assertEqual(json.loads(self.state_path.read_text(encoding='utf-8')), persisted_before)
        with self.assertRaisesRegex(runtime.SetContractError, 'active session'):
            self.manager.select(self.alt_id)
        self.manager.end_session()
        self.assertFalse(self.manager.session_temporary)
        self.assertEqual(self.manager.runtime_set.set_id, selected_before)

    def test_temporary_session_refuses_active_session_and_missing_required_asset(self):
        self.manager.begin_session()
        with self.assertRaisesRegex(runtime.SetContractError, 'active session'):
            self.manager.begin_temporary_session(self.draft)
        self.manager.end_session()
        first_asset = self.draft.assets()[0]
        Path(self.draft.resolve_asset(first_asset['id'])).unlink()
        with self.assertRaisesRegex(runtime.SetContractError, 'unavailable'):
            self.manager.begin_temporary_session(self.draft)


class DraftTestMediaTests(unittest.TestCase):
    def setUp(self):
        self.catalog_tmp, self.catalog_root, self.alt_id = make_two_set_root()
        self.addCleanup(self.catalog_tmp.cleanup)
        self.media, self.media_runtime = build_media(self.catalog_root)
        self.media._intro_done = True
        self.media.on_phase_changed('MENU')
        self.applied = []
        self.engine = {
            'indexa': 0,
            'jt_apply_power_paths': lambda table: self.applied.append(table),
        }
        self.media._engine = self.engine

        class PhaseStub:
            def __init__(phase_self):
                phase_self.name = 'MENU'
                phase_self.failed = []
            def sync(phase_self):
                phase_self.name = 'ROUND_INTRO'
                self.media.on_phase_changed('ROUND_INTRO')
            def apply_ui(phase_self):
                pass
            def video_complete(phase_self, state, failed=False):
                phase_self.failed.append((state, failed))
        self.media.phases = PhaseStub()

        draft_tmp, draft_root, manifest, resolve = make_portable_fixture()
        self.draft_tmp = draft_tmp
        self.addCleanup(draft_tmp.cleanup)
        manifest['set_id'] = 'draft_test'
        manifest['display_name'] = 'Draft Test'
        (draft_root / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
        self.draft_root = draft_root
        self.draft = runtime.load_set_manifest(resolve)

    def test_start_draft_test_uses_physical_draft_media_and_power_identity_without_persistence(self):
        before = json.loads((self.catalog_root / 'userdata/jt-set-selection.json').read_text(encoding='utf-8'))
        returned = []

        selection = self.media.start_draft_test(self.draft, return_callback=lambda: returned.append(True))

        self.assertEqual(selection.set_id, 'draft_test')
        self.assertTrue(self.media.sets.session_temporary)
        self.assertEqual(self.engine['indexa'], 4)
        self.assertEqual(self.media.selection.set_id, 'draft_test')
        self.assertTrue(self.applied)
        self.assertTrue(Path(self.applied[-1][1]['ready']).is_file())
        self.assertTrue(str(self.applied[-1][1]['ready']).startswith(str(self.draft_root)))
        scene = self.media._scene_config('charge')
        self.assertEqual(scene['file'], self.draft.media_path('charge_red_blue'))
        self.assertEqual(scene['resolved_file'], self.draft.resolve_path(scene['file']))
        self.assertIsNotNone(self.media._scene_player)
        self.assertTrue(self.media._scene_player.filename.startswith(str(self.draft_root)))
        self.assertEqual(json.loads((self.catalog_root / 'userdata/jt-set-selection.json').read_text(encoding='utf-8')), before)
        self.assertEqual(returned, [])

    def test_return_to_menu_restores_normal_selection_once_and_stale_test_callbacks_do_nothing(self):
        returned = []
        self.media.start_draft_test(self.draft, return_callback=lambda: returned.append('returned'))
        old_player = self.media._scene_player
        old_generation = self.media._scene_generation
        old_frame = self.media._scene_frame_callback
        old_eos = self.media._scene_eos_callback

        self.media.on_phase_changed('MENU')
        self.assertFalse(self.media.sets.session_active)
        self.assertFalse(self.media.sets.session_temporary)
        self.assertEqual(self.media.selection.set_id, runtime.CANONICAL_SET_ID)
        self.assertIsNone(self.media._scene_player)

        for event in list(Clock.events):
            if not getattr(event, 'cancelled', False):
                event.callback(0)
        self.assertEqual(returned, ['returned'])

        # A delayed frame/EOS from the draft cannot revive or mutate the normal context.
        if old_frame is not None:
            old_player.texture = SimpleNamespace(size=(640, 360))
            old_frame(old_player)
        if old_eos is not None:
            old_eos(old_player)
        self.assertEqual(self.media.selection.set_id, runtime.CANONICAL_SET_ID)
        self.assertFalse(self.media.sets.session_active)
        self.media.on_phase_changed('MENU')
        self.assertEqual(returned, ['returned'])

    def test_decoder_failure_is_bounded_and_menu_return_still_restores_normal_selection(self):
        class FailingVideo:
            def __init__(self, **kwargs):
                raise OSError('decoder boom')
        original = self.media_runtime.CoreVideo
        self.media_runtime.CoreVideo = FailingVideo
        self.addCleanup(lambda: setattr(self.media_runtime, 'CoreVideo', original))

        self.media.start_draft_test(self.draft)

        self.assertTrue(self.media.sets.session_temporary)
        self.assertTrue(self.media.phases.failed)
        self.media.on_phase_changed('MENU')
        self.assertEqual(self.media.selection.set_id, runtime.CANONICAL_SET_ID)
        self.assertFalse(self.media.sets.session_active)


if __name__ == '__main__':
    unittest.main()
