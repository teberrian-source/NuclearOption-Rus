# -*- coding: utf-8 -*-
"""Показывает окружение подписей слотов в resources.assets и в aa-бандлах."""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
files = [
    r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data\resources.assets",
    r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data\StreamingAssets\aa\StandaloneWindows64\defaultlocalgroup_assets_all_4f72d928a181be6a6cb9aee9ac38f476.bundle",
    r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data\StreamingAssets\aa\StandaloneWindows64\skins_assets_all_88de9169e4d0cdc55253aeff4b669446.bundle",
]
needles = [b"Turret mount", b"Coaxial", b"subturret", b"Ammo box", b"Main Turret", b"Point Defense"]
for p in files:
    if not os.path.exists(p):
        continue
    data = io.open(p, "rb").read()
    print("#" * 100)
    print(os.path.basename(p), len(data))
    for n in needles:
        for m in re.finditer(re.escape(n), data, re.I):
            off = m.start()
            chunk = data[max(0, off - 260):off + 260]
            txt = "".join(chr(c) if 32 <= c < 127 else "." for c in chunk)
            print("=" * 90)
            print(n.decode(), "@", off)
            print(txt)
