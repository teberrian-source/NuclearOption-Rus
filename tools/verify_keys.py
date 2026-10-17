# -*- coding: utf-8 -*-
"""Сверяет roadmap-ключи ru.json с ключами из свежего untranslated.txt (v3.1.0)."""
import json, re, io, sys

sys.stdout.reconfigure(encoding="utf-8")
ru = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch\ru.json"
un = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch\untranslated.txt"

raw = io.open(ru, encoding="utf-8-sig").read()
ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
data = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

# ключи untranslated.txt — это готовые JSON-строки
keys_un = []
for line in io.open(un, encoding="utf-8", errors="replace"):
    s = line.strip()
    if not s.startswith('"'):
        continue
    lit = s[: s.rfind('": ""') + 1]
    try:
        keys_un.append(json.loads(lit))
    except Exception:
        pass

tested = 0
ok = 0
for k in keys_un:
    if k.startswith("\u2022 "):  # roadmap
        tested += 1
        hit = k in data
        ok += hit
        print("roadmap ключ:", "СОВПАЛ" if hit else "НЕ СОВПАЛ", "|", repr(k[:50]))
        if not hit:
            print("   ru  есть похожий:", [x[:50] for x in data if x.startswith("\u2022 ")][:3])

# остальные реальные тексты из экспорта
real = [k for k in keys_un if len(k) > 40 and not k.startswith("\u2022 ")]
print("\nдлинных не-roadmap строк в экспорте:", len(real))
for k in real[:15]:
    print("  ", "ПЕРЕВЕДЕНО" if k in data else "НЕТ", "|", repr(k[:70]))
print("\nитого roadmap:", ok, "/", tested)
