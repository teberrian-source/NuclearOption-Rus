# -*- coding: utf-8 -*-
"""Считает записи в ru.json (текущем, бэкапах, безопасной копии) и показывает даты."""
import io, re, sys, json, os, glob, datetime

sys.stdout.reconfigure(encoding="utf-8")
paths = [
    r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch\ru.json",
    r"C:\Users\user\Documents\NuclearOption_Rus\ru.json",
    r"C:\Users\user\AppData\Local\Temp\lp_build\ru_safe_3116.json",
]
for p in paths:
    if not os.path.exists(p):
        print("нет:", p)
        continue
    st = os.stat(p)
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    try:
        data = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)
        cnt = f"{len(data)} записей"
    except Exception as e:
        cnt = "ОШИБКА JSON: " + str(e)[:60]
    print(f"{cnt:>16}  {st.st_size:>7} б  {datetime.datetime.fromtimestamp(st.st_mtime):%d.%m %H:%M:%S}  {p}")

print()
print("--- бэкапы в папке плагина ---")
for p in sorted(glob.glob(r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch\ru.backup_*.json")):
    st = os.stat(p)
    print(f"  {st.st_size:>7} б  {datetime.datetime.fromtimestamp(st.st_mtime):%d.%m %H:%M:%S}  {os.path.basename(p)}")
