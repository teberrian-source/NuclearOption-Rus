# -*- coding: utf-8 -*-
"""Развёртывание ru.json (раунд 19) в игру."""
import os, shutil, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SRC = r"C:\Users\user\Documents\NuclearOption_Rus\dict\ru.json"
DST = r"C:\Users\user\Desktop\Nuclear.Option.v0.34.6\BepInEx\plugins\LocalizationPatch\ru.json"
print("размер:", os.path.getsize(SRC), "Б")
try:
    shutil.copy2(SRC, DST)
    print("развёрнуто OK")
except PermissionError:
    print("Игра запущена — файл занят, попробуй после закрытия")
