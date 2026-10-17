# -*- coding: utf-8 -*-
"""Читает Корзину Windows: $I-файлы содержат исходный путь, $R-файлы — сами данные."""
import os, sys, glob, struct, datetime

sys.stdout.reconfigure(encoding="utf-8")

def filetime_to_dt(v):
    try:
        return datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=v // 10)
    except Exception:
        return None

def parse_I(path):
    data = open(path, "rb").read()
    if len(data) < 24:
        return None
    size = struct.unpack("<Q", data[8:16])[0]
    ft = struct.unpack("<Q", data[16:24])[0]
    version = struct.unpack("<Q", data[0:8])[0]
    if version >= 2 and len(data) >= 28:
        namelen = struct.unpack("<I", data[24:28])[0]
        raw = data[28 : 28 + namelen * 2]
        orig = raw.decode("utf-16-le", "replace").rstrip("\x00")
    else:
        orig = data[24:].decode("utf-16-le", "replace").rstrip("\x00")
    return size, filetime_to_dt(ft), orig, version

rows = []
for drv in ("C:", "D:", "E:"):
    base = drv + "\\$Recycle.Bin"
    if not os.path.isdir(base):
        continue
    for sid in os.listdir(base):
        d = os.path.join(base, sid)
        if not os.path.isdir(d):
            continue
        try:
            files = os.listdir(d)
        except PermissionError:
            continue
        for f in files:
            if not f.startswith("$I"):
                continue
            p = os.path.join(d, f)
            try:
                info = parse_I(p)
            except Exception:
                continue
            if not info:
                continue
            size, dt, orig, ver = info
            if "NuclearOption" in orig or "Localization" in orig or "ru.json" in orig.lower():
                r = os.path.join(d, "$R" + f[2:])
                rsize = os.path.getsize(r) if os.path.exists(r) else -1
                rows.append((dt, size, rsize, orig, r))

rows.sort(key=lambda x: x[0] or datetime.datetime(1900, 1, 1), reverse=True)
print(f"найдено в Корзине (по нашей игре): {len(rows)}")
for dt, size, rsize, orig, r in rows:
    print(f"  удалён {dt:%d.%m %H:%M:%S}  было {size:>8} б  в корзине {rsize:>8} б  {orig}")
    print(f"        $R: {r}")
