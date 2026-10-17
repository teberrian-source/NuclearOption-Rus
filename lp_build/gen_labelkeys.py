# -*- coding: utf-8 -*-
"""Генерирует новый блок LabelWithValueKeys для Plugin.cs (имена точек/задач)."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
tmp = r"C:\Users\user\AppData\Local\Temp\lp_build"
idx = json.load(io.open(tmp + r"\r15_index.json", encoding="utf-8"))

HUD_UI = {
    "! DANGER - INCOMING MISSILE !", "MAIN ROTOR DAMAGE", "UPPER ROTOR FAILURE",
    "LOWER ROTOR FAILURE", "TAIL ROTOR FAIL", "L ENG FAIL", "R ENG FAIL",
    "VORTEX RING STATE", "REDUCE COLLECTIVE", "Next Camera", "Previous Camera",
    "Next Unit", "Previous Unit", "Select Unit Mode", "Rotate Unit Mode",
    "Translate Unit Mode", "Deploy Unit", "Deploy FOB", "Call Resupply",
    "Call Resupply - Player", "Objective Info", "Vote Kick Yes", "Vote Kick No", "Radar ECM",
}

base = ["Return To Base", "Search For Convoy", "Break Blockade", "Defend Island",
        "Destroy Vehicles", "Detected units", "Repaired unit", "Take Off", "Taxi",
        "Taxi to Runway", "Cleared for landing on Runway", "Cleared to taxi to Runway",
        "Successful Sortie +"]
names = [m["en"] for m in idx.values() if m["kind"] == "label" and m["en"] not in HUD_UI]
allk = base + sorted(set(names))
print("всего в белом списке:", len(allk))

lines = []
cur = "\t\t"
for k in allk:
    item = json.dumps(k, ensure_ascii=False) + ", "
    if len(cur) + len(item) > 100:
        lines.append(cur.rstrip())
        cur = "\t\t"
    cur += item
lines.append(cur.rstrip().rstrip(","))
block = ("\tprivate static readonly HashSet<string> LabelWithValueKeys = new HashSet<string>\n\t{\n"
         + "\n".join(lines) + "\n\t};")
io.open(tmp + r"\label_keys.txt", "w", encoding="utf-8", newline="\r\n").write(block)
print("готово -> label_keys.txt, строк:", len(lines))
