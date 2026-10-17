# -*- coding: utf-8 -*-
"""Ищет TextAsset с описаниями узлов оружия ('supersonic stand-off') по всем ассетам."""
import sys, re, os
import UnityPy

root = r"C:\Users\user\Desktop\Nuclear Option\NuclearOption_Data"
sys.stdout.reconfigure(encoding='utf-8')

files = ["resources.assets", "sharedassets0.assets", "sharedassets1.assets",
         "sharedassets2.assets", "sharedassets3.assets", "sharedassets4.assets",
         "globalgamemanagers.assets"]
needle = 'supersonic stand-off'
for f in files:
    p = os.path.join(root, f)
    if not os.path.exists(p):
        continue
    try:
        env = UnityPy.load(p)
    except Exception as e:
        print(f"!! {f}: {e}")
        continue
    for obj in env.objects:
        if obj.type.name != "TextAsset":
            continue
        try:
            s = obj.read().m_Script
        except Exception:
            continue
        if s and needle in s:
            print(f"=== {f} path_id={obj.path_id} len={len(s)}")
            i = s.find(needle)
            print(repr(s[max(0,i-400):i+400]))
            print()
            # Radome в этом же ассете?
            for m in re.finditer(r'.{0,150}Radome.{0,250}', s):
                print("RADOME CTX:", repr(m.group(0))[:450], "\n")
