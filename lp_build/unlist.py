# -*- coding: utf-8 -*-
"""Печатает текущий untranslated.txt (после фильтра мусора)."""
import io, json, re, sys

sys.stdout.reconfigure(encoding="utf-8")
p = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch\untranslated.txt"
raw = io.open(p, encoding="utf-8", errors="replace").read()
items = []
for line in raw.split("\n"):
    s = line.strip().rstrip(",")
    m = re.match(r'^"((?:[^"\\]|\\.)*)":\s*""$', s)
    if m:
        try:
            items.append(json.loads('"' + m.group(1) + '"'))
        except Exception:
            items.append(m.group(1))
print("всего:", len(items))
for i, t in enumerate(items):
    print(f"{i:>4} | {t}")
