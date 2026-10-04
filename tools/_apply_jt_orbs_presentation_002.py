#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import subprocess

REPO_FILE = "StegTrexPlageVideoenboucledesorbes.mp4"
DEST = Path("assets/combat") / REPO_FILE
SOURCE_COMMIT = "995a2eb9c35f2dfb06de587f0b6641e5dedd342c"
EXPECTED_BLOB = "908d0f2bc2db08522d9924bd0909b5ef36ddd1dd"
EXPECTED_SIZE = 9848376


def replace_exact(path, old, new, count=1):
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    actual = text.count(old)
    if actual != count:
        raise SystemExit(f"{path}: expected {count} occurrence(s), found {actual}: {old!r}")
    path.write_text(text.replace(old, new), encoding="utf-8")


def main():
    subprocess.run(["git", "fetch", "origin", "main"], check=True)
    data = subprocess.check_output(["git", "show", f"{SOURCE_COMMIT}:{REPO_FILE}"])
    if len(data) != EXPECTED_SIZE:
        raise SystemExit(f"beach size {len(data)} != {EXPECTED_SIZE}")
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_bytes(data)
    blob = subprocess.check_output(["git", "hash-object", str(DEST)], text=True).strip()
    if blob != EXPECTED_BLOB:
        raise SystemExit(f"beach blob {blob} != {EXPECTED_BLOB}")
    print("BEACH sha256", hashlib.sha256(data).hexdigest(), "size", len(data), flush=True)
    probe = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=index,codec_name,codec_type,width,height,r_frame_rate",
        "-of", "json", str(DEST)
    ], text=True)
    print("BEACH ffprobe", probe, flush=True)
    json.loads(probe)

    phase = "tools/jtrex_phase_runtime.py"
    old = '''    def _begin_fight(self, target):\n        if target not in ("orbs", "yellow"):\n            raise ValueError("unknown FIGHT target: {}".format(target))\n        self.fight_target = target\n'''
    new = '''    def _prepare_new_orb_exchange(self):\n        """Reset only state that belongs to a genuinely new orb exchange."""\n        self.engine["car2"] = 10\n        for name in ("stopg", "stopd"):\n            if name in self.engine:\n                self.engine[name] = False\n        colstop = self.engine.get("colstop")\n        if isinstance(colstop, dict):\n            for slot in range(1, 7):\n                colstop[slot] = False\n        elif isinstance(colstop, list):\n            for slot in range(1, min(7, len(colstop))):\n                colstop[slot] = False\n        stop_cause = self.engine.get("_JT_STOP_CAUSE")\n        if isinstance(stop_cause, dict):\n            for slot in range(1, 7):\n                stop_cause.pop(slot, None)\n        print(\n            "[JT-ORB-EXCHANGE] reset car2=10 stops=clear phase={} indexa={} car={}".format(\n                self.name, self.engine["indexa"], self.engine["car"]\n            ),\n            flush=True,\n        )\n\n    def _begin_fight(self, target):\n        if target not in ("orbs", "yellow"):\n            raise ValueError("unknown FIGHT target: {}".format(target))\n        if target == "orbs":\n            self._prepare_new_orb_exchange()\n        self.fight_target = target\n'''
    replace_exact(phase, old, new)

    replace_exact(
        "tools/jtrex_media_runtime.py",
        '"file": "assets/combat/StegVsTrexvaetviensremolacebisorigune.mp4",',
        '"file": "assets/combat/StegTrexPlageVideoenboucledesorbes.mp4",',
    )
    replace_exact(
        "tools/prepare_android.py",
        'VERSION = "1.0.13"\nNUMERIC_VERSION = "113"',
        'VERSION = "1.0.14"\nNUMERIC_VERSION = "114"',
    )
    marker = '    "assets/combat/StegVsTrexvaetviensremolacebisorigune.mp4": 2472718,\n'
    replace_exact(
        "tools/prepare_android.py", marker,
        marker + '    "assets/combat/StegTrexPlageVideoenboucledesorbes.mp4": 9848376,\n'
    )
    replace_exact(
        "buildozer.spec",
        "version = 1.0.13\nandroid.numeric_version = 113",
        "version = 1.0.14\nandroid.numeric_version = 114",
    )
    marker = '              "StegVsTrexvaetviensremolacebisorigune.mp4",\n'
    replace_exact(
        ".github/workflows/android.yml", marker,
        marker + '              "StegTrexPlageVideoenboucledesorbes.mp4",\n'
    )

    subprocess.run([
        "python3", "-m", "py_compile",
        "tools/jtrex_phase_runtime.py", "tools/jtrex_media_runtime.py",
        "tools/prepare_android.py", "tests/test_orb_presentation.py"
    ], check=True)


if __name__ == "__main__":
    main()
