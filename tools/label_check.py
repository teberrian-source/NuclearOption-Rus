# -*- coding: utf-8 -*-
"""Значения в ru.json для подписей-кандидатов (миссионные задачи/ВПП)."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
raw = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in raw.split("\n") if not l.strip().startswith("//"))), strict=False)

keys = [
    "Return To Base", "Search For Convoy", "Break Blockade", "Defend Island",
    "Destroy Vehicles", "Detected units", "Repaired unit", "Take Off", "Taxi",
    "Taxi to Runway", "Taxi to Runway 01", "Taxi to Runway 34",
    "Cleared for landing on Runway", "Cleared to taxi to Runway",
    "Successfull Sortie", "Successfull Sortie +",
    "RNG", "REL", "ALT", "ETA", "MAX", "V", "2h", "3h", "Mobile FOB",
]
for k in keys:
    print(f"{'ЕСТЬ' if k in ru else 'нет ':5} | {k!r} -> {ru.get(k)!r}")
