# -*- coding: utf-8 -*-
"""Проверка текущего состояния: версия DLL в игре, процесс игры, свежие строки лога."""
import hashlib, io, os, re, subprocess, sys, datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
GAME_DIR = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
LOG = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\LogOutput.log"

def h(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16].upper()

print("DLL в игре      :", os.path.getsize(os.path.join(GAME_DIR, "LocalizationPatch.dll")), "Б, sha16", h(os.path.join(GAME_DIR, "LocalizationPatch.dll")))
print("3.3.1 собранный :", "62 464 Б, 2D65BBC639241683")
print("3.3.2 собранный :", "67 072 Б, 6F712EFF7260D106")

out = subprocess.run(["tasklist"], capture_output=True).stdout.decode("cp1251", "replace")
running = [l.split()[0] for l in out.splitlines() if l.lower().startswith("nuclearoption")]
print("игра запущена   :", running or "нет")

lines = io.open(LOG, encoding="utf-8", errors="replace").read().split("\n")
print("строк в логе    :", len(lines))
print()
print("=== версии плагина в сессиях ===")
for i, l in enumerate(lines):
    if "Localization Patch v" in l:
        print("%6d | %s" % (i + 1, l.strip()[:120]))
print()
print("=== строки про тормоза/конфликты/диалоги (весь лог) ===")
pat = re.compile(r"Brake|Conflict|Replace|Assignment|Content Text|\bTitle\b|Rewired", re.I)
n = 0
for i, l in enumerate(lines):
    if pat.search(l) and "[TRACE]" in l or ("Rewired" in l and "Info" in l):
        n += 1
        if n <= 30:
            print("%6d | %s" % (i + 1, l.strip()[:150]))
print("всего совпадений:", n)
print()
print("=== последние 25 строк лога ===")
for i in range(max(0, len(lines) - 25), len(lines)):
    l = lines[i].strip()
    if l:
        print("%6d | %s" % (i + 1, l[:150]))
