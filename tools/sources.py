# -*- coding: utf-8 -*-
"""Показывает, из каких полей (метки // Тип.Поле) пришли строки в extracted_strings.txt."""
import io, re, sys, json
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
raw = io.open(base + r"\extracted_strings.txt", encoding="utf-8", errors="replace").read()
raw = raw.split("// ========== RAW LONG STRINGS")[0]

cur = "?"
cnt = Counter()
for line in raw.split("\n"):
    s = line.strip()
    if s.startswith("//"):
        src = s[2:].strip()
        if src and "===" not in src:
            cur = src
        continue
    m = re.match(r'^"((?:[^"\\]|\\.)*)": ""', s)
    if m:
        cnt[cur] += 1

print("источников:", len(cnt))
for src, n in cnt.most_common(60):
    print(f"{n:>5}  {src}")
