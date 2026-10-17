# -*- coding: utf-8 -*-
"""Ищет подписи слотов в .NET-сборках модов с учётом UTF-16LE (#US heap)."""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
root = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins"
needles = ["subturret", "Ammo box", "Truck bed", "cargo 2x", "turret mount", "Point Defence", "Main Turret", "Coaxial"]

def variants(n):
    return [n.encode("ascii"), n.encode("utf-16-le"), n.lower().encode("ascii"), n.lower().encode("utf-16-le")]

for dirpath, dirs, files in os.walk(root):
    if "LocalizationPatch" in dirpath:
        continue
    for f in files:
        if not f.lower().endswith(".dll"):
            continue
        p = os.path.join(dirpath, f)
        try:
            data = io.open(p, "rb").read()
        except Exception:
            continue
        found = []
        for n in needles:
            for v in variants(n):
                for m in re.finditer(re.escape(v), data):
                    found.append((m.start(), n))
        if not found:
            continue
        print("=" * 100)
        print("FILE:", p, os.path.getsize(p), "hits:", len(found))
        for off, n in sorted(found)[:30]:
            chunk = data[max(0, off - 120):off + 160]
            txt = "".join(chr(c) if 32 <= c < 127 else "." for c in chunk)
            print(f"   {n} @ {off}: {txt}")
