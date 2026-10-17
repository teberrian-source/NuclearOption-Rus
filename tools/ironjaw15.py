# -*- coding: utf-8 -*-
"""Строки миссий из пользовательской папки Missions (Ironjaw Sound pack)."""
import io, os, re, sys, json, collections

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
raw = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in raw.split("\n") if not l.strip().startswith("//"))), strict=False)

root = r"C:\Users\user\AppData\LocalLow\Shockfront\NuclearOption\Missions"
found = collections.defaultdict(set)

def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, path + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path + "[%d]" % i)
    else:
        yield path, o

for mission in sorted(os.listdir(root)):
    d = os.path.join(root, mission)
    if not os.path.isdir(d):
        continue
    for fn in os.listdir(d):
        if not fn.lower().endswith(".json") or fn.lower() == "meta.json":
            continue
        try:
            data = json.load(io.open(os.path.join(d, fn), encoding="utf-8-sig"))
        except Exception as e:
            print("ошибка", fn, e)
            continue
        for path, v in walk(data):
            if not isinstance(v, str) or len(v) < 3:
                continue
            key = re.sub(r"\[\d+\]", "[]", path)
            if key.endswith("/description") or key.endswith("/Message") or key.endswith("/DisplayName"):
                if v not in ru:
                    found[key].add(v)

total = 0
with io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\ironjaw_todo.txt", "w", encoding="utf-8", newline="\n") as f:
    for k in sorted(found):
        f.write(f"##### {k} ({len(found[k])})\n")
        for v in sorted(found[k]):
            f.write(v + "\n----\n")
            total += 1
print("строк Ironjaw к переводу:", total)
for k in sorted(found):
    print("  ", k, len(found[k]))
