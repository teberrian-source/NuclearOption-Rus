# -*- coding: utf-8 -*-
"""Строки дампа со словом Sortie."""
import io, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
norm = io.open(base + r"\untranslated.txt", encoding="utf-8", errors="replace").read().replace("\\n", "\n")
seen = set()
for line in norm.split("\n"):
    if "Sortie" in line:
        s = re.sub(r'"\s*:\s*""\s*,?$', "", line.strip())
        if s.startswith('"'):
            s = s[1:]
        if s.startswith("Success"):
            seen.add(s)
print("вариантов:", len(seen))
for s in sorted(seen)[:20]:
    print(repr(s))
