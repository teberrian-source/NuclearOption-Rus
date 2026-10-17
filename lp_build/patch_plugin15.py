# -*- coding: utf-8 -*-
"""Правки Plugin.cs: версия 3.2.4, хоткеи Ctrl+F4/F5/F6, расширенный белый список подписей."""
import io, re, sys, json, shutil, datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
src = r"C:\Users\user\AppData\Local\Temp\lp_build\KoreanPatch\Plugin.cs"
raw_bytes = open(src, "rb").read()
bom = raw_bytes.startswith(b"\xef\xbb\xbf")
text = raw_bytes.decode("utf-8-sig").replace("\r\n", "\n")
crlf = text.count("\r\n")
print("BOM:", bom, "| CRLF:", crlf, "| LF всего:", text.count("\n"))

def sub1(old, new, name):
    global text
    n = text.count(old)
    if n != 1:
        print(f"!! {name}: найдено {n} совпадений — ПРОПУСК")
        return False
    text = text.replace(old, new)
    print(f"ok {name}")
    return True

# 1. версия
sub1('"Localization Patch", "3.2.3"', '"Localization Patch", "3.2.4"', "версия (BepInPlugin)")
sub1('Localization Patch v3.2.3 loaded', 'Localization Patch v3.2.4 loaded', "версия (лог)")
sub1('GUILayout.Label("Localization Patch v3.2.3 (', 'GUILayout.Label("Localization Patch v3.2.4 (', "версия (окно)")

# 2. хоткеи
old_toggle = '''		if (Input.GetKeyDown((KeyCode)291) || Input.GetKeyDown((KeyCode)290))
		{
			showUI = !showUI;
			Log.LogInfo((object)$"UI toggle: {showUI}");
		}
		if (Input.GetKey((KeyCode)306) && Input.GetKeyDown((KeyCode)291))
		{
			LoadTranslations();
			translatedInstances.Clear();
			Log.LogInfo((object)$"Translations reloaded: {Translations.Count} entries");
		}
		if (Input.GetKey((KeyCode)306) && Input.GetKeyDown((KeyCode)292))
		{
			ExtractGameData();
		}
		if (Input.GetKey((KeyCode)306) && Input.GetKeyDown((KeyCode)293))
		{
			ExtractAllStrings();
		}'''
new_toggle = '''		if (!CtrlHeld() && (Input.GetKeyDown((KeyCode)290) || Input.GetKeyDown((KeyCode)291)))
		{
			showUI = !showUI;
			Log.LogInfo((object)$"UI toggle: {showUI}");
		}
		if (CtrlHeld() && (Input.GetKeyDown((KeyCode)286) || Input.GetKeyDown((KeyCode)291)))
		{
			LoadTranslations();
			translatedInstances.Clear();
			Log.LogInfo((object)$"Translations reloaded: {Translations.Count} entries");
		}
		if (CtrlHeld() && (Input.GetKeyDown((KeyCode)285) || Input.GetKeyDown((KeyCode)292)))
		{
			ExtractGameData();
		}
		if (CtrlHeld() && (Input.GetKeyDown((KeyCode)287) || Input.GetKeyDown((KeyCode)293)))
		{
			ExtractAllStrings();
		}'''
sub1(old_toggle, new_toggle, "хоткеи Ctrl+F4/F5/F6")

# 3. helper CtrlHeld рядом с DoPerFrameLogic
old_hdr = "	internal void DoPerFrameLogic()"
new_hdr = '''	/// <summary>Зажат ли Ctrl (левый или правый) — для горячих клавиш Ctrl+F4/F5/F6.</summary>
	internal static bool CtrlHeld()
	{
		return Input.GetKey((KeyCode)306) || Input.GetKey((KeyCode)305);
	}

	internal void DoPerFrameLogic()'''
sub1(old_hdr, new_hdr, "метод CtrlHeld")

# 4. белый список подписей
block = io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\label_keys.txt", encoding="utf-8").read().replace("\r\n", "\n").rstrip("\n")
m = re.search(r"\tprivate static readonly HashSet<string> LabelWithValueKeys = new HashSet<string>\n\t\{\n.*?\n\t\};", text, re.S)
if not m:
    print("!! старый блок LabelWithValueKeys не найден")
else:
    text = text[:m.start()] + block + text[m.end():]
    print("ok белый список подписей:", block.count('", "') + 1, "записей")

backup = src + ".bak_" + datetime.datetime.now().strftime("%H%M%S")
shutil.copy2(src, backup)
open(src, "wb").write((b"\xef\xbb\xbf" if bom else b"") + text.replace("\n", "\r\n").encode("utf-8"))
print("записано, бэкап:", backup)
