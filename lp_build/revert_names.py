# -*- coding: utf-8 -*-
"""Возврат названий предметов/техники на английский: удаляем указанные ключи из ru.json."""
import io, re, sys, json, shutil, datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
p = base + r"\ru.json"

KEYS = [
    "Ammo box",
    "Ammo Box",
    "Cursor Class LFD",
    "Argus Class Frigate",
    "4xS1 Turret",
    "MSV LADS",
    "MSV MRAP",
]

raw = io.open(p, encoding="utf-8-sig").read()
out, removed = [], []
for l in raw.split("\n"):
    m = re.match(r'\s*"((?:[^"\\]|\\.)*)"\s*:', l)
    if m and m.group(1).replace('\\"', '"') in KEYS:
        removed.append(l.strip())
        continue
    out.append(l)
print("удалено строк:", len(removed))
for r in removed:
    print("  ", r[:120])

new = "\n".join(out)
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in new.split("\n") if not l.strip().startswith("//"))), strict=False)
for k in KEYS:
    assert k not in ru, f"ключ {k!r} остался!"
print("всего записей:", len(ru))

backup = base + r"\ru.backup_" + datetime.datetime.now().strftime("%H%M%S") + ".json"
shutil.copy2(p, backup)
io.open(p, "w", encoding="utf-8", newline="").write(new)
ru2 = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in io.open(p, encoding="utf-8-sig").read().split("\n") if not l.strip().startswith("//"))), strict=False)
print("после записи записей:", len(ru2))
shutil.copy2(p, r"C:\Users\user\Documents\NuclearOption_Rus\ru.json")
shutil.copy2(p, r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\config\LocalizationPatch\ru.json")
print("копии обновлены; бэкап:", backup)
