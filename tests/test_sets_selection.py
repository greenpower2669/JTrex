import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.jtrex_sets_runtime import (
    CANONICAL_SET_ID,
    SetContractError,
    JTSetSessionManager,
    load_official_catalog,
)

ROOT = Path(__file__).resolve().parents[1]


def resolver(root):
    def resolve(relative):
        path = root / relative
        return str(path) if path.is_file() else None
    return resolve


def make_fixture_root():
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    source = ROOT / "assets/sets/trex_vs_steg/manifest.json"
    target = root / "assets/sets/trex_vs_steg/manifest.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    catalog = ROOT / "assets/sets/catalog.json"
    (root / "assets/sets").mkdir(parents=True, exist_ok=True)
    shutil.copy2(catalog, root / "assets/sets/catalog.json")
    return tmp, root


def add_second_official_set(root, set_id="raptor_vs_trike", display_name="Raptor vs Trike"):
    manifest_path = root / f"assets/sets/{set_id}/manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((root / "assets/sets/trex_vs_steg/manifest.json").read_text(encoding="utf-8"))
    manifest["set_id"] = set_id
    manifest["display_name"] = display_name
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    catalog_path = root / "assets/sets/catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    catalog["sets"].append({"set_id": set_id, "manifest": f"assets/sets/{set_id}/manifest.json"})
    catalog_path.write_text(json.dumps(catalog), encoding="utf-8")


class OfficialCatalogTests(unittest.TestCase):
    def test_catalog_loads_all_official_sets_in_declared_order(self):
        tmp, root = make_fixture_root()
        self.addCleanup(tmp.cleanup)
        add_second_official_set(root)

        catalog = load_official_catalog(resolver(root))

        self.assertEqual([entry.set_id for entry in catalog], [CANONICAL_SET_ID, "raptor_vs_trike"])
        self.assertEqual(catalog[1].display_name, "Raptor vs Trike")

    def test_catalog_rejects_duplicate_set_ids_even_if_requested_set_is_unique(self):
        tmp, root = make_fixture_root()
        self.addCleanup(tmp.cleanup)
        catalog_path = root / "assets/sets/catalog.json"
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        catalog["sets"].append(dict(catalog["sets"][0]))
        catalog_path.write_text(json.dumps(catalog), encoding="utf-8")

        with self.assertRaisesRegex(SetContractError, "duplicate official set_id"):
            load_official_catalog(resolver(root))


class SessionManagerTests(unittest.TestCase):
    def setUp(self):
        self.tmp, self.root = make_fixture_root()
        self.addCleanup(self.tmp.cleanup)
        add_second_official_set(self.root)
        self.state_path = self.root / "state/selected-set.json"
        self.resolve = resolver(self.root)

    def manager(self):
        return JTSetSessionManager(self.resolve, self.state_path)

    def test_valid_persisted_selection_is_restored_for_menu_and_startup_intro(self):
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(json.dumps({"format_version": 1, "set_id": "raptor_vs_trike"}), encoding="utf-8")

        manager = self.manager()

        self.assertEqual(manager.selected_set.set_id, "raptor_vs_trike")
        self.assertEqual(manager.startup_intro_set.set_id, "raptor_vs_trike")
        self.assertIsNone(manager.session_set)

    def test_invalid_persisted_json_falls_back_to_canonical_and_repairs_state(self):
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text("{broken", encoding="utf-8")

        manager = self.manager()

        self.assertEqual(manager.selected_set.set_id, CANONICAL_SET_ID)
        self.assertEqual(json.loads(self.state_path.read_text(encoding="utf-8")), {"format_version": 1, "set_id": CANONICAL_SET_ID})

    def test_unknown_persisted_set_id_falls_back_to_canonical(self):
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(json.dumps({"format_version": 1, "set_id": "missing"}), encoding="utf-8")

        manager = self.manager()

        self.assertEqual(manager.selected_set.set_id, CANONICAL_SET_ID)
        self.assertEqual(json.loads(self.state_path.read_text(encoding="utf-8"))["set_id"], CANONICAL_SET_ID)

    def test_select_persists_with_atomic_replace_and_no_temp_file_left(self):
        manager = self.manager()
        replace_calls = []
        real_replace = os.replace

        def recording_replace(src, dst):
            replace_calls.append((Path(src), Path(dst)))
            return real_replace(src, dst)

        manager._replace = recording_replace
        chosen = manager.select("raptor_vs_trike")

        self.assertEqual(chosen.set_id, "raptor_vs_trike")
        self.assertEqual(json.loads(self.state_path.read_text(encoding="utf-8"))["set_id"], "raptor_vs_trike")
        self.assertEqual(len(replace_calls), 1)
        self.assertEqual(replace_calls[0][1], self.state_path)
        self.assertEqual(list(self.state_path.parent.glob("*.tmp")), [])

    def test_session_freezes_selection_and_refuses_menu_change_until_end(self):
        manager = self.manager()
        manager.select("raptor_vs_trike")

        frozen = manager.begin_session()

        self.assertEqual(frozen.set_id, "raptor_vs_trike")
        self.assertEqual(manager.runtime_set.set_id, "raptor_vs_trike")
        with self.assertRaisesRegex(SetContractError, "active session"):
            manager.select(CANONICAL_SET_ID)
        self.assertEqual(manager.session_set.set_id, "raptor_vs_trike")

    def test_after_return_to_menu_new_selection_applies_to_next_session(self):
        manager = self.manager()
        manager.select("raptor_vs_trike")
        session_a = manager.begin_session()
        manager.end_session()

        manager.select(CANONICAL_SET_ID)
        session_b = manager.begin_session()

        self.assertEqual(session_a.set_id, "raptor_vs_trike")
        self.assertEqual(session_b.set_id, CANONICAL_SET_ID)
        self.assertIsNot(session_a, session_b)
        self.assertEqual(manager.runtime_set.set_id, CANONICAL_SET_ID)


if __name__ == "__main__":
    unittest.main()
