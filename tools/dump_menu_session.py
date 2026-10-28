# -*- coding: utf-8 -*-
"""Точный дамп строк [TRACE] вокруг меню управления новой сессии + последняя выгрузка untranslated."""
import io, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
LOG = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\LogOutput.log"
lines = io.open(LOG, encoding="utf-8", errors="replace").read().split("\n")

out = ["=== лог: строки 1100-1310 (сессия v3.3.2) ===", ""]
for i in range(1099, min(1310, len(lines))):
    l = lines[i].strip()
    if l and ("[TRACE]" in l or "Localization Patch v" in l):
        out.append("%5d | %s" % (i + 1, l.lstrip("[Info   :Localization Patch] ")))

out.append("")
out.append("=== untranslated.txt: строки с кириллицей (двойные записи игры) ===")
try:
    u = io.open(r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch\untranslated.txt",
                encoding="utf-8", errors="replace").read()
    cyr = [l for l in u.split("\n") if re.search(r"[А-Яа-яЁё]", l)]
    out.append("строк с кириллицей: %d" % len(cyr))
    out.extend("  " + s for s in cyr[:120])
except Exception as e:
    out.append("нет файла: " + str(e))

with open(io.os.environ["TEMP"] + "\\dump.txt", "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(out) + "\n")
print("ok")
