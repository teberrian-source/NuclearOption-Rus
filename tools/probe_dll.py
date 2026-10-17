# -*- coding: utf-8 -*-
"""Ищет определения оружия в DLL модов (AryxWeaponsPack, Apex-6): контекст вокруг."""
import sys, os, re, glob

sys.stdout.reconfigure(encoding="utf-8")
files = [
    r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\com.nikkorap.blueprinter\addons\aryx.weaponpack\AryxWeaponsPack_1.1.1.dll",
    r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\Apex-6\Apex-6.dll",
]
for p in files:
    if not os.path.exists(p):
        print("нет:", p)
        continue
    data = open(p, "rb").read()
    print("=" * 80)
    print(os.path.basename(p), len(data), "б")
    for q in ("flare-resistant", "Scythe", "MissileDefinition", "Gladius"):
        i = data.find(q.encode())
        print(f"  {q!r}: {'найден ' + str(i) if i >= 0 else 'НЕ найден'}")
        if i >= 0:
            txt = data[max(0, i - 200) : i + 400].decode("utf-8", "ignore")
            txt = re.sub(r"[\x00-\x08\x0b-\x1f]+", " | ", txt)
            print("     ", txt[:400])
