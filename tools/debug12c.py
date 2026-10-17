# -*- coding: utf-8 -*-
import io, re, sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
lines = io.open(base + r"\untranslated.txt", encoding="utf-8", errors="replace").read().split("\n")
print("строк, начинающихся с кавычки и содержащих '•':")
n = 0
for i, l in enumerate(lines):
    if "PALA Landing" in l or "Dynamic music" in l:
        print(f"{i:6} {l!r}")
        n += 1
print("всего таких:", n)
print("\n-- сколько строк начинается с '\"•':", sum(1 for l in lines if l.startswith('"•')))
print("-- есть ли полный ключ-пуля:", any(l == '"• Dynamic music": "",' for l in lines))
