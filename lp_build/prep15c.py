# -*- coding: utf-8 -*-
"""Отбирает показываемые имена целей/точек базовых миссий для перевода."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
tmp = r"C:\Users\user\AppData\Local\Temp\lp_build"
cand = [l for l in io.open(tmp + r"\wpt_cand.txt", encoding="utf-8").read().split("\n") if l.strip()]

# служебные идентификаторы (в игре игроку не показываются)
bad = re.compile(
    r"^(Box|box|wait|Wait|close|final|spot|started|not |waypoint|Message|Reinf|Veh\d|SS\d|Corvette|Shard|"
    r"Weather|CaptureMessage|_|PALA_|BDF_|Fail Condition|Tutorial)"
    r"|Delay$|Spawn|Timer$|Behaviour|Move$|Lost$|Conditions$|Alert$|_|Location$"
)
keep, skip = [], []
for v in cand:
    if bad.search(v):
        skip.append(v)
        continue
    if v in ("Hyperion Class Carrier", "Annex Class Carrier", "Maris Heliport", "Ravine Beach",
             "The Farm", "Southgate Plaza", "City Airport", "Camp Westpoint", "Agrapol City Supply Point",
             "North Coast Enrichment Plant", "South Coast Enrichment Plant", "Bridgehead Operations Base"):
        skip.append(v)
        continue
    keep.append(v)
keep = sorted(set(keep))
io.open(tmp + r"\r15b_labels.txt", "w", encoding="utf-8", newline="\n").write("\n".join(keep))
print("к переводу:", len(keep))
print("пропущено:", len(skip))
for v in keep:
    print("  ", v)
