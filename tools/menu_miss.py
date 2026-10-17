# -*- coding: utf-8 -*-
"""Собирает miss/hit из TRACE-строк лога последней сессии."""
import sys, re
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
p = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\LogOutput.log"
data = open(p, "rb").read().decode("utf-8", "replace")

miss = re.findall(r'\[TRACE\] miss: ("(?:[^"\\]|\\.)*")', data)
hit = re.findall(r"\[TRACE\] hit:", data)
print("hit:", len(hit), " miss:", len(miss))

c = Counter(miss)
for s, n in c.most_common(80):
    print(f"{n:3} {s[:160]}")
