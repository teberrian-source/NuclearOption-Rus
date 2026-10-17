# -*- coding: utf-8 -*-
"""Проверяет, какие подписи слотов уже есть в ru.json (моды + игра)."""
import io, json, re, sys

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

def parse_json(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse_json(base + r"\ru.json")

cands = [
    # KAR
    "Ammo Box", "Ammo box", "Cargo", "Cargo 2x", "cargo", "cargo 2x", "Gun", "Launchers",
    "Left Pylon", "Right Pylon", "Main Turret", "Point Defence", "Point Defense", "Roof Mount",
    "roof mount", "roof turret", "The Device", "Truck bed", "Turret", "Vehicle Cargo",
    "coax", "subturret", "subturret (H)", "subturrets", "tow hook", "turret mount",
    # Aryx / боты
    "Bomb Bay (2x)", "Cargo Bay Front", "Cargo Bay Rear", "Centreline Pylon", "Forward Weapon Bay",
    "Front Turret", "Gun Mount", "Heater Bays", "Infantry", "Inner L Bay", "Inner Left Pylon",
    "Inner R Bay", "Inner Right Pylon", "Inner Weapon Bays", "Inner Wing Pylons", "Internal Bays",
    "Internal Cannon", "Internal Gun", "Internal Guns", "Left Bay", "Left Internal Bay",
    "Mid Wing Pylons", "Mission Bay", "Outer L Bay", "Outer Left Pylon", "Outer R Bay",
    "Outer Right Pylon", "Outer Weapon Bays", "Outer Wing Pylons", "Radar Station", "Radome",
    "Rear Mount", "Rear Turret", "Rear Turrets", "Rear Weapon Bay", "Right Bay", "Right Internal Bay",
    "Side Mount", "TGP", "Tail Hook", "Tailhook", "Top Mount", "Turret Left", "Turret Right", "VLS",
    "Weapon Bay", "Weapon Bays", "Wing Glove Pylons", "Wing Pylons", "Wingtip Pylons",
    "Long-range sky scanning radar",
    # игра
    "Cargo Bay", "Cargo Bay (Front)", "Cargo Bay (Rear)", "Cargo Bay(Rear)", "Floor Turret Mount",
    "Left Sponson Pylon", "Right Sponson Pylon", "Sponson Pylons", "Slingload Hook",
    "Left Fuselage Pylon", "Right Fuselage Pylon", "Fuselage Pylons", "Door guns",
]
miss = [c for c in cands if c not in ru]
have = [c for c in cands if c in ru]
print("УЖЕ ЕСТЬ (%d):" % len(have))
for c in have:
    print(f'   "{c}" -> "{ru[c]}"')
print("\nНУЖНО ДОБАВИТЬ (%d):" % len(miss))
with io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\labels_missing.json", "w", encoding="utf-8") as fh:
    json.dump(miss, fh, ensure_ascii=False, indent=1)
for c in miss:
    print("   ", c)
