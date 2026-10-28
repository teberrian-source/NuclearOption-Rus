# -*- coding: utf-8 -*-
"""Собирает [TRACE] hit-строки из LogOutput.log в файл (для списка строк меню управления)."""
import io, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SRC = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\LogOutput.log"
DST = r"C:\Users\user\AppData\Local\Temp\hits.txt"

lines = io.open(SRC, encoding="utf-8", errors="replace").read().split("\n")
hits = []
for i, l in enumerate(lines, 1):
    m = re.search(r"\[TRACE\] hit: \"(.*)\"$", l.strip())
    if m:
        hits.append((i, m.group(1)))
out = ["всего hit-строк: %d" % len(hits), ""]
out.append("=== hit-строки 800-1049 ===")
for i, s in hits:
    if 800 <= i <= 1049:
        out.append("%5d | %s" % (i, s))
io.open(DST, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("ok, строк:", len(hits))
