# -*- coding: utf-8 -*-
"""Аудит-2 (широкое окно): переведённые нами ключи, за которыми в бандле идёт
описание (>=60 символов, >=8 слов) в пределах 20 токенов → скорее всего это
имя предмета/техники и должно остаться английским."""
import io, os, re, sys, json

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import UnityPy
UnityPy.config.FALLBACK_UNITY_VERSION = "2022.3.62f1"

unpack = r"C:\Users\user\AppData\Local\Temp\lp_build\unpack"
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
SPLIT = re.compile(rb"[\x00-\x08\x0B-\x1F\x7F]")
CYR = re.compile(r"[А-Яа-яЁё]")

def parse_json(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse_json(base + r"\ru.json")
cand = {k for k, v in ru.items()
        if 2 <= len(k) <= 80 and CYR.search(v) and not CYR.search(k)
        and re.fullmatch(r"[A-Za-z0-9 .'\-/+()\[\]]+", k)}

def is_desc(t):
    return 60 <= len(t) <= 3000 and t.count(" ") >= 8 and not re.search(r"[;{}|]", t)

found = {}
for f in sorted(os.listdir(unpack)):
    try:
        env = UnityPy.load(os.path.join(unpack, f))
    except Exception:
        continue
    for o in env.objects:
        try:
            raw = o.get_raw_data()
        except Exception:
            continue
        toks = [c.decode("utf-8", "ignore").strip() for c in SPLIT.split(raw)]
        for i, t in enumerate(toks):
            if t not in cand or t in found:
                continue
            for j, nxt in enumerate(toks[i + 1:i + 21]):
                if is_desc(nxt):
                    found[t] = {"ru": ru[t], "files": {f}, "dist": j + 1, "desc": nxt}
                    break

out = [f"=== кандидаты (переведённые ключи рядом с описанием): {len(found)} ==="]
for t in sorted(found, key=lambda x: (found[x]["dist"], x)):
    d = found[t]
    out.append(f"\n• {t!r} -> {d['ru']!r}   [через {d['dist']} ток., {', '.join(sorted(d['files']))[:90]}]\n  {d['desc'][:150]}")
txt = "\n".join(out)
io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\name_audit2.txt", "w", encoding="utf-8").write(txt)
print(txt)
