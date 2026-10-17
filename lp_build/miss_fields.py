# -*- coding: utf-8 -*-
"""Все длинные строки дампа, которых нет в ru.json — по полям."""
import io, json, re, sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

def parse_json(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse_json(base + r"\ru.json")
raw = io.open(base + r"\extracted_strings.txt", encoding="utf-8", errors="replace").read()
raw = raw.split("// ========== RAW LONG STRINGS")[0]
cur, groups = "?", defaultdict(list)
for line in raw.split("\n"):
    s = line.strip()
    if s.startswith("//"):
        x = s[2:].strip()
        if x and "===" not in x:
            cur = x
        continue
    m = re.match(r'^"((?:[^"\\]|\\.)*)":\s*""', s)
    if not m:
        continue
    try:
        t = json.loads('"' + m.group(1) + '"')
    except Exception:
        continue
    if t not in ru:
        groups[cur].append(t)

tot = sum(len(v) for v in groups.values())
print("нет в ru.json:", tot)
for f, items in sorted(groups.items(), key=lambda kv: -len(kv[1])):
    print(f"\n### {f}  ({len(items)})")
    for t in items[:12]:
        print("   ", t[:150].replace("\n", " / "))
