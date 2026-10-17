# -*- coding: utf-8 -*-
"""Проверка влитых переводов миссий/подсказок."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
raw = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in raw.split("\n") if not l.strip().startswith("//"))), strict=False)
print("всего записей:", len(ru))

show_keys = [
    "A BDF engineer team is currently trying to recover a pair of tanks that were immobilised in yesterday's fighting.",
    "Our task is to interrupt them. They are without any air defence, and should be easy pickings.",
    "Learn how to prepare for and perform a landing. For this lesson you will be piloting the T/A-30 Compass trainer aircraft.",
    "A battle for air superiority fought between two large airbases, using high-end assets. Rank 3 aircraft available at start.",
]
for k in show_keys:
    print("\nEN:", k)
    print("RU:", ru.get(k))

# заголовки с выравниванием
for k in list(ru):
    if k.startswith("Aerial Targets") or k.startswith("Infrared Countermeasures"):
        print("\nTITLE-KEY:", repr(k))
        print("TITLE-RU :", repr(ru[k]))

# сколько записей с тегами <bind=
print("\nзаписей с <bind=:", sum(1 for k in ru if "<bind=" in k))
# проверка: у каждой ли пары теги совпадают
bad = 0
for k, v in ru.items():
    if re.findall(r"<[^>]+>", k) != re.findall(r"<[^>]+>", v):
        bad += 1
        if bad <= 5:
            print("РАСХОЖДЕНИЕ ТЕГОВ:", repr(k[:70]), re.findall(r"<[^>]+>", k)[:4], "->", re.findall(r"<[^>]+>", v)[:4])
print("пар с расхождением тегов:", bad)
