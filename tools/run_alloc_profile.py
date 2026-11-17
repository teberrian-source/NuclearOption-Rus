# -*- coding: utf-8 -*-
"""Запуск игры с Mono-профайлером аллокаций (попытка А).
MONO_OPTIONS=--profile=log:alloc,logfile=<abs path>.mlpd
Выход: <game>\\alloc_profile\\alloc.mlpd, если профайлер собран в Mono."""
import os, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
GAME = r"C:\Users\user\Desktop\Nuclear.Option.v0.34.6"
EXE = os.path.join(GAME, "NuclearOption.exe")
OUTDIR = os.path.join(GAME, "alloc_profile")
MLPD = os.path.join(OUTDIR, "alloc.mlpd")

if not os.path.isfile(EXE):
    print("не найден:", EXE)
    sys.exit(1)

os.makedirs(OUTDIR, exist_ok=True)
if os.path.exists(MLPD):
    os.remove(MLPD)

env = dict(os.environ)
env["MONO_OPTIONS"] = "--profile=log:alloc,logfile=" + MLPD
env["MONO_PATH"] = env.get("MONO_PATH", "")

proc = subprocess.Popen([EXE], cwd=GAME, env=env)
print("игра запущена, PID", proc.pid)
print("MONO_OPTIONS =", env["MONO_OPTIONS"])
print("ждём .mlpd:", MLPD)
print("через 2-3 минуты игры скажи 'смотри' — проверю, что лог пишется")
