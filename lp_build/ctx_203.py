# -*- coding: utf-8 -*-
"""Печатает контекст лога вокруг описания 203mm (имя оружия)."""
import sys

sys.stdout.reconfigure(encoding="utf-8")
p = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\LogOutput.log"
data = open(p, "rb").read().decode("utf-8", "replace")
i = data.find("Medium range heavy")
print(data[max(0, i - 2500) : i + 400])
