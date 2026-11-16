# -*- coding: utf-8 -*-
"""Сверка ключей словаря с дампом + поиск полного описания Cascadia Falling в nomapz."""
import io, json, os, re, sys, zipfile

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT = os.path.join(REPO, "dict", "ru.json")
MAPZ = os.path.join(os.environ["USERPROFILE"], "Desktop", "Nuclear.Option.v0.34.6",
                    "BepInEx", "plugins", "NOCustomMaps", "maps", "cascadia-0.1.0.nomapz")

t = io.open(DICT, encoding="utf-8-sig").read()
print("=== ключи словаря, начинающиеся с фрагментов ===")
for frag in ["A Confrontation-style war", "A small, Altercation-size",
             "The whole of Ironjaw Sound at war", "A Primeva amphibious fleet"]:
    idx = t.find('"' + frag)
    if idx < 0:
        print("НЕТ:", frag)
        continue
    end = t.find('"', idx + 1)
    while t[end - 1] == "\\":
        end = t.find('"', end + 1)
    key = t[idx + 1:end]
    print(f"ключ (len={len(key)}): {key[:70]} ... {key[-50:]}")

print()
print("=== содержимое nomapz ===")
z = zipfile.ZipFile(MAPZ)
for n in z.namelist():
    print(" ", n, z.getinfo(n).file_size)
