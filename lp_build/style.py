# -*- coding: utf-8 -*-
"""Показывает в ru.json существующие ключи/значения со словами turret/pylon/cargo/mount/coax/launcher."""
import io, json, re, sys

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

def parse_json(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse_json(base + r"\ru.json")
words = ["turret", "pylon", "cargo", "mount", "coax", "launcher", "hook", "bed", "sponson", "bay"]
for w in words:
    print("=" * 80)
    print("СЛОВО:", w)
    n = 0
    for k, v in ru.items():
        if w in k.lower() and len(k) < 40:
            print(f"   {k!r:<40} -> {v!r}")
            n += 1
            if n >= 25:
                break
