# -*- coding: utf-8 -*-
"""Все полные подсказки из extracted_gamedata.txt -> проверка наличия в ru.json, отсутствующие в файл."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

def parse(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse(base + r"\ru.json")
lines = io.open(base + r"\extracted_gamedata.txt", encoding="utf-8", errors="replace").read().split("\n")

hints = []
for l in lines:
    s = l.strip()
    m = re.match(r'^Did you know\?;(.+)$', s)
    if m:
        hints.append(m.group(1).strip())

# плюс подсказки, которые начинаются с «Did you know?» внутри одной длинной строки CSV
for l in lines:
    if "Did you know?;" in l and l.strip().count("Did you know?;") > 1:
        for part in l.split("Did you know?;")[1:]:
            parts = re.split(r"(?<=[.!?])\s(?=[A-Z][a-z])", part.strip())
            hints.extend([p for p in parts if len(p) > 25])

uniq = sorted(set(hints))
missing = [h for h in uniq if h not in ru]
print("подсказок всего:", len(uniq), "| нет в ru.json:", len(missing))
for h in missing:
    print("  MISSING:", json.dumps(h[:120], ensure_ascii=False))

with io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\hints_missing.txt", "w", encoding="utf-8") as f:
    for h in missing:
        f.write(h + "\n")
if missing:
    print("файл: hints_missing.txt")
