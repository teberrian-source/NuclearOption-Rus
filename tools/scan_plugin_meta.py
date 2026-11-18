# -*- coding: utf-8 -*-
"""Извлечение имён плагинов (BepInPlugin GUID/name/version) из DLL модов."""
import os, re, sys, glob

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BE = r"C:\Users\user\Desktop\Nuclear.Option.v0.34.6\BepInEx"
PLUGINS = os.path.join(BE, "plugins")

# GUID вида xxxxxxxx-xxxx-... в метаданных хранится как ASCII-строка
guid = re.compile(rb"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")
ascii_str = re.compile(rb"[\x20-\x7e]{4,80}")

targets = [
    "GroundControlRts", "KnockPush", "NOSMR", "NOX", "NavalPower",
    "NOCustomMaps", "NOMapLoader", "PlayableVehicles", "PlayableVehicles.dll",
    "Solar_Su30VXN", "aryx.f99", "aryx.fs41", "aryx.mc260", "aryx.rah72",
    "com.nikkorap.blueprinter",
]
for name in targets:
    p = os.path.join(PLUGINS, name)
    dlls = []
    if os.path.isfile(p) and p.lower().endswith(".dll"):
        dlls = [p]
    else:
        for root, dirs, files in os.walk(p):
            for f in files:
                if f.lower().endswith(".dll") and f.lower() not in ("baseclasses.dll",):
                    dlls.append(os.path.join(root, f))
    print("=" * 60)
    print("Мод:", name)
    for d in dlls[:3]:
        try:
            data = open(d, "rb").read()
        except Exception as e:
            print("   ?", d, e)
            continue
        # найти GUID, рядом (в пределах 200 байт) обычно лежат name/version
        found = set()
        for m in guid.finditer(data):
            seg = data[max(0, m.start() - 120): m.end() + 160]
            strs = [s.decode() for s in ascii_str.findall(seg)]
            strs = [s for s in strs if not re.fullmatch(r"[0-9a-fA-F\-]{36}", s)
                    and not s.startswith(("get_", "set_", "System", "Microsoft", "mscorlib", "BepInEx", "Unity", "Mono"))]
            for s in strs:
                if len(s) >= 4 and not s.endswith(".dll"):
                    found.add(s)
        print("  ", os.path.basename(d))
        for s in sorted(found)[:12]:
            print("     -", s)
