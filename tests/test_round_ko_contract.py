import unittest

from runtime_harness import Harness


class KOBasedRoundContract(unittest.TestCase):
    def _open_round(self):
        h = Harness(); h.state(4); h.finish_start()
        self.assertEqual(h.media.phases.name, 'CHARGE_INTERACTIVE')
        self.assertEqual(h.media.phases.round_number, 1)
        return h

    def _run_until_state_changes(self, h, state, limit=500):
        for _ in range(limit):
            h.root.mc1(.03)
            if h.ns['indexa'] != state:
                return
        self.fail('engine remained in state {} for {} ticks'.format(state, limit))

    def test_orb_verdict_does_not_score_round_without_ko(self):
        h = Harness(); h.start_round(); h.state(8); self._run_until_state_changes(h, 8)
        self.assertEqual(h.media.phases.round_wins, {'st': 0, 'tr': 0})
        self.assertEqual(h.media.phases.round_number, 1)
        self.assertEqual(h.media.phases.name, 'FIGHT_INTRO')

    def test_yellow_verdict_does_not_score_round_without_ko(self):
        h = Harness(); h.start_round(); h.state(7); h.finish_start()
        self.assertEqual(h.media.phases.name, 'YELLOW_INTERACTIVE')
        h.state(5); h.state(1)
        self.assertEqual(h.media.phases.round_wins, {'st': 0, 'tr': 0})
        self.assertEqual(h.media.phases.round_number, 1)
        self.assertEqual(h.media.phases.name, 'GAUGE_VERDICT')

    def test_red_blue_result_is_followed_by_fight_before_orbs(self):
        h = self._open_round(); h.ns.update(anim1=1, anim1vv=1)
        self._run_until_state_changes(h, 4)
        self.assertEqual(h.ns['indexa'], 1)
        self.assertEqual(h.media.phases.name, 'GAUGE_VERDICT')
        h.frame(); h.eos(); h.media._sync_current_scene()
        self.assertEqual(h.media.phases.name, 'FIGHT_INTRO')
        self.assertEqual(h.media._round_overlay.title.text, 'FIGHT!')

    def test_first_ko_scores_once_resets_round_and_does_not_finish_match(self):
        h = self._open_round()
        h.ns.update(degg=123, degd=500000000, degg0=123, degd0=500000000)
        for slot in range(1, 7): h.ns['selected'][slot] = True
        h.state(10)
        self.assertEqual(h.media.phases.round_wins, {'st': 1, 'tr': 0})
        self.assertEqual(h.media.phases.round_number, 2)
        self.assertEqual(h.ns['indexa'], 4)
        self.assertEqual(h.media.phases.name, 'ROUND_INTRO')
        self.assertEqual((h.ns['degg'], h.ns['degd'], h.ns['degg0'], h.ns['degd0']), (0, 0, 0, 0))
        self.assertFalse(any(h.ns['selected'][i] for i in range(1, 7)))
        h.media.phases.sync()
        self.assertEqual(h.media.phases.round_wins, {'st': 1, 'tr': 0})

    def test_two_zero_ko_finishes_match_but_split_score_opens_round_three(self):
        h = self._open_round(); h.state(10); h.finish_start(); h.state(10)
        self.assertEqual(h.media.phases.round_wins, {'st': 2, 'tr': 0})
        self.assertEqual(h.ns['indexa'], 10)
        self.assertEqual(h.media.phases.name, 'FINISH')

        h = self._open_round(); h.state(10); h.finish_start(); h.state(11)
        self.assertEqual(h.media.phases.round_wins, {'st': 1, 'tr': 1})
        self.assertEqual(h.media.phases.round_number, 3)
        self.assertEqual(h.ns['indexa'], 4)
        self.assertEqual(h.media.phases.name, 'ROUND_INTRO')
        h.finish_start(); h.state(10)
        self.assertEqual(h.media.phases.round_wins, {'st': 2, 'tr': 1})
        self.assertEqual(h.ns['indexa'], 10)
        self.assertEqual(h.media.phases.name, 'FINISH')

    def test_lethal_power_waits_for_eos_before_round_two(self):
        h = Harness(); h.start_round(); h.ns.update(anim1=0, anim1vv=1)
        h.ns['degd'] = h.ns['degd0'] = 450000000
        h.state(21); h.frame(); power_player = h.media._scene_player
        for _ in range(300): h.root.mc1(.03)
        self.assertEqual(h.media.phases.name, 'POWER')
        self.assertIs(h.media._scene_player, power_player)
        self.assertEqual(h.media.phases.round_wins, {'st': 1, 'tr': 0})
        h.eos(); h.media._sync_current_scene()
        self.assertEqual(h.media.phases.round_number, 2)
        self.assertEqual(h.ns['indexa'], 4)
        self.assertEqual(h.media.phases.name, 'ROUND_INTRO')

    def test_exactly_one_visible_round_marker_per_camp(self):
        h = Harness()
        self.assertEqual(len(h.media.phases._round_marker_shapes), 2)
        self.assertEqual(len(h.media._round_marker_shapes), 2)


if __name__ == '__main__':
    unittest.main()
