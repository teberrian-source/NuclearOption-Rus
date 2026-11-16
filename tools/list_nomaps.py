# -*- coding: utf-8 -*-
"""Список файлов NOCustomMaps (карты и аддоны) с размерами."""
import os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
M = r"C:\Users\user\Desktop\Nuclear.Option.v0.34.6\BepInEx\plugins\NOCustomMaps"
for root, dirs, files in os.walk(M):
    for f in files:
        fp = os.path.join(root, f)
        rel = fp.replace(M, "NOCustomMaps")
        print(f"{os.path.getsize(fp) / 1048576:9.1f} МБ  {rel}")
