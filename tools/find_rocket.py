# -*- coding: utf-8 -*-
"""Ищет полное описание ракеты 203mm и другие длинные miss-описания в ресурсах."""
import sys, re

sys.stdout.reconfigure(encoding="utf-8")
f = r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data\resources.assets"
data = open(f, "rb").read()

q = "Medium range heavy 203mm"
i = data.find(q.encode())
enc = "utf-8"
if i < 0:
    i = data.find(q.encode("utf-16-le"))
    enc = "utf-16-le"
print("найдено:", i, enc)
if i >= 0:
    raw = data[i : i + 1500]
    text = raw.decode(enc, "ignore")
    # описание до разделителя ';'
    end = text.find(";")
    print("ОПИСАНИЕ:", text[:end] if 0 < end < 1000 else text[:600])

# все длинные описания RocketDefinition/WeaponDefinition со словом rocket
print("\n=== кандидаты с 'laser-guided' ===")
for m in re.finditer(rb"[A-Za-z0-9 ,\.\-'\"()/&:;]{60,400}", data):
    s = m.group().decode("ascii", "ignore")
    if "laser-guided" in s or "203mm" in s:
        print("-", s[:300])
