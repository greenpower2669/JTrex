import io
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

try:
    from tools import jtrex_sets_android as androidmod
except ImportError:
    androidmod = None
from tools.jtrex_sets_io import JTSetStorage


class ManualThread:
    instances = []

    def __init__(self, target=None, daemon=None):
        self.target = target
        self.daemon = daemon
        self.started = False
        self.instances.append(self)

    def start(self):
        self.started = True

    def run(self):
        self.target()


class ManualClock:
    events = []

    @classmethod
    def schedule_once(cls, callback, delay=0):
        event = SimpleNamespace(callback=callback, delay=delay)
        cls.events.append(event)
        return event


class AsyncIngressTests(unittest.TestCase):
    def setUp(self):
        if androidmod is None:
            self.fail('tools.jtrex_sets_android missing')
        ManualThread.instances = []
        ManualClock.events = []
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.storage = JTSetStorage(root / 'official', root / 'user', root / 'draft')

    def test_copy_returns_immediately_worker_reads_and_completion_runs_on_clock(self):
        opens = []
        results = []
        ingress = androidmod.JTAsyncIngress(self.storage, ManualClock, thread_factory=ManualThread)
        with patch.object(androidmod, 'open_content_stream', side_effect=lambda uri: opens.append(uri) or io.BytesIO(b'abcdef')):
            thread = ingress.copy('content://video/1', 'picked.mp4', lambda path, error: results.append((path, error)))
            self.assertTrue(thread.started)
            self.assertEqual(opens, [])
            self.assertEqual(results, [])
            self.assertEqual(ManualClock.events, [])

            thread.run()
            self.assertEqual(opens, ['content://video/1'])
            self.assertEqual(results, [])
            self.assertEqual(len(ManualClock.events), 1)
            ManualClock.events[0].callback(0)

        self.assertIsNone(results[0][1])
        self.assertEqual(Path(results[0][0]).read_bytes(), b'abcdef')

    def test_copy_error_is_marshaled_and_partial_file_is_cleaned(self):
        class BrokenStream(io.BytesIO):
            def read(self, *args):
                if self.tell() > 0:
                    raise OSError('read failed')
                return super().read(3)

        results = []
        ingress = androidmod.JTAsyncIngress(self.storage, ManualClock, thread_factory=ManualThread)
        with patch.object(androidmod, 'open_content_stream', return_value=BrokenStream(b'abcdef')):
            thread = ingress.copy('content://video/bad', 'bad.mp4', lambda path, error: results.append((path, error)))
            thread.run()
            self.assertFalse((self.storage.draft_root / 'bad.mp4').exists())
            self.assertFalse((self.storage.draft_root / '.bad.mp4.tmp').exists())
            ManualClock.events[-1].callback(0)
        self.assertIsNone(results[0][0])
        self.assertIsInstance(results[0][1], OSError)

    def test_export_builds_and_writes_off_ui_thread_then_cleans_temp(self):
        output = Path(self.tmp.name) / 'export-target.bin'
        output.write_bytes(b'')
        target_fd = os.open(output, os.O_RDWR)
        self.addCleanup(lambda: os.close(target_fd))
        results = []
        calls = []
        egress = androidmod.JTAsyncEgress(ManualClock, thread_factory=ManualThread)

        def build_archive():
            calls.append('build')
            source = Path(self.tmp.name) / 'generated.jtrex.zip'
            source.write_bytes(b'zip-payload')
            return source

        def fake_output(uri):
            calls.append(('open', uri))
            return os.fdopen(os.dup(target_fd), 'wb', closefd=True)

        with patch.object(androidmod, 'open_content_output_stream', side_effect=fake_output):
            thread = egress.export(
                'content://exports/1', build_archive,
                lambda written, error: results.append((written, error)),
            )
            self.assertTrue(thread.started)
            self.assertEqual(calls, [])
            self.assertEqual(results, [])
            thread.run()
            self.assertEqual(calls, ['build', ('open', 'content://exports/1')])
            self.assertFalse((Path(self.tmp.name) / 'generated.jtrex.zip').exists())
            self.assertEqual(results, [])
            ManualClock.events[-1].callback(0)

        self.assertEqual(output.read_bytes(), b'zip-payload')
        self.assertEqual(results, [(len(b'zip-payload'), None)])


if __name__ == '__main__':
    unittest.main()
