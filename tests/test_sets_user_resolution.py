import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tests.test_sets_io import make_portable_fixture
from tools.jtrex_sets_io import JTSetStorage
from tools.jtrex_sets_runtime import (
    CANONICAL_SET_ID,
    SetContractError,
    load_official_set,
    load_set_manifest,
)

ROOT = Path(__file__).resolve().parents[1]


def resolver(root):
    root = Path(root)
    def resolve(relative):
        path = root / relative
        return str(path) if path.is_file() else None
    return resolve


def install_user_revision(storage, set_id='raptor_vs_trike', revision=1):
    fixture, source_root, manifest, _ = make_portable_fixture()
    manifest['set_id'] = set_id
    manifest['revision'] = revision
    manifest['display_name'] = f'User {set_id} r{revision}'
    (source_root / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
    final = storage.user_revision_path(set_id, revision)
    final.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_root, final)
    return fixture, final, manifest


class SelectionResolverTests(unittest.TestCase):
    def test_official_and_user_selection_keep_their_own_physical_resolver(self):
        official = load_official_set(resolver(ROOT))
        fixture, user_root, manifest, user_resolve = make_portable_fixture()
        self.addCleanup(fixture.cleanup)
        manifest['set_id'] = 'raptor_vs_trike'
        (user_root / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
        user = load_set_manifest(user_resolve)

        relative = official.assets()[0]['path']
        asset_id = official.assets()[0]['id']
        self.assertEqual(Path(official.resolve_path(relative)), ROOT / relative)
        self.assertEqual(Path(user.resolve_path(relative)), user_root / relative)
        self.assertNotEqual(official.resolve_path(relative), user.resolve_path(relative))
        self.assertEqual(user.resolve_asset(asset_id), user.resolve_path(relative))

    def test_deepcopied_selection_preserves_runtime_resolver(self):
        fixture, root, manifest, resolve = make_portable_fixture()
        self.addCleanup(fixture.cleanup)
        selection = load_set_manifest(resolve)
        import copy
        cloned = copy.deepcopy(selection)
        relative = manifest['assets'][0]['path']
        self.assertEqual(cloned.resolve_path(relative), str(root / relative))


class PromotedUserCatalogTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        official = self.root / 'official'
        (official / 'assets/sets').mkdir(parents=True)
        shutil.copy2(ROOT / 'assets/sets/catalog.json', official / 'assets/sets/catalog.json')
        self.storage = JTSetStorage(official, self.root / 'user', self.root / 'draft')

    def test_list_user_revisions_and_loaded_selection_resolve_inside_installed_revision(self):
        f2, r2, m2 = install_user_revision(self.storage, revision=2)
        f1, r1, m1 = install_user_revision(self.storage, revision=1)
        self.addCleanup(f1.cleanup)
        self.addCleanup(f2.cleanup)

        self.assertEqual(self.storage.list_user_revisions(), (('raptor_vs_trike', 1), ('raptor_vs_trike', 2)))
        loaded = self.storage.load_user_revision('raptor_vs_trike', 2)
        asset = m2['assets'][0]
        self.assertEqual(loaded.resolve_asset(asset['id']), str(r2 / asset['path']))

    def test_promote_is_atomic_and_promoted_catalog_loads_exact_revision(self):
        fixture, final, manifest = install_user_revision(self.storage, revision=2)
        self.addCleanup(fixture.cleanup)
        calls = []
        real_replace = self.storage._replace
        def record(src, dst):
            calls.append((Path(src), Path(dst)))
            return real_replace(src, dst)
        self.storage._replace = record

        self.storage.promote('raptor_vs_trike', 2)

        self.assertEqual(self.storage.load_promotions(), {'raptor_vs_trike': 2})
        self.assertEqual(len(calls), 1)
        promoted = self.storage.promoted_catalog()
        self.assertEqual([(s.set_id, s.revision) for s in promoted], [('raptor_vs_trike', 2)])
        self.assertEqual(promoted[0].resolve_path(manifest['assets'][0]['path']), str(final / manifest['assets'][0]['path']))
        self.assertEqual(list(self.storage.user_root.glob('*.tmp')), [])

    def test_promoted_catalog_prunes_missing_or_corrupt_revision(self):
        fixture, final, manifest = install_user_revision(self.storage, revision=3)
        self.addCleanup(fixture.cleanup)
        self.storage.promote('raptor_vs_trike', 3)
        shutil.rmtree(final)

        self.assertEqual(self.storage.promoted_catalog(), ())
        self.assertEqual(self.storage.load_promotions(), {})

    def test_official_id_cannot_be_promoted_as_user_set(self):
        fixture, final, manifest = install_user_revision(self.storage, set_id=CANONICAL_SET_ID, revision=9)
        self.addCleanup(fixture.cleanup)
        with self.assertRaisesRegex(SetContractError, 'official'):
            self.storage.promote(CANONICAL_SET_ID, 9)


if __name__ == '__main__':
    unittest.main()
