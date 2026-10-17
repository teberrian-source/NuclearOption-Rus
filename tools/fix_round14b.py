# -*- coding: utf-8 -*-
"""Правка неточных переводов (ловушки). Пишем во временный файл, проверяем, затем заменяем."""
import io, re, sys, json, shutil, datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
p = base + r"\ru.json"

def parse_text(raw):
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in raw.split("\n") if not l.strip().startswith("//"))), strict=False)

raw = io.open(p, encoding="utf-8-sig").read()
ru = parse_text(raw)
before = len(ru)

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
    idx = raw.rfind("\n}")
    head, tail = raw[:idx].rstrip(), raw[idx:]
    lines = ["    " + json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False) for k, v in ru.items()]
    text = head + ",\n" + ",\n".join(lines) + "\n" + tail.lstrip("\n")
    try:
        ru2 = parse_text(text)
        assert len(ru2) == before, (len(ru2), before)
        for k, v in fixes.items():
            assert ru2[k] == v
    except Exception as e:
        print("ОШИБКА записи, файл не менялся:", e)
        sys.exit(1)
    backup = base + r"\ru.backup_" + datetime.datetime.now().strftime("%H%M%S") + ".json"
    shutil.copy2(p, backup)
    io.open(p, "w", encoding="utf-8", newline="").write(text)
    print("записей:", before, "| исправлено:", changed)
    shutil.copy2(p, r"C:\Users\user\Documents\NuclearOption_Rus\ru.json")
    shutil.copy2(p, r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\config\LocalizationPatch\ru.json")
    print("копии обновлены; бэкап:", backup)
else:
    print("нечего исправлять")
