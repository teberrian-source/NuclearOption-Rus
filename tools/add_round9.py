# -*- coding: utf-8 -*-
"""Раунд 9: подписи слотов/хардпоинтов модовых юнитов (KAR, Aryx, Bote, MC260)."""
import io, re, sys, json, shutil, datetime

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
p = base + r"\ru.json"

pairs = [
    # KAR (наземная техника)
    ("Ammo Box", "Ящик боеприпасов"),
    ("Ammo box", "Ящик боеприпасов"),
    ("Cargo 2x", "Груз 2x"),
    ("cargo", "Груз"),
    ("cargo 2x", "Груз 2x"),
    ("Launchers", "Пусковые установки"),
    ("Point Defence", "Точечная оборона"),
    ("Point Defense", "Точечная оборона"),
    ("Roof Mount", "Крышная установка"),
    ("roof mount", "Крышная установка"),
    ("roof turret", "Крышная турель"),
    ("The Device", "Устройство"),
    ("Truck bed", "Кузов"),
    ("Turret", "Турель"),
    ("Vehicle Cargo", "Груз техники"),
    ("coax", "Соосное"),
    ("subturret", "Доп. турель"),
    ("subturret (H)", "Доп. турель (H)"),
    ("subturrets", "Доп. турели"),
    ("tow hook", "Буксирный крюк"),
    ("turret mount", "Турельная установка"),
    # Aryx (авиация) и Bote (корабли)
    ("Bomb Bay (2x)", "Бомбовый отсек (2x)"),
    ("Gun Mount", "Пушечная установка"),
    ("Inner L Bay", "Внутренний левый отсек"),
    ("Inner R Bay", "Внутренний правый отсек"),
    ("Internal Gun", "Встроенная пушка"),
    ("Mission Bay", "Отсек полезной нагрузки"),
    ("Outer L Bay", "Наружный левый отсек"),
    ("Outer R Bay", "Наружный правый отсек"),
    ("Outer Weapon Bays", "Наружные оружейные отсеки"),
    ("Radome", "Обтекатель РЛС"),
    ("Side Mount", "Бортовая установка"),
    ("TGP", "Контейнер целеуказания"),
    ("Tailhook", "Посадочный гак"),
    ("Top Mount", "Верхняя установка"),
    ("VLS", "УВП"),
    ("Weapon Bays", "Оружейные отсеки"),
]

raw = io.open(p, encoding="utf-8-sig").read()
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in raw.split("\n") if not l.strip().startswith("//"))), strict=False)
before = len(ru)
backup = base + r"\ru.backup_" + datetime.datetime.now().strftime("%H%M%S") + ".json"
shutil.copy2(p, backup)

# 1) исправляем незапереведённую "Internal Cannon"
raw2, n_fix = re.subn(r'"Internal Cannon":\s*"Internal Cannon"', '"Internal Cannon": "Встроенная пушка"', raw)

# 2) добавляем новые пары
new = [(k, v) for k, v in pairs if k not in ru]
if new:
    idx = raw2.rfind("\n}")
    head, tail = raw2[:idx], raw2[idx:]
    if not head.rstrip().endswith(","):
        head = head.rstrip() + ","
    lines = ["    " + json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False) for k, v in new]
    raw2 = head + "\n" + ",\n".join(lines) + tail
io.open(p, "w", encoding="utf-8", newline="").write(raw2)

ru2 = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in io.open(p, encoding="utf-8-sig").read().split("\n") if not l.strip().startswith("//"))), strict=False)
print(f"исправлено Internal Cannon: {n_fix}; записей: {before} -> {len(ru2)} (+{len(new)})")
for k, v in pairs:
    assert ru2[k] == v, (k, ru2.get(k))
assert ru2["Internal Cannon"] == "Встроенная пушка"
print("JSON валиден, все записи на месте")
shutil.copy2(p, r"C:\Users\user\Documents\NuclearOption_Rus\ru.json")
shutil.copy2(p, r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\config\LocalizationPatch\ru.json")
print("копии обновлены; бэкап:", backup)
