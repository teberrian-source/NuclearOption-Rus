# -*- coding: utf-8 -*-
"""Распаковывает gzip-потоки внутри модовой сборки и ищет подписи слотов."""
import io, os, re, sys, zlib

sys.stdout.reconfigure(encoding="utf-8")
p = sys.argv[1]
needles = [b"subturret", b"Ammo box", b"Truck bed", b"cargo 2x", b"(KAR)", b"Main Turret", b"Point Defense"]
data = io.open(p, "rb").read()
print("file:", p, len(data))
offs = [m.start() for m in re.finditer(b"\x1f\x8b\x08", data)]
print("gzip-потоков:", len(offs))
outdir = r"C:\Users\user\AppData\Local\Temp\lp_build\unpack"
os.makedirs(outdir, exist_ok=True)
total = 0
for k, off in enumerate(offs):
    try:
        d = zlib.decompressobj(31)
        raw = d.decompress(data[off:])
        raw += d.flush()
    except Exception:
        continue
    total += len(raw)
    if any(n in raw for n in needles):
        print("HIT в потоке", k, "@", off, "размер", len(raw))
        for n in needles:
            c = raw.count(n)
            if c:
                print("   ", n.decode(), "x", c)
        fn = os.path.join(outdir, f"stream_{k}_{off}.bin")
        io.open(fn, "wb").write(raw)
        print("   ->", fn)
        for n in needles:
            for m in list(re.finditer(re.escape(n), raw))[:3]:
                s = m.start()
                chunk = raw[max(0, s - 200):s + 200]
                txt = "".join(chr(c) if 32 <= c < 127 else "." for c in chunk)
                print("      ...", txt)
print("распаковано всего байт:", total)
