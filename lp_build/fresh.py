# -*- coding: utf-8 -*-
"""Свежие кандидаты на перевод: длинные описания + короткие текстовые (без чисел/kill-feed)."""
import json, re, io, sys

base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
sys.stdout.reconfigure(encoding="utf-8")

# ключи untranslated
keys = []
for line in io.open(base + r"\untranslated.txt", encoding="utf-8-sig").read().split("\n"):
    line = line.strip()
    if not line.startswith('"'):
        continue
    try:
        obj = json.loads("{" + line.rstrip(",") + "}")
    except Exception:
        continue
    keys.append(next(iter(obj)))

# уже переведённые ключи ru.json
raw = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)
print("непереведённых ключей:", len(keys), "| в ru.json:", len(ru))

FEED = (" intercepted ", " destroyed ", " shot down ", " demolished ",
        " was captured by ", " sank ", " joined the game")

def is_feed(k):
    plain = re.sub(r"</?color=[^>]*>", "", k)
    return any(v in plain for v in FEED)

def is_numeric(k):
    s = re.sub(r"</?color=[^>]*>", "", k)
    s = re.sub(r"[<>?=/%:.,()\s\-$+0-9a-zA-Z#Ω°]+", "", s)
    return len(s.strip()) <= 1

cand = []
for k in keys:
    if k in ru:
        continue  # уже переведён (просто не совпал ключ в игре? нет — это untranslated значит miss)
    if is_feed(k) or is_numeric(k):
        continue
    if not re.search(r"[A-Za-z]", k):
        continue
    cand.append(k)

# разделить на длинные (описания) и короткие
long = [k for k in cand if len(k) >= 70]
short = [k for k in cand if len(k) < 70]
print("описаний:", len(long), "| коротких:", len(short))

out = io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\cand2.jsonl", "w", encoding="utf-8")
for k in cand:
    out.write(json.dumps(k, ensure_ascii=False) + "\n")
out.close()

print("\n===== ОПИСАНИЯ =====")
for i, k in enumerate(long, 1):
    print(f"{i:3}. {k!r}")
print("\n===== КОРОТКИЕ (первые 200) =====")
for i, k in enumerate(short[:200], 1):
    print(f"{i:3}. {k!r}")
