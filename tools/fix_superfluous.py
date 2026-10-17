# -*- coding: utf-8 -*-
"""Убирает лишнее из релиза плагина (v3.3.1):
окно отладки — по флагу ShowDebugWindow, TRACE-логи и untranslated.txt — по флагу VerboseLog.
Оба по умолчанию выключены; логика перевода не затрагивается.
"""
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

# --- версия -------------------------------------------------------------
sub1('"Localization Patch", "3.3.0"', '"Localization Patch", "3.3.1"', "версия (BepInPlugin)")
sub1("Localization Patch v3.3.0 loaded", "Localization Patch v3.3.1 loaded", "версия (лог)")
sub1('GUILayout.Label("Localization Patch v3.3.0 (', 'GUILayout.Label("Localization Patch v3.3.1 (', "версия (окно)")

# --- поля конфига -------------------------------------------------------
sub1("\tprivate ConfigEntry<bool> autoDumpConfig;\n",
     "\tprivate ConfigEntry<bool> autoDumpConfig;\n\n"
     "\tprivate ConfigEntry<bool> debugWindowConfig;\n\n"
     "\tprivate ConfigEntry<bool> verboseLogConfig;\n\n"
     "\t/// <summary>Окно отладки разрешено (ShowDebugWindow = true).</summary>\n"
     "\tinternal static bool WindowAllowed;\n\n"
     "\t/// <summary>Подробные логи и выгрузка untranslated.txt (VerboseLog = true).</summary>\n"
     "\tinternal static bool Verbose;\n",
     "поля конфига")

# --- привязка конфига ---------------------------------------------------
sub1('\t\t\t+ "Обычно не нужно: выгрузка доступна по Ctrl+F4 и Ctrl+F6.");\n',
     '\t\t\t+ "Обычно не нужно: выгрузка доступна по Ctrl+F4 и Ctrl+F6.");\n'
     '\t\tdebugWindowConfig = ((BaseUnityPlugin)this).Config.Bind<bool>("General", "ShowDebugWindow", false,\n'
     '\t\t\t"Показывать окно отладки (переключение по F9/F10). Игрокам не нужно.");\n'
     '\t\tverboseLogConfig = ((BaseUnityPlugin)this).Config.Bind<bool>("General", "VerboseLog", false,\n'
     '\t\t\t"Подробные [TRACE] логи и периодическая выгрузка untranslated.txt (для доработки перевода).");\n'
     '\t\tWindowAllowed = debugWindowConfig.Value;\n'
     '\t\tVerbose = verboseLogConfig.Value;\n',
     "привязка ShowDebugWindow/VerboseLog")

# --- хоткей окна только при разрешённом окне ----------------------------
sub1("\t\tif (!CtrlHeld() && (Input.GetKeyDown((KeyCode)290) || Input.GetKeyDown((KeyCode)291)))\n",
     "\t\tif (WindowAllowed && !CtrlHeld() && (Input.GetKeyDown((KeyCode)290) || Input.GetKeyDown((KeyCode)291)))\n",
     "хоткей окна")

# --- пульс в лог только в подробном режиме ------------------------------
sub1('\t\t\tLog.LogInfo((object)$"[HB] Enabled={Enabled} isPatching={isPatching} translated={translatedCount} missed={missedCount} untranslated={untranslatedStrings.Count} scanUntil={sceneScanUntilTime:F1} now={Time.time:F1} hooks={hookLogCount} {DescribePatches()}");\n',
     '\t\t\tif (Verbose)\n'
     '\t\t\t{\n'
     '\t\t\t\tLog.LogInfo((object)$"[HB] Enabled={Enabled} isPatching={isPatching} translated={translatedCount} missed={missedCount} untranslated={untranslatedStrings.Count} scanUntil={sceneScanUntilTime:F1} now={Time.time:F1} hooks={hookLogCount} {DescribePatches()}");\n'
     '\t\t\t}\n',
     "пульс [HB] в лог")

# --- TRACE hit ----------------------------------------------------------
sub1("\t\t\tif (traceLoggedHits.Count < 1500 && traceLoggedHits.Add(text))\n",
     "\t\t\tif (Verbose && traceLoggedHits.Count < 1500 && traceLoggedHits.Add(text))\n",
     "TRACE hit")

# --- сбор непереведённых и TRACE miss ----------------------------------
sub1("\t\t\tif (Instance.untranslatedStrings.Count < 100000)\n",
     "\t\t\tif (Verbose && Instance.untranslatedStrings.Count < 100000)\n",
     "сбор untranslated")
sub1("\t\t\tif (traceLoggedMisses.Count < 2000 && traceLoggedMisses.Add(text))\n",
     "\t\t\tif (Verbose && traceLoggedMisses.Count < 2000 && traceLoggedMisses.Add(text))\n",
     "TRACE miss")

# --- авто-выгрузка untranslated.txt раз в 60 с -------------------------
sub1("\t\tif (Enabled && Time.time - lastAutoExportTime > 60f)\n",
     "\t\tif (Enabled && Verbose && Time.time - lastAutoExportTime > 60f)\n",
     "авто-выгрузка untranslated.txt")

# --- рисование окна ----------------------------------------------------
sub1("\t\tif (showUI)\n", "\t\tif (showUI && WindowAllowed)\n", "рисование окна")

# --- подпись кнопки ----------------------------------------------------
sub1('GUILayout.Button("Reload translations (Ctrl+F10)"', 'GUILayout.Button("Reload translations (Ctrl+F5)"', "подпись кнопки")

shutil.copy2(src, src + ".bak_" + datetime.datetime.now().strftime("%H%M%S"))
open(src, "wb").write((b"\xef\xbb\xbf" if bom else b"") + text.replace("\n", "\r\n").encode("utf-8"))
print("Plugin.cs записан, строк:", text.count("\n") + 1)
