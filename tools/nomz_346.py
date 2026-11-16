# -*- coding: utf-8 -*-
"""Разбор контейнера cascadia-0.1.0.nomapz (NOMZ) и поиск полного описания миссии."""
import io, os, sys, zlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
MAPZ = os.path.join(os.environ["USERPROFILE"], "Desktop", "Nuclear.Option.v0.34.6",
                    "BepInEx", "plugins", "NOCustomMaps", "maps", "cascadia-0.1.0.nomapz")
b = open(MAPZ, "rb").read()
print("размер:", len(b))
print("первые 64 байта:", b[:64].hex(" "))
print("заголовок текстом:", b[4:32])

# попытка zlib с разных смещений
for off in (8, 12, 16, 20, 24, 32):
    try:
        d = zlib.decompressobj()
        out = d.decompress(b[off:])
        print(f"zlib@{off}: OK, {len(out)} байт, начало: {out[:60]!r}")
        outpath = os.path.join(os.path.dirname(MAPZ), "_cascadia_extract.bin")
        open(outpath, "wb").write(out)
        print("сохранено:", outpath)
        break
    except Exception as e:
        print(f"zlib@{off}: {type(e).__name__}")
