# -*- coding: utf-8 -*-
"""repr-дамп фрагмента свежего untranslated.txt (строки 20-70)."""
import io, sys

sys.stdout.reconfigure(encoding="utf-8")
un = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch\untranslated.txt"
txt = io.open(un, encoding="utf-8", errors="replace").read()
lines = txt.split("\n")
print("всего строк:", len(lines), " всего символов:", len(txt))
for i in range(20, min(70, len(lines))):
    print(f"{i+1:3}: {lines[i]!r}")
