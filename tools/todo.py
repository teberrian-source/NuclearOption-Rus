# -*- coding: utf-8 -*-
"""Собирает из extracted_strings.txt только игровые описания/подсказки/тултипы, которых нет в ru.json."""
import io, os, re, sys, json

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

raw_ru = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ls = [l for l in raw_ru.split("\n") if not l.strip().startswith("//")]
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

raw = io.open(base + r"\extracted_strings.txt", encoding="utf-8", errors="replace").read()
raw = raw.split("// ========== RAW LONG STRINGS")[0]

GROUPS = {
    "weapon": ("WeaponInfo.description", "MissileDefinition.description"),
    "vehicle": ("VehicleDefinition.description", "AircraftDefinition.description", "UnitDefinition.description",
                "ShipDefinition.description", "BuildingDefinition.description"),
    "hint": ("HintTip.text",),
    "tooltip": ("WingButton.tooltip", "StyleLabel.tooltip", "ShowHoverText.showText", "AvTooltipTarget.tooltip"),
}

cur = "?"
buckets = {k: {} for k in GROUPS}
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
    for k, srcs in GROUPS.items():
        if cur in srcs:
            buckets[k].setdefault(text, cur)

total = sum(len(v) for v in buckets.values())
print("итого к переводу:", total)
for k, v in buckets.items():
    print(f"  {k}: {len(v)}")

out = r"C:\Users\user\AppData\Local\Temp\lp_build\translate_todo.txt"
with io.open(out, "w", encoding="utf-8") as f:
    for k, v in buckets.items():
        f.write(f"########## {k} ({len(v)}) ##########\n")
        for text, src in sorted(v.items()):
            f.write(f"[{src}] {text}\n")
print("файл:", out)

for k, v in buckets.items():
    print(f"\n===== {k} ({len(v)}) =====")
    for text, src in sorted(v.items()):
        print(json.dumps(text, ensure_ascii=False)[:170])
