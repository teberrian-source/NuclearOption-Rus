# -*- coding: utf-8 -*-
"""Описания/брифинги миссий и подсказки: что уже переведено, что нет."""
import io, os, re, sys, json, collections

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
root = r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data"
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

ru_raw = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in ru_raw.split("\n") if not l.strip().startswith("//"))), strict=False)

pair_re = re.compile(rb'"([A-Za-z][A-Za-z0-9_]{1,24})"\s*:\s*"((?:[^"\\]|\\.){1,6000})"')
fields = collections.defaultdict(set)
for fn in ["resources.assets", "level0", "level1", "level2", "level3", "level4", "level5"]:
    p = os.path.join(root, fn)
    if not os.path.exists(p):
        continue
    data = open(p, "rb").read()
    for m in pair_re.finditer(data):
        k = m.group(1).decode("ascii")
        if k not in ("description", "Message", "title", "body", "message", "objectiveName"):
            continue
        raw = m.group(2).decode("utf-8", "replace")
        try:
            val = json.loads('"' + raw + '"')
        except Exception:
            continue
        fields[k].add(val)

report = []
for k in sorted(fields):
    vals = sorted(fields[k])
    miss = [v for v in vals if v not in ru]
    report.append((k, len(vals), len(miss)))
    print(f"{k}: всего {len(vals)}, нет в словаре {len(miss)}")

with io.open("mission_todo.txt", "w", encoding="utf-8", newline="\n") as f:
    for k in sorted(fields):
        for v in sorted(fields[k]):
            if v in ru:
                continue
            f.write("##### " + k + "\n" + v + "\n----\n")
print("список: mission_todo.txt")
