# -*- coding: utf-8 -*-
"""Показывает сырой фрагмент untranslated.txt с roadmap-ключами (repr)."""
import sys, io

sys.stdout.reconfigure(encoding="utf-8")
p = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch\untranslated.txt"
data = io.open(p, encoding="utf-8", errors="replace").read()
i = data.find("Additional Boats / Ships")
print(repr(data[i - 20 : i + 1300]))
