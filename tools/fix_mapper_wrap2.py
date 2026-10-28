# -*- coding: utf-8 -*-
"""Вторая часть фикса v3.3.2: вставка вызова DisableWordWrap в два TMP-хука
(первый insert с шириной 3 таба не совпал — там 4 таба)."""
import io, shutil, sys, datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
src = r"C:\Users\user\Documents\NuclearOption_Rus\plugin\KoreanPatch\Plugin.cs"
raw = open(src, "rb").read()
bom = raw.startswith(b"\xef\xbb\xbf")
text = raw.decode("utf-8-sig").replace("\r\n", "\n")

def sub1(old, new, name):
    global text
    n = text.count(old)
    if n != 1:
        print(f"!! {name}: найдено {n} — ПРОПУСК")
        return False
    text = text.replace(old, new)
    print("ok", name)
    return True

sub1(
    "\t\t\t\tstring text = Translate(value);\n\t\t\t\tif (text != value)\n",
    "\t\t\t\tstring text = Translate(value);\n"
    "\t\t\t\tif (mapperLabels.Contains(text.Trim()) || mapperLabels.Contains(value.Trim()))\n"
    "\t\t\t\t{\n"
    "\t\t\t\t\tDisableWordWrap(__instance);\n"
    "\t\t\t\t}\n"
    "\t\t\t\tif (text != value)\n",
    "хук set_text: отключение переноса",
)

sub1(
    "\t\t\t\tstring text = Translate(sourceText);\n\t\t\t\tif (text != sourceText)\n",
    "\t\t\t\tstring text = Translate(sourceText);\n"
    "\t\t\t\tif (mapperLabels.Contains(text.Trim()) || mapperLabels.Contains(sourceText.Trim()))\n"
    "\t\t\t\t{\n"
    "\t\t\t\t\tDisableWordWrap(__instance);\n"
    "\t\t\t\t}\n"
    "\t\t\t\tif (text != sourceText)\n",
    "хук SetText(args): отключение переноса",
)

shutil.copy2(src, src + ".bak_" + datetime.datetime.now().strftime("%H%M%S"))
open(src, "wb").write((b"\xef\xbb\xbf" if bom else b"") + text.replace("\n", "\r\n").encode("utf-8"))
print("Plugin.cs записан, строк:", text.count("\n") + 1)
