# -*- coding: utf-8 -*-
"""Проверка roadmap-ключей в формате старой DLL (без удвоения слэшей)."""
import sys, io

sys.stdout.reconfigure(encoding="utf-8")
src = io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\add_menu2.py", encoding="utf-8").read()
cut = src.index('p = base + r"\\ru.json"')
ns = {}
exec(src[:cut], ns)

p = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch\untranslated.txt"
data = io.open(p, encoding="utf-8", errors="replace").read()

for name in ("RM1", "RM2", "RM3"):
    k = ns[name]
    esc_old = k.replace("\n", "\\n")   # старая DLL: только перевод строки
    esc_new = k.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")  # новая DLL
    print(name, "старый формат:", f'"{esc_old}": ""' in data, "| новый формат:", f'"{esc_new}": ""' in data)
