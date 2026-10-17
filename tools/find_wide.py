# -*- coding: utf-8 -*-
"""Широкий поиск '203mm'/'Medium range heavy' в AppData/LocalLow, Documents, Steam."""
import sys, os, glob

sys.stdout.reconfigure(encoding="utf-8")

roots = [
    r"C:\Users\user\AppData\LocalLow",
    r"C:\Users\user\Documents",
]
QUERIES = ["203mm", "Medium range heavy", "laser-guided rocket"]
left = dict.fromkeys(QUERIES)
scanned = 0
for root in roots:
    for dirpath, dirnames, filenames in os.walk(root):
        for name in filenames:
            if not left:
                break
            p = os.path.join(dirpath, name)
            try:
                if os.path.getsize(p) > 400_000_000:
                    continue
                data = open(p, "rb").read()
            except Exception:
                continue
            scanned += 1
            for q in list(left):
                for enc in ("utf-8", "utf-16-le"):
                    i = data.find(q.encode(enc))
                    if i >= 0:
                        break
                if i < 0:
                    continue
                left.pop(q)
                print("=" * 70)
                print(f"{q!r} enc={enc} ФАЙЛ: {p}")
        if not left:
            break
    if not left:
        break

print("проверено файлов:", scanned)
for q in left:
    print("НЕ НАЙДЕН:", q)
