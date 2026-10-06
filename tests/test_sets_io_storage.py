import io
import tempfile
import unittest
from pathlib import Path


class FailingStream(io.BytesIO):
    def __init__(self, initial, fail_after=1):
        super().__init__(initial)
        self._reads = 0
        self._fail_after = fail_after

    def read(self, size=-1):
        self._reads += 1
        if self._reads > self._fail_after:
            raise OSError('stream interrupted')
        return super().read(size)


class StorageContractTests(unittest.TestCase):
    def setUp(self):
        from tools.jtrex_sets_io import JTSetIOLimits, JTSetStorage
        self.JTSetIOLimits = JTSetIOLimits
        self.JTSetStorage = JTSetStorage
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def storage(self, limits=None):
        return self.JTSetStorage(
            self.root / 'official',
            self.root / 'user',
            self.root / 'draft',
            limits=limits,
        )

    def test_v1_limits_are_exact_and_centralized(self):
        limits = self.JTSetIOLimits()
        self.assertEqual(limits.max_zip_bytes, 512 * 1024 * 1024)
        self.assertEqual(limits.max_extracted_bytes, 1024 * 1024 * 1024)
        self.assertEqual(limits.max_files, 512)
        self.assertEqual(limits.max_file_bytes, 512 * 1024 * 1024)
        self.assertEqual(limits.max_manifest_bytes, 1024 * 1024)
        self.assertEqual(limits.max_path_chars, 240)

    def test_roots_are_separate_and_constructor_does_not_modify_official_root(self):
        official = self.root / 'official'
        storage = self.storage()
        self.assertFalse(official.exists())
        self.assertTrue(storage.user_root.is_dir())
        self.assertTrue(storage.draft_root.is_dir())
        with self.assertRaises(ValueError):
            self.JTSetStorage(self.root / 'same', self.root / 'same', self.root / 'draft2')
        with self.assertRaises(ValueError):
            self.JTSetStorage(self.root / 'a', self.root / 'a/user', self.root / 'd')

    def test_user_revision_path_is_confined_and_revisioned(self):
        storage = self.storage()
        self.assertEqual(storage.user_revision_path('raptor_vs_trike', 3), storage.user_root / 'raptor_vs_trike' / 'r3')
        for set_id, revision in (('../x', 1), ('bad/id', 1), ('ok', 0), ('ok', True)):
            with self.subTest(set_id=set_id, revision=revision):
                with self.assertRaises(ValueError):
                    storage.user_revision_path(set_id, revision)

    def test_draft_path_is_local_and_rejects_unsafe_name(self):
        storage = self.storage()
        self.assertEqual(storage.draft_path('incoming.zip'), storage.draft_root / 'incoming.zip')
        for name in ('../x', '/tmp/x', 'dir/x', 'dir\\x', '', 'x\x00.zip'):
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    storage.draft_path(name)

    def test_copy_content_uri_writes_local_draft_file(self):
        storage = self.storage()
        opened = []
        def open_stream(uri):
            opened.append(uri)
            return io.BytesIO(b'abc123')

        path = storage.copy_content_uri('content://provider/item/7', open_stream, 'picked.bin')

        self.assertEqual(opened, ['content://provider/item/7'])
        self.assertEqual(path, storage.draft_root / 'picked.bin')
        self.assertEqual(path.read_bytes(), b'abc123')

    def test_copy_content_uri_rejects_non_content_uri_and_existing_destination(self):
        storage = self.storage()
        with self.assertRaises(ValueError):
            storage.copy_content_uri('file:///tmp/a', lambda uri: io.BytesIO(b'x'), 'a.bin')
        existing = storage.draft_path('a.bin')
        existing.write_bytes(b'old')
        with self.assertRaises(FileExistsError):
            storage.copy_content_uri('content://provider/a', lambda uri: io.BytesIO(b'new'), 'a.bin')
        self.assertEqual(existing.read_bytes(), b'old')

    def test_copy_content_uri_enforces_real_byte_limit_and_cleans_partial(self):
        limits = self.JTSetIOLimits(max_file_bytes=4)
        storage = self.storage(limits)
        with self.assertRaisesRegex(ValueError, 'limit'):
            storage.copy_content_uri('content://provider/large', lambda uri: io.BytesIO(b'12345'), 'large.bin')
        self.assertFalse((storage.draft_root / 'large.bin').exists())
        self.assertEqual(list(storage.draft_root.glob('*.tmp')), [])

    def test_copy_content_uri_cleans_partial_on_stream_failure(self):
        storage = self.storage()
        with self.assertRaisesRegex(OSError, 'interrupted'):
            storage.copy_content_uri(
                'content://provider/broken',
                lambda uri: FailingStream(b'abcdef', fail_after=1),
                'broken.bin',
                chunk_size=2,
            )
        self.assertFalse((storage.draft_root / 'broken.bin').exists())
        self.assertEqual(list(storage.draft_root.glob('*.tmp')), [])


if __name__ == '__main__':
    unittest.main()
