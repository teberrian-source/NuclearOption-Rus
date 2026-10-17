# -*- coding: utf-8 -*-
"""Проверяет, есть ли уже переводы для найденных описаний (в т.ч. обтекателя РЛС)."""
import io, json, re, sys

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

def parse_json(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse_json(base + r"\ru.json")
probes = [
    "An extremely powerful long-range all-aspect radar system",
    "A short ranged missile, consisting of 6 cluster Active Radar homing bomblets",
    "The Andromeda-class Aviation Missile Cruiser",
    "The missile is hot-launched and orientates itself",
    "Various systems for deploying cargo and support equipment",
    "Coming in at 20,000 tonnes and common with mid-tier regional powers",
    "At 309m length and displacing over 100,000 tonnes",
    "The available carriers are the original six-drone Apex-6 TEL",
    "Both pallets use the native cargo ramp and parachute",
]
for p in probes:
    keys = [k for k in ru if k.startswith(p[:60])]
    if not keys:
        print("НЕТ  ", p[:70])
    else:
        for k in keys:
            print("ЕСТЬ ", p[:55], "->", ru[k][:70])
