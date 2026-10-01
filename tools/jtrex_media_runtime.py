"""Kivy video integration for June T-Rex.

Gameplay stays in the historical main.py. This module owns launch intros and
audiovisual replacements for selected combat scenes. Video EOS never changes the
historical state machine.
"""

import random
import time
from pathlib import Path

from kivy.clock import Clock
from kivy.core.video import Video as CoreVideo
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.metrics import dp
from kivy.resources import resource_find
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
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
        "file": "assets/combat/Chargestegtrexchargerougebleucorrected.mp4",
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
    "power-stsf": {
        "states": frozenset((21,)),
        "file": "assets/powers/stsf-sanctuary-force.mp4",
        "loop": False,
        "play_to_end": True,
    },
    "power-stls": {
        "states": frozenset((22,)),
        "file": "assets/powers/stls-lifestream.mp4",
        "loop": False,
        "play_to_end": True,
    },
    "power-stta": {
        "states": frozenset((23,)),
        "file": "assets/powers/stta-tornado-attack.mp4",
        "loop": False,
        "play_to_end": True,
    },
    "power-trfs": {
        "states": frozenset((24,)),
        "file": "assets/powers/trfs-fire-storm.mp4",
        "loop": False,
        "play_to_end": True,
    },
    "power-trph": {
        "states": frozenset((25,)),
        "file": "assets/powers/trph-phoenix-attack.mp4",
        "loop": False,
        "play_to_end": True,
    },
    "power-trma": {
        "states": frozenset((26,)),
        "file": "assets/powers/trma-meteor-attack.mp4",
        "loop": False,
        "play_to_end": True,
    },
    "finish-st": {
        "states": frozenset((10,)),
        "file": "assets/finishing/steg-finishing-trex.mp4",
        "loop": False,
        "play_to_end": True,
    },
    "finish-tr": {
        "states": frozenset((11,)),
        "file": "assets/finishing/trex-finishing-steg.mp4",
        "loop": False,
        "play_to_end": True,
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
        self._scene_state = None
        self._scene_generation = 0
        self._scene_has_frame = False
        self._scene_audio_native = False
        self._scene_eos_reached = False
        self._scene_timeout = None
        self._scene_frame_callback = None
        self._scene_eos_callback = None
        self._scene_failed_key = None
        self._scene_rect_pos = None
        self._scene_rect_size = None
        self._paused_player = None
        self._engine_state = None
        self._legacy_names = {}
        self._legacy_lengths = {}
        self._legacy_genres = {}
        self._legacy_sounds = {}
        self._admin_tap_count = 0
        self._admin_tap_deadline = 0.0
        self._admin_popup = None
        self._admin_label = None
        self._admin_refresh_event = None
        self._admin_enabled = False
        self._indicator_phase = False

        self.root._jt_scene_video_active = False
        self.root._jt_scene_cinematic_lock = False
        # Compatibility with the first wait-only integration.
        self.root._jt_wait_video_active = False

        self._status_dot = Widget(
            size_hint=(None, None),
            size=(dp(18), dp(18)),
            pos=(dp(8), dp(8)),
        )
        with self._status_dot.canvas:
            self._status_dot_color = Color(1, 0, 0, 0)
            self._status_dot_shape = Ellipse(
                pos=self._status_dot.pos, size=self._status_dot.size
            )
        self._status_dot.bind(pos=self._layout_status_dot, size=self._layout_status_dot)
        self.root.add_widget(self._status_dot)
        self._status_label = Label(
            text="",
            size_hint=(None, None),
            size=(dp(300), dp(32)),
            pos=(dp(6), dp(29)),
            font_size=dp(16),
            halign="left",
            valign="middle",
            opacity=0,
        )
        self._status_label.text_size = self._status_label.size
        self.root.add_widget(self._status_label)
        self._indicator_event = Clock.schedule_interval(
            self._update_status_indicator, 0.35
        )
        Window.bind(on_touch_down=self._on_admin_trigger)

        provider = getattr(CoreVideo, "__module__", repr(CoreVideo))
        print("[JT-MEDIA] video provider={}".format(provider), flush=True)

    def set_legacy_catalog(self, names, lengths, genres, sounds):
        self._legacy_names = dict(names)
        self._legacy_lengths = dict(lengths)
        self._legacy_genres = dict(genres)
        self._legacy_sounds = dict(sounds)
        print(
            "[JT-ADMIN] legacy catalog states={}".format(
                sorted(self._legacy_names)
            ),
            flush=True,
        )

    def _layout_status_dot(self, *args):
        self._status_dot_shape.pos = self._status_dot.pos
        self._status_dot_shape.size = self._status_dot.size

    def _update_status_indicator(self, dt):
        if not self._intro_done or not self._admin_enabled:
            self._status_dot_color.rgba = (1, 0, 0, 0)
            self._status_label.text = ""
            self._status_label.opacity = 0
            return
        self._indicator_phase = not self._indicator_phase
        alpha = 1.0 if self._indicator_phase else 0.22
        video_active = bool(getattr(self.root, "_jt_scene_video_active", False))
        if video_active:
            self._status_dot_color.rgba = (0.0, 1.0, 0.0, alpha)
            self._status_label.text = ""
            self._status_label.opacity = 0
        else:
            self._status_dot_color.rgba = (1.0, 0.0, 0.0, alpha)
            if self._admin_enabled:
                prefix = self._legacy_names.get(self._engine_state, "")
                directory = self._legacy_directory(prefix) if prefix else "LEGACY"
                self._status_label.text = directory
                self._status_label.opacity = 1
            else:
                self._status_label.text = ""
                self._status_label.opacity = 0

    def _on_admin_trigger(self, window, touch):
        if self._admin_popup is not None:
            return False
        width, height = Window.size
        if width <= 0 or height <= 0:
            return False
        in_corner = touch.x >= width * 0.88 and touch.y <= height * 0.12
        if not in_corner:
            self._admin_tap_count = 0
            self._admin_tap_deadline = 0.0
            return False
        now = time.monotonic()
        if now > self._admin_tap_deadline:
            self._admin_tap_count = 0
        self._admin_tap_count += 1
        self._admin_tap_deadline = now + 10.0
        if self._admin_tap_count >= 20:
            self._admin_tap_count = 0
            self._admin_tap_deadline = 0.0
            self._admin_enabled = True
            print("[JT-ADMIN] 20-tap mode enabled", flush=True)
            Clock.schedule_once(lambda dt: self._open_admin(), 0)
        return False

    @staticmethod
    def _legacy_directory(prefix):
        if not prefix:
            return "(aucun)"
        if "/" not in prefix:
            return prefix
        return prefix.rsplit("/", 1)[0] + "/"

    def _admin_status_text(self):
        current = self._engine_state
        actual_video = bool(getattr(self.root, "_jt_scene_video_active", False))
        lines = [
            "JUNE T-REX — ADMIN MEDIA",
            "MODE 20 TOUCHES : ACTIF",
            "Voyant jeu : VERT = vraie video / ROUGE = animation historique",
            "ROUGE : le repertoire legacy est affiche au-dessus du voyant",
            "",
            "ETAT ACTUEL : indexa={}  MODE={}".format(
                current, "VIDEO MP4" if actual_video else "LEGACY / FALLBACK"
            ),
            "",
        ]
        catalog_states = set(self._legacy_names)
        for scene in SCENES.values():
            catalog_states.update(scene["states"])
        for state in sorted(catalog_states):
            key = self._key_for_state(state)
            legacy_prefix = self._legacy_names.get(state, "")
            legacy_dir = self._legacy_directory(legacy_prefix)
            sound = self._legacy_sounds.get(state, "(aucun)")
            length = self._legacy_lengths.get(state, "?")
            genre = self._legacy_genres.get(state, "?")
            marker = ">> " if state == current else "   "
            if key is None:
                lines.append(
                    "{}indexa {:>2} | LEGACY | video=NON RACCORDEE".format(
                        marker, state
                    )
                )
                lines.append(
                    "      dossier={}  prefix={}  frames={}  mode={}  son={}".format(
                        legacy_dir, legacy_prefix or "(aucun)", length, genre, sound
                    )
                )
                continue
            scene = SCENES[key]
            video_file = scene["file"]
            video_present = bool(self._resolve(video_file))
            if state == current:
                mode = "VIDEO ACTIVE" if actual_video else "LEGACY / FALLBACK"
            else:
                mode = "VIDEO DISPONIBLE" if video_present else "VIDEO MANQUANTE"
            lines.append(
                "{}indexa {:>2} | {} | mp4={}".format(
                    marker, state, mode, "OUI" if video_present else "NON"
                )
            )
            lines.append("      video={}".format(video_file))
            lines.append(
                "      fallback={}  prefix={}  frames={}  mode={}  son={}".format(
                    legacy_dir, legacy_prefix or "(aucun)", length, genre, sound
                )
            )
        return "\n".join(lines)

    def _refresh_admin(self, dt=0):
        if self._admin_label is not None:
            self._admin_label.text = self._admin_status_text()

    def _open_admin(self):
        if self._admin_popup is not None:
            return
        label = Label(
            text=self._admin_status_text(),
            size_hint_y=None,
            font_size=dp(18),
            halign="left",
            valign="top",
        )
        label.bind(
            width=lambda instance, value: setattr(
                instance, "text_size", (value, None)
            )
        )
        label.bind(
            texture_size=lambda instance, value: setattr(
                instance, "height", value[1] + dp(24)
            )
        )
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(label)
        close_button = Button(
            text="FERMER",
            size_hint=(1, None),
            height=dp(58),
            font_size=dp(20),
        )
        content = BoxLayout(orientation="vertical", spacing=dp(8), padding=dp(8))
        content.add_widget(scroll)
        content.add_widget(close_button)
        popup = Popup(
            title="ADMIN MEDIA — diagnostic uniquement",
            content=content,
            size_hint=(0.96, 0.94),
            auto_dismiss=True,
        )
        self._admin_popup = popup
        self._admin_label = label
        close_button.bind(on_release=lambda *args: popup.dismiss())
        popup.bind(on_dismiss=self._on_admin_dismiss)
        self._admin_refresh_event = Clock.schedule_interval(
            self._refresh_admin, 0.5
        )
        print(
            "[JT-ADMIN] open state={} video_active={}".format(
                self._engine_state,
                bool(getattr(self.root, "_jt_scene_video_active", False)),
            ),
            flush=True,
        )
        popup.open()

    def _on_admin_dismiss(self, *args):
        if self._admin_refresh_event is not None:
            self._admin_refresh_event.cancel()
            self._admin_refresh_event = None
        self._admin_popup = None
        self._admin_label = None
        print("[JT-ADMIN] close", flush=True)

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
        self._engine_state = indexa
        key = self._key_for_state(indexa)

        if self._scene_player is not None and self._scene_key is not None:
            current_scene = SCENES[self._scene_key]
            if (
                current_scene.get("play_to_end", False)
                and not self._scene_eos_reached
                and indexa not in current_scene["states"]
            ):
                texture = self._scene_player.texture
                if texture is not None and self.root._jt_scene_video_active:
                    bounds_pos, bounds_size = self._game_bounds()
                    self._cover_rectangle(
                        self.root.deux, texture, bounds_pos, bounds_size
                    )
                return

        if key == self._scene_key and self._scene_player is not None:
            self._scene_state = indexa
            # Families 2/3/4 and 5/6/7 deliberately keep one player.
            # Re-apply aspect-fill even after EOS/pause if the viewport changed.
            texture = self._scene_player.texture
            if texture is not None and self.root._jt_scene_video_active:
                bounds_pos, bounds_size = self._game_bounds()
                self._cover_rectangle(
                    self.root.deux, texture, bounds_pos, bounds_size
                )
            return
        if key == self._scene_failed_key and self._scene_key == key:
            return
        if key != self._scene_key:
            self._stop_scene("state={}".format(indexa), preserve_failure=False)
        self._scene_state = indexa
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
        self._scene_audio_native = False
        self._scene_eos_reached = False
        self.root._jt_scene_video_active = False
        self.root._jt_scene_cinematic_lock = False
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
            if scene["loop"]:
                eos_policy = "loop"
            elif scene.get("play_to_end", False):
                eos_policy = "stop"
            else:
                eos_policy = "pause"
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
            self.root._jt_scene_cinematic_lock = bool(
                scene.get("play_to_end", False)
            )
            self._scene_timeout = Clock.schedule_once(
                lambda dt: self._scene_frame_timeout(generation), 4.0
            )
            print(
                "[JT-SCENE] enter key={} state={} file={} loop={} play_to_end={} audio=pending-first-frame generation={}".format(
                    key,
                    indexa,
                    scene["file"],
                    scene["loop"],
                    scene.get("play_to_end", False),
                    generation,
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

        first_frame = not self._scene_has_frame
        self._scene_has_frame = True
        if self._scene_timeout is not None:
            self._scene_timeout.cancel()
            self._scene_timeout = None

        self.root.deux.texture = texture
        self.root._jt_scene_video_active = True
        self.root._jt_wait_video_active = self._scene_key == "wait"

        if first_frame:
            callback = getattr(self.app, "_jt_set_native_scene_audio", None)
            if callback is not None:
                try:
                    callback(True, self._scene_state)
                except Exception as exc:
                    print(
                        "[JT-SCENE][WARN] AUDIO_LEGACY suppress state={} error={!r}".format(
                            self._scene_state, exc
                        ),
                        flush=True,
                    )
            try:
                player.volume = 1.0
                self._scene_audio_native = True
                print(
                    "[JT-SCENE] AUDIO_NATIVE enabled key={} state={} generation={}".format(
                        self._scene_key, self._scene_state, generation
                    ),
                    flush=True,
                )
            except Exception as exc:
                self._scene_audio_native = False
                if callback is not None:
                    try:
                        callback(False, self._scene_state)
                    except Exception:
                        pass
                print(
                    "[JT-SCENE][ERROR] AUDIO_NATIVE unavailable key={} state={} error={!r}".format(
                        self._scene_key, self._scene_state, exc
                    ),
                    flush=True,
                )

        bounds_pos, bounds_size = self._game_bounds()
        self._cover_rectangle(self.root.deux, texture, bounds_pos, bounds_size)

    def _on_scene_eos(self, player, generation):
        if player is not self._scene_player or generation != self._scene_generation:
            return
        self._scene_eos_reached = True
        key = self._scene_key
        scene = SCENES.get(key, {})
        print(
            "[JT-SCENE] eos key={} generation={} play_to_end={} state-machine=unchanged".format(
                key, generation, scene.get("play_to_end", False)
            ),
            flush=True,
        )
        if scene.get("play_to_end", False):
            engine_state = self._engine_state
            self._stop_scene("eos-complete", preserve_failure=False)
            if engine_state is not None:
                Clock.schedule_once(
                    lambda dt, state=engine_state: self.sync_scene_state(state), 0
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
        state = self._scene_state
        audio_native = self._scene_audio_native
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
        self.root._jt_scene_cinematic_lock = False
        self._scene_has_frame = False
        self._scene_eos_reached = False

        if player is not None:
            try:
                player.volume = 0.0
            except Exception:
                pass
            try:
                player.stop()
            except Exception:
                pass
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

        if audio_native:
            if preserve_failure:
                callback = getattr(self.app, "_jt_set_native_scene_audio", None)
                if callback is not None:
                    try:
                        callback(False, state)
                    except Exception as exc:
                        print(
                            "[JT-SCENE][WARN] AUDIO_LEGACY fallback state={} error={!r}".format(
                                state, exc
                            ),
                            flush=True,
                        )
                print(
                    "[JT-SCENE] AUDIO_LEGACY fallback key={} state={}".format(
                        key, state
                    ),
                    flush=True,
                )
            else:
                print(
                    "[JT-SCENE] AUDIO_STOP key={} state={} reason={}".format(
                        key, state, reason
                    ),
                    flush=True,
                )
        self._scene_audio_native = False

        # Restore geometry before historical JPEG rendering resumes.
        if self._scene_rect_pos is not None:
            self.root.deux.pos = self._scene_rect_pos
        if self._scene_rect_size is not None:
            self.root.deux.size = self._scene_rect_size
        self._scene_rect_pos = None
        self._scene_rect_size = None

        self._scene_key = key if preserve_failure else None
        self._scene_state = state if preserve_failure else None
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
        if self._admin_popup is not None:
            try:
                self._admin_popup.dismiss()
            except Exception:
                pass
        try:
            Window.unbind(on_touch_down=self._on_admin_trigger)
        except Exception:
            pass
        if self._indicator_event is not None:
            self._indicator_event.cancel()
            self._indicator_event = None
        if self._status_dot is not None:
            try:
                self.root.remove_widget(self._status_dot)
            except Exception:
                pass
            self._status_dot = None
        if self._status_label is not None:
            try:
                self.root.remove_widget(self._status_label)
            except Exception:
                pass
            self._status_label = None
        if not self._intro_done:
            self._finish_intro("shutdown")
        self._stop_scene("shutdown", preserve_failure=False)
