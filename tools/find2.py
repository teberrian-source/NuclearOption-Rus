# -*- coding: utf-8 -*-
"""Ищет 'Main Turret' и другие подписи слотов в файлах игры (включая resS) и в temp."""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
targets = [
    r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data\resources.assets",
    r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data\sharedassets1.assets",
    r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data\resources.resource",
    r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data\sharedassets1.resource",
    r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data\globalgamemanagers",
]
needles = [b"Main Turret", b"subturret", b"Coaxial", b"Ammo box", b"Truck bed", b"cargo 2x", b"Turret mount"]
for p in targets:
    if not os.path.exists(p):
        print("нет", p); continue
    data = io.open(p, "rb").read()
    print("==", os.path.basename(p), len(data))
    for n in needles:
        c = len(re.findall(re.escape(n), data, re.I))
        if c:
            print("   ", n.decode(), "x", c)
