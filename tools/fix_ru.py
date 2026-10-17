# -*- coding: utf-8 -*-
"""Правки ru.json: возврат английских названий + добавление 8 описаний."""
import json, re, io, shutil, sys

p = r"C:\Users\user\Desktop\Nuclear Option\BepInEx\plugins\LocalizationPatch\ru.json"
bak = p + ".bak2"
sys.stdout.reconfigure(encoding='utf-8')

shutil.copy2(p, bak)
print("бэкап:", bak)
raw = io.open(p, encoding='utf-8-sig').read()

# 1) названия → вернуть оригинал (value = key)
names = [
    'Infantry Squad', 'ECM Pod', 'LCV25 SAM', 'LCV25 Cannon',
    'Naval Supply Container', 'GPO-N (1.5kt)', 'GBM-500LR', 'Radar Jamming Pod',
    'Tusko-B (HE) x4', 'IRM-S2', 'RADOME',
    'Fuel Container 1500L', 'Fuel Container 10,000L', '70mm Cannon', 'GS25', 'NL-98',
    '127mm Guided Shell', 'Eyeball Mk.II', 'AT-145 Emplacement',
    'AAM -', 'AAM ?', 'AGM -', 'AGM ?',
    'Bomb', 'Cannon', 'Machine Gun', 'Missile', 'Rocket', 'Nuclear Warhead', 'Warhead',
    'Rotary Cannon', 'Internal Cannon', 'Single Container', 'Main Container',
    'Detonating missile ',
]
changed = 0
for n in names:
    pat = re.compile('("' + re.escape(n) + r'"\s*:\s*)"(?:[^"\\]|\\.)*"')
    new, cnt = pat.subn(lambda m: m.group(1) + '"' + n + '"', raw)
    if cnt == 1 and new != raw:
        raw = new
        changed += 1
    elif cnt == 0:
        print("  НЕ НАЙДЕН:", repr(n))
    elif cnt > 1:
        print("  НЕСКОЛЬКО СОВПАДЕНИЙ:", repr(n), cnt)
print("заменено названий:", changed)

# 2) добавить недостающие описания (перед закрывающей скобкой)
add = {
    'An advanced jet trainer which is well suited for light combat duty, the T/A-30 is highly maneuverable at low to medium speeds and possesses forgiving flight characteristics. Particularly adept at low-altitude strike missions, the Compass features redundant control surfaces and twin engines to improve survivability. ':
        'Продвинутый учебный реактивный самолёт, отлично подходящий для лёгких боевых задач. T/A-30 высоко маневрен на малых и средних скоростях и обладает лётными характеристиками, прощающими пилоту ошибки. Особенно хорош для ударов на малой высоте: у Compass дублированные органы управления и два двигателя для повышенной живучести. ',
    'Combining vertical lift capability with a 20 ton cargo capacity, this large quad tiltwing can deliver crucial supplies to forward positions or serve as a versatile gunship. Its 4 proprotors are linked by internal driveshafts, allowing the Tarantula to continue flying after absorbing significant damage. ':
        'Сочетая возможности вертикального взлёта и грузоподъёмность в 20 тонн, этот крупный четырёхвинтовой тилтвинг может доставлять важнейшие припасы на передовые позиции или служить универсальным штурмовиком. Его 4 проточных винта связаны внутренними валами, что позволяет Tarantula продолжать полёт даже после серьёзных повреждений. ',
    'long range air defense trailer capable of engaging aerial targets detected by nearby radar trucks':
        'Зенитный прицеп большой дальности, способный поражать воздушные цели, обнаруженные ближайшими радарными машинами',
    'Capable of tracking multiple aerial units at ranges of up to 40km':
        'Способен сопровождать несколько воздушных целей на дальности до 40 км',
    'structural element': 'конструктивный элемент',
}

# валидация текущего состояния
ls = [l for l in raw.split('\n') if not l.strip().startswith('//')]
clean = re.sub(r',\s*([}\]])', r'\1', '\n'.join(ls))
data = json.loads(clean, strict=False)
before = len(data)

lines = raw.split('\n')
# вставка в самый конец: перед последней строкой '}'
idx = raw.rfind('\n}')
assert idx > 0, "не найдена закрывающая скобка"
head, tail = raw[:idx], raw[idx:]
if not head.rstrip().endswith(','):
    head = head.rstrip() + ','

new_entries = []
for k, v in add.items():
    if k in data:
        print("  уже есть:", repr(k[:50]))
        continue
    new_entries.append('    ' + json.dumps(k, ensure_ascii=False) + ': ' + json.dumps(v, ensure_ascii=False))
if new_entries:
    raw = head + '\n' + ',\n'.join(new_entries) + tail

# финальная валидация
ls = [l for l in raw.split('\n') if not l.strip().startswith('//')]
clean = re.sub(r',\s*([}\]])', r'\1', '\n'.join(ls))
data2 = json.loads(clean, strict=False)
print(f"записей: {before} -> {len(data2)}")
assert len(data2) == before + len(new_entries), "счётчик не сошёлся"

io.open(p, 'w', encoding='utf-8', newline='').write(raw)
print("ФАЙЛ СОХРАНЁН")
# контроль названий
for n in ['Infantry Squad', 'ECM Pod', 'Radar Jamming Pod', 'IRM-S2', 'RADOME']:
    print("  ", repr(n), "=>", repr(data2[n]))
