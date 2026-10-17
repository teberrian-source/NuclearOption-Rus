# -*- coding: utf-8 -*-
"""Выгружает все ключи из untranslated.txt в JSONL для разбора + базовая статистика."""
import json, io, sys

u = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch\untranslated.txt"
sys.stdout.reconfigure(encoding="utf-8")

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

print("всего ключей:", len(keys))
with io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\cand.jsonl", "w",
             encoding="utf-8") as f:
    for k in keys:
        f.write(json.dumps(k, ensure_ascii=False) + "\n")

# статистика по длине и характеру
groups = {"<70": 0, "70-200": 0, ">200": 0}
for k in keys:
    if len(k) < 70:
        groups["<70"] += 1
    elif len(k) <= 200:
        groups["70-200"] += 1
    else:
        groups[">200"] += 1
print("по длине:", groups)
