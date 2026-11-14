# -*- coding: utf-8 -*-
"""Что из видимого на скринах 0.34.6 уже есть в словаре."""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
desk = os.path.join(os.environ["USERPROFILE"], "Desktop")
ru = os.path.join(desk, "Nuclear.Option.v0.34.6", "BepInEx", "plugins", "LocalizationPatch", "ru.json")
t = io.open(ru, encoding="utf-8-sig").read()

needles = [
    "Centreline", "CenterLine", "Middle Pylons", "Wingtip", "Aft Bay",
    "Forward Bay", "Форвард", "Recent", "Laser C-RAM",
    "twin-engine, fourth-generation", "older but proven design",
    "Long-endurance multirole", "MiG-15s in the big",
    "NEEDS: NOCustomMaps", "Cascadia Falling. PALA attacks",
    "rounds)",
]
for n in needles:
    ms = [m.group(0) for m in re.finditer(r"[^\n]*" + re.escape(n) + r"[^\n]*", t)]
    print("###", n, "->", len(ms))
    for m in ms[:3]:
        print("   ", m[:110])
