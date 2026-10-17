# -*- coding: utf-8 -*-
"""Чистые токены (нарезка по control-байтам) вокруг строк раунда 9:
имя предмета (далее идёт код и описание) или просто подпись слота в списке."""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import UnityPy
UnityPy.config.FALLBACK_UNITY_VERSION = "2022.3.62f1"

unpack = r"C:\Users\user\AppData\Local\Temp\lp_build\unpack"
SPLIT = re.compile(rb"[\x00-\x08\x0B-\x1F\x7F]")

KEYS = ["Ammo Box", "Ammo box", "Cargo 2x", "Launchers", "Point Defence", "Point Defense",
        "Roof Mount", "roof mount", "roof turret", "The Device", "Truck bed",
        "Vehicle Cargo", "coax", "subturret (H)", "subturrets", "tow hook", "turret mount",
        "Gun Mount", "Internal Gun", "Internal Cannon", "Outer Weapon Bays",
        "Side Mount", "TGP", "Tailhook", "Top Mount", "VLS", "Weapon Bays",
        "Radome", "Turret"]

res = {k: [] for k in KEYS}
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
        toks = []
        for ch in SPLIT.split(raw):
            t = ch.decode("utf-8", "ignore").strip()
            toks.append(t)
        for i, t in enumerate(toks):
            for k in KEYS:
                if t == k:
                    ctx = " ┃ ".join(x[:70] for x in toks[max(0, i - 3):i + 7])
                    res[k].append((f, ctx))

out = []
for k in KEYS:
    out.append(f"\n########## {k!r} — вхождений: {len(res[k])}")
    seen = set()
    n = 0
    for f, ctx in res[k]:
        key = ctx[:160]
        if key in seen:
            continue
        seen.add(key)
        n += 1
        if n > 4:
            break
        out.append(f"  [{f[:34]}] {ctx}")

io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\item_toks.txt", "w", encoding="utf-8").write("\n".join(out))
print("\n".join(out))
