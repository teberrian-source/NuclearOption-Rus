# -*- coding: utf-8 -*-
"""Фикс наложения строк в меню управления (v3.3.2):
для строк списка действий принудительно отключаем перенос строк (TMP enableWordWrapping).
Причина: русские надписи на 30-80% шире английских и переносятся на 2 строки,
а высота строки в списке фиксирована, вторая строка ложится поверх соседней.
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

labels = [
    "None", "Controller:", "Assigned Controllers:", "Remove", "Calibrate",
    "Assign Controller", "Categories:", "Game", "Chat", "Mission Editor", "Debug",
    "Done", "Restore Defaults", "Actions", "Keyboard", "Mouse", "Controller",
    "Flight Controls", "Camera Controls", "Gameplay",
    "Pitch Axis", "Pitch Up", "Pitch Down", "Roll Axis", "Roll Right", "Roll Left",
    "Yaw Axis", "Yaw Right", "Yaw Left", "Throttle Axis", "Increase Throttle",
    "Decrease Throttle", "Brake Axis", "Apply Brakes", "Brake Axis -", "Custom Axis 1",
    "Custom Axis 1 Up", "Custom Axis 1 Down", "Fire", "Target Select", "Target Cancel",
    "Open Weapon Wheel", "Next Weapon", "Previous Weapon", "Link Guns",
    "Toggle Turret Control", "Next Countermeasure", "Countermeasures",
    "Open Radial Menu", "Eject", "Toggle Engine", "Toggle Flight Assist",
    "Toggle Gear", "Toggle Night Vision", "Toggle Radar", "Toggle Navigation Lights",
    "Axis Modifier", "Center View", "Switch View", "Tilt View", "Tilt Up", "Tilt Down",
    "Pan View", "Pan Right", "Pan Left", "Zoom View", "Zoom In", "Zoom Out",
    "Free Look", "Field of View", "Increase FoV", "Decrease FoV",
    "Move Longitudinal", "Move Forward", "Move Backward", "Move Lateral",
    "Move Right", "Move Left", "Move Vertical", "Move Up", "Move Down", "Camera Jump",
    "Look At Enemy Aircraft", "Jump to Enemy Aircraft", "Look At Target", "Pause",
    "Toggle Slow Motion", "Toggle Map", "Open Chat",
    "Move Map Horizontal", "Move Map Right", "Move Map Left", "Move Map Vertical",
    "Move Map Up", "Move Map Down",
    "Radial Menu Horizontal", "Radial Menu Right", "Radial Menu Left",
    "Radial Menu Vertical", "Radial Menu Up", "Radial Menu Down",
    "Submit Chat", "Cancel Chat", "Vote Kick Yes", "Vote Kick No",
    "Focus Unit", "Delete Unit", "Select Unit Mode", "Translate Unit Mode",
    "Rotate Unit Mode", "Toggle Left Panel", "Toggle mission debug menu",
    "Toggle debug graphs", "Toggle performance numbers",
    "Deploy Unit", "Next Unit", "Previous Unit", "Call Resupply",
    "Call Resupply - Player", "Deploy FOB", "Next Camera", "Previous Camera",
]
args = [("\"%s\"" % s) for s in labels]
rows = "".join(["\t\t" + ", ".join(args[i:i+4]) + ",\n" for i in range(0, len(args), 4)])

new_field = (
    "\tprivate static HashSet<string> traceLoggedMisses = new HashSet<string>();\n"
    "\tprivate static HashSet<string> traceLoggedHits = new HashSet<string>();\n\n"
    "\t/// <summary>Строки меню управления: русские подписи шире английских, перенос ломает список.</summary>\n"
    "\tprivate static readonly HashSet<string> mapperLabels = new HashSet<string>(new string[]\n\t{\n"
    + rows +
    "\t});\n\n"
    "\t/// <summary>Отключает перенос строк в TMP-лейбле (надпись одной строкой, без наложения).</summary>\n"
    "\tinternal static void DisableWordWrap(TMP_Text tmp)\n\t{\n"
    "\t\tif ((Object)(object)tmp == (Object)null)\n\t\t{\n\t\t\treturn;\n\t\t}\n"
    "\t\ttry\n\t\t{\n\t\t\ttmp.enableWordWrapping = false;\n\t\t}\n"
    "\t\tcatch (Exception ex)\n\t\t{\n"
    "\t\t\tLog.LogWarning((object)(\"DisableWordWrap failed: \" + ex.Message));\n\t\t}\n"
    "\t}\n"
)

sub1(
    "\tprivate static HashSet<string> traceLoggedMisses = new HashSet<string>();\n"
    "\tprivate static HashSet<string> traceLoggedHits = new HashSet<string>();\n",
    new_field,
    "список mapperLabels + helper DisableWordWrap",
)

# хук TMP_Text.text setter
sub1(
    "\t\t\tstring text = Translate(value);\n"
    "\t\t\tif (text != value)\n"
    "\t\t\t{\n"
    "\t\t\t\tvalue = text;\n"
    "\t\t\t\tif (FontReady && ContainsKorean(text))\n"
    "\t\t\t\t{\n"
    "\t\t\t\t\tEnsureKoreanFallback(__instance);\n"
    "\t\t\t\t}\n"
    "\t\t\t}\n",
    "\t\t\tstring text = Translate(value);\n"
    "\t\t\tif (mapperLabels.Contains(text.Trim()) || mapperLabels.Contains(value.Trim()))\n"
    "\t\t\t{\n"
    "\t\t\t\tDisableWordWrap(__instance);\n"
    "\t\t\t}\n"
    "\t\t\tif (text != value)\n"
    "\t\t\t{\n"
    "\t\t\t\tvalue = text;\n"
    "\t\t\t\tif (FontReady && ContainsKorean(text))\n"
    "\t\t\t\t{\n"
    "\t\t\t\t\tEnsureKoreanFallback(__instance);\n"
    "\t\t\t\t}\n"
    "\t\t\t}\n",
    "хук set_text: отключение переноса",
)

# хук TMP_Text.SetText(string, ...)
sub1(
    "\t\t\tstring text = Translate(sourceText);\n"
    "\t\t\tif (text != sourceText)\n"
    "\t\t\t{\n"
    "\t\t\t\tsourceText = text;\n"
    "\t\t\t\tif (FontReady && ContainsKorean(text))\n"
    "\t\t\t\t{\n"
    "\t\t\t\t\tEnsureKoreanFallback(__instance);\n"
    "\t\t\t\t}\n"
    "\t\t\t}\n",
    "\t\t\tstring text = Translate(sourceText);\n"
    "\t\t\tif (mapperLabels.Contains(text.Trim()) || mapperLabels.Contains(sourceText.Trim()))\n"
    "\t\t\t{\n"
    "\t\t\t\tDisableWordWrap(__instance);\n"
    "\t\t\t}\n"
    "\t\t\tif (text != sourceText)\n"
    "\t\t\t{\n"
    "\t\t\t\tsourceText = text;\n"
    "\t\t\t\tif (FontReady && ContainsKorean(text))\n"
    "\t\t\t\t{\n"
    "\t\t\t\t\tEnsureKoreanFallback(__instance);\n"
    "\t\t\t\t}\n"
    "\t\t\t}\n",
    "хук SetText(args): отключение переноса",
)

# версия 3.3.2
sub1("\"Localization Patch\", \"3.3.1\"", "\"Localization Patch\", \"3.3.2\"", "версия (BepInPlugin)")
sub1("Localization Patch v3.3.1 loaded", "Localization Patch v3.3.2 loaded", "версия (лог)")
sub1('GUILayout.Label("Localization Patch v3.3.1 (', 'GUILayout.Label("Localization Patch v3.3.2 (', "версия (окно)")

shutil.copy2(src, src + ".bak_" + datetime.datetime.now().strftime("%H%M%S"))
open(src, "wb").write((b"\xef\xbb\xbf" if bom else b"") + text.replace("\n", "\r\n").encode("utf-8"))
print("Plugin.cs записан, строк:", text.count("\n") + 1)
