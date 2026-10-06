"""Thin Android SAF bridge for JTrex set workshop ingress.

Android imports are deferred so desktop/unit-test environments can import this
module. Security, byte limits and cleanup remain owned by JTSetStorage.
"""
import os
from pathlib import Path
import threading

if __package__:
    from .jtrex_sets_io import JTSetStorage
else:
    from jtrex_sets_io import JTSetStorage


def _android_objects():
    from android import activity
    from jnius import autoclass
    return activity, autoclass


class AndroidDocumentPicker:
    _next_request_code = 64100

    def __init__(self, on_pause=None, on_resume=None):
        self._on_pause = on_pause
        self._on_resume = on_resume
        self._activity_module = None
        self._callback = None
        self._request_code = None
        self._bound = False
        self._closed_generation = 0

    @classmethod
    def _allocate_request_code(cls):
        cls._next_request_code += 1
        if cls._next_request_code > 64999:
            cls._next_request_code = 64101
        return cls._next_request_code

    def _unbind(self):
        if self._bound and self._activity_module is not None:
            try:
                self._activity_module.unbind(on_activity_result=self._on_activity_result)
            except Exception:
                pass
        self._bound = False

    def _resume(self):
        callback = self._on_resume
        if callback is not None:
            try:
                callback()
            except Exception:
                pass

    def _begin(self, intent, callback, activity_module, PythonActivity):
        if not callable(callback):
            raise TypeError("callback must be callable")
        if self._callback is not None:
            raise RuntimeError("document picker already active")
        request_code = self._allocate_request_code()
        self._activity_module = activity_module
        self._callback = callback
        self._request_code = request_code
        activity_module.bind(on_activity_result=self._on_activity_result)
        self._bound = True
        try:
            if self._on_pause is not None:
                self._on_pause()
            PythonActivity.mActivity.startActivityForResult(intent, request_code)
        except Exception as exc:
            cb = self._callback
            self._callback = None
            self._request_code = None
            self._unbind()
            self._resume()
            cb(None, exc)
        return request_code

    def choose(self, mime_type, callback):
        if not isinstance(mime_type, str) or not mime_type:
            raise ValueError("mime_type required")
        activity_module, autoclass = _android_objects()
        Intent = autoclass("android.content.Intent")
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        intent = Intent(Intent.ACTION_OPEN_DOCUMENT)
        intent.addCategory(Intent.CATEGORY_OPENABLE)
        intent.setType(mime_type)
        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        return self._begin(intent, callback, activity_module, PythonActivity)

    def create(self, mime_type, suggested_name, callback):
        if not isinstance(mime_type, str) or not mime_type:
            raise ValueError("mime_type required")
        if (
            not isinstance(suggested_name, str)
            or not suggested_name.strip()
            or "\x00" in suggested_name
        ):
            raise ValueError("suggested_name required")
        activity_module, autoclass = _android_objects()
        Intent = autoclass("android.content.Intent")
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        intent = Intent(Intent.ACTION_CREATE_DOCUMENT)
        intent.addCategory(Intent.CATEGORY_OPENABLE)
        intent.setType(mime_type)
        intent.putExtra(Intent.EXTRA_TITLE, suggested_name)
        intent.addFlags(Intent.FLAG_GRANT_WRITE_URI_PERMISSION)
        return self._begin(intent, callback, activity_module, PythonActivity)

    def _on_activity_result(self, request_code, result_code, data):
        if self._callback is None or request_code != self._request_code:
            return
        callback = self._callback
        self._callback = None
        self._request_code = None
        self._unbind()
        uri = None
        error = None
        try:
            _activity_module, autoclass = _android_objects()
            Activity = autoclass("android.app.Activity")
            if result_code == Activity.RESULT_OK:
                if data is None:
                    raise OSError("document picker returned no data")
                picked = data.getData()
                if picked is None:
                    raise OSError("document picker returned no URI")
                uri = str(picked)
                if not uri.startswith("content://"):
                    raise OSError("document picker returned non-content URI")
        except Exception as exc:
            error = exc
            uri = None
        finally:
            self._resume()
        callback(uri, error)

    def close(self):
        was_active = self._callback is not None
        self._callback = None
        self._request_code = None
        self._closed_generation += 1
        self._unbind()
        if was_active:
            self._resume()


def open_content_stream(uri):
    if not isinstance(uri, str) or not uri.startswith("content://"):
        raise ValueError("content:// URI required")
    _activity_module, autoclass = _android_objects()
    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    Uri = autoclass("android.net.Uri")
    resolver = PythonActivity.mActivity.getContentResolver()
    descriptor = resolver.openFileDescriptor(Uri.parse(uri), "r")
    if descriptor is None:
        raise OSError("content descriptor unavailable")
    try:
        fd = descriptor.detachFd()
    finally:
        try:
            descriptor.close()
        except Exception:
            pass
    if not isinstance(fd, int) or fd < 0:
        raise OSError("invalid content file descriptor")
    try:
        return os.fdopen(fd, "rb", closefd=True)
    except Exception:
        os.close(fd)
        raise


def open_content_output_stream(uri):
    if not isinstance(uri, str) or not uri.startswith("content://"):
        raise ValueError("content:// URI required")
    _activity_module, autoclass = _android_objects()
    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    Uri = autoclass("android.net.Uri")
    resolver = PythonActivity.mActivity.getContentResolver()
    descriptor = resolver.openFileDescriptor(Uri.parse(uri), "w")
    if descriptor is None:
        raise OSError("content descriptor unavailable")
    try:
        fd = descriptor.detachFd()
    finally:
        try:
            descriptor.close()
        except Exception:
            pass
    if not isinstance(fd, int) or fd < 0:
        raise OSError("invalid content file descriptor")
    try:
        return os.fdopen(fd, "wb", closefd=True)
    except Exception:
        os.close(fd)
        raise


class JTAsyncIngress:
    def __init__(self, storage, clock, thread_factory=None):
        if not isinstance(storage, JTSetStorage):
            raise TypeError("storage must be JTSetStorage")
        self.storage = storage
        self.clock = clock
        self.thread_factory = thread_factory or threading.Thread

    def copy(self, uri, draft_name, on_done):
        if not callable(on_done):
            raise TypeError("on_done must be callable")

        def worker():
            path = None
            error = None
            try:
                path = self.storage.copy_content_uri(uri, open_content_stream, draft_name)
            except Exception as exc:
                error = exc
            self.clock.schedule_once(
                lambda dt, path=path, error=error: on_done(path, error), 0
            )

        thread = self.thread_factory(target=worker, daemon=True)
        thread.start()
        return thread


class JTAsyncEgress:
    """Build and copy one portable archive without blocking the Kivy thread."""

    def __init__(self, clock, thread_factory=None):
        self.clock = clock
        self.thread_factory = thread_factory or threading.Thread

    def export(self, uri, build_archive, on_done, chunk_size=1024 * 1024):
        if not isinstance(uri, str) or not uri.startswith("content://"):
            raise ValueError("content:// URI required")
        if not callable(build_archive):
            raise TypeError("build_archive must be callable")
        if not callable(on_done):
            raise TypeError("on_done must be callable")
        if not isinstance(chunk_size, int) or isinstance(chunk_size, bool) or chunk_size < 1:
            raise ValueError("chunk_size must be >= 1")

        def worker():
            source_path = None
            written = 0
            error = None
            try:
                source_path = Path(build_archive())
                if not source_path.is_file():
                    raise OSError("export archive unavailable")
                with source_path.open("rb") as source, open_content_output_stream(uri) as target:
                    while True:
                        block = source.read(chunk_size)
                        if not block:
                            break
                        target.write(block)
                        written += len(block)
                    target.flush()
            except Exception as exc:
                error = exc
            finally:
                if source_path is not None:
                    try:
                        source_path.unlink()
                    except OSError:
                        pass
            self.clock.schedule_once(
                lambda dt, written=written, error=error: on_done(written, error), 0
            )

        thread = self.thread_factory(target=worker, daemon=True)
        thread.start()
        return thread
