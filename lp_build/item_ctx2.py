# -*- coding: utf-8 -*-
"""Точный контекст: имя предмета или его код? (порядок полей jsonKey, name, code, description)"""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import UnityPy
UnityPy.config.FALLBACK_UNITY_VERSION = "2022.3.62f1"

unpack = r"C:\Users\user\AppData\Local\Temp\lp_build\unpack"
SPLIT = re.compile(rb"[\x00-\x08\x0B-\x1F\x7F]")
TARGETS = ["MBT", "Ammo box", "Ammo Box", "Cursor Class LFD", "Radar", "RADAR", "Radome", "AA"]

FILES = [f for f in os.listdir(unpack) if any(s in f for s in ("Kar_", "Bote_", "MC260_"))]
for f in sorted(set(FILES)):
    env = UnityPy.load(os.path.join(unpack, f))
    for o in env.objects:
        try:
            raw = o.get_raw_data()
        except Exception:
            continue
        toks = [c.decode("utf-8", "ignore").strip() for c in SPLIT.split(raw)]
        for i, t in enumerate(toks):
            if t in TARGETS:
                left = " ┃ ".join(x[:60] for x in toks[max(0, i - 5):i])
                right = " ┃ ".join(x[:90] for x in toks[i + 1:i + 6])
                print(f"\n[{f[:30]}] <<{left}>>  【{t}】  <<{right}>>")
