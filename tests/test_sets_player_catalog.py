import json
import shutil
import tempfile
import unittest
from pathlib import Path
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from jtrex_sets_runtime import CANONICAL_SET_ID, load_set_manifest
from tests.test_sets_io import make_portable_fixture
from tests.test_sets_media_session import Root, load_media_runtime



class PlayerCatalogWorkshopTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.runtime = load_media_runtime(ROOT)
        self.root = Root()
        app = SimpleNamespace(root=self.root, user_data_dir=self.tmp.name)
        self.media = self.runtime.JTMediaController(app)
        self.media._intro_done = True
        self.media.on_phase_changed('MENU')
        self.media._admin_enabled = True

    def make_archive(self, set_id='imported_dinos', revision=1):
        fixture, source_root, manifest, resolve = make_portable_fixture()
        self.addCleanup(fixture.cleanup)
        manifest['set_id'] = set_id
        manifest['revision'] = revision
        manifest['display_name'] = 'Imported Dinosaurs'
        (source_root / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
        selection = load_set_manifest(resolve)
        archive = Path(self.tmp.name) / f'{set_id}.zip'
        self.media._set_storage.export_set(selection, selection.resolve_path, archive)
        return archive

    def test_import_is_not_player_visible_until_explicit_promotion_then_selector_marks_origin(self):
        result = self.media.workshop_import_zip(self.make_archive())
        self.assertEqual(result.set_id, 'imported_dinos')
        self.assertNotIn('imported_dinos', [s.set_id for s in self.media.sets.catalog()])

        self.media.promote_user_revision(result.set_id, result.revision)
        self.assertIn('imported_dinos', [s.set_id for s in self.media.sets.catalog()])
        self.media._open_set_selector()
        labels = [button.text for button in self.media._set_option_buttons]
        self.assertTrue(any('[OFFICIEL]' in label and 'Steg vs T-Rex' in label for label in labels))
        self.assertTrue(any('[UTILISATEUR]' in label and 'Imported Dinosaurs' in label for label in labels))

    def test_missing_promoted_revision_refresh_falls_back_to_canonical(self):
        result = self.media.workshop_import_zip(self.make_archive(set_id='vanishing'))
        self.media.promote_user_revision(result.set_id, result.revision)
        self.media.select_official_set('vanishing')
        shutil.rmtree(result.installed_path)

        self.media.refresh_player_catalog()

        self.assertEqual(self.media.sets.selected_set.set_id, CANONICAL_SET_ID)
        persisted = json.loads((Path(self.tmp.name) / 'jt-set-selection.json').read_text(encoding='utf-8'))
        self.assertEqual(persisted['set_id'], CANONICAL_SET_ID)


if __name__ == '__main__':
    unittest.main()
