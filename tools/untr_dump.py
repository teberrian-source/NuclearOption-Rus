# -*- coding: utf-8 -*-
"""Печатает untranslated.txt целиком (без мусора), чтобы выбрать остатки для перевода."""
import io, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch\untranslated.txt"
lines = [l.rstrip("\n") for l in io.open(p, encoding="utf-8", errors="replace") if l.strip()]
print("всего строк:", len(lines))
CYR = re.compile(r"[А-Яа-яЁё]")
skip = re.compile(r"^(?:[A-Za-z0-9_'{}\[\]().,:;/\\|+\-*%$#@!?=<>~^`\u0400-\u04FF ]{0,3})$")
print("\n--- КАНДИДАТЫ (английский, не ники/числа) ---")
i = 0
for l in lines:
    i += 1
    t = l.strip()
    if CYR.search(t):
        continue
    if len(t) < 4:
        continue
    if re.fullmatch(r"[\w\-. ]{1,16}", t) and not t[0].isupper():
        continue
    print(f"{i:4d} | {t[:170]}")
