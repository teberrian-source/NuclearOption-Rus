# -*- coding: utf-8 -*-
"""Проверяет значения описаний RAH-72 / MC-260 в ru.json и ищет описание 'Radome' в бандле MC-260."""
import io, json, re, sys

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

def parse_json(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse_json(base + r"\ru.json")
print("--- ключи со словом RAH-72 / Chimera / Cricket в значении ---")
for k, v in ru.items():
    if "RAH-72 is a recon" in k or "largest aircraft so far" in k or "Chimera" in k[:200]:
        print(f"KEY: {k[:90]!r}\n  -> {v[:120]!r}\n")

print("--- поиск 'Radome' в бандле MC-260 ---")
b = r"C:\Users\user\AppData\Local\Temp\lp_build\unpack\Aryx_MC260_Chimera_1.2.0.dll.84708.unity3d"
if io.open(b, "rb").read(4):
    import UnityPy
    UnityPy.config.FALLBACK_UNITY_VERSION = "2022.3.62f1"
    env = UnityPy.load(b)
    n = 0
    for o in env.objects:
        try:
            raw = o.get_raw_data()
        except Exception:
            continue
        if b"adome" not in raw and b"Radome" not in raw:
            continue
        n += 1
        print("=" * 80)
        print("TYPE", o.type.name, "size", len(raw))
        for s in re.findall(rb"[ -~]{3,200}", raw)[:60]:
            print("   |", s.decode("ascii", "replace"))
        if n >= 6:
            break
