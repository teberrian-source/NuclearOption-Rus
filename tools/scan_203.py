# -*- coding: utf-8 -*-
"""Полный скан папки игры на '203mm' (без раннего выхода)."""
import sys, os, re

sys.stdout.reconfigure(encoding="utf-8")
root = r"C:\Users\user\Desktop\NuclearOption_0.34.2"
q = "203mm"
hits = []
scanned = 0
for dirpath, dirnames, filenames in os.walk(root):
    for name in filenames:
        p = os.path.join(dirpath, name)
        if os.path.basename(p) in ("LogOutput.log", "untranslated.txt", "Player.log"):
            continue
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
    txt = data[max(0, i - 400) : i + 800].decode(enc, "ignore")
    txt = re.sub(r"[\x00-\x08\x0b-\x1f]+", " | ", txt)
    print(txt)
