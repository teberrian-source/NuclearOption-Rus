# -*- coding: utf-8 -*-
"""Добавляет в ru.json переводы UI-строк из todo3.json (файл переводов tr10.json)."""
import io, re, sys, json, shutil, datetime, os

sys.stdout.reconfigure(encoding="utf-8")
T = r"C:\Users\user\AppData\Local\Temp\lp_build"
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
p = base + r"\ru.json"

items = json.loads(io.open(T + r"\todo3.json", encoding="utf-8").read())
tr = json.loads(io.open(T + r"\tr10.json", encoding="utf-8").read())
missing = [it["i"] for it in items if str(it["i"]) not in tr]
if missing:
    raise SystemExit("нет переводов для индексов: " + str(missing))

def parse(txt):
    ls = [l for l in txt.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

raw = io.open(p, encoding="utf-8-sig").read()
ru = parse(raw)
before = len(ru)
shutil.copy2(p, base + r"\ru.backup_" + datetime.datetime.now().strftime("%H%M%S") + ".json")

pairs = [(it["en"], tr[str(it["i"])]) for it in items if it["en"] not in ru]
if pairs:
    idx = raw.rfind("\n}")
    head, tail = raw[:idx], raw[idx:]
    if not head.rstrip().endswith(","):
        head = head.rstrip() + ","
    lines = ["    " + json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False) for k, v in pairs]
    io.open(p, "w", encoding="utf-8", newline="").write(head + "\n" + ",\n".join(lines) + tail)

ru2 = parse(io.open(p, encoding="utf-8-sig").read())
print(f"записей: {before} -> {len(ru2)} (+{len(pairs)})")
for it in items:
    assert ru2[it["en"]] == tr[str(it["i"])], it["i"]
print("JSON валиден, все записи на месте")
shutil.copy2(p, r"C:\Users\user\Documents\NuclearOption_Rus\ru.json")
shutil.copy2(p, r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\config\LocalizationPatch\ru.json")
print("копии обновлены")
