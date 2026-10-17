# -*- coding: utf-8 -*-
"""Поиск строк в BepInEx (моды/DLL) — байтовый поиск, без дампов плагина."""
import io, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
root = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx"
needles = [b"catapults of a Penumbra-class", b"Ingress Via Mountains", b"[FS-41] The Bigger They Are",
           b"Cursor-class LFD of BDF"]
skip = ("untranslated.txt", "extracted_strings.txt", "extracted_gamedata.txt", "LogOutput.log", "ru.json",
        ".backup_")

for dirpath, dirnames, filenames in os.walk(root):
    for fn in filenames:
        if any(s in fn for s in skip):
            continue
        p = os.path.join(dirpath, fn)
        try:
            if os.path.getsize(p) > 300 * 1024 * 1024:
                continue
            data = open(p, "rb").read()
        except OSError:
            continue
        hits = [n.decode() for n in needles if n in data]
        if hits:
            print(os.path.relpath(p, root), os.path.getsize(p), hits)
print("готово")
