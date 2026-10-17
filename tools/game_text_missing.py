# -*- coding: utf-8 -*-
"""Оставляет из game_text_cand.txt только строки, которых нет в ru.json."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
ru_raw = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in ru_raw.split("\n") if not l.strip().startswith("//"))), strict=False)

lines = io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\game_text_cand.txt", encoding="utf-8").read().split("\n")
cur_file = None
res = {}
for l in lines:
    if l.startswith("#### "):
        cur_file = l[5:].strip()
        res[cur_file] = []
        continue
    if l == "====" or not l.strip():
        continue
    res[cur_file].append(l)

total_missing = 0
with io.open("game_text_missing.txt", "w", encoding="utf-8", newline="\n") as f:
    for fn, items in res.items():
        miss = [s for s in items if s not in ru]
        total_missing += len(miss)
        f.write(f"#### {fn}: всего {len(items)}, нет в словаре {len(miss)}\n")
        for s in miss:
            f.write(s + "\n----\n")
print("нет в словаре:", total_missing, "-> game_text_missing.txt")
