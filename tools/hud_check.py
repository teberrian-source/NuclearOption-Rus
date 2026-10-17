# -*- coding: utf-8 -*-
"""Уточняет переводы для HUD-аббревиатур и статусов."""
import io, json, re, sys

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

def parse_json(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse_json(base + r"\ru.json")
for w in ["Air-to-Air", "Air-to-Ground", "GEAR", "Down", "UP", "TGT", "WMC", "AVG", "TRANS", "LDR",
          "RNG", "ROT", "YAW", "SPD", "MACH", "In-game", "Online", "Offline", "Mission Title",
          "Choose"]:
    hits = [k for k in ru if w.lower() == k.lower()]
    print(f"{w:<16} ключ: {hits} -> {[ru[h] for h in hits]}")
