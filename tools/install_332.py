# -*- coding: utf-8 -*-
"""Установка DLL v3.3.2 в игру (игра должна быть закрыта) + синхронизация plugin\\build."""
import hashlib, os, shutil, sys, time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
GAME = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
SRC = r"C:\Users\user\Documents\NuclearOption_Rus\plugin\bin\Release\LocalizationPatch.dll"

def placed():
    dst = os.path.join(GAME, "LocalizationPatch.dll")
    stamp = time.strftime("%H%M%S")
    shutil.copy2(dst, dst + ".bak_" + stamp)
    shutil.copy2(SRC, dst)
    shutil.copy2(SRC, r"C:\Users\user\Documents\NuclearOption_Rus\plugin\build\LocalizationPatch.dll")

def h(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16].upper()

placed()
print("bin     :", h(SRC))
print("build   :", h(r"C:\Users\user\Documents\NuclearOption_Rus\plugin\build\LocalizationPatch.dll"))
print("в игре  :", h(os.path.join(GAME, "LocalizationPatch.dll")))
