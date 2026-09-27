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


VERSION = "1.0.2"
NUMERIC_VERSION = "102"
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
    "assets/combat/StegVsTrexvaetviensremolace.mp4": 7711195,
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
    ]
    lines[start:end] = replacement

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
        body_indent + "\tmedia_controller.sync_wait_state(indexa)" + newline,
    ]
    lines[global_index + 1:global_index + 1] = hook

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
        src_indent + "if not getattr(self, '_jt_wait_video_active', False):" + newline,
        src_indent + unit + original_source,
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
    require(
        "ffpyplayer" in config.get("app", "requirements"),
        "ffpyplayer absent des requirements.",
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
            "assets/combat/StegVsTrexvaetviensremolace.mp4",
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
            "mission": "JT-MEDIA-001",
            "version": VERSION,
            "numeric_version": NUMERIC_VERSION,
            "package": "com.junedady.junetrex",
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
                "version 1.0.2 / versionCode 102",
                "titre June T-Rex",
                "menu music deferred until intro end",
                "one random intro per process launch",
                "indexa=1 scene texture replaced by looping Steg/T-Rex video",
                "wait-video audio muted; historical game audio preserved",
                "pause/resume/shutdown video lifecycle hooks",
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
