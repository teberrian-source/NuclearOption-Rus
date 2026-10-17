# -*- coding: utf-8 -*-
"""Делает todo.json — точный список строк к переводу (индекс -> группа/источник/текст)."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

raw_ru = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ls = [l for l in raw_ru.split("\n") if not l.strip().startswith("//")]
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

raw = io.open(base + r"\extracted_strings.txt", encoding="utf-8", errors="replace").read()
raw = raw.split("// ========== RAW LONG STRINGS")[0]

GROUPS = [
    ("weapon", ("WeaponInfo.description", "MissileDefinition.description")),
    ("vehicle", ("VehicleDefinition.description", "AircraftDefinition.description", "UnitDefinition.description",
                 "ShipDefinition.description", "BuildingDefinition.description")),
    ("hint", ("HintTip.text",)),
    ("tooltip", ("WingButton.tooltip", "StyleLabel.tooltip", "ShowHoverText.showText", "AvTooltipTarget.tooltip")),
]

cur = "?"
buckets = {k: {} for k, _ in GROUPS}
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
        text = json.loads('"' + m.group(1) + '"')
    except Exception:
        continue
    if text in ru or len(text) < 12:
        continue
    for k, srcs in GROUPS:
        if cur in srcs:
            buckets[k].setdefault(text, cur)

items = []
for k, _ in GROUPS:
    for text, src in sorted(buckets[k].items()):
        items.append({"i": len(items) + 1, "group": k, "src": src, "en": text})

io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\todo.json", "w", encoding="utf-8").write(
    json.dumps(items, ensure_ascii=False, indent=1))
print("всего:", len(items))
for k, _ in GROUPS:
    print(" ", k, sum(1 for it in items if it["group"] == k))
print("todo.json записан")
