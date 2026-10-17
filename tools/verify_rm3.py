# -*- coding: utf-8 -*-
"""Отладка сверки roadmap-ключей ru.json <-> untranslated.txt."""
import json, io, re, sys

sys.stdout.reconfigure(encoding="utf-8")
un = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch\untranslated.txt"
ru = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch\ru.json"

raw = io.open(ru, encoding="utf-8-sig").read()
ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
data = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

lines = io.open(un, encoding="utf-8", errors="replace").read().split("\n")
cand = [l for l in lines if "Additional Boats" in l or "landlocked map" in l or "low-rank aircraft" in l]
print("строк с roadmap:", len(cand))
for l in cand:
    lit = l.strip()
    lit = lit[: lit.rfind('": ""') + 1]
    try:
        k = json.loads(lit)
        print("OK | в ru.json:", k in data, "| repr:", repr(k[:60]))
    except Exception as e:
        print("ОШИБКА:", e, "|", repr(lit[:100]))
# показать мои roadmap-ключи
mine = [k for k in data if k.startswith("\u2022 ")]
print("мои roadmap-ключей в ru.json:", len(mine))
for k in mine:
    print("  repr:", repr(k[:60]))
