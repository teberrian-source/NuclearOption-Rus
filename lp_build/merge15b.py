# -*- coding: utf-8 -*-
"""Раунд 15б: имена целей/точек базовых миссий -> ru.json + белый список подписей в Plugin.cs."""
import io, re, sys, json, shutil, datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base_dir = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
p = base_dir + r"\ru.json"
tmp = r"C:\Users\user\AppData\Local\Temp\lp_build"

TR = {
    "Assist Attack on Airfield": "Поддержать атаку на аэродром",
    "Capture Airport": "Захватить аэропорт",
    "Capture Depot": "Захватить склад",
    "Capture South Boscali": "Захватить южный Boscali",
    "Capture Supply Point": "Захватить пункт снабжения",
    "Come to a stop": "Полностью остановиться",
    "Defend Bridge": "Оборонять мост",
    "Defend Maris Airport": "Оборонять Maris Airport",
    "Defend bridge": "Оборонять мост",
    "Deploy Team One": "Высадить группу 1",
    "Deploy Team Two": "Высадить группу 2",
    "Destroy AAA": "Уничтожить ПВО",
    "Destroy Airfield": "Уничтожить аэродром",
    "Destroy Depot": "Уничтожить склад",
    "Destroy Fuel Stores": "Уничтожить запасы топлива",
    "Destroy Launchers": "Уничтожить пусковые установки",
    "Destroy Neutral Shard 1": "Уничтожить нейтральный Shard 1",
    "Destroy Neutral Shard 2": "Уничтожить нейтральный Shard 2",
    "Destroy Radar": "Уничтожить РЛС",
    "Destroy Radar Truck": "Уничтожить РЛС на шасси",
    "Destroy Shelter": "Уничтожить укрытие",
    "Destroy Supply Point": "Уничтожить пункт снабжения",
    "Destroy Target": "Уничтожить цель",
    "Destroy Targets": "Уничтожить цели",
    "Destroy Trucks": "Уничтожить грузовики",
    "Destroy Vehicle Depots": "Уничтожить склады техники",
    "Eliminate Depot": "Ликвидировать склад",
    "Enemy Aircraft": "Авиация противника",
    "Enemy Formation": "Группа противника",
    "Ingress Via Mountains": "Вход в район через горы",
    "Intercept Bomber": "Перехватить бомбардировщик",
    "Intercept Cruise Missiles": "Перехватить крылатые ракеты",
    "Land at Naval Base": "Сесть на военно-морской базе",
    "Landing Site 1": "Площадка посадки 1",
    "Landing Site 2": "Площадка посадки 2",
    "Leave Combat Area": "Покинуть зону боя",
    "Locate Enemy Carrier": "Обнаружить авианосец противника",
    "Navigate Storm": "Пройти через шторм",
    "Neutralize Airfield": "Подавить аэродром",
    "Neutralize Artillery": "Подавить артиллерию",
    "Neutralize Inlet Base": "Подавить базу в заливе",
    "PALA Troops Retreat": "Войска PALA отступают",
    "Re-capture K92": "Отбить K92",
    "Rendezvous with ships": "Встретиться с кораблями",
    "Resupply Point": "Точка снабжения",
    "Return to Base": "Возврат на базу",
    "Reveal Base": "Раскрыть базу",
    "Shoot Down Commander": "Сбить командира",
    "Sink Enemy Carrier": "Потопить авианосец противника",
    "Spot Vehicles": "Обнаружить технику",
    "Take off": "Взлёт",
    "Touch Down": "Касание",
    "Upload Targets": "Передать координаты целей",
    "Use Airbakes": "Использовать воздушные тормоза",
    "West Coast Landing": "Посадка на западном побережье",
}

labels = [l for l in io.open(tmp + r"\r15b_labels.txt", encoding="utf-8").read().split("\n") if l.strip()]
missing = [k for k in TR if k not in labels]
print("нет в списке целей (проверь опечатки):", missing)

def parse_text(raw):
    return json.loads(re.sub(r",\s*([}\]])", r"\1",
                             "\n".join(l for l in raw.split("\n") if not l.strip().startswith("//"))), strict=False)

raw = io.open(p, encoding="utf-8-sig").read()
ru = parse_text(raw)
before = len(ru)
new = {k: v for k, v in TR.items() if k not in ru}
print("новых записей:", len(new))
if new:
    idx2 = raw.rfind("\n}")
    head, tail = raw[:idx2], raw[idx2:]
    if not head.rstrip().endswith(","):
        head = head.rstrip() + ","
    lines = ["    " + json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False) for k, v in new.items()]
    text = head.rstrip() + "\n" + ",\n".join(lines) + "\n" + tail.lstrip("\n")
    ru2 = parse_text(text)
    assert len(ru2) == before + len(new)
    for k, v in new.items():
        assert ru2[k] == v
    backup = base_dir + r"\ru.backup_" + datetime.datetime.now().strftime("%H%M%S") + ".json"
    shutil.copy2(p, backup)
    io.open(p, "w", encoding="utf-8", newline="").write(text)
    shutil.copy2(p, r"C:\Users\user\Documents\NuclearOption_Rus\ru.json")
    shutil.copy2(p, r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\config\LocalizationPatch\ru.json")
    print(f"ru.json: {before} -> {len(ru2)} | бэкап: {backup}")

# --- белый список подписей: перегенерируем (раунд 15 цели + новые) ---
idx = json.load(io.open(tmp + r"\r15_index.json", encoding="utf-8"))
HUD_UI = {
    "! DANGER - INCOMING MISSILE !", "MAIN ROTOR DAMAGE", "UPPER ROTOR FAILURE", "LOWER ROTOR FAILURE",
    "TAIL ROTOR FAIL", "L ENG FAIL", "R ENG FAIL", "VORTEX RING STATE", "REDUCE COLLECTIVE",
    "Next Camera", "Previous Camera", "Next Unit", "Previous Unit", "Select Unit Mode",
    "Rotate Unit Mode", "Translate Unit Mode", "Deploy Unit", "Deploy FOB", "Call Resupply",
    "Call Resupply - Player", "Objective Info", "Vote Kick Yes", "Vote Kick No", "Radar ECM",
}
base_keys = ["Return To Base", "Search For Convoy", "Break Blockade", "Defend Island",
             "Destroy Vehicles", "Detected units", "Repaired unit", "Take Off", "Taxi",
             "Taxi to Runway", "Cleared for landing on Runway", "Cleared to taxi to Runway",
             "Successful Sortie +"]
allk = base_keys + sorted({m["en"] for m in idx.values() if m["kind"] == "label" and m["en"] not in HUD_UI} | set(TR))
lines, cur = [], "\t\t"
for k in allk:
    item = json.dumps(k, ensure_ascii=False) + ", "
    if len(cur) + len(item) > 100:
        lines.append(cur.rstrip())
        cur = "\t\t"
    cur += item
lines.append(cur.rstrip().rstrip(","))
block = ("\tprivate static readonly HashSet<string> LabelWithValueKeys = new HashSet<string>\n\t{\n"
         + "\n".join(lines) + "\n\t};")
io.open(tmp + r"\label_keys.txt", "w", encoding="utf-8", newline="\n").write(block)
print("белый список:", len(allk), "подписей")

src = r"C:\Users\user\AppData\Local\Temp\lp_build\KoreanPatch\Plugin.cs"
raw_src = open(src, "rb").read()
bom = raw_src.startswith(b"\xef\xbb\xbf")
t = raw_src.decode("utf-8-sig").replace("\r\n", "\n")
m = re.search(r"\tprivate static readonly HashSet<string> LabelWithValueKeys = new HashSet<string>\n\t\{\n.*?\n\t\};", t, re.S)
if not m:
    print("!! блок не найден")
    sys.exit(1)
t = t[:m.start()] + block + t[m.end():]
shutil.copy2(src, src + ".bak_" + datetime.datetime.now().strftime("%H%M%S"))
open(src, "wb").write((b"\xef\xbb\xbf" if bom else b"") + t.replace("\n", "\r\n").encode("utf-8"))
print("Plugin.cs обновлён")
