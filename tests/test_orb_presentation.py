import unittest

from runtime_harness import Harness

# JT-BEACH-ENERGY-CANON-003: this suite guards the phone-tested beach/energy contract.


class OrbPresentationCanon(unittest.TestCase):
    def test_new_orb_exchange_resets_countdown_and_stop_state_before_release(self):
        h = Harness(); h.start_round()
        h.ns['car2'] = 2
        h.ns['stopg'] = True
        h.ns['stopd'] = True
        h.ns['colstop'] = {i: True for i in range(1, 7)}

        h.media.phases._begin_fight('orbs')

        self.assertEqual(h.media.phases.name, 'FIGHT_INTRO')
        self.assertEqual(h.ns['car2'], 10)
        self.assertFalse(h.ns['stopg'])
        self.assertFalse(h.ns['stopd'])
        self.assertTrue(all(not h.ns['colstop'][i] for i in range(1, 7)))
        self.assertEqual(h.root.label2.text, '10')
        self.assertIsNone(h.media.phases._timer_event)

        h.finish_start()
        self.assertEqual(h.media.phases.name, 'ROUND_ACTIVE')
        self.assertEqual(h.ns['car2'], 10)
        event = h.media.phases._timer_event
        self.assertIsNotNone(event)
        self.assertEqual(event.delay, 1.0)
        event.callback(1.0)
        self.assertEqual(h.ns['car2'], 9)

    def test_power_return_keeps_remaining_orb_countdown(self):
        h = Harness(); h.start_round()
        h.ns.update(anim1=0, anim1vv=1, car=73, car2=4)
        h.state(21); h.frame()
        for _ in range(260):
            h.root.mc1(.03)
        self.assertEqual(h.media.phases.name, 'POWER')
        self.assertEqual((h.ns['car'], h.ns['car2']), (73, 4))
        h.eos(); h.media._sync_current_scene()
        self.assertEqual(h.media.phases.name, 'ROUND_ACTIVE')
        self.assertEqual((h.ns['car'], h.ns['car2']), (73, 4))

    def test_orb_wait_scene_uses_new_beach_loop_exclusively(self):
        h = Harness()
        scene = h.runtime.SCENES['wait']
        self.assertTrue(scene['loop'])
        self.assertEqual(
            scene['file'],
            'assets/combat/StegTrexPlageVideoenboucledesorbes.mp4',
        )
        self.assertFalse(hasattr(h.runtime, 'LEGACY_WAIT_FILE'))
        self.assertTrue(all(
            'StegVsTrexvaetviensremolace' not in item['file']
            for item in h.runtime.SCENES.values()
        ))

    def test_new_round_resets_both_energy_bars_to_zero(self):
        h = Harness(); h.start_round()
        h.ns['stamg'] = 91.5
        h.ns['stamd'] = 87.25
        h.ns['selected'] = {i: True for i in range(1, 7)}

        h.media.phases._reset_between_rounds()

        self.assertEqual(h.ns['stamg'], 0)
        self.assertEqual(h.ns['stamd'], 0)
        self.assertTrue(all(not h.ns['selected'][i] for i in range(1, 7)))


if __name__ == '__main__':
    unittest.main()
