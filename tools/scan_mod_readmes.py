# -*- coding: utf-8 -*-
"""Сбор описаний активных модов: readme/manifest/AssemblyInfo в папках плагинов."""
import io, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BE = r"C:\Users\user\Desktop\Nuclear.Option.v0.34.6\BepInEx"
PLUGINS = os.path.join(BE, "plugins")

for name in sorted(os.listdir(PLUGINS)):
    p = os.path.join(PLUGINS, name)
    print("=" * 70)
    print("Мод:", name)
    if os.path.isfile(p):
        continue
    for root, dirs, files in os.walk(p):
        for f in files:
            lf = f.lower()
            if lf.endswith((".md", ".txt", ".json")) and any(
                k in lf for k in ("readme", "manifest", "info", "about", "license")
            ):
                fp = os.path.join(root, f)
                try:
                    txt = io.open(fp, encoding="utf-8-sig", errors="replace").read()
                except Exception as e:
                    txt = str(e)
                print("  ---", os.path.relpath(fp, p))
                for line in txt.splitlines()[:15]:
                    print("   |", line[:150])
