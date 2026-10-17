# -*- coding: utf-8 -*-
"""Добавляет переводы из разбора экспорта 19:54: описания модового оружия, FS-3 Ternion,
пилоны/отсеки, уровни эскалации, названия фракций."""
import json, re, io, sys, shutil, datetime

base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
sys.stdout.reconfigure(encoding="utf-8")
p = base + r"\ru.json"

NEW = {
    # ---- подсказка (короткий вариант строки; длинный уже переведён) ----
    "The engine of your aircraft can be stopped and started mid-flight with a dedicated keybind or a radial menu action.":
        "Двигатель самолёта можно остановить и запустить в полёте отдельной клавишей или через радиальное меню.",

    # ---- описание модового оружия ----
    "A compact medium-range INS/OPT guidance cruise missile designed to give small aircraft standoff capability.":
        "Компактная крылатая ракета средней дальности с инерциально-оптической системой наведения, дающая лёгким самолётам возможность действовать вне зоны ПВО.",

    # ---- описание техники (FS-3 Ternion) ----
    "Conceived at the turn of the century, the FS-3 Ternion is a large, twin-engine multirole fighter. "
    "Initially developed for long-endurance patrols over the Pacific, it was later adapted to meet expanding "
    "operational demands. Despite lacking stealth characteristics, frequent upgrade packages have allowed the "
    "Ternion to continue serving as a reliable defender of the Heartland.":
        "Разработанный на рубеже веков, FS-3 Ternion — большой двухдвигательный многоцелевой истребитель. "
        "Изначально созданный для длительных патрулей над Тихим океаном, позже он был адаптирован под растущие "
        "оперативные задачи. Несмотря на отсутствие малозаметности, частые пакеты модернизации позволяют Ternion "
        "оставаться надёжным защитником Хартленда.",

    # ---- пилоны / отсеки ----
    "Front Fuselage Pylons": "Передние пилоны фюзеляжа",
    "Rear Fuselage Pylons": "Задние пилоны фюзеляжа",
    "Combined Weapon Bay": "Комбинированный оружейный отсек",

    # ---- уровень эскалации (в стиле «NON-NUCLEAR» -> «НЕЯДЕРНОЕ») ----
    "TACTICAL": "ТАКТИЧЕСКИЙ",

    # ---- названия фракций из модов/миссий ----
    "Primeva Alliance Liberation Army": "Армия освобождения Альянса Примева",
    "PRIMEVA ARMED LIBERATION ALLIANCE": "АЛЬЯНС ВООРУЖЁННОГО ОСВОБОЖДЕНИЯ ПРИМЕВА",
    "SOUTH BOSCALI GENERAL AVIATION": "АВИАЦИЯ ОБЩЕГО НАЗНАЧЕНИЯ ЮЖНОГО БОСКАЛИ",
}

backup = base + r"\ru.backup_" + datetime.datetime.now().strftime("%H%M%S") + ".json"
shutil.copy2(p, backup)
print("бэкап:", backup)

raw = io.open(p, encoding="utf-8-sig").read()
ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
data = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)
before = len(data)

idx = raw.rfind("\n}")
head, tail = raw[:idx], raw[idx:]
if not head.rstrip().endswith(","):
    head = head.rstrip() + ","

new_entries, skipped = [], []
for k, v in NEW.items():
    if k in data:
        skipped.append(k[:70])
        continue
    new_entries.append("    " + json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False))
if new_entries:
    raw = head + "\n" + ",\n".join(new_entries) + tail

ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
data2 = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)
io.open(p, "w", encoding="utf-8", newline="").write(raw)

print(f"записей: {before} -> {len(data2)} (+{len(new_entries)})")
if skipped:
    print("уже были:", skipped)
for k, v in NEW.items():
    assert data2[k] == v, k
print("все новые записи на месте, JSON валиден")
