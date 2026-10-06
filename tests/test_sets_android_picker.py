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


class FakeActivityModule:
    def __init__(self):
        self.bound = {}
        self.unbound = []

    def bind(self, **kwargs):
        self.bound.update(kwargs)

    def unbind(self, **kwargs):
        self.unbound.extend(kwargs)
        for key in kwargs:
            self.bound.pop(key, None)


class FakeCurrentActivity:
    def __init__(self):
        self.started = []
        self.error = None
        self.resolver = None

    def startActivityForResult(self, intent, request_code):
        if self.error:
            raise self.error
        self.started.append((intent, request_code))

    def getContentResolver(self):
        return self.resolver


class FakeIntent:
    ACTION_OPEN_DOCUMENT = 'OPEN'
    ACTION_CREATE_DOCUMENT = 'CREATE'
    CATEGORY_OPENABLE = 'OPENABLE'
    EXTRA_TITLE = 'TITLE'
    FLAG_GRANT_READ_URI_PERMISSION = 1
    FLAG_GRANT_WRITE_URI_PERMISSION = 2

    def __init__(self, action=None):
        self.action = action
        self.category = None
        self.mime = None
        self.flags = 0
        self.extras = {}

    def addCategory(self, category):
        self.category = category
        return self

    def setType(self, mime):
        self.mime = mime
        return self

    def addFlags(self, flags):
        self.flags |= flags
        return self

    def putExtra(self, key, value):
        self.extras[key] = value
        return self


class FakeActivity:
    RESULT_OK = -1
    RESULT_CANCELED = 0


class FakeUri:
    @staticmethod
    def parse(value):
        return 'parsed:' + value


class FakePFD:
    def __init__(self, fd):
        self.fd = fd
        self.closed = False

    def detachFd(self):
        fd, self.fd = self.fd, -1
        return fd

    def close(self):
        self.closed = True


class FakeResolver:
    def __init__(self, fd=None, error=None):
        self.fd = fd
        self.error = error
        self.calls = []

    def openFileDescriptor(self, uri, mode):
        self.calls.append((uri, mode))
        if self.error:
            raise self.error
        return None if self.fd is None else FakePFD(os.dup(self.fd))


class PickerTests(unittest.TestCase):
    def setUp(self):
        if androidmod is None:
            self.fail('tools.jtrex_sets_android missing')
        self.activity_module = FakeActivityModule()
        self.current = FakeCurrentActivity()
        self.pauses = 0
        self.resumes = 0

        class PythonActivity:
            pass
        PythonActivity.mActivity = self.current
        self.PythonActivity = PythonActivity

        def autoclass(name):
            return {
                'android.content.Intent': FakeIntent,
                'android.app.Activity': FakeActivity,
                'android.net.Uri': FakeUri,
                'org.kivy.android.PythonActivity': PythonActivity,
            }[name]

        self.bridge = (self.activity_module, autoclass)
        self.patch = patch.object(androidmod, '_android_objects', return_value=self.bridge)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def picker(self):
        return androidmod.AndroidDocumentPicker(
            on_pause=lambda: setattr(self, 'pauses', self.pauses + 1),
            on_resume=lambda: setattr(self, 'resumes', self.resumes + 1),
        )

    def test_picker_success_and_cancel_unbind_once(self):
        picker = self.picker()
        results = []
        first_code = picker.choose('video/mp4', lambda uri, error: results.append((uri, error)))
        self.assertEqual(self.pauses, 1)
        intent, code = self.current.started[-1]
        self.assertEqual(code, first_code)
        self.assertEqual((intent.action, intent.category, intent.mime), ('OPEN', 'OPENABLE', 'video/mp4'))
        cb = self.activity_module.bound['on_activity_result']
        cb(first_code, FakeActivity.RESULT_OK, SimpleNamespace(getData=lambda: 'content://picked/video'))
        self.assertEqual(results, [('content://picked/video', None)])
        self.assertEqual(self.resumes, 1)
        self.assertNotIn('on_activity_result', self.activity_module.bound)

        cancel = []
        second_code = picker.choose('image/*', lambda uri, error: cancel.append((uri, error)))
        self.activity_module.bound['on_activity_result'](second_code, FakeActivity.RESULT_CANCELED, None)
        self.assertEqual(cancel, [(None, None)])

    def test_create_document_uses_write_saf_and_returns_content_uri(self):
        picker = self.picker()
        results = []
        code = picker.create(
            'application/zip', 'raptor-r2.jtrex.zip',
            lambda uri, error: results.append((uri, error)),
        )
        intent, started_code = self.current.started[-1]
        self.assertEqual(started_code, code)
        self.assertEqual((intent.action, intent.category, intent.mime), ('CREATE', 'OPENABLE', 'application/zip'))
        self.assertEqual(intent.extras[FakeIntent.EXTRA_TITLE], 'raptor-r2.jtrex.zip')
        self.assertTrue(intent.flags & FakeIntent.FLAG_GRANT_WRITE_URI_PERMISSION)
        self.activity_module.bound['on_activity_result'](
            code, FakeActivity.RESULT_OK, SimpleNamespace(getData=lambda: 'content://exports/raptor')
        )
        self.assertEqual(results, [('content://exports/raptor', None)])

    def test_stale_or_duplicate_activity_result_is_ignored(self):
        picker = self.picker()
        first, second = [], []
        old_code = picker.choose('*/*', lambda uri, error: first.append(uri))
        old_callback = self.activity_module.bound['on_activity_result']
        picker.close()
        new_code = picker.choose('*/*', lambda uri, error: second.append(uri))
        self.assertNotEqual(old_code, new_code)
        current_callback = self.activity_module.bound['on_activity_result']

        old_callback(old_code, FakeActivity.RESULT_OK, SimpleNamespace(getData=lambda: 'content://old'))
        current_callback(old_code, FakeActivity.RESULT_OK, SimpleNamespace(getData=lambda: 'content://old2'))
        self.assertEqual(first, [])
        self.assertEqual(second, [])
        current_callback(new_code, FakeActivity.RESULT_OK, SimpleNamespace(getData=lambda: 'content://new'))
        current_callback(new_code, FakeActivity.RESULT_OK, SimpleNamespace(getData=lambda: 'content://duplicate'))
        self.assertEqual(second, ['content://new'])

    def test_start_failure_reports_error_and_close_unbinds(self):
        picker = self.picker()
        self.current.error = RuntimeError('no activity')
        results = []
        picker.choose('*/*', lambda uri, error: results.append((uri, error)))
        self.assertIsNone(results[0][0])
        self.assertIsInstance(results[0][1], RuntimeError)
        self.assertNotIn('on_activity_result', self.activity_module.bound)
        picker.close()

    def test_open_content_stream_detaches_read_fd_and_rejects_failures(self):
        with tempfile.NamedTemporaryFile(delete=False) as source:
            source.write(b'hello-content')
            source_path = source.name
        self.addCleanup(lambda: Path(source_path).unlink(missing_ok=True))
        fd = os.open(source_path, os.O_RDONLY)
        self.addCleanup(lambda: os.close(fd))
        self.current.resolver = FakeResolver(fd=fd)

        with androidmod.open_content_stream('content://docs/1') as stream:
            self.assertEqual(stream.read(), b'hello-content')
        self.assertEqual(self.current.resolver.calls, [('parsed:content://docs/1', 'r')])

        with self.assertRaises(ValueError):
            androidmod.open_content_stream('file:///tmp/nope')
        self.current.resolver = FakeResolver(error=PermissionError('denied'))
        with self.assertRaises(PermissionError):
            androidmod.open_content_stream('content://docs/denied')
        self.current.resolver = FakeResolver(fd=None)
        with self.assertRaises(OSError):
            androidmod.open_content_stream('content://docs/missing')

    def test_open_content_output_stream_detaches_write_fd(self):
        with tempfile.NamedTemporaryFile(delete=False) as target:
            target_path = target.name
        self.addCleanup(lambda: Path(target_path).unlink(missing_ok=True))
        fd = os.open(target_path, os.O_RDWR)
        self.addCleanup(lambda: os.close(fd))
        self.current.resolver = FakeResolver(fd=fd)

        with androidmod.open_content_output_stream('content://exports/1') as stream:
            stream.write(b'portable-zip')
            stream.flush()
        self.assertEqual(self.current.resolver.calls, [('parsed:content://exports/1', 'w')])
        self.assertEqual(Path(target_path).read_bytes(), b'portable-zip')

        with self.assertRaises(ValueError):
            androidmod.open_content_output_stream('file:///tmp/nope')


if __name__ == '__main__':
    unittest.main()
