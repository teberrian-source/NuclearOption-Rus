# -*- coding: utf-8 -*-
"""Список реальных описаний (без kill-feed) + короткие текстовые кандидаты."""
import json, re, io, sys

sys.stdout.reconfigure(encoding="utf-8")
keys = [json.loads(l) for l in io.open(
    r"C:\Users\user\AppData\Local\Temp\lp_build\cand.jsonl", encoding="utf-8")]

FEED = (" intercepted ", " destroyed ", " shot down ", " demolished ",
        " was captured by ", " joined the game")

def is_feed(k):
    plain = re.sub(r"</?color=[^>]*>", "", k)
    return any(v in plain for v in FEED)

desc = [k for k in keys if len(k) >= 70 and not is_feed(k)]
print("===== ОПИСАНИЯ (не kill-feed), len>=70:", len(desc), "=====")
for i, k in enumerate(desc, 1):
    print(f"{i:3}. {k!r}")

# короткие текстовые: есть латинские слова, не числа, не kill-feed, не названия оружия/миссий
def is_junk(k):
    if not re.search(r"[A-Za-z]", k):
        return True
    s = re.sub(r"[<>?=/%:.,()\s\-$+0-9a-fA-F#]", "", k)
    if len(s) <= 2:
        return True
    return False

short = [k for k in keys if len(k) < 70 and not is_junk(k) and not is_feed(k)]
# убрать названия миссий и явные индейтифаторы
MISSION = re.compile(r"^(\[[A-Z0-9-]+\]|\d{2}\.)")
short = [k for k in short if not MISSION.match(k)]
print("\n===== КОРОТКИЕ ТЕКСТОВЫЕ:", len(short), "=====")
for i, k in enumerate(short, 1):
    print(f"{i:3}. {k!r}")
