import json
import tempfile
import unittest
from pathlib import Path

from tests.test_sets_io import make_portable_fixture
from tools import jtrex_sets_runtime as runtime
from tools.jtrex_sets_io import JTSetIOLimits, JTSetStorage

try:
    from tools.jtrex_sets_admin import JTSetAdminService
except ImportError:
    JTSetAdminService = None


class AdminDraftTests(unittest.TestCase):
    def _storage(self, limits=None):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        return root, JTSetStorage(root / 'official', root / 'user', root / 'draft', limits=limits)

    def _source(self):
        tmp, root, manifest, resolve = make_portable_fixture()
        self.addCleanup(tmp.cleanup)
        return tmp, root, manifest, runtime.load_set_manifest(resolve)

    def _service_and_draft(self, *, limits=None, target='my_dinos'):
        root, storage = self._storage(limits=limits)
        _tmp, source_root, manifest, selection = self._source()
        service = JTSetAdminService(storage, {'trex_vs_steg'})
        state = service.create_from_selection(
            selection, draft_id='draft-one', set_id=target, source_kind='official'
        )
        return root, storage, source_root, manifest, service, state

    def test_clone_is_self_contained_and_resumes_state_after_source_disappears(self):
        root, storage, source_root, manifest, service, state = self._service_and_draft()
        self.assertEqual(state.draft_id, 'draft-one')
        self.assertEqual(state.set_id, 'my_dinos')
        self.assertEqual(state.revision, 1)
        self.assertEqual(state.role_index, 0)
        self.assertEqual(state.source_kind, 'official')

        draft = storage.draft_path('draft-one')
        self.assertTrue((draft / 'manifest.json').is_file())
        self.assertTrue((draft / 'draft-state.json').is_file())
        self.assertEqual(len([p for p in draft.rglob('*') if p.is_file() and p.name != 'draft-state.json']), 42)

        # Prove the draft no longer depends on the source resolver/files.
        for child in sorted(source_root.rglob('*'), reverse=True):
            if child.is_file():
                child.unlink()
            elif child.is_dir():
                child.rmdir()
        source_root.rmdir()

        service.keep_and_next('draft-one')
        reopened_service = JTSetAdminService(storage, {'trex_vs_steg'})
        reopened = reopened_service.open_draft('draft-one')
        self.assertEqual(reopened.role_index, 1)
        verified = reopened_service.validate_complete('draft-one')
        self.assertEqual(verified.set_id, 'my_dinos')
        self.assertIsNotNone(verified.resolve_asset(verified.manifest()['media']['orbs_background']))

    def test_candidate_is_separate_until_accept_then_manifest_hash_and_orphan_are_updated(self):
        root, storage, source_root, manifest, service, state = self._service_and_draft()
        before = service.validate_complete('draft-one').manifest()
        old_asset_id = before['media']['orbs_background']
        old_asset = next(a for a in before['assets'] if a['id'] == old_asset_id)
        old_file = storage.draft_path('draft-one') / old_asset['path']
        self.assertTrue(old_file.is_file())

        candidate = root / 'replacement.mp4'
        candidate.write_bytes(b'new-video-data')
        staged = service.stage_candidate('draft-one', 'media.orbs_background', candidate)
        self.assertTrue(staged.is_file())
        during = json.loads((storage.draft_path('draft-one') / 'manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(during['media']['orbs_background'], old_asset_id)

        service.accept_candidate('draft-one', 'media.orbs_background')
        after = service.validate_complete('draft-one').manifest()
        new_asset_id = after['media']['orbs_background']
        self.assertNotEqual(new_asset_id, old_asset_id)
        new_asset = next(a for a in after['assets'] if a['id'] == new_asset_id)
        self.assertEqual(new_asset['size'], len(b'new-video-data'))
        self.assertEqual(new_asset['type'], 'video')
        self.assertNotIn(old_asset_id, {a['id'] for a in after['assets']})
        self.assertFalse(old_file.exists())
        self.assertTrue((storage.draft_path('draft-one') / new_asset['path']).is_file())

    def test_candidate_rejects_wrong_type_and_real_size_limit(self):
        limits = JTSetIOLimits(max_file_bytes=4)
        root, storage, source_root, manifest, service, state = self._service_and_draft(limits=limits)
        wrong = root / 'wrong.wav'
        wrong.write_bytes(b'1234')
        with self.assertRaisesRegex(ValueError, 'type'):
            service.stage_candidate('draft-one', 'media.orbs_background', wrong)
        large = root / 'large.mp4'
        large.write_bytes(b'12345')
        with self.assertRaisesRegex(ValueError, 'limit'):
            service.stage_candidate('draft-one', 'media.orbs_background', large)

    def test_identity_changes_are_closed_and_user_revision_defaults_to_next(self):
        root, storage, source_root, manifest, service, state = self._service_and_draft()
        service.set_identity(
            'draft-one',
            display_name='Raptors vs Trikes',
            left_name='Raptor',
            right_name='Trike',
            power_labels={'left_1': 'Bouclier Raptor', 'right_3': 'Météore Trike'},
        )
        updated = service.validate_complete('draft-one').manifest()
        self.assertEqual(updated['display_name'], 'Raptors vs Trikes')
        self.assertEqual(updated['dinosaurs']['left']['display_name'], 'Raptor')
        self.assertEqual(updated['dinosaurs']['right']['display_name'], 'Trike')
        self.assertEqual(updated['powers']['left_1']['label'], 'Bouclier Raptor')
        self.assertEqual(updated['powers']['right_3']['label'], 'Météore Trike')
        self.assertEqual(updated['powers']['left_1']['parameters'], {})
        self.assertEqual(updated['powers']['left_1']['mechanism'], 'left_slot_1_target_damage')

        installed = service.install_revision('draft-one')
        self.assertEqual((installed.set_id, installed.revision), ('my_dinos', 1))

        source_user = storage.load_user_revision('my_dinos', 1)
        second = service.create_from_selection(
            source_user, draft_id='draft-two', set_id='my_dinos', source_kind='user'
        )
        self.assertEqual(second.revision, 2)

    def test_official_set_id_and_invalid_identity_are_refused(self):
        root, storage = self._storage()
        _tmp, _source_root, manifest, selection = self._source()
        service = JTSetAdminService(storage, {'trex_vs_steg'})
        with self.assertRaisesRegex(ValueError, 'official'):
            service.create_from_selection(
                selection, draft_id='bad-official', set_id='trex_vs_steg', source_kind='official'
            )
        state = service.create_from_selection(
            selection, draft_id='good', set_id='user_set', source_kind='official'
        )
        with self.assertRaises(ValueError):
            service.set_identity('good', set_id='../bad')
        with self.assertRaises(ValueError):
            service.set_identity('good', revision=0)
        with self.assertRaises(ValueError):
            service.set_identity('good', display_name='')
        with self.assertRaisesRegex(ValueError, 'official'):
            service.set_identity('good', set_id='trex_vs_steg')

    def test_export_revision_uses_validated_draft(self):
        root, storage, source_root, manifest, service, state = self._service_and_draft()
        destination = root / 'exported.jtrex.zip'
        result = service.export_revision('draft-one', destination)
        self.assertEqual(result, destination)
        self.assertTrue(destination.is_file())
        imported_storage = JTSetStorage(root / 'official2', root / 'user2', root / 'draft2')
        imported = imported_storage.import_set_zip(destination, official_set_ids={'trex_vs_steg'})
        self.assertEqual((imported.set_id, imported.revision), ('my_dinos', 1))


if __name__ == '__main__':
    unittest.main()
