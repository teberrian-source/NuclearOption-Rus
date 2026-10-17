# -*- coding: utf-8 -*-
"""Контекст только для спорных строк: имя или код?"""
import io, os, re, sys, json

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import UnityPy
UnityPy.config.FALLBACK_UNITY_VERSION = "2022.3.62f1"

unpack = r"C:\Users\user\AppData\Local\Temp\lp_build\unpack"
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
SPLIT = re.compile(rb"[\x00-\x08\x0B-\x1F\x7F]")

def parse_json(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse_json(base + r"\ru.json")
TARGETS = ["Cursor Class LFD", "Ammo box", "Ammo Box", "Type-12 MBT", "Radar Container"]
for t in TARGETS:
    print(f"  в словаре: {t!r} -> {ru.get(t)!r}")

FILES = [f for f in sorted(os.listdir(unpack)) if any(s in f for s in ("Kar_", "Bote_"))]
for f in FILES:
    env = UnityPy.load(os.path.join(unpack, f))
    for o in env.objects:
        try:
            raw = o.get_raw_data()
        except Exception:
            continue
        toks = [c.decode("utf-8", "ignore").strip() for c in SPLIT.split(raw)]
        for i, t in enumerate(toks):
            if t in TARGETS:
                left = " ┃ ".join(x[:55] for x in toks[max(0, i - 8):i] if x)
                right = " ┃ ".join(x[:100] for x in toks[i + 1:i + 8] if x)
                print(f"\n[{f[:28]}] <<{left}>> 【{t}】 <<{right}>>")
