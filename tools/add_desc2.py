# -*- coding: utf-8 -*-
"""Добавляет вторую партию описаний (паллеты, 6000L, лазер, GMG) в ru.json."""
import json, re, io, sys

base = r"C:\Users\user\Desktop\Nuclear Option\BepInEx\plugins\LocalizationPatch"
sys.stdout.reconfigure(encoding='utf-8')

wanted = {
    'Automatic grenade launcher firing low-velocity 40mm':
        'Автоматический гранатомёт, стреляющий малоскоростными 40-мм осколочными боеприпасами; идеален для уничтожения небольших зданий и групп легкобронированных целей',
    'A 6-ton munitions pallet for replenishing':
        '6-тонная паллета с боеприпасами для пополнения боезапаса корабля. Имеет средства плавучести и может быть подобрана кораблями в пределах 200 м после сброса в воду. Не подвергайте паллеты сильным ударам — они могут взорваться.',
    'A 6-ton munitions pallet. When placed':
        '6-тонная паллета с боеприпасами. На земле обеспечивает непрерывное пополнение боеприпасов наземной техники и самолётов в радиусе 100 м. Не подвергайте паллеты сильным ударам — они могут взорваться.',
    'An air transportable 6000L fuel tank':
        'Перевозимый по воздуху топливный бак на 6000 л, разворачиваемый на передовых оперативных базах.',
    'High energy laser weapon designed':
        'Лазерное оружие высокой энергии, предназначенное для перехвата ракет и бомб на дальности до 15 км.',
}

# точные ключи из untranslated.txt
entries = io.open(base + r"\untranslated.txt", encoding='utf-8-sig').read().split('\n')
keys = {}
for line in entries:
    line = line.strip()
    if not line.startswith('"'):
        continue
    body = line.rstrip(',')
    try:
        obj = json.loads('{' + body + '}')
    except Exception:
        continue
    k = next(iter(obj))
    for sub, tr in wanted.items():
        if sub in k:
            keys[sub] = k
missing = [s for s in wanted if s not in keys]
print("найдено:", len(keys), "| не найдено:", missing)

p = base + r"\ru.json"
raw = io.open(p, encoding='utf-8-sig').read()
ls = [l for l in raw.split('\n') if not l.strip().startswith('//')]
clean = re.sub(r',\s*([}\]])', r'\1', '\n'.join(ls))
data = json.loads(clean, strict=False)
before = len(data)

idx = raw.rfind('\n}')
head, tail = raw[:idx], raw[idx:]
if not head.rstrip().endswith(','):
    head = head.rstrip() + ','

new_entries = []
for sub, tr in wanted.items():
    k = keys.get(sub)
    if not k:
        continue
    if k in data:
        print("  уже есть:", repr(k[:55]))
        continue
    new_entries.append('    ' + json.dumps(k, ensure_ascii=False) + ': ' + json.dumps(tr, ensure_ascii=False))
if new_entries:
    raw = head + '\n' + ',\n'.join(new_entries) + tail

ls = [l for l in raw.split('\n') if not l.strip().startswith('//')]
clean = re.sub(r',\s*([}\]])', r'\1', '\n'.join(ls))
data2 = json.loads(clean, strict=False)
print(f"записей: {before} -> {len(data2)}")
assert len(data2) == before + len(new_entries)
io.open(p, 'w', encoding='utf-8', newline='').write(raw)
print("СОХРАНЕНО")
