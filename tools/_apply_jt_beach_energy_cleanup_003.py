#!/usr/bin/env python3
from pathlib import Path
import subprocess

MARK = "JT-BEACH-ENERGY-CANON-003"
BEACH = "assets/combat/StegTrexPlageVideoenboucledesorbes.mp4"
OLD_WAIT = (
    "assets/combat/StegVsTrexvaetviensremolace.mp4",
    "assets/combat/StegVsTrexvaetviensremolacebisorigune.mp4",
)


def replace_once(path, old, new):
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected 1 occurrence of {old!r}, got {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def append_memory(path):
    text = path.read_text(encoding="utf-8")
    if MARK in text:
        return
    block = f"""## {MARK} — avenant Fab 2026-10-04

Décision canonique téléphone, postérieure à JT-ORBS-PRESENTATION-002 :
- le fond des orbes est exclusivement `{BEACH}`, joué en boucle ;
- les anciens `StegVsTrexvaetviensremolace*.mp4` sont remplacés et ne doivent plus être packagés ni utilisés ;
- au début de chaque **nouveau vrai round**, `stamg=0` et `stamd=0` : les deux barres d'énergie repartent de zéro ;
- le réarmement des six pouvoirs reste distinct de leur énergie : `selected[1..6]` est réarmé puis la disponibilité est recalculée avec l'énergie remise à zéro ;
- un simple retour de pouvoir ne crée pas un nouveau round et ne remet donc ni le chrono d'orbes ni l'énergie à zéro ;
- les règles KO / 2 rounds gagnants / coûts 60-40-60 et 60-60-80 / seuil strict `energy > cost` restent inchangées.

Cet avenant remplace explicitement les anciennes mentions « énergie préservée entre rounds » et « conserver l'ancien média wait disponible ». L'historique peut rester documenté mais ne doit plus être interprété comme règle active."""
    path.write_text(text.rstrip() + "\n\n" + block + "\n", encoding="utf-8")


def main():
    media = Path("tools/jtrex_media_runtime.py")
    phase = Path("tools/jtrex_phase_runtime.py")
    prep = Path("tools/prepare_android.py")
    spec = Path("buildozer.spec")

    text = media.read_text(encoding="utf-8")
    legacy = 'LEGACY_WAIT_FILE = "assets/combat/StegVsTrexvaetviensremolacebisorigune.mp4"\n\n'
    if legacy in text:
        text = text.replace(legacy, "", 1)
    wait = '"file": "assets/combat/StegTrexPlageVideoenboucledesorbes.mp4",\n        "loop": True,'
    if wait not in text:
        raise SystemExit("beach wait loop is not canonical in media runtime")
    if "StegVsTrexvaetviensremolace" in text:
        raise SystemExit("legacy wait reference remains in media runtime")
    media.write_text(text, encoding="utf-8")

    text = phase.read_text(encoding="utf-8")
    old = '''    def _reset_between_rounds(self):\n        """Restore round-local state without passing through the menu or changing energy rules."""'''
    new = '''    def _reset_between_rounds(self):\n        """Restore round-local state; a new true round starts with zero energy."""'''
    if old not in text:
        raise SystemExit("phase reset docstring guard failed")
    text = text.replace(old, new, 1)
    old = '''        colstop = self.engine.get("colstop")\n        if isinstance(colstop, dict):\n            for slot in range(1, 7):\n                colstop[slot] = False\n        refresh = self.engine.get("jt_refresh_power_flags")'''
    new = '''        colstop = self.engine.get("colstop")\n        if isinstance(colstop, dict):\n            for slot in range(1, 7):\n                colstop[slot] = False\n        for name in ("stamg", "stamd"):\n            if name in self.engine:\n                self.engine[name] = 0\n        refresh = self.engine.get("jt_refresh_power_flags")'''
    if old not in text:
        raise SystemExit("phase energy insertion guard failed")
    text = text.replace(old, new, 1)
    old = 'print("[JT-ROUND] reset lives/damage/power-usage; energy preserved", flush=True)'
    new = 'print("[JT-ROUND] reset lives/damage/power-usage; energy ST=0 TR=0", flush=True)'
    if old not in text:
        raise SystemExit("phase log guard failed")
    phase.write_text(text.replace(old, new, 1), encoding="utf-8")

    replace_once(prep, 'VERSION = "1.0.14"', 'VERSION = "1.0.15"')
    replace_once(prep, 'NUMERIC_VERSION = "114"', 'NUMERIC_VERSION = "115"')
    text = prep.read_text(encoding="utf-8")
    stale = '    "assets/combat/StegVsTrexvaetviensremolacebisorigune.mp4": 2472718,\n'
    if stale not in text:
        raise SystemExit("legacy wait MEDIA_ASSETS guard failed")
    prep.write_text(text.replace(stale, "", 1), encoding="utf-8")

    replace_once(spec, 'version = 1.0.14', 'version = 1.0.15')
    replace_once(spec, 'android.numeric_version = 114', 'android.numeric_version = 115')

    for doc in ("brain.md", "brainmap.md", "debughistorical.md", "todo.md", "ordres-de-mission.md"):
        append_memory(Path(doc))

    for old_asset in OLD_WAIT:
        p = Path(old_asset)
        if p.exists():
            subprocess.run(["git", "rm", "--", old_asset], check=True)

    subprocess.run(["python3", "-m", "py_compile", str(media), str(phase), str(prep)], check=True)


if __name__ == "__main__":
    main()
