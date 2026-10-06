import json
import stat
import struct
import tempfile
import unittest
import zipfile
from pathlib import Path

from tests.test_sets_io import make_portable_fixture
from tools.jtrex_sets_io import JTSetIOLimits, JTSetStorage


def clone_zip(source, destination, transform=None, skip=None, extras=()):
    skip = set(skip or ())
    with zipfile.ZipFile(source, 'r') as src, zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_STORED) as dst:
        for info in src.infolist():
            if info.filename in skip:
                continue
            data = src.read(info.filename)
            new_info = zipfile.ZipInfo(info.filename)
            new_info.external_attr = info.external_attr
            new_info.compress_type = zipfile.ZIP_STORED
            if transform:
                new_info, data = transform(new_info, data)
            dst.writestr(new_info, data)
        for name, data, external_attr in extras:
            info = zipfile.ZipInfo(name)
            info.external_attr = external_attr
            dst.writestr(info, data)


def mark_first_member_encrypted(path):
    raw = bytearray(Path(path).read_bytes())
    local = raw.find(b'PK\x03\x04')
    central = raw.find(b'PK\x01\x02')
    if local < 0 or central < 0:
        raise AssertionError('zip headers missing')
    lflag = struct.unpack_from('<H', raw, local + 6)[0] | 1
    cflag = struct.unpack_from('<H', raw, central + 8)[0] | 1
    struct.pack_into('<H', raw, local + 6, lflag)
    struct.pack_into('<H', raw, central + 8, cflag)
    Path(path).write_bytes(raw)


class ZipSecurityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.storage = JTSetStorage(self.root / 'official', self.root / 'user', self.root / 'draft')
        fixture, self.source_root, manifest, self.resolve = make_portable_fixture()
        self.addCleanup(fixture.cleanup)
        from tools.jtrex_sets_runtime import load_set_manifest
        self.selection = load_set_manifest(self.resolve)
        self.good = self.storage.export_set(self.selection, self.resolve, self.root / 'good.zip')

    def assert_import_rejected(self, archive, pattern=None, storage=None):
        storage = storage or self.storage
        context = self.assertRaisesRegex(Exception, pattern) if pattern else self.assertRaises(Exception)
        with context:
            storage.import_set_zip(archive)
        self.assertEqual(list(storage.user_root.glob('.jtrex-stage-*')), [])

    def test_rejects_unsafe_member_names_and_casefold_duplicates_before_install(self):
        for name in ('../escape.bin', '/absolute.bin', 'dir\\evil.bin', 'C:drive.bin'):
            with self.subTest(name=name):
                bad = self.root / ('bad-' + str(abs(hash(name))) + '.zip')
                clone_zip(self.good, bad, extras=((name, b'x', 0),))
                self.assert_import_rejected(bad, 'path|member|unsafe')
        with self.assertRaises(ValueError):
            self.storage._validate_member_name('bad\x00name')
        first_asset = self.selection.assets()[0]['path']
        dup = self.root / 'casefold.zip'
        clone_zip(self.good, dup, extras=((first_asset.upper(), b'x', 0),))
        self.assert_import_rejected(dup, 'duplicate|collision')

    def test_rejects_symlink_encrypted_and_executable_or_extra_members(self):
        target = self.selection.assets()[0]['path']
        symlink = self.root / 'symlink.zip'
        def symlink_transform(info, data):
            if info.filename == target:
                info.external_attr = (stat.S_IFLNK | 0o777) << 16
                return info, b'../../outside'
            return info, data
        clone_zip(self.good, symlink, transform=symlink_transform)
        self.assert_import_rejected(symlink, 'symlink')

        encrypted = self.root / 'encrypted.zip'
        clone_zip(self.good, encrypted)
        mark_first_member_encrypted(encrypted)
        self.assert_import_rejected(encrypted, 'encrypted')

        extra = self.root / 'extra.zip'
        clone_zip(self.good, extra, extras=(('evil.py', b'print(1)', 0),))
        self.assert_import_rejected(extra, 'executable|extra|unexpected')

    def test_rejects_missing_asset_and_incompatible_manifest(self):
        missing = self.root / 'missing.zip'
        clone_zip(self.good, missing, skip={self.selection.assets()[0]['path']})
        self.assert_import_rejected(missing, 'missing|member')

        incompatible = self.root / 'format.zip'
        def change_manifest(info, data):
            if info.filename == 'manifest.json':
                payload = json.loads(data.decode('utf-8'))
                payload['format_version'] = 999
                data = json.dumps(payload).encode('utf-8')
            return info, data
        clone_zip(self.good, incompatible, transform=change_manifest)
        self.assert_import_rejected(incompatible, 'format')

    def test_rejects_forged_manifest_size_and_sha(self):
        for field in ('size', 'sha256'):
            with self.subTest(field=field):
                bad = self.root / f'forged-{field}.zip'
                def mutate(info, data, field=field):
                    if info.filename == 'manifest.json':
                        payload = json.loads(data.decode('utf-8'))
                        if field == 'size':
                            payload['assets'][0]['size'] += 1
                        else:
                            payload['assets'][0]['sha256'] = '0' * 64
                        data = json.dumps(payload).encode('utf-8')
                    return info, data
                clone_zip(self.good, bad, transform=mutate)
                self.assert_import_rejected(bad, field)

    def test_rejects_official_id_collision(self):
        with self.assertRaisesRegex(Exception, 'official'):
            self.storage.import_set_zip(self.good, official_set_ids=(self.selection.set_id,))
        self.assertFalse(self.storage.user_revision_path(self.selection.set_id, self.selection.revision).exists())

    def test_rejects_archive_file_count_and_member_limits(self):
        limited = JTSetStorage(
            self.root / 'official2', self.root / 'user2', self.root / 'draft2',
            limits=JTSetIOLimits(max_files=2, max_file_bytes=8),
        )
        self.assert_import_rejected(self.good, 'limit|files|size', storage=limited)

    def test_rejects_real_extracted_byte_mismatch(self):
        # Unit-level guard for a malicious/lying ZipInfo: actual copied bytes must
        # match the declared uncompressed size even when they stay below global limits.
        class Info:
            filename = 'asset.bin'
            file_size = 3
        class Reader:
            def open(self, info, mode='r'):
                import io
                return io.BytesIO(b'abcd')
        destination = self.root / 'real-bytes.bin'
        with self.assertRaisesRegex(Exception, 'size|bytes'):
            self.storage._extract_member(Reader(), Info(), destination, [0])
        self.assertFalse(destination.exists())


if __name__ == '__main__':
    unittest.main()
