# -*- coding: utf-8 -*-
"""Делит длинные untranslated-ключи на kill-feed и настоящие описания."""
import json, re, io, sys

sys.stdout.reconfigure(encoding="utf-8")
keys = [json.loads(l) for l in io.open(
    r"C:\Users\user\AppData\Local\Temp\lp_build\cand.jsonl", encoding="utf-8")]
long = [k for k in keys if len(k) >= 70]

FEED_VERBS = (" intercepted ", " destroyed ", " shot down ", " demolished ",
              " was captured by ", " joined the game")

feed, desc = [], []
for k in long:
    # kill-feed: содержит color-теги и глаголы событий, много \n-составных
    plain = re.sub(r"</?color=[^>]*>", "", k)
    if any(v in plain for v in FEED_VERBS) and plain.count("\n") >= 0 and len(plain) < 400:
        # отличие: события = "X <verb> Y" (короткие сегменты через \n)
        segs = plain.split("\n")
        if all(len(s) < 80 for s in segs):
            feed.append(k); continue
    desc.append(k)

print("kill-feed:", len(feed), "| описания/текст:", len(desc))
print("\n===== НАСТОЯЩИЕ ОПИСАНИЯ/ТЕКСТЫ =====")
for i, k in enumerate(desc, 1):
    print(f"--- {i}. len={len(k)}")
    print(repr(k))
