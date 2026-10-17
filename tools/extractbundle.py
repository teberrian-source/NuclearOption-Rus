# -*- coding: utf-8 -*-
"""Извлекает встроенный UnityFS-бандл из модовой сборки по заголовку и ищет в нём подписи."""
import io, os, re, struct, sys

sys.stdout.reconfigure(encoding="utf-8")
p = sys.argv[1]
outdir = r"C:\Users\user\AppData\Local\Temp\lp_build\unpack"
os.makedirs(outdir, exist_ok=True)
data = io.open(p, "rb").read()
print("file:", p, len(data))
for m in re.finditer(b"UnityFS\x00", data):
    off = m.start()
    try:
        pos = off + 8
        version = struct.unpack_from(">i", data, pos)[0]; pos += 4
        # строки с выравниванием
        def rdstr(pos):
            end = data.index(b"\x00", pos)
            return data[pos:end].decode("latin1"), end + 1
        unityver, pos = rdstr(pos)
        # выравнивание до 4
        pos = (pos + 3) & ~3
        unityrev, pos = rdstr(pos)
        pos = (pos + 3) & ~3
        size, = struct.unpack_from(">q", data, pos)
        print("  бандл @", off, "version", version, "unity", unityver, "rev", unityrev, "size", size)
        blob = data[off:off + size] if size > 0 else data[off:]
        if size <= 0 or len(blob) > 200 * 1024 * 1024:
            blob = data[off:]
        fn = os.path.join(outdir, f"bundle_{os.path.basename(p)}_{off}.unity3d")
        io.open(fn, "wb").write(blob)
        print("  ->", fn, len(blob), "байт")
    except Exception as e:
        print("  ошибка разбора @", off, e)
