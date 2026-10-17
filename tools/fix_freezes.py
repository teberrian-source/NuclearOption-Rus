# -*- coding: utf-8 -*-
"""Фикс зависаний: авто-выгрузки только по флагу в конфиге (по умолчанию выключены). Версия 3.3.0."""
import io, re, sys, shutil, datetime

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

# 1. Версия
sub1('"Localization Patch", "3.2.4"', '"Localization Patch", "3.3.0"', "версия (BepInPlugin)")
sub1('Localization Patch v3.2.4 loaded', 'Localization Patch v3.3.0 loaded', "версия (лог)")
sub1('GUILayout.Label("Localization Patch v3.2.4 (', 'GUILayout.Label("Localization Patch v3.3.0 (', "версия (окно)")

# 2. Поле конфига
sub1("\tprivate ConfigEntry<string> languageConfig;\n",
     "\tprivate ConfigEntry<string> languageConfig;\n\n"
     "\t/// <summary>Авто-выгрузка определений при запуске (по умолчанию выключена — она подвешивает игру).</summary>\n"
     "\tprivate ConfigEntry<bool> autoDumpConfig;\n",
     "поле autoDumpConfig")

# 3. Привязка конфига
sub1('\t\tCurrentLanguage = languageConfig.Value.ToLower().Trim();\n',
     '\t\tCurrentLanguage = languageConfig.Value.ToLower().Trim();\n'
     '\t\tautoDumpConfig = ((BaseUnityPlugin)this).Config.Bind<bool>("General", "AutoDump", false,\n'
     '\t\t\t"Авто-выгрузка определений игры при запуске (extracted_gamedata.txt, extracted_strings.txt). "\n'
     '\t\t\t+ "Сканирует все объекты игры рефлексией и подвешивает игру примерно на 10-20 секунд, 3 прохода. "\n'
     '\t\t\t+ "Обычно не нужно: выгрузка доступна по Ctrl+F4 и Ctrl+F6.");\n',
     "привязка AutoDump")

# 4. Условие авто-выгрузки
sub1("\t\tif (Enabled && autoDumpCount < 3 && Time.time >= nextAutoDumpTime)\n",
     "\t\tif (Enabled && autoDumpConfig != null && autoDumpConfig.Value && autoDumpCount < 3 && Time.time >= nextAutoDumpTime)\n",
     "условие авто-выгрузки")

shutil.copy2(src, src + ".bak_" + datetime.datetime.now().strftime("%H%M%S"))
open(src, "wb").write((b"\xef\xbb\xbf" if bom else b"") + text.replace("\n", "\r\n").encode("utf-8"))
print("Plugin.cs записан, строк:", text.count("\n") + 1)

# 5. csproj: путь к игре через $(UserProfile) — не ломается при переносе папки
cs = r"C:\Users\user\Documents\NuclearOption_Rus\plugin\LocalizationPatch.csproj"
raw_cs = open(cs, "rb").read().decode("utf-8-sig")
n = raw_cs.count(r"..\..\..\..\Desktop\NuclearOption_0.34.2")
raw_cs = raw_cs.replace(r"..\..\..\..\Desktop\NuclearOption_0.34.2", r"$(UserProfile)\Desktop\NuclearOption_0.34.2")
open(cs, "wb").write(raw_cs.encode("utf-8"))
print("csproj: поправлено ссылок на игру:", n)
