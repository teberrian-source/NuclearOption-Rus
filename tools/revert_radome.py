# -*- coding: utf-8 -*-
"""Возврат названия оружия "Radome" на английский: убираем ключ из ru.json."""
import io, re, sys, json, shutil, datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
p = base + r"\ru.json"

raw = io.open(p, encoding="utf-8-sig").read()
lines = raw.split("\n")
out, removed = [], []
for l in lines:
    key = None
    m = re.match(r'\s*"((?:[^"\\]|\\.)*)"\s*:\s*', l)
    if m:
        key = m.group(1).replace('\\"', '"')
    if key == "Radome":
        removed.append(l.strip())
        continue
    out.append(l)
print("удалено строк:", len(removed))
for r in removed:
    print("  ", r[:120])

# проверяем, что в словаре больше нет "Radome"
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in "\n".join(out).split("\n") if not l.strip().startswith("//"))), strict=False)
assert "Radome" not in ru, "ключ Radome остался!"
print("всего записей:", len(ru))

backup = base + r"\ru.backup_" + datetime.datetime.now().strftime("%H%M%S") + ".json"
shutil.copy2(p, backup)
io.open(p, "w", encoding="utf-8", newline="").write("\n".join(out))
ru2 = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in io.open(p, encoding="utf-8-sig").read().split("\n") if not l.strip().startswith("//"))), strict=False)
print("после записи записей:", len(ru2), "| Radome в словаре:", "Radome" in ru2)
shutil.copy2(p, r"C:\Users\user\Documents\NuclearOption_Rus\ru.json")
shutil.copy2(p, r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\config\LocalizationPatch\ru.json")
print("копии обновлены; бэкап:", backup)
