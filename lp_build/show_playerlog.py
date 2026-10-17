# -*- coding: utf-8 -*-
"""Печатает контекст 'Medium range heavy' из Player.log (полный текст)."""
import sys, re

sys.stdout.reconfigure(encoding="utf-8")
p = r"C:\Users\user\AppData\LocalLow\Shockfront\NuclearOption\Player.log"
data = open(p, "rb").read().decode("utf-8", "replace")
i = data.find("Medium range heavy")
print("pos:", i, "len:", len(data))
seg = data[max(0, i - 800) : i + 1200]
print(seg)
