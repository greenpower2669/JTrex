"""Closed DATA-only set contract for June T-Rex.

This module resolves official set metadata only. Gameplay states, timings, EOS
policies and power formulas remain owned by the engine/runtime modules.
"""
from copy import deepcopy
import json
import re
from pathlib import Path, PurePosixPath

CATALOG_PATH = "assets/sets/catalog.json"
FORMAT_VERSION = 1
ENGINE_CONTRACT = "jtrex-combat-v1"
MEDIA_KEYS = frozenset((
    "intros", "orbs_background", "charge_red_blue", "charge_yellow",
    "verdict_draw", "verdict_left", "verdict_right",
    "finishing_left", "finishing_right",
))
POWER_KEYS = ("left_1", "left_2", "left_3", "right_1", "right_2", "right_3")
MECHANISMS = {
    "left_1": "left_slot_1_target_damage",
    "left_2": "left_slot_2_self_heal",
    "left_3": "left_slot_3_target_damage",
    "right_1": "right_slot_1_target_damage",
    "right_2": "right_slot_2_target_damage",
    "right_3": "right_slot_3_target_damage",
}
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_SIMPLE_ID = re.compile(r"^[a-z0-9][a-z0-9._-]*$")


class SetContractError(ValueError):
    pass


def _fail(message):
    raise SetContractError(message)


def _expect_keys(obj, allowed, context):
    if not isinstance(obj, dict):
        _fail(f"{context}: object expected")
    actual = set(obj)
    if actual != set(allowed):
        _fail(f"{context}: fields {sorted(actual)} != {sorted(allowed)}")


def _nonempty_string(value, context):
    if not isinstance(value, str) or not value:
        _fail(f"{context}: non-empty string expected")
    return value


def _safe_path(value, context):
    value = _nonempty_string(value, context)
    if "\\" in value or "://" in value or value.startswith("/"):
        _fail(f"{context}: unsafe path")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        _fail(f"{context}: unsafe path")
    return value


def _read_json(resolve_path, relative, context):
    physical = resolve_path(relative)
    if not physical:
        _fail(f"{context}: unavailable {relative}")
    try:
        return json.loads(Path(physical).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        _fail(f"{context}: invalid JSON {relative}: {exc}")


class JTSetSelection:
    def __init__(self, manifest, manifest_path):
        self._manifest = deepcopy(manifest)
        self._assets = {entry["id"]: deepcopy(entry) for entry in manifest["assets"]}
        self.manifest_path = manifest_path
        self.set_id = manifest["set_id"]
        self.format_version = manifest["format_version"]
        self.engine_contract = manifest["engine_contract"]
        self.revision = manifest["revision"]
        self.display_name = manifest["display_name"]

    def dinosaurs(self):
        return deepcopy(self._manifest["dinosaurs"])

    def asset_path(self, asset_id):
        try:
            return self._assets[asset_id]["path"]
        except KeyError:
            _fail(f"unknown asset id: {asset_id}")

    def media_path(self, role):
        if role == "intros":
            _fail("intros is a collection; use intro_paths()")
        if role not in MEDIA_KEYS:
            _fail(f"unknown media role: {role}")
        return self.asset_path(self._manifest["media"][role])

    def intro_paths(self):
        return tuple(self.asset_path(asset_id) for asset_id in self._manifest["media"]["intros"])

    def power(self, power_key):
        if power_key not in POWER_KEYS:
            _fail(f"unknown power key: {power_key}")
        return deepcopy(self._manifest["powers"][power_key])

    def power_media_path(self, power_key):
        return self.asset_path(self.power(power_key)["media"])

    def assets(self):
        return tuple(deepcopy(entry) for entry in self._manifest["assets"])


def _validate_manifest(manifest):
    _expect_keys(manifest, (
        "format_version", "set_id", "revision", "display_name", "engine_contract",
        "catalog", "dinosaurs", "media", "powers", "assets",
    ), "manifest")
    if manifest["format_version"] != FORMAT_VERSION:
        _fail("unsupported format_version")
    if manifest["engine_contract"] != ENGINE_CONTRACT:
        _fail("unsupported engine_contract")
    set_id = _nonempty_string(manifest["set_id"], "set_id")
    if not _SIMPLE_ID.fullmatch(set_id):
        _fail("invalid set_id")
    if not isinstance(manifest["revision"], int) or manifest["revision"] < 1:
        _fail("revision must be >= 1")
    _nonempty_string(manifest["display_name"], "display_name")

    _expect_keys(manifest["catalog"], ("thumbnail",), "catalog")
    _expect_keys(manifest["dinosaurs"], ("left", "right"), "dinosaurs")
    for side in ("left", "right"):
        entry = manifest["dinosaurs"][side]
        _expect_keys(entry, ("id", "display_name", "portrait"), f"dinosaurs.{side}")
        _nonempty_string(entry["id"], f"dinosaurs.{side}.id")
        _nonempty_string(entry["display_name"], f"dinosaurs.{side}.display_name")

    _expect_keys(manifest["media"], MEDIA_KEYS, "media")
    intros = manifest["media"]["intros"]
    if not isinstance(intros, list) or not intros:
        _fail("media.intros must be a non-empty list")
    for role in MEDIA_KEYS - {"intros"}:
        _nonempty_string(manifest["media"][role], f"media.{role}")

    _expect_keys(manifest["powers"], POWER_KEYS, "powers")
    for key in POWER_KEYS:
        entry = manifest["powers"][key]
        _expect_keys(entry, (
            "label", "media", "images", "activation_audio",
            "legacy_fallback_audio", "mechanism", "parameters",
        ), f"powers.{key}")
        _nonempty_string(entry["label"], f"powers.{key}.label")
        _nonempty_string(entry["media"], f"powers.{key}.media")
        _expect_keys(entry["images"], ("ready", "used"), f"powers.{key}.images")
        _nonempty_string(entry["images"]["ready"], f"powers.{key}.images.ready")
        _nonempty_string(entry["images"]["used"], f"powers.{key}.images.used")
        if entry["activation_audio"] is not None:
            _nonempty_string(entry["activation_audio"], f"powers.{key}.activation_audio")
        if entry["legacy_fallback_audio"] is not None:
            _nonempty_string(entry["legacy_fallback_audio"], f"powers.{key}.legacy_fallback_audio")
        if entry["mechanism"] != MECHANISMS[key]:
            _fail(f"powers.{key}: mechanism is engine-owned for v1")
        if entry["parameters"] != {}:
            _fail(f"powers.{key}: parameters are closed in v1")

    assets = manifest["assets"]
    if not isinstance(assets, list) or not assets:
        _fail("assets must be a non-empty list")
    asset_ids = set()
    for index, asset in enumerate(assets):
        _expect_keys(asset, ("id", "path", "type", "size", "sha256"), f"assets[{index}]")
        asset_id = _nonempty_string(asset["id"], f"assets[{index}].id")
        if asset_id in asset_ids:
            _fail(f"duplicate asset id: {asset_id}")
        asset_ids.add(asset_id)
        _safe_path(asset["path"], f"assets[{index}].path")
        if asset["type"] not in ("video", "image", "audio"):
            _fail(f"assets[{index}].type invalid")
        if not isinstance(asset["size"], int) or asset["size"] < 0:
            _fail(f"assets[{index}].size invalid")
        if not isinstance(asset["sha256"], str) or not _HEX64.fullmatch(asset["sha256"]):
            _fail(f"assets[{index}].sha256 invalid")

    refs = []
    thumb = manifest["catalog"]["thumbnail"]
    if thumb is not None:
        refs.append(thumb)
    for side in ("left", "right"):
        portrait = manifest["dinosaurs"][side]["portrait"]
        if portrait is not None:
            refs.append(portrait)
    refs.extend(intros)
    refs.extend(manifest["media"][role] for role in MEDIA_KEYS - {"intros"})
    for key in POWER_KEYS:
        power = manifest["powers"][key]
        refs.extend((power["media"], power["images"]["ready"], power["images"]["used"]))
        if power["activation_audio"] is not None:
            refs.append(power["activation_audio"])
        if power["legacy_fallback_audio"] is not None:
            refs.append(power["legacy_fallback_audio"])
    missing = sorted(set(refs) - asset_ids)
    if missing:
        _fail(f"referenced asset ids missing: {missing}")


def load_official_set(resolve_path, set_id="trex_vs_steg"):
    catalog = _read_json(resolve_path, CATALOG_PATH, "catalog")
    _expect_keys(catalog, ("format_version", "sets"), "catalog")
    if catalog["format_version"] != FORMAT_VERSION or not isinstance(catalog["sets"], list):
        _fail("invalid catalog format")
    matches = []
    for index, entry in enumerate(catalog["sets"]):
        _expect_keys(entry, ("set_id", "manifest"), f"catalog.sets[{index}]")
        _nonempty_string(entry["set_id"], f"catalog.sets[{index}].set_id")
        _safe_path(entry["manifest"], f"catalog.sets[{index}].manifest")
        if entry["set_id"] == set_id:
            matches.append(entry)
    if len(matches) != 1:
        _fail(f"official set not found uniquely: {set_id}")
    manifest_path = matches[0]["manifest"]
    manifest = _read_json(resolve_path, manifest_path, "manifest")
    _validate_manifest(manifest)
    if manifest["set_id"] != set_id:
        _fail("catalog/manifest set_id mismatch")
    return JTSetSelection(manifest, manifest_path)
