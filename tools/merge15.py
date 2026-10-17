# -*- coding: utf-8 -*-
"""Вливает переводы раунда 15 в ru.json."""
import io, re, sys, json, shutil, datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
p = base + r"\ru.json"
tmp = r"C:\Users\user\AppData\Local\Temp\lp_build"

def parse_text(raw):
    return json.loads(re.sub(r",\s*([}\]])", r"\1",
                             "\n".join(l for l in raw.split("\n") if not l.strip().startswith("//"))), strict=False)

raw = io.open(p, encoding="utf-8-sig").read()
ru = parse_text(raw)
before = len(ru)

idx = json.load(io.open(tmp + r"\r15_index.json", encoding="utf-8"))
tr = {}
for fn in ("tr15_prose.json", "tr15_labels.json"):
    d = json.load(io.open(tmp + "\\" + fn, encoding="utf-8"))
    for k, v in d.items():
        if k in tr:
            print("дубль id:", k)
        tr[k] = v
print("нет перевода для id:", [k for k in idx if k not in tr][:20])

pairs, problems = {}, []
for k, meta in idx.items():
    en, kind = meta["en"], meta["kind"]
    if k not in tr:
        continue
    ru_v = tr[k].strip()
    key = en.strip()
    if not ru_v or ru_v == key or not re.search(r"[А-Яа-яЁё]", ru_v):
        problems.append((k, kind, en[:60], ru_v[:60]))
        continue
    if re.findall(r"<[^>]+>", key) != re.findall(r"<[^>]+>", ru_v):
        problems.append((k, kind, "ТЕГИ", en[:50], ru_v[:50]))
        continue
    pairs[key] = ru_v

print("проблемных:", len(problems))
for pr in problems[:15]:
    print("   ", pr)
new = {k: v for k, v in pairs.items() if k not in ru}
print("к добавлению:", len(new), "| уже было:", len(pairs) - len(new))

if new:
    idx2 = raw.rfind("\n}")
    head, tail = raw[:idx2], raw[idx2:]
    if not head.rstrip().endswith(","):
        head = head.rstrip() + ","
    lines = []
    for k, v in new.items():
        lines.append("    " + json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False))
    text = head.rstrip() + "\n" + ",\n".join(lines) + "\n" + tail.lstrip("\n")
    try:
        ru2 = parse_text(text)
        assert len(ru2) == before + len(new), (len(ru2), before, len(new))
        for k, v in new.items():
            assert ru2[k] == v, k
    except Exception as e:
        print("ОШИБКА, файл не изменён:", e)
        sys.exit(1)
    backup = base + r"\ru.backup_" + datetime.datetime.now().strftime("%H%M%S") + ".json"
    shutil.copy2(p, backup)
    io.open(p, "w", encoding="utf-8", newline="").write(text)
    shutil.copy2(p, r"C:\Users\user\Documents\NuclearOption_Rus\ru.json")
    shutil.copy2(p, r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\config\LocalizationPatch\ru.json")
    print(f"записей: {before} -> {len(ru2)} | бэкап: {backup}")
