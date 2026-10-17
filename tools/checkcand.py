# -*- coding: utf-8 -*-
"""Сверяет кандидаты-подписи из модовых бандлов с ru.json и untranslated.txt."""
import io, json, re, sys

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

def parse_json(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse_json(base + r"\ru.json")
un_raw = io.open(base + r"\untranslated.txt", encoding="utf-8", errors="replace").read()
un = set()
for line in un_raw.split("\n"):
    m = re.match(r'^"((?:[^"\\]|\\.)*)":\s*"",?\s*$', line.strip())
    if m:
        try:
            un.add(json.loads('"' + m.group(1) + '"'))
        except Exception:
            pass

cands = ["Ammo Box", "Ammo box", "Cargo", "Cargo 2x", "cargo", "cargo 2x", "Gun", "Launchers",
         "Left Pylon", "Right Pylon", "Main Turret", "Point Defence", "Point Defense",
         "Roof Mount", "roof mount", "roof turret", "The Device", "Truck bed", "Turret",
         "Vehicle Cargo", "coax", "subturret", "subturret (H)", "subturrets", "tow hook",
         "turret mount", "Cargo Bay", "Mounted Cargo", "Mounted Missile"]
print(f"{'строка':<20} {'ru.json':<8} {'untranslated':<13}")
for c in cands:
    print(f"{c:<20} {('ЕСТЬ' if c in ru else 'нет'):<8} {('ЕСТЬ' if c in un else 'нет'):<13} {ru.get(c,'')}")
print("\nвсего untranslated:", len(un), "| ru.json:", len(ru))
