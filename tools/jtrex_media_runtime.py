"""Kivy video integration for June T-Rex.

Gameplay stays in the historical main.py. This module owns launch intros and
visual replacements for selected combat scenes. Video EOS never changes the
historical state machine.
"""

import random
from pathlib import Path

from kivy.clock import Clock
from kivy.core.video import Video as CoreVideo
from kivy.graphics import Color, Rectangle
from kivy.resources import resource_find
from kivy.uix.widget import Widget


INTRO_FILES = (
    "assets/intro/JTrexintro1.mp4",
    "assets/intro/JTrexintro2.mp4",
    "assets/intro/JTrexintro3.mp4",
)

SCENES = {
    "wait": {
        "states": frozenset((1,)),
        "file": "assets/combat/StegVsTrexvaetviensremolacebisorigune.mp4",
        "loop": True,
    },
    "charge": {
        "states": frozenset((2, 3, 4)),
        "file": "assets/combat/Chargestegtrexchargerougebleu.mp4",
        "loop": False,
    },
    "yellow": {
        "states": frozenset((5, 6, 7)),
        "file": "assets/combat/Stegtrexegalitechargeboutonjaune.mp4",
        "loop": False,
    },
    "st-win": {
        "states": frozenset((8,)),
        "file": "assets/combat/Stegtrexresultstegwin.mp4",
        "loop": False,
    },
    "tr-win": {
        "states": frozenset((9,)),
        "file": "assets/combat/Stegtrexresulttrexwin.mp4",
        "loop": False,
    },
}


class IntroOverlay(Widget):
    """Black letterbox overlay that swallows touches during the intro."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._texture_size = None
        with self.canvas:
            Color(0, 0, 0, 1)
            self._background = Rectangle(pos=self.pos, size=self.size)
            Color(1, 1, 1, 1)
            self._video = Rectangle(pos=self.pos, size=(0, 0))
        self.bind(pos=self._layout, size=self._layout)

    def set_texture(self, texture):
        self._video.texture = texture
        self._texture_size = texture.size if texture is not None else None
        self._layout()

    def _layout(self, *args):
        self._background.pos = self.pos
        self._background.size = self.size
        if not self._texture_size:
            self._video.pos = self.pos
            self._video.size = (0, 0)
            return
        tw, th = self._texture_size
        ww, wh = self.size
        if tw <= 0 or th <= 0 or ww <= 0 or wh <= 0:
            return
        # Intros deliberately remain aspect-fit / complete.
        scale = min(ww / float(tw), wh / float(th))
        vw, vh = tw * scale, th * scale
        self._video.size = (vw, vh)
        self._video.pos = (
            self.x + (ww - vw) / 2.0,
            self.y + (wh - vh) / 2.0,
        )

    def on_touch_down(self, touch):
        return True

    def on_touch_move(self, touch):
        return True

    def on_touch_up(self, touch):
        return True


class JTMediaController:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self._intro_player = None
        self._intro_overlay = None
        self._intro_timeout = None
        self._intro_done_callback = None
        self._intro_done = False

        self._scene_player = None
        self._scene_key = None
        self._scene_generation = 0
        self._scene_has_frame = False
        self._scene_timeout = None
        self._scene_frame_callback = None
        self._scene_eos_callback = None
        self._scene_failed_key = None
        self._scene_rect_pos = None
        self._scene_rect_size = None
        self._paused_player = None

        self.root._jt_scene_video_active = False
        # Compatibility with the first wait-only integration.
        self.root._jt_wait_video_active = False

        provider = getattr(CoreVideo, "__module__", repr(CoreVideo))
        print("[JT-MEDIA] video provider={}".format(provider), flush=True)

    @staticmethod
    def _resolve(relative_path):
        found = resource_find(relative_path)
        if found:
            return found
        path = Path(relative_path)
        return str(path) if path.is_file() else None

    @staticmethod
    def _cover_rectangle(rectangle, texture, bounds_pos, bounds_size):
        """Aspect-fill a game scene while preserving source proportions."""
        tw, th = texture.size
        bw, bh = bounds_size
        bx, by = bounds_pos
        if tw <= 0 or th <= 0 or bw <= 0 or bh <= 0:
            return
        scale = max(bw / float(tw), bh / float(th))
        rw, rh = tw * scale, th * scale
        rectangle.size = (rw, rh)
        rectangle.pos = (bx + (bw - rw) / 2.0, by + (bh - rh) / 2.0)

    def _game_bounds(self):
        pos = tuple(getattr(self.root, "pos", (0, 0)))
        size = tuple(getattr(self.root, "size", (0, 0)))
        if size[0] <= 0 or size[1] <= 0:
            pos = self._scene_rect_pos or tuple(self.root.deux.pos)
            size = self._scene_rect_size or tuple(self.root.deux.size)
        return pos, size

    @staticmethod
    def _key_for_state(indexa):
        for key, scene in SCENES.items():
            if indexa in scene["states"]:
                return key
        return None

    def start_intro(self, done_callback):
        if self._intro_done:
            Clock.schedule_once(lambda dt: done_callback(), 0)
            return
        self._intro_done_callback = done_callback
        chosen = random.choice(INTRO_FILES)
        path = self._resolve(chosen)
        print("[JT-INTRO] chosen={}".format(chosen), flush=True)
        if not path or CoreVideo is None:
            print("[JT-INTRO][ERROR] unavailable file/provider; continuing", flush=True)
            self._finish_intro("unavailable")
            return

        try:
            overlay = IntroOverlay(size_hint=(1, 1))
            self.root.add_widget(overlay)
            player = CoreVideo(filename=path, eos="stop", autoplay=False)
            player.volume = 1.0
            player.bind(on_frame=self._on_intro_frame, on_eos=self._on_intro_eos)
            self._intro_overlay = overlay
            self._intro_player = player
            self._intro_timeout = Clock.schedule_once(
                lambda dt: self._finish_intro("timeout"), 40.0
            )
            print("[JT-INTRO] begin={}".format(chosen), flush=True)
            player.play()
        except Exception as exc:
            print("[JT-INTRO][ERROR] {!r}; continuing".format(exc), flush=True)
            self._finish_intro("exception")

    def _on_intro_frame(self, player, *args):
        if self._intro_overlay is not None and player.texture is not None:
            self._intro_overlay.set_texture(player.texture)

    def _on_intro_eos(self, player, *args):
        self._finish_intro("eos")

    def _finish_intro(self, reason):
        if self._intro_done:
            return
        self._intro_done = True
        if self._intro_timeout is not None:
            self._intro_timeout.cancel()
            self._intro_timeout = None
        if self._intro_player is not None:
            try:
                self._intro_player.unbind(
                    on_frame=self._on_intro_frame, on_eos=self._on_intro_eos
                )
            except Exception:
                pass
            try:
                self._intro_player.unload()
            except Exception as exc:
                print("[JT-INTRO][WARN] unload={!r}".format(exc), flush=True)
            self._intro_player = None
        if self._intro_overlay is not None:
            try:
                self.root.remove_widget(self._intro_overlay)
            except Exception:
                pass
            self._intro_overlay = None
        print("[JT-INTRO] end reason={}".format(reason), flush=True)
        callback = self._intro_done_callback
        self._intro_done_callback = None
        if callback is not None:
            Clock.schedule_once(lambda dt: callback(), 0)

    def sync_scene_state(self, indexa):
        """Follow the state *after* the historical engine has transitioned."""
        if not self._intro_done:
            return
        key = self._key_for_state(indexa)
        if key == self._scene_key and self._scene_player is not None:
            # Families 2/3/4 and 5/6/7 deliberately keep one player.
            return
        if key == self._scene_failed_key and self._scene_key == key:
            return
        if key != self._scene_key:
            self._stop_scene("state={}".format(indexa), preserve_failure=False)
        if key is None:
            self._scene_failed_key = None
            return
        if self._scene_player is None:
            self._start_scene(key, indexa)

    # Backward-compatible name used by older generated main.py revisions.
    def sync_wait_state(self, indexa):
        self.sync_scene_state(indexa)

    def _start_scene(self, key, indexa):
        scene = SCENES[key]
        path = self._resolve(scene["file"])
        self._scene_key = key
        self._scene_generation += 1
        generation = self._scene_generation
        self._scene_has_frame = False
        self.root._jt_scene_video_active = False
        self.root._jt_wait_video_active = False

        if not path or CoreVideo is None:
            self._scene_failed_key = key
            print(
                "[JT-SCENE][ERROR] key={} file={} unavailable; historical frames kept".format(
                    key, scene["file"]
                ),
                flush=True,
            )
            return

        try:
            self._scene_rect_pos = tuple(self.root.deux.pos)
            self._scene_rect_size = tuple(self.root.deux.size)
            eos_policy = "loop" if scene["loop"] else "pause"
            player = CoreVideo(filename=path, eos=eos_policy, autoplay=False)
            player.volume = 0.0

            def frame_callback(bound_player, *args):
                self._on_scene_frame(bound_player, generation)

            def eos_callback(bound_player, *args):
                self._on_scene_eos(bound_player, generation)

            self._scene_frame_callback = frame_callback
            self._scene_eos_callback = eos_callback
            player.bind(on_frame=frame_callback, on_eos=eos_callback)
            self._scene_player = player
            self._scene_timeout = Clock.schedule_once(
                lambda dt: self._scene_frame_timeout(generation), 4.0
            )
            print(
                "[JT-SCENE] enter key={} state={} file={} loop={} audio=muted generation={}".format(
                    key, indexa, scene["file"], scene["loop"], generation
                ),
                flush=True,
            )
            player.play()
        except Exception as exc:
            self._scene_failed_key = key
            print(
                "[JT-SCENE][ERROR] key={} {!r}; historical frames kept".format(
                    key, exc
                ),
                flush=True,
            )
            self._stop_scene("exception", preserve_failure=True)

    def _on_scene_frame(self, player, generation):
        if (
            player is not self._scene_player
            or generation != self._scene_generation
            or self._scene_key is None
        ):
            return
        texture = player.texture
        if texture is None:
            return

        self._scene_has_frame = True
        if self._scene_timeout is not None:
            self._scene_timeout.cancel()
            self._scene_timeout = None

        self.root.deux.texture = texture
        self.root._jt_scene_video_active = True
        self.root._jt_wait_video_active = self._scene_key == "wait"
        bounds_pos, bounds_size = self._game_bounds()
        self._cover_rectangle(self.root.deux, texture, bounds_pos, bounds_size)

    def _on_scene_eos(self, player, generation):
        if player is not self._scene_player or generation != self._scene_generation:
            return
        # eos=loop handles wait; eos=pause keeps the last decoded frame.
        print(
            "[JT-SCENE] eos key={} generation={} state-machine=unchanged".format(
                self._scene_key, generation
            ),
            flush=True,
        )

    def _scene_frame_timeout(self, generation):
        if generation != self._scene_generation:
            return
        self._scene_timeout = None
        if not self._scene_has_frame:
            key = self._scene_key
            self._scene_failed_key = key
            print(
                "[JT-SCENE][ERROR] key={} no frame after 4s; historical frames restored".format(
                    key
                ),
                flush=True,
            )
            self._stop_scene("no-frame", preserve_failure=True)

    def _stop_scene(self, reason, preserve_failure=False):
        key = self._scene_key
        self._scene_generation += 1
        if self._scene_timeout is not None:
            self._scene_timeout.cancel()
            self._scene_timeout = None

        player = self._scene_player
        frame_callback = self._scene_frame_callback
        eos_callback = self._scene_eos_callback
        self._scene_player = None
        self._scene_frame_callback = None
        self._scene_eos_callback = None

        self.root._jt_scene_video_active = False
        self.root._jt_wait_video_active = False
        self._scene_has_frame = False

        if player is not None:
            try:
                if frame_callback is not None:
                    player.unbind(on_frame=frame_callback)
                if eos_callback is not None:
                    player.unbind(on_eos=eos_callback)
            except Exception:
                pass
            try:
                player.unload()
            except Exception as exc:
                print("[JT-SCENE][WARN] unload={!r}".format(exc), flush=True)

        # Restore geometry before historical JPEG rendering resumes.
        if self._scene_rect_pos is not None:
            self.root.deux.pos = self._scene_rect_pos
        if self._scene_rect_size is not None:
            self.root.deux.size = self._scene_rect_size
        self._scene_rect_pos = None
        self._scene_rect_size = None

        self._scene_key = key if preserve_failure else None
        if not preserve_failure:
            self._scene_failed_key = None
        print(
            "[JT-SCENE] exit key={} reason={} generation={}".format(
                key, reason, self._scene_generation
            ),
            flush=True,
        )

    def on_pause(self):
        player = self._intro_player or self._scene_player
        self._paused_player = None
        if player is not None and getattr(player, "state", "") == "playing":
            try:
                player.pause()
                self._paused_player = player
                print("[JT-MEDIA] pause", flush=True)
            except Exception as exc:
                print("[JT-MEDIA][WARN] pause={!r}".format(exc), flush=True)

    def on_resume(self):
        player = self._paused_player
        self._paused_player = None
        if player is not None:
            try:
                player.play()
                print("[JT-MEDIA] resume", flush=True)
            except Exception as exc:
                print("[JT-MEDIA][WARN] resume={!r}".format(exc), flush=True)

    def shutdown(self):
        if not self._intro_done:
            self._finish_intro("shutdown")
        self._stop_scene("shutdown", preserve_failure=False)
