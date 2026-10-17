# -*- coding: utf-8 -*-
"""Ищет источник описаний предметов LOADOUT по уникальным фразам из ru.json."""
import sys, re, os
import UnityPy

root = r"C:\Users\user\Desktop\Nuclear Option\NuclearOption_Data"
sys.stdout.reconfigure(encoding='utf-8')

needles = ['deploys a parachute', 'picked up by ships', 'delay fuse']
files = ["resources.assets", "sharedassets0.assets", "sharedassets1.assets",
         "sharedassets2.assets", "sharedassets3.assets", "sharedassets4.assets"]
for f in files:
    p = os.path.join(root, f)
    if not os.path.exists(p):
        continue
    env = UnityPy.load(p)
    for obj in env.objects:
        if obj.type.name != "TextAsset":
            continue
        try:
            s = obj.read().m_Script
        except Exception:
            continue
        if not s:
            continue
        for nd in needles:
            if nd in s:
                i = s.find(nd)
                print(f"=== {f} path_id={obj.path_id} len={len(s)} nd={nd!r}")
                print(repr(s[max(0,i-600):i+600]))
                print()
                # Radome рядом?
                for m in re.finditer(r'.{0,120}Radome.{0,200}', s):
                    print("RADOME:", repr(m.group(0))[:400])
                break
