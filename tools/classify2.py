# -*- coding: utf-8 -*-
"""Классифицирует свежий untranslated.txt: kill-feed / числа / реальный текст."""
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
    if any(v in low for v in VERBS) and ("color=" in k or "\n" in k):
        return "feed"
    s = re.sub(r"[<>?=/%:.,()\\s\\-$+0-9a-zA-Z#Ω°\[\]']", "", plain)
    if len(s.strip()) <= 1:
        return "numeric"
    if re.fullmatch(r"[\d\s.,:/a-zA-Z\[\]+\-]+$", plain) and len(plain) < 25:
        return "short_mixed"
    return "real"

buckets = Counter()
groups = {"feed": [], "numeric": [], "short_mixed": [], "real": []}
for k in keys:
    c = classify(k)
    buckets[c] += 1
    groups[c].append(k)

print("всего ключей:", len(keys))
for name, cnt in buckets.most_common():
    print(f"  {name}: {cnt}")

print("\n===== КОРНЕВЫЕ ГЛАГОЛЫ KILL-FEED (что не покрыто) =====")
verb_pat = re.compile(r"</color>\s*([a-z ]+?)\s*(?:<color|$)")
vc = Counter()
for k in groups["feed"]:
    plain = k.replace("\n", " | ")
    for seg in plain.split(" | "):
        m = verb_pat.match(seg.strip())
        if m:
            vc[m.group(1)] += 1
for v, c in vc.most_common(30):
    print(f"{c:6}  {v!r}")

print("\n===== REAL: первые 120 =====")
seen = set()
n = 0
for k in groups["real"]:
    kk = k[:120]
    if kk in seen:
        continue
    seen.add(kk)
    n += 1
    if n > 120:
        break
    print(f"{n:3}. {k[:150]!r}")

out = io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\cand3.jsonl", "w", encoding="utf-8")
for k in groups["real"]:
    out.write(json.dumps(k, ensure_ascii=False) + "\n")
out.close()
print("\nreal-ключи сохранены в cand3.jsonl:", len(groups["real"]))
