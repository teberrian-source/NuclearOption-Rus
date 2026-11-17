# -*- coding: utf-8 -*-
"""Попытка А, шаг 2: запуск с MONO_OPTIONS + самоконтроль.
Через 12 с проверяем, жив ли процесс; если умер — читаем хвост Player.log."""
import os, subprocess, sys, time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
GAME = r"C:\Users\user\Desktop\Nuclear.Option.v0.34.6"
EXE = os.path.join(GAME, "NuclearOption.exe")
PLAYER_LOG = os.path.join(os.environ.get("USERPROFILE", ""), r"AppData\LocalLow\Shockfront\Nuclear Option\Player.log")
MLPD = os.path.join(GAME, "alloc_profile", "alloc.mlpd")

os.makedirs(os.path.dirname(MLPD), exist_ok=True)
if os.path.exists(MLPD):
    os.remove(MLPD)

env = dict(os.environ)
env["MONO_OPTIONS"] = "--profile=log:alloc,logfile=" + MLPD
proc = subprocess.Popen([EXE], cwd=GAME, env=env)
print("PID", proc.pid, "| MONO_OPTIONS =", env["MONO_OPTIONS"])
time.sleep(12)

alive = subprocess.run(["tasklist", "/FI", f"PID eq {proc.pid}"],
                       capture_output=True, text=True).stdout
if str(proc.pid) in alive:
    print("процесс ЖИВ через 12 с — профайлер принят, играй 2-3 мин и скажи 'смотри'")
    if os.path.exists(MLPD):
        print(".mlpd уже пишется:", os.path.getsize(MLPD) // 1024, "КБ")
    else:
        print(".mlpd пока нет (может создаться позже)")
    sys.exit(0)

print("процесс УМЕР. Ищем причину...")
if os.path.exists(PLAYER_LOG):
    tail = open(PLAYER_LOG, encoding="utf-8", errors="replace").read()[-2000:]
    print("--- Player.log (хвост) ---")
    print(tail)
else:
    print("Player.log не найден:", PLAYER_LOG)
    for f in os.listdir(GAME):
        if f.lower().endswith(".txt") or "error" in f.lower():
            print("  кандидат:", f)
