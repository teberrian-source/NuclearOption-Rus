# -*- coding: utf-8 -*-
"""Поиск в дампе строк «подпись + число/единица» (кандидаты для шаблона)."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
raw = io.open(base + r"\untranslated.txt", encoding="utf-8", errors="replace").read()
norm = raw.replace("\\n", "\n")

value_re = re.compile(r"^(?P<label>.+?)\s(?P<value>[+\-]?[\d][\d.,]*(?:\s?(?:km|m|nm|kt|ft|s|min))?)$")
labels = {}
for line in norm.split("\n"):
    s = line.strip()
    if s.startswith('"'):
        s = s[1:]
    s = re.sub(r'"\s*:\s*""\s*,?$', "", s).strip()
    if not s:
        continue
    m = value_re.match(s)
    if m:
        labels.setdefault(m.group("label"), set()).add(m.group("value"))

ru_raw = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in ru_raw.split("\n") if not l.strip().startswith("//"))), strict=False)

print("кандидатов-подписей:", len(labels))
for k in sorted(labels):
    mark = "ЕСТЬ В СЛОВАРЕ" if k in ru else "нет в словаре"
    print(f"  {mark:15} | {k!r} -> {sorted(labels[k])[:4]}")
