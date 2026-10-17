# -*- coding: utf-8 -*-
"""Финальная проверка ru.json после раунда 14."""
import io, re, sys, json, collections

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
p = base + r"\ru.json"
raw = io.open(p, encoding="utf-8-sig").read()
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in raw.split("\n") if not l.strip().startswith("//"))), strict=False)
print("записей:", len(ru))

for k in ["Flares rearmed by", "Flares rearmed by ", "Popping Flares", "Waypoint", "Destroy FARP",
          "Learn how to prepare for and perform a landing. For this lesson you will be piloting the T/A-30 Compass trainer aircraft.",
          "A BDF engineer team is currently trying to recover a pair of tanks that were immobilised in yesterday's fighting.",
          "Our task is to interrupt them. They are without any air defence, and should be easy pickings.",
          "Use the FS-12 Revoker to intercept a volley of cruise missiles launched at your base from Primeva."]:
    print(repr(k[:58]), "->", repr(ru.get(k)))

occ = collections.Counter(m.group(1) for m in re.finditer(r'^\s*"((?:[^"\\]|\\.)*)"\s*:', raw, re.M))
for k, c in occ.items():
    if c > 1:
        vals = [m.group(1) for m in re.finditer(r'^\s*"' + re.escape(k) + r'":\s*("(?:[^"\\]|\\.)*")', raw, re.M)]
        print("ДУБЛЬ", c, repr(k[:45]))
        for v in vals:
            print("     ", v[:110])
