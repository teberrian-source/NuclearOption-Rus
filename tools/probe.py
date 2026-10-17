# -*- coding: utf-8 -*-
"""Проверяет наличие конкретных строк из скриншотов и собирает игровые подписи хардпоинтов."""
import io, json, re, sys

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

def parse_json(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse_json(base + r"\ru.json")
probes = [
    "This upfit for the AFV8 chassis features a 25mm cannon and anti-armor missile launcher, turning it into a fast infantry fighting vehicle. It's also amphibious",
    "A large anti-surface bomb granted extended range with an unpowered glide kit and INS guidance, able to destroy multiple hardened structures in a single hit.",
]
for p in probes:
    print(("ЕСТЬ " if p in ru else "НЕТ  "), json.dumps(p[:70], ensure_ascii=False), "->", ru.get(p, "")[:70])
