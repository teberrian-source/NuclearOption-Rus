# -*- coding: utf-8 -*-
"""Печатает точные строки по выбранным полям (для точного перевода)."""
import io, json, re, sys

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
raw = io.open(base + r"\extracted_strings.txt", encoding="utf-8", errors="replace").read()
raw = raw.split("// ========== RAW LONG STRINGS")[0]

WANT = ["ShowMessageSavedOutcome.Message", "AllowBanListTabs", "LinkTooltipMapping.hoverText",
        "Plugin.statusMessage", "ConvoyGroup.Name", "Slot.value", "TextMeshProUGUI.m_text"]
cur = "?"
for line in raw.split("\n"):
    s = line.strip()
    if s.startswith("//"):
        x = s[2:].strip()
        if x and "===" not in x:
            cur = x
        continue
    if not any(w in cur for w in WANT):
        continue
    m = re.match(r'^"((?:[^"\\]|\\.)*)":\s*""', s)
    if not m:
        continue
    try:
        t = json.loads('"' + m.group(1) + '"')
    except Exception:
        continue
    if re.search(r"[A-Za-z]{3}", t):
        print(f"[{cur}] {t!r}")
