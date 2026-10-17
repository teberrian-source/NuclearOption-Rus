# -*- coding: utf-8 -*-
"""Полные (не обрезанные) длинные строки из бандлов модов -> что отсутствует в ru.json."""
import io, os, re, sys, json

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import UnityPy
UnityPy.config.FALLBACK_UNITY_VERSION = "2022.3.62f1"

base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
unpack = r"C:\Users\user\AppData\Local\Temp\lp_build\unpack"

def parse_json(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse_json(base + r"\ru.json")
OK = re.compile(rb"^[A-Za-z0-9 ,.'()\-/:;\"%+&\[\]?!*_=#~@<>|\\{}`^$]{50,3000}$")

found = {}
for f in sorted(os.listdir(unpack)):
    p = os.path.join(unpack, f)
    try:
        env = UnityPy.load(p)
    except Exception as e:
        print("!!", f, e, flush=True)
        continue
    for o in env.objects:
        try:
            raw = o.get_raw_data()
        except Exception:
            continue
        if len(raw) > 60000 or len(raw) < 60:
            continue
        for s in re.findall(rb"[ -~]{50,3000}", raw):
            if not OK.match(s):
                continue
            t = s.decode("ascii", "replace").strip()
            if len(t.split()) < 9 or t.count(" ") < 8:
                continue
            if ";" in t or t.startswith("{") or t.startswith('"'):
                continue
            found.setdefault(t, set()).add(f)
    print(f, "->", len(found), flush=True)

missing = sorted(t for t in found if t not in ru)
print("\nвсего длинных строк:", len(found), "| нет в ru.json:", len(missing))
json.dump(missing, io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\missing_full.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\missing_full.txt", "w", encoding="utf-8").write("\n\n".join(missing))
for t in missing:
    print("|", t)
