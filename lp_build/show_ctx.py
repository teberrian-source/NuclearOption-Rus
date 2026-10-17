# -*- coding: utf-8 -*-
"""Печатает переводы для контекстных ключей (фракции, эскалация, режимы)."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
raw = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

for k in ["Heartland", "CONVENTIONAL", "Conventional", "NUCLEAR", "Nuclear",
          "TACTICAL", "Tactical", "Air to Air", "Air to Ground", "Escalation",
          "TACTICAL NUCLEAR", "Primeva", "Boscali", "SOUTH BOSCALI", "WMC", "SPRHD", "LDR"]:
    print(f"  {k!r} -> {ru.get(k, '(нет)')!r}")

print()
print("--- ключи, содержащие 'Heartland' / 'Conventional' / 'Escalation' ---")
for k in sorted(ru):
    if re.search(r"(?i)(heartland|conventional|escalation|nuclear level)", k):
        print(f"  {k!r} -> {ru[k]!r}")
