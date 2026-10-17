# -*- coding: utf-8 -*-
"""Ищет расхождения ключей ru.json с рантайм-строками: хвостовые пробелы и точные совпадения."""
import io, re, json, sys

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

def parse_json(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse_json(base + r"\ru.json")
print("ru.json записей:", len(ru))

# ключи с хвостовым/ведущим пробелом
ws = [k for k in ru if k != k.strip()]
print("ключей с крайними пробелами в ru.json:", len(ws))
for k in ws[:10]:
    print("   ", json.dumps(k, ensure_ascii=False)[:90])

# разбор дампа
raw = io.open(base + r"\extracted_strings.txt", encoding="utf-8", errors="replace").read()
raw = raw.split("// ========== RAW LONG STRINGS")[0]
entries = []
cur = "?"
for line in raw.split("\n"):
    s = line.strip()
    if s.startswith("//"):
        x = s[2:].strip()
        if x and "===" not in x:
            cur = x
        continue
    m = re.match(r'^"((?:[^"\\]|\\.)*)":\s*""', s)
    if not m:
        continue
    try:
        t = json.loads('"' + m.group(1) + '"')
    except Exception:
        continue
    entries.append((cur, t))
print("строк в дампе:", len(entries))

DESC = ("description", "HintTip.text")
eng = [e for e in entries if len(e[1]) > 40 and any(d in e[0] for d in DESC)]
missing = [(f, t) for f, t in eng if t not in ru]
strip_hit = [(f, t) for f, t in missing if t.strip() in ru]
print("англ. описаний/подсказок:", len(eng), "| нет перевода:", len(missing), "| из них совпадёт после strip():", len(strip_hit))
for f, t in strip_hit[:15]:
    print("   TRAIL", f, "|", json.dumps(t[-40:], ensure_ascii=False), "|", ru[t.strip()][:50])
print("--- примеры реально отсутствующих ---")
for f, t in missing[:20]:
    print("   MISS ", f, "|", t[:90])

# не переведено из рантайма
un = io.open(base + r"\untranslated.txt", encoding="utf-8", errors="replace").read().split("\n")
long_un = []
for line in un:
    m = re.match(r'^"((?:[^"\\]|\\.)*)":\s*"",?\s*$', line.strip())
    if not m:
        continue
    try:
        t = json.loads('"' + m.group(1) + '"')
    except Exception:
        continue
    if len(t) > 60:
        long_un.append(t)
print("длинных (>60) строк в untranslated.txt:", len(long_un))
print("   из них уже ЕСТЬ в ru.json точно:", sum(1 for t in long_un if t in ru))
print("   из них совпадут после strip():", sum(1 for t in long_un if t not in ru and t.strip() in ru))
for t in long_un[:15]:
    print("   UNSTRIPED-DIFF:", json.dumps(t[:60], ensure_ascii=False), "| in_ru:", t in ru, "| strip_in_ru:", t.strip() in ru)
