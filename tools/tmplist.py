# -*- coding: utf-8 -*-
"""Печатает все строки полей TextMeshProUGUI.m_text и Text.m_Text, отсутствующие в ru.json."""
import io, json, re, sys

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

def parse_json(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse_json(base + r"\ru.json")
raw = io.open(base + r"\extracted_strings.txt", encoding="utf-8", errors="replace").read().split("// ========== RAW LONG STRINGS")[0]
cur = "?"
for line in raw.split("\n"):
    s = line.strip()
    if s.startswith("//"):
        x = s[2:].strip()
        if x and "===" not in x:
            cur = x
        continue
    if "m_text" not in cur and "m_Text" not in cur:
        continue
    m = re.match(r'^"((?:[^"\\]|\\.)*)":\s*""', s)
    if not m:
        continue
    try:
        t = json.loads('"' + m.group(1) + '"')
    except Exception:
        continue
    if t in ru:
        continue
    if not re.search(r"[A-Za-z]{3}", t):
        continue
    print("|", t[:200].replace("\n", " / "))
