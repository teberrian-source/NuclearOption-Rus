# -*- coding: utf-8 -*-
"""Контекст: где именно встречаются строки раунда 9 в бандлах модов
(подпись слота / имя устанавливаемого предмета)."""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import UnityPy
UnityPy.config.FALLBACK_UNITY_VERSION = "2022.3.62f1"

unpack = r"C:\Users\user\AppData\Local\Temp\lp_build\unpack"

KEYS = ["Ammo Box", "Ammo box", "Cargo 2x", "Launchers", "Point Defence", "Point Defense",
        "Roof Mount", "roof mount", "roof turret", "The Device", "Truck bed", "Turret",
        "Vehicle Cargo", "coax", "subturret", "tow hook", "turret mount", "Bomb Bay (2x)",
        "Gun Mount", "Internal Gun", "Internal Cannon", "Mission Bay", "Outer Weapon Bays",
        "Side Mount", "TGP", "Tailhook", "Top Mount", "VLS", "Weapon Bays",
        # для сравнения — заведомо имена предметов
        "Radome", "20mm Rotary Cannon", "R9 SAM Launcher", "Radar Container"]

hits = {k: [] for k in KEYS}

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
        txt = raw.decode("utf-8", "replace")
        if "\ufffd" in txt:
            txt = raw.decode("utf-8", "ignore")
        for k in KEYS:
            for m in re.finditer(re.escape(k), txt):
                a, b = max(0, m.start() - 70), min(len(txt), m.end() + 90)
                ctx = re.sub(r"[\x00-\x1f\x7f]+", " | ", txt[a:b]).strip()
                hits[k].append((f, ctx))

out = []
for k in KEYS:
    out.append(f"\n########## {k!r} — вхождений: {len(hits[k])}")
    seen = set()
    for f, ctx in hits[k]:
        if ctx in seen:
            continue
        seen.add(ctx)
        out.append(f"  [{f}] {ctx}")

io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\item_ctx.txt", "w", encoding="utf-8").write("\n".join(out))
print("\n".join(out))
