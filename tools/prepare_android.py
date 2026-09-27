#!/usr/bin/env python3
"""Préparation contrôlée de June T-Rex pour JT-ANDROID-001."""

import argparse
import configparser
import hashlib
import json
import shutil
import tempfile
import zipfile
from pathlib import Path, PurePosixPath


VERSION = "1.0.1"
ARCHIVE_SIZE = 327992765
ARCHIVE_SHA256 = (
    "f73ca1fd5e96ca6e11df5987bda8b2e59"
    "ebac26b1beb23fe34883b15bee66647"
)
MAIN_SHA256 = (
    "3673fb85d12bea18276e485c5956530b4b8"
    "c0dda283cacb022e784bfe8c35231"
)
EXTENSIONS = {"py", "kv", "png", "jpg", "jpeg", "gif", "wav"}
EXCLUDED_DIRS = {".kivy", ".buildozer", "__pycache__", "bin"}


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

    # Réutiliser l'indentation historique, sans reformater le programme.
    output = []
    insertions = 0
    for line in source.splitlines(keepends=True):
        if line.strip() == "Clock.max_iteration = 100000":
            indent = line[: len(line) - len(line.lstrip(" \t"))]
            output.append(
                indent
                + 'print("[JT-START] on_start; Kivy={}; window={}".format('
                + "kivy.__version__, Window.size), flush=True)"
                + newline
            )
            insertions += 1
        output.append(line)

    require(insertions == 1, "Bloc on_start historique non identifié.")
    result = "".join(output)

    # Contrôle syntaxique uniquement : aucune exécution du jeu.
    compile(result, "JuneTrex/main.py", "exec")
    return result


def prepare(archive, destination, spec):
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
        config.get("app", "package.name") == "junetrex"
        and config.get("app", "package.domain") == "com.junedady",
        "Identité du paquet différente de la référence.",
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

                # Le programme audité n'importe aucun module local annexe.
                # Les autres .py sont des variantes historiques.
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

        for resource in (
            "main.kv",
            "A.png",
            "boutBleu0.png",
            "pter/pter0.png",
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
            "mission": "JT-ANDROID-001",
            "version": VERSION,
            "package": "com.junedady.junetrex",
            "archive_sha256": ARCHIVE_SHA256,
            "historical_main_sha256": MAIN_SHA256,
            "prepared_main_sha256": digest(main),
            "buildozer_spec_sha256": digest(stage / "buildozer.spec"),
            "extracted_files": len(extracted),
            "icon_source": "pter/pter0.png",
            "known_missing_resources": known_missing,
            "changes": [
                "a.png -> A.png: 4 références",
                "boutbleu0.png -> boutBleu0.png: 4 références",
                "version 1.0.1",
                "titre June T-Rex",
                "messages JT-BOOT et JT-START",
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
        "Paquet préparé ; jeu non exécuté.",
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
    args = parser.parse_args()
    prepare(
        args.archive.resolve(),
        args.output.resolve(),
        args.spec.resolve(),
    )


if __name__ == "__main__":
    main()
