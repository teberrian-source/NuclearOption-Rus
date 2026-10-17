# -*- coding: utf-8 -*-
"""Поиск известных строк по бинарным файлам игры (bundle, Assembly-CSharp, ресурсы)."""
import io, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
root = r"C:\Users\user\Desktop\NuclearOption_0.34.2"
needles = [b"For this lesson you will be piloting", b"immobilised in yesterday",
           b"engineer team is currently trying"]

targets = []
for dirpath, dirnames, filenames in os.walk(root):
    if "BepInEx" in dirpath:
        continue
    for fn in filenames:
        p = os.path.join(dirpath, fn)
        try:
            if os.path.getsize(p) > 200 * 1024 * 1024:
                continue
        except OSError:
            continue
        targets.append(p)
print("файлов к проверке:", len(targets))

for p in targets:
    try:
        data = open(p, "rb").read()
    except OSError:
        continue
    hits = [n.decode() for n in needles if n in data]
    if hits:
        print(os.path.relpath(p, root), "->", hits)
