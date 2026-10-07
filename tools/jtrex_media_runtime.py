"""Kivy video integration for June T-Rex.

Gameplay stays in the historical main.py. This module owns launch intros and
audiovisual replacements for selected combat scenes. Video EOS never changes the
historical state machine.
"""

import random
import tempfile
import time
from pathlib import Path

from kivy.clock import Clock
from kivy.core.video import Video as CoreVideo
from kivy.core.image import Image as CoreImage
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.metrics import dp
from kivy.resources import resource_find
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from jtrex_phase_runtime import JTPhaseController
from jtrex_sets_runtime import (
    CATALOG_PATH, JTSetSessionManager, POWER_KEYS, SetContractError,
)
from jtrex_sets_io import JTSetStorage
from jtrex_sets_admin import JTSetAdminService
from jtrex_sets_preview import JTSetPreviewController
from jtrex_sets_android import AndroidDocumentPicker, JTAsyncEgress, JTAsyncIngress


SCENE_SPECS = {
    "wait": {"states": frozenset((1,)), "media_role": "orbs_background", "loop": True},
    "charge": {"states": frozenset((2, 3, 4)), "media_role": "charge_red_blue", "loop": False},
    "yellow": {"states": frozenset((5, 6, 7)), "media_role": "charge_yellow", "loop": False},
    "zero-win": {"states": frozenset((-7,)), "media_role": "verdict_draw", "loop": False},
    "st-win": {"states": frozenset((8,)), "media_role": "verdict_left", "loop": False},
    "tr-win": {"states": frozenset((9,)), "media_role": "verdict_right", "loop": False},
    "power-stsf": {"states": frozenset((21,)), "power_key": "left_1", "loop": False, "play_to_end": True},
    "power-stls": {"states": frozenset((22,)), "power_key": "left_2", "loop": False, "play_to_end": True},
    "power-stta": {"states": frozenset((23,)), "power_key": "left_3", "loop": False, "play_to_end": True},
    "power-trfs": {"states": frozenset((24,)), "power_key": "right_1", "loop": False, "play_to_end": True},
    "power-trph": {"states": frozenset((25,)), "power_key": "right_2", "loop": False, "play_to_end": True},
    "power-trma": {"states": frozenset((26,)), "power_key": "right_3", "loop": False, "play_to_end": True},
    "finish-st": {"states": frozenset((10,)), "media_role": "finishing_left", "loop": False, "play_to_end": True},
    "finish-tr": {"states": frozenset((11,)), "media_role": "finishing_right", "loop": False, "play_to_end": True},
}


POWER_SCENE_KEYS = frozenset((
    "power-stsf", "power-stls", "power-stta",
    "power-trfs", "power-trph", "power-trma",
))
FINISH_SCENE_KEYS = frozenset(("finish-st", "finish-tr"))
MP4_ONLY_STATES = frozenset((1,2,3,4,5,6,7,8,9,10,11,21,22,23,24,25,26))


class WorkshopPreviewSurface(Widget):
    """Large aspect-fit surface for admin previews; never connected to gameplay."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._texture_size = None
        with self.canvas:
            Color(0, 0, 0, 1)
            self._background = Rectangle(pos=self.pos, size=self.size)
            Color(1, 1, 1, 1)
            self._preview = Rectangle(pos=self.pos, size=(0, 0))
        self.bind(pos=self._layout, size=self._layout)

    def set_texture(self, texture):
        self._preview.texture = texture
        self._texture_size = texture.size if texture is not None else None
        self._layout()

    def _layout(self, *args):
        self._background.pos = self.pos
        self._background.size = self.size
        if not self._texture_size:
            self._preview.pos = self.pos
            self._preview.size = (0, 0)
            return
        tw, th = self._texture_size
        ww, wh = self.size
        if tw <= 0 or th <= 0 or ww <= 0 or wh <= 0:
            return
        scale = min(ww / float(tw), wh / float(th))
        rw, rh = tw * scale, th * scale
        self._preview.size = (rw, rh)
        self._preview.pos = (self.x + (ww-rw)/2.0, self.y + (wh-rh)/2.0)


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


class RoundOverlay(Widget):
    """ROUND followed by a rendered START animation; completion releases play."""
    def __init__(self, media, number, token, **kwargs):
        super().__init__(**kwargs)
        self.media, self.token = media, token
        self.stage, self.elapsed = "ROUND", 0.0
        self.shadow = Label(text="ROUND {}".format(number), bold=True, color=(0, 0, 0, .9))
        self.title = Label(text=self.shadow.text, bold=True, color=(1, .9, .05, 1))
        self.add_widget(self.shadow)
        self.add_widget(self.title)
        self.bind(size=self._layout, pos=self._layout)
        self._layout()
        self.event = Clock.schedule_interval(self._tick, 1.0 / 60.0)

    def _layout(self, *args):
        self.title.pos, self.title.size = self.pos, self.size
        self.shadow.pos = (self.x + dp(4), self.y - dp(4))
        self.shadow.size = self.size
        self._font = min(self.width * .16, self.height * .32)
        self.title.font_size = self.shadow.font_size = self._font * .55

    def _tick(self, dt):
        phase = self.media.phases
        if phase is None or phase.paused:
            return
        # A delayed UI frame must not skip the visible presentation entirely.
        self.elapsed += min(max(dt, 0), .1)
        if self.stage == "ROUND":
            if self.elapsed < 1.0:
                return
            self.stage, self.elapsed = "START", 0.0
            self.title.text = self.shadow.text = "START!"
            print("[JT-ROUND] START animation round={} token={}".format(phase.round_number, self.token), flush=True)
        progress = min(self.elapsed / 1.1, 1.0)
        if progress < .3:
            t = progress / .3 - 1
            # Back easing gives START a short overshoot without flashing.
            scale = .45 + .55 * (1 + 2.70158*t*t*t + 1.70158*t*t)
        else:
            scale = 1.0 + .12 * max(0, (progress - .75) / .25)
        self.title.font_size = self.shadow.font_size = self._font * scale
        alpha = 1.0 if progress < .75 else max(0, (1-progress)/.25)
        self.title.opacity = self.shadow.opacity = alpha
        if progress >= 1:
            phase.finish_start(self.token)

    def close(self):
        self.event.cancel()


class JTMediaController:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        raw_state_root = getattr(app, "user_data_dir", None)
        state_root = Path(raw_state_root) if raw_state_root else (
            Path(tempfile.gettempdir()) / "jtrex-user-data-{}".format(id(app))
        )
        catalog_physical = self._resolve(CATALOG_PATH)
        official_root = (
            Path(catalog_physical).resolve().parents[2]
            if catalog_physical else Path.cwd().resolve()
        )
        storage_root = state_root.resolve(strict=False)
        if (
            storage_root == official_root
            or storage_root in official_root.parents
            or official_root in storage_root.parents
        ):
            storage_root = Path(tempfile.gettempdir()) / "jtrex-set-storage-{}".format(id(app))
        self._state_root = state_root
        self._set_storage = JTSetStorage(
            official_root, storage_root / "jt-user-sets", storage_root / "jt-set-drafts"
        )
        self.sets = JTSetSessionManager(
            self._resolve, state_root / "jt-set-selection.json",
            user_catalog_provider=self._set_storage.promoted_catalog,
        )
        self._official_set_ids = frozenset(
            selection.set_id for selection in self.sets.official_catalog()
        )
        self._set_admin = JTSetAdminService(self._set_storage, self._official_set_ids)
        image_cls = globals().get("CoreImage")
        sound_loader = globals().get("SoundLoader")
        self._set_preview = JTSetPreviewController(
            self.root, CoreVideo, Clock,
            image_loader=(lambda path: image_cls(path)) if image_cls is not None else None,
            sound_loader=(lambda path: sound_loader.load(path)) if sound_loader is not None else None,
        )
        self._set_picker = AndroidDocumentPicker()
        self._set_ingress = JTAsyncIngress(self._set_storage, Clock)
        self._set_egress = JTAsyncEgress(Clock)
        self._workshop_draft_id = None
        self._workshop_popup = None
        self._workshop_editor_popup = None
        self._workshop_editor_label = None
        self._workshop_editor_scroll = None
        self._workshop_progress_label = None
        self._workshop_resume_scroll = None
        self._workshop_menu_scroll = None
        self._workshop_create_scroll = None
        self._workshop_preview_popup = None
        self._workshop_preview_surface = None
        self._workshop_preview_label = None
        self._workshop_preview_event = None
        self._workshop_parameter_popup = None
        self._workshop_parameter_labels = {}
        self._workshop_buttons = {}
        self._workshop_status = ""
        self.selection = self.sets.runtime_set
        self._phase_name = "INTRO"
        self._set_popup = None
        self._set_option_buttons = []
        self._set_selector_scroll = None
        self._draft_test_return_callback = None
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
        self._wait_resume_fraction = 0.0
        self._wait_seek_pending = False
        self._paused_player = None
        self._engine_state = None
        self._engine = None
        self.phases = None
        self._round_overlay = None
        self._scene_completed_key = None
        self._legacy_names = {}
        self._legacy_lengths = {}
        self._legacy_genres = {}
        self._legacy_sounds = {}
        self._admin_tap_count = 0
        self._admin_tap_deadline = 0.0
        self._admin_popup = None
        self._admin_label = None
        self._admin_workshop_button = None
        self._admin_refresh_event = None
        self._admin_enabled = False
        self._indicator_phase = False
        self._menu_right_dino_event = None

        self.root._jt_scene_video_active = False
        self.root._jt_scene_cinematic_lock = False
        self.root._jt_power_video_hold = False
        self.root._jt_finishing_video_hold = False
        self.root._jt_finishing_complete_pending = None
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
        self._set_button = Button(
            text="",
            size_hint=(None, None),
            size=(dp(220), dp(40)),
            font_size=dp(15),
            opacity=0,
            disabled=True,
        )
        self._set_button.bind(on_release=lambda *args: self._open_set_selector())
        self.root.add_widget(self._set_button)
        self._set_edit_button = Button(
            text="MOD",
            size_hint=(None, None),
            size=(dp(48), dp(40)),
            font_size=dp(13),
            opacity=0,
            disabled=True,
        )
        self._set_edit_button.bind(on_release=lambda *args: self._quick_edit_selected_set())
        self.root.add_widget(self._set_edit_button)
        self.root.bind(size=self._layout_set_button, pos=self._layout_set_button)
        self._layout_set_button()
        self._refresh_set_button()
        self._indicator_event = Clock.schedule_interval(
            self._update_status_indicator, 0.35
        )
        self._menu_right_dino_event = Clock.schedule_interval(
            self._guard_menu_right_dinosaur_crop, 0.05
        )
        Window.bind(on_touch_down=self._on_admin_trigger)

        provider = getattr(CoreVideo, "__module__", repr(CoreVideo))
        print("[JT-MEDIA] video provider={}".format(provider), flush=True)

    def set_engine(self, engine):
        self._engine = engine
        self.phases = JTPhaseController(self, engine, Clock, Rectangle, Label)
        engine['_JT_PHASES'] = self.phases
        if self.sets.session_active:
            self._apply_session_power_identity()
        self.phases.sync()

    def _session_power_path_table(self):
        selection = self.sets.session_set
        table = {}
        for slot, power_key in enumerate(POWER_KEYS, 1):
            logical = selection.power_paths(power_key)
            table[slot] = {
                name: (
                    None if relative is None
                    else (selection.resolve_path(relative) or relative)
                )
                for name, relative in logical.items()
            }
        return table

    def _session_power_parameter_table(self):
        selection = self.sets.session_set
        return {
            slot: selection.power_effect_fraction(power_key)
            for slot, power_key in enumerate(POWER_KEYS, 1)
        }

    def _apply_session_power_identity(self):
        if self._engine is None or not self.sets.session_active:
            return
        path_callback = self._engine.get('jt_apply_power_paths')
        if path_callback is not None:
            path_callback(self._session_power_path_table())
        parameter_callback = self._engine.get('jt_apply_power_parameters')
        if parameter_callback is not None:
            parameter_callback(self._session_power_parameter_table())
        print(
            "[JT-SET] power identity session={}".format(self.sets.session_set.set_id),
            flush=True,
        )

    def _guard_menu_right_dinosaur_crop(self, dt=0):
        """Keep the intentionally cropped right selection dinosaur edge off-screen."""
        if self._phase_name != "MENU":
            return
        try:
            root_x = float(getattr(self.root, "x", 0.0))
            root_width = float(getattr(self.root, "width", 0.0))
        except (TypeError, ValueError):
            return
        if root_width <= 0:
            return
        screen_right = root_x + root_width
        visible_threshold = root_x + root_width * 0.78
        candidates = []
        for name in ("jh", "jb"):
            rect = getattr(self.root, name, None)
            if rect is None:
                continue
            try:
                x, y = rect.pos
                width, height = rect.size
                x, y = float(x), float(y)
                width, height = float(width), float(height)
            except (AttributeError, TypeError, ValueError):
                continue
            if width <= 0 or height <= 0:
                continue
            right_edge = x + width
            if right_edge < visible_threshold:
                continue
            candidates.append((x, rect, width, y))
        if not candidates:
            return
        x, rect, width, y = max(candidates, key=lambda item: item[0])
        safety = min(dp(44), max(dp(18), width * 0.08))
        minimum_x = screen_right + safety - width
        if x < minimum_x:
            rect.pos = (minimum_x, y)

    def _layout_set_button(self, *args):
        root_width = float(getattr(self.root, "width", dp(520)))
        root_height = float(getattr(self.root, "height", dp(100)))
        width = min(dp(240), max(dp(150), root_width * 0.26))
        height = dp(40)
        edit_visible = bool(self._admin_enabled)
        edit_width = dp(48) if edit_visible else 0.0
        gap = dp(6) if edit_visible else 0.0
        group_width = width + gap + edit_width
        x = max(dp(8), (root_width - group_width) / 2.0)
        y = max(dp(8), root_height - dp(50))
        self._set_button.size = (width, height)
        self._set_button.pos = (x, y)
        self._set_edit_button.size = (dp(48), height)
        self._set_edit_button.pos = (x + width + gap, y)

    def _refresh_set_button(self):
        selected = self.sets.selected_set
        self._set_button.text = "SET v  {}".format(selected.display_name)

    def _set_selector_visible(self, visible):
        visible = bool(visible)
        self._set_button.opacity = 1 if visible else 0
        self._set_button.disabled = not visible
        edit_visible = visible and self._admin_enabled
        self._set_edit_button.opacity = 1 if edit_visible else 0
        self._set_edit_button.disabled = not edit_visible
        self._layout_set_button()
        if not visible and self._set_popup is not None:
            try:
                self._set_popup.dismiss()
            except Exception:
                pass
            self._set_popup = None
            self._set_option_buttons = []
            self._set_selector_scroll = None

    def _invalidate_set_media(self):
        self._stop_scene("set-change", preserve_failure=False)
        self._wait_resume_fraction = 0.0
        self._wait_seek_pending = False
        self._scene_completed_key = None
        self._scene_failed_key = None
        self._paused_player = None
        self.root._jt_finishing_complete_pending = None

    def on_phase_changed(self, name):
        self._phase_name = name
        if name == "MENU":
            was_temporary = self.sets.session_temporary
            return_callback = self._draft_test_return_callback if was_temporary else None
            if was_temporary:
                self._invalidate_set_media()
            if self.sets.session_active:
                self.sets.end_session()
            self.selection = self.sets.selected_set
            self._refresh_set_button()
            self._set_selector_visible(True)
            if was_temporary:
                self._draft_test_return_callback = None
                if return_callback is not None:
                    Clock.schedule_once(lambda dt, cb=return_callback: cb(), 0)
            return
        self._set_selector_visible(False)
        if name != "INTRO" and not self.sets.session_active:
            self.selection = self.sets.begin_session()
            self._apply_session_power_identity()


    def start_draft_test(self, selection, return_callback=None):
        if self._phase_name != "MENU" or self.sets.session_active:
            raise SetContractError("draft test only available from idle menu")
        if return_callback is not None and not callable(return_callback):
            raise TypeError("return_callback must be callable")
        if self._engine is None or self.phases is None:
            raise SetContractError("draft test requires active engine controller")
        self._invalidate_set_media()
        temporary = self.sets.begin_temporary_session(selection)
        self.selection = temporary
        self._draft_test_return_callback = return_callback
        try:
            self._apply_session_power_identity()
            self._engine["indexa"] = 4
            self.sync_scene_state(4)
            return self.sets.session_set
        except Exception:
            self._invalidate_set_media()
            self.sets.end_session()
            self.selection = self.sets.selected_set
            self._draft_test_return_callback = None
            raise

    def select_official_set(self, set_id):
        if self.sets.session_active:
            # Keep the session manager as the authority for the rejection reason.
            return self.sets.select(set_id)
        if self._phase_name != "MENU":
            raise SetContractError("set selection only available in menu")
        selection = self.sets.select(set_id)
        self._invalidate_set_media()
        self.selection = selection
        self._refresh_set_button()
        print("[JT-SET] menu selection={}".format(selection.set_id), flush=True)
        return selection

    def _set_selector_closed(self, *args):
        self._set_popup = None
        self._set_option_buttons = []
        self._set_selector_scroll = None

    def _choose_set_from_popup(self, set_id, popup):
        self.select_official_set(set_id)
        try:
            popup.dismiss()
        except Exception:
            pass
        self._set_selector_closed()

    def _quick_edit_selected_set(self):
        self._require_workshop_idle()
        if self.sets.selected_set.set_id in self._official_set_ids:
            self._workshop_create_dialog()
            return
        self._workshop_modify_current_action()

    def _open_set_selector(self):
        if self._phase_name != "MENU" or self.sets.session_active or self._set_popup is not None:
            return
        entries = self.sets.catalog()
        body = BoxLayout(
            orientation="vertical", spacing=dp(8), padding=dp(8),
            size_hint_y=None,
            height=max(dp(92), dp(84) * len(entries) + dp(16)),
        )
        self._set_option_buttons = []
        for selection in entries:
            dinosaurs = selection.dinosaurs()
            origin = "OFFICIEL" if selection.set_id in self._official_set_ids else "UTILISATEUR"
            button = Button(
                text="[{}] {}\n{}  VS  {}".format(
                    origin, selection.display_name,
                    dinosaurs["left"]["display_name"],
                    dinosaurs["right"]["display_name"],
                ),
                size_hint=(1, None),
                height=dp(76),
                font_size=dp(20),
            )
            self._set_option_buttons.append(button)
            body.add_widget(button)
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(body)
        close_button = Button(text="FERMER", size_hint=(1, None), height=dp(52), font_size=dp(18))
        content = BoxLayout(orientation="vertical", spacing=dp(8), padding=dp(8))
        content.add_widget(scroll)
        content.add_widget(close_button)
        popup = Popup(
            title="CHOISIR LES DINOSAURES",
            content=content,
            size_hint=(0.92, 0.86),
            auto_dismiss=True,
        )
        for button, selection in zip(self._set_option_buttons, entries):
            button.bind(
                on_release=lambda instance, sid=selection.set_id: self._choose_set_from_popup(sid, popup)
            )
        close_button.bind(on_release=lambda *args: popup.dismiss())
        popup.bind(on_dismiss=self._set_selector_closed)
        self._set_selector_scroll = scroll
        self._set_popup = popup
        popup.open()

    def _require_workshop_idle(self):
        if not self._admin_enabled:
            raise SetContractError("admin workshop is not enabled")
        if self._phase_name != "MENU" or self.sets.session_active:
            raise SetContractError("workshop only available in menu with no active session")

    def refresh_player_catalog(self):
        catalog = self.sets.refresh_catalog()
        self.selection = self.sets.runtime_set
        self._refresh_set_button()
        return catalog

    def workshop_import_zip(self, archive_path):
        self._require_workshop_idle()
        return self._set_storage.import_set_zip(
            archive_path, official_set_ids=self._official_set_ids
        )

    def promote_user_revision(self, set_id, revision):
        self._require_workshop_idle()
        self._set_storage.promote(set_id, revision)
        self.refresh_player_catalog()
        return self._set_storage.load_user_revision(set_id, revision)

    def workshop_resume_draft(self, draft_id):
        self._require_workshop_idle()
        state = self._set_admin.open_draft(draft_id)
        self._workshop_draft_id = draft_id
        return state

    def workshop_create_from_current(self, set_id, display_name=None, draft_id=None):
        self._require_workshop_idle()
        source = self.sets.selected_set
        source_kind = "official" if source.set_id in self._official_set_ids else "user"
        if draft_id is None:
            draft_id = "draft-{}".format(int(time.time() * 1000))
        state = self._set_admin.create_from_selection(
            source, draft_id=draft_id, set_id=set_id, source_kind=source_kind
        )
        if display_name is not None:
            state = self._set_admin.set_identity(draft_id, display_name=display_name)
        self._workshop_draft_id = draft_id
        return state

    def workshop_modify_selected_user(self, draft_id=None):
        self._require_workshop_idle()
        source = self.sets.selected_set
        if source.set_id in self._official_set_ids:
            raise SetContractError("select a user set before modification")
        if draft_id is None:
            draft_id = "edit-{}-{}".format(source.set_id, int(time.time() * 1000))
        state = self._set_admin.create_from_selection(
            source, draft_id=draft_id, set_id=source.set_id, source_kind="user"
        )
        self._workshop_draft_id = draft_id
        return state

    def workshop_current_role_info(self):
        if self._workshop_draft_id is None:
            raise SetContractError("no workshop draft selected")
        state = self._set_admin.open_draft(self._workshop_draft_id)
        roles = self._set_admin.roles(self._workshop_draft_id)
        role = roles[state.role_index]
        return {
            "state": state,
            "role": role,
            "progress": (state.role_index + 1, len(roles)),
            "current_path": self._set_admin.role_asset_path(self._workshop_draft_id, role.role_id),
            "candidate_path": self._set_admin.candidate_path(self._workshop_draft_id, role.role_id),
        }

    def workshop_keep_and_next(self):
        if self._workshop_draft_id is None:
            raise SetContractError("no workshop draft selected")
        self._set_admin.keep_and_next(self._workshop_draft_id)
        return self.workshop_current_role_info()

    def workshop_previous(self):
        if self._workshop_draft_id is None:
            raise SetContractError("no workshop draft selected")
        self._set_admin.previous_role(self._workshop_draft_id)
        return self.workshop_current_role_info()

    def workshop_stage_candidate(self, local_path):
        info = self.workshop_current_role_info()
        return self._set_admin.stage_candidate(
            self._workshop_draft_id, info["role"].role_id, local_path
        )

    def workshop_preview_current(self):
        info = self.workshop_current_role_info()
        if info["current_path"] is None:
            raise ValueError("current role has no media")
        return self._set_preview.preview(
            info["current_path"], info["role"].asset_type, info["role"].role_id
        )

    def workshop_preview_candidate(self):
        info = self.workshop_current_role_info()
        if info["candidate_path"] is None:
            raise ValueError("replacement candidate unavailable")
        return self._set_preview.preview(
            info["candidate_path"], info["role"].asset_type, info["role"].role_id
        )

    def workshop_accept_and_next(self):
        info = self.workshop_current_role_info()
        if info["candidate_path"] is None:
            raise ValueError("replacement candidate unavailable")
        self._set_admin.accept_candidate(self._workshop_draft_id, info["role"].role_id)
        self._set_admin.keep_and_next(self._workshop_draft_id)
        return self.workshop_current_role_info()

    def workshop_validate(self):
        if self._workshop_draft_id is None:
            raise SetContractError("no workshop draft selected")
        return self._set_admin.validate_complete(self._workshop_draft_id)

    def workshop_install_promote(self):
        self._require_workshop_idle()
        if self._workshop_draft_id is None:
            raise SetContractError("no workshop draft selected")
        result = self._set_admin.install_revision(self._workshop_draft_id)
        self._set_storage.promote(result.set_id, result.revision)
        self.refresh_player_catalog()
        return result

    def workshop_export_revision(self, destination_zip):
        self._require_workshop_idle()
        if self._workshop_draft_id is None:
            raise SetContractError("no workshop draft selected")
        return self._set_admin.export_revision(self._workshop_draft_id, destination_zip)

    def workshop_power_parameter_fields(self):
        self._require_workshop_idle()
        if self._workshop_draft_id is None:
            raise SetContractError("no workshop draft selected")
        return self._set_admin.power_parameter_fields(self._workshop_draft_id)

    def workshop_set_power_parameter(self, power_key, value):
        self._require_workshop_idle()
        if self._workshop_draft_id is None:
            raise SetContractError("no workshop draft selected")
        field = self._set_admin.set_power_parameter(
            self._workshop_draft_id, power_key, value
        )
        self._refresh_workshop_power_parameter_rows()
        return field

    def workshop_reset_power_parameter(self, power_key):
        self._require_workshop_idle()
        if self._workshop_draft_id is None:
            raise SetContractError("no workshop draft selected")
        field = self._set_admin.reset_power_parameter(
            self._workshop_draft_id, power_key
        )
        self._refresh_workshop_power_parameter_rows()
        return field

    def present_round(self, number, token):
        self.cancel_round_presentation()
        self._round_overlay = RoundOverlay(self, number, token, size_hint=(1, 1))
        self.root.add_widget(self._round_overlay)
        print("[JT-ROUND] ROUND {} token={} timers=frozen".format(number, token), flush=True)

    def cancel_round_presentation(self):
        if self._round_overlay is not None:
            self._round_overlay.close()
            self.root.remove_widget(self._round_overlay)
            self._round_overlay = None

    def _sync_current_scene(self, dt=0):
        state = self._engine['indexa'] if self._engine is not None else self._engine_state
        if state is not None:
            self.sync_scene_state(state)

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
                if self._engine_state in MP4_ONLY_STATES:
                    directory = "MP4-ONLY " + directory
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
            self._set_selector_visible(self._phase_name == "MENU" and not self.sets.session_active)
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
        if self.phases is not None:
            lines.append("PHASE={} ROUND={} car={} car2={} generation={}".format(
                self.phases.name, self.phases.round_number,
                self._engine['car'], self._engine['car2'], self._scene_generation))
        catalog_states = set(self._legacy_names)
        for scene in SCENE_SPECS.values():
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
            scene = self._scene_config(key)
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
            fallback = (
                "SUPPRIME (MP4-ONLY) " + legacy_dir
                if state in MP4_ONLY_STATES
                else legacy_dir
            )
            lines.append(
                "      fallback={}  prefix={}  frames={}  mode={}  son={}".format(
                    fallback, legacy_prefix or "(aucun)", length, genre, sound
                )
            )
        return "\n".join(lines)

    def _set_workshop_status(self, message):
        self._workshop_status = str(message or "")
        self._refresh_workshop_editor()

    def _workshop_closed(self, *args):
        self._workshop_popup = None
        self._workshop_menu_scroll = None
        self._workshop_buttons = {}

    def _close_workshop(self, *args):
        popup = self._workshop_popup
        self._workshop_closed()
        if popup is not None:
            try:
                popup.dismiss()
            except Exception:
                pass

    def _open_workshop(self):
        self._require_workshop_idle()
        if self._workshop_popup is not None:
            return self._workshop_popup
        content = BoxLayout(orientation="vertical", spacing=dp(8), padding=dp(8))
        title = Label(
            text="ATELIER SETS — DATA / MEDIA + COEFFICIENTS BORNÉS\nCoûts, chrono, KO, jalons et règles moteur restent verrouillés.",
            size_hint=(1, None), height=dp(72), font_size=dp(17),
        )
        content.add_widget(title)
        specs = (
            ("create", "CREER DEPUIS LE SET ACTUEL", self._workshop_create_dialog),
            ("resume", "REPRENDRE UN BROUILLON", self._workshop_resume_dialog),
            ("modify", "MODIFIER LE SET UTILISATEUR", self._workshop_modify_current_action),
            ("import", "IMPORTER UN ZIP", self._workshop_import_action),
        )
        body = BoxLayout(
            orientation="vertical", spacing=dp(8), padding=dp(8),
            size_hint_y=None, height=dp(64) * len(specs) + dp(16),
        )
        self._workshop_buttons = {}
        for key, label, callback in specs:
            button = Button(
                text=label, size_hint=(1, None), height=dp(56), font_size=dp(18)
            )
            button.bind(on_release=lambda instance, cb=callback: cb())
            body.add_widget(button)
            self._workshop_buttons[key] = button
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(body)
        content.add_widget(scroll)
        close = Button(text="FERMER", size_hint=(1, None), height=dp(56), font_size=dp(18))
        close.bind(on_release=lambda *args: self._close_workshop())
        content.add_widget(close)
        self._workshop_buttons["close"] = close
        popup = Popup(
            title="ATELIER DINOSAURES", content=content,
            size_hint=(0.92, 0.92), auto_dismiss=True,
        )
        self._workshop_menu_scroll = scroll
        self._workshop_popup = popup
        popup.bind(on_dismiss=self._workshop_closed)
        popup.open()
        return popup

    def _workshop_create_dialog(self):
        self._require_workshop_idle()
        set_id = TextInput(
            text="set-{}".format(int(time.time())), multiline=False,
            size_hint=(1, None), height=dp(58), font_size=dp(20),
        )
        display = TextInput(
            text="Nouveau set", multiline=False,
            size_hint=(1, None), height=dp(58), font_size=dp(20),
        )
        save = Button(text="CREER", size_hint=(1, None), height=dp(56), font_size=dp(18))
        cancel = Button(text="ANNULER", size_hint=(1, None), height=dp(52), font_size=dp(18))
        body = BoxLayout(
            orientation="vertical", spacing=dp(8), padding=dp(8),
            size_hint_y=None, height=dp(238),
        )
        body.add_widget(Label(text="Identifiant technique (minuscules, chiffres, . _ -)", size_hint=(1, None), height=dp(44)))
        body.add_widget(set_id)
        body.add_widget(Label(text="Nom affiché", size_hint=(1, None), height=dp(44)))
        body.add_widget(display)
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(body)
        content = BoxLayout(orientation="vertical", spacing=dp(8), padding=dp(8))
        content.add_widget(scroll)
        content.add_widget(save)
        content.add_widget(cancel)
        popup = Popup(title="NOUVEAU SET", content=content, size_hint=(0.86, 0.82), auto_dismiss=True)
        self._workshop_create_scroll = scroll
        popup.bind(on_dismiss=lambda *args: setattr(self, "_workshop_create_scroll", None))
        def create(*args):
            try:
                state = self.workshop_create_from_current(set_id.text.strip(), display.text.strip())
                popup.dismiss()
                self._close_workshop()
                self._workshop_open_editor(state.draft_id)
            except Exception as exc:
                self._set_workshop_status("Création refusée : {}".format(exc))
        save.bind(on_release=create)
        cancel.bind(on_release=lambda *args: popup.dismiss())
        popup.open()

    def _workshop_resume_dialog(self):
        self._require_workshop_idle()
        drafts = self._set_admin.list_drafts()
        row_count = max(1, len(drafts))
        body = BoxLayout(
            orientation="vertical", spacing=dp(8), padding=dp(8),
            size_hint_y=None, height=dp(72) * row_count + dp(16),
        )
        if not drafts:
            body.add_widget(Label(text="Aucun brouillon disponible", size_hint=(1, None), height=dp(56)))
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(body)
        content = BoxLayout(orientation="vertical", spacing=dp(8), padding=dp(8))
        popup = Popup(title="REPRENDRE UN BROUILLON", content=content, size_hint=(0.9, 0.9), auto_dismiss=True)
        for state in drafts:
            button = Button(
                text="{} — {} r{} — étape {}".format(
                    state.draft_id, state.set_id, state.revision, state.role_index + 1
                ), size_hint=(1, None), height=dp(64), font_size=dp(19),
            )
            def resume(instance, draft_id=state.draft_id):
                self.workshop_resume_draft(draft_id)
                popup.dismiss()
                self._close_workshop()
                self._workshop_open_editor(draft_id)
            button.bind(on_release=resume)
            body.add_widget(button)
        close = Button(text="FERMER", size_hint=(1, None), height=dp(52), font_size=dp(18))
        close.bind(on_release=lambda *args: popup.dismiss())
        content.add_widget(scroll)
        content.add_widget(close)
        self._workshop_resume_scroll = scroll
        popup.bind(on_dismiss=lambda *args: setattr(self, "_workshop_resume_scroll", None))
        popup.open()

    def _workshop_modify_current_action(self):
        try:
            state = self.workshop_modify_selected_user()
        except Exception as exc:
            self._set_workshop_status("Modification refusée : {}".format(exc))
            return
        self._close_workshop()
        self._workshop_open_editor(state.draft_id)

    def _workshop_import_action(self):
        self._require_workshop_idle()
        stamp = int(time.time() * 1000)
        draft_name = "import-{}.zip".format(stamp)
        def picked(uri, error):
            if error is not None:
                self._set_workshop_status("Import : {}".format(error))
                return
            if uri is None:
                self._set_workshop_status("Import annulé")
                return
            def copied(path, copy_error):
                try:
                    if copy_error is not None:
                        raise copy_error
                    result = self.workshop_import_zip(path)
                    self._set_workshop_status(
                        "Importé {} r{} — non promu tant que vous ne validez pas.".format(
                            result.set_id, result.revision
                        )
                    )
                except Exception as exc:
                    self._set_workshop_status("Import refusé : {}".format(exc))
                finally:
                    if path is not None:
                        try:
                            Path(path).unlink()
                        except OSError:
                            pass
            self._set_ingress.copy(uri, draft_name, copied)
        self._set_picker.choose("application/zip", picked)

    def _refresh_workshop_editor(self, dt=0):
        if self._workshop_editor_label is None or self._workshop_draft_id is None:
            return
        try:
            info = self.workshop_current_role_info()
            current, total = info["progress"]
            role = info["role"]
            current_name = Path(info["current_path"]).name if info["current_path"] else "(aucun)"
            candidate_name = Path(info["candidate_path"]).name if info["candidate_path"] else "(aucun)"
            self._workshop_editor_label.text = (
                "BROUILLON : {}\n{}\nTYPE : {}{}\nACTUEL : {}\nREMPLACEMENT : {}\n{}".format(
                    self._workshop_draft_id, role.label,
                    role.asset_type.upper(), " — OBLIGATOIRE" if role.required else " — OPTIONNEL",
                    current_name, candidate_name, self._workshop_status,
                )
            )
            if self._workshop_progress_label is not None:
                self._workshop_progress_label.text = "ÉTAPE {}/{}".format(current, total)
        except Exception as exc:
            self._workshop_editor_label.text = "Atelier indisponible : {}".format(exc)
            if self._workshop_progress_label is not None:
                self._workshop_progress_label.text = "ÉTAPE ?/?"

    def _workshop_open_editor(self, draft_id=None):
        self._require_workshop_idle()
        if draft_id is not None:
            self.workshop_resume_draft(draft_id)
        if self._workshop_draft_id is None:
            raise SetContractError("no workshop draft selected")
        if self._workshop_editor_popup is not None:
            try:
                self._workshop_editor_popup.dismiss()
            except Exception:
                pass
        label = Label(
            text="", size_hint=(1, None), height=dp(132), font_size=dp(17),
            halign="left", valign="middle",
        )
        previous = Button(text="◀ PRÉC.", size_hint=(0.26, 1), font_size=dp(17))
        progress = Label(text="", size_hint=(0.48, 1), font_size=dp(17))
        following = Button(text="SUIVANT ▶", size_hint=(0.26, 1), font_size=dp(17))
        navigation = BoxLayout(
            orientation="horizontal", spacing=dp(6), size_hint=(1, None), height=dp(50)
        )
        navigation.add_widget(previous)
        navigation.add_widget(progress)
        navigation.add_widget(following)
        previous.bind(on_release=lambda *args: self._workshop_previous_action())
        following.bind(on_release=lambda *args: self._workshop_keep_action())

        actions = (
            ("CHOISIR VIDÉO / MÉDIA", self._workshop_choose_replacement),
            ("APERÇU ACTUEL", self._workshop_preview_current_action),
            ("APERÇU REMPLACEMENT", self._workshop_preview_candidate_action),
            ("VALIDER REMPLACEMENT", self._workshop_accept_action),
            ("IDENTITÉ / NOMS", self._workshop_identity_dialog),
            ("PARAMÈTRES POUVOIRS", self._workshop_power_parameters_dialog),
            ("TESTER CE SET", self._workshop_test_action),
            ("INSTALLER + PROMOUVOIR", self._workshop_promote_action),
            ("EXPORTER ZIP", self._workshop_export_action),
        )
        body = BoxLayout(
            orientation="vertical", spacing=dp(7), padding=dp(4),
            size_hint_y=None, height=dp(60) * len(actions) + dp(16),
        )
        for text, callback in actions:
            button = Button(text=text, size_hint=(1, None), height=dp(52), font_size=dp(17))
            button.bind(on_release=lambda instance, cb=callback: cb())
            body.add_widget(button)
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(body)

        content = BoxLayout(orientation="vertical", spacing=dp(6), padding=dp(7))
        content.add_widget(label)
        content.add_widget(navigation)
        content.add_widget(scroll)
        close = Button(text="RETOUR ATELIER", size_hint=(1, None), height=dp(52), font_size=dp(18))
        content.add_widget(close)
        popup = Popup(title="ASSISTANT SET", content=content, size_hint=(0.96, 0.96), auto_dismiss=True)
        self._workshop_editor_popup = popup
        self._workshop_editor_label = label
        self._workshop_editor_scroll = scroll
        self._workshop_progress_label = progress
        close.bind(on_release=lambda *args: popup.dismiss())
        popup.bind(on_dismiss=lambda *args: self._workshop_editor_closed())
        self._refresh_workshop_editor()
        popup.open()
        return popup

    def _workshop_editor_closed(self):
        self._workshop_editor_popup = None
        self._workshop_editor_label = None
        self._workshop_editor_scroll = None
        self._workshop_progress_label = None
        self._close_workshop_preview_popup()
        self._set_preview.close("editor-close")

    def _workshop_preview_current_action(self):
        try:
            self._close_workshop_preview_popup()
            result = self.workshop_preview_current()
            self._set_workshop_status(self._preview_status(result))
            self._open_workshop_preview_popup("APERÇU ACTUEL")
        except Exception as exc:
            self._set_workshop_status("Aperçu actuel impossible : {}".format(exc))

    def _workshop_preview_candidate_action(self):
        try:
            self._close_workshop_preview_popup()
            result = self.workshop_preview_candidate()
            self._set_workshop_status(self._preview_status(result))
            self._open_workshop_preview_popup("APERÇU REMPLACEMENT")
        except Exception as exc:
            self._set_workshop_status("Aperçu remplacement impossible : {}".format(exc))

    def _open_workshop_preview_popup(self, title):
        surface = WorkshopPreviewSurface(size_hint=(1, 1))
        status = Label(
            text="", size_hint=(1, None), height=dp(56), font_size=dp(15),
            halign="center", valign="middle",
        )
        close = Button(
            text="FERMER APERÇU", size_hint=(0.62, None), pos_hint={"center_x": 0.5},
            height=dp(46), font_size=dp(16)
        )
        content = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(10))
        content.add_widget(surface)
        content.add_widget(status)
        content.add_widget(close)
        popup = Popup(title=title, content=content, size_hint=(0.96, 0.94), auto_dismiss=True)
        self._workshop_preview_popup = popup
        self._workshop_preview_surface = surface
        self._workshop_preview_label = status

        def refresh(dt=0):
            if self._workshop_preview_popup is not popup:
                return
            surface.set_texture(self._set_preview.current_texture)
            result = self._set_preview.current_result
            status.text = self._preview_status(result) if result is not None else "Aperçu fermé"

        self._workshop_preview_event = Clock.schedule_interval(refresh, 1.0 / 30.0)
        close.bind(on_release=lambda *args: popup.dismiss())
        popup.bind(on_dismiss=lambda *args: self._close_workshop_preview_popup())
        refresh(0)
        popup.open()
        return popup

    def _close_workshop_preview_popup(self):
        event = self._workshop_preview_event
        self._workshop_preview_event = None
        if event is not None:
            try:
                event.cancel()
            except Exception:
                pass
        popup = self._workshop_preview_popup
        self._workshop_preview_popup = None
        self._workshop_preview_surface = None
        self._workshop_preview_label = None
        if popup is not None:
            try:
                popup.dismiss()
            except Exception:
                pass
        self._set_preview.close("preview-popup-close")

    @staticmethod
    def _preview_status(result):
        if result.opened and result.kind == "video" and not result.first_frame:
            details = ["Chargement vidéo…"]
        else:
            details = ["Aperçu {}".format("OK" if result.opened else "NON OUVERT")]
        if result.dimensions:
            details.append("{}x{}".format(*result.dimensions))
        if result.duration is not None:
            details.append("{:.2f}s".format(result.duration))
        details.extend(result.warnings)
        return " — ".join(details)

    def _workshop_keep_action(self):
        try:
            self.workshop_keep_and_next()
            self._set_workshop_status("Ressource actuelle conservée")
        except Exception as exc:
            self._set_workshop_status("Navigation impossible : {}".format(exc))

    def _workshop_accept_action(self):
        try:
            self.workshop_accept_and_next()
            self._set_workshop_status("Remplacement validé")
        except Exception as exc:
            self._set_workshop_status("Validation impossible : {}".format(exc))

    def _workshop_previous_action(self):
        try:
            self.workshop_previous()
            self._set_workshop_status("Etape précédente")
        except Exception as exc:
            self._set_workshop_status("Retour impossible : {}".format(exc))

    def _workshop_choose_replacement(self):
        try:
            info = self.workshop_current_role_info()
        except Exception as exc:
            self._set_workshop_status("Sélection impossible : {}".format(exc))
            return
        mime = {"video": "video/mp4", "image": "image/*", "audio": "audio/*"}[info["role"].asset_type]
        suffix = {"video": ".mp4", "image": ".jpg", "audio": ".wav"}[info["role"].asset_type]
        draft_name = "ingress-{}-{}{}".format(
            self._workshop_draft_id, int(time.time() * 1000), suffix
        )
        def picked(uri, error):
            if error is not None:
                self._set_workshop_status("Sélecteur : {}".format(error)); return
            if uri is None:
                self._set_workshop_status("Sélection annulée"); return
            def copied(path, copy_error):
                try:
                    if copy_error is not None:
                        raise copy_error
                    self.workshop_stage_candidate(path)
                    self._set_workshop_status("Remplacement chargé — utilisez APERÇU puis VALIDER")
                except Exception as exc:
                    self._set_workshop_status("Remplacement refusé : {}".format(exc))
                finally:
                    if path is not None:
                        try: Path(path).unlink()
                        except OSError: pass
            self._set_ingress.copy(uri, draft_name, copied)
        self._set_picker.choose(mime, picked)

    def _workshop_adjust_power_parameter(self, power_key, delta):
        fields = {field.power_key: field for field in self.workshop_power_parameter_fields()}
        field = fields[power_key]
        target = round(field.value + float(delta), 10)
        target = min(max(target, field.minimum), field.maximum)
        return self.workshop_set_power_parameter(power_key, target)

    @staticmethod
    def _power_parameter_text(field):
        return "{} — {:.0f} % ({}–{} %)".format(
            field.label, field.value * 100.0,
            int(round(field.minimum * 100.0)), int(round(field.maximum * 100.0)),
        )

    def _refresh_workshop_power_parameter_rows(self):
        if not self._workshop_parameter_labels or self._workshop_draft_id is None:
            return
        try:
            fields = self.workshop_power_parameter_fields()
        except Exception:
            return
        for field in fields:
            label = self._workshop_parameter_labels.get(field.power_key)
            if label is not None:
                label.text = self._power_parameter_text(field)

    def _close_workshop_power_parameters(self, *args):
        popup = self._workshop_parameter_popup
        self._workshop_parameter_popup = None
        self._workshop_parameter_labels = {}
        if popup is not None:
            try:
                popup.dismiss()
            except Exception:
                pass

    def _workshop_power_parameters_dialog(self):
        self._require_workshop_idle()
        if self._workshop_draft_id is None:
            raise SetContractError("no workshop draft selected")
        if self._workshop_parameter_popup is not None:
            return self._workshop_parameter_popup

        fields = self.workshop_power_parameter_fields()
        body = BoxLayout(
            orientation="vertical", spacing=dp(8), padding=dp(8), size_hint_y=None,
            height=dp(len(fields) * 124),
        )
        self._workshop_parameter_labels = {}
        for field in fields:
            label = Label(
                text=self._power_parameter_text(field), size_hint=(1, None),
                height=dp(52), font_size=dp(18), halign="left", valign="middle",
            )
            self._workshop_parameter_labels[field.power_key] = label
            body.add_widget(label)
            controls = BoxLayout(orientation="horizontal", spacing=dp(8), size_hint=(1, None), height=dp(62))
            minus = Button(text="−1 %", size_hint=(1, None), height=dp(60), font_size=dp(19))
            plus = Button(text="+1 %", size_hint=(1, None), height=dp(60), font_size=dp(19))
            reset = Button(text="DÉFAUT", size_hint=(1, None), height=dp(60), font_size=dp(19))
            minus.bind(on_release=lambda instance, key=field.power_key: self._workshop_adjust_power_parameter(key, -0.01))
            plus.bind(on_release=lambda instance, key=field.power_key: self._workshop_adjust_power_parameter(key, +0.01))
            reset.bind(on_release=lambda instance, key=field.power_key: self.workshop_reset_power_parameter(key))
            controls.add_widget(minus)
            controls.add_widget(plus)
            controls.add_widget(reset)
            body.add_widget(controls)

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(body)
        close = Button(text="RETOUR ASSISTANT", size_hint=(1, None), height=dp(62), font_size=dp(20))
        content = BoxLayout(orientation="vertical", spacing=dp(8), padding=dp(8))
        content.add_widget(Label(
            text="Six coefficients seulement — ajustement par pas de 1 %.",
            size_hint=(1, None), height=dp(48), font_size=dp(18),
        ))
        content.add_widget(scroll)
        content.add_widget(close)
        popup = Popup(
            title="PARAMÈTRES POUVOIRS", content=content,
            size_hint=(0.94, 0.94), auto_dismiss=True,
        )
        self._workshop_parameter_popup = popup
        close.bind(on_release=lambda *args: popup.dismiss())
        popup.bind(on_dismiss=lambda *args: self._close_workshop_power_parameters())
        popup.open()
        return popup

    def _workshop_identity_dialog(self):
        try:
            selection = self.workshop_validate()
        except Exception as exc:
            self._set_workshop_status("Identité indisponible : {}".format(exc)); return
        manifest = selection.manifest()
        display = TextInput(text=manifest["display_name"], multiline=False, size_hint=(1, None), height=dp(52))
        left = TextInput(text=manifest["dinosaurs"]["left"]["display_name"], multiline=False, size_hint=(1, None), height=dp(52))
        right = TextInput(text=manifest["dinosaurs"]["right"]["display_name"], multiline=False, size_hint=(1, None), height=dp(52))
        power_fields = {}
        body = BoxLayout(orientation="vertical", spacing=dp(6), padding=dp(8), size_hint_y=None)
        body.bind(minimum_height=body.setter("height"))
        for title, field in (("Nom du set", display), ("Dinosaure gauche", left), ("Dinosaure droit", right)):
            body.add_widget(Label(text=title, size_hint=(1, None), height=dp(36)))
            body.add_widget(field)
        for power_key in POWER_KEYS:
            side, slot = power_key.split("_", 1)
            field = TextInput(
                text=manifest["powers"][power_key]["label"], multiline=False,
                size_hint=(1, None), height=dp(52),
            )
            power_fields[power_key] = field
            body.add_widget(Label(
                text="Pouvoir {} {}".format("gauche" if side == "left" else "droit", slot),
                size_hint=(1, None), height=dp(36),
            ))
            body.add_widget(field)
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(body)
        save = Button(text="VALIDER IDENTITE", size_hint=(1, None), height=dp(60), font_size=dp(19))
        content = BoxLayout(orientation="vertical", spacing=dp(6), padding=dp(8))
        content.add_widget(scroll)
        content.add_widget(save)
        popup = Popup(title="IDENTITE ET POUVOIRS", content=content, size_hint=(0.88, 0.92), auto_dismiss=True)
        def apply(*args):
            try:
                power_labels = {power_key: field.text for power_key, field in power_fields.items()}
                self._set_admin.set_identity(
                    self._workshop_draft_id, display_name=display.text,
                    left_name=left.text, right_name=right.text,
                    power_labels=power_labels,
                )
                popup.dismiss(); self._set_workshop_status("Identité mise à jour")
            except Exception as exc:
                self._set_workshop_status("Identité refusée : {}".format(exc))
        save.bind(on_release=apply)
        popup.open()

    def _workshop_test_action(self):
        try:
            selection = self.workshop_validate()
            popup = self._workshop_editor_popup
            if popup is not None:
                popup.dismiss()
            self.start_draft_test(
                selection,
                return_callback=lambda: self._workshop_open_editor(self._workshop_draft_id),
            )
        except Exception as exc:
            self._set_workshop_status("Test impossible : {}".format(exc))

    def _workshop_promote_action(self):
        try:
            result = self.workshop_install_promote()
            self._set_workshop_status(
                "Installé et promu : {} r{}".format(result.set_id, result.revision)
            )
        except Exception as exc:
            self._set_workshop_status("Installation/promotion refusée : {}".format(exc))

    def _workshop_export_action(self):
        try:
            self._require_workshop_idle()
            if self._workshop_draft_id is None:
                raise SetContractError("no workshop draft selected")
            state = self._set_admin.open_draft(self._workshop_draft_id)
            suggested = "{}-r{}.jtrex.zip".format(state.set_id, state.revision)
        except Exception as exc:
            self._set_workshop_status("Export refusé : {}".format(exc)); return

        def picked(uri, error):
            if error is not None:
                self._set_workshop_status("Export : {}".format(error)); return
            if uri is None:
                self._set_workshop_status("Export annulé"); return
            self._set_workshop_status("Export ZIP en cours…")

            def build_archive():
                export_root = self._state_root / "jt-set-exports"
                export_root.mkdir(parents=True, exist_ok=True)
                target = export_root / ".share-{}-{}".format(int(time.time() * 1000), suggested)
                self.workshop_export_revision(target)
                return target

            def finished(written, export_error):
                if export_error is not None:
                    self._set_workshop_status("Export refusé : {}".format(export_error))
                else:
                    self._set_workshop_status("ZIP exporté — {} octets".format(written))

            self._set_egress.export(uri, build_archive, finished)

        self._set_picker.create("application/zip", suggested, picked)

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
        workshop_button = Button(
            text="ATELIER SETS",
            size_hint=(1, None),
            height=dp(64),
            font_size=dp(20),
        )
        close_button = Button(
            text="FERMER",
            size_hint=(1, None),
            height=dp(58),
            font_size=dp(20),
        )
        content = BoxLayout(orientation="vertical", spacing=dp(8), padding=dp(8))
        content.add_widget(scroll)
        content.add_widget(workshop_button)
        content.add_widget(close_button)
        popup = Popup(
            title="ADMIN MEDIA — diagnostic uniquement",
            content=content,
            size_hint=(0.96, 0.94),
            auto_dismiss=True,
        )
        self._admin_popup = popup
        self._admin_label = label
        self._admin_workshop_button = workshop_button
        workshop_button.bind(on_release=lambda *args: self._open_workshop())
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
        self._admin_workshop_button = None
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
        for key, scene in SCENE_SPECS.items():
            if indexa in scene["states"]:
                return key
        return None

    def _scene_config(self, key):
        spec = dict(SCENE_SPECS[key])
        selection = self.sets.runtime_set
        if "media_role" in spec:
            spec["file"] = selection.media_path(spec["media_role"])
        elif "power_key" in spec:
            spec["file"] = selection.power_media_path(spec["power_key"])
        else:
            raise KeyError("scene without media selector: {}".format(key))
        # Official selections must keep using the controller's live Kivy resolver
        # so runtime/media failures remain observable. Portable user/draft sets
        # own a private physical resolver and must never fall through to an APK
        # asset with the same relative name.
        if selection.manifest_path == "manifest.json":
            resolved = selection.resolve_path(spec["file"])
        else:
            resolved = self._resolve(spec["file"])
        spec["resolved_file"] = resolved
        return spec

    def start_intro(self, done_callback):
        if self._intro_done:
            Clock.schedule_once(lambda dt: done_callback(), 0)
            return
        self._intro_done_callback = done_callback
        startup_selection = self.sets.startup_intro_set
        chosen = random.choice(startup_selection.intro_paths())
        if startup_selection.manifest_path == "manifest.json":
            path = startup_selection.resolve_path(chosen)
        else:
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
        if self._engine is not None:
            indexa = self._engine['indexa']
            self.phases.sync()
            self.phases.apply_ui()
        if not self._intro_done:
            return
        self._engine_state = indexa
        if indexa == 0 and self._scene_key != "wait":
            self._wait_resume_fraction = 0.0
        key = self._key_for_state(indexa)
        if key is not None and key == self._scene_completed_key:
            return
        if key != self._scene_completed_key:
            self._scene_completed_key = None

        if self._scene_player is not None and self._scene_key is not None:
            current_scene = self._scene_config(self._scene_key)
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
        scene = self._scene_config(key)
        path = scene.get("resolved_file")
        self._scene_key = key
        self._scene_generation += 1
        generation = self._scene_generation
        self._scene_has_frame = False
        self._scene_audio_native = False
        self._scene_eos_reached = False
        self._wait_seek_pending = (
            key == "wait" and self._wait_resume_fraction > 0.001
        )
        self.root._jt_scene_video_active = False
        self.root._jt_scene_cinematic_lock = False
        self.root._jt_power_video_hold = False
        self.root._jt_wait_video_active = False

        if not path or CoreVideo is None:
            self._scene_failed_key = key
            if self.phases is not None:
                self.phases.video_complete(indexa, failed=True)
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
            self.root._jt_power_video_hold = key in POWER_SCENE_KEYS
            if self.root._jt_power_video_hold:
                print(
                    "[JT-POWER-VIDEO] hold controls/timers until real MP4 EOS key={} state={}".format(
                        key, indexa
                    ),
                    flush=True,
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
            if self.phases is not None:
                self.phases.video_complete(indexa, failed=True)
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
        if (
            first_frame
            and self._scene_key == "wait"
            and self._wait_seek_pending
        ):
            self._wait_seek_pending = False
            resume = self._wait_resume_fraction % 1.0
            try:
                try:
                    player.seek(resume, precise=True)
                except TypeError:
                    player.seek(resume)
                print(
                    "[JT-WAIT] resume fraction={:.4f}".format(resume),
                    flush=True,
                )
                return
            except Exception as exc:
                print(
                    "[JT-WAIT][WARN] resume seek failed fraction={:.4f} error={!r}".format(
                        resume, exc
                    ),
                    flush=True,
                )

        self._scene_has_frame = True
        if self._scene_timeout is not None:
            self._scene_timeout.cancel()
            self._scene_timeout = None

        self.root.deux.texture = texture
        self.root._jt_scene_video_active = True
        self.root._jt_wait_video_active = self._scene_key == "wait"

        if first_frame:
            if self._scene_key in FINISH_SCENE_KEYS:
                self.root._jt_finishing_video_hold = True
                self.root._jt_finishing_complete_pending = None
                print(
                    "[JT-FINISH] hold historical state until real MP4 EOS key={} state={}".format(
                        self._scene_key, self._scene_state
                    ),
                    flush=True,
                )
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
        scene = self._scene_config(key) if key in SCENE_SPECS else {}
        print(
            "[JT-SCENE] eos key={} generation={} play_to_end={} file={} position={} duration={} engine={} state-machine=unchanged".format(
                key, generation, scene.get("play_to_end", False), scene.get("file"),
                getattr(player, "position", None), getattr(player, "duration", None),
                self._engine['indexa'] if self._engine is not None else self._engine_state
            ),
            flush=True,
        )
        if scene.get("play_to_end", False):
            self._scene_completed_key = key
            if self.phases is not None:
                self.phases.video_complete(self._scene_state)
            finishing_state = (
                self._scene_state
                if key in FINISH_SCENE_KEYS
                else None
            )
            if finishing_state in (10, 11):
                self.root._jt_finishing_complete_pending = finishing_state
                print(
                    "[JT-FINISH] real MP4 EOS; release historical finish state={}".format(
                        finishing_state
                    ),
                    flush=True,
                )
            self._stop_scene("eos-complete", preserve_failure=False)
            if finishing_state in (10, 11):
                return
            Clock.schedule_once(self._sync_current_scene, 0)

    def _scene_frame_timeout(self, generation):
        if generation != self._scene_generation:
            return
        self._scene_timeout = None
        if not self._scene_has_frame:
            key = self._scene_key
            self._scene_failed_key = key
            if self.phases is not None:
                self.phases.video_complete(self._scene_state, failed=True)
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
        if key == "wait" and reason == "state=0":
            self._wait_resume_fraction = 0.0
            print("[JT-WAIT] reset resume at menu", flush=True)
        if (
            key == "wait"
            and player is not None
            and reason not in ("state=0", "shutdown")
        ):
            try:
                duration = float(getattr(player, "duration", 0.0) or 0.0)
                position = float(getattr(player, "position", 0.0) or 0.0)
                if duration > 0.0:
                    self._wait_resume_fraction = (position % duration) / duration
                    print(
                        "[JT-WAIT] remember position={:.3f}s duration={:.3f}s fraction={:.4f}".format(
                            position, duration, self._wait_resume_fraction
                        ),
                        flush=True,
                    )
            except Exception as exc:
                print("[JT-WAIT][WARN] remember position={!r}".format(exc), flush=True)
        frame_callback = self._scene_frame_callback
        eos_callback = self._scene_eos_callback
        self._scene_player = None
        self._scene_frame_callback = None
        self._scene_eos_callback = None

        self.root._jt_scene_video_active = False
        self.root._jt_wait_video_active = False
        self.root._jt_scene_cinematic_lock = False
        self.root._jt_power_video_hold = False
        self.root._jt_finishing_video_hold = False
        self._wait_seek_pending = False
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

        # Retain the last frame in aspect-fill while the logical action catches
        # up to a short MP4. The next state/shutdown restores the base geometry.
        if reason != "eos-complete":
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
        if self.phases is not None:
            self.phases.set_paused(True)
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
        if self.phases is not None:
            self.phases.set_paused(False)
        player = self._paused_player
        self._paused_player = None
        if player is not None:
            try:
                player.play()
                print("[JT-MEDIA] resume", flush=True)
            except Exception as exc:
                print("[JT-MEDIA][WARN] resume={!r}".format(exc), flush=True)

    def shutdown(self):
        if self.phases is not None:
            self.phases.shutdown()
        self.cancel_round_presentation()
        self._close_workshop_preview_popup()
        try:
            self._set_picker.close()
        except Exception:
            pass
        if self._workshop_editor_popup is not None:
            try:
                self._workshop_editor_popup.dismiss()
            except Exception:
                pass
            self._workshop_editor_popup = None
        if self._workshop_popup is not None:
            try:
                self._workshop_popup.dismiss()
            except Exception:
                pass
            self._workshop_popup = None
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
        if self._menu_right_dino_event is not None:
            self._menu_right_dino_event.cancel()
            self._menu_right_dino_event = None
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
        if self._set_popup is not None:
            try:
                self._set_popup.dismiss()
            except Exception:
                pass
            self._set_popup = None
        if self._set_button is not None:
            try:
                self.root.remove_widget(self._set_button)
            except Exception:
                pass
            self._set_button = None
        if self._set_edit_button is not None:
            try:
                self.root.remove_widget(self._set_edit_button)
            except Exception:
                pass
            self._set_edit_button = None
        if not self._intro_done:
            self._finish_intro("shutdown")
        self._stop_scene("shutdown", preserve_failure=False)
