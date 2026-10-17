# -*- coding: utf-8 -*-
"""Разбирает missing_descriptions.json: категории и печать."""
import io, json, re, sys

sys.stdout.reconfigure(encoding="utf-8")
d = json.load(io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\missing_descriptions.json", encoding="utf-8"))
print("всего:", len(d))

csv_rows, json_frags, plain = [], [], []
for t, src in d.items():
    if ";" in t:
        csv_rows.append((t, src))
    elif t.lstrip().startswith('"') or t.lstrip().startswith("}"):
        json_frags.append((t, src))
    else:
        plain.append((t, src))
print("CSV-строки:", len(csv_rows), "| JSON-фрагменты:", len(json_frags), "| обычный текст:", len(plain))

print("\n===== ОБЫЧНЫЙ ТЕКСТ =====")
for t, src in sorted(plain):
    print(f"| {t[:190]}   <{','.join(s[:22] for s in src)}>")
