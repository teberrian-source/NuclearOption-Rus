# -*- coding: utf-8 -*-
"""Раунд 11: дубликаты ключей без крайних пробелов.

Плагин делает original.Trim() перед поиском, поэтому ключи с ведущими/хвостовыми
пробелами никогда не срабатывают. Добавляем их trim-версии (исходные оставляем).
"""
import io, re, sys, json, shutil, datetime

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
p = base + r"\ru.json"

raw = io.open(p, encoding="utf-8-sig").read()
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in raw.split("\n") if not l.strip().startswith("//"))), strict=False)
before = len(ru)

add = {}
for k, v in ru.items():
    st = k.strip()
    if st and st != k and st not in ru:
        add[st] = v

print("ключей с крайними пробелами:", sum(1 for k in ru if k != k.strip()))
print("можно добавить trim-версий:", len(add))
for k in list(add)[:10]:
    print("   ", repr(k[:70]))

if add:
    backup = base + r"\ru.backup_" + datetime.datetime.now().strftime("%H%M%S") + ".json"
    shutil.copy2(p, backup)
    idx = raw.rfind("\n}")
    head, tail = raw[:idx], raw[idx:]
    if not head.rstrip().endswith(","):
        head = head.rstrip() + ","
    lines = ["    " + json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False) for k, v in add.items()]
    io.open(p, "w", encoding="utf-8", newline="").write(head + "\n" + ",\n".join(lines) + tail)
    ru2 = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in io.open(p, encoding="utf-8-sig").read().split("\n") if not l.strip().startswith("//"))), strict=False)
    print(f"записей: {before} -> {len(ru2)}")
    for k, v in add.items():
        assert ru2[k] == v
    shutil.copy2(p, r"C:\Users\user\Documents\NuclearOption_Rus\ru.json")
    shutil.copy2(p, r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\config\LocalizationPatch\ru.json")
    print("копии обновлены; бэкап:", backup)
