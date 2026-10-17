# -*- coding: utf-8 -*-
"""Печатает окрестности 'hardpoint'/'weaponStation'/'mount' в сборке Kar (возможно, там JSON)."""
import io, re, sys

sys.stdout.reconfigure(encoding="utf-8")
p = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\com.nikkorap.blueprinter\addons\kar\Kar_1.1.2.dll"
data = io.open(p, "rb").read()
for n in [b"hardpoint", b"weaponStation", b"mount", b"name", b"subturret", b"turret"]:
    print("#" * 90)
    print("NEEDLE", n.decode())
    for m in list(re.finditer(re.escape(n), data, re.I))[:6]:
        off = m.start()
        chunk = data[max(0, off - 300):off + 300]
        txt = "".join(chr(c) if 32 <= c < 127 else "." for c in chunk)
        print("---", off, "\n", txt)
