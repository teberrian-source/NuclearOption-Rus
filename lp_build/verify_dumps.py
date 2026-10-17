# -*- coding: utf-8 -*-
"""Сколько строк из extracted_strings.txt осталось непереведёнными по каждому источнику."""
import io, re, sys, json
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

def parse(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse(base + r"\ru.json")
raw = io.open(base + r"\extracted_strings.txt", encoding="utf-8", errors="replace").read()
raw = raw.split("// ========== RAW LONG STRINGS")[0]

tot = Counter()
left = defaultdict(list)
cur = "?"
for line in raw.split("\n"):
    s = line.strip()
    if s.startswith("//"):
        src = s[2:].strip()
        if src and "===" not in src:
            cur = src
        continue
    m = re.match(r'^"((?:[^"\\]|\\.)*)": ""', s)
    if not m:
        continue
    try:
        t = json.loads('"' + m.group(1) + '"')
    except Exception:
        continue
    if len(t) < 12:
        continue
    tot[cur] += 1
    if t not in ru:
        left[cur].append(t)

print(f"{'источник':<45} {'всего':>6} {'осталось':>9}")
for src, n in tot.most_common():
    print(f"{src:<45} {n:>6} {len(left[src]):>9}")

print("\n--- осталось (первые 6 по источнику, только игровые) ---")
for src in ("WeaponInfo.description", "MissileDefinition.description", "VehicleDefinition.description",
            "AircraftDefinition.description", "UnitDefinition.description", "ShipDefinition.description",
            "BuildingDefinition.description", "HintTip.text", "WingButton.tooltip", "StyleLabel.tooltip",
            "ShowHoverText.showText", "AvTooltipTarget.tooltip"):
    items = left.get(src)
    if not items:
        continue
    print(f"\n[{src}] осталось {len(items)}:")
    for t in items[:6]:
        print("   ", json.dumps(t, ensure_ascii=False)[:140])
