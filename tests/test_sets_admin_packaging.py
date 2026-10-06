import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Lot05PackagingTests(unittest.TestCase):
    def test_preparer_stages_all_lot05_runtimes_and_reports_hashes(self):
        source = (ROOT / 'tools/prepare_android.py').read_text(encoding='utf-8')
        for name in ('jtrex_sets_admin.py', 'jtrex_sets_preview.py', 'jtrex_sets_android.py'):
            self.assertIn(f'stage / "{name}"', source)
            self.assertIn(f'shutil.copyfile(', source)
        for key in (
            'sets_admin_runtime_sha256',
            'sets_preview_runtime_sha256',
            'sets_android_runtime_sha256',
        ):
            self.assertIn(key, source)

    def test_workflow_triggers_compiles_and_checks_all_lot05_runtimes(self):
        source = (ROOT / '.github/workflows/android.yml').read_text(encoding='utf-8')
        for name in ('jtrex_sets_admin.py', 'jtrex_sets_preview.py', 'jtrex_sets_android.py'):
            self.assertIn(f"- 'tools/{name}'", source)
            self.assertIn(f'app/{name}', source)
        for key in (
            'sets_admin_runtime_sha256',
            'sets_preview_runtime_sha256',
            'sets_android_runtime_sha256',
        ):
            self.assertIn(key, source)


if __name__ == '__main__':
    unittest.main()
