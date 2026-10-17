# -*- coding: utf-8 -*-
"""Правка неточных переводов (ловушки) + отчёт."""
import io, re, sys, json, shutil, datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
p = base + r"\ru.json"

def parse_json(path):
    raw = io.open(path, encoding="utf-8-sig").read()
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in raw.split("\n") if not l.strip().startswith("//"))), strict=False)

ru = parse_json(p)
fixes = {
    "Flares rearmed by": "Ловушки пополнены",
    "Flares rearmed by ": "Ловушки пополнены",
    "Popping Flares": "Отстрел ловушек",
}
changed = 0
for k, v in fixes.items():
    if k in ru and ru[k] != v:
        print(repr(k), ":", repr(ru[k]), "->", repr(v))
        ru[k] = v
        changed += 1

if changed:
    backup = base + r"\ru.backup_" + datetime.datetime.now().strftime("%H%M%S") + ".json"
    shutil.copy2(p, backup)
    raw = io.open(p, encoding="utf-8-sig").read()
    idx = raw.rfind("\n}")
    head, tail = raw[:idx], raw[idx:]
    lines = []
    for k, v in ru.items():
        lines.append("    " + json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False))
    io.open(p, "w", encoding="utf-8", newline="").write(head.rstrip().rstrip(",") + "\n" + ",\n".join(lines) + tail)
    ru2 = parse_json(p)
    print("записей:", len(ru2))
    assert len(ru2) == len(ru)
    shutil.copy2(p, r"C:\Users\user\Documents\NuclearOption_Rus\ru.json")
    shutil.copy2(p, r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\config\LocalizationPatch\ru.json")
    print("исправлено:", changed, "| бэкап:", backup)
else:
    print("нечего исправлять")
