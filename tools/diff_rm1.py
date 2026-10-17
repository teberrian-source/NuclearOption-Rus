# -*- coding: utf-8 -*-
"""Сравнивает ключ RM1 с сырым фрагментом файла посимвольно."""
import sys, io, difflib

sys.stdout.reconfigure(encoding="utf-8")
src = io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\add_menu2.py", encoding="utf-8").read()
cut = src.index('p = base + r"\\ru.json"')
ns = {}
exec(src[:cut], ns)

p = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch\untranslated.txt"
data = io.open(p, encoding="utf-8", errors="replace").read()
i = data.find("Additional Boats / Ships")
start = data.rfind('"', 0, i) + 1
end = data.find('": ""', i)
raw_key = data[start:end]  # как записано в файле (экранированно)

mine = ns["RM1"].replace("\n", "\\n")
print("RAW (файл) первые 120:", repr(raw_key[:120]))
print("MINE  первые 120:", repr(mine[:120]))
print("RAW  длина:", len(raw_key), " MINE длина:", len(mine))
# найти первое расхождение
for n, (a, b) in enumerate(zip(raw_key, mine)):
    if a != b:
        print(f"расхождение на {n}: файл={a!r} mine={b!r}")
        print("файл вокруг:", repr(raw_key[max(0, n - 30):n + 30]))
        print("mine вокруг:", repr(mine[max(0, n - 30):n + 30]))
        break
else:
    print("совпадение префикса, остаток:", repr(raw_key[len(mine):len(mine) + 40]), repr(mine[len(raw_key):len(raw_key) + 40]))
