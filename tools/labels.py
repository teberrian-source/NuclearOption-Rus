# -*- coding: utf-8 -*-
"""Собирает короткие подписи слотов/хардпоинтов из объектов Unity-файла.

Использование: python labels.py <файл|--all-mods>
"""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
UnityPy.config.FALLBACK_UNITY_VERSION = "2022.3.62f1"

TOKENS = [b"subturret", b"coax", b"pylon", b"mount", b"turret", b"cargo", b"hardpoint",
          b"bay", b"hook", b"rack", b"ammo", b"box", b"sponson", b"station"]
# только «категорийные» подписи (не имена оружия)
LABELISH = re.compile(rb"^[A-Za-z][A-Za-z0-9 /().\-]{2,28}$")

def collect(path, sink):
    try:
        env = UnityPy.load(path)
        objs = list(env.objects)
    except Exception as e:
        print("!! не удалось загрузить", path, e)
        return
    n = 0
    for o in objs:
        try:
            raw = o.get_raw_data()
        except Exception:
            continue
        if len(raw) > 6000:
            continue
        if not any(t in raw.lower() for t in TOKENS):
            continue
        strs = []
        for s in re.findall(rb"[ -~]{3,40}", raw):
            if not LABELISH.match(s):
                continue
            strs.append(s.decode("ascii", "replace").strip())
        if not strs:
            continue
        # интересуют объекты-наборы подписей: >=2 «слотоподобных» строки
        if sum(1 for s in strs if any(t.decode() in s.lower() for t in TOKENS)) < 2:
            continue
        n += 1
        for s in strs:
            sink.setdefault(s, set()).add(o.type.name)
    print(f"{os.path.basename(path)}: объектов-наборов {n}, уникальных строк {len(sink)}")

if __name__ == "__main__":
    arg = sys.argv[1]
    sink = {}
    if arg == "--all-mods":
        root = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins"
        for dirpath, dirs, files in os.walk(root):
            if "LocalizationPatch" in dirpath:
                continue
            for f in files:
                if not f.lower().endswith(".dll"):
                    continue
                p = os.path.join(dirpath, f)
                data = io.open(p, "rb").read(4096)
                if b"UnityFS" not in io.open(p, "rb").read():
                    continue
                print("###", os.path.relpath(p, root))
                collect(p, sink)
    else:
        collect(arg, sink)
    print("=" * 80)
    print("ВСЕ КАНДИДАТЫ (%d):" % len(sink))
    for s in sorted(sink):
        print("   ", s)
