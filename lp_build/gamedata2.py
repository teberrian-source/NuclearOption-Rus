# -*- coding: utf-8 -*-
"""Показывает секции extracted_gamedata.txt и собирает все строки-описания, которых нет в ru.json."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
T = r"C:\Users\user\AppData\Local\Temp\lp_build"

def load(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = load(base + r"\ru.json")
todo = json.loads(io.open(T + r"\todo.json", encoding="utf-8").read())
known = {it["en"] for it in todo}

lines = io.open(base + r"\extracted_gamedata.txt", encoding="utf-8", errors="replace").read().split("\n")

print("--- секции ---")
for i, l in enumerate(lines):
    if l.strip().startswith("// =") or (l.strip().startswith("//") and not l.strip().startswith("// Raw")):
        print(f"{i:>6}: {l.strip()[:120]}")

CYR = re.compile(r"[А-Яа-яЁё]")
def sentence_like(s):
    if not (30 <= len(s) <= 1200):
        return False
    if CYR.search(s):
        return False
    letters = sum(1 for c in s if c.isalpha())
    if letters * 100 // max(1, len(s)) < 55:
        return False
    return len(re.findall(r"[A-Za-z]{2,}", s)) >= 5

hints, objs, other = {}, {}, {}
for l in lines:
    s = l.strip()
    if not s or s.startswith("//"):
        continue
    m = re.match(r'^(?:Did you know\?|[^;]{0,20});(.+)$', s)
    if m and not s.startswith('"'):
        t = m.group(1).strip()
        if t not in ru and t not in known and sentence_like(t):
            hints[t] = 1
        continue
    m = re.match(r'^"((?:[^"\\]|\\.)*)":\s*"",?$', s)
    if m:
        try:
            t = json.loads('"' + m.group(1) + '"')
        except Exception:
            continue
        if t not in ru and t not in known and sentence_like(t):
            objs[t] = 1
        continue
    if s not in ru and s not in known and sentence_like(s):
        other[s] = 1

print("\nновых подсказок (CSV):", len(hints))
print("новых описаний объектов:", len(objs))
print("прочее:", len(other))

with io.open(T + r"\todo2.txt", "w", encoding="utf-8") as f:
    for tag, d in (("hint", hints), ("object", objs), ("other", other)):
        f.write(f"########## {tag} ({len(d)}) ##########\n")
        for t in sorted(d):
            f.write(f"[{tag}] {t}\n")
print("файл: todo2.txt")
