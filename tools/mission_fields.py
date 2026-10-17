# -*- coding: utf-8 -*-
"""Собирает JSON-поля миссий из resources.assets и levelN (Message/Description/Name и т. п.)."""
import io, os, re, sys, json, collections

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
root = r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data"
pair_re = re.compile(rb'"([A-Za-z][A-Za-z0-9_]{1,24})"\s*:\s*"((?:[^"\\]|\\.){1,4000})"')

keys = collections.Counter()
values = collections.defaultdict(set)

for fn in ["resources.assets", "level0", "level1", "level2", "level3", "level4", "level5"]:
    p = os.path.join(root, fn)
    if not os.path.exists(p):
        continue
    data = open(p, "rb").read()
    for m in pair_re.finditer(data):
        k = m.group(1).decode("ascii")
        v = m.group(2).decode("utf-8", "replace")
        keys[k] += 1
        values[k].add(v)

print("=== поля JSON (частота) ===")
for k, c in keys.most_common(40):
    print(f"{c:6}  {k}")

# сохраняем «смысловые» поля
interesting = [k for k in keys if k.lower() in
               ("message", "description", "desc", "name", "title", "briefing", "text", "objective", "hint")]
with io.open("mission_fields.txt", "w", encoding="utf-8", newline="\n") as f:
    for k in interesting:
        f.write(f"##### {k} ({len(values[k])})\n")
        for v in sorted(values[k]):
            f.write(v + "\n----\n")
print("сохранено в mission_fields.txt")
