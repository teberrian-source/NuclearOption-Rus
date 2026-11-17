# -*- coding: utf-8 -*-
"""Развёртывание AllocProbe.dll в игру (только при закрытой игре)."""
import os, shutil, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SRC = r"C:\Users\user\Documents\NuclearOption_Rus\plugin\AllocProbe\bin\Release\AllocProbe.dll"
DST = r"C:\Users\user\Desktop\Nuclear.Option.v0.34.6\BepInEx\plugins\AllocProbe.dll"

tl = subprocess.run(["tasklist", "/FI", "IMAGENAME eq NuclearOption.exe"],
                    capture_output=True, text=True).stdout
if "NuclearOption.exe" in tl:
    print("Игра ЗАПУЩЕНА — закрой её, потом скажи 'ставь'")
    sys.exit(1)

shutil.copy2(SRC, DST)
print("AllocProbe.dll развёрнут:", os.path.getsize(DST), "Б")
