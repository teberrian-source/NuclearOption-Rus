# -*- coding: utf-8 -*-
"""Точечный поиск описания 'Medium range heavy ...' по всей папке игры."""
import sys, os, re, glob

sys.stdout.reconfigure(encoding="utf-8")

QUERIES = [
    "Medium range heavy",
    "shaped charge warhead",
    "best used against heavily armoured",
]
root = r"C:\Users\user\Desktop\NuclearOption_0.34.2"
exts = ("*.dll", "*.assets", "*.resource", "*.json", "*.txt", "*.nobp", "*.cat", "*.bytes")
files = []
for e in exts:
    files += glob.glob(os.path.join(root, "**", e), recursive=True)
print("файлов:", len(files))

left = dict.fromkeys(QUERIES)
for f in files:
    if not left:
        break
    try:
        data = open(f, "rb").read()
    except Exception:
        continue
    for q in list(left):
        for enc in ("utf-8", "utf-16-le"):
            i = data.find(q.encode(enc))
            if i >= 0:
                break
        if i < 0:
            continue
        raw = data[max(0, i - 300) : i + 1500]
        text = raw.decode(enc, "ignore")
        text = re.sub(r"[\x00-\x08\x0b-\x1f]+", "\n", text)
        left.pop(q)
        print("=" * 70)
        print(f"ЗАПРОС: {q!r} enc={enc}\nФАЙЛ: {f}")
        print(text[:1300])

for q in left:
    print("НЕ НАЙДЕН:", q)
