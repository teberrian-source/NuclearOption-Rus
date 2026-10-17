# -*- coding: utf-8 -*-
"""Проверяет наличие конкретных ключей-кандидатов в ru.json."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
raw = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)
print("ru.json записей:", len(ru))

cands = [
    "A compact medium-range INS/OPT guidance cruise missile designed to give small aircraft standoff capability.",
    "Conceived at the turn of the century, the FS-3 Ternion is a large, twin-engine multirole fighter. Initially developed for long-endurance patrols over the Pacific, it was later adapted to meet expanding operational demands. Despite lacking stealth characteristics, frequent upgrade packages have allowed the Ternion to continue serving as a reliable defender of the Heartland.",
    "The engine of your aircraft can be stopped and started mid-flight with a dedicated keybind or a radial menu action.",
    "Front Fuselage Pylons",
    "Rear Fuselage Pylons",
    "Combined Weapon Bay",
    "AIR SAR",
    "INS / Opt.",
    "A-A",
    "A-G",
    "Apex-8 Single Rail",
    "Option A",
    "L | R",
    "TACTICAL",
    "HIGHWAY STRIP 1",
    "Primeva Alliance Liberation Army",
    "PRIMEVA ARMED LIBERATION ALLIANCE",
    "SOUTH BOSCALI GENERAL AVIATION",
    "Carrier Duel Lite",
    "Cursor : AA-nn",
    "Aircraft : AA-nn",
    "Score 0,0  --  Conventional level",
    "Score : 1234 - Escalation : Tactical",
]
for c in cands:
    print(("ЕСТЬ  " if c in ru else "НЕТ   ") + repr(c)[:110])

print()
print("--- похожие ключи в ru.json (пилоны / режимы / пинги) ---")
for k in ru:
    if re.search(r"(?i)(pylon|fuselage|weapon bay|SAR|Opt\.|radar|soft lock|TACTICAL|CONVENTIONAL)", k):
        print("   ", repr(k)[:110])
