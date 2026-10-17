# -*- coding: utf-8 -*-
"""Проверяет, что roadmap-ключи скрипта точно совпадают с untranslated.txt."""
import sys, io, json, importlib.util

sys.stdout.reconfigure(encoding="utf-8")
spec = importlib.util.spec_from_file_location(
    "am2", r"C:\Users\user\AppData\Local\Temp\lp_build\add_menu2.py"
)
src = io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\add_menu2.py", encoding="utf-8").read()
# вырезаем только определения RM* и NEW (без записи файла)
cut = src.index('p = base + r"\\ru.json"')
ns = {}
exec(src[:cut], ns)

p = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch\untranslated.txt"
data = io.open(p, encoding="utf-8", errors="replace").read()

def in_file(key):
    """Ключ в файле записан экранированным — сверяем через экранирование как в DLL."""
    esc = key.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{esc}": ""' in data

for name in ("RM1", "RM2", "RM3"):
    k = ns[name]
    print(name, "в файле:", in_file(k))
