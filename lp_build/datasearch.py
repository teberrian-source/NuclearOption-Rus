# -*- coding: utf-8 -*-
"""Ищет подписи слотов подвески в файлах данных игры (не в .resS)."""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
root = r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data"
needles = ["subturret", "Truck bed", "Ammo box", "cargo 2x", "Main Turret", "turret mount", "Point Defense"]

for f in sorted(os.listdir(root)):
    if f.endswith((".resS", ".resource")):
        continue
    p = os.path.join(root, f)
    if not os.path.isfile(p):
        continue
    size = os.path.getsize(p)
    if size > 400 * 1024 * 1024:
        print("skip big", f)
        continue
    data = io.open(p, "rb").read()
    n_hits = 0
    for n in needles:
        c = len(re.findall(re.escape(n.encode()), data, re.I))
        if c:
            n_hits += c
            print(f"{f}: '{n}' x{c}")
    if n_hits:
        print("   size", size)
