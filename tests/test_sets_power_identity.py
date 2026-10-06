import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from jtrex_sets_runtime import POWER_KEYS, load_official_set
from tests.test_sets_media_session import build_media, make_two_set_root


def load_preparer():
    spec = importlib.util.spec_from_file_location("prep_lot03", ROOT / "tools/prepare_android.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def repo_resolve(relative):
    path = ROOT / relative
    return str(path) if path.is_file() else None


def give_alt_unique_power_identity(root, alt_id):
    manifest_path = root / f"assets/sets/{alt_id}/manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for slot, key in enumerate(POWER_KEYS, 1):
        power = manifest["powers"][key]
        replacements = {
            "ready": (f"alt_{slot}_ready", f"assets/sets/{alt_id}/power{slot}-ready.png", "image"),
            "used": (f"alt_{slot}_used", f"assets/sets/{alt_id}/power{slot}-used.png", "image"),
            "activation_audio": (f"alt_{slot}_activation", f"assets/sets/{alt_id}/power{slot}-activate.wav", "audio"),
            "legacy_fallback_audio": (f"alt_{slot}_fallback", f"assets/sets/{alt_id}/power{slot}-fallback.wav", "audio"),
        }
        power["images"]["ready"] = replacements["ready"][0]
        power["images"]["used"] = replacements["used"][0]
        power["activation_audio"] = replacements["activation_audio"][0]
        power["legacy_fallback_audio"] = replacements["legacy_fallback_audio"][0]
        for asset_id, path, kind in replacements.values():
            manifest["assets"].append({
                "id": asset_id,
                "path": path,
                "type": kind,
                "size": 0,
                "sha256": format(slot, "064x"),
            })
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")


class SetPowerIdentityTests(unittest.TestCase):
    def test_selection_resolves_all_power_identity_paths(self):
        selection = load_official_set(repo_resolve)

        paths = selection.power_paths("left_1")

        self.assertEqual(paths, {
            "ready": "stsf1.png",
            "used": "stsf0.png",
            "activation_audio": "sf.wav",
            "legacy_fallback_audio": "stsf.wav",
        })

    def test_preparer_builds_manifest_driven_six_slot_power_table(self):
        prep = load_preparer()
        selection = load_official_set(repo_resolve)

        table = prep.build_power_path_table(selection)

        self.assertEqual(tuple(table), (1, 2, 3, 4, 5, 6))
        self.assertEqual(table[2]["ready"], "sth1.png")
        self.assertEqual(table[4]["activation_audio"], "fs.wav")
        self.assertEqual(table[6]["legacy_fallback_audio"], "trma.wav")

    def test_preparer_rewrites_all_power_icon_assignments_to_engine_table(self):
        prep = load_preparer()
        lines = []
        canonical = ["stsf", "sth", "stta", "trfs", "trph", "trma"]
        for slot, prefix in enumerate(canonical, 1):
            lines.append(f"\tself.b{slot}.source='{prefix}1.png'\n")
            lines.append(f"\tself.b{slot}.source='{prefix}0.png'\n")

        count = prep.rewrite_power_icon_sources(lines, 0, len(lines), "\n")
        text = "".join(lines)

        self.assertEqual(count, 12)
        for slot in range(1, 7):
            self.assertIn(f"self.b{slot}.source=JT_POWER_PATHS[{slot}]['ready']", text)
            self.assertIn(f"self.b{slot}.source=JT_POWER_PATHS[{slot}]['used']", text)
        for prefix in canonical:
            self.assertNotIn(f"'{prefix}1.png'", text)
            self.assertNotIn(f"'{prefix}0.png'", text)

    def test_media_applies_frozen_session_power_table_once_session_begins(self):
        tmp, root, alt_id = make_two_set_root()
        self.addCleanup(tmp.cleanup)
        give_alt_unique_power_identity(root, alt_id)
        media, _ = build_media(root)
        media._intro_done = True
        applied = []
        media._engine = {"jt_apply_power_paths": lambda table: applied.append(table)}
        media.on_phase_changed("MENU")
        media.select_official_set(alt_id)

        media.on_phase_changed("ROUND_INTRO")

        self.assertEqual(len(applied), 1)
        table = applied[0]
        self.assertTrue(table[1]["ready"].endswith("power1-ready.png"))
        self.assertTrue(table[3]["activation_audio"].endswith("power3-activate.wav"))
        self.assertTrue(table[6]["legacy_fallback_audio"].endswith("power6-fallback.wav"))
        self.assertEqual(media.sets.session_set.set_id, alt_id)

    def test_preparer_injects_runtime_power_path_api_not_canonical_tick_literals(self):
        source = (ROOT / "tools/prepare_android.py").read_text(encoding="utf-8")
        self.assertIn("JT_POWER_PATHS", source)
        self.assertIn("def jt_apply_power_paths", source)
        self.assertNotIn("Correct the right-side visual identity: slot 4=TRFS, slot 6=TRMA", source)


if __name__ == "__main__":
    unittest.main()
