# -*- coding: utf-8 -*-
"""Финал: валидация словаря, раскатка в игру, поиск периодической активности в логе."""
import io, json, os, re, shutil, sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT = os.path.join(REPO, "dict", "ru.json")
GAME_RU = os.path.join(os.environ["USERPROFILE"], "Desktop", "Nuclear.Option.v0.34.6",
                       "BepInEx", "plugins", "LocalizationPatch", "ru.json")
LOG = os.path.join(os.environ["USERPROFILE"], "Desktop", "Nuclear.Option.v0.34.6", "BepInEx", "LogOutput.log")

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
print("словарь репо:", len(d), "| 'Next aircraft:' ->", repr(d["Next aircraft:"]))
shutil.copy2(DICT, GAME_RU)
print("репо и игра совпадают побайтово:", open(DICT, "rb").read() == open(GAME_RU, "rb").read())

# периодическая активность: повторяющиеся строки в логе
if os.path.isfile(LOG):
    lines = io.open(LOG, encoding="utf-8", errors="replace").read().splitlines()
    print("строк в логе:", len(lines))
    pat = re.compile(r"\d")
    cnt = Counter(re.sub(r"\d+", "#", l)[:90] for l in lines
                  if not l.startswith("[Message:   BepInEx]") and "VERBOSE" not in l)
    print("самые частые шаблоны строк (после удаления цифр):")
    for s, n in cnt.most_common(12):
        if n > 3:
            print(f"  x{n}: {s}")
