# -*- coding: utf-8 -*-
"""Аудит: какие короткие строки (похожие на названия) у нас переведены на русский."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

def parse_json(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse_json(base + r"\ru.json")
CYR = re.compile(r"[А-Яа-яЁё]")

raw = io.open(base + r"\untranslated.txt", encoding="utf-8", errors="replace").read()
seen = set()
for m in re.finditer(r'^\s*"((?:[^"\\]|\\.)*)"\s*:\s*""\s*,?\s*$', raw, re.M):
    s = m.group(1).replace('\\"', '"')
    if "\n" in s or len(s) > 45:
        continue
    if not re.fullmatch(r"[A-Za-z0-9 .'\-/+%()\[\]x]+", s.strip()):
        continue
    seen.add(s.strip())

hits = [(k, ru[k]) for k in sorted(seen) if k in ru and CYR.search(ru[k])]
print("коротких строк-названий в дампе:", len(seen))
print("из них переведено нами:", len(hits))
for k, v in hits:
    print(f"  {k!r} -> {v!r}")

# дополнительно: любые ключи словаря <=32 символов с русским значением и латинским ключом из 1-3 слов
print("\n=== короткие ключи-названия в ru.json (латиница, 1-3 слова, есть перевод) ===")
c = 0
for k, v in ru.items():
    if not CYR.search(v) or CYR.search(k):
        continue
    if len(k) > 32 or not re.fullmatch(r"[A-Za-z0-9 .'\-/]+", k):
        continue
    if len(k.split()) > 3:
        continue
    c += 1
    print(f"  {k!r} -> {v!r}")
print("таких ключей:", c)
