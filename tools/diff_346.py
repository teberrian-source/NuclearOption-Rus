# -*- coding: utf-8 -*-
"""Формат nomapz + точный diff старых ключей словаря против нового текста 0.34.6."""
import io, json, os, re, sys, difflib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT = os.path.join(REPO, "dict", "ru.json")
MAPZ = os.path.join(os.environ["USERPROFILE"], "Desktop", "Nuclear.Option.v0.34.6",
                    "BepInEx", "plugins", "NOCustomMaps", "maps", "cascadia-0.1.0.nomapz")
DUMP = os.path.join(os.environ["USERPROFILE"], "Desktop", "Nuclear.Option.v0.34.6",
                    "BepInEx", "plugins", "LocalizationPatch", "untranslated.txt")

b = open(MAPZ, "rb").read(16)
print("nomapz первые байты:", b[:8])

# распарсить словарь плагин-стилем
def parse(text):
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

d = parse(io.open(DICT, encoding="utf-8-sig").read())

# строки из дампа
lines = io.open(DUMP, encoding="utf-8").read().splitlines()
dump_texts = {}
for l in lines:
    m = re.match(r'^"(.+)": ""[,]?$', l)
    if m and len(m.group(1)) > 200:
        dump_texts[m.group(1)[:80]] = m.group(1)

print()
print("=== diff старых ключей против нового текста ===")
for frag, new in [
    ("A Confrontation-style war", None),
    ("A small, Altercation-size", None),
    ("The whole of Ironjaw Sound at war, built like the stock Escalation. Bo", None),
]:
    old = next((k for k in d if k.startswith(frag)), None)
    if old is None:
        print("нет ключа:", frag); continue
    # найти новый текст из дампа по префиксу
    cand = next((v for pfx, v in dump_texts.items() if pfx.startswith(frag[:40])), None)
    if cand is None:
        print("нет в дампе:", frag); continue
    print("---", frag[:50])
    if old == cand:
        print("    ПОЛНОЕ СОВПАДЕНИЕ — ключ валиден, проблема в хуках")
        continue
    for line in difflib.unified_diff(old.split(". "), cand.split(". "), lineterm="", n=0):
        if line.startswith(("+", "-", "@@")) and not line.startswith(("+++", "---")):
            print("   ", line[:160])
