# -*- coding: utf-8 -*-
"""Потоковый поиск строки в больших файлах игры (.resS и др.)."""
import io, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
root = r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data"
needles = [b"catapults of a Penumbra-class", b"Ingress Via Mountains", b"[FS-41] The Bigger They Are"]
CH = 8 * 1024 * 1024

for dirpath, dirnames, filenames in os.walk(root):
    for fn in filenames:
        p = os.path.join(dirpath, fn)
        sz = os.path.getsize(p)
        if sz < 5 * 1024 * 1024:
            continue
        found = {n: 0 for n in needles}
        prev = b""
        with open(p, "rb") as f:
            while True:
                buf = f.read(CH)
                if not buf:
                    break
                data = prev + buf
                for n in needles:
                    found[n] += data.count(n)
                prev = data[-64:]
        if any(found.values()):
            print(os.path.relpath(p, root), sz, {k.decode(): v for k, v in found.items() if v})
print("готово")
