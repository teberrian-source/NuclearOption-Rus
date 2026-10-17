# -*- coding: utf-8 -*-
"""Поиск '203mm' во всех файлах папки игры (без фильтра по расширению) и Steam Workshop."""
import sys, os

sys.stdout.reconfigure(encoding="utf-8")

roots = [
    r"C:\Users\user\Desktop\NuclearOption_0.34.2",
    r"C:\Program Files (x86)\Steam\steamapps\workshop\content",
    r"C:\Program Files\Steam\steamapps\workshop\content",
]
QUERIES = ["203mm", "shaped charge warhead, best used"]
left = dict.fromkeys(QUERIES)
scanned = 0
for root in roots:
    if not os.path.isdir(root):
        print("нет:", root)
        continue
    for dirpath, dirnames, filenames in os.walk(root):
        for name in filenames:
            if not left:
                break
            p = os.path.join(dirpath, name)
            try:
                if os.path.getsize(p) > 500_000_000:
                    continue
                data = open(p, "rb").read()
            except Exception:
                continue
            scanned += 1
            for q in list(left):
                i = data.find(q.encode())
                enc = "utf-8"
                if i < 0:
                    i = data.find(q.encode("utf-16-le"))
                    enc = "utf-16-le"
                if i < 0:
                    continue
                left.pop(q)
                print("=" * 70)
                print(f"{q!r} enc={enc} ФАЙЛ: {p} (pos {i})")
                raw = data[max(0, i - 300) : i + 900]
                try:
                    txt = raw.decode(enc, "ignore")
                except Exception:
                    txt = str(raw[:600])
                import re
                txt = re.sub(r"[\x00-\x08\x0b-\x1f]+", " | ", txt)
                print(txt)
        if not left:
            break
    if not left:
        break

print("проверено файлов:", scanned)
for q in left:
    print("НЕ НАЙДЕН:", q)
