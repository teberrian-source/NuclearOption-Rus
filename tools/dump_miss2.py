# -*- coding: utf-8 -*-
"""Полный уникальный список miss-строк сессии в файл (с номерами)."""
import sys, re, io
from collections import Counter, OrderedDict

sys.stdout.reconfigure(encoding="utf-8")
p = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\LogOutput.log"
data = open(p, "rb").read().decode("utf-8", "replace")
miss = re.findall(r'\[TRACE\] miss: ("(?:[^"\\]|\\.)*")', data)
c = Counter(miss)
out = io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\miss_all.txt", "w", encoding="utf-8")
for i, (s, n) in enumerate(c.most_common(), 1):
    out.write(f"{i:3} x{n} {s}\n")
out.close()
print("уникальных miss:", len(c), " всего:", len(miss))
