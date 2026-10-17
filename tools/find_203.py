# -*- coding: utf-8 -*-
"""Ищет полное описание ракеты по кускам ('203mm', 'keep it selected')."""
import sys, re

sys.stdout.reconfigure(encoding="utf-8")
f = r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data\resources.assets"
data = open(f, "rb").read()

for q in ("203mm", "keep it selected to provide guidance", "laser-guided rocket"):
    i = data.find(q.encode())
    print(f"--- {q!r}: {i}")
    if i >= 0:
        text = data[max(0, i - 400) : i + 600].decode("utf-8", "ignore")
        text = re.sub(r"[\x00-\x08\x0b-\x1f]+", " | ", text)
        print(text)
        print()
