#!/usr/bin/env python3
"""Préparation contrôlée de June T-Rex pour Android."""

import argparse
import configparser
import hashlib
import json
import re
import shutil
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

from jtrex_sets_runtime import CATALOG_PATH, POWER_KEYS, load_official_set


VERSION = "1.0.15"
NUMERIC_VERSION = "115"
ARCHIVE_SIZE = 327992765
ARCHIVE_SHA256 = (
    "f73ca1fd5e96ca6e11df5987bda8b2e59"
    "ebac26b1beb23fe34883b15bee66647"
)
MAIN_SHA256 = (
    "3673fb85d12bea18276e485c5956530b4b8"
    "c0dda283cacb022e784bfe8c35231"
)
EXTENSIONS = {"py", "kv", "png", "jpg", "jpeg", "gif", "wav", "mp4", "json"}
EXCLUDED_DIRS = {".kivy", ".buildozer", "__pycache__", "bin"}
LEGACY_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif"}
MP4_ONLY_LEGACY_SEQUENCES = {
    "dinos1": "dinos_",
    "chargetr": "chargetrwin_",
    "chargest": "chargetrwin_",
    "horseg2ko": "chargetrwin_",
    "egtrwin": "egtrwin_",
    "eg2ko": "eg2ko_",
    "stwin": "stwin_",
    "trwin": "trwin_",
    "finishst": "finishst_",
    "finishtr": "finishtr_",
    "stsf": "stsf_",
    "stls": "stls_",
    "stta": "stta_",
    "trfs": "trfs_",
    "trph": "trph_",
    "trma": "trma_",
}
MP4_ONLY_LEGACY_DIRS = frozenset(MP4_ONLY_LEGACY_SEQUENCES)
MP4_ONLY_STATES = (1,2,3,4,5,6,7,8,9,10,11,21,22,23,24,25,26)
APP_ASSETS = {
    "assets/icon/JtrexIcon.png": 2283569,
}



def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def replace_exact(text, old, new, expected):
    actual = text.count(old)
    require(
        actual == expected,
        f"Remplacement refusé pour {old!r}: "
        f"{actual} occurrence(s), {expected} attendue(s).",
    )
    return text.replace(old, new)


def build_power_path_table(selection):
    return {
        slot: selection.power_paths(power_key)
        for slot, power_key in enumerate(POWER_KEYS, 1)
    }


def build_power_parameter_table(selection):
    return {
        slot: selection.power_effect_fraction(power_key)
        for slot, power_key in enumerate(POWER_KEYS, 1)
    }


def rewrite_power_icon_sources(lines, start, end, newline):
    replacements = 0
    for index in range(start, end):
        stripped = lines[index].strip()
        for slot in range(1, 7):
            prefix = f"self.b{slot}.source="
            if not stripped.startswith(prefix):
                continue
            if not (stripped.endswith("1.png'") or stripped.endswith('1.png"')) and not (
                stripped.endswith("0.png'") or stripped.endswith('0.png"')
            ):
                continue
            state = "ready" if "1.png" in stripped.rsplit("=", 1)[-1] else "used"
            indent = lines[index][:len(lines[index]) - len(lines[index].lstrip(" \t"))]
            lines[index] = (
                indent
                + f"self.b{slot}.source=JT_POWER_PATHS[{slot}]['{state}']"
                + newline
            )
            replacements += 1
            break
    return replacements


def _canonical_selection():
    repo_root = Path(__file__).resolve().parents[1]

    def resolve_repo(relative_path):
        path = repo_root.joinpath(*PurePosixPath(relative_path).parts)
        return str(path) if path.is_file() else None

    return load_official_set(resolve_repo)


def _canonical_power_path_table():
    return build_power_path_table(_canonical_selection())


def _canonical_power_parameter_table():
    return build_power_parameter_table(_canonical_selection())


def rewrite_power_effects(source):
    replacements = {
        181: ("degd+=pvd/4", "degd+=pvd*JT_POWER_EFFECT_FRACTIONS[1]"),
        182: ("degg-=pvg/4", "degg-=pvg*JT_POWER_EFFECT_FRACTIONS[2]"),
        183: ("degd+=pvd/4", "degd+=pvd*JT_POWER_EFFECT_FRACTIONS[3]"),
        184: ("degg+=pvg/4", "degg+=pvg*JT_POWER_EFFECT_FRACTIONS[4]"),
        185: ("degg+=pvg/4", "degg+=pvg*JT_POWER_EFFECT_FRACTIONS[5]"),
        186: ("degg+=pvg/3", "degg+=pvg*JT_POWER_EFFECT_FRACTIONS[6]"),
    }
    lines = source.splitlines(keepends=True)
    seen = {marker: 0 for marker in replacements}
    for index in range(len(lines) - 1):
        stripped = lines[index].strip()
        if not stripped.startswith("if anim1==") or not stripped.endswith(":"):
            continue
        try:
            marker = int(stripped[len("if anim1=="):-1])
        except ValueError:
            continue
        if marker not in replacements:
            continue
        old_effect, new_effect = replacements[marker]
        if lines[index + 1].strip() != old_effect:
            continue
        line = lines[index + 1]
        indent = line[:len(line) - len(line.lstrip(" \t"))]
        ending = "\r\n" if line.endswith("\r\n") else ("\n" if line.endswith("\n") else "")
        lines[index + 1] = indent + new_effect + ending
        seen[marker] += 1
    for marker, count in seen.items():
        require(count == 1, f"Jalon pouvoir {marker}: {count} écriture(s), 1 attendue.")
    return "".join(lines)


def method_bounds(lines, method_name):
    target = f"def {method_name}("
    start = None
    base_indent = None
    for index, line in enumerate(lines):
        if line.lstrip().startswith(target):
            start = index
            base_indent = len(line) - len(line.lstrip(" \t"))
            break
    require(start is not None, f"Méthode {method_name} introuvable.")

    end = len(lines)
    for index in range(start + 1, len(lines)):
        stripped = lines[index].strip()
        if not stripped:
            continue
        indent = len(lines[index]) - len(lines[index].lstrip(" \t"))
        if indent <= base_indent:
            end = index
            break
    return start, end


def swap_menu_dinosaur_frame_sources(source):
    """Correct mirrored selection PNGs while keeping historical non-MENU animations.

    jh is left and historically uses d/d_*; jb is right and uses g/g_*.
    g/g_* has visible pixels against its left edge, d/d_* against its right.
    """
    pattern = re.compile(r"""(?P<q>['"])(?P<path>g/g_0\.png|d/d_0\.png|g/g_|d/d_)(?P=q)""")
    counts = {"g/g_0.png": 0, "d/d_0.png": 0, "g/g_": 0, "d/d_": 0}

    def switch(match):
        path, quote = match.group("path"), match.group("q")
        counts[path] += 1
        if path == "g/g_0.png":
            return quote + "d/d_0.png" + quote
        if path == "d/d_0.png":
            return quote + "g/g_0.png" + quote
        if path == "g/g_":
            return "('d/d_' if indexa==0 else 'g/g_')"
        return "('g/g_' if indexa==0 else 'd/d_')"

    patched = pattern.sub(switch, source)
    require(
        all(value == 1 for value in counts.values()),
        "Animation selection dinosaures: exactement une occurrence par "
        "litteral initial/dynamique requise; " + repr(counts),
    )
    return patched


def adapt_main(source, power_paths=None, power_parameters=None):
    newline = "\r\n" if "\r\n" in source else "\n"
    power_paths = power_paths or _canonical_power_path_table()
    power_parameters = power_parameters or _canonical_power_parameter_table()

    source = replace_exact(source, "'a.png'", "'A.png'", 4)
    source = replace_exact(
        source, "'boutbleu0.png'", "'boutBleu0.png'", 4
    )
    source = replace_exact(
        source,
        "b__version__ = '1.0'",
        f"b__version__ = '{VERSION}'"
        + newline
        + 'print("[JT-BOOT] June T-Rex {}: loading Kivy".format('
        + "b__version__), flush=True)",
        1,
    )
    source = replace_exact(
        source, "title = 'Test'", "title = 'June T-Rex'", 1
    )

    # Canonical per-slot power costs approved by Fab. Energy remains float.
    source = replace_exact(
        source,
        "babokepbg,babokepbd=False,False",
        "babokepbg,babokepbd=False,False"
        + newline
        + "POWER_COSTS={1:60,2:40,3:60,4:60,5:60,6:80}"
        + newline
        + "POWER_READY_STATE={1:False,2:False,3:False,4:False,5:False,6:False}"
        + newline
        + "JT_POWER_PATHS=" + repr(power_paths)
        + newline
        + "JT_POWER_EFFECT_FRACTIONS=" + repr(power_parameters)
        + newline
        + "JT_SELECTION_LEFT_OVERHANG_RATIO=0.02"
        + newline
        + "JT_SELECTION_RIGHT_VISUAL_EDGE_RATIO=1.0"
        + newline
        + "JT_SELECTION_RIGHT_OVERHANG_RATIO=0.02"
        + newline
        + "def jt_apply_power_parameters(values):"
        + newline
        + "\tglobal JT_POWER_EFFECT_FRACTIONS"
        + newline
        + "\trequired=set(range(1,7))"
        + newline
        + "\tif set(values)!=required:"
        + newline
        + "\t\traise ValueError('six power parameter slots required')"
        + newline
        + "\tnormalized={}"
        + newline
        + "\tfor slot in range(1,7):"
        + newline
        + "\t\tvalue=values[slot]"
        + newline
        + "\t\tif isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):"
        + newline
        + "\t\t\traise ValueError('finite power parameter required')"
        + newline
        + "\t\tnormalized[slot]=float(value)"
        + newline
        + "\tJT_POWER_EFFECT_FRACTIONS=normalized"
        + newline
        + "def jt_apply_power_paths(paths):"
        + newline
        + "\tglobal JT_POWER_PATHS,sf,ls,ta,fs,ph,maa"
        + newline
        + "\trequired=set(range(1,7))"
        + newline
        + "\tif set(paths)!=required:"
        + newline
        + "\t\traise ValueError('six power slots required')"
        + newline
        + "\tJT_POWER_PATHS={slot:dict(paths[slot]) for slot in range(1,7)}"
        + newline
        + "\taudio_globals={1:'sf',2:'ls',3:'ta',4:'fs',5:'ph',6:'maa'}"
        + newline
        + "\tfor slot,name in audio_globals.items():"
        + newline
        + "\t\told=globals().get(name)"
        + newline
        + "\t\tif old is not None:"
        + newline
        + "\t\t\ttry: old.stop()"
        + newline
        + "\t\t\texcept Exception: pass"
        + newline
        + "\t\tpath=JT_POWER_PATHS[slot].get('activation_audio')"
        + newline
        + "\t\tglobals()[name]=SoundLoader.load(path) if path else None"
        + newline
        + "\t\tif 'sona' in globals():"
        + newline
        + "\t\t\tsona[20+slot]=JT_POWER_PATHS[slot].get('legacy_fallback_audio')"
        + newline
        + "JT_MP4_ONLY_STATES=frozenset((1,2,3,4,5,6,7,8,9,10,11,21,22,23,24,25,26))"
        + newline
        + "def jt_power_available(slot):"
        + newline
        + "\tenergy=stamg if slot<4 else stamd"
        + newline
        + "\tphase=globals().get('_JT_PHASES')"
        + newline
        + "\treturn indexa==1 and (phase is None or phase.round_active) and not selected[slot] and energy>POWER_COSTS[slot]"
        + newline
        + "def jt_refresh_power_flags():"
        + newline
        + "\tfor slot in range(1,7):"
        + newline
        + "\t\tavailable=jt_power_available(slot)"
        + newline
        + "\t\tselect[slot]=available"
        + newline
        + "\t\tbonus[slot]=available"
        + newline
        + "\t\tPOWER_READY_STATE[slot]=available"
        + newline
        + "def jt_sync_scene_now():"
        + newline
        + "\tapp=App.get_running_app()"
        + newline
        + "\tmedia_controller=getattr(app,'_jt_media',None) if app is not None else None"
        + newline
        + "\tif media_controller is not None:"
        + newline
        + "\t\tmedia_controller.sync_scene_state(indexa)",
        1,
    )

    source = swap_menu_dinosaur_frame_sources(source)
    source = rewrite_power_effects(source)

    human_power_guards = {
        1: (
            "if not vsg and bonus[1] and collide(touch.x,touch.y,testx,testy,mdoo):",
            "if not vsg and jt_power_available(1) and collide(touch.x,touch.y,testx,testy,mdoo):",
        ),
        2: (
            "if not vsg and bonus[2] and collide(touch.x,touch.y,testx,testy,mdoo):",
            "if not vsg and jt_power_available(2) and collide(touch.x,touch.y,testx,testy,mdoo):",
        ),
        3: (
            "if not vsg and bonus[3] and collide(touch.x,touch.y,testx,testy,mdo):",
            "if not vsg and jt_power_available(3) and collide(touch.x,touch.y,testx,testy,mdo):",
        ),
        4: (
            "if not vsd and bonus[4] and collide(touch.x,touch.y,testx,testy,mdoo):",
            "if not vsd and jt_power_available(4) and collide(touch.x,touch.y,testx,testy,mdoo):",
        ),
        5: (
            "if not vsd and bonus[5] and collide(touch.x,touch.y,testx,testy,mdoo):",
            "if not vsd and jt_power_available(5) and collide(touch.x,touch.y,testx,testy,mdoo):",
        ),
        6: (
            "if not vsd and bonus[6] and collide(touch.x,touch.y,testx,testy,mdoo):",
            "if not vsd and jt_power_available(6) and collide(touch.x,touch.y,testx,testy,mdoo):",
        ),
    }
    for slot, (old_guard, new_guard) in human_power_guards.items():
        source = replace_exact(source, old_guard, new_guard, 1)

    for slot, state in ((1, 21), (2, 22), (3, 23)):
        source = replace_exact(
            source,
            f"indexa={state};stamg-=60;selected[{slot}]=True",
            (
                f"energy_before=stamg;cost=POWER_COSTS[{slot}];"
                f"stamg-=cost;selected[{slot}]=True;indexa={state};jt_refresh_power_flags();"
                f"print('[JT-POWER] camp=ST slot={slot} state={state} before={{}} cost={{}} after={{}}'.format("
                "energy_before,cost,stamg),flush=True)"
            ),
            1,
        )
    for slot, state in ((4, 24), (5, 25), (6, 26)):
        source = replace_exact(
            source,
            f"indexa={state};stamd-=60;selected[{slot}]=True",
            (
                f"energy_before=stamd;cost=POWER_COSTS[{slot}];"
                f"stamd-=cost;selected[{slot}]=True;indexa={state};jt_refresh_power_flags();"
                f"print('[JT-POWER] camp=TR slot={slot} state={state} before={{}} cost={{}} after={{}}'.format("
                "energy_before,cost,stamd),flush=True)"
            ),
            1,
        )

    source = replace_exact(
        source,
        "if vsg and indexa==1 and computer(10000,lvlg) and stamg>60 and select[i] and not selected[i]:",
        "if vsg and indexa==1 and computer(10000,lvlg) and jt_power_available(i):",
        1,
    )
    source = replace_exact(
        source,
        "selected[i]=True;indexa=20+i;stamg-=60",
        "energy_before=stamg;cost=POWER_COSTS[i];stamg-=cost;selected[i]=True;indexa=20+i;jt_refresh_power_flags();print('[JT-POWER] camp=ST ai=1 slot={} state={} before={} cost={} after={}'.format(i,20+i,energy_before,cost,stamg),flush=True)",
        1,
    )
    source = replace_exact(
        source,
        "if vsd and indexa==1 and computer(10000,lvld) and stamd>60 and select[i] and not selected[i]:",
        "if vsd and indexa==1 and computer(10000,lvld) and jt_power_available(i):",
        1,
    )
    source = replace_exact(
        source,
        "selected[i]=True;indexa=20+i;stamd-=60",
        "energy_before=stamd;cost=POWER_COSTS[i];stamd-=cost;selected[i]=True;indexa=20+i;jt_refresh_power_flags();print('[JT-POWER] camp=TR ai=1 slot={} state={} before={} cost={} after={}'.format(i,20+i,energy_before,cost,stamd),flush=True)",
        1,
    )

    diagnostic_helpers = r"""
_JT_ORIGINAL_COLPTS = colpts
_JT_ORIGINAL_ASB = asb
_JT_STOP_CAUSE = {1:'unknown',2:'unknown',3:'unknown',4:'unknown',5:'unknown',6:'unknown'}
_JT_PREV_COLSTOP = {1:False,2:False,3:False,4:False,5:False,6:False}
_JT_EXCHANGE_ID = 1
_JT_ORB_TOUCH_PROTECT_UNTIL = 0.0

def jt_orb_protected():
    return indexa==1 and Clock.get_time() < _JT_ORB_TOUCH_PROTECT_UNTIL

def _jt_zero_widgets(root, names):
    for name in names:
        widget = getattr(root, name, None)
        if widget is not None:
            try:
                widget.size = (0,0)
            except Exception:
                pass

def jt_hide_power_cinematic_ui(root):
    _jt_zero_widgets(
        root,
        (
            'b1','b2','b3','b4','b5','b6',
            'b1s','b2s','b3s','b4s','b5s','b6s',
            'gr','gg','gb','gj','dr','dg','db','dj',
            'pavé','vh','vb','jh','jb','cadre','calque',
            'vshg','vshd','vscg','vscd',
            'lsg','lsd','lag','lad','lbg','lbd','lcg','lcd','ldg','ldd',
            'start','insertcoin','abcg','abcd',
        ),
    )
    for name in ('label','labelf','label2','label2f'):
        widget = getattr(root, name, None)
        if widget is not None:
            try:
                widget.text = ''
            except Exception:
                pass

def jt_hide_finishing_hud(root):
    _jt_zero_widgets(root, ('nrjg','nrjd','nrjgf','nrjdf','pvg','pvd'))

def colpts():
    global _JT_EXCHANGE_ID
    left_errors = [abs(haut[i]-haut[7]) for i in range(1,4)]
    right_errors = [abs(haut[i]-haut[7]) for i in range(4,7)]
    left_cubes = [value ** 3 for value in left_errors]
    right_cubes = [value ** 3 for value in right_errors]
    left_penalty = sum(left_cubes)
    right_penalty = sum(right_cubes)
    left_score_raw = 150000000-left_penalty
    right_score_raw = 150000000-right_penalty
    left_score = max(0,left_score_raw)
    right_score = max(0,right_score_raw)
    score_diff = abs(left_score-right_score)
    strict_tie = score_diff < 20000
    _JT_ORIGINAL_COLPTS()
    chosen_state = 7 if colptsg and colptsd else (8 if colptsg else 9)
    print(
        '[JT-SCORE][FINAL] exchange={} positions={} target={} chosen_state={} '
        'left_errors={} left_cubes={} left_penalty={} left_raw={} left_score={} '
        'right_errors={} right_cubes={} right_penalty={} right_raw={} right_score={} '
        'diff={} tie_lt_20000={} colptsg={} colptsd={} degdt={} deggt={}'.format(
            _JT_EXCHANGE_ID,
            [haut[i] for i in range(1,7)],
            haut[7],
            chosen_state,
            left_errors,left_cubes,left_penalty,left_score_raw,left_score,
            right_errors,right_cubes,right_penalty,right_score_raw,right_score,
            score_diff,strict_tie,colptsg,colptsd,degdt,deggt,
        ),
        flush=True,
    )
    _JT_EXCHANGE_ID += 1

def asb(self, quia, quib):
    result = _JT_ORIGINAL_ASB(self, quia, quib)
    print(
        '[JT-SCORE][LETTER] exchange={} left={} right={} quia={} quib={}'.format(
            _JT_EXCHANGE_ID,
            getattr(self.abcg,'source',None),
            getattr(self.abcd,'source',None),
            quia,quib,
        ),
        flush=True,
    )
    return result

def _jt_log_new_stops(self, observer):
    rectangles = {1:self.grb,2:self.gvb,3:self.gbb,4:self.drb,5:self.dvb,6:self.dbb}
    targets = {1:self.c3cg,2:self.c3cg,3:self.c3cg,4:self.c3cd,5:self.c3cd,6:self.c3cd}
    for i in range(1,7):
        current = bool(colstop[i])
        previous = bool(_JT_PREV_COLSTOP[i])
        if current and not previous:
            rect = rectangles[i]
            target = targets[i]
            orb_center = (rect.pos[0]+rect.size[0]/2.0, rect.pos[1]+rect.size[1]/2.0)
            target_center = (target.pos[0]+target.size[0]/2.0, target.pos[1]+target.size[1]/2.0)
            signed = orb_center[1]-target_center[1]
            legacy_error = abs(haut[i]-haut[7])
            visual_error = abs(signed)
            texture = getattr(rect,'texture',None)
            target_texture = getattr(target,'texture',None)
            texture_size = getattr(texture,'size',None)
            target_texture_size = getattr(target_texture,'size',None)
            tex_coords = getattr(rect,'tex_coords',None)
            target_tex_coords = getattr(target,'tex_coords',None)
            try:
                widget_window_origin = self.to_window(0,0)
                window_center = self.to_window(orb_center[0],orb_center[1])
                target_window_center = self.to_window(target_center[0],target_center[1])
            except Exception:
                widget_window_origin = (0,0)
                window_center = orb_center
                target_window_center = target_center
            print(
                '[JT-SCORE][STOP] exchange={} orb={} camp={} cause={} observer={} timestamp={} indexa={} '
                'logical_pos={} target_haut={} logical_size={} rect_pos={} rect_size={} '
                'orb_center={} target_pos={} target_size={} target_center={} '
                'widget_window_origin={} window_center={} target_window_center={} '
                'legacy_error={} visual_error={} signed={} texture_size={} target_texture_size={} '
                'tex_coords={} target_tex_coords={} Window={} historical={} mdo={}'.format(
                    _JT_EXCHANGE_ID,i,'ST' if i<4 else 'TR',_JT_STOP_CAUSE[i],observer,time.time(),indexa,
                    (col[i],haut[i]),haut[7],mdo,rect.pos,rect.size,orb_center,target.pos,target.size,target_center,
                    widget_window_origin,window_center,target_window_center,
                    legacy_error,visual_error,signed,texture_size,target_texture_size,
                    tex_coords,target_tex_coords,Window.size,(xmax,ymax),mdo,
                ),
                flush=True,
            )
        _JT_PREV_COLSTOP[i] = current
"""
    source = replace_exact(
        source,
        "class jah(FloatLayout):",
        diagnostic_helpers + newline + "class jah(FloatLayout):",
        1,
    )

    lines = source.splitlines(keepends=True)

    play_indexes = [
        i for i, line in enumerate(lines[:120])
        if line.strip() == "ma.play()"
    ]
    require(len(play_indexes) == 1, "Lecture initiale jtrm0.wav non identifiée.")
    i = play_indexes[0]
    indent = lines[i][: len(lines[i]) - len(lines[i].lstrip(" \t"))]
    lines[i] = (
        indent
        + 'print("[JT-MEDIA] menu music deferred until intro end", flush=True)'
        + newline
    )

    start, end = method_bounds(lines, "on_start")
    replacement = [
        "    def on_start(self):" + newline,
        '        print("[JT-START] on_start; Kivy={}; window={}".format('
        'kivy.__version__, Window.size), flush=True)' + newline,
        "        Clock.max_iteration = 100000" + newline,
        "        try:" + newline,
        "            from jtrex_media_runtime import JTMediaController" + newline,
        "            self._jt_media = JTMediaController(self)" + newline,
        "            self._jt_media.set_engine(globals())" + newline,
        "            self._jt_media.set_legacy_catalog(namea, longanim1, genrea, sona)" + newline,
        "            self._jt_media.start_intro(self._jt_start_gameplay)" + newline,
        "        except Exception as exc:" + newline,
        '            print("[JT-INTRO][ERROR] controller={!r}; continuing".format('
        "exc), flush=True)" + newline,
        "            self._jt_start_gameplay()" + newline,
        newline,
        "    def _jt_start_gameplay(self):" + newline,
        "        global ma" + newline,
        "        if getattr(self, '_jt_gameplay_started', False):" + newline,
        "            return" + newline,
        "        self._jt_gameplay_started = True" + newline,
        "        if ma is not None:" + newline,
        "            ma.stop()" + newline,
        "            ma.loop = True" + newline,
        "            ma.volume = 0.5" + newline,
        "            ma.play()" + newline,
        '        print("[JT-INTRO] gameplay enabled", flush=True)' + newline,
        "        Clock.schedule_interval(self.root.screen_up, 0.04)" + newline,
        "        Clock.schedule_interval(self.root.ga, 0.04)" + newline,
        "        Clock.schedule_interval(self.root.pter, 0.05)" + newline,
        "        Clock.schedule_interval(self.root.da, 0.04)" + newline,
        "        Clock.schedule_interval(self.root.colvv, 0.04)" + newline,
        "        Clock.schedule_interval(self.root.affpv, 0.5)" + newline,
        "        Clock.schedule_interval(self.root.mc1, 0.03)" + newline,
        "        Clock.schedule_interval(self.root.affbt, 0.05)" + newline,
        "        # carupdate is scheduled by the presentation phase after START." + newline,
        newline,
        "    def _jt_set_native_scene_audio(self, active, state):" + newline,
        "        global ma, sona0, sona" + newline,
        "        if active:" + newline,
        "            if ma is not None:" + newline,
        "                ma.stop()" + newline,
        "            print('[JT-SCENE] AUDIO_LEGACY suppressed state={}'.format(state), flush=True)" + newline,
        "            return" + newline,
        "        if state not in sona:" + newline,
        "            return" + newline,
        "        legacy = sona[state]" + newline,
        "        if ma is not None:" + newline,
        "            ma.stop()" + newline,
        "        sona0 = legacy" + newline,
        "        ma = SoundLoader.load(legacy)" + newline,
        "        if ma is not None:" + newline,
        "            ma.loop = state not in (2,3,4,5,6,7)" + newline,
        "            ma.play()" + newline,
        "        print('[JT-SCENE] AUDIO_LEGACY fallback state={} source={}'.format(state, legacy), flush=True)" + newline,
        newline,
    ]
    lines[start:end] = replacement

    # The red MENU aiming reticles are two identical "viseur.png" rectangles:
    # vh follows historical (xh, yh), vb follows (xb, yb). Their visual
    # assignment is reversed with respect to the selection dinosaurs.
    # Swap ONLY their rendered horizontal tracking while indexa == 0.
    # Do not swap global xh/xb or their touch/collision/gameplay roles.
    vh_pos_matches = [
        index for index, line in enumerate(lines)
        if line.strip().replace(" ", "").startswith("self.vh.pos=")
    ]
    vb_pos_matches = [
        index for index, line in enumerate(lines)
        if line.strip().replace(" ", "").startswith("self.vb.pos=")
    ]
    require(
        len(vh_pos_matches) == len(vb_pos_matches) == 1,
        "Viseurs menu : affectation unique self.vh.pos et self.vb.pos requise.",
    )
    vh_pos_index, vb_pos_index = vh_pos_matches[0], vb_pos_matches[0]
    require(
        vb_pos_index == vh_pos_index + 1,
        "Viseurs menu : affectations historiques non consecutives.",
    )
    vh_line, vb_line = lines[vh_pos_index], lines[vb_pos_index]
    vh_indent = vh_line[:len(vh_line) - len(vh_line.lstrip(" \t"))]
    vb_indent = vb_line[:len(vb_line) - len(vb_line.lstrip(" \t"))]
    require(vh_indent == vb_indent, "Viseurs menu : indentation incoherente.")
    vh_rhs = vh_line.strip().split("=", 1)[1]
    vb_rhs = vb_line.strip().split("=", 1)[1]
    lines[vh_pos_index:vb_pos_index + 1] = [
        vh_indent + "_jt_vh_render_pos=" + vh_rhs + newline,
        vh_indent + "_jt_vb_render_pos=" + vb_rhs + newline,
        vh_indent + "if indexa==0:" + newline,
        vh_indent + "\tself.vh.pos=(_jt_vb_render_pos[0],_jt_vh_render_pos[1])" + newline,
        vh_indent + "\tself.vb.pos=(_jt_vh_render_pos[0],_jt_vb_render_pos[1])" + newline,
        vh_indent + "else:" + newline,
        vh_indent + "\tself.vh.pos=_jt_vh_render_pos" + newline,
        vh_indent + "\tself.vb.pos=_jt_vb_render_pos" + newline,
    ]

    # The left selection dinosaur has a valid left stop historically, but no
    # rightward MENU stop. Keep its natural X when farther left, and otherwise
    # clamp its rectangle LEFT edge to the viewport LEFT edge minus 2%.
    # Do this at the canonical pre-render assignment without touching Y or size.
    jh_pos_matches = [
        index for index, line in enumerate(lines)
        if line.strip().replace(" ", "").startswith("self.jh.pos=")
    ]
    require(
        len(jh_pos_matches) == 1,
        f"Position dino gauche self.jh.pos: {len(jh_pos_matches)} occurrence(s), 1 attendue.",
    )
    jh_pos_index = jh_pos_matches[0]
    jh_line = lines[jh_pos_index]
    jh_indent = jh_line[: len(jh_line) - len(jh_line.lstrip(" \t"))]
    jh_rhs = jh_line.strip().split("=", 1)[1]
    lines[jh_pos_index:jh_pos_index + 1] = [
        jh_indent + "_jt_jh_render_pos=" + jh_rhs + newline,
        jh_indent + "if indexa==0:" + newline,
        jh_indent + "\t_jt_jh_max_x=self.x-self.width*JT_SELECTION_LEFT_OVERHANG_RATIO" + newline,
        jh_indent + "\tself.jh.pos=(min(_jt_jh_render_pos[0],_jt_jh_max_x),_jt_jh_render_pos[1])" + newline,
        jh_indent + "else:" + newline,
        jh_indent + "\tself.jh.pos=_jt_jh_render_pos" + newline,
    ]

    # Bound the intentionally cropped right selection dinosaur before rendering.
    # The historical renderer owns self.jb.pos outside screen_up; patch the one
    # canonical display assignment directly so there is no post-render snap.
    jb_pos_matches = [
        index for index, line in enumerate(lines)
        if line.strip().replace(" ", "").startswith("self.jb.pos=")
    ]
    require(
        len(jb_pos_matches) == 1,
        f"Position dino droit self.jb.pos: {len(jb_pos_matches)} occurrence(s), 1 attendue.",
    )
    jb_pos_index = jb_pos_matches[0]
    jb_line = lines[jb_pos_index]
    jb_indent = jb_line[: len(jb_line) - len(jb_line.lstrip(" \t"))]
    jb_rhs = jb_line.strip().split("=", 1)[1]
    lines[jb_pos_index:jb_pos_index + 1] = [
        jb_indent + "_jt_jb_render_pos=" + jb_rhs + newline,
        jb_indent + "if indexa==0:" + newline,
        jb_indent + "\t_jt_jb_parent_right=self.x+self.width" + newline,
        jb_indent + "\t_jt_jb_target_visual_right=_jt_jb_parent_right+self.width*JT_SELECTION_RIGHT_OVERHANG_RATIO" + newline,
        jb_indent + "\t_jt_jb_visual_right_in_rect=self.jb.size[0]*JT_SELECTION_RIGHT_VISUAL_EDGE_RATIO" + newline,
        jb_indent + "\t_jt_jb_min_x=_jt_jb_target_visual_right-_jt_jb_visual_right_in_rect" + newline,
        jb_indent + "\tself.jb.pos=(max(_jt_jb_render_pos[0],_jt_jb_min_x),_jt_jb_render_pos[1])" + newline,
        jb_indent + "else:" + newline,
        jb_indent + "\tself.jb.pos=_jt_jb_render_pos" + newline,
    ]

    # Synchronize video after all historical transitions in mc1.
    start, end = method_bounds(lines, "mc1")
    global_index = None
    for index in range(start + 1, min(end, start + 12)):
        if lines[index].lstrip().startswith("global timea0"):
            global_index = index
            break
    require(global_index is not None, "Global de mc1 non identifié.")
    body_indent = lines[global_index][
        : len(lines[global_index]) - len(lines[global_index].lstrip(" \t"))
    ]
    hook = [
        body_indent + "media_controller = getattr(App.get_running_app(), '_jt_media', None)" + newline,
        body_indent + "if media_controller is not None:" + newline,
        body_indent + "\tmedia_controller.sync_scene_state(indexa)" + newline,
    ]
    lines[end:end] = hook

    start, end = method_bounds(lines, "anim_1")
    aff_index = None
    source_index = None
    for index in range(start, end):
        if lines[index].strip() == "if aff:":
            for j in range(index + 1, min(end, index + 6)):
                if "self.deux.source=" in lines[j].replace(" ", ""):
                    aff_index = index
                    source_index = j
                    break
            if source_index is not None:
                break
    require(source_index is not None, "Affectation visuelle self.deux.source non identifiée.")
    src_indent = lines[source_index][
        : len(lines[source_index]) - len(lines[source_index].lstrip(" \t"))
    ]
    if_indent = lines[aff_index][
        : len(lines[aff_index]) - len(lines[aff_index].lstrip(" \t"))
    ]
    unit = src_indent[len(if_indent):] or "\t"
    original_source = lines[source_index].lstrip(" \t")
    lines[source_index:source_index + 1] = [
        src_indent + "if not getattr(self, '_jt_scene_video_active', False) and indexa not in JT_MP4_ONLY_STATES:" + newline,
        src_indent + unit + original_source,
    ]

    # Keep historical scene audio as fallback until the first usable video frame.
    start, end = method_bounds(lines, "anim_1")
    load_index = None
    loop_end = None
    for index in range(start, end):
        if lines[index].strip() == "ma = SoundLoader.load(sona0)":
            load_index = index
            break
    require(load_index is not None, "Chargement audio historique anim_1 introuvable.")
    for index in range(load_index, end):
        if lines[index].strip() == "ma.loop=True":
            loop_end = index
            break
    require(loop_end is not None, "Fin du bloc audio historique anim_1 introuvable.")
    audio_indent = lines[load_index][
        : len(lines[load_index]) - len(lines[load_index].lstrip(" \t"))
    ]
    audio_unit = "\t"
    for index in range(load_index, loop_end + 1):
        lines[index] = audio_indent + audio_unit + lines[index][len(audio_indent):]
    lines[load_index:load_index] = [
        audio_indent + "if not getattr(self, '_jt_scene_video_active', False):" + newline,
        audio_indent + audio_unit
        + "print('[JT-SCENE] AUDIO_LEGACY start state={} anim={} source={}'.format(indexa,anim1,sona0),flush=True)" + newline,
    ]

    # Rebuild power availability from one canonical rule.
    start, end = method_bounds(lines, "affpv")
    first = second = finish = None
    for index in range(start, end):
        stripped = lines[index].strip()
        if stripped == "for i in range(1,4):" and first is None:
            first = index
        elif stripped == "for i in range(4,7):" and first is not None and second is None:
            second = index
        elif stripped == "b=1/pvd*degd" and second is not None:
            finish = index
            break
    require(
        first is not None and second is not None and finish is not None,
        "Boucles de disponibilité des pouvoirs introuvables.",
    )
    indent = lines[first][: len(lines[first]) - len(lines[first].lstrip(" \t"))]
    unit = "\t"
    power_block = [
        indent + "new_power_available=False" + newline,
        indent + "for i in range(1,7):" + newline,
        indent + unit + "available=jt_power_available(i)" + newline,
        indent + unit + "if available and not POWER_READY_STATE[i]:" + newline,
        indent + unit + unit + "new_power_available=True" + newline,
        indent + unit + "POWER_READY_STATE[i]=available" + newline,
        indent + unit + "select[i]=available" + newline,
        indent + unit + "bonus[i]=available" + newline,
        indent + "babokepbg=any(POWER_READY_STATE[i] for i in range(1,4))" + newline,
        indent + "babokepbd=any(POWER_READY_STATE[i] for i in range(4,7))" + newline,
        indent + "if new_power_available and indexa==1:" + newline,
        indent + unit + "baboke.play()" + newline,
    ]
    lines[first:finish] = power_block

    # Power item identity is data-driven; gameplay availability remains engine-owned.
    start, end = method_bounds(lines, "affbt")
    power_icon_rewrites = rewrite_power_icon_sources(lines, start, end, newline)
    require(
        power_icon_rewrites == 12,
        f"Identité visuelle des pouvoirs: {power_icon_rewrites} remplacement(s), 12 attendus.",
    )

    # Canonical rotating aura: b1s..b6s are the animated select/select0..15 overlays.
    start, end = method_bounds(lines, "affbt")
    method_indent = len(lines[start]) - len(lines[start].lstrip(" \t"))
    body_indent = None
    for index in range(start + 1, end):
        if not lines[index].strip():
            continue
        current_indent = len(lines[index]) - len(lines[index].lstrip(" \t"))
        if current_indent > method_indent:
            body_indent = lines[index][:current_indent]
            break
    require(body_indent is not None, "Indentation de affbt introuvable.")
    aura_block = [
        body_indent + "self.b1s.size=(mdo,mdo) if jt_power_available(1) else (0,0)" + newline,
        body_indent + "self.b2s.size=(mdo,mdo) if jt_power_available(2) else (0,0)" + newline,
        body_indent + "self.b3s.size=(mdo,mdo) if jt_power_available(3) else (0,0)" + newline,
        body_indent + "self.b4s.size=(mdo,mdo) if jt_power_available(4) else (0,0)" + newline,
        body_indent + "self.b5s.size=(mdo,mdo) if jt_power_available(5) else (0,0)" + newline,
        body_indent + "self.b6s.size=(mdo,mdo) if jt_power_available(6) else (0,0)" + newline,
        body_indent + "if getattr(self, '_jt_power_video_hold', False):" + newline,
        body_indent + "\tjt_hide_power_cinematic_ui(self)" + newline,
        body_indent + "\tself._jt_power_controls_were_hidden=True" + newline,
        body_indent + "\treturn" + newline,
        body_indent + "if getattr(self, '_jt_power_controls_were_hidden', False):" + newline,
        body_indent + "\tself._jt_power_controls_were_hidden=False" + newline,
        body_indent + "\tindexa0=-999" + newline,
        body_indent + "if getattr(self, '_jt_finishing_video_hold', False):" + newline,
        body_indent + "\tjt_hide_finishing_hud(self)" + newline,
    ]
    lines[end:end] = aura_block

    # Touch safety: power/finishing cinematics swallow gameplay touches.
    # Orb stop controls are active only in the real orb phase and only after the
    # two-second charge-entry freeze/protection window has elapsed.
    start, end = method_bounds(lines, "on_touch_down")
    global_lines = [
        index
        for index in range(start + 1, min(end, start + 40))
        if lines[index].lstrip().startswith("global ")
    ]
    require(global_lines, "Globals de on_touch_down introuvables.")
    insert_at = max(global_lines) + 1
    touch_body_indent = lines[global_lines[-1]][
        : len(lines[global_lines[-1]]) - len(lines[global_lines[-1]].lstrip(" \t"))
    ]
    lines[insert_at:insert_at] = [
        touch_body_indent + "if getattr(self, '_jt_scene_cinematic_lock', False):" + newline,
        touch_body_indent + "\treturn True" + newline,
    ]

    start, end = method_bounds(lines, "on_touch_down")
    replacements = []
    for index in range(start, end):
        compact = lines[index].strip().replace(" ", "")
        if compact.startswith("colstop[") and compact.endswith("]=True"):
            slot_text = compact[len("colstop["):-len("]=True")]
            if slot_text.isdigit() and 1 <= int(slot_text) <= 6:
                prefix = lines[index][: len(lines[index]) - len(lines[index].lstrip(" \t"))]
                original = lines[index].lstrip(" \t").rstrip("\r\n")
                replacements.append(
                    (
                        index,
                        [
                            prefix + "if indexa==1 and not jt_orb_protected():" + newline,
                            prefix + "\t" + original + newline,
                            prefix + "\t" + f"_JT_STOP_CAUSE[{slot_text}]='human'" + newline,
                        ],
                    )
                )
    require(len(replacements) == 6, f"Protections orbes tactiles: {len(replacements)} arrêt(s), 6 attendus.")
    for index, replacement in reversed(replacements):
        lines[index:index + 1] = replacement

    start, end = method_bounds(lines, "on_touch_down")
    touch_return = None
    for index in range(end - 1, start, -1):
        if lines[index].strip() == "return True":
            touch_return = index
            break
    require(touch_return is not None, "return True final de on_touch_down introuvable.")
    touch_body_indent = lines[touch_return][
        : len(lines[touch_return]) - len(lines[touch_return].lstrip(" \t"))
    ]
    lines[touch_return:touch_return] = [
        touch_body_indent + "jt_sync_scene_now()" + newline,
    ]

    # Arm the two-second freeze exactly when a red/blue charge state (2/3/4)
    # completes and the historical engine enters the six-orb phase (indexa=1).
    start, end = method_bounds(lines, "anim_1")
    anim_global_lines = [
        index
        for index in range(start + 1, min(end, start + 20))
        if lines[index].lstrip().startswith("global ")
    ]
    require(anim_global_lines, "Globals de anim_1 introuvables.")
    anim_global_at = max(anim_global_lines) + 1
    anim_body_indent = lines[anim_global_lines[-1]][
        : len(lines[anim_global_lines[-1]]) - len(lines[anim_global_lines[-1]].lstrip(" \t"))
    ]
    lines[anim_global_at:anim_global_at] = [
        anim_body_indent + "global _JT_ORB_TOUCH_PROTECT_UNTIL" + newline,
        anim_body_indent + "if getattr(self, '_jt_power_video_hold', False) and indexa in (1,10,11):" + newline,
        anim_body_indent + "\treturn" + newline,
        anim_body_indent + "if indexa in (10,11):" + newline,
        anim_body_indent + "\t_jt_finish_pending=getattr(self, '_jt_finishing_complete_pending', None)" + newline,
        anim_body_indent + "\tif _jt_finish_pending==indexa:" + newline,
        anim_body_indent + "\t\tself._jt_finishing_complete_pending=None" + newline,
        anim_body_indent + "\t\tstopg,stopd=False,False" + newline,
        anim_body_indent + "\t\t_finished_state=indexa" + newline,
        anim_body_indent + "\t\tanim1,indexa=0,0" + newline,
        anim_body_indent + "\t\tfor ii in range(1,7):" + newline,
        anim_body_indent + "\t\t\tcolstop[ii]=False" + newline,
        anim_body_indent + "\t\tprint('[JT-FINISH] video-complete state={} -> menu'.format(_finished_state),flush=True)" + newline,
        anim_body_indent + "\t\tjt_sync_scene_now()" + newline,
        anim_body_indent + "\t\treturn" + newline,
        anim_body_indent + "\tif getattr(self, '_jt_finishing_video_hold', False):" + newline,
        anim_body_indent + "\t\treturn" + newline,
    ]
    start, end = method_bounds(lines, "anim_1")
    transition_matches = [
        index for index in range(start, end)
        if lines[index].strip().replace(" ", "") == "anim1,indexa=0,1"
    ]
    require(len(transition_matches) == 1, f"Transition charge→orbes: {len(transition_matches)} occurrence(s), 1 attendue.")
    transition = transition_matches[0]
    prefix = lines[transition][: len(lines[transition]) - len(lines[transition].lstrip(" \t"))]
    lines[transition:transition + 1] = [
        prefix + "_jt_charge_state=indexa" + newline,
        prefix + "anim1,indexa=0,1" + newline,
        prefix + "if _jt_charge_state in (2,3,4):" + newline,
        prefix + "\t_JT_ORB_TOUCH_PROTECT_UNTIL=Clock.get_time()+2.0" + newline,
        prefix + "\tprint('[JT-ORB] charge-entry freeze+protection 2.0s from_state={}'.format(_jt_charge_state),flush=True)" + newline,
    ]

    start, end = method_bounds(lines, "carupdate")
    car_global_lines = [
        index
        for index in range(start + 1, min(end, start + 20))
        if lines[index].lstrip().startswith("global ")
    ]
    require(car_global_lines, "Globals de carupdate introuvables.")
    car_hold_at = max(car_global_lines) + 1
    car_body_indent = lines[car_global_lines[-1]][
        : len(lines[car_global_lines[-1]]) - len(lines[car_global_lines[-1]].lstrip(" \t"))
    ]
    lines[car_hold_at:car_hold_at] = [
        car_body_indent + "if getattr(self, '_jt_power_video_hold', False):" + newline,
        car_body_indent + "\treturn" + newline,
    ]

    # An AI power can be selected inside carupdate itself. Leave immediately
    # before the legacy non-orb branch resets car2 to 10 in that same callback.
    start, end = method_bounds(lines, "carupdate")
    after_ai = [i for i in range(start, end) if lines[i].strip() == "allstopcar=0"]
    require(len(after_ai) == 1, "Sortie IA avant chronomètres introuvable.")
    lines[after_ai[0]:after_ai[0]] = [
        car_body_indent + "if indexa in (21,22,23,24,25,26):" + newline,
        car_body_indent + "\tjt_sync_scene_now()" + newline,
        car_body_indent + "\treturn" + newline,
    ]

    start, end = method_bounds(lines, "carupdate")
    car_guard_rules = {
        "if car2on and indexa==1:": "if car2on and indexa==1 and not jt_orb_protected():",
        "if indexa==1 and not stopd and not stopg:": "if indexa==1 and not stopd and not stopg and not jt_orb_protected():",
    }
    car_guard_hits = {key: 0 for key in car_guard_rules}
    for index in range(start, end):
        stripped = lines[index].strip()
        if stripped in car_guard_rules:
            prefix = lines[index][: len(lines[index]) - len(lines[index].lstrip(" \t"))]
            lines[index] = prefix + car_guard_rules[stripped] + newline
            car_guard_hits[stripped] += 1
    require(all(value == 1 for value in car_guard_hits.values()), f"Gardes timers orbes incohérentes: {car_guard_hits}.")

    start, end = method_bounds(lines, "carupdate")
    for index in range(start, end):
        if lines[index].strip().replace(" ", "") == "colstop[i]=True":
            prefix = lines[index][: len(lines[index]) - len(lines[index].lstrip(" \t"))]
            lines[index + 1:index + 1] = [prefix + "_JT_STOP_CAUSE[i]='timeout'" + newline]
            break
    else:
        raise RuntimeError("Arrêt timeout carupdate introuvable.")
    start, end = method_bounds(lines, "carupdate")
    car_body_indent = lines[start + 1][
        : len(lines[start + 1]) - len(lines[start + 1].lstrip(" \t"))
    ]
    lines[end:end] = [car_body_indent + "jt_sync_scene_now()" + newline]

    start, end = method_bounds(lines, "colvv")
    moving_branches = [
        index for index in range(start, end)
        if lines[index].strip() == "if not colstop[i]:"
    ]
    require(len(moving_branches) == 1, f"Branche mouvement orbes: {len(moving_branches)} occurrence(s), 1 attendue.")
    moving_branch = moving_branches[0]
    prefix = lines[moving_branch][: len(lines[moving_branch]) - len(lines[moving_branch].lstrip(" \t"))]
    lines[moving_branch + 1:moving_branch + 1] = [
        prefix + "\tif jt_orb_protected():" + newline,
        prefix + "\t\tcontinue" + newline,
    ]

    start, end = method_bounds(lines, "colvv")
    ai_insertions = []
    global_index = None
    for index in range(start, end):
        stripped = lines[index].strip().replace(" ", "")
        if lines[index].lstrip().startswith("global ") and global_index is None:
            global_index = index
        if stripped == "colstop[i]=True":
            prefix = lines[index][: len(lines[index]) - len(lines[index].lstrip(" \t"))]
            ai_insertions.append((index + 1, prefix + "_JT_STOP_CAUSE[i]='ai'" + newline))
    require(global_index is not None, "Global de colvv introuvable.")
    for index, line in reversed(ai_insertions):
        lines[index:index] = [line]
    start, end = method_bounds(lines, "colvv")
    body_indent = lines[start + 1][: len(lines[start + 1]) - len(lines[start + 1].lstrip(" \t"))]
    lines[start + 2:start + 2] = [
        body_indent + "if getattr(self, '_jt_power_video_hold', False):" + newline,
        body_indent + "\treturn" + newline,
        body_indent + "_jt_log_new_stops(self, 'colvv-pre-update')" + newline,
    ]
    start, end = method_bounds(lines, "colvv")
    lines[end:end] = [
        body_indent + "_jt_log_new_stops(self, 'colvv-post-update')" + newline,
        body_indent + "jt_sync_scene_now()" + newline,
    ]

    start, end = method_bounds(lines, "on_pause")
    lifecycle = [
        "    def on_pause(self):" + newline,
        "        media_controller = getattr(self, '_jt_media', None)" + newline,
        "        if media_controller is not None:" + newline,
        "            media_controller.on_pause()" + newline,
        "        return True" + newline,
        newline,
        "    def on_resume(self):" + newline,
        "        media_controller = getattr(self, '_jt_media', None)" + newline,
        "        if media_controller is not None:" + newline,
        "            media_controller.on_resume()" + newline,
        newline,
        "    def on_stop(self):" + newline,
        "        media_controller = getattr(self, '_jt_media', None)" + newline,
        "        if media_controller is not None:" + newline,
        "            media_controller.shutdown()" + newline,
        newline,
    ]
    lines[start:end] = lifecycle

    result = "".join(lines)
    result = replace_exact(
        result, "class mainApp(App):",
        "from jtrex_phase_runtime import install_phase_hooks" + newline
        + "install_phase_hooks(jah, globals())" + newline + newline
        + "class mainApp(App):", 1,
    )
    require(
        result.count("[JT-START] on_start") == 1,
        "Trace JT-START incohérente après adaptation média.",
    )
    compile(result, "JuneTrex/main.py", "exec")
    return result


def prepare(archive, destination, spec, media_root, runtime):
    require(archive.is_file(), "Archive absente.")
    require(
        archive.stat().st_size == ARCHIVE_SIZE,
        "Taille de l'archive différente de la référence.",
    )
    require(
        digest(archive) == ARCHIVE_SHA256,
        "SHA-256 de l'archive différent de la référence.",
    )
    require(spec.is_file(), "buildozer.spec absent.")
    require(media_root.is_dir(), "Dossier assets absent.")
    require(runtime.is_file(), "Runtime vidéo absent.")
    sets_runtime = runtime.with_name("jtrex_sets_runtime.py")
    require(sets_runtime.is_file(), "Runtime de sets absent.")
    sets_io_runtime = runtime.with_name("jtrex_sets_io.py")
    require(sets_io_runtime.is_file(), "Runtime I/O de sets absent.")
    sets_admin_runtime = runtime.with_name("jtrex_sets_admin.py")
    require(sets_admin_runtime.is_file(), "Runtime admin de sets absent.")
    sets_preview_runtime = runtime.with_name("jtrex_sets_preview.py")
    require(sets_preview_runtime.is_file(), "Runtime preview de sets absent.")
    sets_android_runtime = runtime.with_name("jtrex_sets_android.py")
    require(sets_android_runtime.is_file(), "Runtime Android de sets absent.")
    repo_root = media_root.parent
    def resolve_repo(relative_path):
        path = repo_root.joinpath(*PurePosixPath(relative_path).parts)
        return str(path) if path.is_file() else None
    selection = load_official_set(resolve_repo)
    manifest_source = repo_root.joinpath(*PurePosixPath(selection.manifest_path).parts)
    catalog_source = repo_root.joinpath(*PurePosixPath(CATALOG_PATH).parts)
    require(catalog_source.is_file(), "Catalogue de sets absent.")
    require(manifest_source.is_file(), "Manifeste canonique absent.")
    canonical_manifest_sha256 = digest(manifest_source)
    require(
        not destination.exists(),
        "Le dossier de sortie existe déjà : aucun écrasement effectué.",
    )

    config = configparser.ConfigParser(interpolation=None)
    config.read_string(spec.read_text(encoding="utf-8"))
    require(
        config.get("app", "version") == VERSION,
        "Version du buildozer.spec incohérente avec la préparation.",
    )
    require(
        config.get("app", "android.numeric_version") == NUMERIC_VERSION,
        "versionCode Android incohérent.",
    )
    require(
        config.get("app", "package.name") == "junetrex"
        and config.get("app", "package.domain") == "com.junedady",
        "Identité du paquet différente de la référence.",
    )
    include_exts = {
        item.strip().lower()
        for item in config.get("app", "source.include_exts").split(",")
    }
    require("mp4" in include_exts, "MP4 absent de source.include_exts.")
    require("json" in include_exts, "JSON absent de source.include_exts.")
    requirements = config.get("app", "requirements")
    require(
        "ffpyplayer" in requirements,
        "ffpyplayer absent des requirements.",
    )
    require(
        "python3==3.12.14" in requirements,
        "Python cible doit rester figé sur 3.12.14 pour ffpyplayer.",
    )

    destination.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(
        prefix="jtrex-prepare-", dir=destination.parent
    ) as temporary:
        stage = Path(temporary) / "app"
        stage.mkdir()
        extracted = set()
        pruned_legacy_image_files = 0
        pruned_legacy_image_bytes = 0
        pruned_legacy_image_dirs = set()
        preserved_legacy_nonframe_images = 0
        preserved_legacy_nonframe_bytes = 0

        with zipfile.ZipFile(archive) as bundle:
            require(
                "JuneTrex/main.py" in bundle.namelist(),
                "JuneTrex/main.py absent : mauvaise archive ou racine.",
            )

            for entry in sorted(
                bundle.infolist(), key=lambda item: item.filename
            ):
                path = PurePosixPath(entry.filename)

                if not path.parts or path.parts[0] != "JuneTrex":
                    continue

                require(
                    "\\" not in entry.filename
                    and ".." not in path.parts,
                    f"Chemin d'archive refusé : {entry.filename!r}",
                )

                relative = PurePosixPath(*path.parts[1:])
                if entry.is_dir() or not relative.parts:
                    continue
                if any(
                    part in EXCLUDED_DIRS
                    for part in relative.parts[:-1]
                ):
                    continue
                if relative.suffix.lstrip(".").lower() not in EXTENSIONS:
                    continue

                if (
                    relative.suffix.lower() == ".py"
                    and relative != PurePosixPath("main.py")
                ):
                    continue

                if (
                    relative.parts
                    and relative.parts[0] in MP4_ONLY_LEGACY_SEQUENCES
                    and relative.suffix.lower() in LEGACY_IMAGE_EXTENSIONS
                ):
                    legacy_dir = relative.parts[0]
                    legacy_prefix = MP4_ONLY_LEGACY_SEQUENCES[legacy_dir]
                    if relative.name.startswith(legacy_prefix):
                        pruned_legacy_image_files += 1
                        pruned_legacy_image_bytes += entry.file_size
                        pruned_legacy_image_dirs.add(legacy_dir)
                        continue
                    preserved_legacy_nonframe_images += 1
                    preserved_legacy_nonframe_bytes += entry.file_size

                name = relative.as_posix()
                require(
                    name not in extracted,
                    f"Entrée dupliquée dans l'archive : {name}",
                )
                extracted.add(name)

                target = stage.joinpath(*relative.parts)
                target.parent.mkdir(parents=True, exist_ok=True)
                with bundle.open(entry) as incoming:
                    with target.open("wb") as outgoing:
                        shutil.copyfileobj(incoming, outgoing)

        main = stage / "main.py"
        require(
            digest(main) == MAIN_SHA256,
            "main.py ne correspond pas à la référence auditée.",
        )

        original = main.read_bytes().decode("utf-8")
        adapted = adapt_main(
            original,
            build_power_path_table(selection),
            build_power_parameter_table(selection),
        )
        main.write_bytes(adapted.encode("utf-8"))

        app_asset_report = {}
        for target_name, expected_size in APP_ASSETS.items():
            rel = PurePosixPath(target_name)
            source = repo_root.joinpath(*rel.parts)
            require(source.is_file(), f"Ressource application absente : {target_name}")
            require(source.stat().st_size == expected_size, f"Taille inattendue pour {target_name}")
            target = stage.joinpath(*rel.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            app_asset_report[target_name] = {"size": target.stat().st_size, "sha256": digest(target)}

        canonical_set_assets = {}
        for asset in selection.assets():
            target_name = asset["path"]
            rel = PurePosixPath(target_name)
            target = stage.joinpath(*rel.parts)
            if rel.parts and rel.parts[0] == "assets":
                source = repo_root.joinpath(*rel.parts)
                require(source.is_file(), f"Ressource set fournie absente : {target_name}")
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
            require(target.is_file(), f"Ressource set absente après préparation : {target_name}")
            require(target.stat().st_size == asset["size"], f"Taille set inattendue pour {target_name}")
            actual_sha = digest(target)
            require(actual_sha == asset["sha256"], f"SHA-256 set inattendu pour {target_name}")
            canonical_set_assets[target_name] = {"size": target.stat().st_size, "sha256": actual_sha}

        shutil.copyfile(runtime, stage / "jtrex_media_runtime.py")
        shutil.copyfile(sets_runtime, stage / "jtrex_sets_runtime.py")
        shutil.copyfile(sets_io_runtime, stage / "jtrex_sets_io.py")
        shutil.copyfile(sets_admin_runtime, stage / "jtrex_sets_admin.py")
        shutil.copyfile(sets_preview_runtime, stage / "jtrex_sets_preview.py")
        shutil.copyfile(sets_android_runtime, stage / "jtrex_sets_android.py")
        phase_runtime = runtime.with_name("jtrex_phase_runtime.py")
        require(phase_runtime.is_file(), "Runtime de phases absent.")
        shutil.copyfile(phase_runtime, stage / "jtrex_phase_runtime.py")
        compile(phase_runtime.read_text(encoding="utf-8"), "jtrex_phase_runtime.py", "exec")
        compile(
            (stage / "jtrex_media_runtime.py").read_text(encoding="utf-8"),
            "jtrex_media_runtime.py",
            "exec",
        )
        compile(
            (stage / "jtrex_sets_runtime.py").read_text(encoding="utf-8"),
            "jtrex_sets_runtime.py",
            "exec",
        )
        compile(
            (stage / "jtrex_sets_io.py").read_text(encoding="utf-8"),
            "jtrex_sets_io.py",
            "exec",
        )
        for runtime_name in (
            "jtrex_sets_admin.py", "jtrex_sets_preview.py", "jtrex_sets_android.py"
        ):
            compile(
                (stage / runtime_name).read_text(encoding="utf-8"),
                runtime_name,
                "exec",
            )
        for source_file, relative_name in ((catalog_source, CATALOG_PATH), (manifest_source, selection.manifest_path)):
            target = stage.joinpath(*PurePosixPath(relative_name).parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_file, target)

        for resource in (
            "main.kv",
            "A.png",
            "boutBleu0.png",
            "pter/pter0.png",
            "assets/icon/JtrexIcon.png",
            "jtrex_sets_runtime.py",
            "jtrex_sets_io.py",
            "jtrex_sets_admin.py",
            "jtrex_sets_preview.py",
            "jtrex_sets_android.py",
            CATALOG_PATH,
            selection.manifest_path,
        ):
            require(
                (stage / resource).is_file(),
                f"Ressource requise absente : {resource}",
            )

        require(
            pruned_legacy_image_dirs == set(MP4_ONLY_LEGACY_DIRS),
            "Nettoyage MP4 incomplet: dossiers trouvés={} attendus={}".format(
                sorted(pruned_legacy_image_dirs), sorted(MP4_ONLY_LEGACY_DIRS)
            ),
        )
        remaining_legacy_frames = []
        for legacy_dir, legacy_prefix in MP4_ONLY_LEGACY_SEQUENCES.items():
            folder = stage / legacy_dir
            if folder.is_dir():
                remaining_legacy_frames.extend(
                    path.relative_to(stage).as_posix()
                    for path in folder.rglob("*")
                    if (
                        path.is_file()
                        and path.suffix.lower() in LEGACY_IMAGE_EXTENSIONS
                        and path.name.startswith(legacy_prefix)
                    )
                )
        require(
            not remaining_legacy_frames,
            "Frames legacy MP4 encore présentes: {}".format(remaining_legacy_frames[:10]),
        )
        print(
            "[JT-PREP] pruned legacy MP4 frames files={} bytes={} dirs={}".format(
                pruned_legacy_image_files,
                pruned_legacy_image_bytes,
                sorted(pruned_legacy_image_dirs),
            ),
            flush=True,
        )
        print(
            "[JT-PREP] preserved non-frame images in MP4 dirs files={} bytes={}".format(
                preserved_legacy_nonframe_images,
                preserved_legacy_nonframe_bytes,
            ),
            flush=True,
        )
        known_missing = []

        shutil.copyfile(spec, stage / "buildozer.spec")

        report = {
            "mission": "JT-MP4-CLEANUP-003",
            "version": VERSION,
            "numeric_version": NUMERIC_VERSION,
            "package": "com.junedady.junetrex",
            "python_target": "3.12.14",
            "archive_sha256": ARCHIVE_SHA256,
            "historical_main_sha256": MAIN_SHA256,
            "prepared_main_sha256": digest(main),
            "runtime_sha256": digest(stage / "jtrex_media_runtime.py"),
            "phase_runtime_sha256": digest(stage / "jtrex_phase_runtime.py"),
            "sets_runtime_sha256": digest(stage / "jtrex_sets_runtime.py"),
            "sets_io_runtime_sha256": digest(stage / "jtrex_sets_io.py"),
            "sets_admin_runtime_sha256": digest(stage / "jtrex_sets_admin.py"),
            "sets_preview_runtime_sha256": digest(stage / "jtrex_sets_preview.py"),
            "sets_android_runtime_sha256": digest(stage / "jtrex_sets_android.py"),
            "buildozer_spec_sha256": digest(stage / "buildozer.spec"),
            "canonical_set_id": selection.set_id,
            "canonical_manifest_sha256": canonical_manifest_sha256,
            "canonical_set_asset_count": len(selection.assets()),
            "canonical_set_assets": canonical_set_assets,
            "extracted_historical_files": len(extracted),
            "pruned_legacy_image_files": pruned_legacy_image_files,
            "pruned_legacy_image_bytes": pruned_legacy_image_bytes,
            "pruned_legacy_image_dirs": sorted(pruned_legacy_image_dirs),
            "preserved_legacy_nonframe_images": preserved_legacy_nonframe_images,
            "preserved_legacy_nonframe_bytes": preserved_legacy_nonframe_bytes,
            "mp4_only_states": list(MP4_ONLY_STATES),
            "icon_source": "assets/icon/JtrexIcon.png",
            "app_assets": app_asset_report,
            "known_missing_resources": known_missing,
            "changes": [
                "a.png -> A.png: 4 références",
                "boutbleu0.png -> boutBleu0.png: 4 références",
                f"version {VERSION} / versionCode {NUMERIC_VERSION}",
                "explicit presentation phases own UI masking, inputs and round countdown scheduling",
                "ROUND N yellow 1s then animated START 1.1s; gameplay released only at presentation completion",
                "power EOS latches completion without replay or impact; resumes live engine state after both media and historical action complete",
                "Python cible 3.12.14 pour compatibilité ffpyplayer",
                "titre June T-Rex",
                "menu music deferred until intro end",
                "one random intro per process launch",
                "states 1/2-4/5-7/8/9 mapped to combat videos; charge uses corrected red/blue gauge video",
                "power states 21/22/23/24/25/26 mapped to STSF/STLS/STTA/TRFS/TRPH/TRMA videos",
                "finishing states 10/11 mapped to Steg-finishes-Trex / Trex-finishes-Steg videos",
                "power and finishing videos are play-to-end cinematics; gameplay touch is locked while they cover the board",
                "power videos hide gameplay buttons and pause orb movement/countdowns until real MP4 EOS while historical power effect timing remains authoritative; once the power effect returns to state 1, historical restart animation also waits for EOS",
                "if a power causes state 10/11, finishing progression waits for the power MP4 EOS before the finishing video starts",
                "finishing states 10/11 freeze historical animation after first real MP4 frame, hide energy/health HUD and return to menu only after real MP4 EOS",
                "wait state 1 remembers its MP4 playback fraction across charge/power interruptions and resumes there; the MP4 itself loops from its end to its beginning",
                "legacy image sequences for all MP4-mapped states are pruned by exact animation prefix; unrelated images/icons in the same directories are preserved; gauge controls remain separate and interactive",
                "combat videos aspect-fill with native MP4 audio after first usable frame; intros remain aspect-fit with audio",
                "one scene player per state family with generation-safe callbacks",
                "legacy scene soundtrack remains fallback until first usable video frame and on media failure",
                "POWER_COSTS ST=60/40/60 TR=60/60/80 with strict energy>cost",
                "power availability shared by UI, touch and AI; right sound lock corrected",
                "rotating select/select0..15 aura visibility is forced from jt_power_available(slot); power item icons remain historical",
                "charge 2/3/4 -> orb phase arms a Clock-based two-second freeze: positions, orb AI, timeout and human stops are paused",
                "TRFS slot 4 / TRMA slot 6 visual identity corrected",
                "score/stop/letter diagnostics added without changing legacy score",
                "pause/resume/shutdown video lifecycle hooks",
                "hidden media admin opens after 20 bottom-right taps",
                "bottom-left blinking dot: green for actual MP4 rendering, red for legacy/fallback",
                "admin lists every historical animation prefix/directory and mapped MP4 availability",
                "20-tap mode shows the active legacy directory above the red status dot",
            ],
            "game_executed": False,
        }

        (stage / "android-preparation.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        stage.rename(destination)

    print(
        "[JT-PREP] Racine JuneTrex et empreintes vérifiées. "
        "Paquet média préparé ; jeu non exécuté.",
        flush=True,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--spec", type=Path, default=Path("buildozer.spec")
    )
    parser.add_argument(
        "--media-root", type=Path, default=Path("assets")
    )
    parser.add_argument(
        "--runtime", type=Path, default=Path("tools/jtrex_media_runtime.py")
    )
    args = parser.parse_args()
    prepare(
        args.archive.resolve(),
        args.output.resolve(),
        args.spec.resolve(),
        args.media_root.resolve(),
        args.runtime.resolve(),
    )


if __name__ == "__main__":
    main()
