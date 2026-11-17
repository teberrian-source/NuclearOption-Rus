# -*- coding: utf-8 -*-
"""Создаёт .cmd в папке игры: двойной клик = запуск с профайлером аллокаций.
Пользователь сам решает, когда запускать. Лог: alloc_profile\\alloc.mlpd"""
import os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
GAME = r"C:\Users\user\Desktop\Nuclear.Option.v0.34.6"
CMD = os.path.join(GAME, "Запустить с профилем аллокаций.cmd")

content = """@echo off
cd /d %~dp0
if not exist alloc_profile mkdir alloc_profile
set MONO_OPTIONS=--profile=log:alloc,logfile=%~dp0alloc_profile\\alloc.mlpd
start "" "NuclearOption.exe"
echo Игра запускается с профайлером аллокаций.
echo Лог появится в alloc_profile\\alloc.mlpd после ВЫХОДА из игры.
timeout /t 5 >nul
"""
io = open(CMD, "w", encoding="utf-8", newline="\r\n")
io.write(content)
io.close()
print("создан:", CMD)
print("проверка содержимого:")
print(open(CMD, encoding="utf-8").read())
