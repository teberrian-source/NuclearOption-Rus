# -*- coding: utf-8 -*-
"""Выборка переводов раунда 14 для глазной проверки (в UTF-8 файл)."""
import io, re, sys, json

base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
raw = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in raw.split("\n") if not l.strip().startswith("//"))), strict=False)

keys = [
    "A BDF engineer team is currently trying to recover a pair of tanks that were immobilised in yesterday's fighting.",
    "Our task is to interrupt them. They are without any air defence, and should be easy pickings.",
    "A battle for air superiority fought between two large airbases, using high-end assets. Rank 3 aircraft available at start.",
    "A pure air & sea battle between two carrier groups. Boscali's Annex Class Assault Carrier vs Primeva's Hyperion Class Fleet Carrier, with their respective compliments of aircraft.\x0b\x0bThe first side to sink the other's carrier wins. All 36 carrier aircraft are available immediately, and cannot be replaced easily if shot down. Fly, fight, and land with care.",
    "Use various SEAD/DEAD abilities unique to the EW-25 Medusa to facilitate an attack against a heavily defended ammo dump.",
    "Learn how to defeat semi-active radar homing missiles. For this lesson you will be piloting the T/A-30 Compass trainer aircraft.",
]
out = []
for k in keys:
    out.append("EN: " + k + "\nRU: " + str(ru.get(k)) + "\n" + "-" * 40)

# заголовки с выравниванием + подсказки с тегами
out.append("### Заголовки (сохранили ли пробелы и счётчик):")
n = 0
for k, v in ru.items():
    if re.search(r"\s{2,}\d+/\d+$", k):
        out.append("EN: " + repr(k) + "   length " + str(len(k)))
        out.append("RU: " + repr(v) + "   length " + str(len(v)))
        n += 1
        if n >= 6:
            break

out.append("\n### Подсказка с тегами <bind=>:")
n = 0
for k, v in ru.items():
    if "<bind=" in k:
        out.append("EN: " + k)
        out.append("RU: " + v)
        n += 1
        if n >= 2:
            break

io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\sample14.txt", "w", encoding="utf-8", newline="\n").write("\n".join(out))
print("готово")
