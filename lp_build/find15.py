# -*- coding: utf-8 -*-
"""Ищем файл со строкой описания миссии в профиле пользователя."""
import io, os, sys, time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
roots = [r"C:\Users\user\AppData\LocalLow", r"C:\Users\user\AppData\Local\Steam",
         r"C:\Users\user\AppData\Roaming\Steam", r"C:\Users\user\Documents",
         r"C:\Users\user\Desktop\NuclearOption_0.34.2\FreeTP"]
needles = [b"catapults of a Penumbra-class", b"Ingress Via Mountains", b"Ironjaw Sound - Sill Strike"]
t0 = time.time()
scanned = 0
for root in roots:
    if not os.path.isdir(root):
        print("нет папки:", root)
        continue
    for dirpath, dirnames, filenames in os.walk(root):
        if time.time() - t0 > 240:
            print("таймаут поиска")
            sys.exit(0)
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            try:
                sz = os.path.getsize(p)
                if sz == 0 or sz > 200 * 1024 * 1024:
                    continue
                data = open(p, "rb").read()
            except OSError:
                continue
            scanned += 1
            hits = [n.decode() for n in needles if n in data]
            if hits:
                print("НАЙДЕНО:", p, hits)
    print("просканировано файлов:", scanned, "| %.0f с" % (time.time() - t0))
print("готово, файлов:", scanned)
