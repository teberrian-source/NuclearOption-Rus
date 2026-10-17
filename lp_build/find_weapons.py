# -*- coding: utf-8 -*-
"""Найти в ru.json ключи-названия вооружения (кандидаты на удаление перевода)."""
import json, re, io, sys

p = r"C:\Users\user\Desktop\Nuclear Option\BepInEx\plugins\LocalizationPatch\ru.json"
raw = io.open(p, encoding='utf-8-sig').read()
lines = [l for l in raw.split('\n') if not l.strip().startswith('//')]
clean = '\n'.join(lines)
clean = re.sub(r',\s*([}\]])', r'\1', clean)
data = json.loads(clean)
sys.stdout.reconfigure(encoding='utf-8')
print("entries:", len(data))

pat = re.compile(
    r'^(AAM[- ]|AGM[- ]|AGR[- ]|PAB[- ]|GPO[- ]|GBM[- ]|NL[- ]|IRM[- ]|'
    r'Tusko|Eyeball|GS25|AT-145|\d+mm\b|.*\b(Cannon|Autocannon|Rotary|Shell|Rocket|'
    r'Bomb|Missile|Pod|Howitzer|Launcher|Warhead|Submunition|Gunpod|Cluster)\b)',
    re.I)

cands = [k for k in data if len(k) <= 60 and pat.match(k)]
for c in sorted(cands):
    print(repr(c), "=>", repr(data[c])[:70])
print("TOTAL:", len(cands))
