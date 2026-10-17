# -*- coding: utf-8 -*-
"""Ищет в дампе подписи слотов подвески (turret mount, subturret, coax, Point Defense, Cargo 2x, Ammo box...)."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

def parse(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse(base + r"\ru.json")
raw = io.open(base + r"\extracted_strings.txt", encoding="utf-8", errors="replace").read()
raw = raw.split("// ========== RAW LONG STRINGS")[0]

WANT = ["turret mount", "subturret", "coax", "Point Defense", "Cargo 2x", "Ammo box", "Main Turret",
        "Основная турель", "Матовая", "Matte Gray", "Tusko", "PAB-3000LR", "hardpoint", "mount"]
found = {}
cur = "?"
for line in raw.split("\n"):
    s = line.strip()
    if s.startswith("//"):
        x = s[2:].strip()
        if x and "===" not in x:
            cur = x
        continue
    m = re.match(r'^"((?:[^"\\]|\\.)*)": ""', s)
    if not m:
        continue
    try:
        t = json.loads('"' + m.group(1) + '"')
    except Exception:
        continue
    for w in WANT:
        if w.lower() in t.lower():
            found.setdefault(w, []).append((cur, t, t in ru))

for w in WANT:
    rows = found.get(w, [])
    print(f"\n=== {w} ({len(rows)}) ===")
    for cur, t, inru in rows[:25]:
        print(f"   [{'ЕСТЬ' if inru else 'НЕТ '}] {cur:<38} {json.dumps(t, ensure_ascii=False)[:110]}")

print("\n--- есть ли в ru.json ---")
for k in ["turret mount", "subturret", "coax", "Point Defense", "Cargo 2x", "Ammo box", "Main Turret", "Matte Gray", "TEST"]:
    print(f"   {'ЕСТЬ' if k in ru else 'НЕТ '}  {k}  ->  {ru.get(k, '')[:60]}")
