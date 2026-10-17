# -*- coding: utf-8 -*-
"""Раунд 10: остатки UI из untranslated.txt (лобби, редактор миссий, HUD-сокращения)."""
import io, re, sys, json, shutil, datetime

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
p = base + r"\ru.json"

pairs = [
    ("Choose a Mission", "Выбор миссии"),
    ("Mission Title", "Название миссии"),
    ("In-game", "В игре"),
    ("Online", "В сети"),
    ("Offline", "Не в сети"),
    ("Creating Lobby...", "Создание лобби…"),
    ("SPD", "СКР"),
    ("MACH", "МАХ"),
    ("ROT", "РОТ"),
    ("YAW", "РЫСК"),
    ("A-A", "В-В"),
    ("A-G", "В-З"),
    ("<i>password</i>", "<i>пароль</i>"),
    ("<i>no password</i>", "<i>без пароля</i>"),
    ("<color=#FF0><font=\"MaterialSymbolsSharp\">\ue002</font></color> <i>no password</i>",
     "<color=#FF0><font=\"MaterialSymbolsSharp\">\ue002</font></color> <i>без пароля</i>"),
    ("<NOT LOADED>", "<НЕ ЗАГРУЖЕНО>"),
    ("Player A killed Player B", "Игрок A убил игрока B"),
]

raw = io.open(p, encoding="utf-8-sig").read()
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in raw.split("\n") if not l.strip().startswith("//"))), strict=False)
before = len(ru)
backup = base + r"\ru.backup_" + datetime.datetime.now().strftime("%H%M%S") + ".json"
shutil.copy2(p, backup)

new = [(k, v) for k, v in pairs if k not in ru]
if new:
    idx = raw.rfind("\n}")
    head, tail = raw[:idx], raw[idx:]
    if not head.rstrip().endswith(","):
        head = head.rstrip() + ","
    lines = ["    " + json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False) for k, v in new]
    raw = head + "\n" + ",\n".join(lines) + tail
io.open(p, "w", encoding="utf-8", newline="").write(raw)

ru2 = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in io.open(p, encoding="utf-8-sig").read().split("\n") if not l.strip().startswith("//"))), strict=False)
print(f"записей: {before} -> {len(ru2)} (+{len(new)})")
for k, v in pairs:
    assert ru2[k] == v, (k, ru2.get(k))
print("JSON валиден, все записи на месте")
shutil.copy2(p, r"C:\Users\user\Documents\NuclearOption_Rus\ru.json")
shutil.copy2(p, r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\config\LocalizationPatch\ru.json")
print("копии обновлены; бэкап:", backup)
