import unittest
from pathlib import Path


class OrbMediaManifestCanon(unittest.TestCase):
    def test_beach_loop_is_guarded_by_android_media_manifest(self):
        preparation = Path("tools/prepare_android.py").read_text(encoding="utf-8")
        self.assertIn(
            '"assets/combat/StegTrexPlageVideoenboucledesorbes.mp4": 9848376,',
            preparation,
        )


if __name__ == "__main__":
    unittest.main()
