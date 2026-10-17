# -*- coding: utf-8 -*-
"""Выравнивание счётчиков в заголовках подсказок: сохраняем исходную длину строки."""
import io, re, sys, json, shutil, datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
p = base + r"\ru.json"

def parse(raw):
    return json.loads(re.sub(r",\s*([}\]])", r"\1",
                             "\n".join(l for l in raw.split("\n") if not l.strip().startswith("//"))), strict=False)

raw = io.open(p, encoding="utf-8-sig").read()
ru = parse(raw)
pat = re.compile(r"^(?P<label>.+?)(?P<gap>\s{2,})(?P<cnt>\d+/\d+)$")

changes = []
lines = raw.split("\n")
out = []
used = set()
for line in lines:
    m = re.match(r'^(\s*)"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"(,?)\s*$', line)
    if not m:
        out.append(line)
        continue
    indent, key_e, val_e, comma = m.groups()
    key = json.loads('"' + key_e + '"', strict=False)
    val = json.loads('"' + val_e + '"', strict=False)
    mk = pat.match(key)
    if not mk or key in used:
        out.append(line)
        continue
    used.add(key)
    en_label, gap, cnt = mk.group("label"), mk.group("gap"), mk.group("cnt")
    mv = pat.match(val)
    ru_label = (mv.group("label") if mv else val.rstrip()).strip()
    new_gap = max(2, len(gap) - (len(ru_label) - len(en_label)))
    new_val = ru_label + " " * new_gap + cnt
    if new_val != val:
        changes.append((en_label, len(key), ru_label, len(new_val), new_gap))
    line = indent + json.dumps(key, ensure_ascii=False) + ": " + json.dumps(new_val, ensure_ascii=False) + comma
    out.append(line)

print("заголовков со сдвинутым счётчиком:", len(changes))
for c in changes:
    print("   ", c)

text = "\n".join(out)
ru2 = parse(text)
assert len(ru2) == len(ru)
backup = base + r"\ru.backup_" + datetime.datetime.now().strftime("%H%M%S") + ".json"
shutil.copy2(p, backup)
io.open(p, "w", encoding="utf-8", newline="").write(text)
shutil.copy2(p, r"C:\Users\user\Documents\NuclearOption_Rus\ru.json")
shutil.copy2(p, r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\config\LocalizationPatch\ru.json")
print("записей:", len(ru2), "| бэкап:", backup)
