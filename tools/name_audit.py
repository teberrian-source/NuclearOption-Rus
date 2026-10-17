# -*- coding: utf-8 -*-
"""Аудит: какие ПЕРЕВЕДЁННЫЕ нами строки являются именами предметов/техники —
т.е. в бандле сразу за ними идёт длинное описание (>=60 символов с пробелами).
Такие имена по правилу должны остаться английскими."""
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
# кандидаты — короткие ключи с русским значением (латиница в ключе)
cand = {k for k, v in ru.items()
        if 2 <= len(k) <= 60 and CYR.search(v) and not CYR.search(k)
        and re.fullmatch(r"[A-Za-z0-9 .'\-/+()\[\]]+", k)}

def is_desc(t):
    return len(t) >= 60 and t.count(" ") >= 8 and not re.search(r"[;{}|]", t)

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
            if t not in cand:
                continue
            for nxt in toks[i + 1:i + 8]:
                if is_desc(nxt):
                    found.setdefault(t, {"ru": ru[t], "files": set(), "desc": nxt})
                    found[t]["files"].add(f)
                    break

out = [f"=== имён предметов/техники с описанием (переведены нами): {len(found)} ==="]
for t in sorted(found):
    d = found[t]
    out.append(f"\n• {t!r} -> {d['ru']!r}\n  файлы: {', '.join(sorted(d['files']))[:120]}\n  описание: {d['desc'][:140]}")
txt = "\n".join(out)
io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\name_audit.txt", "w", encoding="utf-8").write(txt)
print(txt)
