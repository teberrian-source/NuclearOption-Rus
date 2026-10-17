# -*- coding: utf-8 -*-
"""Готовит задания на перевод раунда 15: миссии и подписи."""
import io, os, re, sys, json, collections

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
raw = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in raw.split("\n") if not l.strip().startswith("//"))), strict=False)

root = r"C:\Users\user\AppData\LocalLow\Shockfront\NuclearOption\Missions"

def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, path + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path + "[%d]" % i)
    else:
        yield path, o

desc, msgs, objnames, airbases = [], [], [], []
for mission in sorted(os.listdir(root)):
    d = os.path.join(root, mission)
    if not os.path.isdir(d):
        continue
    for fn in os.listdir(d):
        if not fn.lower().endswith(".json") or fn.lower() == "meta.json":
            continue
        try:
            data = json.load(io.open(os.path.join(d, fn), encoding="utf-8-sig"))
        except Exception:
            continue
        for path, v in walk(data):
            if not isinstance(v, str) or len(v) < 3 or v in ru:
                continue
            key = re.sub(r"\[\d+\]", "[]", path)
            if key.endswith("/description"):
                desc.append(v)
            elif key.endswith("/Message"):
                msgs.append(v)
            elif key.endswith("/objectives[]/DisplayName"):
                objnames.append(v)
            elif key.endswith("/airbases[]/DisplayName"):
                airbases.append(v)

def uniq(x):
    return sorted(set(x))

desc, msgs, objnames, airbases = map(uniq, (desc, msgs, objnames, airbases))
print("описания:", len(desc), "| сообщения:", len(msgs), "| цели:", len(objnames), "| аэродромы:", len(airbases))

# внутренние идентификаторы целей (не показываются игроку)
ident = re.compile(r"^[A-Za-z0-9_.\-]+$|^(box|wait|close|final|spot|started|not |waypoint)", re.I)
obj_show = [v for v in objnames if not ident.match(v) and len(re.findall(r"[A-Za-z']{2,}", v)) >= 1]
obj_hidden = [v for v in objnames if v not in obj_show]

with io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\r15_objnames.txt", "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(obj_show))
with io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\r15_objhidden.txt", "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(obj_hidden))
with io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\r15_objairbases.txt", "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(airbases))
print("показываемые цели:", len(obj_show), "| скрытые/идентификаторы:", len(obj_hidden))

idx = {}
n = 0
out_m = []
for v in desc + msgs:
    n += 1
    idx[str(n)] = {"kind": "prose", "en": v}
    out_m.append(f"### {n}\n{re.sub(r'[ \\t]*\\n[ \\t]*', chr(10), v).strip()}\n")
out_l = []
for v in obj_show:
    n += 1
    idx[str(n)] = {"kind": "label", "en": v}
    out_l.append(f"### {n}\n{v}\n")
io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\r15_prose.txt", "w", encoding="utf-8", newline="\n").write("\n".join(out_m))
io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\r15_labels.txt", "w", encoding="utf-8", newline="\n").write("\n".join(out_l))
json.dump(idx, io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\r15_index.json", "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
print("к переводу: проза", len(desc + msgs), "| подписи", len(obj_show), "| всего", n)
