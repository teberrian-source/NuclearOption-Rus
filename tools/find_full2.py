# -*- coding: utf-8 -*-
"""Ищет полные тексты miss-строк в UTF-16 (DLL модов) и полный #12 в ассетах."""
import sys, os, re, glob

sys.stdout.reconfigure(encoding="utf-8")

QUERIES = [
    "Additional Boats",
    "Additional low-rank aircraft",
    "New large landlocked map",
    "What the fuck did you just",
    "This is how wide the text box",
    "Medium range heavy 203mm laser-guided rocket",
]

roots = [
    r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins",
    r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data",
]
files = []
for r0 in roots:
    for ext in ("*.dll", "*.assets", "*.resource", "*.nobp"):
        files += glob.glob(os.path.join(r0, "**", ext), recursive=True)

left = dict.fromkeys(QUERIES)
for f in files:
    if not left:
        break
    try:
        data = open(f, "rb").read()
    except Exception:
        continue
    for q in list(left):
        qb = q.encode("utf-16-le")
        i = data.find(qb)
        if i < 0:
            i = data.find(q.encode("ascii"))
            if i < 0:
                continue
            raw = data[i : i + 3000]
            text = raw.decode("ascii", "ignore")
        else:
            raw = data[i : i + 6000]
            text = raw.decode("utf-16-le", "ignore")
        # обрезаем по невалидные символы
        text = "".join(ch if (31 < ord(ch) < 0x110000 and ch not in "\ud800\ud801\ud802") else "\n" for ch in text)
        text = re.sub(r"[\x00-\x08\x0b-\x1f]+", " ", text)
        left.pop(q)
        print("=" * 70)
        print(f"ЗАПРОС: {q}\nФАЙЛ: {os.path.basename(f)}")
        print(text[:900])

for q in left:
    print("НЕ НАЙДЕН:", q)
