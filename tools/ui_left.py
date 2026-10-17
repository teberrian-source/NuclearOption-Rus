# -*- coding: utf-8 -*-
"""Показывает остаток по источникам UI-текста (TextMeshProUGUI.m_text, Text.m_Text, Slot.value, Entry.name...)."""
import io, re, sys, json
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

def parse(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse(base + r"\ru.json")
raw = io.open(base + r"\extracted_strings.txt", encoding="utf-8", errors="replace").read()
raw = raw.split("// ========== RAW LONG STRINGS")[0]

SRC = ("TextMeshProUGUI.m_text", "Text.m_Text", "Slot.value", "Entry.name",
       "StyleLabel.displayLabel", "WeaponMount.mountName", "Livery.name", "TMP_InputField.m_Text")
left = defaultdict(list)
cur = "?"
for line in raw.split("\n"):
    s = line.strip()
    if s.startswith("//"):
        x = s[2:].strip()
        if x and "===" not in x:
            cur = x
        continue
    m = re.match(r'^"((?:[^"\\]|\\.)*)": ""', s)
    if not m or cur not in SRC:
        continue
    try:
        t = json.loads('"' + m.group(1) + '"')
    except Exception:
        continue
    if t not in ru:
        left[cur].append(t)

for src in SRC:
    items = sorted(set(left.get(src, [])))
    if not items:
        continue
    print(f"\n=== {src} ({len(items)}) ===")
    limit = 120 if src == "TextMeshProUGUI.m_text" else 45
    for t in items[:limit]:
        print("   ", json.dumps(t, ensure_ascii=False)[:230])
