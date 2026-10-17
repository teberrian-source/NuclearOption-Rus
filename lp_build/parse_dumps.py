# -*- coding: utf-8 -*-
"""Собирает из дампов (extracted_*.txt) строки-описания, которых ещё нет в ru.json."""
import io, os, re, sys, json

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

# --- текущий словарь ---
raw = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)
print("ru.json:", len(ru))

CYR = re.compile(r"[А-Яа-яЁё]")

def sentence_like(s):
    """Похоже на человеческое описание, а не на код/имя."""
    if not (40 <= len(s) <= 900):
        return False
    if CYR.search(s):
        return False
    letters = sum(1 for c in s if c.isalpha())
    lower = sum(1 for c in s if c.islower())
    spaces = s.count(" ")
    if spaces < 5 or lower < 20:
        return False
    if letters * 100 // max(1, len(s)) < 60:
        return False
    words = re.findall(r"[A-Za-z]{2,}", s)
    if len(words) < 8:
        return False
    return True

cands = {}

# --- extracted_strings.txt: строки вида "текст": "",  + сырые блобы ---
p1 = base + r"\extracted_strings.txt"
raw1 = io.open(p1, encoding="utf-8", errors="replace").read()
raw1 = raw1.split("// ========== RAW LONG STRINGS")[0]
for m in re.finditer(r'"((?:[^"\\]|\\.)*)": ""', raw1):
    try:
        s = json.loads('"' + m.group(1) + '"')
    except Exception:
        continue
    if s not in ru and sentence_like(s):
        cands.setdefault(s, set()).add("strings")

# --- extracted_gamedata.txt: любые длинные английские строки ---
p2 = base + r"\extracted_gamedata.txt"
raw2 = io.open(p2, encoding="utf-8", errors="replace").read()
for line in raw2.split("\n"):
    s = line.strip()
    if s.startswith("//") or not s:
        continue
    for part in [s]:
        if part not in ru and sentence_like(part):
            cands.setdefault(part, set()).add("gamedata")

# --- untranslated.txt (свежий) ---
p3 = base + r"\untranslated.txt"
raw3 = io.open(p3, encoding="utf-8", errors="replace").read()
for m in re.finditer(r'"((?:[^"\\]|\\.)*)": ""', raw3):
    try:
        s = json.loads('"' + m.group(1) + '"')
    except Exception:
        continue
    if s not in ru and sentence_like(s):
        cands.setdefault(s, set()).add("untranslated")

print("кандидатов-описаний:", len(cands))
out = [r"C:\Users\user\AppData\Local\Temp\lp_build\desc_dump.txt"]
with io.open(out[0], "w", encoding="utf-8") as f:
    for i, (s, src) in enumerate(sorted(cands.items()), 1):
        f.write(f"### {i}. [{','.join(sorted(src))}] {len(s)} симв.\n{s}\n\n")
for i, (s, src) in enumerate(sorted(cands.items()), 1):
    print(f"{i:>3}. [{','.join(sorted(src))[:16]}] {json.dumps(s, ensure_ascii=False)[:150]}")
print("\nфайл:", out[0])
