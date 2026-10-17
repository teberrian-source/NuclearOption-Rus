# -*- coding: utf-8 -*-
"""Проверяет гипотезу: ключи с хвостовым пробелом не срабатывали (плагин делает Trim)."""
import io, json, re, sys, sqlite3

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

def parse_json(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse_json(base + r"\ru.json")
probes = {
    "RAH-72": "The RAH-72 is a recon and light attack helicopter.",
    "MC-260": "Aryx Dynamics' largest aircraft so far",
    "ASD-16": "ASD-16 Aerial Submunitions Dispenser",
}
for tag, pref in probes.items():
    keys = [k for k in ru if k.startswith(pref)]
    print(tag, "ключей:", len(keys))
    for k in keys:
        print("   хвост:", repr(k[-25:]), "| пробел в конце:", k != k.rstrip(), "| значение:", ru[k][:60])
