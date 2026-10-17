# -*- coding: utf-8 -*-
"""Выгружает длинные miss-строки из лога в файл целиком."""
import sys, re, io

sys.stdout.reconfigure(encoding="utf-8")
p = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\LogOutput.log"
data = open(p, "rb").read().decode("utf-8", "replace")
miss = re.findall(r'\[TRACE\] miss: ("(?:[^"\\]|\\.)*")', data)
out = io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\miss_full.txt", "w", encoding="utf-8")
n = 0
for s in miss:
    if len(s) > 100:
        n += 1
        out.write("=" * 60 + f"\n#{n}\n" + s + "\n")
out.close()
print("длинных miss:", n)
