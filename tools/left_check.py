# -*- coding: utf-8 -*-
"""Проверяет остатки UI-строк из untranslated.txt в ru.json."""
import io, json, re, sys

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

def parse_json(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse_json(base + r"\ru.json")
probes = ["Choose a Mission", "Choose Mission", "Mission Title", "In-game", "Online", "Offline",
          "Refresh", "password", "no password", "<i>password</i>", "<i>no password</i>",
          "<NOT LOADED>", "< NOT LOADED>", "A-A", "A-G", "SPD", "HDG", "UP", "LDR", "ROT", "YAW",
          "WMC", "AVG", "TRANS", "RNG -", "Creating Lobby...", "Player A killed Player B",
          "Test", "Aircraft : AA-nn", "Cursor : AA-nn", "AVG ", "LOCAL 10M", "2h 30m"]
for c in probes:
    print(f'{"ЕСТЬ" if c in ru else "нет "}  {c!r:<28} {ru.get(c,"")}')
print("\n--- похожие ключи ---")
for w in ["Choose", "Lobby", "Online", "password", "Refresh", "In-game", "Air-to", "A-A"]:
    hits = [k for k in ru if w.lower() in k.lower()][:12]
    print(f"{w}: {hits}")
