"""Presentation phases around the historical June T-Rex engine.

The legacy engine remains authoritative for taps, score, damage, energy and its
animation-frame impacts. This controller only owns presentation gates, the
model-game round structure and the two-win match score.
"""
from functools import wraps


class JTPhaseController:
    ZERO_WIN_STATE = -7
    BLOCKED = frozenset(("INTRO", "ROUND_INTRO", "FIGHT_INTRO", "POWER", "FINISH"))
    FROZEN = BLOCKED | frozenset(("GAUGE_VERDICT", "ORB_FREEZE"))
    TOUCHES = frozenset(("on_touch_down", "on_touch_move", "on_touch_up"))
    MINIMAL_HUD = frozenset(("cadre", "calque", "pvg", "pvd"))
    GAUGE_PRESENTATION = {2: 9, 3: 8, 4: ZERO_WIN_STATE, 5: 8, 6: 9, 7: ZERO_WIN_STATE}

    def __init__(self, media, engine, clock, rectangle_type, label_type):
        self.media, self.root, self.engine, self.clock = media, media.root, engine, clock
        self.name = "INTRO"
        self.state = None
        self.round_number = 0
        self.round_wins = {"st": 0, "tr": 0}
        self.round_token = 0
        self.last_exchange = engine["_JT_EXCHANGE_ID"]
        self.cinematic_state = None
        self.media_done = False
        self.media_failed = False
        self.gauge_verdict_state = None
        self.gauge_verdict_done = False
        self.gauge_verdict_failed = False
        self.post_verdict_action = None
        self.yellow_active = False
        self.yellow_outcome = None
        self.paused = False
        self._timer_event = None
        self._orb_freeze_event = None
        self._orb_freeze_generation = 0
        self._masked = False
        self._saved_sizes = {}
        self._masked_graphics = {}
        self._rectangles = {
            name: obj for name, obj in vars(self.root).items()
            if isinstance(obj, rectangle_type) and name != "deux"
        }
        self._labels = {
            name: obj for name, obj in vars(self.root).items()
            if isinstance(obj, label_type)
        }
        self._saved_opacity = {name: obj.opacity for name, obj in self._labels.items()}
        self._install_zero_win_scene()
        self._install_gauge_media_hooks()
        self._install_round_markers()

    @property
    def round_active(self):
        return self.name == "ROUND_ACTIVE" and not self.paused

    def _install_zero_win_scene(self):
        scenes = self.media._key_for_state.__globals__["SCENES"]
        scenes["zero-win"] = {
            "states": frozenset((self.ZERO_WIN_STATE,)),
            "file": "assets/combat/Zerowinstegtrexsurleschargedejaugejauneetbleuetrouge.mp4",
            "loop": False,
        }

    def _install_round_markers(self):
        """Two symmetric match-win lamps per camp, second one farther outward."""
        self.media._round_score_values = (0, 0)
        self._round_marker_colors = []
        self._round_marker_shapes = []
        try:
            color_type = type(self.media._status_dot_color)
            ellipse_type = type(self.media._status_dot_shape)
            with self.root.canvas.after:
                for _ in range(4):
                    color = color_type(.18, .18, .18, .72)
                    shape = ellipse_type(pos=(0, 0), size=(0, 0))
                    self._round_marker_colors.append(color)
                    self._round_marker_shapes.append(shape)
            self.root.bind(size=self._layout_round_markers, pos=self._layout_round_markers)
            self._layout_round_markers()
        except Exception as exc:
            print("[JT-ROUND-SCORE][WARN] marker-init={!r}".format(exc), flush=True)
        self._paint_round_markers()

    def _layout_round_markers(self, *args):
        if len(self._round_marker_shapes) != 4:
            return
        w, h = float(self.engine["xmax"]), float(self.engine["ymax"])
        diameter = max(10.0, min(w, h) * .026)
        y = h * .865
        centers = (
            (w * .325, y), (w * .292, y),
            (w * .675, y), (w * .708, y),
        )
        for shape, (cx, cy) in zip(self._round_marker_shapes, centers):
            shape.size = (diameter, diameter)
            shape.pos = (cx - diameter / 2.0, cy - diameter / 2.0)

    def _paint_round_markers(self):
        st, tr = self.round_wins["st"], self.round_wins["tr"]
        self.media._round_score_values = (st, tr)
        visible = self.name not in ("INTRO", "MENU", "POWER", "FINISH")
        for i, color in enumerate(self._round_marker_colors):
            lit = (i < 2 and i < st) or (i >= 2 and (i - 2) < tr)
            try:
                color.rgba = ((.08, .95, .18, 1.0) if lit else (.18, .18, .18, .72)) if visible else (0, 0, 0, 0)
            except Exception:
                pass
        print("[JT-ROUND-SCORE] ST={} TR={} round={}".format(st, tr, self.round_number), flush=True)

    def _install_gauge_media_hooks(self):
        """Present gauge verdict media without re-entering historical states 8/9."""
        media = self.media
        if getattr(media, "_jt_gauge_verdict_hooks", False):
            return
        original_sync_scene_state = media.sync_scene_state
        original_scene_eos = media._on_scene_eos
        media._jt_gauge_verdict_hooks = True
        media._jt_original_sync_scene_state = original_sync_scene_state
        media._jt_original_scene_eos = original_scene_eos

        def sync_scene_state(indexa):
            self.sync()
            self.apply_ui()
            presentation_state = (
                self.gauge_verdict_state
                if self.name == "GAUGE_VERDICT" and not self.gauge_verdict_done
                else None
            )
            if presentation_state is None:
                return original_sync_scene_state(self.engine["indexa"])
            if not media._intro_done:
                return
            media._engine_state = self.engine["indexa"]
            key = media._key_for_state(presentation_state)
            if key is None:
                self.video_complete(presentation_state, failed=True)
                return
            if key != media._scene_key:
                media._stop_scene("gauge-verdict={}".format(presentation_state), preserve_failure=False)
            media._scene_state = presentation_state
            if (
                media._scene_player is None
                and not (key == media._scene_failed_key and media._scene_key == key)
            ):
                media._start_scene(key, presentation_state)

        def scene_eos(player, generation):
            if (
                self.name == "GAUGE_VERDICT"
                and self.gauge_verdict_state in (8, 9, self.ZERO_WIN_STATE)
                and media._scene_state == self.gauge_verdict_state
                and media._scene_key in ("st-win", "tr-win", "zero-win")
            ):
                if player is not media._scene_player or generation != media._scene_generation:
                    return
                media._scene_eos_reached = True
                print(
                    "[JT-GAUGE-VERDICT] eos presentation={} engine={} key={} generation={}".format(
                        self.gauge_verdict_state, self.engine["indexa"], media._scene_key, generation
                    ),
                    flush=True,
                )
                self.video_complete(self.gauge_verdict_state)
                media._stop_scene("gauge-verdict-eos", preserve_failure=False)
                return
            return original_scene_eos(player, generation)

        media.sync_scene_state = sync_scene_state
        media._on_scene_eos = scene_eos

    def _begin_round(self):
        self.round_number += 1
        self.round_token += 1
        self.yellow_active = False
        self.yellow_outcome = None
        self.engine["tapg"] = 0
        self.engine["tapd"] = 0
        self.engine["anim1"] = 0
        self.engine["anim1vv"] = 1
        self.engine["indexa"] = 4
        self.state = 4
        self._set_phase("ROUND_INTRO")
        self.media.present_round(self.round_number, self.round_token)
        print("[JT-ROUND] begin round={} score={}".format(self.round_number, self.round_wins), flush=True)

    def _begin_fight(self):
        self.yellow_active = True
        self.yellow_outcome = None
        self.round_token += 1
        self._set_phase("FIGHT_INTRO")
        self.media.present_round(self.round_number, self.round_token)
        overlay = self.media._round_overlay
        if overlay is not None:
            overlay.stage = "FIGHT"
            overlay.elapsed = 0.0
            overlay.title.text = overlay.shadow.text = "FIGHT!"
            try:
                overlay.title.color = (1, .9, .05, 1)
            except Exception:
                pass
        print("[JT-FIGHT] yellow confrontation round={} token={}".format(self.round_number, self.round_token), flush=True)

    def _record_round_win(self, camp, source):
        self.round_wins[camp] += 1
        self._paint_round_markers()
        print("[JT-ROUND] winner={} source={} score={}".format(camp, source, self.round_wins), flush=True)
        return self.round_wins[camp] >= 2

    def _queue_gauge_verdict(self, outcome, family):
        self.gauge_verdict_state = self.GAUGE_PRESENTATION[outcome]
        self.gauge_verdict_done = self.gauge_verdict_failed = False
        if family == "yellow" and outcome in (5, 6):
            camp = "st" if outcome == 5 else "tr"
            final = self._record_round_win(camp, "yellow")
            self.post_verdict_action = ("finish", camp) if final else ("next_round", camp)
        else:
            self.post_verdict_action = ("orbs", None)
        print(
            "[JT-GAUGE-VERDICT] queue family={} outcome={} presentation={} action={}".format(
                family, outcome, self.gauge_verdict_state, self.post_verdict_action
            ),
            flush=True,
        )
        self._set_phase("GAUGE_VERDICT")

    def _release_gauge_verdict(self):
        state = self.gauge_verdict_state
        action = self.post_verdict_action
        print(
            "[JT-GAUGE-VERDICT] release presentation={} failed={} action={}".format(
                state, self.gauge_verdict_failed, action
            ),
            flush=True,
        )
        self.gauge_verdict_state = None
        self.gauge_verdict_done = self.gauge_verdict_failed = False
        self.post_verdict_action = None
        self.yellow_active = False
        self.yellow_outcome = None
        if action and action[0] == "finish":
            self.engine["anim1"] = 0
            self.engine["indexa"] = 10 if action[1] == "st" else 11
            self.state = self.engine["indexa"]
            self.cinematic_state = self.state
            self.media_done = self.media_failed = False
            self._set_phase("FINISH")
            return
        if action and action[0] == "next_round":
            self._begin_round()
            return
        self._enter_orb_freeze()

    def _enter_orb_freeze(self):
        self.engine["indexa"] = 1
        self.state = 1
        self.engine["car2"] = 10
        self.engine["_JT_ORB_TOUCH_PROTECT_UNTIL"] = self.clock.get_time() + 2.0
        self._orb_freeze_generation += 1
        generation = self._orb_freeze_generation
        if self._orb_freeze_event is not None:
            self._orb_freeze_event.cancel()
        self._set_phase("ORB_FREEZE")
        self._orb_freeze_event = self.clock.schedule_once(
            lambda dt: self._finish_orb_freeze(generation), 2.0
        )
        print("[JT-ORB] presentation freeze 2.0s round={}".format(self.round_number), flush=True)

    def _finish_orb_freeze(self, generation):
        if generation != self._orb_freeze_generation:
            return
        self._orb_freeze_event = None
        if self.name != "ORB_FREEZE" or self.engine["indexa"] != 1 or self.paused:
            return
        self.engine["_JT_ORB_TOUCH_PROTECT_UNTIL"] = self.clock.get_time()
        self._set_phase("ROUND_ACTIVE")
        self.apply_ui()

    def _resolve_orb_round(self, previous_state):
        camp = "st" if previous_state == 8 else "tr"
        final = self._record_round_win(camp, "orbs")
        if final:
            self.engine["anim1"] = 0
            self.engine["indexa"] = 10 if camp == "st" else 11
            self.state = self.engine["indexa"]
            self.cinematic_state = self.state
            self.media_done = self.media_failed = False
            self._set_phase("FINISH")
        else:
            self._begin_round()

    def sync(self):
        state = self.engine["indexa"]
        previous_state = self.state
        if state != self.state:
            print(
                "[JT-PHASE] engine {} -> {} anim={} car={} car2={} media={} generation={}".format(
                    self.state, state, self.engine["anim1"], self.engine["car"], self.engine["car2"],
                    self.media._scene_key, self.media._scene_generation
                ),
                flush=True,
            )
            self.state = state

        if not self.media._intro_done:
            self._set_phase("INTRO")
            return

        if self.cinematic_state is not None:
            if not self.media_done or state == self.cinematic_state:
                self._set_phase("POWER" if self.cinematic_state >= 21 else "FINISH")
                return
            self.cinematic_state = None

        if state in (10, 11, 21, 22, 23, 24, 25, 26):
            if self.cinematic_state != state:
                self.cinematic_state = state
                self.media_done = self.media_failed = False
            self._set_phase("POWER" if state >= 21 else "FINISH")
            return

        if state == 0:
            self.gauge_verdict_state = None
            self.gauge_verdict_done = self.gauge_verdict_failed = False
            self.post_verdict_action = None
            self.yellow_active = False
            self.yellow_outcome = None
            self.round_number = 0
            self.round_wins = {"st": 0, "tr": 0}
            self.media._round_score_values = (0, 0)
            self.last_exchange = self.engine["_JT_EXCHANGE_ID"]
            self.round_token += self.name != "MENU"
            self.media.cancel_round_presentation()
            self._cancel_orb_freeze()
            self._set_phase("MENU")
            self._paint_round_markers()
            return

        if state == 4 and self.round_number == 0:
            self._begin_round()
            return

        if state in (5, 6):
            self.yellow_outcome = state

        if state == 1:
            if self.gauge_verdict_state is not None:
                if not self.gauge_verdict_done:
                    self._set_phase("GAUGE_VERDICT")
                    return
                self._release_gauge_verdict()
                return

            if previous_state in (8, 9):
                self._resolve_orb_round(previous_state)
                return

            if self.yellow_outcome in (5, 6):
                outcome = self.yellow_outcome
                self._queue_gauge_verdict(outcome, "yellow")
                return
            if self.yellow_active and previous_state == 7:
                self._queue_gauge_verdict(7, "yellow")
                return
            if previous_state in (2, 3, 4):
                self._queue_gauge_verdict(previous_state, "red-blue")
                return

            if self.name != "ORB_FREEZE":
                self._set_phase("ROUND_ACTIVE")
            return

        if state in (2, 3, 4):
            if self.name == "ROUND_INTRO":
                return
            self._set_phase("CHARGE_INTERACTIVE")
            return

        if state == 7 and not self.yellow_active:
            self._begin_fight()
            return

        if state in (5, 6, 7):
            if self.name == "FIGHT_INTRO":
                return
            self._set_phase("YELLOW_INTERACTIVE")
            return

        if state in (8, 9):
            self._set_phase("VERDICT")
            return

        self._set_phase("VERDICT")

    def finish_start(self, token):
        if token != self.round_token or self.paused:
            return
        if self.name == "ROUND_INTRO":
            if self.engine["indexa"] not in (2, 3, 4):
                return
            self.media.cancel_round_presentation()
            self._set_phase("CHARGE_INTERACTIVE")
            self.apply_ui()
            return
        if self.name == "FIGHT_INTRO":
            if self.engine["indexa"] not in (5, 6, 7):
                return
            self.media.cancel_round_presentation()
            self._set_phase("YELLOW_INTERACTIVE")
            self.apply_ui()

    def video_complete(self, state, failed=False):
        if state == self.gauge_verdict_state:
            self.gauge_verdict_done = True
            self.gauge_verdict_failed = failed
            print(
                "[JT-GAUGE-VERDICT] media-complete presentation={} failed={} engine={}".format(
                    state, failed, self.engine["indexa"]
                ),
                flush=True,
            )
            self.clock.schedule_once(self.media._sync_current_scene, 0)
            return
        if state == self.cinematic_state:
            self.media_done = True
            self.media_failed = failed
            print(
                "[JT-PHASE] media-complete state={} failed={} pending-engine={}".format(
                    state, failed, self.engine["indexa"]
                ),
                flush=True,
            )

    def _set_phase(self, name):
        if self.name == name:
            return
        previous = self.name
        self.name = name
        if previous in ("ROUND_INTRO", "FIGHT_INTRO") and name != previous:
            self.media.cancel_round_presentation()
        self._reset_timer()
        if self._masked:
            self._restore_ui()
        if name != "INTRO":
            self.engine["indexa0"] = -999
            originals = self.engine["_JT_PHASE_ORIGINALS"]
            originals["affbt"](self.root, 0)
            originals["affpv"](self.root, 0)
            for label in ("label", "labelf", "label2", "label2f"):
                small = "2" in label
                visible = (
                    name in ("ROUND_INTRO", "FIGHT_INTRO", "ORB_FREEZE", "ROUND_ACTIVE")
                    if small else name not in ("INTRO", "MENU", "POWER", "FINISH")
                )
                self._labels[label].text = str(self.engine["car2" if small else "car"]) if visible else ""
        print(
            "[JT-PHASE] {} -> {} round={} score={}-{} indexa={} car={} car2={}".format(
                previous, name, self.round_number, self.round_wins["st"], self.round_wins["tr"],
                self.engine["indexa"], self.engine["car"], self.engine["car2"]
            ),
            flush=True,
        )
        self._paint_round_markers()
        self.apply_ui()

    def _reset_timer(self):
        if self._timer_event is not None:
            self._timer_event.cancel()
            self._timer_event = None
        if self.round_active:
            self._timer_event = self.clock.schedule_interval(self.root.carupdate, 1.0)

    def _cancel_orb_freeze(self):
        self._orb_freeze_generation += 1
        if self._orb_freeze_event is not None:
            self._orb_freeze_event.cancel()
            self._orb_freeze_event = None

    def set_paused(self, paused):
        self.paused = paused
        self._reset_timer()

    def allows(self, callback):
        if callback == "on_touch_up":
            return True
        if self.paused:
            return False
        if callback == "carupdate":
            return self.round_active and not self.engine["jt_orb_protected"]()
        if callback == "affpv":
            return True
        if callback in ("anim_1", "mc1", "savemc1"):
            if self.name == "POWER":
                return self.engine["indexa"] == self.cinematic_state
            if self.name == "FINISH":
                return self.media_failed or self.root._jt_finishing_complete_pending == self.engine["indexa"]
        return self.name not in self.FROZEN

    def apply_ui(self):
        if self.name not in self.BLOCKED:
            return
        if not self._masked:
            self._masked_graphics = dict(self._rectangles)
            seen = {id(obj) for obj in self._masked_graphics.values()}
            seen.add(id(self.root.deux))
            for layer in (self.root.canvas.before, self.root.canvas, self.root.canvas.after):
                for obj in layer.children:
                    if id(obj) not in seen and hasattr(obj, "size") and hasattr(obj, "pos"):
                        self._masked_graphics["canvas-{}".format(id(obj))] = obj
                        seen.add(id(obj))
            self._saved_sizes = {name: tuple(obj.size) for name, obj in self._masked_graphics.items()}
            self._masked = True
        for obj in self._masked_graphics.values():
            obj.size = (0, 0)
        for obj in self._labels.values():
            obj.opacity = 0
        if self.name in ("ROUND_INTRO", "FIGHT_INTRO"):
            w, h = self.engine["xmax"], self.engine["ymax"]
            for name in self.MINIMAL_HUD:
                self._rectangles[name].size = (w, h / 8) if name in ("cadre", "calque") else (w / 3.7, h / 21)
            for name in ("label", "labelf", "label2", "label2f"):
                obj = self._labels[name]
                obj.text = str(self.engine["car2" if "2" in name else "car"])
                obj.opacity = self._saved_opacity[name]

    def _restore_ui(self):
        for name, size in self._saved_sizes.items():
            self._masked_graphics[name].size = size
        for name, opacity in self._saved_opacity.items():
            self._labels[name].opacity = opacity
        self._masked = False
        self._masked_graphics = {}

    def shutdown(self):
        self.paused = True
        self.round_token += 1
        self._cancel_orb_freeze()
        self._reset_timer()


def install_phase_hooks(game_class, engine):
    """Wrap all historical update/input entry points in one phase policy."""
    originals = {}
    engine["_JT_PHASE_ORIGINALS"] = originals
    for name in (
        "on_touch_down", "on_touch_move", "on_touch_up", "carupdate", "colvv",
        "anim_1", "mc1", "savemc1", "affbt", "affpv", "screen_up", "pter", "ga", "da",
    ):
        original = getattr(game_class, name)
        originals[name] = original

        def wrap(method, callback):
            @wraps(method)
            def guarded(root, *args, **kwargs):
                phase = engine.get("_JT_PHASES")
                if phase is None:
                    return method(root, *args, **kwargs)
                phase.sync()
                if not phase.allows(callback):
                    phase.apply_ui()
                    return True if callback in phase.TOUCHES else None
                try:
                    return method(root, *args, **kwargs)
                finally:
                    phase.sync()
                    phase.apply_ui()
            return guarded
        setattr(game_class, name, wrap(original, name))
