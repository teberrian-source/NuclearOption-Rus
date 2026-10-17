# -*- coding: utf-8 -*-
"""Скан Steam workshop и общих папок Steam на '203mm'."""
import sys, os, re, glob

sys.stdout.reconfigure(encoding="utf-8")

cands = []
for base in (r"C:\Program Files (x86)\Steam\steamapps", r"C:\Program Files\Steam\steamapps",
             r"D:\Steam\steamapps", r"D:\SteamLibrary\steamapps", r"E:\Steam\steamapps"):
    if os.path.isdir(base):
        cands.append(base)
        print("есть:", base)
if not cands:
    # найти Steam через реестр/шорткаты
    for p in glob.glob(r"C:\Program Files*\Steam\steamapps"):
        cands.append(p)
        print("есть:", p)

q = "203mm"
hits, scanned = [], 0
for base in cands:
    for dirpath, dirnames, filenames in os.walk(base):
        for name in filenames:
            p = os.path.join(dirpath, name)
            try:
                if os.path.getsize(p) > 600_000_000:
                    continue
                data = open(p, "rb").read()
            except Exception:
                continue
            scanned += 1
            for enc in ("utf-8", "utf-16-le"):
                i = data.find(q.encode(enc))
                if i >= 0:
                    hits.append((p, enc, i, data))
                    break

print("проверено:", scanned, " совпадений:", len(hits))
for p, enc, i, data in hits:
    print("=" * 70)
    print(f"ФАЙЛ: {p} enc={enc} pos={i}")
    txt = data[max(0, i - 300) : i + 700].decode(enc, "ignore")
    txt = re.sub(r"[\x00-\x08\x0b-\x1f]+", " | ", txt)
    print(txt)
