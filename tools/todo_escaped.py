# -*- coding: utf-8 -*-
"""Печатает todo.json в виде: индекс|JSON-строка (для точного копирования переводов)."""
import io, json, sys
sys.stdout.reconfigure(encoding="utf-8")
items = json.loads(io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\todo.json", encoding="utf-8").read())
out = []
for it in items:
    out.append(f"{it['i']}|{it['group']}|{json.dumps(it['en'], ensure_ascii=False)}")
io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\todo_escaped.txt", "w", encoding="utf-8").write("\n".join(out))
print("строк:", len(out))
