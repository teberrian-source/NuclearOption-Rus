# -*- coding: utf-8 -*-
"""Ищет в ru.json ключи по русским значениям (обратный поиск) — для понимания конвенций."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
raw = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

for val in ["НЕЯДЕРНОЕ", "Неядерное", "ТАКТИЧЕСКИЙ", "ТАКТИЧЕСКАЯ", "СТРАТЕГИЧЕСКИЙ", "ИНС", "Активное"]:
    hits = [k for k, v in ru.items() if v == val]
    print(f"  значение {val!r}: {hits if hits else '(нет)'}")

print()
print("--- ключи, начинающиеся с 'INS' / содержащие 'INS' ---")
for k in sorted(ru):
    if re.match(r"(?i)^ins\b", k) or re.search(r"(?i)\bINS\b", k):
        print(f"  {k!r} -> {ru[k]!r}")
