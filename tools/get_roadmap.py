# -*- coding: utf-8 -*-
"""Достаёт полные roadmap-ключи из untranslated.txt."""
import sys, re, io, json

sys.stdout.reconfigure(encoding="utf-8")
p = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch\untranslated.txt"
data = io.open(p, encoding="utf-8", errors="replace").read()
for q in ("Additional Boats / Ships", "Additional low-rank aircraft", "New large landlocked map"):
    i = data.find(q)
    print("=" * 70)
    print(f"[{q}] pos={i}")
    if i >= 0:
        start = data.rfind("\n", 0, i) + 1
        end = data.find("\n", i)
        print(repr(data[start:end])[:2000])
