# -*- coding: utf-8 -*-
"""Добавляет в ru.json переводы 309 описаний/подсказок/тултипов (по индексам todo.json)."""
import io, re, sys, json, shutil, datetime, os

sys.stdout.reconfigure(encoding="utf-8")
T = r"C:\Users\user\AppData\Local\Temp\lp_build"
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
p = base + r"\ru.json"

items = json.loads(io.open(T + r"\todo.json", encoding="utf-8").read())
tr = {}
for part in sorted(f for f in os.listdir(T) if re.fullmatch(r"tr0\d\.json", f)):
    d = json.loads(io.open(os.path.join(T, part), encoding="utf-8").read())
    for k, v in d.items():
        if k in tr:
            raise SystemExit("дубль индекса " + k)
        tr[k] = v
print("переводов в файлах:", len(tr), "| строк в todo:", len(items))

missing = [it["i"] for it in items if str(it["i"]) not in tr]
extra = [k for k in tr if not (1 <= int(k) <= len(items))]
if missing or extra:
    raise SystemExit(f"неполно: нет {missing}, лишние {extra}")

# проверка на латиницу внутри кириллических слов (частый промах раскладки)
bad = []
for it in items:
    v = tr[str(it["i"])]
    for m in re.finditer(r"[А-Яа-яЁё]+[A-Za-z]+[А-Яа-яЁё]*|[A-Za-z]+[А-Яа-яЁё]+", v):
        bad.append((it["i"], m.group(0), v[:60]))
if bad:
    print("ВНИМАНИЕ, смешанные слова:")
    for i, w, ctx in bad:
        print("  ", i, w, "|", ctx)

raw = io.open(p, encoding="utf-8-sig").read()
if not raw.lstrip().startswith("{"):
    raise SystemExit("неожиданный формат ru.json")
shutil.copy2(p, base + r"\ru.backup_" + datetime.datetime.now().strftime("%H%M%S") + ".json")

def parse(txt):
    ls = [l for l in txt.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse(raw)
before = len(ru)

pairs = []
for it in items:
    en = it["en"]
    if en in ru:
        continue
    pairs.append((en, tr[str(it["i"])]))
print("к добавлению:", len(pairs))

if pairs:
    idx = raw.rfind("\n}")
    head, tail = raw[:idx], raw[idx:]
    if not head.rstrip().endswith(","):
        head = head.rstrip() + ","
    lines = ["    " + json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False) for k, v in pairs]
    raw = head + "\n" + ",\n".join(lines) + tail
    io.open(p, "w", encoding="utf-8", newline="").write(raw)

ru2 = parse(io.open(p, encoding="utf-8-sig").read())
print(f"записей: {before} -> {len(ru2)}")
for it in items:
    assert ru2[it["en"]] == tr[str(it["i"])], it["i"]
print("все новые записи на месте, JSON валиден")

shutil.copy2(p, r"C:\Users\user\Documents\NuclearOption_Rus\ru.json")
shutil.copy2(p, r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\config\LocalizationPatch\ru.json")
print("копии обновлены: Documents\\NuclearOption_Rus и BepInEx\\config\\LocalizationPatch")
