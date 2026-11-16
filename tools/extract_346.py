# -*- coding: utf-8 -*-
"""Вытащить полные исходные строки для перевода из untranslated.txt -> tools/src_346.json."""
import io, json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUMP = os.path.join(os.environ["USERPROFILE"], "Desktop", "Nuclear.Option.v0.34.6",
                    "BepInEx", "plugins", "LocalizationPatch", "untranslated.txt")

lines = io.open(DUMP, encoding="utf-8").read().splitlines()
texts = []
for l in lines:
    m = re.match(r'^"(.+)": ""[,]?$', l)
    if m:
        texts.append(m.group(1))

prefixes = [
    "The whole of Ironjaw Sound at war, built like the stock Escalation, with two fronts",
    "The whole of Ironjaw Sound at war, built like the stock Escalation. Boscali hold the south",
    "A Confrontation-style war",
    "A Primeva amphibious fleet is massing",
    "A small, Altercation-size strike",
    "Primeva has walled off the Lower Ice",
    "Primeva have spread seven long-range SAM sites",
    "Take part in a PALA operation",
    "Welcome to the beautiful Swiss Alps",
    "NEEDS: NOCustomMaps 1.4+",
    "Light short-range infrared missile",
    "Short-range infrared missile. Thrust vectoring",
]
out = {}
for p in prefixes:
    match = [t for t in texts if t.startswith(p)]
    if match:
        out[p] = match[0]
        print(f"[OK] len={len(match[0])}: {p[:60]}")
    else:
        print("[НЕТ]", p[:60])

io.open(os.path.join(REPO, "tools", "src_346.json"), "w", encoding="utf-8").write(
    json.dumps(out, ensure_ascii=False, indent=1))
print("сохранено: tools/src_346.json,", len(out), "строк")
