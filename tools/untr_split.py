# -*- coding: utf-8 -*-
"""Разбор дампа untranslated.txt: сколько ключей, сколько уже в ru.json, что осталось."""
import io, json, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

def parse_json(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse_json(base + r"\ru.json")

raw = io.open(base + r"\untranslated.txt", encoding="utf-8", errors="replace").read()
keys = re.findall(r'^\s*"((?:[^"\\]|\\.)*)"\s*:\s*""\s*,?\s*$', raw, re.M)
keys = [k.encode("utf-8").decode("unicode_escape").encode("latin1", "ignore").decode("utf-8", "ignore") if "\\u" in k else k.replace('\\"', '"').replace("\\n", "\n") for k in keys]
uniq = sorted(set(keys))
print("строк в дампе:", len(keys), "| уникальных:", len(uniq))

notin = [k for k in uniq if k.strip() not in ru]
print("нет в ru.json:", len(notin))

def kind(t):
    t = t.strip()
    if re.fullmatch(r"[\W\d_]+", t):
        return "знаки/цифры"
    if re.fullmatch(r"[A-Za-z0-9 .'\-/()\[\]+%°:,#&$]{1,40}", t):
        return "короткое (имя/код)"
    if len(t) >= 60:
        return "длинный текст"
    return "среднее"

from collections import Counter
c = Counter(kind(k) for k in notin)
print("по категориям:", dict(c))

io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\untr_notin.json", "w", encoding="utf-8").write(
    json.dumps(notin, ensure_ascii=False, indent=1))

print("\n=== СРЕДНИЕ (10..60 символов) ===")
for t in notin:
    if kind(t) == "среднее":
        print("|", t.strip()[:120])
print("\n=== ДЛИННЫЕ (>=60) ===")
for t in notin:
    if kind(t) == "длинный текст":
        print("|", t.strip()[:200].replace("\n", "\\n"))
