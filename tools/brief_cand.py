# -*- coding: utf-8 -*-
"""Разбор дампа на «записи» (с учётом многострочных ключей) + отбор брифингов/описаний."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
text = io.open(base + r"\untranslated.txt", encoding="utf-8", errors="replace").read()
lines = text.split("\n")

entries = []
cur = None
for line in lines:
    if cur is None:
        s = line.lstrip()
        if s.startswith('"'):
            cur = s[1:]
            m = re.search(r'"\s*:\s*""\s*,?\s*$', cur)
            if m:
                entries.append(cur[:m.start()])
                cur = None
    else:
        m = re.search(r'"\s*:\s*""\s*,?\s*$', line)
        if m:
            entries.append(cur + "\n" + line[:m.start()])
            cur = None
        else:
            cur += "\n" + line

# декодируем экранирование
def unesc(s):
    return s.replace("\\n", "\n").replace("\\'", "'").replace('\\"', '"').replace("\\\\", "\\")

entries = sorted({unesc(e) for e in entries})

ru_raw = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in ru_raw.split("\n") if not l.strip().startswith("//"))), strict=False)

print("записей в дампе:", len(entries))
cands = []
for e in entries:
    e = e.strip()
    if not e or e in ru:
        continue
    if "<color=" in e or e.startswith("•"):
        continue
    words = re.findall(r"[A-Za-z']{2,}", e)
    if len(words) < 6:
        continue
    cands.append(e)
print("кандидатов (>=6 слов, нет в словаре):", len(cands))
with io.open("brief_cand.txt", "w", encoding="utf-8", newline="\n") as f:
    for c in cands:
        f.write(c + "\n" + "=" * 8 + "\n")
print("записано в brief_cand.txt")
