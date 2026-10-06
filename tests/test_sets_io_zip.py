import tempfile
import unittest
import zipfile
from pathlib import Path

from tests.test_sets_io import make_portable_fixture
from tools.jtrex_sets_runtime import verify_selection_assets
from tools.jtrex_sets_io import JTSetStorage


class ZipRoundTripTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.storage = JTSetStorage(
            self.root / 'official', self.root / 'user', self.root / 'draft'
        )
        self.fixture, self.source_root, self.manifest, self.resolve = make_portable_fixture()
        self.addCleanup(self.fixture.cleanup)
        from tools.jtrex_sets_runtime import load_set_manifest
        self.selection = load_set_manifest(self.resolve)

    def test_export_contains_exactly_manifest_and_referenced_assets(self):
        output = self.root / 'portable.jtrex.zip'

        result = self.storage.export_set(self.selection, self.resolve, output)

        self.assertEqual(result, output)
        with zipfile.ZipFile(output) as archive:
            names = archive.namelist()
            expected = ['manifest.json'] + [asset['path'] for asset in self.selection.assets()]
            self.assertEqual(set(names), set(expected))
            self.assertEqual(len(names), len(expected))

    def test_export_import_round_trip_restores_identical_manifest_and_hashes(self):
        archive = self.storage.export_set(self.selection, self.resolve, self.root / 'portable.zip')

        result = self.storage.import_set_zip(archive)
        loaded = self.storage.load_user_revision(result.set_id, result.revision)

        self.assertEqual(result.set_id, self.selection.set_id)
        self.assertEqual(result.revision, self.selection.revision)
        self.assertEqual(result.installed_path, self.storage.user_revision_path(result.set_id, result.revision))
        self.assertEqual(loaded.manifest(), self.selection.manifest())
        verified = verify_selection_assets(loaded, lambda rel: str(result.installed_path / rel) if (result.installed_path / rel).is_file() else None)
        self.assertEqual(tuple(a['sha256'] for a in verified), tuple(a['sha256'] for a in self.selection.assets()))

    def test_same_revision_collision_never_overwrites_existing_install(self):
        archive = self.storage.export_set(self.selection, self.resolve, self.root / 'portable.zip')
        first = self.storage.import_set_zip(archive)
        sentinel = first.installed_path / 'sentinel.txt'
        sentinel.write_text('keep', encoding='utf-8')

        with self.assertRaises(FileExistsError):
            self.storage.import_set_zip(archive)

        self.assertEqual(sentinel.read_text(encoding='utf-8'), 'keep')

    def test_failed_final_rename_preserves_previous_revision_and_cleans_staging(self):
        archive = self.storage.export_set(self.selection, self.resolve, self.root / 'portable.zip')
        prior = self.storage.user_revision_path(self.selection.set_id, 99)
        prior.mkdir(parents=True)
        (prior / 'keep.txt').write_text('old', encoding='utf-8')
        real_rename = self.storage._rename
        def fail_rename(src, dst):
            raise OSError('simulated interruption')
        self.storage._rename = fail_rename
        self.addCleanup(setattr, self.storage, '_rename', real_rename)

        with self.assertRaisesRegex(Exception, 'simulated interruption'):
            self.storage.import_set_zip(archive)

        self.assertEqual((prior / 'keep.txt').read_text(encoding='utf-8'), 'old')
        self.assertFalse(self.storage.user_revision_path(self.selection.set_id, self.selection.revision).exists())
        self.assertEqual(list(self.storage.user_root.glob('.jtrex-stage-*')), [])
