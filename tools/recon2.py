# -*- coding: utf-8 -*-
"""Точная разведка: CI-22 ключ, Radome, описания предметов."""
import json, re, io, sys

p = r"C:\Users\user\Desktop\Nuclear Option\BepInEx\plugins\LocalizationPatch\ru.json"
raw = io.open(p, encoding='utf-8-sig').read()
lines = [l for l in raw.split('\n') if not l.strip().startswith('//')]
clean = '\n'.join(lines)
clean = re.sub(r',\s*([}\]])', r'\1', clean)
data = json.loads(clean, strict=False)
sys.stdout.reconfigure(encoding='utf-8')

# 1) точный ключ CI-22 и его полный вид (repr) + перевод
print("=== CI-22: точные ключи ===")
for k in data:
    if 'CI-22' in k or 'counter insurgency' in k.lower():
        print("KEY :", repr(k))
        print("VAL :", repr(data[k])[:300])
        print()

# 2) radome описание
print("=== RADOME: все упоминания ===")
for k in data:
    if 'radome' in k.lower():
        print("KEY :", repr(k)[:200])
        print("VAL :", repr(data[k])[:250])
        print()

# 3) описания предметов из списка пользователя
print("=== описания предметов (длинные ключи с названиями) ===")
subj = ['Infantry Squad', 'ECM Pod', 'LCV25', 'Naval Supply', 'GPO-N', 'GBM-500LR',
        'Radar Jamming', 'Tusko-B', 'IRM-S2', 'RADOME']
for k in data:
    if len(k) > 60:
        for s in subj:
            if s.lower() in k.lower():
                has_ru = re.search(r'[а-яё]', data[k], re.I) is not None
                print(f"RU={has_ru} KEY: {k[:120]!r}")
                break
