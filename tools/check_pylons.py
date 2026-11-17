# -*- coding: utf-8 -*-
"""Проверка 'Wingtip Rails'/'Belly' в дампе и словаре."""
import io, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAW = r"C:\Users\user\Desktop\Nuclear.Option.v0.34.6\BepInEx\plugins\LocalizationPatch\extracted_strings.txt"
DICT = r"C:\Users\user\Documents\NuclearOption_Rus\dict\ru.json"

raw = io.open(RAW, encoding="utf-8", errors="replace").read()
for k in ["Wingtip Rails", "Belly", "Wingtip"]:
    hits = [l for l in raw.splitlines() if k in l]
    print("###", k, "->", len(hits))
    for h in hits[:4]:
        print("  ", h[:160])

d = io.open(DICT, encoding="utf-8-sig").read()
key = '"Belly"'
print("в словаре key Belly:", key in d)
print("в словаре Wingtip Rails:", "Wingtip Rails" in d)
