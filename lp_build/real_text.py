# -*- coding: utf-8 -*-
"""Извлекает только настоящие текстовые непереведённые строки (без чисел/мусора)."""
import sys, json, io, re
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
u = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch\untranslated.txt"

keys = []
for line in io.open(u, encoding="utf-8-sig").read().split("\n"):
    line = line.strip()
    if not line.startswith('"'):
        continue
    try:
        obj = json.loads("{" + line.rstrip(",") + "}")
    except Exception:
        continue
    keys.append(next(iter(obj)))

def strip_color(k):
    return re.sub(r"</?color=[^>]*>", "", k)

# настоящий текст: есть слово из 4+ букв
WORD = re.compile(r"[A-Za-zА-Яа-яЁё]{4,}")
# мусор: числа, дистанции, таймеры, миссии, внутренние имена
JUNK = re.compile(
    r"^[\d\s.,:+\-/><=%$()]*$"          # почти всё из цифр/символов
    r"|^\[?[A-Z]{2,4}-?\d*\]?\s+\w+$"    # [FS-41] Force Projection (миссии)
    r"|m/s$|/s$|km$|^\d{2}:\d{2}"        # скорости/дистанции/таймеры
    r"|_\d+$|^\(.*\)$"                   # internal names, скобки целиком
)

real = []
for k in keys:
    plain = strip_color(k)
    if not WORD.search(plain):
        continue
    # пропускаем строки, где все "слова" — на самом деле коды/числа
    words = [w for w in WORD.findall(plain) if len(w) >= 4]
    if not words:
        continue
    if JUNK.search(plain.strip()):
        continue
    real.append(k)

print("текстовых непереведённых:", len(real))
out = io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\real_text.jsonl", "w", encoding="utf-8")
for k in real:
    out.write(json.dumps(k, ensure_ascii=False) + "\n")
out.close()

seen = set()
n = 0
for k in real:
    kk = k[:90]
    if kk in seen:
        continue
    seen.add(kk)
    n += 1
    if n > 180:
        break
    print(f"{n:3}. {k[:150]!r}")
