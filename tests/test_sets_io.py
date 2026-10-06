import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from tools import jtrex_sets_runtime as runtime

ROOT = Path(__file__).resolve().parents[1]


def make_portable_fixture():
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    manifest = json.loads((ROOT / 'assets/sets/trex_vs_steg/manifest.json').read_text(encoding='utf-8'))
    for index, asset in enumerate(manifest['assets']):
        data = ('asset-%02d-%s' % (index, asset['id'])).encode('utf-8')
        path = root / asset['path']
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        asset['size'] = len(data)
        asset['sha256'] = hashlib.sha256(data).hexdigest()
    (root / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')

    def resolve(relative):
        path = root / relative
        return str(path) if path.is_file() else None

    return tmp, root, manifest, resolve


class PortableSetRuntimeTests(unittest.TestCase):
    def test_load_set_manifest_validates_portable_manifest_without_catalog(self):
        tmp, root, manifest, resolve = make_portable_fixture()
        self.addCleanup(tmp.cleanup)

        selection = runtime.load_set_manifest(resolve)

        self.assertEqual(selection.set_id, manifest['set_id'])
        self.assertEqual(selection.revision, manifest['revision'])
        self.assertEqual(selection.manifest_path, 'manifest.json')

    def test_manifest_returns_defensive_copy(self):
        tmp, root, manifest, resolve = make_portable_fixture()
        self.addCleanup(tmp.cleanup)
        selection = runtime.load_set_manifest(resolve)

        copy_a = selection.manifest()
        copy_a['display_name'] = 'mutated'
        copy_a['assets'][0]['path'] = 'wrong'

        copy_b = selection.manifest()
        self.assertEqual(copy_b['display_name'], manifest['display_name'])
        self.assertEqual(copy_b['assets'][0]['path'], manifest['assets'][0]['path'])

    def test_verify_selection_assets_streams_and_returns_verified_entries(self):
        tmp, root, manifest, resolve = make_portable_fixture()
        self.addCleanup(tmp.cleanup)
        selection = runtime.load_set_manifest(resolve)

        verified = runtime.verify_selection_assets(selection, resolve)

        self.assertEqual(len(verified), len(manifest['assets']))
        self.assertEqual(verified[0]['id'], manifest['assets'][0]['id'])
        self.assertEqual(verified[-1]['sha256'], manifest['assets'][-1]['sha256'])

    def test_verify_selection_assets_rejects_missing_file(self):
        tmp, root, manifest, resolve = make_portable_fixture()
        self.addCleanup(tmp.cleanup)
        selection = runtime.load_set_manifest(resolve)
        (root / manifest['assets'][0]['path']).unlink()

        with self.assertRaisesRegex(runtime.SetContractError, 'unavailable'):
            runtime.verify_selection_assets(selection, resolve)

    def test_verify_selection_assets_rejects_forged_size_or_sha(self):
        for field in ('size', 'sha256'):
            with self.subTest(field=field):
                tmp, root, manifest, resolve = make_portable_fixture()
                self.addCleanup(tmp.cleanup)
                if field == 'size':
                    manifest['assets'][0]['size'] += 1
                else:
                    manifest['assets'][0]['sha256'] = '0' * 64
                (root / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
                selection = runtime.load_set_manifest(resolve)

                with self.assertRaisesRegex(runtime.SetContractError, field):
                    runtime.verify_selection_assets(selection, resolve)


if __name__ == '__main__':
    unittest.main()
