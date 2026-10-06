import ast
import json
import tempfile
import unittest
from pathlib import Path
from types import ModuleType, SimpleNamespace

from tests.runtime_harness import Canvas, Clock, Event, Label, Rectangle, Video, Widget
from jtrex_sets_runtime import CANONICAL_SET_ID, SetContractError

ROOT = Path(__file__).resolve().parents[1]


class PopupStub(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opened = False
        self.content = kwargs.get("content")
        self.title = kwargs.get("title", "")

    def open(self):
        self.opened = True

    def dismiss(self):
        self.opened = False


class ButtonStub(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disabled = kwargs.get("disabled", False)
        self.font_size = kwargs.get("font_size", 0)


class Root(Widget):
    def __init__(self):
        super().__init__()
        self.deux = Rectangle()


def execute_without_kivy(source, ns):
    tree = ast.parse(source)
    tree.body = [n for n in tree.body if not (
        isinstance(n, ast.ImportFrom) and n.module.startswith("kivy")
        or isinstance(n, ast.Import) and any(a.name == "kivy" for a in n.names)
    )]
    exec(compile(tree, "<jtrex-media-lot03>", "exec"), ns)


def make_two_set_root():
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    sets = root / "assets/sets"
    canon_dir = sets / CANONICAL_SET_ID
    canon_dir.mkdir(parents=True)
    canonical = json.loads((ROOT / "assets/sets/trex_vs_steg/manifest.json").read_text(encoding="utf-8"))
    (canon_dir / "manifest.json").write_text(json.dumps(canonical), encoding="utf-8")

    alt_id = "raptor_vs_trike"
    alt = json.loads(json.dumps(canonical))
    alt["set_id"] = alt_id
    alt["display_name"] = "Raptor vs Trike"
    alt["dinosaurs"]["left"]["display_name"] = "Raptor"
    alt["dinosaurs"]["right"]["display_name"] = "Trike"
    alt["media"]["intros"] = ["alt_intro"]
    alt["media"]["orbs_background"] = "alt_orbs"
    alt["assets"].extend([
        {"id": "alt_intro", "path": "assets/sets/raptor_vs_trike/intro.mp4", "type": "video", "size": 0, "sha256": "0" * 64},
        {"id": "alt_orbs", "path": "assets/sets/raptor_vs_trike/orbs.mp4", "type": "video", "size": 0, "sha256": "1" * 64},
    ])
    alt_dir = sets / alt_id
    alt_dir.mkdir(parents=True)
    (alt_dir / "manifest.json").write_text(json.dumps(alt), encoding="utf-8")
    (alt_dir / "intro.mp4").touch()
    (alt_dir / "orbs.mp4").touch()

    catalog = {
        "format_version": 1,
        "sets": [
            {"set_id": CANONICAL_SET_ID, "manifest": "assets/sets/trex_vs_steg/manifest.json"},
            {"set_id": alt_id, "manifest": "assets/sets/raptor_vs_trike/manifest.json"},
        ],
    }
    sets.mkdir(parents=True, exist_ok=True)
    (sets / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
    return tmp, root, alt_id


def load_media_runtime(asset_root):
    Clock.now, Clock.events, Video.instances = 100.0, [], []
    window = Widget()
    ns = {
        "__name__": "jtrex_media_runtime_lot03",
        "Widget": Widget,
        "Label": Label,
        "Rectangle": Rectangle,
        "Color": Widget,
        "Ellipse": Widget,
        "BoxLayout": Widget,
        "Button": ButtonStub,
        "Popup": PopupStub,
        "ScrollView": Widget,
        "Clock": Clock,
        "CoreVideo": Video,
        "Window": window,
        "dp": lambda value: value,
        "resource_find": lambda relative: str(asset_root / relative) if (asset_root / relative).is_file() else None,
    }
    runtime = ModuleType("jtrex_media_runtime_lot03")
    runtime.__dict__.update(ns)
    execute_without_kivy((ROOT / "tools/jtrex_media_runtime.py").read_text(encoding="utf-8"), runtime.__dict__)
    return runtime


def build_media(asset_root):
    runtime = load_media_runtime(asset_root)
    root = Root()
    app = SimpleNamespace(root=root, user_data_dir=str(asset_root / "userdata"))
    return runtime.JTMediaController(app), runtime


class MediaSetSessionTests(unittest.TestCase):
    def setUp(self):
        self.tmp, self.root, self.alt_id = make_two_set_root()
        self.addCleanup(self.tmp.cleanup)
        self.state_path = self.root / "userdata/jt-set-selection.json"

    def persist(self, set_id):
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(json.dumps({"format_version": 1, "set_id": set_id}), encoding="utf-8")

    def test_startup_intro_uses_last_valid_persisted_set(self):
        self.persist(self.alt_id)
        media, _ = build_media(self.root)

        media.start_intro(lambda: None)

        self.assertTrue(Video.instances)
        self.assertTrue(Video.instances[-1].filename.endswith("assets/sets/raptor_vs_trike/intro.mp4"))

    def test_round_intro_begins_frozen_session_and_uses_session_media(self):
        media, _ = build_media(self.root)
        media._intro_done = True
        media.on_phase_changed("MENU")
        media.select_official_set(self.alt_id)

        media.on_phase_changed("ROUND_INTRO")

        self.assertTrue(media.sets.session_active)
        self.assertEqual(media.sets.session_set.set_id, self.alt_id)
        self.assertTrue(media._scene_config("wait")["file"].endswith("assets/sets/raptor_vs_trike/orbs.mp4"))
        with self.assertRaisesRegex(SetContractError, "active session"):
            media.select_official_set(CANONICAL_SET_ID)

    def test_return_to_menu_ends_session_and_next_match_uses_new_selection(self):
        media, _ = build_media(self.root)
        media._intro_done = True
        media.on_phase_changed("MENU")
        media.select_official_set(self.alt_id)
        media.on_phase_changed("ROUND_INTRO")
        self.assertEqual(media.sets.runtime_set.set_id, self.alt_id)

        media.on_phase_changed("MENU")
        media.select_official_set(CANONICAL_SET_ID)
        media.on_phase_changed("ROUND_INTRO")

        self.assertEqual(media.sets.runtime_set.set_id, CANONICAL_SET_ID)

    def test_menu_change_invalidates_old_player_generation_and_wait_resume(self):
        media, _ = build_media(self.root)
        media._intro_done = True
        media.on_phase_changed("MENU")
        old_player = Video(filename="old.mp4", eos="loop", autoplay=False)
        old_player.position = 5.0
        old_player.duration = 10.0
        media._scene_player = old_player
        media._scene_key = "wait"
        media._scene_state = 1
        media._scene_generation = 7
        media._wait_resume_fraction = 0.5
        media._scene_completed_key = "wait"
        old_generation = media._scene_generation

        media.select_official_set(self.alt_id)

        self.assertGreater(media._scene_generation, old_generation)
        self.assertEqual(media._wait_resume_fraction, 0.0)
        self.assertIsNone(media._scene_completed_key)
        self.assertIsNone(media._scene_player)
        self.assertEqual(old_player.state, "unloaded")

    def test_selector_is_readable_official_catalog_and_visible_only_in_menu(self):
        media, _ = build_media(self.root)
        media._intro_done = True

        media.on_phase_changed("MENU")
        media._open_set_selector()

        self.assertEqual(media._set_button.opacity, 1)
        self.assertFalse(media._set_button.disabled)
        self.assertIn("Steg vs T-Rex", media._set_button.text)
        labels = [button.text for button in media._set_option_buttons]
        self.assertTrue(any("Steg vs T-Rex" in label for label in labels))
        self.assertTrue(any("Raptor vs Trike" in label for label in labels))
        self.assertTrue(media._set_popup.opened)

        media.on_phase_changed("ROUND_INTRO")
        self.assertEqual(media._set_button.opacity, 0)
        self.assertTrue(media._set_button.disabled)

    def test_phase_controller_notifies_media_on_every_real_phase_change(self):
        source = (ROOT / "tools/jtrex_phase_runtime.py").read_text(encoding="utf-8")
        self.assertIn("self.media.on_phase_changed(name)", source)


if __name__ == "__main__":
    unittest.main()
