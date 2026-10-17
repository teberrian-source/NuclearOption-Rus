# -*- coding: utf-8 -*-
"""Извлекает глаголы kill-feed из untranslated.txt: <color..>X</color> VERB <color..>Y</color>."""
import sys, json, io, re
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
u = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch\untranslated.txt"

keys = []
for line in io.open(u, encoding="utf-8-sig").read().split("\n"):
    line = line.strip()
    if not line.startswith('"'):
        continue
    try:
        obj = json.loads("{" + line.rstrip(",") + "}")
    except Exception:
        continue
    keys.append(next(iter(obj)))

pat = re.compile(r"^<color=[^>]*>[^<]*</color>\s*(.+?)\s*(?:<color=[^>]*>|$)")
verbs = Counter()
no_color = Counter()
for k in keys:
    plain = k.replace("\n", " | ")
    if "color=" not in plain:
        continue
    for seg in plain.split(" | "):
        m = pat.match(seg.strip())
        if m:
            verbs[m.group(1)] += 1
        elif seg.strip():
            no_color[seg.strip()[:60]] += 1

print("=== ГЛАГОЛЫ (X VERB Y) ===")
for v, c in verbs.most_common(40):
    print(f"{c:6}  {v!r}")
print("\n=== БЕЗ COLOR-ОБЁРТКИ (в составных kill-feed) ===")
for v, c in no_color.most_common(25):
    print(f"{c:6}  {v!r}")
