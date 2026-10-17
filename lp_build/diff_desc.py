# -*- coding: utf-8 -*-
"""Сравнивает описания из ассетов с ru.json — что ещё не переведено."""
import sys, json, io, re

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

raw = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

descs = []
for line in io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\asset_desc.jsonl", encoding="utf-8"):
    o = json.loads(line)
    t = o["text"]
    # пропускаем CSV-строки таблицы (Type;UnitName;Code;...)
    if t.count(";") > 3:
        continue
    descs.append(t)

missing = [t for t in descs if t not in ru]
print("описаний из ассетов:", len(descs), "| уже переведено:", len(descs) - len(missing), "| не переведено:", len(missing))
out = io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\missing_desc.jsonl", "w", encoding="utf-8")
for t in sorted(missing):
    out.write(json.dumps(t, ensure_ascii=False) + "\n")
out.close()
print()
for i, t in enumerate(sorted(missing), 1):
    print(f"{i:3}. {t}")
