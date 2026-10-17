# -*- coding: utf-8 -*-
"""Полный проход: вытаскивает встроенные Unity-бандлы из модовых сборок и собирает подписи слотов.

Результат: C:\\Users\\user\\AppData\\Local\\Temp\\lp_build\\mod_labels.txt
"""
import io, os, re, struct, sys

sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
UnityPy.config.FALLBACK_UNITY_VERSION = "2022.3.62f1"

root = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins"
outdir = r"C:\Users\user\AppData\Local\Temp\lp_build\unpack"
os.makedirs(outdir, exist_ok=True)

TOKENS = [b"subturret", b"coax", b"pylon", b"mount", b"turret", b"cargo", b"hardpoint",
          b"bay", b"hook", b"rack", b"ammo", b"sponson", b"station"]
LABELISH = re.compile(rb"^[A-Za-z][A-Za-z0-9 /().\-]{2,28}$")

sink = {}
report = []

def groups_of(path):
    """Возвращает список (тип, строки) для объектов-наборов подписей."""
    env = UnityPy.load(path)
    out = []
    for o in env.objects:
        try:
            raw = o.get_raw_data()
        except Exception:
            continue
        if len(raw) > 6000:
            continue
        if not any(t in raw.lower() for t in TOKENS):
            continue
        strs = [s.decode("ascii", "replace").strip() for s in re.findall(rb"[ -~]{3,40}", raw) if LABELISH.match(s)]
        if sum(1 for s in strs if any(t.decode() in s.lower() for t in TOKENS)) < 2:
            continue
        out.append((o.type.name, strs))
    return out

def extract_bundles(p):
    """Нарезает встроенные UnityFS-бандлы из PE-файла, возвращает список путей."""
    data = io.open(p, "rb").read()
    res = []
    for m in re.finditer(b"UnityFS\x00", data):
        off = m.start()
        try:
            pos = off + 8
            version = struct.unpack_from(">i", data, pos)[0]; pos += 4
            end = data.index(b"\x00", pos)
            unityver = data[pos:end].decode("latin1"); pos = end + 1
            end = data.index(b"\x00", pos)
            unityrev = data[pos:end].decode("latin1"); pos = end + 1
            size = struct.unpack_from(">q", data, pos)[0]
        except Exception:
            continue
        if size <= 0 or off + size > len(data):
            size = len(data) - off
        fn = os.path.join(outdir, f"{os.path.basename(p)}.{off}.unity3d")
        if not os.path.exists(fn) or os.path.getsize(fn) != size:
            io.open(fn, "wb").write(data[off:off + size])
        res.append(fn)
    return res

for dirpath, dirs, files in os.walk(root):
    if "LocalizationPatch" in dirpath:
        continue
    for f in files:
        if not f.lower().endswith(".dll"):
            continue
        p = os.path.join(dirpath, f)
        head = io.open(p, "rb").read()
        if b"UnityFS" not in head:
            continue
        rel = os.path.relpath(p, root)
        print("###", rel, flush=True)
        for b in extract_bundles(p):
            try:
                gs = groups_of(b)
            except Exception as e:
                print("   !! ошибка", b, e, flush=True)
                continue
            print("   ", os.path.basename(b), "групп:", len(gs), flush=True)
            for t, strs in gs:
                for s in strs:
                    sink.setdefault(s, set()).add(f"{rel}:{t}")

with io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\mod_labels.txt", "w", encoding="utf-8") as fh:
    fh.write("ВСЕ КАНДИДАТЫ (%d)\n" % len(sink))
    for s in sorted(sink):
        fh.write("%s\t%s\n" % (s, ",".join(sorted(sink[s]))))
print("готово, кандидатов:", len(sink))
