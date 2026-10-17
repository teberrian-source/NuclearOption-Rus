# -*- coding: utf-8 -*-
"""Разбор untranslated.txt: сколько записей и какие модовые подписи в нём есть."""
import io, json, re, sys

sys.stdout.reconfigure(encoding="utf-8")
p = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch\untranslated.txt"
raw = io.open(p, encoding="utf-8", errors="replace").read()
lines = [l for l in raw.split("\n")]
print("всего строк:", len(lines))
print("строк, начинающихся с кавычки:", sum(1 for l in lines if l.startswith('"')))
# гибкий разбор: первый и последний кавычки
un = set()
bad = 0
for l in lines:
    s = l.strip().rstrip(",")
    if not (s.startswith('"') and s.endswith('": ""')):
        continue
    try:
        un.add(json.loads(s[:s.rindex('"') + 1]))
    except Exception:
        bad += 1
print("распознано:", len(un), "битых:", bad)
cands = ["subturret", "subturret (H)", "subturrets", "coax", "cargo", "cargo 2x", "Cargo 2x", "Ammo box",
         "Ammo Box", "Truck bed", "Point Defense", "Point Defence", "Roof Mount", "roof mount",
         "roof turret", "tow hook", "turret mount", "Vehicle Cargo", "The Device", "Launchers", "Turret",
         "Internal Gun", "Outer Wing Pylons", "Wing Pylons", "Tail Hook", "VLS", "Radome", "Infantry",
         "Bomb Bay (2x)", "Mission Bay", "Weapon Bay", "Weapon Bays", "Front Turret", "Rear Turret"]
print("\n--- кандидаты в untranslated.txt ---")
for c in cands:
    print(("ЕСТЬ " if c in un else "нет  "), c)
