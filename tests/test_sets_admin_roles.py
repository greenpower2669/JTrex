import tempfile
import unittest
from pathlib import Path

from tests.test_sets_io import make_portable_fixture
from tools import jtrex_sets_runtime as runtime
from tools.jtrex_sets_io import JTSetStorage

try:
    from tools.jtrex_sets_admin import JTAdminRole, JTSetAdminService
except ImportError:
    JTAdminRole = JTSetAdminService = None


class AdminRoleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.storage = JTSetStorage(root / 'official', root / 'user', root / 'draft')
        source_tmp, source_root, manifest, resolve = make_portable_fixture()
        self.source_tmp = source_tmp
        self.addCleanup(source_tmp.cleanup)
        self.service = JTSetAdminService(self.storage, {'trex_vs_steg'})
        self.service.create_from_selection(
            runtime.load_set_manifest(resolve),
            draft_id='roles', set_id='user_roles', source_kind='official'
        )

    def test_roles_cover_data_media_identity_without_gameplay_fields(self):
        roles = self.service.roles('roles')
        self.assertEqual(len(roles), 44)
        self.assertTrue(all(isinstance(role, JTAdminRole) for role in roles))
        by_id = {role.role_id: role for role in roles}
        expected = {
            'catalog.thumbnail',
            'dinosaurs.left.portrait', 'dinosaurs.right.portrait',
            'media.intros.0', 'media.intros.1', 'media.intros.2',
            'media.orbs_background', 'media.charge_red_blue', 'media.charge_yellow',
            'media.verdict_draw', 'media.verdict_left', 'media.verdict_right',
            'media.finishing_left', 'media.finishing_right',
            'powers.left_1.media', 'powers.left_1.images.ready',
            'powers.left_1.images.used', 'powers.left_1.activation_audio',
            'powers.left_1.legacy_fallback_audio',
            'powers.right_3.media', 'powers.right_3.images.ready',
            'powers.right_3.images.used', 'powers.right_3.activation_audio',
            'powers.right_3.legacy_fallback_audio',
        }
        self.assertTrue(expected.issubset(by_id))
        self.assertEqual(by_id['catalog.thumbnail'].asset_type, 'image')
        self.assertFalse(by_id['catalog.thumbnail'].required)
        self.assertEqual(by_id['media.orbs_background'].asset_type, 'video')
        self.assertTrue(by_id['media.orbs_background'].required)
        self.assertEqual(by_id['powers.left_1.activation_audio'].asset_type, 'audio')
        forbidden = ('mechanism', 'parameters', 'cost', 'damage', 'chrono', 'eos', 'energy')
        self.assertFalse(any(any(word in role.role_id.lower() for word in forbidden) for role in roles))

    def test_navigation_previous_keep_and_resume_progress(self):
        roles = self.service.roles('roles')
        self.assertEqual(self.service.current_role('roles'), roles[0])
        self.assertEqual(self.service.previous_role('roles'), roles[0])
        self.assertEqual(self.service.keep_and_next('roles'), roles[1])
        self.assertEqual(self.service.keep_and_next('roles'), roles[2])
        self.assertEqual(self.service.previous_role('roles'), roles[1])

        reopened = JTSetAdminService(self.storage, {'trex_vs_steg'})
        self.assertEqual(reopened.current_role('roles').role_id, roles[1].role_id)


if __name__ == '__main__':
    unittest.main()
