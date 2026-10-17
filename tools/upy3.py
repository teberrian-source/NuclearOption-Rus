# -*- coding: utf-8 -*-
"""UnityPy с явной версией Unity: ищет подписи хардпоинтов и модовые юниты в бандлах."""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
UnityPy.config.FALLBACK_UNITY_VERSION = "2022.3.62f1"

path = sys.argv[1]
needles = [b"subturret", b"Ammo box", b"Truck bed", b"cargo 2x", b"(KAR)", b"AFV8", b"Linebreaker", b"Cargo Bay", b"turret mount"]
env = UnityPy.load(path)
objs = list(env.objects)
print("objects:", len(objs))
err = 0
hits = 0
for o in objs:
    try:
        raw = o.get_raw_data()
    except Exception:
        err += 1
        continue
    if any(n in raw for n in needles):
        hits += 1
        print("=" * 90)
        print("TYPE", o.type.name, "path_id", o.path_id, "size", len(raw))
        for s in re.findall(rb"[ -~]{3,}", raw)[:500]:
            print("   |", s.decode("ascii", "replace")[:200])
print("errors:", err, "hits:", hits)
