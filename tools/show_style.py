# -*- coding: utf-8 -*-
"""Печатает переводы-образцы из ru.json (пилоны, отсеки, режимы радара)."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
raw = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

keys = [
    "Fuselage Pylons", "Inner Fuselage Pylons", "Outer Fuselage Pylons",
    "Inner Wing Pylons", "Middle Wing Pylons", "Outer Wing Pylons",
    "Weapon Bay", "Combined Weapon Bays", "Forward Weapon Bay", "Rear Weapon Bay",
    "Center Pylon", "Centreline Pylon", "Radar Guided", "SARH",
    "Radar Countermeasures", "INS / Opt", "Cpu", "CPU", "Gpu", "GPU",
]
for k in keys:
    if k in ru:
        print(f"  {k!r} -> {ru[k]!r}")
    else:
        print(f"  {k!r} -> (нет)")

print()
print("--- короткие ключи (<= 10 симв.), похожие на режимы/аббревиатуры ---")
for k in sorted(ru):
    if len(k) <= 10 and re.fullmatch(r"[A-Za-z0-9 /\-\.:]+", k or ""):
        if re.search(r"(?i)(sar|opt|ins|a-a|a-g|radar|tgt|cpu|gpu)", k):
            print(f"  {k!r} -> {ru[k]!r}")
