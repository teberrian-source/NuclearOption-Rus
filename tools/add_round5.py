# -*- coding: utf-8 -*-
"""Добавляет подсказки из модов (экспорт 20:16)."""
import json, re, io, sys, shutil, datetime

base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
sys.stdout.reconfigure(encoding="utf-8")
p = base + r"\ru.json"

NEW = {
    "Bombs generally have much heavier casings than missiles, and as such they are more resistant to anti-air lasers.":
        "Корпуса бомб обычно значительно тяжелее ракетных, поэтому они лучше противостоят лазерам ПВО.",
    "Vehicles deployed from an aircraft's cargo bay at altitude can land safely by parachute.":
        "Техника, сброшенная из грузового отсека самолёта на высоте, может безопасно приземлиться на парашюте.",
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
        skipped.append(k[:60])
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
print("JSON валиден")

# обновляем безопасную копию
shutil.copy2(p, r"C:\Users\user\Documents\NuclearOption_Rus\ru.json")
print("копия обновлена: Documents\\NuclearOption_Rus\\ru.json")
