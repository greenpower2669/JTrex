import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

try:
    from tools.jtrex_sets_preview import JTPreviewResult, JTSetPreviewController
except ImportError:
    JTPreviewResult = JTSetPreviewController = None


class FakePlayer:
    instances = []
    fail_paths = set()

    def __init__(self, filename=None, eos=None, autoplay=False, **kwargs):
        if filename in self.fail_paths:
            raise OSError('decoder refused')
        self.filename = filename
        self.eos = eos
        self.autoplay = autoplay
        self.callbacks = {}
        self.texture = None
        self.duration = 12.5
        self.position = 0.0
        self.state = 'new'
        self.instances.append(self)

    def bind(self, **kwargs):
        self.callbacks.update(kwargs)

    def unbind(self, **kwargs):
        for key in kwargs:
            self.callbacks.pop(key, None)

    def play(self):
        self.state = 'playing'

    def stop(self):
        self.state = 'stopped'

    def unload(self):
        self.state = 'unloaded'


class FakeClock:
    events = []

    @classmethod
    def schedule_once(cls, callback, delay=0):
        event = SimpleNamespace(callback=callback, delay=delay, cancelled=False)
        event.cancel = lambda: setattr(event, 'cancelled', True)
        cls.events.append(event)
        return event


class PreviewTests(unittest.TestCase):
    def setUp(self):
        FakePlayer.instances = []
        FakePlayer.fail_paths = set()
        FakeClock.events = []
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = SimpleNamespace(children=[])

    def path(self, name, data=b'x'):
        p = Path(self.tmp.name) / name
        p.write_bytes(data)
        return p

    def test_video_preview_replaces_previous_and_stale_callbacks_are_ignored(self):
        controller = JTSetPreviewController(self.root, FakePlayer, FakeClock)
        first = controller.preview(self.path('first.mp4'), 'video')
        old = FakePlayer.instances[-1]
        old_frame = old.callbacks['on_frame']
        old_eos = old.callbacks['on_eos']
        old.texture = SimpleNamespace(size=(1280, 720))
        old_frame(old)
        self.assertTrue(first.first_frame)
        self.assertEqual(first.dimensions, (1280, 720))

        second = controller.preview(self.path('second.mp4'), 'video')
        new = FakePlayer.instances[-1]
        self.assertEqual(old.state, 'unloaded')
        self.assertEqual(old.callbacks, {})
        self.assertFalse(second.first_frame)

        old.texture = SimpleNamespace(size=(99, 77))
        old_frame(old)
        old_eos(old)
        self.assertFalse(second.first_frame)
        self.assertIs(controller.current_player, new)

        new.texture = SimpleNamespace(size=(640, 480))
        new.callbacks['on_frame'](new)
        self.assertTrue(second.first_frame)
        self.assertEqual(controller.current_texture.size, (640, 480))

    def test_close_releases_player_callbacks_and_current_texture(self):
        controller = JTSetPreviewController(self.root, FakePlayer, FakeClock)
        result = controller.preview(self.path('clip.mp4'), 'video')
        player = FakePlayer.instances[-1]
        player.texture = SimpleNamespace(size=(852, 480))
        player.callbacks['on_frame'](player)

        controller.close('user-close')

        self.assertEqual(player.state, 'unloaded')
        self.assertEqual(player.callbacks, {})
        self.assertIsNone(controller.current_player)
        self.assertIsNone(controller.current_texture)
        self.assertIsNone(controller.current_result)

    def test_video_probe_reports_open_first_frame_dimensions_duration_and_role_warning(self):
        controller = JTSetPreviewController(self.root, FakePlayer, FakeClock)
        result = controller.preview(self.path('portrait.mp4'), 'video', expected_role='portrait')
        player = FakePlayer.instances[-1]
        player.duration = 7.25
        player.texture = SimpleNamespace(size=(1920, 1080))
        player.callbacks['on_frame'](player)

        self.assertTrue(result.opened)
        self.assertTrue(result.first_frame)
        self.assertEqual(result.dimensions, (1920, 1080))
        self.assertEqual(result.duration, 7.25)
        self.assertTrue(any('orientation' in warning.lower() for warning in result.warnings))

    def test_video_decoder_failure_and_invalid_dimensions_are_bounded_warnings(self):
        bad = str(self.path('bad.mp4'))
        FakePlayer.fail_paths.add(bad)
        controller = JTSetPreviewController(self.root, FakePlayer, FakeClock)
        failed = controller.preview(Path(bad), 'video')
        self.assertFalse(failed.opened)
        self.assertTrue(any('decoder' in warning.lower() for warning in failed.warnings))

        zero = controller.preview(self.path('zero.mp4'), 'video')
        player = FakePlayer.instances[-1]
        player.texture = SimpleNamespace(size=(0, 0))
        player.callbacks['on_frame'](player)
        self.assertFalse(zero.first_frame)
        self.assertTrue(any('dimensions' in warning.lower() for warning in zero.warnings))

    def test_image_and_audio_probe_use_injected_loaders(self):
        image_obj = SimpleNamespace(texture=SimpleNamespace(size=(400, 600)))
        sound = SimpleNamespace(length=3.5, stopped=False, unloaded=False)
        sound.stop = lambda: setattr(sound, 'stopped', True)
        sound.unload = lambda: setattr(sound, 'unloaded', True)
        image_calls, audio_calls = [], []
        controller = JTSetPreviewController(
            self.root, FakePlayer, FakeClock,
            image_loader=lambda path: image_calls.append(path) or image_obj,
            sound_loader=lambda path: audio_calls.append(path) or sound,
        )

        image = controller.preview(self.path('portrait.png'), 'image', expected_role='portrait')
        self.assertTrue(image.opened)
        self.assertTrue(image.first_frame)
        self.assertEqual(image.dimensions, (400, 600))
        audio = controller.preview(self.path('voice.wav'), 'audio')
        self.assertTrue(audio.opened)
        self.assertEqual(audio.duration, 3.5)
        self.assertTrue(image_calls and audio_calls)
        controller.close()
        self.assertTrue(sound.stopped)
        self.assertTrue(sound.unloaded)

    def test_controller_has_no_gameplay_surface_and_preview_events_cannot_mutate_sentinel(self):
        sentinel = {'life': 500000000, 'energy': 61.5, 'round': 1, 'ko': 0}
        controller = JTSetPreviewController(self.root, FakePlayer, FakeClock)
        self.assertFalse(any(hasattr(controller, name) for name in (
            'engine', 'phases', 'apply_damage', 'apply_ko', 'set_energy', 'round_score'
        )))
        result = controller.preview(self.path('safe.mp4'), 'video')
        player = FakePlayer.instances[-1]
        player.texture = SimpleNamespace(size=(800, 450))
        player.callbacks['on_frame'](player)
        player.callbacks['on_eos'](player)
        self.assertEqual(sentinel, {'life': 500000000, 'energy': 61.5, 'round': 1, 'ko': 0})


if __name__ == '__main__':
    unittest.main()
