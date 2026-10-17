# -*- coding: utf-8 -*-
"""Поиск строк миссий в сырых данных объектов AssetBundle (после распаковки LZ4)."""
import io, re, sys, time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import UnityPy

UnityPy.config.FALLBACK_UNITY_VERSION = "2022.3.62f1"
aa = r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data\StreamingAssets\aa\StandaloneWindows64"
bundles = ["defaultlocalgroup_assets_all_4f72d928a181be6a6cb9aee9ac38f476.bundle",
           "skins_assets_all_88de9169e4d0cdc55253aeff4b669446.bundle"]
needles = [b"Penumbra-class", b"Ingress Via Mountains", b"Ternion"]

ascii_run = re.compile(rb"[\x20-\x7E]{25,}")

for b in bundles:
    t0 = time.time()
    env = UnityPy.load(aa + "\\" + b)
    n = 0
    hits = 0
    texts = []
    for obj in env.objects:
        n += 1
        try:
            raw = obj.get_raw_data()
        except Exception:
            continue
        if not raw:
            continue
        for nd in needles:
            if nd in raw:
                hits += 1
                break
        for m in ascii_run.finditer(raw):
            s = m.group(0)
            if b" " in s and len(s) >= 40:
                texts.append(s.decode("ascii", "replace"))
    print(b[:20], "объектов:", n, "| с искомой строкой:", hits, "| строк:", len(texts), "| %.1f с" % (time.time() - t0))
    if hits:
        io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\bundle_raw_" + b[:12] + ".txt", "w",
                encoding="utf-8", newline="\n").write("\n".join(sorted(set(texts))))
