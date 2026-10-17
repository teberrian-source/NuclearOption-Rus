# -*- coding: utf-8 -*-
"""Классификация untranslated.txt: кандидаты на перевод vs пропуск."""
import json, re, io, sys

u = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch\untranslated.txt"
sys.stdout.reconfigure(encoding='utf-8')

keys = []
for line in io.open(u, encoding='utf-8-sig').read().split('\n'):
    line = line.strip()
    if not line.startswith('"'):
        continue
    body = line.rstrip(',')
    try:
        obj = json.loads('{' + body + '}')
    except Exception:
        continue
    keys.append(next(iter(obj)))
print("всего ключей:", len(keys))

# --- SKIP-правила ---
def is_numberish(k):
    # числа, единицы, валюты, размерности
    s = k.replace('<pos=50%>', '').replace('<color=#FFFFFFFF>', '')
    s = re.sub(r'</?color=[^>]*>', '', s)
    s = s.replace('$', '').replace('+', '').replace('(', '').replace(')', '')
    s = re.sub(r'[0-9\s,\.%/:kmghstwWΩkjKMGFP]+', '', s)
    return len(s.strip()) <= 2

WEAPON = re.compile(
    r'^(\d+([.,]\d+)?\s?(mm|km|kg|t|kW|G)\b|.*\((\d+) rounds\)|'
    r'AAM-|AGM-|AGR-|ALM-|AShM|PAB-|GPO-|GBM-|NL-|IRM-|HSM-|Tusko|'
    r'.*\b(Cannon|Autocannon|Gunpod|Machine Gun|Rotary|Container|Drop Tank|Emplacement|AAA)\b|x\d+$)',
    re.I)
MISSION = re.compile(r'^(\[[A-Z0-9-]+\]|\d{2}\.\s)')
GARBAGE = ['This is how wide', 'What the fuck did you', 'A long username']

skip, cand = [], []
for k in keys:
    if any(g in k for g in GARBAGE):
        skip.append(('мусор', k)); continue
    # кракозябры: нет ни латиницы, ни нормальных символов
    if not re.search(r'[A-Za-z]', k):
        skip.append(('не-латиница', k)); continue
    if is_numberish(k):
        skip.append(('число', k)); continue
    if MISSION.search(k):
        skip.append(('миссия-название', k)); continue
    if WEAPON.match(k) and len(k) < 70:
        skip.append(('оружие-название', k)); continue
    cand.append(k)

print("SKIP:", len(skip), "| КАНДИДАТЫ:", len(cand))
print("\n===== КАНДИДАТЫ =====")
for i, k in enumerate(cand, 1):
    print(f"{i:3}. {k!r}")
