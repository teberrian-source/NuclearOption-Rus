# -*- coding: utf-8 -*-
"""Сырые строки дампа вокруг дорожной карты и вокруг 'The BDF is on the run'."""
import io, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
dump = io.open(base + r"\untranslated.txt", encoding="utf-8", errors="replace").read()
lines = dump.split("\n")
print("всего строк:", len(lines), "| переводов строк:", dump.count("\n"), "| CR:", dump.count("\r"))

def show(needle, before=2, after=4, limit=2):
    print("=" * 30, needle)
    n = 0
    for i, l in enumerate(lines):
        if needle in l:
            for j in range(max(0, i - before), min(len(lines), i + after)):
                print(f"{j:6} {lines[j]!r}")
            print("   ----")
            n += 1
            if n >= limit:
                break

show("Additional Boats")
show("Weapon safety lock <b>Enabled</b>")
show("The BDF is on the run, and trying")
