import unittest

from runtime_harness import Harness


class CanonicalRoundModel(unittest.TestCase):
    def _run_until_state_changes(self, h, state, limit=500):
        for _ in range(limit):
            h.root.mc1(.03)
            if h.ns['indexa'] != state:
                return
        self.fail('engine remained in state {} for {} ticks'.format(state, limit))

    def _run_until_wait(self, h, limit=500):
        for _ in range(limit):
            h.root.mc1(.03)
            if h.ns['indexa'] == 1:
                return
        self.fail('engine did not return to orb wait state')

    def test_true_round_one_announcement_precedes_opening_red_blue_charge(self):
        h = Harness(); h.state(4)
        self.assertEqual(h.media.phases.name, 'ROUND_INTRO')
        self.assertEqual(h.media.phases.round_number, 1)
        self.assertEqual(h.media._round_overlay.title.text, 'ROUND 1')
        self.assertEqual(h.ns['indexa'], 4)
        h.finish_start()
        self.assertEqual(h.media.phases.name, 'CHARGE_INTERACTIVE')

    def test_red_blue_winner_deals_real_damage_but_does_not_score_a_round(self):
        for button, decided_state, damaged in (('gr', 3, 'degd'), ('dr', 2, 'degg')):
            with self.subTest(button=button):
                h = Harness(); h.state(4); h.finish_start(); h.ns['anim1'] = 1
                for _ in range(3): h.touch(button)
                self.assertEqual(h.ns['indexa'], decided_state)
                self._run_until_wait(h)
                self.assertGreater(h.ns[damaged], 0)
                other = 'degg' if damaged == 'degd' else 'degd'
                self.assertEqual(h.ns[other], 0)
                self.assertEqual(h.media.phases.round_wins, {'st': 0, 'tr': 0})
                self.assertEqual(h.media.phases.name, 'GAUGE_VERDICT')

    def test_red_blue_tie_damages_both_uses_zero_win_then_fight_then_orbs(self):
        h = Harness(); h.state(4); h.finish_start(); h.ns.update(anim1=1, anim1vv=1)
        self._run_until_wait(h)
        self.assertGreater(h.ns['degg'], 0)
        self.assertEqual(h.ns['degg'], h.ns['degd'])
        self.assertEqual(h.media.phases.round_wins, {'st': 0, 'tr': 0})
        self.assertEqual(h.media.phases.name, 'GAUGE_VERDICT')
        self.assertEqual(h.media._scene_key, 'zero-win')
        h.frame(); h.eos(); h.media._sync_current_scene()
        self.assertEqual(h.media.phases.name, 'FIGHT_INTRO')
        self.assertEqual(h.media._round_overlay.title.text, 'FIGHT!')
        h.finish_start()
        self.assertEqual(h.media.phases.name, 'ROUND_ACTIVE')
        self.assertEqual(h.ns['indexa'], 1)

    def test_orb_tie_announces_yellow_fight_before_yellow_controls(self):
        h = Harness(); h.state(7)
        self.assertEqual(h.media.phases.name, 'FIGHT_INTRO')
        self.assertEqual(h.media._round_overlay.title.text, 'FIGHT!')
        self.assertEqual(h.media._round_overlay.title.color[:3], (1, .9, .05))
        h.finish_start()
        self.assertEqual(h.media.phases.name, 'YELLOW_INTERACTIVE')

    def test_orb_winner_is_only_a_fight_verdict_without_ko(self):
        h = Harness(); h.start_round(); h.state(8)
        self._run_until_state_changes(h, 8)
        self.assertEqual(h.media.phases.round_wins, {'st': 0, 'tr': 0})
        self.assertEqual(h.media.phases.round_number, 1)
        self.assertEqual(h.media.phases.name, 'FIGHT_INTRO')
        self.assertEqual(h.media._round_overlay.title.text, 'FIGHT!')


if __name__ == '__main__':
    unittest.main()
