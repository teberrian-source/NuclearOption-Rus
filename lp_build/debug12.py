# -*- coding: utf-8 -*-
"""Отладка: почему ключи раунда 12 не находятся в дампе."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
dump = io.open(base + r"\untranslated.txt", encoding="utf-8", errors="replace").read()

for needle in ["Additional Boats", "The BDF is on the run", "and remember, they can still"]:
    print("=" * 20, needle)
    n = 0
    for m in re.finditer(re.escape(needle), dump):
        s = m.start()
        ls = dump.rfind("\n", 0, s) + 1
        le = dump.find("\n", s)
        line = dump[ls:le]
        print("RAW:", repr(line[:160]))
        n += 1
        if n >= 2:
            break

print("\n--- проверка пар ---")
tests = [
    "• Additional Boats / Ships",
    "The BDF is on the run, and trying to evacuate as much fuel from the area as they can.",
]
for t in tests:
    print(repr(t))
    print("  codepoints:", [hex(ord(c)) for c in t[:12]])
