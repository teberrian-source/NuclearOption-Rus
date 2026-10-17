# -*- coding: utf-8 -*-
"""Кандидаты в «имена точек/задач» из DisplayName/objectiveName/Name в resources.assets."""
import io, re, sys, json, collections

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
raw = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in raw.split("\n") if not l.strip().startswith("//"))), strict=False)

txt = io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\wpt_names.txt", encoding="utf-8").read()
sections = re.split(r"^##### (\w+) \((\d+)\)$", txt, flags=re.M)
sections = [s for s in sections if s.strip()]
data = {}
for i in range(0, len(sections) - 2, 3):
    key, cnt, body = sections[i], sections[i + 1], sections[i + 2]
    data[key] = [v.strip() for v in body.split("\n---\n") if v.strip()]

weap = re.compile(r"(\d+\s*(mm|kg|kJ|km|m)\b|x\d+\b|\bAGM-|\bIRM-|\bAAM-|\bMMR-|\bPAB-|\bAGR-|\bR9\b|\bSAM\b|Mk\.|Turret|Pod\b|Dispenser|Mount\b|Rail\b|Gunpod)", re.I)
junk = re.compile(r"^(AA-nn|.*\bnn\b|Aircraft|Cursor|FS-12)$", re.I)

print("=== objectiveName ===")
for v in sorted(data.get("objectiveName", [])):
    print(f"  {'[есть]' if v in ru else '[НЕТ ]'} {v}")
print("=== Name (8) ===")
for v in sorted(data.get("Name", [])):
    print(f"  {'[есть]' if v in ru else '[НЕТ ]'} {v}")

cand = []
for v in sorted(set(data.get("DisplayName", []))):
    if not v or len(v) < 4:
        continue
    if weap.search(v) or junk.match(v):
        continue
    if re.search(r"^\d", v):
        continue
    if v in ru:
        continue
    words = re.findall(r"[A-Za-z']{2,}", v)
    if len(words) < 2:
        continue
    cand.append(v)
print("=== DisplayName-кандидаты (не в словаре):", len(cand))
for v in cand:
    print("   ", v)
io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\wpt_cand.txt", "w", encoding="utf-8", newline="\n").write("\n".join(cand))
