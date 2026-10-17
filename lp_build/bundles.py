# -*- coding: utf-8 -*-
"""Ищет внутри модовых сборок встроенные Unity-бандлы (UnityFS/UnityWeb) и др."""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
root = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins"
magics = [b"UnityFS", b"UnityWeb", b"UnityRaw", b"PK\x03\x04", b"\x1f\x8b"]
for dirpath, dirs, files in os.walk(root):
    if "LocalizationPatch" in dirpath:
        continue
    for f in files:
        if not f.lower().endswith(".dll"):
            continue
        p = os.path.join(dirpath, f)
        data = io.open(p, "rb").read()
        found = []
        for mg in magics:
            for m in re.finditer(re.escape(mg), data):
                found.append((m.start(), mg))
        if found:
            print(os.path.relpath(p, root), os.path.getsize(p), [(o, mg.decode("latin1")) for o, mg in found[:8]])
