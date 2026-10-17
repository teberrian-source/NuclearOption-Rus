# -*- coding: utf-8 -*-
"""Проверяет текущую сессию: версия плагина, экспорты, время файлов."""
import io, os, sys, re, datetime

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx"
log = os.path.join(base, "LogOutput.log")
data = io.open(log, encoding="utf-8", errors="replace").read()
lines = data.split("\n")

print("=== старты плагина ===")
for l in lines:
    if "Loading [Loc" in l or "v3." in l and "Localization Patch" in l or "Exported" in l:
        print(" ", l.strip()[:150])

print("\n=== последний [HB] ===")
hb = [l for l in lines if "[HB]" in l and "Localization Patch" in l]
for l in hb[-2:]:
    print(" ", l.strip()[:200])

print("\n=== время файлов ===")
for f in ("LogOutput.log", r"plugins\LocalizationPatch\untranslated.txt",
          r"plugins\LocalizationPatch\ru.json", r"plugins\LocalizationPatch\LocalizationPatch.dll"):
    p = os.path.join(base, f)
    st = os.stat(p)
    print(f"  {f}: {datetime.datetime.fromtimestamp(st.st_mtime):%H:%M:%S}  {st.st_size} б")
print("  сейчас:", datetime.datetime.now().strftime("%H:%M:%S"))
