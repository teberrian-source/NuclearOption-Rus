# -*- coding: utf-8 -*-
"""Через UnityPy ищет в resources.assets объекты с подписями слотов и печатает их строки."""
import io, re, sys

sys.stdout.reconfigure(encoding="utf-8")
import UnityPy

p = r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data\resources.assets"
env = UnityPy.load(p)
needles = [b"turret mount", b"Point Defense", b"subturret", b"Ammo box", b"Truck bed"]
print("objects:", len(env.objects))
for obj in env.objects:
    try:
        raw = obj.get_raw_data()
    except Exception as e:
        continue
    if not any(n in raw for n in needles):
        continue
    print("=" * 100)
    print("TYPE:", obj.type.name, "path_id:", obj.path_id, "size:", len(raw))
    strs = re.findall(rb"[ -~]{3,}", raw)
    out = [s.decode("ascii", "replace") for s in strs]
    for s in out:
        print("   |", s)
