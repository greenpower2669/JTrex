import unittest
from pathlib import Path


class OrbMediaManifestCanon(unittest.TestCase):
    def test_beach_loop_is_guarded_by_android_media_manifest(self):
        preparation = Path("tools/prepare_android.py").read_text(encoding="utf-8")
        self.assertIn(
            '"assets/combat/StegTrexPlageVideoenboucledesorbes.mp4": 9848376,',
            preparation,
        )

    def test_legacy_wait_media_remains_available_without_runtime_activation(self):
        legacy = Path("assets/combat/StegVsTrexvaetviensremolacebisorigune.mp4")
        self.assertTrue(legacy.is_file())
        self.assertEqual(legacy.stat().st_size, 2472718)
        runtime = Path("tools/jtrex_media_runtime.py").read_text(encoding="utf-8")
        self.assertNotIn("StegVsTrexvaetviensremolace", runtime)


if __name__ == "__main__":
    unittest.main()
