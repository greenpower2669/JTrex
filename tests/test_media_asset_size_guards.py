import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREPARE_ANDROID = ROOT / "tools" / "prepare_android.py"


def read_media_assets():
    tree = ast.parse(PREPARE_ANDROID.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "MEDIA_ASSETS":
                    return ast.literal_eval(node.value)
    raise AssertionError("MEDIA_ASSETS not found in tools/prepare_android.py")


class MediaAssetSizeGuardTests(unittest.TestCase):
    def test_declared_media_sizes_match_repository_assets(self):
        mismatches = []
        for relative, expected_size in read_media_assets().items():
            path = ROOT / relative
            if not path.is_file():
                mismatches.append((relative, expected_size, "missing"))
                continue
            actual_size = path.stat().st_size
            if actual_size != expected_size:
                mismatches.append((relative, expected_size, actual_size))
        self.assertEqual([], mismatches)


if __name__ == "__main__":
    unittest.main()
