import json
import unittest
from pathlib import Path

from tests.runtime_harness import Video
from tests.test_sets_media_session import build_media, make_two_set_root
from tests.test_sets_power_identity import give_alt_unique_power_identity


def add_second_synthetic_set(root, source_id, second_id):
    source_path = root / f"assets/sets/{source_id}/manifest.json"
    source = source_path.read_text(encoding="utf-8")
    second = json.loads(source.replace(source_id, second_id))
    second["set_id"] = second_id
    second["display_name"] = "Ankyl vs Spino"
    second["dinosaurs"]["left"]["display_name"] = "Ankyl"
    second["dinosaurs"]["right"]["display_name"] = "Spino"
    second_dir = root / f"assets/sets/{second_id}"
    second_dir.mkdir(parents=True)
    (second_dir / "manifest.json").write_text(json.dumps(second), encoding="utf-8")
    (second_dir / "intro.mp4").touch()
    (second_dir / "orbs.mp4").touch()

    catalog_path = root / "assets/sets/catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    catalog["sets"].append({
        "set_id": second_id,
        "manifest": f"assets/sets/{second_id}/manifest.json",
    })
    catalog_path.write_text(json.dumps(catalog), encoding="utf-8")


class SetSessionIsolationTests(unittest.TestCase):
    def setUp(self):
        self.tmp, self.root, self.first_id = make_two_set_root()
        self.addCleanup(self.tmp.cleanup)
        give_alt_unique_power_identity(self.root, self.first_id)
        self.second_id = "ankyl_vs_spino"
        add_second_synthetic_set(self.root, self.first_id, self.second_id)

    def test_two_successive_synthetic_sessions_use_only_their_frozen_identity(self):
        media, _ = build_media(self.root)
        media._intro_done = True
        applied = []
        media._engine = {"jt_apply_power_paths": lambda table: applied.append(table)}

        media.on_phase_changed("MENU")
        media.select_official_set(self.first_id)
        media.on_phase_changed("ROUND_INTRO")
        first_orbs = media._scene_config("wait")["file"]
        first_power = applied[-1][1]["ready"]

        media.on_phase_changed("MENU")
        media.select_official_set(self.second_id)
        media.on_phase_changed("ROUND_INTRO")
        second_orbs = media._scene_config("wait")["file"]
        second_power = applied[-1][1]["ready"]

        self.assertIn(self.first_id, first_orbs)
        self.assertIn(self.first_id, first_power)
        self.assertIn(self.second_id, second_orbs)
        self.assertIn(self.second_id, second_power)
        self.assertEqual(media.sets.session_set.set_id, self.second_id)
        self.assertEqual(len(applied), 2)

    def test_stale_frame_and_eos_from_session_a_cannot_mutate_session_b(self):
        media, _ = build_media(self.root)
        media._intro_done = True
        media.on_phase_changed("MENU")
        media.select_official_set(self.first_id)
        media.on_phase_changed("ROUND_INTRO")

        old_player = Video(filename="session-a.mp4", eos="stop", autoplay=False)
        old_generation = 11
        media._scene_player = old_player
        media._scene_key = "power-stsf"
        media._scene_state = 21
        media._scene_generation = old_generation

        media.on_phase_changed("MENU")
        media.select_official_set(self.second_id)
        media.on_phase_changed("ROUND_INTRO")

        new_player = Video(filename="session-b.mp4", eos="stop", autoplay=False)
        media._scene_player = new_player
        media._scene_key = "power-trph"
        media._scene_state = 25
        current_generation = media._scene_generation
        media._scene_eos_reached = False
        media._scene_completed_key = None

        media._on_scene_frame(old_player, old_generation)
        media._on_scene_eos(old_player, old_generation)

        self.assertIs(media._scene_player, new_player)
        self.assertEqual(media._scene_generation, current_generation)
        self.assertFalse(media._scene_eos_reached)
        self.assertIsNone(media._scene_completed_key)
        self.assertEqual(media.sets.session_set.set_id, self.second_id)


if __name__ == "__main__":
    unittest.main()
