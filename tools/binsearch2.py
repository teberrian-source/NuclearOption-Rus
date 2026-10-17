# -*- coding: utf-8 -*-
"""Ищет подписи слотов подвески только в указанных DLL (быстро)."""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
root = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins"
files = [
    r"PlayableVehicles\PlayableVehicles.dll",
    r"Apex-6\Apex-6.dll",
    r"com.nikkorap.blueprinter\addons\kar\Kar_1.1.2.dll",
    r"com.nikkorap.blueprinter\addons\bote\Bote_1.5.2.dll",
    r"NavalPower\NavalPower.dll",
]
needles = ["subturret", "turret mount", "Truck bed", "Ammo box", "cargo 2x", "Point Defense", "Point Defence", "coax"]

for rel in files:
    p = os.path.join(root, rel)
    if not os.path.exists(p):
        print("нет файла", p); continue
    data = io.open(p, "rb").read()
    hits = []
    for n in needles:
        for m in re.finditer(re.escape(n.encode()), data, re.I):
            hits.append((m.start(), n))
    print("=" * 100)
    print("FILE:", rel, os.path.getsize(p), "hits:", len(hits))
    for off, n in sorted(hits)[:40]:
        chunk = data[max(0, off - 160):off + 160]
        txt = "".join(chr(c) if 32 <= c < 127 else "." for c in chunk)
        print(f"--- {n} @ {off}\n    {txt}")
