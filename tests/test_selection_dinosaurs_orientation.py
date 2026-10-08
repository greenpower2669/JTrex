#!/usr/bin/env python3
"""Tests the historical g/d asset wiring and safe MENU orientation swap."""
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from prepare_android import swap_menu_dinosaur_frame_sources


class TestSelectionDinoSources(unittest.TestCase):
    def test_swap_initial_and_animated_sources(self):
        original = (
            "self.jb = Rectangle(source='g/g_0.png')\n"
            'self.jh = Rectangle(source="d/d_0.png")\n'
            "self.jb.source='g/g_'+str(int(gavv))+'.png'\n"
            'self.jh.source="d/d_"+str(int(davv))+".png"\n'
        )
        actual = swap_menu_dinosaur_frame_sources(original)
        self.assertIn("self.jb = Rectangle(source='d/d_0.png')", actual)
        self.assertIn('self.jh = Rectangle(source="g/g_0.png")', actual)
        self.assertIn("self.jb.source=('d/d_' if indexa==0 else 'g/g_')", actual)
        self.assertIn("self.jh.source=('g/g_' if indexa==0 else 'd/d_')", actual)
        self.assertIn("str(int(gavv))+'.png'", actual)
        self.assertIn('str(int(davv))+".png"', actual)

    def test_fail_closed_if_archive_wiring_changed(self):
        with self.assertRaises(RuntimeError):
            swap_menu_dinosaur_frame_sources("self.jb.source='g/g_'")

if __name__ == "__main__":
    unittest.main()
