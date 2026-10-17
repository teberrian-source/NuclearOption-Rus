# -*- coding: utf-8 -*-
"""Разбор AssetBundle: ищем TextAsset'ы с описаниями миссий."""
import io, sys, os, time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import UnityPy

UnityPy.config.FALLBACK_UNITY_VERSION = "2022.3.62f1"

bundle = r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data\StreamingAssets\aa\StandaloneWindows64\defaultlocalgroup_assets_all_4f72d928a181be6a6cb9aee9ac38f476.bundle"
t0 = time.time()
env = UnityPy.load(bundle)
print("загружено за %.1f с" % (time.time() - t0))

needle = "catapults of a Penumbra-class"
counts = {}
found = []
for obj in env.objects:
    counts[obj.type.name] = counts.get(obj.type.name, 0) + 1
print("типов объектов:", sorted(counts.items(), key=lambda x: -x[1])[:15])

out = []
for obj in env.objects:
    if obj.type.name not in ("TextAsset", "MonoBehaviour"):
        continue
    try:
        data = obj.read()
    except Exception:
        continue
    name = getattr(data, "m_Name", "") or ""
    text = getattr(data, "m_Script", None) or getattr(data, "script", None)
    if isinstance(text, bytes):
        try:
            text = text.decode("utf-8")
        except Exception:
            continue
    if not isinstance(text, str) or not text:
        continue
    out.append((name, len(text), text))
    if needle in text:
        found.append(name)

print("текстовых объектов:", len(out), "| с искомой строкой:", found[:5])
with io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\bundle_texts.txt", "w", encoding="utf-8", newline="\n") as f:
    for name, ln, text in sorted(out, key=lambda x: -x[1])[:400]:
        f.write(f"##### {name} ({ln})\n{text}\n\n")
print("сохранено в bundle_texts.txt")
