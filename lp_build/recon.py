# -*- coding: utf-8 -*-
"""Разведка ru.json: названия-кандидаты на удаление + наличие описаний."""
import json, re, io, sys

p = r"C:\Users\user\Desktop\Nuclear Option\BepInEx\plugins\LocalizationPatch\ru.json"
raw = io.open(p, encoding='utf-8-sig').read()
lines = [l for l in raw.split('\n') if not l.strip().startswith('//')]
clean = '\n'.join(lines)
clean = re.sub(r',\s*([}\]])', r'\1', clean)
data = json.loads(clean, strict=False)
sys.stdout.reconfigure(encoding='utf-8')
print("entries:", len(data))

# 1) конкретные названия из списка пользователя + похожие
names = [
    "Infantry Squad", "RAB Container", "RAB container", "LCV25 SAM",
    "Naval Supply Container", "GPO-N (1.5kt)", "GBM-500LR",
    "Radar Jamming Pod", "Tusko-B (HE) x4", "IRM-S2", "LCV25 Cannon",
    "LCV25", "Fuel Container 1500L", "Fuel Container 10,000L", "70mm Cannon",
    "GS25", "NL-98", "127mm Guided Shell", "Eyeball Mk.II", "AT-145 Emplacement",
    "Alkyon AB-4", "CI-22 Cricket", "GPO-N (250kt)",
]
print("\n=== названия из списка ===")
for n in names:
    if n in data:
        print(f"  ЕСТЬ: {n!r} => {data[n]!r}")
    else:
        print(f"  нет:  {n!r}")

# 2) все короткие ключи с оружиевыми паттернами (кандидаты на удаление перевода)
pat = re.compile(
    r'^(AAM[- ]|AGM[- ]|ALM[- ]|AShM|AGR[- ]|PAB[- ]|GPO[- ]|GBM[- ]|NL[- ]|IRM[- ]|'
    r'Tusko|Eyeball|GS25|AT-145|LCV25|RAB |Radome|\d+([.,]\d+)?mm\b|'
    r'.*\b(Cannon|Autocannon|Rotary|Shell|Rocket|Bomb|Missile|Pod|Warhead|'
    r'Submunition|Container|Machine Gun|Howitzer|Launcher)\b)',
    re.I)
print("\n=== все ключи-названия с паттернами (<=60 символов) ===")
for k in sorted(data):
    if len(k) <= 60 and pat.match(k):
        print(f"  {k!r} => {data[k]!r}")

# 3) есть ли описание CI-22
print("\n=== описание CI-22 (поиск) ===")
for k in data:
    if "CI-22" in k and len(k) > 60:
        print("  КЛЮЧ:", k[:130])
        print("  ПЕР:", data[k][:80])
    if "counter insurgency" in k.lower():
        print("  НАЙДЕНО 'counter insurgency':", k[:130])

# 4) длинные ключи-описания, начинающиеся с названий предметов (есть ли описания предметов)
print("\n=== описания, содержащие названия предметов ===")
for k in data:
    if len(k) > 60 and re.search(r'(infantry squad|container|LCV25|GPO|GBM|IRM|Tusko)', k, re.I):
        print(" ", k[:100])
