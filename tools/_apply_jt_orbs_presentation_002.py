#!/usr/bin/env python3
from pathlib import Path
import subprocess


def main():
    path = Path("tools/jtrex_media_runtime.py")
    text = path.read_text(encoding="utf-8")
    marker = "SCENES = {\n"
    legacy = 'LEGACY_WAIT_FILE = "assets/combat/StegVsTrexvaetviensremolacebisorigune.mp4"\n\n'
    if legacy not in text:
        if text.count(marker) != 1:
            raise SystemExit("SCENES marker not unique")
        text = text.replace(marker, legacy + marker, 1)
        path.write_text(text, encoding="utf-8")
    subprocess.run(["python3", "-m", "py_compile", str(path)], check=True)


if __name__ == "__main__":
    main()
