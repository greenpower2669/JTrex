"""Kivy video integration for June T-Rex.

Gameplay stays in the historical main.py. This module owns only the random
launch intro and the visual wait-loop replacement.
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
WAIT_FILE = "assets/combat/StegVsTrexvaetviensremolace.mp4"


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
        self._wait_player = None
        self._wait_timeout = None
        self._wait_has_frame = False
        self._wait_rect_pos = None
        self._wait_rect_size = None
        self._paused_player = None
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
    def _fit_rectangle(rectangle, texture, bounds_pos, bounds_size):
        tw, th = texture.size
        bw, bh = bounds_size
        bx, by = bounds_pos
        if tw <= 0 or th <= 0 or bw <= 0 or bh <= 0:
            return
        scale = min(bw / float(tw), bh / float(th))
        rw, rh = tw * scale, th * scale
        rectangle.size = (rw, rh)
        rectangle.pos = (bx + (bw - rw) / 2.0, by + (bh - rh) / 2.0)

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
                lambda dt: self._finish_intro("timeout"), 20.0
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

    def sync_wait_state(self, indexa):
        if not self._intro_done:
            return
        if indexa == 1:
            if self._wait_player is None and not self.root._jt_wait_video_active:
                self._start_wait_video()
        elif self._wait_player is not None or self.root._jt_wait_video_active:
            self._stop_wait_video("state={}".format(indexa))

    def _start_wait_video(self):
        path = self._resolve(WAIT_FILE)
        if not path or CoreVideo is None:
            print("[JT-WAIT][ERROR] video/provider unavailable; historical frames kept", flush=True)
            self.root._jt_wait_video_active = False
            return
        try:
            self._wait_has_frame = False
            self._wait_rect_pos = tuple(self.root.deux.pos)
            self._wait_rect_size = tuple(self.root.deux.size)
            self.root._jt_wait_video_active = True
            player = CoreVideo(filename=path, eos="loop", autoplay=False)
            player.volume = 0.0
            player.bind(on_frame=self._on_wait_frame)
            self._wait_player = player
            self._wait_timeout = Clock.schedule_once(self._wait_frame_timeout, 4.0)
            print("[JT-WAIT] enter={} audio=muted".format(WAIT_FILE), flush=True)
            player.play()
        except Exception as exc:
            print("[JT-WAIT][ERROR] {!r}; historical frames kept".format(exc), flush=True)
            self._stop_wait_video("exception")

    def _on_wait_frame(self, player, *args):
        texture = player.texture
        if texture is None:
            return
        self._wait_has_frame = True
        if self._wait_timeout is not None:
            self._wait_timeout.cancel()
            self._wait_timeout = None
        self.root.deux.texture = texture
        if self._wait_rect_pos is not None and self._wait_rect_size is not None:
            self._fit_rectangle(
                self.root.deux, texture, self._wait_rect_pos, self._wait_rect_size
            )

    def _wait_frame_timeout(self, dt):
        self._wait_timeout = None
        if not self._wait_has_frame:
            print("[JT-WAIT][ERROR] no frame after 4s; historical frames restored", flush=True)
            self._stop_wait_video("no-frame")

    def _stop_wait_video(self, reason):
        if self._wait_timeout is not None:
            self._wait_timeout.cancel()
            self._wait_timeout = None
        player = self._wait_player
        self._wait_player = None
        self.root._jt_wait_video_active = False
        self._wait_has_frame = False
        if player is not None:
            try:
                player.unbind(on_frame=self._on_wait_frame)
            except Exception:
                pass
            try:
                player.unload()
            except Exception as exc:
                print("[JT-WAIT][WARN] unload={!r}".format(exc), flush=True)
        if self._wait_rect_pos is not None:
            self.root.deux.pos = self._wait_rect_pos
        if self._wait_rect_size is not None:
            self.root.deux.size = self._wait_rect_size
        self._wait_rect_pos = None
        self._wait_rect_size = None
        print("[JT-WAIT] exit reason={}".format(reason), flush=True)

    def on_pause(self):
        player = self._intro_player or self._wait_player
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
        self._stop_wait_video("shutdown")
