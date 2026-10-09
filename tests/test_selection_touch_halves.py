#!/usr/bin/env python3
"""MENU split screen: routing, finger ownership and gameplay isolation."""
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from prepare_android import JT_TOUCH_ROUTING_HELPERS


class TestHalfScreenTouchRouting(unittest.TestCase):
    def setUp(self):
        self.env = {"Window": SimpleNamespace(width=1000), "xmax": 1000, "indexa": 0}
        exec(JT_TOUCH_ROUTING_HELPERS, self.env)

    def finger(self, x):
        return SimpleNamespace(x=x, ud={"_jt_menu_half": "left" if x < 500 else "right"})

    def test_left_and_right_control_their_own_dinosaurs(self):
        left, right = self.finger(200), self.finger(800)
        self.assertTrue(self.env["jt_menu_touch_left"](left))
        self.assertFalse(self.env["jt_menu_touch_right"](left))
        self.assertTrue(self.env["jt_menu_touch_right"](right))
        self.assertFalse(self.env["jt_menu_touch_left"](right))
        self.assertEqual(self.env["jt_menu_aim_x"](left, "left"), 200)
        self.assertEqual(self.env["jt_menu_aim_x"](right, "right"), 800)

    def test_two_fingers_keep_ownership_across_the_middle(self):
        left, right = self.finger(100), self.finger(900)
        left.x, right.x = 900, 100
        self.assertTrue(self.env["jt_menu_touch_left"](left))
        self.assertTrue(self.env["jt_menu_touch_right"](right))
        self.assertLess(self.env["jt_menu_aim_x"](left,"left"), 500)
        self.assertGreaterEqual(self.env["jt_menu_aim_x"](right,"right"), 500)

    def test_midline_belongs_to_right_and_non_menu_stays_historical(self):
        right = self.finger(500)
        self.assertTrue(self.env["jt_menu_touch_right"](right))
        self.env["indexa"] = 1
        left = self.finger(100)
        self.assertFalse(self.env["jt_menu_touch_left"](left))
        self.assertTrue(self.env["jt_menu_touch_right"](left))
        self.assertEqual(self.env["jt_menu_aim_x"](left,"left"),100)

if __name__ == "__main__":
    unittest.main()
