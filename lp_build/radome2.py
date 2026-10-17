# -*- coding: utf-8 -*-
"""Точная запись обтекателя РЛС в ru.json + hit/miss в логе."""
import io, json, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

def parse_json(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse_json(base + r"\ru.json")
print("--- запись обтекателя РЛС в ru.json ---")
for k, v in ru.items():
    if k.startswith("An extremely powerful long-range all-aspect radar", 0) or k.startswith("An extremely powerful"):
        print("KEY  :", repr(k))
        print("LEN  :", len(k))
        print("VALUE:", repr(v))
        print()

log = io.open(r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\LogOutput.log", encoding="utf-8", errors="replace").read()
print("--- hit/miss по обтекателю ---")
n = 0
for m in re.finditer(r'\[TRACE\] (hit|miss): "(.*)"$', log, re.M):
    if "extremely powerful" in m.group(2) or "Radome" in m.group(2) or "Обтекател" in m.group(2):
        n += 1
        print(m.group(1), "::", m.group(2)[:160])
print("всего:", n)
