# -*- coding: utf-8 -*-
"""Контекст имён точек маршрута в resources.assets + список всех route/waypoint имён."""
import io, re, sys, json, collections

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data\resources.assets"
data = open(p, "rb").read()
needle = b"Ingress Via Mountains"

out = []
for i, m in enumerate(re.finditer(re.escape(needle), data)):
    s, e = max(0, m.start() - 450), min(len(data), m.end() + 450)
    out.append(f"=== {i} @ {m.start()}\n" + repr(data[s:e]))
io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\wpt_ctx.txt", "w", encoding="utf-8", newline="\n").write("\n\n".join(out))

# все пары "ключ": "значение" рядом с needle — ищем поля Name/DisplayName/objectiveName
pair_re = re.compile(rb'"([A-Za-z][A-Za-z0-9_]{1,24})"\s*:\s*"((?:[^"\\]|\\.){1,120})"')
keys = collections.Counter()
samples = collections.defaultdict(set)
for m in pair_re.finditer(data):
    k = m.group(1).decode("ascii")
    if k.lower() in ("name", "displayname", "objectivename", "uniquename", "label", "title"):
        v = m.group(2).decode("utf-8", "replace")
        keys[k] += 1
        samples[k].add(v)
print({k: c for k, c in keys.items()})
with io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\wpt_names.txt", "w", encoding="utf-8", newline="\n") as f:
    for k in samples:
        f.write(f"##### {k} ({len(samples[k])})\n")
        for v in sorted(samples[k]):
            f.write(v + "\n---\n")
print("файлы: wpt_ctx.txt, wpt_names.txt")
