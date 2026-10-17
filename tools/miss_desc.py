# -*- coding: utf-8 -*-
"""Описания обучения/миссий и брифинги в дампе: поиск по ключевым фразам."""
import io, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
norm = io.open(base + r"\untranslated.txt", encoding="utf-8", errors="replace").read().replace("\\n", "\n")

needles = ["Learn how", "lesson", "engineer team", "immobilised", "immobilized"]
seen = set()
for line in norm.split("\n"):
    s = re.sub(r'"\s*:\s*""\s*,?$', "", line.strip())
    if s.startswith('"'):
        s = s[1:]
    if any(n in s for n in needles) and s not in seen:
        seen.add(s)
print("найдено строк:", len(seen))
for s in sorted(seen):
    print(repr(s))
