# -*- coding: utf-8 -*-
"""Ищет копии ru.json / архивов LocalizationPatch вне папки игры (кеш менеджера модов)."""
import os, sys, datetime

sys.stdout.reconfigure(encoding="utf-8")
roots = [
    r"C:\Users\user\Desktop",
    r"C:\Users\user\Documents",
    r"C:\Users\user\Downloads",
    r"C:\Users\user\AppData\Local",
    r"C:\Users\user\AppData\Roaming",
    r"C:\Users\user\AppData\LocalLow\Shockfront",
]
SKIP_DIR = ("NuclearOption_0.34.2", "__pycache__", "node_modules")
hits = []
for root in roots:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR]
        for name in filenames:
            low = name.lower()
            if low == "ru.json" or ("localization" in low and low.endswith((".zip", ".json", ".txt"))) or "nomodmanager" in low:
                p = os.path.join(dirpath, name)
                try:
                    st = os.stat(p)
                except Exception:
                    continue
                hits.append((st.st_mtime, st.st_size, p))
hits.sort(reverse=True)
print(f"найдено: {len(hits)}")
for mtime, size, p in hits[:40]:
    print(f"  {datetime.datetime.fromtimestamp(mtime):%d.%m %H:%M:%S}  {size:>8} б  {p}")

print()
print("--- папки с 'mod' в имени (ищем кеш менеджера) ---")
for root in [r"C:\Users\user\AppData\Local", r"C:\Users\user\AppData\Roaming", r"C:\Users\user\Documents"]:
    try:
        for name in os.listdir(root):
            low = name.lower()
            if "mod" in low and "node" not in low:
                print("  ", os.path.join(root, name))
    except Exception:
        pass
