# -*- coding: utf-8 -*-
"""Ищет тексты описаний (CI-22, Radome) в Unity-ассетах через UnityPy."""
import sys, io
import UnityPy

root = r"C:\Users\user\Desktop\Nuclear Option\NuclearOption_Data"
targets = ["counter insurgency", "radome", "weapon types"]
files = ["sharedassets1.assets", "resources.assets", "sharedassets3.assets",
         "sharedassets0.assets", "globalgamemanagers.assets",
         "level0", "level1", "level2", "level3", "level4"]
sys.stdout.reconfigure(encoding='utf-8')

def texts_from(obj):
    """Возвращает возможные строковые данные объекта."""
    out = []
    try:
        if obj.type.name == "TextAsset":
            d = obj.read()
            out.append(d.m_Script if hasattr(d, 'm_Script') else None)
        elif obj.type.name == "MonoBehaviour":
            d = obj.read()
            # сырой тип-дерево
            try:
                out.append(str(d))
            except Exception:
                pass
        elif obj.type.name == "String":
            out.append(obj.read())
    except Exception:
        pass
    return [t for t in out if t]

for f in files:
    p = root + "\\" + f
    try:
        env = UnityPy.load(p)
    except Exception as e:
        print(f"!! {f}: {e}")
        continue
    found = 0
    for obj in env.objects:
        for t in texts_from(obj):
            low = t.lower()
            for nd in targets:
                if nd in low:
                    print(f"=== {f} obj={obj.path_id} type={obj.type.name} nd={nd}")
                    i = low.find(nd)
                    print(repr(t[max(0, i-100):i+700]))
                    print()
                    found += 1
                    break
    print(f"-- {f}: scanned, found {found}")
