# -*- coding: utf-8 -*-
"""Показывает строки из экспорта, которых НЕТ в ru.json (всё, что не переведено)."""
import io, os, re, sys, json, datetime

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
raw_un = open(base + r"\untranslated.txt", "rb").read().decode("utf-8", "replace")
raw_ru = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ls = [l for l in raw_ru.split("\n") if not l.strip().startswith("//")]
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

# ключи экспорта: собираем с учётом многострочных записей (CR/LF внутри ключа)
keys = []
for m in re.finditer(r'"((?:[^"\\]|\\.)*)": ""', raw_un.replace("\r", "\n") + " ", re.S):
    try:
        keys.append(json.loads('"' + m.group(1) + '"'))
    except Exception:
        pass

missing = [k for k in keys if k not in ru]
print(f"экспорт: {len(keys)}  |  не найдено в ru.json: {len(missing)}")

CYR = re.compile(r"[А-Яа-яЁё]")
junk = re.compile(r"^(Time |Score |\d|R: |AP: |HE: |C: |ЭПР|ALT|SPD|FORM|FUEL|HULL|x \d|— CR|Pass: |RANK |\$|0,|-0,|G[a-j]\d{2}|H[a-j]\d{2}|I[a-j]\d{2,3}|J[a-j]\d{2,3})")
real = [k for k in missing if len(k) >= 25 and not junk.match(k) and not re.match(r"^[A-Za-z0-9 /\-\.'\(\)]+$", k)]
print(f"\nосмысленных длинных: {len(real)}")
for k in real:
    print("-", json.dumps(k, ensure_ascii=False)[:220])
