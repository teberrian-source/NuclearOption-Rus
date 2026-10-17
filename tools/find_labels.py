# -*- coding: utf-8 -*-
"""Ищет точные UI-ключи в untranslated.txt по подстрокам."""
import sys, json, io

sys.stdout.reconfigure(encoding="utf-8")
u = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch\untranslated.txt"

NEEDLES = ["Internal Cannon", "Pylon", "Turret", "Purchase", "Rank", "Owned",
           "Faction", "YES", "NO ", "Main ", "Left ", "Right ", "Front", "Rear"]

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

seen = set()
for n in NEEDLES:
    hits = [k for k in keys if n in k and len(k) < 60 and k not in seen]
    if hits:
        print(f"--- {n!r} ---")
        for k in sorted(set(hits))[:25]:
            seen.add(k)
            print("   ", repr(k))
