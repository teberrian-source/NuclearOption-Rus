# -*- coding: utf-8 -*-
"""Проверка раунда 12: ключ точно есть в дампе / как сегмент многострочной строки / где расхождение."""
import io, re, sys, json, difflib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
sys.path.insert(0, r"C:\Users\user\AppData\Local\Temp\lp_build")
import importlib.util
spec = importlib.util.spec_from_file_location("r12", r"C:\Users\user\AppData\Local\Temp\lp_build\add_round12.py")
# не исполняем модуль (он пишет файл), поэтому список берём копией:
PAIRS = [
    ("The BDF is on the run, and trying to evacuate as much fuel from the area as they can.", ""),
    ("A large convoy of fuel trucks was last spotted about 5km north of Dustbowl. We're headed to the convoy's last known position.", ""),
    ("Your aircraft's visual sensors can detect ground vehicles within a range of 6km. We are to locate and destroy the convoy.", ""),
    ("Convoy has been spotted. Lets get to work.", ""),
    ("Headed to the target now.", ""),
    ("Form up on me and I'll lead us to the target.", ""),
    ("The vehicles should be targetable now. Select them as targets.", ""),
    ("Drop the bombs when the countdown reaches zero and the arrows on your HUD converge.", ""),
    ("Good hits. We'll finish off any remaining vehicles with our guns. Remember to pull up. Don't get so fixated on shooting that you forget the terrain exists.", ""),
    ("... and remember, they can still shoot back. Don't make it easy for them.", ""),
    ("Good shooting. That's the last of them. We should clear out before any response comes our way.", ""),
    ("Excellent work, every convoy vehicle has been destroyed.", ""),
    ("Enemy planes are after us! Stay near our base, our anti-air will protect us!", ""),
    ("Back to basics with bombs & guns on a CI-22 Cricket in a low-intensity engagement.", ""),
    ("Fly a T/A-30 Compass on a ground attack mission. Use missiles, rockets, bombs and guns to destroy a BDF convoy of lightly defended vehicles.", ""),
    ("Escalation co-op as BDF", ""),
    ("End Game for Everyone", ""),
    ("No reserve CI-22 Crickets currently available. You are first in queue for this airframe", ""),
    ("Cleared for landing on Runway 16", ""),
    ("Cleared to taxi to Runway 34", ""),
    ("Stability Assist <b>Enabled</b>", ""),
    ("Weapon safety lock <b>Enabled</b>", ""),
    ("Weapon safety lock <b>Disabled</b>", ""),
    ("Nav Lights <b>On</b>", ""),
    ("Nav Lights <b>Off</b>", ""),
    ("STALL WARNING", ""), ("INOPERABLE", ""), ("NO SIGNAL", ""), ("LOWER GEAR", ""),
    ("L ENG FIRE", ""), ("R ENG FIRE", ""), ("MISSILE CAMERA", ""), ("FAULT", ""),
    ("• Additional Boats / Ships", ""), ("• PALA Landing ship", ""), ("• Additional high-end SAMs", ""),
    ("• Additional ground units", ""), ("• More infantry mechanics", ""), ("• Missile mechanic changes", ""),
    ("• Further development on Ignus Archipelago", ""), ("• More destructible/interactible environment", ""),
    ("• AI improvements for aircraft, ships, and ground units", ""), ("• Additional control customization", ""),
    ("• Menu UI improvements", ""), ("• Additional low-rank aircraft", ""), ("• Existing aircraft remasters", ""),
    ("• Light utility VTOL", ""), ("• Aerial drones", ""), ("• Additional helicopters", ""),
    ("• Additional nuclear weapon types", ""), ("• Additional conventional weapon types", ""),
    ("• Terrain and runway cratering", ""), ("• Campaign system", ""), ("• VR implementation", ""),
    ("• Console version", ""), ("• Localization", ""), ("• New large landlocked map", ""),
    ("• Heavy cargo plane", ""), ("• Continued development and detailing of existing maps", ""),
    ("• More props and buildings", ""), ("• Logistics and economy changes", ""), ("• Graphics improvements", ""),
    ("• Sound improvements", ""), ("• Expanded modding support", ""),
    ("• More destructible/interactible environment and props", ""), ("• Expanded Mission Editor functionality", ""),
    ("• Dynamic music", ""),
]

dump = io.open(base + r"\untranslated.txt", encoding="utf-8", errors="replace").read()
keys, segs = set(), set()
for m in re.finditer(r'^\s*"((?:[^"\\]|\\.)*)"\s*:\s*""\s*,?\s*$', dump, re.M):
    try:
        s = json.loads('"' + m.group(1) + '"')
    except Exception:
        continue
    keys.add(s)
    for seg in s.split("\n"):
        if seg.strip():
            segs.add(seg.strip())

for k, _ in PAIRS:
    pos = "ключ" if k in keys else ("сегмент" if k in segs else "НЕТ")
    print(f"{pos:9} | {k[:80]!r}")
    if pos == "НЕТ":
        cand = difflib.get_close_matches(k, list(keys) + list(segs), n=2, cutoff=0.6)
        for c in cand:
            print("            ближайшее:", repr(c[:120]))
        # ищем по префиксу
        pref = k[:25]
        for s in list(keys) + list(segs):
            if s.startswith(pref[:20]):
                print("            по префиксу:", repr(s[:120]))
                break
