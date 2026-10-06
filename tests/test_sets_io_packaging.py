import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SetIOPackagingTests(unittest.TestCase):
    def test_preparer_stages_and_compiles_sets_io_runtime(self):
        source = (ROOT / 'tools/prepare_android.py').read_text(encoding='utf-8')
        self.assertIn('jtrex_sets_io.py', source)
        self.assertIn('shutil.copyfile(sets_io_runtime', source)
        self.assertIn('compile(', source)

    def test_preparer_reports_sets_io_runtime_sha(self):
        source = (ROOT / 'tools/prepare_android.py').read_text(encoding='utf-8')
        self.assertIn('sets_io_runtime_sha256', source)
        self.assertIn('digest(stage / "jtrex_sets_io.py")', source)

    def test_android_workflow_triggers_and_validates_sets_io_runtime(self):
        source = (ROOT / '.github/workflows/android.yml').read_text(encoding='utf-8')
        self.assertIn("- 'tools/jtrex_sets_io.py'", source)
        self.assertIn('app/jtrex_sets_io.py', source)
        self.assertIn('sets_io_runtime_sha256', source)

    def test_android_workflow_compiles_sets_io_runtime(self):
        source = (ROOT / '.github/workflows/android.yml').read_text(encoding='utf-8')
        self.assertIn('py_compile', source)
        self.assertIn('jtrex_sets_io.py', source)


if __name__ == '__main__':
    unittest.main()
