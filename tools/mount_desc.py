# -*- coding: utf-8 -*-
"""obj=3793: все описания узлов (WeaponMount), сравнение с ru.json, строка Radome."""
import sys, json, re, io
from collections import Counter
import UnityPy

root = r"C:\Users\user\Desktop\Nuclear Option\NuclearOption_Data"
sys.stdout.reconfigure(encoding='utf-8')

env = UnityPy.load(root + r"\resources.assets")
asset = None
for obj in env.objects:
    if obj.type.name == "TextAsset" and obj.path_id == 3793:
        asset = obj.read().m_Script
        break
print("asset len:", len(asset))

lines = asset.split('\n')
types = Counter(re.findall(r'^([A-Za-z]+);', asset, re.M))
print("types:", types)

# все строки: найти поля, похожие на описание (содержат точку предлож. или длинные)
desc_fields = []
for line in lines:
    if not line.strip():
        continue
    parts = line.split(';')
    for idx, f in enumerate(parts):
        if len(f) > 40 and re.search(r'\b(the|a|an|is|are|for|with)\b', f, re.I) and ' ' in f:
            desc_fields.append((parts[0], parts[1] if len(parts) > 1 else '', idx, f))

print("полей-описаний:", len(desc_fields))
# ru.json
p = r"C:\Users\user\Desktop\Nuclear Option\BepInEx\plugins\LocalizationPatch\ru.json"
raw = io.open(p, encoding='utf-8-sig').read()
ls = [l for l in raw.split('\n') if not l.strip().startswith('//')]
clean = re.sub(r',\s*([}\]])', r'\1', '\n'.join(lines2 := ls))
data = json.loads(clean, strict=False)

missing = []
for typ, name, idx, f in desc_fields:
    if f not in data:
        missing.append((typ, name, idx, f))

print("\n=== НЕТ в ru.json:", len(missing), "===")
for typ, name, idx, f in missing:
    print(f"[{typ}] {name} field{idx}: {f[:200]}")

# строка Radome целиком
print("\n=== Radome строка ===")
for line in lines:
    if re.search(r'\bRadome\d?;', line):
        print(repr(line))
