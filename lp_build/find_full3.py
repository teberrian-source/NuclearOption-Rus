# -*- coding: utf-8 -*-
"""Точечный поиск фрагментов miss-строк по всем файлам папки игры."""
import sys, os, re, glob

sys.stdout.reconfigure(encoding="utf-8")

QUERIES = [
    "Additional Boats",
    "PALA Landing ship",
    "Ignus Archipelag",
    "low-rank aircraft",
    "landlocked map",
    "Navy Seals",
    "how wide the text box",
    "203mm laser-guided rocket",
]

root = r"C:\Users\user\Desktop\NuclearOption_0.34.2"
exts = ("*.dll", "*.assets", "*.resource", "*.json", "*.txt", "*.nobp", "*.cat", "*.bytes", "*.html")
files = []
for e in exts:
    files += glob.glob(os.path.join(root, "**", e), recursive=True)
print("файлов проверяется:", len(files))

left = dict.fromkeys(QUERIES)
for f in files:
    if not left:
        break
    try:
        data = open(f, "rb").read()
    except Exception:
        continue
    for q in list(left):
        i = data.find(q.encode())
        enc = "utf-8"
        if i < 0:
            i = data.find(q.encode("utf-16-le"))
            enc = "utf-16-le"
        if i < 0:
            continue
        raw = data[max(0, i - 200) : i + 2500]
        try:
            text = raw.decode(enc, "ignore")
        except Exception:
            continue
        text = re.sub(r"[\x00-\x08\x0b-\x1f]+", "\n", text)
        left.pop(q)
        print("=" * 70)
        print(f"ЗАПРОС: {q!r}  enc={enc}\nФАЙЛ: {f}")
        print(text[:1200])

for q in left:
    print("НЕ НАЙДЕН:", q)
