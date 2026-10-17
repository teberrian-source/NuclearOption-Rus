# -*- coding: utf-8 -*-
"""Ищет в extracted_gamedata.txt (энциклопедия) английские описания, которых нет в ru.json."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

def load(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = load(base + r"\ru.json")
todo = json.loads(io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\todo.json", encoding="utf-8").read())
todo_en = {it["en"] for it in todo}

print("--- шапка extracted_gamedata.txt ---")
head = io.open(base + r"\extracted_gamedata.txt", encoding="utf-8", errors="replace").read().split("\n")
for l in head[:25]:
    print("   ", l[:150])

CYR = re.compile(r"[А-Яа-яЁё]")
def sentence_like(s):
    if not (35 <= len(s) <= 900):
        return False
    if CYR.search(s):
        return False
    letters = sum(1 for c in s if c.isalpha())
    if letters * 100 // max(1, len(s)) < 60:
        return False
    if len(re.findall(r"[A-Za-z]{2,}", s)) < 8:
        return False
    return True

cands = {}
for line in head:
    s = line.strip()
    if not s or s.startswith("//") or s.startswith("["):
        continue
    for piece in re.split(r"\s\|\s", s):
        p2 = piece.strip()
        if p2 and p2 not in ru and p2 not in todo_en and sentence_like(p2):
            cands[p2] = cands.get(p2, 0) + 1

print()
print("кандидатов из энциклопедии:", len(cands))
for i, (s, n) in enumerate(sorted(cands.items()), 1):
    print(f"{i:>3}. {json.dumps(s, ensure_ascii=False)[:190]}")
