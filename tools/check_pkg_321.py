# -*- coding: utf-8 -*-
"""Проверка пакета v3.3.2.1: состав zip, хэши, число записей словаря."""
import hashlib, io, json, os, re, sys, zipfile

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIP = os.path.join(REPO, "dist", "NuclearOption-Rus-v3.3.2.1.zip")

z = zipfile.ZipFile(ZIP)
print("=== состав zip ===")
for n in z.namelist():
    b = z.read(n)
    print(f"  {n:70s} {len(b):>9} Б {hashlib.sha256(b).hexdigest()[:16].upper()}")

# словарь из пакета
t = z.read("NuclearOption-Rus-v3.3.2.1/BepInEx/plugins/LocalizationPatch/ru.json").decode("utf-8-sig")
outl, in_str, esc, i = [], False, False, 0
while i < len(t):
    c = t[i]
    if in_str:
        if esc: esc = False
        elif c == "\\": esc = True
        elif c == '"': in_str = False
        outl.append(c)
    else:
        if c == '"': in_str = True; outl.append(c)
        elif c == "/" and i + 1 < len(t) and t[i + 1] == "/":
            while i < len(t) and t[i] != "\n": i += 1
            continue
        else: outl.append(c)
    i += 1
d = json.loads("".join(outl), strict=False)
print("словарь в пакете:", len(d), "записей")
checks = ["Радиозаметность :", "ПЕРЕЗАПУСК МИССИИ", "Дорожная карта", "Наше сообщество",
          "Cascadia Falling. PALA attacks", "Следующий: никогда"]
for c in checks:
    ok = any(c == v or c in v for v in d.values()) or c in d
    print(("  OK " if ok else "  !! "), c)

dll = z.read("NuclearOption-Rus-v3.3.2.1/BepInEx/plugins/LocalizationPatch/LocalizationPatch.dll")
print("DLL в пакете == DLL в игре:",
      hashlib.sha256(dll).hexdigest()[:16].upper() == "80D7024E7A8EC404")
