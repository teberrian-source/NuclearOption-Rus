# -*- coding: utf-8 -*-
"""Где лежат описания миссий ([FS-41], Carrier Duel Lite, Ironjaw) и имена точек маршрута."""
import io, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
root = r"C:\Users\user\Desktop\NuclearOption_0.34.2"
needles = [
    b"catapults of a Penumbra-class",
    b"Ingress Via Mountains",
    b"Terrison's diverse and heavy armament",
    b"Cursor-class LFD of BDF",
    b"Air race on Ironjaw Sound: Fjord Sprint",
]
skip_dirs = ("\\BepInEx\\",)

for dirpath, dirnames, filenames in os.walk(root):
    if any(s in dirpath + "\\" for s in skip_dirs):
        continue
    for fn in filenames:
        p = os.path.join(dirpath, fn)
        try:
            if os.path.getsize(p) > 300 * 1024 * 1024:
                continue
            data = open(p, "rb").read()
        except OSError:
            continue
        hits = [n.decode() for n in needles if n in data]
        if hits:
            print(os.path.relpath(p, root), "->", len(hits), [h[:32] for h in hits])
