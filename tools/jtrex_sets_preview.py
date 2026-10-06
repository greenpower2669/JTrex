"""Isolated media probing for the JTrex set workshop.

The preview controller intentionally has no combat-engine dependency. It owns only
one decoder/resource at a time and guards callbacks with a private generation.
"""
from dataclasses import dataclass
import math
from pathlib import Path


@dataclass
class JTPreviewResult:
    kind: str
    opened: bool = False
    first_frame: bool = False
    dimensions: tuple | None = None
    duration: float | None = None
    warnings: tuple = ()


class JTSetPreviewController:
    def __init__(self, root, core_video_cls, clock, image_loader=None, sound_loader=None):
        self.root = root
        self._core_video_cls = core_video_cls
        self._clock = clock
        self._image_loader = image_loader
        self._sound_loader = sound_loader
        self._generation = 0
        self._player = None
        self._aux_resource = None
        self._frame_callback = None
        self._eos_callback = None
        self._result = None
        self._texture = None

    @property
    def current_player(self):
        return self._player

    @property
    def current_result(self):
        return self._result

    @property
    def current_texture(self):
        return self._texture

    @staticmethod
    def _duration(value):
        try:
            value = float(value)
        except (TypeError, ValueError):
            return None
        return value if math.isfinite(value) and value >= 0 else None

    @staticmethod
    def _dimensions(texture):
        try:
            width, height = texture.size
            width, height = int(width), int(height)
        except (AttributeError, TypeError, ValueError):
            return None
        return (width, height) if width > 0 and height > 0 else None

    @staticmethod
    def _role_warnings(dimensions, expected_role):
        if not dimensions or not expected_role:
            return ()
        width, height = dimensions
        role = str(expected_role).lower()
        warnings = []
        if "portrait" in role and width > height:
            warnings.append("Orientation paysage pour un rôle portrait")
        if any(word in role for word in ("combat", "orbs", "charge", "verdict", "finishing")) and height > width:
            warnings.append("Orientation portrait pour une scène de combat")
        return tuple(warnings)

    def _append_warning(self, result, message):
        if message not in result.warnings:
            result.warnings = result.warnings + (message,)

    def close(self, reason="close"):
        self._generation += 1
        player = self._player
        if player is not None:
            callbacks = {}
            if self._frame_callback is not None:
                callbacks["on_frame"] = self._frame_callback
            if self._eos_callback is not None:
                callbacks["on_eos"] = self._eos_callback
            if callbacks:
                try:
                    player.unbind(**callbacks)
                except Exception:
                    pass
            for method in ("stop", "unload"):
                try:
                    getattr(player, method)()
                except Exception:
                    pass
        resource = self._aux_resource
        if resource is not None:
            for method in ("stop", "unload"):
                try:
                    getattr(resource, method)()
                except Exception:
                    pass
        self._player = None
        self._aux_resource = None
        self._frame_callback = None
        self._eos_callback = None
        self._texture = None
        self._result = None

    def preview(self, path, kind, expected_role=None):
        if kind not in ("video", "image", "audio"):
            raise ValueError("preview kind must be video, image or audio")
        path = Path(path)
        if not path.is_file():
            raise ValueError("preview file unavailable")
        self.close("replace")
        generation = self._generation
        result = JTPreviewResult(kind=kind)
        self._result = result
        physical = str(path)

        if kind == "video":
            try:
                player = self._core_video_cls(filename=physical, eos="stop", autoplay=False)
            except Exception as exc:
                self._append_warning(result, "Decoder video indisponible: {}".format(exc))
                return result
            self._player = player
            result.opened = True

            def on_frame(instance, *args):
                if generation != self._generation or instance is not self._player or result is not self._result:
                    return
                texture = getattr(instance, "texture", None)
                dimensions = self._dimensions(texture)
                if dimensions is None:
                    self._append_warning(result, "Dimensions video invalides")
                    return
                self._texture = texture
                result.first_frame = True
                result.dimensions = dimensions
                result.duration = self._duration(getattr(instance, "duration", None))
                for warning in self._role_warnings(dimensions, expected_role):
                    self._append_warning(result, warning)

            def on_eos(instance, *args):
                if generation != self._generation or instance is not self._player or result is not self._result:
                    return
                # Preview EOS is observational only. It never calls gameplay.
                result.duration = self._duration(getattr(instance, "duration", None))

            self._frame_callback = on_frame
            self._eos_callback = on_eos
            try:
                player.bind(on_frame=on_frame, on_eos=on_eos)
                player.play()
            except Exception as exc:
                self._append_warning(result, "Decoder video lecture impossible: {}".format(exc))
                self.close("video-open-error")
                # Preserve the diagnostic result after releasing resources.
                self._result = result
                result.opened = False
            return result

        if kind == "image":
            if self._image_loader is None:
                self._append_warning(result, "Decodeur image indisponible")
                return result
            try:
                resource = self._image_loader(physical)
                texture = getattr(resource, "texture", resource)
                dimensions = self._dimensions(texture)
            except Exception as exc:
                self._append_warning(result, "Decodeur image indisponible: {}".format(exc))
                return result
            self._aux_resource = resource
            result.opened = True
            if dimensions is None:
                self._append_warning(result, "Dimensions image invalides")
                return result
            self._texture = texture
            result.first_frame = True
            result.dimensions = dimensions
            for warning in self._role_warnings(dimensions, expected_role):
                self._append_warning(result, warning)
            return result

        if self._sound_loader is None:
            self._append_warning(result, "Decodeur audio indisponible")
            return result
        try:
            sound = self._sound_loader(physical)
        except Exception as exc:
            self._append_warning(result, "Decodeur audio indisponible: {}".format(exc))
            return result
        if sound is None:
            self._append_warning(result, "Decodeur audio indisponible")
            return result
        self._aux_resource = sound
        result.opened = True
        result.duration = self._duration(
            getattr(sound, "length", getattr(sound, "duration", None))
        )
        if result.duration is None:
            self._append_warning(result, "Duree audio inconnue")
        return result
