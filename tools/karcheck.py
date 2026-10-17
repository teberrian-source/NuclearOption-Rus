# -*- coding: utf-8 -*-
"""Проверка: как хранятся строки в модовой сборке Kar."""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
p = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\com.nikkorap.blueprinter\addons\kar\Kar_1.1.2.dll"
data = io.open(p, "rb").read()
for n in ["(KAR)", "AFV8", "Linebreaker", "subturret", "Ammo box", "Main Turret", "weaponStation", "hardpoint", "mount"]:
    a = len(re.findall(re.escape(n.encode()), data, re.I))
    u = len(re.findall(re.escape(n.encode("utf-16-le")), data, re.I))
    print(f"{n:<16} ascii={a:<5} utf16={u}")
# найдём любые строки с KAR
print("--- контекст (KAR) ---")
for m in list(re.finditer(rb"\(.{0,2}K.{0,2}A.{0,2}R.{0,2}\)", data))[:5]:
    off = m.start()
    chunk = data[max(0, off - 120):off + 160]
    txt = "".join(chr(c) if 32 <= c < 127 else "." for c in chunk)
    print("   ", off, txt)
