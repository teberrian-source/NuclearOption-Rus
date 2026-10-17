# -*- coding: utf-8 -*-
"""Извлекает текстовые строки-предложения из resources.assets и levelN (описания/брифинги миссий)."""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
root = r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data"
files = ["resources.assets", "level0", "level1", "level2", "level3", "level4", "level5"]
split_re = re.compile(rb"[\x00-\x08\x0B-\x1F\x7F]+")

allowed = re.compile(r"^[A-Za-z0-9 ,.'!?\-:;()/&%+°\[\]\u2019\u2014\u2026\u00b0]+$")

out = {}
for fn in files:
    p = os.path.join(root, fn)
    if not os.path.exists(p):
        continue
    data = open(p, "rb").read()
    found = set()
    for chunk in split_re.split(data):
        if len(chunk) < 25 or len(chunk) > 2000:
            continue
        try:
            s = chunk.decode("utf-8")
        except UnicodeDecodeError:
            continue
        s = s.strip()
        if not allowed.match(s):
            continue
        words = re.findall(r"[A-Za-z']{2,}", s)
        if len(words) < 6:
            continue
        if "<color=" in s or s.startswith("http") or "@" in s:
            continue
        found.add(s)
    out[fn] = sorted(found)
    print(fn, "->", len(found))

with io.open("game_text_cand.txt", "w", encoding="utf-8", newline="\n") as f:
    for fn, items in out.items():
        f.write("#### " + fn + "\n")
        for s in items:
            f.write(s + "\n====\n")
print("всего:", sum(len(v) for v in out.values()))
