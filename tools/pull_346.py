# -*- coding: utf-8 -*-
"""Достаём полные длинные строки из untranslated.txt и проверяем их наличие в dict/ru.json."""
import io, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUMP = os.path.join(os.environ["USERPROFILE"], "Desktop", "Nuclear.Option.v0.34.6",
                    "BepInEx", "plugins", "LocalizationPatch", "untranslated.txt")
DICT = os.path.join(REPO, "dict", "ru.json")

lines = io.open(DUMP, encoding="utf-8").read().splitlines()
long_lines = [l for l in lines if len(l) > 260]
out = io.open(os.path.join(REPO, "tools", "long_lines_346.txt"), "w", encoding="utf-8")
for l in long_lines:
    out.write(l + "\n\n")
out.close()
print("длинных строк:", len(long_lines), "-> tools/long_lines_346.txt")

dt = io.open(DICT, encoding="utf-8-sig").read()
import json
# наличие ключей (первые 90 символов) в словаре
def present(s):
    key_frag = json.dumps(s[:90], ensure_ascii=False)[1:-1]  # тело ключа без кавычек
    return key_frag in dt

for probe in [
    "The whole of Ironjaw Sound at war, built like the stock Escalation, with two fronts",
    "The whole of Ironjaw Sound at war, built like the stock Escalation. Boscali hold the south",
    "A Confrontation-style war over the east half",
    "A Primeva amphibious fleet is massing",
    "A small, Altercation-size strike up Graylock Fjord",
    "Primeva has walled off the Lower Ice",
    "Primeva have spread seven long-range SAM sites",
    "Take part in a PALA operation",
    "Welcome to the beautiful Swiss Alps",
    "NEEDS: NOCustomMaps 1.4+ and the Cascadia map",
    "Light short-range infrared missile. Very agile",
    "Short-range infrared missile. Thrust vectoring and a 45 degree",
    "Hardened Aircraft Shelter",
    "Initiates a vote-kick",
    "No Results",
]:
    print(("ЕСТЬ   " if present(probe) else "НЕТ    "), probe[:70])
