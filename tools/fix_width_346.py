# -*- coding: utf-8 -*-
"""Валидация словаря после правок ширины (раунд 18) и раскатка в игру."""
import io, json, os, shutil, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT = os.path.join(REPO, "dict", "ru.json")
GAME_RU = os.path.join(os.environ["USERPROFILE"], "Desktop", "Nuclear.Option.v0.34.6",
                       "BepInEx", "plugins", "LocalizationPatch", "ru.json")

t = io.open(DICT, encoding="utf-8-sig").read()
outl, in_str, esc, i = [], False, False, 0
while i < len(t):
    c = t[i]
    if in_str:
        if esc: esc = False
        elif c == "\\": esc = True
        elif c == '"': in_str = False
        outl.append(c)
    else:
        if c == '"': in_str = True; outl.append(c)
        elif c == "/" and i + 1 < len(t) and t[i + 1] == "/":
            while i < len(t) and t[i] != "\n": i += 1
            continue
        else: outl.append(c)
    i += 1
d = json.loads("".join(outl), strict=False)
print("записей:", len(d))
for k in ["RCS :", "RCS:", "Next aircraft:", "Next aircraft:\nNever",
          "RESTART MISSION", "Development Roadmap", "Join our Community", "Join Our Community"]:
    print(repr(k), "->", repr(d.get(k)))
shutil.copy2(DICT, GAME_RU)
print("репо и игра совпадают побайтово:", open(DICT, "rb").read() == open(GAME_RU, "rb").read())
