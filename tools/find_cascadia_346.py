# -*- coding: utf-8 -*-
"""Поиск полного описания Cascadia Falling: лог игры, кэш NOMM, AppData."""
import io, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
needles = ["each silo field", "PALA wins by taking", "assault carriers"]
roots = [
    os.path.join(os.environ["USERPROFILE"], "Desktop", "Nuclear.Option.v0.34.6", "BepInEx", "LogOutput.log"),
    os.path.join(os.environ["USERPROFILE"], "Desktop", "Nuclear.Option.v0.34.6", "BepInEx"),
    os.path.join(os.environ["USERPROFILE"], "Desktop", "NuclearOption_Music"),
]
# NOMM-кэш
for base in (os.environ.get("LOCALAPPDATA", ""), os.environ.get("APPDATA", "")):
    if base:
        for d in os.listdir(base):
            if "nomm" in d.lower() or "nuclear" in d.lower():
                roots.append(os.path.join(base, d))

hits = 0
for r in roots:
    if os.path.isfile(r):
        files = [r]
    elif os.path.isdir(r):
        files = []
        for root, dirs, fs in os.walk(r):
            dirs[:] = [d for d in dirs if d not in ("Blueprinter_Cache", "cache")]
            files += [os.path.join(root, f) for f in fs if os.path.getsize(os.path.join(root, f)) < 20_000_000]
    else:
        continue
    for p in files:
        try:
            t = io.open(p, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        for n in needles:
            i = t.find(n)
            if i >= 0:
                print("НАЙДЕНО", repr(n), "в", p)
                print("   контекст:", t[max(0, i - 200):i + 400].replace("\\n", " ")[:500])
                hits += 1
                break
print("итого файлов с вхождениями:", hits)
