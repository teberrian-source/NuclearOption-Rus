# -*- coding: utf-8 -*-
"""Вытаскивает все описания (длинные англ. фразы) из бандлов модов и данных игры,
сравнивает с ru.json и пишет отсутствующие в missing_descriptions.json."""
import io, os, re, sys, json

sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
UnityPy.config.FALLBACK_UNITY_VERSION = "2022.3.62f1"

base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
unpack = r"C:\Users\user\AppData\Local\Temp\lp_build\unpack"

def parse_json(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse_json(base + r"\ru.json")

WORDY = re.compile(rb"^[A-Za-z0-9 ,.'()\-/:;\"%+&\[\]]{50,600}$")

def candidates(path):
    try:
        env = UnityPy.load(path)
    except Exception as e:
        print("!! не загрузился", path, e, flush=True)
        return []
    out = []
    for o in env.objects:
        try:
            raw = o.get_raw_data()
        except Exception:
            continue
        if len(raw) > 40000 or len(raw) < 60:
            continue
        for s in re.findall(rb"[ -~]{50,600}", raw):
            if not WORDY.match(s):
                continue
            t = s.decode("ascii", "replace").strip()
            if len(t.split()) < 8:
                continue
            out.append(t)
    return out

files = []
for f in os.listdir(unpack):
    files.append(os.path.join(unpack, f))
files.append(r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data\resources.assets")

allc = {}
for p in files:
    cs = candidates(p)
    print(os.path.basename(p), "кандидатов:", len(cs), flush=True)
    for t in cs:
        allc.setdefault(t, set()).add(os.path.basename(p))

missing = {t: sorted(v) for t, v in allc.items() if t not in ru}
print("=" * 80)
print("всего кандидатов:", len(allc), "| нет в ru.json:", len(missing))
json.dump(missing, io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\missing_descriptions.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for t in sorted(missing):
    print("|", t[:180])
