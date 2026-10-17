# -*- coding: utf-8 -*-
"""Чиним ru.json: восстановление из бэкапа + точечная замена 3 значений (без перезаписи всего файла)."""
import io, re, sys, json, shutil, datetime, collections

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
p = base + r"\ru.json"

# 1. восстановление из бэкапа (до испорченной записи)
src = base + r"\ru.backup_235746.json"
shutil.copy2(src, p)
raw = io.open(p, encoding="utf-8-sig").read()
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in raw.split("\n") if not l.strip().startswith("//"))), strict=False)
print("восстановлено записей:", len(ru), "| размер:", len(raw))

# 2. дубликаты ключей в тексте?
dups = collections.Counter()
for m in re.finditer(r'^\s*"((?:[^"\\]|\\.)*)"\s*:', raw, re.M):
    dups[m.group(1)] += 1
multi = {k: c for k, c in dups.items() if c > 1}
print("ключей, встречающихся в тексте >1 раза:", len(multi))
for k, c in list(multi.items())[:10]:
    print("   ", c, repr(k[:60]))

# 3. точечные замены значений
repl = {
    '"Flares rearmed by": ': "Ловушки пополнены",
    '"Flares rearmed by ": ': "Ловушки пополнены",
    '"Popping Flares": ': "Отстрел ловушек",
}
text = raw
changed = 0
for key, newval in repl.items():
    pat = re.compile(r"^(\s*" + re.escape(key) + r')((?:"(?:[^"\\]|\\.)*")|"")?(,?)\s*$', re.M)
    m = pat.search(text)
    if not m:
        print("не найден в тексте:", key)
        continue
    old = m.group(0)
    new = m.group(1) + json.dumps(newval, ensure_ascii=False) + m.group(3)
    if old == new:
        continue
    text = text[:m.start()] + new + text[m.end():]
    changed += 1
    print("заменено:", key, "->", newval)

if changed:
    ru2 = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in text.split("\n") if not l.strip().startswith("//"))), strict=False)
    assert len(ru2) == len(ru)
    for k, v in (("Flares rearmed by", "Ловушки пополнены"), ("Flares rearmed by ", "Ловушки пополнены"), ("Popping Flares", "Отстрел ловушек")):
        assert ru2[k] == v, k
    backup = base + r"\ru.backup_" + datetime.datetime.now().strftime("%H%M%S") + ".json"
    shutil.copy2(p, backup)
    io.open(p, "w", encoding="utf-8", newline="").write(text)
    shutil.copy2(p, r"C:\Users\user\Documents\NuclearOption_Rus\ru.json")
    shutil.copy2(p, r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\config\LocalizationPatch\ru.json")
    print("записей:", len(ru2), "| размер:", len(text), "| бэкап:", backup)
else:
    print("изменений нет")
