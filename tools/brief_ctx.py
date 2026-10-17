# -*- coding: utf-8 -*-
"""Контекст вокруг строки-брифинга в resources.assets (как хранится текст миссий)."""
import io, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data\resources.assets"
data = open(p, "rb").read()
needle = b"engineer team is currently trying"

for i, m in enumerate(re.finditer(re.escape(needle), data)):
    s = max(0, m.start() - 700)
    e = min(len(data), m.end() + 700)
    chunk = data[s:e]
    print(f"=== совпадение {i} @ {m.start()}")
    print(repr(chunk[:1400]))
    if i >= 3:
        break
