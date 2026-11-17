# -*- coding: utf-8 -*-
"""Диагностика попытки А: принял ли Unity Mono опцию --profile=log:alloc."""
import io, os, re, sys, time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
GAME = r"C:\Users\user\Desktop\Nuclear.Option.v0.34.6"
PLAYER = os.path.join(os.environ.get("USERPROFILE", ""), r"AppData\LocalLow\Shockfront\Nuclear Option\Player.log")
BEX = os.path.join(GAME, r"BepInEx\LogOutput.log")

for name, p in (("Player.log", PLAYER), ("BepInEx LogOutput.log", BEX)):
    if not os.path.exists(p):
        print(name, "— нет файла")
        continue
    print("===", name, "| изменён", time.strftime("%H:%M:%S", time.localtime(os.path.getmtime(p))))
    t = io.open(p, encoding="utf-8", errors="replace").read()
    lines = t.splitlines()
    print("строк:", len(lines))
    pat = re.compile(r"(?i)profile|MONO_OPTIONS|profiler|Unknown option|mono|alloc")
    hits = [l for l in lines if pat.search(l)]
    print("совпадений:", len(hits))
    for l in hits[:25]:
        print("  ", l[:180])
    print("  --- первые 6 строк файла ---")
    for l in lines[:6]:
        print("  |", l[:180])
