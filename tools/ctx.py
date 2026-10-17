# -*- coding: utf-8 -*-
"""Печатает окружение найденных подписей в resources.assets."""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
p = r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data\resources.assets"
data = io.open(p, "rb").read()
for n in ["turret mount", "Point Defense"]:
    for m in re.finditer(re.escape(n.encode()), data, re.I):
        off = m.start()
        chunk = data[max(0, off - 400):off + 400]
        txt = "".join(chr(c) if 32 <= c < 127 else "." for c in chunk)
        print("=" * 100)
        print(n, "@", off)
        print(txt)
