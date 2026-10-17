# -*- coding: utf-8 -*-
"""Показывает примеры длинных переводов из ru.json (для единого стиля)."""
import io, re, sys, json
sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
raw = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

longs = [(k, v) for k, v in ru.items() if len(v) > 90 and len(k) > 60]
print("длинных переводов:", len(longs))
for k, v in longs[:18]:
    print("-", k[:90])
    print("  ->", v[:220])
print()
for word in ["боев", "РЛС", "ГСН", "торпед", "вертолёт", "авианос", "фрегат", "малозамет", "глушил"]:
    hits = [v for v in ru.values() if word.lower() in v.lower()]
    print(f"{word}: {len(hits)} | пример: {hits[0][:120] if hits else '-'}")
