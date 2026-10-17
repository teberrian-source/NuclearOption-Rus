# -*- coding: utf-8 -*-
"""Ищет в бинарниках модов подписи слотов подвески и печатает окружение."""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
root = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins"
needles = ["subturret", "turret mount", "Truck bed", "Ammo box", "cargo 2x", "Point Defense"]

for dirpath, dirs, files in os.walk(root):
    if "LocalizationPatch" in dirpath:
        continue
    for f in files:
        p = os.path.join(dirpath, f)
        try:
            data = io.open(p, "rb").read()
        except Exception:
            continue
        hits = []
        for n in needles:
            for m in re.finditer(re.escape(n.encode()), data, re.I):
                hits.append((n, m.start()))
        if not hits:
            continue
        print("=" * 100)
        print("FILE:", p, os.path.getsize(p))
        seen = set()
        for n, off in sorted(hits, key=lambda x: x[1]):
            if off in seen:
                continue
            seen.add(off)
            chunk = data[max(0, off - 220):off + 220]
            txt = "".join(chr(c) if 32 <= c < 127 else "." for c in chunk)
            print(f"--- {n} @ {off}")
            print("   ", txt)
