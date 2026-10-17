# -*- coding: utf-8 -*-
"""Только удалённые файлы нашего плагина (LocalizationPatch) + удаления после 19:30 сегодня."""
import os, sys, struct, datetime

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
        orig = data[28 : 28 + namelen * 2].decode("utf-16-le", "replace").rstrip("\x00")
    else:
        orig = data[24:].decode("utf-16-le", "replace").rstrip("\x00")
    return size, filetime_to_dt(ft), orig

rows = []
for drv in ("C:", "D:", "E:", "F:"):
    base = drv + "\\$Recycle.Bin"
    if not os.path.isdir(base):
        continue
    for sid in os.listdir(base):
        d = os.path.join(base, sid)
        try:
            files = os.listdir(d)
        except Exception:
            continue
        for f in files:
            if not f.startswith("$I"):
                continue
            try:
                info = parse_I(os.path.join(d, f))
            except Exception:
                continue
            if not info:
                continue
            size, dt, orig = info
            fresh = dt and dt >= datetime.datetime(2026, 10, 16, 19, 30)
            if "LocalizationPatch" in orig or fresh:
                r = os.path.join(d, "$R" + f[2:])
                rows.append((dt, size, os.path.getsize(r) if os.path.exists(r) else -1, orig, r))

rows.sort(key=lambda x: x[0] or datetime.datetime(1900, 1, 1), reverse=True)
print(f"найдено: {len(rows)}")
for dt, size, rsize, orig, r in rows:
    print(f"  удалён {dt:%d.%m %H:%M:%S} | было {size:>7} б | в корзине {rsize:>7} б")
    print(f"    {orig}")
