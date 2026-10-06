"""Safe storage and portable ZIP I/O for June T-Rex DATA/MEDIA sets."""
from contextlib import closing
from dataclasses import dataclass
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import tempfile
import zipfile

if __package__:
    from .jtrex_sets_runtime import (
        JTSetSelection, load_set_manifest, verify_selection_assets,
    )
else:
    from jtrex_sets_runtime import (
        JTSetSelection, load_set_manifest, verify_selection_assets,
    )

_SAFE_ID = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
_SAFE_DRAFT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_FORBIDDEN_SUFFIXES = frozenset({
    ".py", ".pyc", ".pyo", ".kv", ".so", ".dll", ".dylib", ".exe",
    ".apk", ".aab", ".jar", ".class", ".pickle", ".pkl", ".sh",
    ".bat", ".cmd", ".ps1", ".js", ".html", ".htm",
})


class JTSetIOError(ValueError):
    pass


@dataclass(frozen=True)
class JTSetIOLimits:
    max_zip_bytes: int = 512 * 1024 * 1024
    max_extracted_bytes: int = 1024 * 1024 * 1024
    max_files: int = 512
    max_file_bytes: int = 512 * 1024 * 1024
    max_manifest_bytes: int = 1024 * 1024
    max_path_chars: int = 240

    def __post_init__(self):
        for name, value in self.__dict__.items():
            if not isinstance(value, int) or isinstance(value, bool) or value < 1:
                raise ValueError(f"{name} must be a positive integer")


@dataclass(frozen=True)
class ImportResult:
    set_id: str
    revision: int
    installed_path: Path


def _resolved(path):
    return Path(path).expanduser().resolve(strict=False)


def _paths_overlap(left, right):
    left = _resolved(left)
    right = _resolved(right)
    return left == right or left in right.parents or right in left.parents


def _safe_set_id(set_id):
    if not isinstance(set_id, str) or not _SAFE_ID.fullmatch(set_id):
        raise ValueError("unsafe set_id")
    return set_id


def _safe_revision(revision):
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        raise ValueError("revision must be >= 1")
    return revision


def _safe_draft_name(name, max_chars):
    if (
        not isinstance(name, str)
        or not name
        or len(name) > max_chars
        or "\x00" in name
        or not _SAFE_DRAFT.fullmatch(name)
        or name in (".", "..")
    ):
        raise ValueError("unsafe draft name")
    return name


class JTSetStorage:
    def __init__(self, official_root, user_root, draft_root, limits=None):
        self.limits = limits or JTSetIOLimits()
        self.official_root = _resolved(official_root)
        self.user_root = _resolved(user_root)
        self.draft_root = _resolved(draft_root)
        roots = (self.official_root, self.user_root, self.draft_root)
        for index, left in enumerate(roots):
            for right in roots[index + 1:]:
                if _paths_overlap(left, right):
                    raise ValueError("storage roots must be separate")
        self.user_root.mkdir(parents=True, exist_ok=True)
        self.draft_root.mkdir(parents=True, exist_ok=True)
        self._rename = os.rename

    def user_revision_path(self, set_id, revision):
        set_id = _safe_set_id(set_id)
        revision = _safe_revision(revision)
        return self.user_root / set_id / f"r{revision}"

    def draft_path(self, draft_id):
        name = _safe_draft_name(draft_id, self.limits.max_path_chars)
        return self.draft_root / name

    def copy_content_uri(self, uri, open_stream, draft_name, chunk_size=1024 * 1024):
        if not isinstance(uri, str) or not uri.startswith("content://"):
            raise ValueError("content:// URI required")
        if not callable(open_stream):
            raise TypeError("open_stream must be callable")
        if not isinstance(chunk_size, int) or isinstance(chunk_size, bool) or chunk_size < 1:
            raise ValueError("chunk_size must be >= 1")
        destination = self.draft_path(draft_name)
        if destination.exists():
            raise FileExistsError(str(destination))
        temp = destination.with_name(f".{destination.name}.tmp")
        if temp.exists():
            temp.unlink()
        written = 0
        try:
            stream = open_stream(uri)
            if stream is None:
                raise OSError("content stream unavailable")
            with closing(stream), temp.open("xb") as target:
                while True:
                    block = stream.read(chunk_size)
                    if not block:
                        break
                    if not isinstance(block, (bytes, bytearray, memoryview)):
                        raise OSError("content stream returned non-bytes")
                    written += len(block)
                    if written > self.limits.max_file_bytes:
                        raise ValueError("content copy exceeds file limit")
                    target.write(block)
                target.flush()
                os.fsync(target.fileno())
            os.replace(temp, destination)
            return destination
        except Exception:
            try:
                temp.unlink()
            except FileNotFoundError:
                pass
            raise

    def _validate_member_name(self, name):
        if not isinstance(name, str) or not name or len(name) > self.limits.max_path_chars:
            raise JTSetIOError("unsafe archive member path")
        if "\x00" in name or "\\" in name or ":" in name or name.startswith("/"):
            raise JTSetIOError("unsafe archive member path")
        raw_parts = name.split("/")
        if any(part in ("", ".", "..") for part in raw_parts):
            raise JTSetIOError("unsafe archive member path")
        path = PurePosixPath(name)
        if path.is_absolute() or ".." in path.parts:
            raise JTSetIOError("unsafe archive member path")
        if path.suffix.casefold() in _FORBIDDEN_SUFFIXES:
            raise JTSetIOError("executable archive member is forbidden")
        return name

    def _preflight_infos(self, infos):
        if len(infos) > self.limits.max_files:
            raise JTSetIOError("archive files limit exceeded")
        seen = set()
        declared_total = 0
        by_name = {}
        for info in infos:
            name = self._validate_member_name(info.filename)
            if info.is_dir() or name.endswith("/"):
                raise JTSetIOError("directory archive members are forbidden")
            folded = name.casefold()
            if folded in seen:
                raise JTSetIOError("duplicate or casefold collision in archive")
            seen.add(folded)
            if info.flag_bits & 0x1:
                raise JTSetIOError("encrypted archive member is forbidden")
            unix_mode = (info.external_attr >> 16) & 0xFFFF
            if stat.S_IFMT(unix_mode) == stat.S_IFLNK:
                raise JTSetIOError("symlink archive member is forbidden")
            if info.file_size < 0 or info.file_size > self.limits.max_file_bytes:
                raise JTSetIOError("archive member size limit exceeded")
            if name == "manifest.json" and info.file_size > self.limits.max_manifest_bytes:
                raise JTSetIOError("manifest size limit exceeded")
            declared_total += info.file_size
            if declared_total > self.limits.max_extracted_bytes:
                raise JTSetIOError("archive extracted size limit exceeded")
            by_name[name] = info
        if "manifest.json" not in by_name:
            raise JTSetIOError("missing manifest.json")
        return by_name

    def _extract_member(self, archive, info, destination, total_counter, chunk_size=1024 * 1024):
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        written = 0
        try:
            with archive.open(info, "r") as source, destination.open("xb") as target:
                while True:
                    block = source.read(chunk_size)
                    if not block:
                        break
                    written += len(block)
                    total_counter[0] += len(block)
                    if written > info.file_size or written > self.limits.max_file_bytes:
                        raise JTSetIOError("archive member real size mismatch")
                    if total_counter[0] > self.limits.max_extracted_bytes:
                        raise JTSetIOError("archive real extracted bytes limit exceeded")
                    target.write(block)
                target.flush()
                os.fsync(target.fileno())
            if written != info.file_size:
                raise JTSetIOError("archive member real size mismatch")
            return written
        except Exception:
            try:
                destination.unlink()
            except FileNotFoundError:
                pass
            raise

    def _stage_resolver(self, root):
        root = Path(root)
        def resolve(relative):
            target = root.joinpath(*PurePosixPath(relative).parts)
            try:
                target.relative_to(root)
            except ValueError:
                return None
            return str(target) if target.is_file() else None
        return resolve

    def export_set(self, selection, resolve_path, destination_zip):
        if not isinstance(selection, JTSetSelection):
            raise TypeError("selection must be JTSetSelection")
        verified = verify_selection_assets(selection, resolve_path)
        manifest = selection.manifest()
        asset_paths = [asset["path"] for asset in verified]
        folded = [path.casefold() for path in asset_paths]
        if len(set(folded)) != len(folded) or "manifest.json" in folded:
            raise JTSetIOError("asset path collision")
        for path in asset_paths:
            self._validate_member_name(path)
        if 1 + len(asset_paths) > self.limits.max_files:
            raise JTSetIOError("archive files limit exceeded")
        manifest_bytes = json.dumps(
            manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8") + b"\n"
        if len(manifest_bytes) > self.limits.max_manifest_bytes:
            raise JTSetIOError("manifest size limit exceeded")
        if len(manifest_bytes) + sum(a["size"] for a in verified) > self.limits.max_extracted_bytes:
            raise JTSetIOError("archive extracted size limit exceeded")

        destination = Path(destination_zip)
        destination.parent.mkdir(parents=True, exist_ok=True)
        temp = destination.with_name(f".{destination.name}.tmp")
        try:
            try:
                temp.unlink()
            except FileNotFoundError:
                pass
            with zipfile.ZipFile(temp, "x", compression=zipfile.ZIP_STORED, allowZip64=True) as archive:
                archive.writestr("manifest.json", manifest_bytes)
                for asset in verified:
                    physical = resolve_path(asset["path"])
                    if not physical:
                        raise JTSetIOError(f"asset unavailable: {asset['path']}")
                    archive.write(physical, arcname=asset["path"], compress_type=zipfile.ZIP_STORED)
            if temp.stat().st_size > self.limits.max_zip_bytes:
                raise JTSetIOError("ZIP size limit exceeded")
            os.replace(temp, destination)
            return destination
        except Exception:
            try:
                temp.unlink()
            except FileNotFoundError:
                pass
            raise

    def import_set_zip(self, archive_path, official_set_ids=()):
        archive_path = Path(archive_path)
        try:
            archive_size = archive_path.stat().st_size
        except OSError as exc:
            raise JTSetIOError(f"archive unavailable: {exc}") from exc
        if archive_size > self.limits.max_zip_bytes:
            raise JTSetIOError("ZIP size limit exceeded")
        official_ids = {_safe_set_id(value) for value in official_set_ids}
        stage = None
        final_parent_created = False
        final_parent = None
        try:
            with zipfile.ZipFile(archive_path, "r") as archive:
                infos = archive.infolist()
                by_name = self._preflight_infos(infos)
                stage = Path(tempfile.mkdtemp(prefix=".jtrex-stage-", dir=self.user_root))
                total = [0]
                self._extract_member(archive, by_name["manifest.json"], stage / "manifest.json", total)
                resolve = self._stage_resolver(stage)
                selection = load_set_manifest(resolve)
                if selection.set_id in official_ids:
                    raise JTSetIOError("official set_id collision")
                asset_paths = [asset["path"] for asset in selection.assets()]
                folded = [path.casefold() for path in asset_paths]
                if len(set(folded)) != len(folded) or "manifest.json" in folded:
                    raise JTSetIOError("asset path collision")
                for path in asset_paths:
                    self._validate_member_name(path)
                expected = {"manifest.json", *asset_paths}
                actual = set(by_name)
                if actual != expected:
                    missing = sorted(expected - actual)
                    extra = sorted(actual - expected)
                    raise JTSetIOError(f"archive member mismatch missing={missing} extra={extra}")
                final = self.user_revision_path(selection.set_id, selection.revision)
                if final.exists():
                    raise FileExistsError(str(final))
                for path in asset_paths:
                    self._extract_member(archive, by_name[path], stage / path, total)
                verify_selection_assets(selection, resolve)

            final_parent = final.parent
            if not final_parent.exists():
                final_parent.mkdir(parents=True, exist_ok=False)
                final_parent_created = True
            if final.exists():
                raise FileExistsError(str(final))
            self._rename(stage, final)
            stage = None
            return ImportResult(selection.set_id, selection.revision, final)
        except zipfile.BadZipFile as exc:
            raise JTSetIOError(f"invalid ZIP: {exc}") from exc
        finally:
            if stage is not None:
                shutil.rmtree(stage, ignore_errors=True)
            if final_parent_created and final_parent is not None:
                try:
                    final_parent.rmdir()
                except OSError:
                    pass

    def load_user_revision(self, set_id, revision):
        root = self.user_revision_path(set_id, revision)
        if not root.is_dir():
            raise JTSetIOError("user revision unavailable")
        resolve = self._stage_resolver(root)
        selection = load_set_manifest(resolve)
        if selection.set_id != set_id or selection.revision != revision:
            raise JTSetIOError("user revision identity mismatch")
        verify_selection_assets(selection, resolve)
        return selection
