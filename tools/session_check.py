# -*- coding: utf-8 -*-
"""Свежая сессия: версия плагина, блок меню управления (hits/misses), порядок строк."""
import io, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
LOG = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\LogOutput.log"
lines = io.open(LOG, encoding="utf-8", errors="replace").read().split("\n")
print("строк в логе:", len(lines))
print()
print("=== версии плагина ===")
for i, l in enumerate(lines):
    if "Localization Patch v" in l:
        print("%6d | %s" % (i + 1, l.strip()[:130]))
print()
# найдём все трассировки
tr = [(i, "hit" if "hit:" in l else "miss", l.split('"')[1] if '"' in l else l.strip())
      for i, l in enumerate(lines) if "[TRACE]" in l]
print("всего трассировок:", len(tr))
# интервалы подряд hits/misses
print("=== точки смены hit/miss (границы блоков) ===")
prev = None
for k, (i, kind, s) in enumerate(tr):
    if kind != prev:
        print("%6d | смена на %s | %s" % (i + 1, kind, s[:60]))
        prev = kind
