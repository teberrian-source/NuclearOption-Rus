# -*- coding: utf-8 -*-
"""3.3.3: версия плагина + рескан по Ctrl+F5 (только по хоткею)."""
import io, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
P = r"C:\Users\user\Documents\NuclearOption_Rus\plugin\KoreanPatch\Plugin.cs"
t = io.open(P, encoding="utf-8-sig").read()

t = t.replace('"Localization Patch", "3.3.2"', '"Localization Patch", "3.3.3"')
t = t.replace("v3.3.2 loaded", "v3.3.3 loaded")
t = t.replace('"Localization Patch v3.3.2 ("', '"Localization Patch v3.3.3 ("')

old = (
    '\t\t\tLoadTranslations();\n'
    '\t\t\ttranslatedInstances.Clear();\n'
    '\t\t\tLog.LogInfo((object)$"Translations reloaded: {Translations.Count} entries");\n'
    '\t\t}'
)
new = (
    '\t\t\tLoadTranslations();\n'
    '\t\t\ttranslatedInstances.Clear();\n'
    '\t\t\tLog.LogInfo((object)$"Translations reloaded: {Translations.Count} entries");\n'
    '\t\t\ttry\n'
    '\t\t\t{\n'
    '\t\t\t\t// Рескан по хоткею (только Ctrl+F5): переводит надписи, которые\n'
    '\t\t\t\t// уже были установлены мимо хуков (описания миссий в браузере и т.п.).\n'
    '\t\t\t\t// Постоянного периодического скана нет — ноль нагрузки в фоне.\n'
    '\t\t\t\tScanAndTranslateAllText();\n'
    '\t\t\t\tLog.LogInfo((object)"[HB] Ctrl+F5 rescan finished");\n'
    '\t\t\t}\n'
    '\t\t\tcatch (Exception rescanEx)\n'
    '\t\t\t{\n'
    '\t\t\t\tLog.LogWarning((object)("Ctrl+F5 rescan failed: " + rescanEx.Message));\n'
    '\t\t\t}\n'
    '\t\t}'
)
assert old in t, "Ctrl+F5 block not found"
t = t.replace(old, new, 1)
io.open(P, "w", encoding="utf-8", newline="").write(t)
print("правки внесены; упоминаний 3.3.2 осталось:", t.count("3.3.2"))
