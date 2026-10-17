# -*- coding: utf-8 -*-
"""Быстрая классификация untranslated: сколько kill-feed / чисел / реального текста."""
import sys, json, io, re
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
u = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch\untranslated.txt"

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

VERBS = ("intercepted", "destroyed", "shot down", "demolished", "sank", "was destroyed",
         "was rescued by", "collapsed", "joined the game", "was captured by", "captured")

def classify(k):
    plain = re.sub(r"</?color=[^>]*>", "", k)
    low = plain.lower()
    if any(v in low for v in VERBS):
        return "feed"
    s = re.sub(r"[^A-Za-zА-Яа-яЁё]", "", plain)
    if len(s) <= 1:
        return "numeric"
    return "real"

buckets = Counter()
groups = {"feed": [], "numeric": [], "real": []}
for k in keys:
    c = classify(k)
    buckets[c] += 1
    groups[c].append(k)

print("всего ключей:", len(keys))
for name, cnt in buckets.most_common():
    print(f"  {name}: {cnt}")

out = io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\cand_real.jsonl", "w", encoding="utf-8")
for k in groups["real"]:
    out.write(json.dumps(k, ensure_ascii=False) + "\n")
out.close()

print("\n===== REAL (уникальные, первые 150) =====")
seen = set()
n = 0
for k in groups["real"]:
    kk = k[:100]
    if kk in seen:
        continue
    seen.add(kk)
    n += 1
    if n > 150:
        break
    print(f"{n:3}. {k[:140]!r}")
