# -*- coding: utf-8 -*-
"""Определяет тип файлов модов и ищет в них подписи хардпоинтов (с распаковкой бандлов)."""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
root = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins"
files = [
    r"com.nikkorap.blueprinter\addons\kar\Kar_1.1.2.dll",
    r"com.nikkorap.blueprinter\addons\bote\Bote_1.5.2.dll",
    r"PlayableVehicles\PlayableVehicles.dll",
    r"com.nikkorap.blueprinter\addons\aryx.rah72\Aryx_RAH_72_Knockout_1.1.1.dll",
]
for rel in files:
    p = os.path.join(root, rel)
    with io.open(p, "rb") as f:
        head = f.read(16)
    print(rel, "| size", os.path.getsize(p), "| head", head[:8])
