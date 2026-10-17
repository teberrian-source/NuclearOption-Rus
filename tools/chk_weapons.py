# -*- coding: utf-8 -*-
"""Проверяет, переводим ли названия вооружения (gunpod, drop tank, dispenser, pod)."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
raw = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

pat = re.compile(r"(?i)(autocannon|rotary cannon|machine gun|gunpod|drop tank|dispenser|targeting pod|jammer|rounds)")
print("--- ключи с названиями подвесного вооружения ---")
for k in sorted(ru):
    if pat.search(k) and len(k) < 70:
        print(f"  {k!r} -> {ru[k]!r}")
