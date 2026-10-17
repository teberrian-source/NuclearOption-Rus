# -*- coding: utf-8 -*-
"""Показывает сырые байты вокруг roadmap-ключа (CR/LF/escapes)."""
import sys

sys.stdout.reconfigure(encoding="utf-8")
p = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch\untranslated.txt"
data = open(p, "rb").read()
i = data.find(b"Additional Boats / Ships")
seg = data[i - 5 : i + 90]
print("hex:", seg.hex(" "))
print()
print("repr:", repr(seg))
