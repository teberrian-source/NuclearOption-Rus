# -*- coding: utf-8 -*-
"""UnityPy: распаковывает бандл/файл и ищет подписи хардпоинтов в объектах (с подсчётом ошибок)."""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
import UnityPy

path = sys.argv[1]
needles = [b"subturret", b"Ammo box", b"Truck bed", b"cargo 2x", b"turret mount", b"Turret mount", b"Cargo Bay"]
env = UnityPy.load(path)
objs = list(env.objects)
print("objects:", len(objs))
err = 0
hits = 0
for o in objs:
    try:
        raw = o.get_raw_data()
    except Exception as e:
        err += 1
        continue
    if any(n in raw for n in needles):
        hits += 1
        print("=" * 90)
        print("TYPE", o.type.name, "path_id", o.path_id, "size", len(raw))
        for s in re.findall(rb"[ -~]{3,}", raw)[:400]:
            print("   |", s.decode("ascii", "replace")[:160])
print("errors:", err, "hits:", hits)
