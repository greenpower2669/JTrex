#!/usr/bin/env python3
"""Préparation contrôlée de June T-Rex pour Android."""

import argparse
import configparser
import hashlib
import json
import shutil
import tempfile
import zipfile
from pathlib import Path, PurePosixPath


VERSION = "1.0.7"
NUMERIC_VERSION = "107"
ARCHIVE_SIZE = 327992765
ARCHIVE_SHA256 = (
    "f73ca1fd5e96ca6e11df5987bda8b2e59"
    "ebac26b1beb23fe34883b15bee66647"
)
MAIN_SHA256 = (
    "3673fb85d12bea18276e485c5956530b4b8"
    "c0dda283cacb022e784bfe8c35231"
)
EXTENSIONS = {"py", "kv", "png", "jpg", "jpeg", "gif", "wav", "mp4"}
EXCLUDED_DIRS = {".kivy", ".buildozer", "__pycache__", "bin"}
MEDIA_ASSETS = {
    "assets/icon/JtrexIcon.png": 2283569,
    "assets/intro/JTrexintro1.mp4": 3278089,
    "assets/intro/JTrexintro2.mp4": 2584105,
    "assets/intro/JTrexintro3.mp4": 3349412,
    "assets/combat/Chargestegtrexchargerougebleucorrected.mp4": 746721,
    "assets/powers/stsf-sanctuary-force.mp4": 2525411,
    "assets/powers/stls-lifestream.mp4": 2243703,
    "assets/powers/stta-tornado-attack.mp4": 2928334,
    "assets/powers/trfs-fire-storm.mp4": 2431111,
    "assets/powers/trph-phoenix-attack.mp4": 2379231,
    "assets/powers/trma-meteor-attack.mp4": 2544535,
    "assets/finishing/steg-finishing-trex.mp4": 2184229,
    "assets/finishing/trex-finishing-steg.mp4": 1834787,
    "assets/combat/Stegtrexegalitechargeboutonjaune.mp4": 1432415,
    "assets/combat/StegVsTrexvaetviensremolacebisorigune.mp4": 2472718,
    "assets/combat/Stegtrexresultstegwin.mp4": 1521350,
    "assets/combat/Stegtrexresulttrexwin.mp4": 760242,
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


def adapt_main(source):
    newline = "\r\n" if "\r\n" in source else "\n"

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
        + "def jt_power_available(slot):"
        + newline
        + "\tenergy=stamg if slot<4 else stamd"
        + newline
        + "\treturn indexa==1 and not selected[slot] and energy>POWER_COSTS[slot]"
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
        "        Clock.schedule_interval(self.root.carupdate, 1)" + newline,
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
        src_indent + "if not getattr(self, '_jt_scene_video_active', False):" + newline,
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
        audio_indent + "if not getattr(self, '_jt_scene_video_active', False):" + newline
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

    # Correct the right-side visual identity: slot 4=TRFS, slot 6=TRMA.
    start, end = method_bounds(lines, "affbt")
    tr_identity_swaps = 0
    for index in range(start, end):
        if "self.b4.source" in lines[index] and "trma" in lines[index]:
            lines[index] = lines[index].replace("trma", "trfs")
            tr_identity_swaps += 1
        elif "self.b6.source" in lines[index] and "trfs" in lines[index]:
            lines[index] = lines[index].replace("trfs", "trma")
            tr_identity_swaps += 1
    require(
        tr_identity_swaps == 4,
        f"Identité visuelle TRFS/TRMA: {tr_identity_swaps} remplacement(s), 4 attendus.",
    )

    # Canonical rotating aura: b1s..b6s are the animated select/select0..15 overlays.
    # Keep the power item icons historical; only the aura follows actual launchability.
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
    ]
    lines[end:end] = aura_block

    # Touch safety: the tap that starts charge must never freeze an orb, then orb
    # stop taps remain protected for two seconds. Full cinematics also swallow
    # gameplay touches while the video is still covering the board.
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
        touch_body_indent + "global _JT_ORB_TOUCH_PROTECT_UNTIL" + newline,
        touch_body_indent + "_jt_touch_start_indexa=indexa" + newline,
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
                            prefix + "if _jt_touch_start_indexa!=1 and time.time()>=_JT_ORB_TOUCH_PROTECT_UNTIL:" + newline,
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
        touch_body_indent + "if _jt_touch_start_indexa==1 and indexa in (2,3,4):" + newline,
        touch_body_indent + "\t_JT_ORB_TOUCH_PROTECT_UNTIL=max(_JT_ORB_TOUCH_PROTECT_UNTIL,time.time()+2.0)" + newline,
        touch_body_indent + "\tprint('[JT-ORB] touch protection 2.0s state={}'.format(indexa),flush=True)" + newline,
        touch_body_indent + "jt_sync_scene_now()" + newline,
    ]

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
    lines[start + 2:start + 2] = [body_indent + "_jt_log_new_stops(self, 'colvv-pre-update')" + newline]
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
    require(
        "mp4" in {
            item.strip().lower()
            for item in config.get("app", "source.include_exts").split(",")
        },
        "MP4 absent de source.include_exts.",
    )
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
        adapted = adapt_main(original)
        main.write_bytes(adapted.encode("utf-8"))

        asset_report = {}
        for target_name, expected_size in MEDIA_ASSETS.items():
            rel = PurePosixPath(target_name)
            source = media_root.joinpath(*rel.parts[1:])
            require(source.is_file(), f"Ressource fournie absente : {target_name}")
            require(
                source.stat().st_size == expected_size,
                f"Taille inattendue pour {target_name}",
            )
            target = stage.joinpath(*rel.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            asset_report[target_name] = {
                "size": target.stat().st_size,
                "sha256": digest(target),
            }

        shutil.copyfile(runtime, stage / "jtrex_media_runtime.py")
        compile(
            (stage / "jtrex_media_runtime.py").read_text(encoding="utf-8"),
            "jtrex_media_runtime.py",
            "exec",
        )

        for resource in (
            "main.kv",
            "A.png",
            "boutBleu0.png",
            "pter/pter0.png",
            "assets/icon/JtrexIcon.png",
            "assets/intro/JTrexintro1.mp4",
            "assets/intro/JTrexintro2.mp4",
            "assets/intro/JTrexintro3.mp4",
            "assets/combat/Chargestegtrexchargerougebleucorrected.mp4",
            "assets/powers/stsf-sanctuary-force.mp4",
            "assets/powers/stls-lifestream.mp4",
            "assets/powers/stta-tornado-attack.mp4",
            "assets/powers/trfs-fire-storm.mp4",
            "assets/powers/trph-phoenix-attack.mp4",
            "assets/powers/trma-meteor-attack.mp4",
            "assets/finishing/steg-finishing-trex.mp4",
            "assets/finishing/trex-finishing-steg.mp4",
            "assets/combat/Stegtrexegalitechargeboutonjaune.mp4",
            "assets/combat/StegVsTrexvaetviensremolacebisorigune.mp4",
            "assets/combat/Stegtrexresultstegwin.mp4",
            "assets/combat/Stegtrexresulttrexwin.mp4",
        ):
            require(
                (stage / resource).is_file(),
                f"Ressource requise absente : {resource}",
            )

        missing_frame = "horseg2ko/chargetrwin_83.jpeg"
        known_missing = []
        if not (stage / missing_frame).is_file():
            known_missing.append(missing_frame)
            print(
                "[JT-PREP][KNOWN-MISSING] "
                f"{missing_frame}; aucun remplacement effectué.",
                flush=True,
            )

        shutil.copyfile(spec, stage / "buildozer.spec")

        report = {
            "mission": "JT-CINEMATIC-FINISHING-001",
            "version": VERSION,
            "numeric_version": NUMERIC_VERSION,
            "package": "com.junedady.junetrex",
            "python_target": "3.12.14",
            "archive_sha256": ARCHIVE_SHA256,
            "historical_main_sha256": MAIN_SHA256,
            "prepared_main_sha256": digest(main),
            "runtime_sha256": digest(stage / "jtrex_media_runtime.py"),
            "buildozer_spec_sha256": digest(stage / "buildozer.spec"),
            "extracted_historical_files": len(extracted),
            "icon_source": "assets/icon/JtrexIcon.png",
            "media_assets": asset_report,
            "known_missing_resources": known_missing,
            "changes": [
                "a.png -> A.png: 4 références",
                "boutbleu0.png -> boutBleu0.png: 4 références",
                "version 1.0.7 / versionCode 107",
                "Python cible 3.12.14 pour compatibilité ffpyplayer",
                "titre June T-Rex",
                "menu music deferred until intro end",
                "one random intro per process launch",
                "states 1/2-4/5-7/8/9 mapped to combat videos; charge uses corrected red/blue gauge video",
                "power states 21/22/23/24/25/26 mapped to STSF/STLS/STTA/TRFS/TRPH/TRMA videos",
                "finishing states 10/11 mapped to Steg-finishes-Trex / Trex-finishes-Steg videos",
                "power and finishing videos are play-to-end cinematics; gameplay touch is locked while they cover the board",
                "combat videos aspect-fill with native MP4 audio after first usable frame; intros remain aspect-fit with audio",
                "one scene player per state family with generation-safe callbacks",
                "legacy scene soundtrack remains fallback until first usable video frame and on media failure",
                "POWER_COSTS ST=60/40/60 TR=60/60/80 with strict energy>cost",
                "power availability shared by UI, touch and AI; right sound lock corrected",
                "rotating select/select0..15 aura visibility is forced from jt_power_available(slot); power item icons remain historical",
                "charge-start tap cannot stop an orb and orb touch-stop is protected for two seconds",
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
