# -*- coding: utf-8 -*-
"""Извлекает все определения/описания из TextAsset (resources.assets 3783),
сравнивает с ru.json: чего не хватает. Плюс строка Radome целиком."""
import sys, json, re, io
import UnityPy

root = r"C:\Users\user\Desktop\Nuclear Option\NuclearOption_Data"
sys.stdout.reconfigure(encoding='utf-8')

env = UnityPy.load(root + r"\resources.assets")
asset = None
for obj in env.objects:
    if obj.type.name == "TextAsset" and obj.path_id == 3783:
        asset = obj.read().m_Script
        break
print("asset len:", len(asset))

# типы строк
types = re.findall(r'^([A-Za-z]+);', asset, re.M)
from collections import Counter
print("types:", Counter(types))

# строки Radome целиком
for line in asset.split('\n'):
    if 'Radome' in line and 'Aircraft' not in line:
        print("RADOME LINE:", repr(line))

# все строки: поле описания = 4-е (index 3) для Definition-строк
descs = {}
for line in asset.split('\n'):
    parts = line.split(';')
    if len(parts) >= 4 and parts[0].endswith('Definition'):
        name, desc = parts[1], parts[3]
        if desc.strip():
            descs[name] = (parts[0], desc)

print("\nописаний в игре:", len(descs))

# ru.json
p = r"C:\Users\user\Desktop\Nuclear Option\BepInEx\plugins\LocalizationPatch\ru.json"
raw = io.open(p, encoding='utf-8-sig').read()
lines = [l for l in raw.split('\n') if not l.strip().startswith('//')]
clean = re.sub(r',\s*([}\]])', r'\1', '\n'.join(lines))
data = json.loads(clean, strict=False)

missing = []
present = []
for name, (typ, desc) in sorted(descs.items()):
    if desc in data:
        has_ru = bool(re.search(r'[а-яё]', data[desc], re.I))
        present.append((name, has_ru))
    else:
        missing.append((name, typ, desc))

print("\n=== есть в ru.json:", len(present), "| НЕТ:", len(missing), "===")
print("\n--- НЕДСТАЮЩИЕ описания ---")
for name, typ, desc in missing:
    print(f"[{typ}] {name}: {desc[:160]}")

print("\n--- есть, но НЕ переведено (нет кириллицы) ---")
for name, has_ru in present:
    if not has_ru:
        print(name)
