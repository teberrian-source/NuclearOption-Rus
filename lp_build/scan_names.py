# -*- coding: utf-8 -*-
"""Находит имена предметов (WeaponInfo.name) в бандлах модов и сверяет с ru.json."""
import io, os, re, sys, json

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import UnityPy
UnityPy.config.FALLBACK_UNITY_VERSION = "2022.3.62f1"

unpack = r"C:\Users\user\AppData\Local\Temp\lp_build\unpack"
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

def parse_json(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse_json(base + r"\ru.json")

# что мы переводили в раунде 9
KEYS = ["Ammo Box", "Ammo box", "Cargo 2x", "cargo", "cargo 2x", "Launchers", "Point Defence",
        "Point Defense", "Roof Mount", "roof mount", "roof turret", "The Device", "Truck bed",
        "Turret", "Vehicle Cargo", "coax", "subturret", "subturret (H)", "subturrets", "tow hook",
        "turret mount", "Bomb Bay (2x)", "Gun Mount", "Inner L Bay", "Inner R Bay", "Internal Gun",
        "Mission Bay", "Outer L Bay", "Outer R Bay", "Outer Weapon Bays", "Side Mount", "TGP",
        "Tailhook", "Top Mount", "VLS", "Weapon Bays", "Internal Cannon"]

names = {}   # имя предмета -> файлы
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
        if len(raw) > 20000:
            continue
        txt = raw.decode("utf-8", "ignore")
        toks = [t.strip() for t in re.split(r"[\x00-\x1f\x7f]+", txt) if t.strip()]
        for i, t in enumerate(toks):
            if t.endswith("_WI") and i + 2 < len(toks):
                nm, code = toks[i + 1], toks[i + 2]
                if re.fullmatch(r"[A-Z0-9/\- ]{2,10}", code) and 1 < len(nm) < 40:
                    names.setdefault(nm, set()).add(f)
    print(f, "->", len(names), flush=True)

print("\n=== имена предметов (WeaponInfo.name) и их статус в ru.json ===")
for nm in sorted(names):
    st = "ПЕРЕВЕДЕНО: " + ru[nm] if nm in ru else ("есть ключ = сам себе" if nm in ru else "не переведено")
    print(f"{'!' if nm in ru else ' '} {nm!r}  ({len(names[nm])} шт.)  {st}")

print("\n=== из раунда 9: что является именем предмета ===")
for k in KEYS:
    hit = [nm for nm in names if nm == k or nm.lower() == k.lower()]
    print(f"{'ИМЯ ПРЕДМЕТА' if hit else 'не найдено как имя'}: {k!r} -> {ru.get(k)!r}")
