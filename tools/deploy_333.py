# -*- coding: utf-8 -*-
"""Развёртывание 3.3.3 (рескан по Ctrl+F5) в игру."""
import hashlib, os, shutil, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SRC = r"C:\Users\user\Documents\NuclearOption_Rus\plugin\bin\Release\LocalizationPatch.dll"
DST = r"C:\Users\user\Desktop\Nuclear.Option.v0.34.6\BepInEx\plugins\LocalizationPatch\LocalizationPatch.dll"
print("собрано:", os.path.getsize(SRC), "Б, sha256",
      hashlib.sha256(open(SRC, "rb").read()).hexdigest()[:16].upper())
try:
    shutil.copy2(SRC, DST)
    print("развёрнуто в игру OK")
except PermissionError:
    print("Игра запущена — DLL занята, копирую в резерв")
    shutil.copy2(SRC, DST + ".new")
