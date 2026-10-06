"""Pure DATA/MEDIA workshop services for June T-Rex user sets.

This module owns resumable drafts only. It deliberately has no Kivy, Android,
combat-engine, phase, timing, KO, score, or power-effect dependency.
"""
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile

if __package__:
    from .jtrex_sets_runtime import POWER_KEYS, JTSetSelection, load_set_manifest, verify_selection_assets
    from .jtrex_sets_io import JTSetStorage, _safe_revision, _safe_set_id
else:
    from jtrex_sets_runtime import POWER_KEYS, JTSetSelection, load_set_manifest, verify_selection_assets
    from jtrex_sets_io import JTSetStorage, _safe_revision, _safe_set_id


@dataclass(frozen=True)
class JTAdminRole:
    role_id: str
    label: str
    asset_type: str
    required: bool


@dataclass(frozen=True)
class JTDraftState:
    draft_id: str
    set_id: str
    revision: int
    role_index: int
    source_kind: str


_EXTENSIONS = {
    "video": frozenset((".mp4",)),
    "image": frozenset((".png", ".jpg", ".jpeg", ".gif")),
    "audio": frozenset((".wav",)),
}
_ROLE_SLUG = re.compile(r"[^A-Za-z0-9._-]+")
_STATE_VERSION = 1


def _nonempty(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def _atomic_json(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    try:
        with temp.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, separators=(",", ":"))
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        try:
            temp.unlink()
        except FileNotFoundError:
            pass


def _resolver(root):
    root = Path(root).resolve(strict=False)

    def resolve(relative):
        path = root.joinpath(*PurePosixPath(relative).parts).resolve(strict=False)
        try:
            path.relative_to(root)
        except ValueError:
            return None
        return str(path) if path.is_file() else None

    return resolve


def _role_slug(role_id):
    slug = _ROLE_SLUG.sub("-", role_id).strip(".-")
    if not slug:
        raise ValueError("invalid role id")
    return slug


def _manifest_refs(manifest):
    refs = []
    optional = (
        manifest["catalog"]["thumbnail"],
        manifest["dinosaurs"]["left"]["portrait"],
        manifest["dinosaurs"]["right"]["portrait"],
    )
    refs.extend(value for value in optional if value is not None)
    refs.extend(manifest["media"]["intros"])
    refs.extend(value for key, value in manifest["media"].items() if key != "intros")
    for key in POWER_KEYS:
        power = manifest["powers"][key]
        refs.extend((power["media"], power["images"]["ready"], power["images"]["used"]))
        if power["activation_audio"] is not None:
            refs.append(power["activation_audio"])
        if power["legacy_fallback_audio"] is not None:
            refs.append(power["legacy_fallback_audio"])
    return refs


def _role_value(manifest, role_id):
    parts = role_id.split(".")
    if parts[:2] == ["catalog", "thumbnail"] and len(parts) == 2:
        return manifest["catalog"]["thumbnail"]
    if len(parts) == 3 and parts[0] == "dinosaurs" and parts[2] == "portrait":
        return manifest["dinosaurs"][parts[1]]["portrait"]
    if parts[:2] == ["media", "intros"] and len(parts) == 3:
        return manifest["media"]["intros"][int(parts[2])]
    if parts[0] == "media" and len(parts) == 2:
        return manifest["media"][parts[1]]
    if parts[0] == "powers" and len(parts) >= 3:
        power = manifest["powers"][parts[1]]
        if parts[2] in ("media", "activation_audio", "legacy_fallback_audio") and len(parts) == 3:
            return power[parts[2]]
        if parts[2] == "images" and len(parts) == 4:
            return power["images"][parts[3]]
    raise ValueError(f"unknown admin role: {role_id}")


def _set_role_value(manifest, role_id, value):
    parts = role_id.split(".")
    if parts[:2] == ["catalog", "thumbnail"] and len(parts) == 2:
        manifest["catalog"]["thumbnail"] = value
        return
    if len(parts) == 3 and parts[0] == "dinosaurs" and parts[2] == "portrait":
        manifest["dinosaurs"][parts[1]]["portrait"] = value
        return
    if parts[:2] == ["media", "intros"] and len(parts) == 3:
        manifest["media"]["intros"][int(parts[2])] = value
        return
    if parts[0] == "media" and len(parts) == 2:
        manifest["media"][parts[1]] = value
        return
    if parts[0] == "powers" and len(parts) >= 3:
        power = manifest["powers"][parts[1]]
        if parts[2] in ("media", "activation_audio", "legacy_fallback_audio") and len(parts) == 3:
            power[parts[2]] = value
            return
        if parts[2] == "images" and len(parts) == 4:
            power["images"][parts[3]] = value
            return
    raise ValueError(f"unknown admin role: {role_id}")


class JTSetAdminService:
    def __init__(self, storage, official_set_ids):
        if not isinstance(storage, JTSetStorage):
            raise TypeError("storage must be JTSetStorage")
        self.storage = storage
        self.official_set_ids = frozenset(_safe_set_id(value) for value in official_set_ids)

    def _root(self, draft_id):
        return self.storage.draft_path(draft_id)

    def _state_path(self, draft_id):
        return self._root(draft_id) / "draft-state.json"

    def _manifest_path(self, draft_id):
        return self._root(draft_id) / "manifest.json"

    def _load_manifest(self, draft_id):
        try:
            return json.loads(self._manifest_path(draft_id).read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"draft manifest unavailable: {exc}") from exc

    def _write_manifest(self, draft_id, manifest):
        root = self._root(draft_id)
        # Validate the whole closed v1 document before replacing the draft manifest.
        temp_manifest = root / ".manifest-validate.json"
        _atomic_json(temp_manifest, manifest)
        try:
            load_set_manifest(_resolver(root), temp_manifest.name)
        finally:
            try:
                temp_manifest.unlink()
            except FileNotFoundError:
                pass
        _atomic_json(self._manifest_path(draft_id), manifest)

    def _write_state(self, state):
        _atomic_json(self._state_path(state.draft_id), {
            "format_version": _STATE_VERSION,
            "draft_id": state.draft_id,
            "set_id": state.set_id,
            "revision": state.revision,
            "role_index": state.role_index,
            "source_kind": state.source_kind,
        })

    def open_draft(self, draft_id):
        path = self._state_path(draft_id)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"draft state unavailable: {exc}") from exc
        if not isinstance(payload, dict) or set(payload) != {
            "format_version", "draft_id", "set_id", "revision", "role_index", "source_kind"
        }:
            raise ValueError("invalid draft state")
        if payload["format_version"] != _STATE_VERSION or payload["draft_id"] != draft_id:
            raise ValueError("invalid draft state")
        _safe_set_id(payload["set_id"])
        _safe_revision(payload["revision"])
        if payload["source_kind"] not in ("official", "user", "imported"):
            raise ValueError("invalid draft source_kind")
        roles = self.roles(draft_id, _state_check=False)
        role_index = payload["role_index"]
        if not isinstance(role_index, int) or isinstance(role_index, bool) or not 0 <= role_index < len(roles):
            raise ValueError("invalid draft role_index")
        manifest = self._load_manifest(draft_id)
        if manifest.get("set_id") != payload["set_id"] or manifest.get("revision") != payload["revision"]:
            raise ValueError("draft state/manifest identity mismatch")
        return JTDraftState(draft_id, payload["set_id"], payload["revision"], role_index, payload["source_kind"])

    def _next_revision(self, set_id):
        existing = [revision for sid, revision in self.storage.list_user_revisions() if sid == set_id]
        return (max(existing) + 1) if existing else 1

    def list_drafts(self):
        drafts = []
        if not self.storage.draft_root.is_dir():
            return ()
        for child in self.storage.draft_root.iterdir():
            if not child.is_dir():
                continue
            try:
                drafts.append(self.open_draft(child.name))
            except (OSError, ValueError):
                continue
        return tuple(sorted(drafts, key=lambda state: state.draft_id))

    def create_from_selection(self, selection, *, draft_id, set_id, revision=None, source_kind="official"):
        if not isinstance(selection, JTSetSelection):
            raise TypeError("selection must be JTSetSelection")
        set_id = _safe_set_id(set_id)
        if set_id in self.official_set_ids:
            raise ValueError("official set_id cannot be used for a user draft")
        if source_kind not in ("official", "user", "imported"):
            raise ValueError("invalid source_kind")
        revision = self._next_revision(set_id) if revision is None else _safe_revision(revision)
        root = self._root(draft_id)
        if root.exists():
            raise FileExistsError(str(root))
        verify_selection_assets(selection, selection.resolve_path)
        manifest = selection.manifest()
        manifest["set_id"] = set_id
        manifest["revision"] = revision
        root.mkdir(parents=True, exist_ok=False)
        try:
            for asset in manifest["assets"]:
                source = selection.resolve_path(asset["path"])
                if not source:
                    raise ValueError(f"source asset unavailable: {asset['path']}")
                destination = root.joinpath(*PurePosixPath(asset["path"]).parts)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, destination)
            _atomic_json(root / "manifest.json", manifest)
            # The changed identity must still satisfy the closed manifest and all copied hashes.
            draft_selection = load_set_manifest(_resolver(root))
            verify_selection_assets(draft_selection, draft_selection.resolve_path)
            state = JTDraftState(draft_id, set_id, revision, 0, source_kind)
            self._write_state(state)
            return state
        except Exception:
            shutil.rmtree(root, ignore_errors=True)
            raise

    def roles(self, draft_id, _state_check=True):
        manifest = self._load_manifest(draft_id)
        result = [
            JTAdminRole("catalog.thumbnail", "Vignette du set", "image", False),
            JTAdminRole("dinosaurs.left.portrait", "Portrait dinosaure gauche", "image", False),
            JTAdminRole("dinosaurs.right.portrait", "Portrait dinosaure droit", "image", False),
        ]
        for index, _asset_id in enumerate(manifest["media"]["intros"]):
            result.append(JTAdminRole(f"media.intros.{index}", f"Intro {index + 1}", "video", True))
        media_labels = (
            ("orbs_background", "Fond des orbes"),
            ("charge_red_blue", "Charge rouge / bleue"),
            ("charge_yellow", "Charge jaune"),
            ("verdict_draw", "Verdict égalité"),
            ("verdict_left", "Verdict gauche"),
            ("verdict_right", "Verdict droit"),
            ("finishing_left", "Finishing gauche"),
            ("finishing_right", "Finishing droit"),
        )
        result.extend(JTAdminRole(f"media.{key}", label, "video", True) for key, label in media_labels)
        for power_key in POWER_KEYS:
            prefix = f"Pouvoir {power_key}"
            result.extend((
                JTAdminRole(f"powers.{power_key}.media", prefix + " — vidéo", "video", True),
                JTAdminRole(f"powers.{power_key}.images.ready", prefix + " — image disponible", "image", True),
                JTAdminRole(f"powers.{power_key}.images.used", prefix + " — image utilisée", "image", True),
                JTAdminRole(f"powers.{power_key}.activation_audio", prefix + " — son activation", "audio", False),
                JTAdminRole(f"powers.{power_key}.legacy_fallback_audio", prefix + " — son fallback", "audio", False),
            ))
        return tuple(result)

    def current_role(self, draft_id):
        state = self.open_draft(draft_id)
        return self.roles(draft_id)[state.role_index]

    def role_asset_path(self, draft_id, role_id=None):
        role = self.current_role(draft_id) if role_id is None else self._role(draft_id, role_id)
        asset_id = _role_value(self._load_manifest(draft_id), role.role_id)
        if asset_id is None:
            return None
        selection = load_set_manifest(_resolver(self._root(draft_id)))
        return selection.resolve_asset(asset_id)

    def candidate_path(self, draft_id, role_id=None):
        role = self.current_role(draft_id) if role_id is None else self._role(draft_id, role_id)
        try:
            candidate = self._candidate(draft_id, role.role_id)
        except ValueError:
            return None
        return str(candidate) if candidate.is_file() else None

    def _move_role(self, draft_id, delta):
        state = self.open_draft(draft_id)
        roles = self.roles(draft_id)
        index = min(max(state.role_index + delta, 0), len(roles) - 1)
        updated = JTDraftState(state.draft_id, state.set_id, state.revision, index, state.source_kind)
        self._write_state(updated)
        return roles[index]

    def previous_role(self, draft_id):
        return self._move_role(draft_id, -1)

    def keep_and_next(self, draft_id):
        return self._move_role(draft_id, 1)

    def _role(self, draft_id, role_id):
        matches = [role for role in self.roles(draft_id) if role.role_id == role_id]
        if len(matches) != 1:
            raise ValueError(f"unknown admin role: {role_id}")
        return matches[0]

    def stage_candidate(self, draft_id, role_id, local_path):
        role = self._role(draft_id, role_id)
        source = Path(local_path)
        if not source.is_file():
            raise ValueError("candidate unavailable")
        suffix = source.suffix.casefold()
        if suffix not in _EXTENSIONS[role.asset_type]:
            raise ValueError(f"candidate type must be {role.asset_type}")
        size = source.stat().st_size
        if size > self.storage.limits.max_file_bytes:
            raise ValueError("candidate file limit exceeded")
        candidate_dir = self._root(draft_id) / ".candidates"
        candidate_dir.mkdir(parents=True, exist_ok=True)
        slug = _role_slug(role_id)
        for old in candidate_dir.glob(slug + ".*"):
            old.unlink()
        destination = candidate_dir / (slug + suffix)
        shutil.copyfile(source, destination)
        if destination.stat().st_size != size:
            destination.unlink(missing_ok=True)
            raise ValueError("candidate copy size mismatch")
        return destination

    def _candidate(self, draft_id, role_id):
        slug = _role_slug(role_id)
        candidates = tuple((self._root(draft_id) / ".candidates").glob(slug + ".*"))
        if len(candidates) != 1 or not candidates[0].is_file():
            raise ValueError("candidate not staged")
        return candidates[0]

    def accept_candidate(self, draft_id, role_id):
        role = self._role(draft_id, role_id)
        candidate = self._candidate(draft_id, role_id)
        data_hash = hashlib.sha256()
        size = 0
        with candidate.open("rb") as source:
            for block in iter(lambda: source.read(1024 * 1024), b""):
                size += len(block)
                if size > self.storage.limits.max_file_bytes:
                    raise ValueError("candidate file limit exceeded")
                data_hash.update(block)
        digest = data_hash.hexdigest()
        manifest = self._load_manifest(draft_id)
        old_asset_id = _role_value(manifest, role_id)
        slug = _role_slug(role_id)
        asset_id = f"admin_{slug}_{digest[:12]}"
        relative = f"assets/admin/{slug}-{digest[:12]}{candidate.suffix.casefold()}"
        root = self._root(draft_id)
        target = root.joinpath(*PurePosixPath(relative).parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            target.unlink()
        shutil.copyfile(candidate, target)
        new_asset = {"id": asset_id, "path": relative, "type": role.asset_type, "size": size, "sha256": digest}
        manifest["assets"] = [entry for entry in manifest["assets"] if entry["id"] != asset_id]
        manifest["assets"].append(new_asset)
        _set_role_value(manifest, role_id, asset_id)

        referenced = set(_manifest_refs(manifest))
        removed = [entry for entry in manifest["assets"] if entry["id"] not in referenced]
        manifest["assets"] = [entry for entry in manifest["assets"] if entry["id"] in referenced]
        self._write_manifest(draft_id, manifest)
        # Only after the manifest is committed may old unreferenced files disappear.
        remaining_paths = {entry["path"] for entry in manifest["assets"]}
        for entry in removed:
            if entry["path"] not in remaining_paths:
                try:
                    (root / entry["path"]).unlink()
                except FileNotFoundError:
                    pass
        try:
            candidate.unlink()
        except FileNotFoundError:
            pass
        return self.validate_complete(draft_id)

    def set_identity(self, draft_id, *, set_id=None, revision=None, display_name=None,
                     left_name=None, right_name=None, power_labels=None):
        state = self.open_draft(draft_id)
        manifest = self._load_manifest(draft_id)
        new_set_id = state.set_id if set_id is None else _safe_set_id(set_id)
        if new_set_id in self.official_set_ids:
            raise ValueError("official set_id cannot be used for a user draft")
        new_revision = state.revision if revision is None else _safe_revision(revision)
        manifest["set_id"] = new_set_id
        manifest["revision"] = new_revision
        if display_name is not None:
            manifest["display_name"] = _nonempty(display_name, "display_name")
        if left_name is not None:
            manifest["dinosaurs"]["left"]["display_name"] = _nonempty(left_name, "left_name")
        if right_name is not None:
            manifest["dinosaurs"]["right"]["display_name"] = _nonempty(right_name, "right_name")
        if power_labels is not None:
            if not isinstance(power_labels, dict) or not set(power_labels).issubset(POWER_KEYS):
                raise ValueError("invalid power_labels")
            for power_key, label in power_labels.items():
                manifest["powers"][power_key]["label"] = _nonempty(label, f"power_labels.{power_key}")
        self._write_manifest(draft_id, manifest)
        updated = JTDraftState(state.draft_id, new_set_id, new_revision, state.role_index, state.source_kind)
        self._write_state(updated)
        return updated

    def validate_complete(self, draft_id):
        self.open_draft(draft_id)
        selection = load_set_manifest(_resolver(self._root(draft_id)))
        verify_selection_assets(selection, selection.resolve_path)
        return selection

    def export_revision(self, draft_id, destination_zip):
        selection = self.validate_complete(draft_id)
        return self.storage.export_set(selection, selection.resolve_path, destination_zip)

    def install_revision(self, draft_id):
        selection = self.validate_complete(draft_id)
        fd, name = tempfile.mkstemp(prefix=".jtrex-admin-", suffix=".zip", dir=self.storage.draft_root)
        os.close(fd)
        archive = Path(name)
        try:
            archive.unlink()
            self.storage.export_set(selection, selection.resolve_path, archive)
            return self.storage.import_set_zip(archive, official_set_ids=self.official_set_ids)
        finally:
            try:
                archive.unlink()
            except FileNotFoundError:
                pass
