# -*- coding: utf-8 -*-
"""Раунд 13: подписи задач (label) для шаблона «подпись + число/единица» в плагине."""
import io, re, sys, json, shutil, datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
p = base + r"\ru.json"

PAIRS = [
    ("Return To Base", "Возврат на базу"),
    ("Search For Convoy", "Поиск конвоя"),
    ("Break Blockade", "Прорыв блокады"),
    ("Defend Island", "Оборона острова"),
    ("Destroy Vehicles", "Уничтожение техники"),
    ("Detected units", "Обнаружено единиц"),
    ("Repaired unit", "Отремонтировано единиц"),
    ("Take Off", "Взлёт"),
    ("Taxi", "Руление"),
    ("Taxi to Runway", "Руление к ВПП"),
    ("Taxi to Catapult", "Руление к катапульте"),
    ("Cleared for landing on Runway", "Разрешение на посадку, ВПП"),
    ("Cleared to taxi to Runway", "Разрешение на руление, ВПП"),
    ("Successful Sortie +", "Успешный вылет +"),
]


def parse_json(path):
    raw = io.open(path, encoding="utf-8-sig").read()
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in raw.split("\n") if not l.strip().startswith("//"))), strict=False)


ru = parse_json(p)
before = len(ru)

norm = io.open(base + r"\untranslated.txt", encoding="utf-8", errors="replace").read().replace("\\n", "\n")

add, already, notfound = {}, [], []
for k, v in PAIRS:
    if k in ru:
        already.append(k)
    elif k not in norm:
        notfound.append(k)
    else:
        add[k] = v

print("новых:", len(add), "| уже были:", len(already), "| НЕ найдено в дампе:", len(notfound))
for k in notfound:
    print("   ОПЕЧАТКА?:", repr(k))

if add:
    backup = base + r"\ru.backup_" + datetime.datetime.now().strftime("%H%M%S") + ".json"
    shutil.copy2(p, backup)
    raw = io.open(p, encoding="utf-8-sig").read()
    idx = raw.rfind("\n}")
    head, tail = raw[:idx], raw[idx:]
    if not head.rstrip().endswith(","):
        head = head.rstrip() + ","
    lines = ["    " + json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False) for k, v in add.items()]
    io.open(p, "w", encoding="utf-8", newline="").write(head + "\n" + ",\n".join(lines) + tail)
    ru2 = parse_json(p)
    print(f"записей: {before} -> {len(ru2)}")
    for k, v in add.items():
        assert ru2[k] == v, k
    shutil.copy2(p, r"C:\Users\user\Documents\NuclearOption_Rus\ru.json")
    shutil.copy2(p, r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\config\LocalizationPatch\ru.json")
    print("копии обновлены; бэкап:", backup)
