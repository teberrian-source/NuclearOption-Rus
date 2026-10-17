# -*- coding: utf-8 -*-
"""Сверка: что именно изменилось после выравнивания заголовков."""
import io, sys, difflib, hashlib

base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
a = io.open(base + r"\ru.backup_235931.json", encoding="utf-8-sig").read().split("\n")
b = io.open(base + r"\ru.json", encoding="utf-8-sig").read().split("\n")
print("строк было/стало:", len(a), len(b))
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
chg = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        continue
    chg += max(i2 - i1, j2 - j1)
    for k in range(max(i2 - i1, j2 - j1)):
        old = a[i1 + k] if i1 + k < i2 else ""
        new = b[j1 + k] if j1 + k < j2 else ""
        print(tag, "| было:", repr(old[:70]))
        print("     | стало:", repr(new[:70]))
print("изменённых строк:", chg)

h = [hashlib.sha256(io.open(p, "rb").read()).hexdigest().upper() for p in
     (base + r"\ru.json",
      r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\config\LocalizationPatch\ru.json",
      r"C:\Users\user\Documents\NuclearOption_Rus\ru.json")]
print("хэши копий:", h[0][:16], "| совпадают:", len(set(h)) == 1)
