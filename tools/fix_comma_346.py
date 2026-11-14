# -*- coding: utf-8 -*-
"""Чинит пропущенную запятую после 'West Coast Landing' и валидирует словарь."""
import io, json, os, shutil, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT = os.path.join(REPO, "dict", "ru.json")
GAME_RU = os.path.join(os.environ["USERPROFILE"], "Desktop",
                       "Nuclear.Option.v0.34.6", "BepInEx", "plugins",
                       "LocalizationPatch", "ru.json")

t = io.open(DICT, encoding="utf-8-sig").read()
bad = '"West Coast Landing": "Посадка на западном побережье"\n    "Centreline"'
good = '"West Coast Landing": "Посадка на западном побережье",\n    "Centreline"'
if bad in t:
    t = t.replace(bad, good, 1)
    print("запятая добавлена")
else:
    print("запятая уже на месте")

if not t.rstrip().endswith("}"):
    t = t.rstrip("\n") + "\n}\n"
    print("закрывающая скобка восстановлена")
io.open(DICT, "w", encoding="utf-8", newline="\n").write(t)

def parse_plugin_style(text):
    outl, in_str, esc, i = [], False, False, 0
    while i < len(text):
        c = text[i]
        if in_str:
            if esc: esc = False
            elif c == "\\": esc = True
            elif c == '"': in_str = False
            outl.append(c)
        else:
            if c == '"': in_str = True; outl.append(c)
            elif c == "/" and i + 1 < len(text) and text[i + 1] == "/":
                while i < len(text) and text[i] != "\n": i += 1
                continue
            else: outl.append(c)
        i += 1
    return json.loads("".join(outl), strict=False)

d = parse_plugin_style(t)
keys = ["Centreline", "CenterLine Pylon", "Middle Pylons", "Wingtips", "Wingtip",
        "Aft Bay", "Laser C-RAM", "Recent", "Early Access Version 0.34.6",
        "A twin-engine, fourth-generation", "Forward Bay"]
print("словарь репо:", len(d), "записей")
print("Forward Bay ->", d.get("Forward Bay"))
ok = all(k in d for k in keys[:9])
print("все новые ключи на месте:", ok)

shutil.copy2(DICT, GAME_RU)
gd = parse_plugin_style(io.open(GAME_RU, encoding="utf-8-sig").read())
print("словарь в игре 0.34.6:", len(gd), "записей")
