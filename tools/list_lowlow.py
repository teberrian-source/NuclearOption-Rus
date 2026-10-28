# -*- coding: utf-8 -*-
"""Содержимое LocalLow\\Shockfront\\NuclearOption (файлы сохранений/конфигов Rewired)."""
import io, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host = r"C:\Users\user\AppData\LocalLow\Shockfront\NuclearOption"
out = []
if not os.path.isdir(host):
    out.append("нет папки: " + host)
else:
    for base, dirs, fs in os.walk(host):
        rel = os.path.relpath(base, host)
        out.append("[папка] " + rel + " (" + str(len(fs)) + " файлов)")
        for f in sorted(fs):
            p = os.path.join(base, f)
            out.append("   %9d  %s" % (os.path.getsize(p), f))
with open(os.environ["TEMP"] + "\\low.txt", "w", encoding="utf-8", newline="\n") as f2:
    f2.write("\n".join(out) + "\n")
print("ok, записей:", len(out))
