# -*- coding: utf-8 -*-
"""Печатает реальные строки дампа для подписей-кандидатов."""
import io, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
norm = io.open(base + r"\untranslated.txt", encoding="utf-8", errors="replace").read().replace("\\n", "\n")

labels = [
    "Return To Base", "Search For Convoy", "Break Blockade", "Defend Island",
    "Destroy Vehicles", "Detected units", "Repaired unit", "Take Off",
    "Taxi", "Cleared for landing on Runway", "Cleared to taxi to Runway",
    "Successfull Sortie", "Mobile FOB",
]
for lab in labels:
    hits = set()
    for line in norm.split("\n"):
        s = re.sub(r'"\s*:\s*""\s*,?$', "", line.strip())
        if s.startswith('"'):
            s = s[1:]
        if s.startswith(lab + " "):
            hits.add(s)
    print(f"--- {lab!r}: {len(hits)}")
    for h in sorted(hits)[:6]:
        print("    ", repr(h))
