# -*- coding: utf-8 -*-
"""Показывает точные ключи ru.json, начинающиеся с заданных префиксов, и сравнивает с экспортом."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
raw = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

for pref in ("The engine of your aircraft", "A compact medium-range INS", "Conceived at the turn of the century"):
    print("=" * 78)
    for k in ru:
        if k.startswith(pref):
            print("ru.json ключ:", repr(k))
            print("  длина:", len(k))
            print("  значение:", repr(ru[k])[:160])
    # ищем в экспорте
    ex = open(base + r"\untranslated.txt", "rb").read().decode("utf-8", "replace")
    for m in re.finditer(r'"((?:[^"\\]|\\.)*)": ""', ex):
        try:
            k = json.loads('"' + m.group(1) + '"')
        except Exception:
            continue
        if k.startswith(pref):
            print("экспорт ключ:", repr(k))
            print("  длина:", len(k))
