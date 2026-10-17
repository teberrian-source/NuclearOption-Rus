# -*- coding: utf-8 -*-
"""Добавляет точные непереведённые описания из untranslated.txt в ru.json с переводами."""
import json, re, io, sys

base = r"C:\Users\user\Desktop\Nuclear Option\BepInEx\plugins\LocalizationPatch"
sys.stdout.reconfigure(encoding='utf-8')

# подстрока поиска -> перевод (точный текст берём из untranslated.txt)
wanted = {
    'Designed for counter insurgency operations':
        'Разработанный для операций по борьбе с повстанцами и боевых действий малой интенсивности, CI-22 Cricket оснащён прочным шасси и возможностью укороченного взлёта и посадки, что позволяет ему действовать с неподготовленных площадок. Несмотря на недостаток скорости и живучести, CI-22 обладает выдающейся манёвренностью и способностью нести широкий спектр вооружений.',
    'Group of 8 troops which stay with the aircraft':
        'Отряд из 8 солдат, которые остаются с самолётом и позволяют захватывать здания и аэродромы при посадке поблизости',
    'Hexhound equipped with an automatic grenade launcher':
        'Hexhound с автоматическим гранатомётом. Гранатомёт способен вести непрямой огонь по целям даталинка на расстоянии до 2 км (1,2 мили).',
    'One single-use containers for replenishing':
        'Одноразовый контейнер для пополнения боезапаса корабля. Оборудован средствами плавучести и может быть подобран кораблями в пределах 200 м после сброса в воду. Не подвергайте контейнеры сильным ударам — они могут взорваться.',
    'A single 10-ton ammo containers':
        'Одиночный 10-тонный контейнер с боеприпасами. На земле обеспечивает непрерывное пополнение боеприпасов наземной техники и самолётов в радиусе 100 м. Не подвергайте контейнеры сильным ударам — они могут взорваться.',
    'Powerful long-range all-aspect radar':
        'Мощная дальнобойная радиолокационная станция кругового обзора, способная обнаруживать самолёты даже на высоте от 5 м (16 футов)',
    'Directional offensive jammer':
        'Направленная станция активных помех, способная «ослепить» одну выбранную РЛС одним контейнером на дальности до 50 км.',
    'Learn how to manage throttle, brake and rudder':
        'Научитесь управлять тягой, тормозом и рулём, чтобы безопасно вырулить на взлётную полосу, а затем выполнить первый взлёт. В этом уроке вы будете пилотировать учебный самолёт T/A-30 Compass.',
}

# 1) точные ключи из untranslated.txt
entries = io.open(base + r"\untranslated.txt", encoding='utf-8-sig').read().split('\n')
keys = {}
for line in entries:
    line = line.strip()
    if not line.startswith('"') or not line.endswith('",') and not line.endswith('"'):
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
print("найдено точных ключей:", len(keys), "| не найдено:", missing)

# 2) добавить в ru.json
p = base + r"\ru.json"
raw = io.open(p, encoding='utf-8-sig').read()
ls = [l for l in raw.split('\n') if not l.strip().startswith('//')]
clean = re.sub(r',\s*([}\]])', r'\1', '\n'.join(ls))
data = json.loads(clean, strict=False)
before = len(data)

idx = raw.rfind('\n}')
assert idx > 0
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
clean = re.sub(r',\s*([}\]])', r'\1', '\n'.join(lines := ls))
data2 = json.loads(clean, strict=False)
print(f"записей: {before} -> {len(data2)}")
assert len(data2) == before + len(new_entries)
io.open(p, 'w', encoding='utf-8', newline='').write(raw)
print("СОХРАНЕНО")
# контроль: точные ключи с точкой
ci = [k for k in data2 if k.startswith('Designed for counter')]
for k in ci:
    print("CI-22 ключ окончание:", repr(k[-40:]))
