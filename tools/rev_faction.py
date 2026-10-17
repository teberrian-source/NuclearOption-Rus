# -*- coding: utf-8 -*-
"""Обратный поиск: какие ключи дают русские названия фракций."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
raw = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

for val in ["Альянс вооруженного освобождения Примева", "Силы обороны Боскали", "Сухопутные войска"]:
    print(f"{val!r}: {[k for k, v in ru.items() if v == val] or '(нет)'}")

print()
print("--- ключи со словами Alliance / Boscali / Aviation / Liberation / Armed ---")
for k in sorted(ru):
    if re.search(r"(?i)(alliance|boscali|liberation|general aviation|armed forces)", k) and len(k) < 90:
        print(f"  {k!r} -> {ru[k]!r}")
