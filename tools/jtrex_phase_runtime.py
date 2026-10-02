"""Presentation phases around the unchanged historical engine.

The engine alone computes outcomes/impacts. Media completion only releases a
presentation gate. The hooks wrap actual engine callbacks, including UI writers.
"""
from functools import wraps


class JTPhaseController:
    BLOCKED = frozenset(("INTRO", "PRE_ROUND", "POWER", "FINISH"))
    TOUCHES = frozenset(("on_touch_down", "on_touch_move", "on_touch_up"))
    MINIMAL_HUD = frozenset(("cadre", "calque", "pvg", "pvd"))

    def __init__(self, media, engine, clock, rectangle_type, label_type):
        self.media, self.root, self.engine, self.clock = media, media.root, engine, clock
        self.name = "INTRO"
        self.state = None
        self.round_number = 0
        self.round_token = 0
        self.last_exchange = engine["_JT_EXCHANGE_ID"]
        self.cinematic_state = None
        self.media_done = False
        self.media_failed = False
        self.paused = False
        self._timer_event = None
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

    @property
    def round_active(self):
        return self.name == "ROUND_ACTIVE" and not self.paused

    def sync(self):
        state = self.engine["indexa"]
        if state != self.state:
            print("[JT-PHASE] engine {} -> {} anim={} car={} car2={} media={} generation={}".format(
                self.state, state, self.engine["anim1"], self.engine["car"],
                self.engine["car2"], self.media._scene_key, self.media._scene_generation), flush=True)
            self.state = state
        if not self.media._intro_done:
            self._set_phase("INTRO")
            return
        if self.cinematic_state is not None:
            # A completed short video must not replay while its logical action
            # is still running. A long video retains the pending engine outcome.
            if not self.media_done or state == self.cinematic_state:
                self._set_phase("POWER" if self.cinematic_state >= 21 else "FINISH")
                return
            self.cinematic_state = None
        if state in (10, 11, 21, 22, 23, 24, 25, 26):
            self.cinematic_state = state
            self.media_done = self.media_failed = False
            self._set_phase("POWER" if state >= 21 else "FINISH")
        elif state == 0:
            self.round_number = 0
            self.last_exchange = self.engine["_JT_EXCHANGE_ID"]
            self.round_token += self.name != "MENU"
            self.media.cancel_round_presentation()
            self._set_phase("MENU")
        elif state == 1:
            exchange = self.engine["_JT_EXCHANGE_ID"]
            if self.round_number == 0 or exchange != self.last_exchange:
                self.last_exchange = exchange
                self.round_number += 1
                self.round_token += 1
                # This is the historical new-exchange countdown reset. It is
                # explicit now because suspended callbacks cannot perform it.
                self.engine["car2"] = 10
                self._set_phase("PRE_ROUND")
                self.media.present_round(self.round_number, self.round_token)
            elif self.name != "PRE_ROUND":
                self._set_phase("ROUND_ACTIVE")
        elif state in (2, 3, 4):
            self._set_phase("CHARGE_INTERACTIVE")
        elif state in (5, 6, 7):
            self._set_phase("YELLOW_INTERACTIVE")
        else:
            self._set_phase("VERDICT")

    def finish_start(self, token):
        if token != self.round_token or self.name != "PRE_ROUND" or self.paused:
            return
        if self.engine["indexa"] != 1:
            return
        # The historical 2 s charge protection overlaps ROUND/START, rather
        # than starting a second invisible delay after START has disappeared.
        if self.engine["jt_orb_protected"]():
            return
        self._set_phase("ROUND_ACTIVE")
        self.media.cancel_round_presentation()
        self.apply_ui()

    def video_complete(self, state, failed=False):
        if state == self.cinematic_state:
            self.media_done = True
            self.media_failed = failed
            print("[JT-PHASE] media-complete state={} failed={} pending-engine={}".format(
                state, failed, self.engine["indexa"]), flush=True)

    def _set_phase(self, name):
        if self.name == name:
            return
        previous = self.name
        self.name = name
        if previous == "PRE_ROUND" and name != "PRE_ROUND":
            self.media.cancel_round_presentation()
        self._reset_timer()
        if self._masked:
            self._restore_ui()
        if name != "INTRO":
            # affbt normally redraws only when indexa changes. A presentation
            # phase can finish without changing indexa, so redraw it once.
            self.engine["indexa0"] = -999
            originals = self.engine["_JT_PHASE_ORIGINALS"]
            originals["affbt"](self.root, 0)
            originals["affpv"](self.root, 0)
            # carupdate no longer runs in menu/gauges/cinematics, so it cannot
            # clear stale countdown labels there. Presentation owns their text.
            for label in ("label", "labelf", "label2", "label2f"):
                small = "2" in label
                visible = (
                    name in ("PRE_ROUND", "ROUND_ACTIVE") if small
                    else name not in ("INTRO", "MENU", "POWER", "FINISH")
                )
                self._labels[label].text = str(self.engine["car2" if small else "car"]) if visible else ""
        print("[JT-PHASE] {} -> {} round={} indexa={} car={} car2={}".format(
            previous, name, self.round_number, self.engine["indexa"],
            self.engine["car"], self.engine["car2"]), flush=True)
        self.apply_ui()

    def _reset_timer(self):
        if self._timer_event is not None:
            self._timer_event.cancel()
            self._timer_event = None
        if self.round_active:
            # The first decrement is a full second AFTER actual START end.
            self._timer_event = self.clock.schedule_interval(self.root.carupdate, 1.0)

    def set_paused(self, paused):
        self.paused = paused
        self._reset_timer()

    def allows(self, callback):
        if callback == "on_touch_up":
            # Historical release only resets tracking/button sprites and removes
            # the touch canvas group. Keep that cleanup even under a cinematic.
            return True
        if self.paused:
            return False
        if callback == "carupdate":
            return self.round_active and not self.engine["jt_orb_protected"]()
        if callback == "affpv":
            # Preserve historical negative-damage clamping (notably healing).
            # apply_ui below always wins over this callback's HUD size writes.
            return True
        if callback in ("anim_1", "mc1", "savemc1"):
            if self.name == "POWER":
                return self.engine["indexa"] == self.cinematic_state
            if self.name == "FINISH":
                return self.media_failed or self.root._jt_finishing_complete_pending == self.engine["indexa"]
        return self.name not in self.BLOCKED

    def apply_ui(self):
        if self.name not in self.BLOCKED:
            return
        if not self._masked:
            self._masked_graphics = dict(self._rectangles)
            seen = {id(obj) for obj in self._masked_graphics.values()}
            seen.add(id(self.root.deux))
            # coul()/scr() draw local Ellipses directly in canvas groups, without
            # attaching attributes to root. Include these existing geometries.
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
        if self.name == "PRE_ROUND":
            w, h = self.engine["xmax"], self.engine["ymax"]
            for name in self.MINIMAL_HUD:
                self._rectangles[name].size = (w, h/8) if name in ("cadre", "calque") else (w/3.7, h/21)
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
