# -*- coding: utf-8 -*-
"""Доп. кандидаты раунда 12: строки с <b> (статусы) и короткие предупреждения."""
import io, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
raw = io.open(base + r"\untranslated.txt", encoding="utf-8", errors="replace").read()
keys = []
for m in re.finditer(r'^\s*"((?:[^"\\]|\\.)*)"\s*:\s*""\s*,?\s*$', raw, re.M):
    keys.append(m.group(1).replace('\\"', '"').replace("\\n", "\n"))
uniq = sorted(set(keys))

print("=== строки с <b> (без <color=) ===")
for t in uniq:
    if "<b>" in t and "<color=" not in t:
        print(repr(t))

print("\n=== короткие (<=3 слова) с WARNING/ALERT/CAUTION или ЦЕЛИКОМ КАПСОМ ===")
for t in uniq:
    if "<" in t or "\n" in t:
        continue
    w = t.split()
    if len(w) > 3:
        continue
    if re.search(r"WARNING|ALERT|CAUTION", t) or (t.isupper() and len(t) > 4):
        print(repr(t))
