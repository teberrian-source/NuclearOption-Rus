# -*- coding: utf-8 -*-
"""Печатает repr трёх roadmap-строк untranslated.txt полностью."""
import io, sys

sys.stdout.reconfigure(encoding="utf-8")
un = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch\untranslated.txt"
txt = io.open(un, encoding="utf-8", errors="replace").read()
lines = txt.split("\n")
for i, l in enumerate(lines, 1):
    if "Additional Boats" in l or "landlocked map" in l or "low-rank aircraft" in l:
        print(f"--- строка {i} (len={len(l)}) ---")
        print(repr(l))
