# -*- coding: utf-8 -*-
"""Контексты всех вхождений "Radome" в бандле MC-260 (ищем определение юнита)."""
import io, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import UnityPy
UnityPy.config.FALLBACK_UNITY_VERSION = "2022.3.62f1"

b = r"C:\Users\user\AppData\Local\Temp\lp_build\unpack\Aryx_MC260_Chimera_1.2.0.dll.84708.unity3d"
env = UnityPy.load(b)
lines = []
for o in env.objects:
    try:
        raw = o.get_raw_data()
    except Exception:
        continue
    idxs = [m.start() for m in re.finditer(rb"[Rr]adome", raw)]
    if not idxs:
        continue
    lines.append(f"===== TYPE={o.type.name} size={len(raw)} вхождений={len(idxs)}")
    for i in idxs[:25]:
        chunk = raw[max(0, i - 500): i + 900]
        txt = "".join(chr(c) if 32 <= c < 127 else ("\n" if c == 10 else ".") for c in chunk)
        txt = re.sub(r"\.{3,}", "…", txt)
        lines.append(f"  @{i}: …{txt}…")
    lines.append("")
io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\radome_ctx.txt", "w", encoding="utf-8").write("\n".join(lines))
print("\n".join(lines)[:12000])
