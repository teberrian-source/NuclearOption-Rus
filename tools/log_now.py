# -*- coding: utf-8 -*-
"""Свежие строки лога: версии плагина, Rewired-предупреждения, последние события сессии."""
import io, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
LOG = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\LogOutput.log"
lines = io.open(LOG, encoding="utf-8", errors="replace").read().split("\n")
out = ["всего строк: %d" % len(lines), ""]
out.append("=== версия плагина ===")
for i, l in enumerate(lines):
    if "Localization Patch v" in l:
        out.append("%5d | %s" % (i + 1, l.strip()[:130]))
out.append("")
out.append("=== Rewired / ошибки / предупреждения за сессию ===")
for i, l in enumerate(lines):
    s = l.strip()
    if "[Error" in s or "[Warning" in s or "Rewired" in s:
        out.append("%5d | %s" % (i + 1, s[:160]))
out.append("")
out.append("=== последние 30 непустых строк ===")
k = 0
for i in range(len(lines) - 1, -1, -1):
    s = lines[i].strip()
    if s:
        out.append("%5d | %s" % (i + 1, s[:160]))
        k += 1
        if k >= 30:
            break
with open(os.environ["TEMP"] + "\\log_now.txt", "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(out) + "\n")
print("ok")
