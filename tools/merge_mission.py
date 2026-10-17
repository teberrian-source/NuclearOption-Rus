# -*- coding: utf-8 -*-
"""Вливает переводы миссий/подсказок в ru.json (ключ — оригинал, значение — перевод)."""
import io, re, sys, json, shutil, datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
p = base + r"\ru.json"
tmp = r"C:\Users\user\AppData\Local\Temp\lp_build"

def parse_json(path):
    raw = io.open(path, encoding="utf-8-sig").read()
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in raw.split("\n") if not l.strip().startswith("//"))), strict=False)

ru = parse_json(p)
before = len(ru)
idx = json.load(io.open(tmp + r"\todo_index.json", encoding="utf-8"))
tr = {}
for fn in ("tr_msgs.json", "tr_bodies.json", "tr_titles.json"):
    d = json.load(io.open(tmp + "\\" + fn, encoding="utf-8"))
    for k, v in d.items():
        if k in tr:
            print("дубль id:", k, "в", fn)
        tr[k] = v

missing_ids = [k for k in idx if k not in tr]
print("нет перевода для id:", missing_ids[:20], "…" if len(missing_ids) > 20 else "")

def norm_title(en, ru_v):
    """Заголовок: RU-текст + оригинальные пробелы + оригинальный счётчик."""
    m = re.search(r"^(.+?)(\s{2,})(\d+/\d+)$", en)
    if not m:
        return ru_v.strip()
    gap, counter = m.group(2), m.group(3)
    label = re.sub(r"\s{2,}\d+/\d+$", "", ru_v).strip()
    label = re.sub(r"\s*\d+/\d+$", "", label).strip()
    return label + gap + counter

pairs = {}
problems = []
for k, meta in idx.items():
    en, fld = meta["en"], meta["field"]
    if k not in tr:
        continue
    ru_v = tr[k]
    if not ru_v or ru_v.strip() == en.strip() or not re.search(r"[А-Яа-яЁё]", ru_v):
        problems.append((k, fld, "не переведено?", en[:60], ru_v[:60]))
        continue
    if fld == "title":
        ru_v = norm_title(en, ru_v)
    if fld in ("body", "Message", "message", "description"):
        tags_en = re.findall(r"<[^>]+>", en)
        tags_ru = re.findall(r"<[^>]+>", ru_v)
        if tags_en != tags_ru:
            problems.append((k, fld, "теги", tags_en[:5], tags_ru[:5]))
            continue
    pairs[en.strip()] = ru_v.strip()
    # вариант с \x0b -> \n (на случай, если игра заменяет вертикальную табуляцию)
    if "\x0b" in en:
        alt = en.replace("\x0b", "\n").strip()
        if alt and alt != en.strip():
            pairs[alt] = ru_v.strip()

pairs["Destroy FARP"] = "Уничтожить FARP"
pairs["Waypoint"] = "Точка маршрута"

print("проблемных записей:", len(problems))
for pr in problems[:20]:
    print("   ", pr)
print("к добавлению:", len(pairs), "| уже в словаре:", sum(1 for k in pairs if k in ru))

backup = base + r"\ru.backup_" + datetime.datetime.now().strftime("%H%M%S") + ".json"
shutil.copy2(p, backup)
raw = io.open(p, encoding="utf-8-sig").read()
idx2 = raw.rfind("\n}")
head, tail = raw[:idx2], raw[idx2:]
if not head.rstrip().endswith(","):
    head = head.rstrip() + ","
lines = []
added = 0
for k, v in pairs.items():
    if k in ru:
        if ru[k] != v:
            print("   отличается от словаря:", repr(k[:50]))
        continue
    lines.append("    " + json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False))
    added += 1
io.open(p, "w", encoding="utf-8", newline="").write(head + "\n" + ",\n".join(lines) + tail)
ru2 = parse_json(p)
print(f"записей: {before} -> {len(ru2)} (добавлено {added})")
for k, v in pairs.items():
    assert ru2[k] == v, k
shutil.copy2(p, r"C:\Users\user\Documents\NuclearOption_Rus\ru.json")
shutil.copy2(p, r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\config\LocalizationPatch\ru.json")
print("копии обновлены; бэкап:", backup)
