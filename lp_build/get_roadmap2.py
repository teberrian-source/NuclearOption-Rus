# -*- coding: utf-8 -*-
"""Извлекает полные многострочные roadmap-ключи из untranslated.txt."""
import sys, io, json

sys.stdout.reconfigure(encoding="utf-8")
p = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch\untranslated.txt"
data = io.open(p, encoding="utf-8", errors="replace").read()
keys = []
for q in ("Additional Boats / Ships", "Additional low-rank aircraft", "New large landlocked map"):
    i = data.find(q)
    start = data.rfind('"', 0, i)  # открывающая кавычка
    end = data.find('"', i)        # закрывающая
    key = data[start + 1 : end]
    keys.append(key)
    print("=" * 70)
    print(json.dumps(key, ensure_ascii=False))

io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\roadmap_keys.json", "w", encoding="utf-8").write(
    json.dumps(keys, ensure_ascii=False, indent=1)
)
print("сохранено:", len(keys))
