# -*- coding: utf-8 -*-
"""Все объекты бандла MC-260, в данных которых есть "Radome": полный список строк."""
import io, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import UnityPy
UnityPy.config.FALLBACK_UNITY_VERSION = "2022.3.62f1"

b = r"C:\Users\user\AppData\Local\Temp\lp_build\unpack\Aryx_MC260_Chimera_1.2.0.dll.84708.unity3d"
env = UnityPy.load(b)
out = []
n = 0
for o in env.objects:
    try:
        raw = o.get_raw_data()
    except Exception:
        continue
    if b"Radome" not in raw and b"RADOME" not in raw:
        continue
    n += 1
    out.append("=" * 100)
    out.append(f"#{n} TYPE={o.type.name} size={len(raw)} path_id={o.path_id}")
    strs = [s.decode("ascii", "replace") for s in re.findall(rb"[ -~]{2,400}", raw)]
    out.append("   " + " | ".join(strs[:200]))
print(f"объектов с Radome: {n}\n")
io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\radome_objs.txt", "w", encoding="utf-8").write("\n".join(out))
for line in out:
    print(line[:1200])
