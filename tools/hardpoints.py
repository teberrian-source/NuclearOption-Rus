# -*- coding: utf-8 -*-
"""Достаёт список подписей хардпоинтов из resources.assets вокруг найденного блока."""
import io, re, sys

sys.stdout.reconfigure(encoding="utf-8")
p = r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data\resources.assets"
data = io.open(p, "rb").read()
off = 137372222
win = data[max(0, off - 40000):off + 40000]
print("окно:", len(win), "байт вокруг", off)
strs = re.findall(rb"[ -~]{3,}", win)
seen = []
for s in strs:
    t = s.decode("ascii", "replace").strip()
    if not t:
        continue
    seen.append(t)
print("строк:", len(seen))
for t in seen:
    print("  |", t)
