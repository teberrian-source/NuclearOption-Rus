# -*- coding: utf-8 -*-
import io, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
files = ["untranslated.txt", "extracted_strings.txt", "extracted_gamedata.txt"]
KEYS = ["RADAR", "Radar", "MBT", "AA", "ЗА", "ОБТ", "РАДАР", "Radome"]
for f in files:
    try:
        d = io.open(f, encoding="utf-8", errors="replace").read()
    except Exception as e:
        print(f, "НЕТ", e)
        continue
    print("=== " + f, len(d))
    for k in KEYS:
        n = d.count(k)
        print(f"   {k!r}: {n}")
        for m in list(re.finditer(re.escape(k), d))[:3]:
            s = re.sub(r"\s+", " ", d[max(0, m.start() - 60):m.end() + 60])
            print("      …" + s + "…")
