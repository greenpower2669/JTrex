#!/usr/bin/env python3
from pathlib import Path

path = Path('tools/prepare_android.py')
text = path.read_text(encoding='utf-8')
old = '            "assets/combat/StegVsTrexvaetviensremolacebisorigune.mp4",\n'
new = '            "assets/combat/StegTrexPlageVideoenboucledesorbes.mp4",\n'
count = text.count(old)
if count != 1:
    raise SystemExit(f'expected exactly one stale required wait resource, got {count}')
text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
compile(text, 'tools/prepare_android.py', 'exec')
