"""Run the real generated engine/controller with only Kivy/decoder IO replaced.

No Android rendering/audio claim is made by this deterministic harness.
"""
import ast
import importlib.util
import os
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))


class Canvas:
    def __init__(self): self.children = []
    before = property(lambda self: self)
    after = property(lambda self: self)
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def remove_group(self, *args): pass


class Widget:
    def __init__(self, *args, **kwargs):
        self.pos = (0, 0)
        self.size = (2400, 1080)
        self.opacity = 1
        self.text = ""
        self.source = ""
        self.texture = None
        self.children = []
        self.canvas = Canvas()
        self.__dict__.update(kwargs)
    x = property(lambda self: self.pos[0])
    y = property(lambda self: self.pos[1])
    width = property(lambda self: self.size[0])
    height = property(lambda self: self.size[1])
    center = property(lambda self: (self.x+self.width/2, self.y+self.height/2))
    def bind(self, **kwargs): pass
    def unbind(self, **kwargs): pass
    def add_widget(self, child): self.children.append(child)
    def remove_widget(self, child):
        if child in self.children: self.children.remove(child)
    def to_window(self, x, y, **kwargs): return x, y
    def get_parent_window(self): return self


class Rectangle(Widget): pass
class Label(Widget): pass


class Event:
    def __init__(self, callback, delay):
        self.callback, self.delay, self.cancelled = callback, delay, False
    def cancel(self): self.cancelled = True


class Clock:
    now = 100.0
    events = []
    @classmethod
    def get_time(cls): return cls.now
    @classmethod
    def schedule_once(cls, callback, delay=0):
        event = Event(callback, delay)
        cls.events.append(event)
        return event
    schedule_interval = schedule_once


class Sound:
    def play(self): pass
    def stop(self): pass


class Video:
    instances = []
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.texture = None
        self.callbacks = {}
        self.state = ""
        self.position, self.duration = 0.0, 12.0
        self.volume = 0
        self.seeks = []
        self.instances.append(self)
    def bind(self, **kwargs): self.callbacks.update(kwargs)
    def unbind(self, **kwargs):
        for key in kwargs: self.callbacks.pop(key, None)
    def play(self): self.state = "playing"
    def pause(self): self.state = "paused"
    def stop(self): self.state = "stopped"
    def unload(self): self.state = "unloaded"
    def seek(self, fraction, **kwargs): self.seeks.append(fraction)


class App:
    current = None
    @classmethod
    def get_running_app(cls): return cls.current


def execute_without_kivy(source, ns):
    tree = ast.parse(source)
    tree.body = [n for n in tree.body if not (
        isinstance(n, ast.ImportFrom) and n.module.startswith("kivy")
        or isinstance(n, ast.Import) and any(a.name == "kivy" for a in n.names)
    )]
    exec(compile(tree, "<generated-jtrex>", "exec"), ns)


class Harness:
    def __init__(self):
        Clock.now, Clock.events, Video.instances = 100.0, [], []
        graphics = {name: Widget for name in (
            "Color", "Ellipse", "Point", "Button", "Popup", "BoxLayout", "ScrollView"
        )}
        ns = dict(graphics, __name__="jtrex_test", Widget=Widget,
                  FloatLayout=Widget, Label=Label, Rectangle=Rectangle, App=App,
                  Clock=Clock, Window=Widget(), WindowBase=Widget,
                  CoreVideo=Video, Video=Video, GraphicException=Exception,
                  kivy=SimpleNamespace(require=lambda x: None, __version__="test"),
                  SoundLoader=SimpleNamespace(load=lambda x: Sound()),
                  dp=lambda x: x, resource_find=lambda x: x)
        runtime = ModuleType("jtrex_media_runtime")
        runtime.__dict__.update(ns)
        execute_without_kivy((ROOT / "tools/jtrex_media_runtime.py").read_text(), runtime.__dict__)
        sys.modules["jtrex_media_runtime"] = runtime
        spec = importlib.util.spec_from_file_location("prep", ROOT / "tools/prepare_android.py")
        prep = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(prep)
        if "JT_GENERATED_MAIN" in os.environ:
            source = Path(os.environ["JT_GENERATED_MAIN"]).read_text()
        elif "JT_HISTORICAL_MAIN" in os.environ:
            source = prep.adapt_main(Path(os.environ["JT_HISTORICAL_MAIN"]).read_text())
        else:
            source = (ROOT / "app/main.py").read_text()
        execute_without_kivy(source, ns)
        self.ns, self.runtime = ns, runtime
        self.root = ns["jah"]()
        self.app = ns["mainApp"]()
        self.app.root = self.root
        App.current = self.app
        self.media = runtime.JTMediaController(self.app)
        self.app._jt_media = self.media
        self.media._intro_done = True
        if hasattr(self.media, "set_engine"):
            self.media.set_engine(ns)
        self.media.sync_scene_state(0)

    def state(self, indexa):
        self.ns["indexa"] = indexa
        self.media.sync_scene_state(indexa)

    def frame(self):
        player = self.media._scene_player
        player.texture = SimpleNamespace(size=(852, 480))
        self.media._on_scene_frame(player, self.media._scene_generation)

    def eos(self):
        self.media._on_scene_eos(self.media._scene_player, self.media._scene_generation)

    def callbacks(self):
        for name, dt in (("affbt", .05), ("affpv", .5), ("carupdate", 1), ("colvv", .04)):
            getattr(self.root, name)(dt)

    def start_round(self):
        self.state(4)
        self.ns["colstop"] = {i: False for i in range(1, 7)}
        self.state(1)
        self.finish_start()

    def finish_start(self):
        for _ in range(60):
            if self.media._round_overlay is None:
                break
            Clock.now += .05
            self.media._round_overlay._tick(.05)

    def touch(self, name):
        x, y = self.ns['pbout'][name]
        x += self.ns['mdo']; y += self.ns['mdo']
        t = SimpleNamespace(x=x, y=y, pos=(x,y), uid='test', id='1', ud={}, profile=[])
        t.grab = lambda widget: setattr(t, 'grab_current', widget)
        t.ungrab = lambda widget: setattr(t, 'grab_current', None)
        self.last_touch = t
        return self.root.on_touch_down(t)
