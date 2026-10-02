import unittest
from types import SimpleNamespace
from runtime_harness import Clock, Harness, Video


class PhaseIntegration(unittest.TestCase):
    def test_direct_canvas_geometry_is_hidden_and_restored(self):
        h = Harness(); h.start_round()
        # coul() creates local Ellipses directly in canvas.before, not root attrs.
        circle = SimpleNamespace(pos=(10,10), size=(180,180))
        h.root.canvas.before.children.append(circle)
        h.state(21); h.frame(); h.callbacks()
        self.assertEqual(circle.size, (0,0))
        h.ns['indexa'] = 1
        h.eos(); h.media._sync_current_scene()
        self.assertEqual(circle.size, (180,180))

    def test_touch_release_during_cinematic_cleans_its_canvas_group(self):
        h = Harness(); h.start_round(); h.touch('gr')
        removed = []
        h.root.canvas.remove_group = removed.append
        h.state(21); h.frame()
        h.root.on_touch_up(h.last_touch)
        self.assertIsNone(h.last_touch.grab_current)
        self.assertIn(h.last_touch.ud['group'], removed)

    def test_timeout_stops_wait_video_and_returns_to_menu(self):
        h = Harness(); h.start_round(); h.frame()
        player = h.media._scene_player
        h.ns['car'] = 0
        h.root.carupdate(1)
        self.assertEqual(h.ns['indexa'], 0)
        self.assertIsNone(h.media._scene_player)
        self.assertEqual(player.volume, 0)

    def test_ai_power_launch_preserves_both_countdowns_and_fractional_cost(self):
        h = Harness(); h.start_round()
        h.ns.update(vsg=True, vsd=False, computer=lambda *args: True,
                    stamg=40.5, car=75, car2=3)
        h.root.carupdate(1)
        self.assertEqual(h.ns['indexa'], 22)
        self.assertEqual(h.ns['stamg'], .5)
        self.assertTrue(h.ns['selected'][2])
        self.assertEqual((h.ns['car'], h.ns['car2']), (75,3))

    def test_start_completion_releases_controls_and_first_full_timer_second(self):
        h = Harness(); h.start_round()
        self.assertEqual(h.media.phases.name, "ROUND_ACTIVE")
        self.assertEqual(h.ns['car'], 100)
        event = h.media.phases._timer_event
        self.assertEqual(event.delay, 1)
        event.callback(1)
        self.assertEqual((h.ns['car'], h.ns['car2']), (99, 9))
        h.touch('gr')
        self.assertTrue(h.ns['colstop'][1])

    def test_gauge_families_keep_real_buttons_and_tap_decisions(self):
        for state, button, winner in ((4, 'gr', 3), (7, 'gj', 5)):
            with self.subTest(state=state):
                h = Harness(); h.state(state); h.frame()
                h.ns['anim1'] = 1
                h.callbacks()
                self.assertNotEqual(getattr(h.root, button).size, (0, 0))
                for _ in range(3): h.touch(button)
                self.assertEqual(h.ns['indexa'], winner)
                self.assertEqual(h.ns['tapg'], 3)
                self.assertEqual(len(Video.instances), 1)

    def test_power_deals_one_historical_impact_then_waits_for_eos(self):
        h = Harness(); h.start_round()
        h.ns.update(anim1=0, anim1vv=1, car=75, car2=7)
        h.state(21); h.frame()
        for _ in range(260): h.root.mc1(.03)
        self.assertEqual(h.ns['indexa'], 1)
        self.assertEqual(h.ns['degd'], 93750000)
        self.assertEqual(h.media.phases.name, 'POWER')
        h.callbacks()
        self.assertEqual((h.ns['car'],h.ns['car2']), (75,7))
        h.eos(); h.media._sync_current_scene()
        self.assertEqual(h.media.phases.name, 'ROUND_ACTIVE')
        self.assertEqual(h.media.phases.round_number, 1)
        self.assertIsNone(h.media._round_overlay)
        self.assertEqual(h.ns['degd'], 93750000)

    def test_lethal_power_queues_both_finishing_directions_until_true_eos(self):
        for power, finish, damage in ((21, 10, 'degd'), (26, 11, 'degg')):
            with self.subTest(power=power):
                h = Harness(); h.start_round()
                h.ns.update(anim1=0, anim1vv=1)
                h.ns[damage] = h.ns[damage+'0'] = 450000000
                h.state(power); h.frame()
                power_player = h.media._scene_player
                for _ in range(300): h.root.mc1(.03)
                self.assertEqual(h.ns['indexa'], finish)
                self.assertIs(h.media._scene_player, power_player)
                self.assertEqual(h.media.phases.name, 'POWER')
                h.eos(); h.media._sync_current_scene(); h.frame()
                self.assertEqual(h.media.phases.name, 'FINISH')
                for _ in range(300): h.root.mc1(.03)
                self.assertEqual(h.ns['indexa'], finish)
                h.eos(); h.root.mc1(.03)
                self.assertEqual(h.ns['indexa'], 0)
                self.assertEqual(h.media.phases.name, 'MENU')
                self.assertEqual(h.root.label.text, '')
                self.assertEqual(h.root.label2.text, '')

    def test_short_power_eos_does_not_apply_damage_and_logic_still_completes(self):
        h = Harness(); h.start_round()
        h.ns.update(anim1=0, anim1vv=1)
        h.state(21); h.frame()
        bounds = (h.root.deux.pos, h.root.deux.size)
        h.eos()
        self.assertEqual((h.root.deux.pos, h.root.deux.size), bounds)
        self.assertEqual(h.ns['degd'], 0)
        self.assertEqual(h.media.phases.name, 'POWER')
        for _ in range(260): h.root.mc1(.03)
        self.assertEqual(h.ns['degd'], 93750000)
        self.assertEqual(h.media.phases.name, 'ROUND_ACTIVE')
        self.assertEqual(sum('sanctuary' in p.filename for p in Video.instances), 1)

    def test_round_number_follows_scored_exchanges_and_resets_at_menu(self):
        h = Harness(); h.start_round()
        h.ns['colstop'] = {i: True for i in range(1,7)}
        h.root.colvv(.04)
        self.assertEqual(h.ns['indexa'], 7)
        h.ns.update(anim1=152, anim1vv=1)
        h.root.mc1(.03)
        self.assertEqual(h.ns['indexa'], 1)
        self.assertEqual(h.media.phases.round_number, 2)
        self.assertEqual(h.media.phases.name, 'PRE_ROUND')
        token = h.media.phases.round_token
        h.state(0)
        h.media.phases.finish_start(token)
        self.assertEqual(h.media.phases.name, 'MENU')
        self.assertEqual(h.media.phases.round_number, 0)

    def test_old_frame_and_old_eos_do_not_affect_current_scene(self):
        h = Harness(); h.start_round(); h.frame()
        old, generation = h.media._scene_player, h.media._scene_generation
        h.state(21); h.frame()
        current = h.media._scene_player
        h.media._on_scene_frame(old, generation)
        h.media._on_scene_eos(old, generation)
        self.assertIs(h.media._scene_player, current)
        self.assertFalse(h.media.phases.media_done)

    def test_wait_remembers_position_and_seeks_once_after_interruption(self):
        h = Harness(); h.start_round(); h.frame()
        h.media._scene_player.position = 6
        h.state(21); h.frame()
        h.ns['indexa'] = 1
        h.eos(); h.media._sync_current_scene()
        h.frame(); h.frame()
        self.assertEqual(h.media._scene_player.seeks, [.5])
        h.eos()  # Natural wait EOS stays in loop, never starts ROUND again.
        self.assertEqual(h.media.phases.name, 'ROUND_ACTIVE')
        self.assertIsNone(h.media._round_overlay)

    def test_pause_cannot_complete_start_or_consume_time(self):
        h = Harness(); h.state(4); h.state(1)
        h.media.on_pause(); h.finish_start(); h.callbacks()
        self.assertEqual(h.media.phases.name, 'PRE_ROUND')
        self.assertEqual((h.ns['car'],h.ns['car2']), (100,10))
        h.media.on_resume(); h.finish_start()
        self.assertEqual(h.media.phases.name, 'ROUND_ACTIVE')

    def test_power_load_failure_does_not_deadlock_or_retry_each_tick(self):
        h = Harness(); h.start_round()
        h.media._resolve = lambda path: None
        h.ns.update(anim1=0, anim1vv=1)
        h.state(21)
        for _ in range(260): h.root.mc1(.03)
        self.assertEqual(h.ns['degd'], 93750000)
        self.assertEqual(h.media.phases.name, 'ROUND_ACTIVE')

    def test_power_ui_cannot_be_recreated_after_engine_returns_to_wait(self):
        h = Harness()
        h.state(21); h.frame()
        h.ns.update(indexa=1, car=63, car2=3)
        h.media.sync_scene_state(1)
        for _ in range(3): h.callbacks()
        self.assertEqual((h.ns["car"], h.ns["car2"]), (63, 3))
        for name in ("cadretr", "grb", "drb", "c3cg", "c3cd", "nrjg", "pvg", "gr", "b1s"):
            self.assertEqual(getattr(h.root, name).size, (0, 0), name)
        self.assertFalse(h.root.label2.text and h.root.label2.opacity)

    def test_finished_short_power_is_not_started_again_while_engine_is_still_in_power(self):
        h = Harness()
        h.state(21); h.frame(); h.eos()
        h.media.sync_scene_state(21)
        self.assertEqual(len(Video.instances), 1)

    def test_finishing_hud_stays_hidden_after_affpv(self):
        h = Harness()
        h.state(11); h.frame(); h.callbacks()
        for name in ("nrjg", "nrjd", "pvg", "pvd", "cadretr"):
            self.assertEqual(getattr(h.root, name).size, (0, 0), name)

    def test_preround_freezes_both_timers_and_orbs_until_start_completion(self):
        h = Harness()
        h.state(4); h.state(1)
        h.ns.update(car=100, car2=10)
        before = h.ns["haut"].copy()
        h.callbacks()
        self.assertEqual((h.ns["car"], h.ns["car2"]), (100, 10))
        self.assertEqual(h.ns["haut"], before)
        self.assertEqual(h.root.label.text, "100")
        self.assertEqual(h.root.label2.text, "10")


if __name__ == "__main__":
    unittest.main()
