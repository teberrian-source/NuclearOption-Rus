# -*- coding: utf-8 -*-
"""Прототип фильтра мусора: проверяем на текущем экспорте, что отсеивается, а что остаётся."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
raw_un = open(base + r"\untranslated.txt", "rb").read().decode("utf-8", "replace")
keys = []
for m in re.finditer(r'"((?:[^"\\]|\\.)*)": ""', raw_un):
    try:
        keys.append(json.loads('"' + m.group(1) + '"'))
    except Exception:
        pass
print("всего в экспорте:", len(keys))

JUNK = [
    r"^\s*[\d\.,]+\s*(kg|km|km/h|kt|t|s|ms|%|h|g|G|k|m|b|m/s|kW/kg|kN|MW|m2|ft|nm)?\s*$",   # числа и единицы
    r"^\s*[\d\.,]+\s*t?\s*/\s*[\d\.,]+\s*t?\s*$",                                            # диапазоны масс
    r"^\s*(\$|€|£)[\d\.,]+\s*[kmb]?\s*$",                                                    # деньги
    r"^\s*[A-Z]{0,4}\s*:?\s*(\$|€|£)[\d\.,]+\s*[kmb]?\s*$",                                  # C: $60,0k
    r"^\s*[\d\.,]+\s*[mMbB]?\s*\$\s*$",                                                      # 380.1M$
    r"^\s*[\d\.,]+\s*[mMbB]\s*\(\+[\d\.,]+\s*[mMbB]\)\s*$",                                  # 12.34m (+2.55m)
    r"^\s*\S{1,4}\s*:\s*[\d\.,]+\s*[A-Za-zА-Яа-я%]{0,6}\s*$",                                 # R: 20km, HE: 100kg, ЭПР: 0.001
    r"^\s*%?\s*[A-ZА-Я]{1,6}\s*:?\s*[\d\.,]+\s*%?\s*$",                                       # AP: 450
    r"^\s*\d+\s+(YES|NO)\s*$",                                                               # 99 YES
    r"^\s*x\s+\d+\s*$",                                                                      # x 2
    r"^\s*[A-Z][a-z]\d{2,3}\s*$",                                                            # Ga94 (сетка)
    r"^\s*Time\b.*\d.*Duration\b.*$",                                                        # таймеры
    r"^\s*Score\b.*\d.*$",                                                                   # Score ...
    r"^\s*Pass\s*:\s*\d+\s*$",
    r"^\s*RANK\s+\d+.*$",
    r"^\s*[\d\.,]+\s*(kW|kg)/kg\s*$",
    r"^\s*%?\s*[A-ZА-Я]{1,6}\s*$",           # только аббревиатура без цифр — проверяем отдельно ниже
]

kept, dropped = [], []
for k in keys:
    if any(re.match(p, k) for p in JUNK[:17]):
        dropped.append(k)
    else:
        kept.append(k)

print(f"\nотсеяно: {len(dropped)}   остаётся: {len(kept)}")
print("\n--- ОСТАЁТСЯ (проверить глазами) ---")
for k in kept:
    print("  ", json.dumps(k, ensure_ascii=False)[:110])
