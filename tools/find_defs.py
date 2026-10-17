# -*- coding: utf-8 -*-
"""Проверяет, где в модах лежат определения оружия (имена/описания)."""
import sys, os, glob, re

sys.stdout.reconfigure(encoding="utf-8")
roots = [r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins"]
targets = ["Scythe", "MissileDefinition", "MRM-S4", "Broadsword", "weaponPack"]
for root in roots:
    for dirpath, dirnames, filenames in os.walk(root):
        for name in filenames:
            p = os.path.join(dirpath, name)
            try:
                if os.path.getsize(p) > 200_000_000:
                    continue
                data = open(p, "rb").read()
            except Exception:
                continue
            found = {}
            for t in targets:
                for enc, tag in (("utf-8", "u8"), ("utf-16-le", "u16")):
                    if data.find(t.encode(enc)) >= 0:
                        found.setdefault(t, []).append(tag)
            if found:
                print(f"{os.path.relpath(p, root)}  ->  {found}")

print("\n=== расширения файлов в blueprinter addons ===")
bp = root + r"\com.nikkorap.blueprinter\addons"
for d in sorted(os.listdir(bp))[:25]:
    sub = os.path.join(bp, d)
    if os.path.isdir(sub):
        files = os.listdir(sub)
        print(f"  {d}: {files[:4]}")
