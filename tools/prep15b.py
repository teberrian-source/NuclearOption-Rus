# -*- coding: utf-8 -*-
"""Собирает пакет раунда 15: проза + короткие подписи, нумерует, пишет индекс."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
tmp = r"C:\Users\user\AppData\Local\Temp\lp_build"

# уже готовые (Ironjaw)
idx = json.load(io.open(tmp + r"\r15_index.json", encoding="utf-8"))
prose = io.open(tmp + r"\r15_prose.txt", encoding="utf-8").read()
labels = io.open(tmp + r"\r15_labels.txt", encoding="utf-8").read()

# проза из дампа плагина (длинные строки)
dump = io.open(tmp + r"\pending15.txt", encoding="utf-8").read().split("\n====\n")
long_dump = [e.strip() for e in dump if len(e.strip()) >= 110 and not e.startswith("<color=") and "CAPACITOR" not in e]
long_dump = sorted(set(long_dump))

# короткие подписи/кнопки/HUD (кураторский список)
SHORT = [
    "! DANGER - INCOMING MISSILE !", "MAIN ROTOR DAMAGE", "UPPER ROTOR FAILURE",
    "LOWER ROTOR FAILURE", "TAIL ROTOR FAIL", "L ENG FAIL", "R ENG FAIL",
    "VORTEX RING STATE", "REDUCE COLLECTIVE",
    "Next Camera", "Previous Camera", "Next Unit", "Previous Unit",
    "Select Unit Mode", "Rotate Unit Mode", "Translate Unit Mode",
    "Deploy Unit", "Deploy FOB", "Call Resupply", "Call Resupply - Player",
    "Objective Info", "Vote Kick Yes", "Vote Kick No", "Radar ECM",
    "Spot Vehicles", "Reveal Base", "Intercept Bomber", "Intercept Cruise Missiles",
    "Sink Enemy Carrier", "Locate Enemy Carrier", "Leave Combat Area",
    "Land at Naval Base", "Touch Down", "Take off", "Come to a stop",
    "Navigate Storm", "Neutralize Airfield", "Neutralize Artillery",
    "Neutralize Inlet Base", "Re-capture K92", "Rendezvous with ships",
    "Shoot Down Commander", "Return to Base", "Orbit Location", "Target Location",
    "Destroy Radar", "Destroy Radar Truck", "Destroy Shelter", "Destroy Depot",
    "Destroy Airfield", "Destroy AAA", "Destroy Launchers", "Destroy Trucks",
    "Destroy Target", "Destroy Targets", "Destroy Supply Point", "Destroy Fuel Stores",
    "Destroy Vehicle Depots", "Eliminate Depot", "Capture Airport", "Capture Depot",
    "Capture Supply Point", "Capture South Boscali", "Defend Bridge", "Defend bridge",
    "Defend Maris Airport", "Assist Attack on Airfield", "Destroy Neutral Shard 1",
    "Destroy Neutral Shard 2", "Upload Targets", "Use Airbakes", "PALA Troops Retreat",
]
SHORT = [s for s in SHORT if s in io.open(tmp + r"\pending15.txt", encoding="utf-8").read()]
existing = {m["en"] for m in idx.values()}
SHORT = [s for s in SHORT if s not in existing]

n = max(int(k) for k in idx)
out_p = [prose.rstrip()]
out_l = [labels.rstrip()]
for v in long_dump:
    if v in existing or any(m["en"] == v for m in idx.values()):
        continue
    n += 1
    idx[str(n)] = {"kind": "prose", "en": v}
    out_p.append(f"### {n}\n{v}\n")
for v in SHORT:
    n += 1
    idx[str(n)] = {"kind": "label", "en": v}
    out_l.append(f"### {n}\n{v}\n")

io.open(tmp + r"\r15_prose_all.txt", "w", encoding="utf-8", newline="\n").write("\n".join(out_p))
io.open(tmp + r"\r15_labels_all.txt", "w", encoding="utf-8", newline="\n").write("\n".join(out_l))
json.dump(idx, io.open(tmp + r"\r15_index.json", "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
kinds = {}
for m in idx.values():
    kinds[m["kind"]] = kinds.get(m["kind"], 0) + 1
print("всего записей:", len(idx), kinds)
print("проза (шт):", sum(1 for m in idx.values() if m["kind"] == "prose"),
      "| подписи:", sum(1 for m in idx.values() if m["kind"] == "label"))
print("добавлено длинных из дампа:", len(long_dump), "| коротких:", len(SHORT))
