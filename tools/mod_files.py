# -*- coding: utf-8 -*-
"""Ищет крупные файлы модов и смотрит их заголовки (bundle/zip/compressed)."""
import sys, os

sys.stdout.reconfigure(encoding="utf-8")
root = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins"
rows = []
for dirpath, dirnames, filenames in os.walk(root):
    for name in filenames:
        p = os.path.join(dirpath, name)
        try:
            sz = os.path.getsize(p)
        except Exception:
            continue
        if sz > 1_000_000:
            head = open(p, "rb").read(16)
            rows.append((sz, os.path.relpath(p, root), head))
rows.sort(reverse=True)
print(f"крупных файлов: {len(rows)}")
for sz, rel, head in rows[:40]:
    printable = "".join(chr(b) if 32 <= b < 127 else "." for b in head)
    print(f"{sz/1048576:8.1f} МБ  {rel[:62]:<62} {printable}")
