# -*- coding: utf-8 -*-
"""Установка v3.3.1 в игру, настройка конфига и уборка папки плагина."""
import glob, io, os, shutil, sys, time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
REPO = r"C:\Users\user\Documents\NuclearOption_Rus"
GAME = r"C:\Users\user\Desktop\NuclearOption_0.34.2"
PLUG = os.path.join(GAME, r"BepInEx\plugins\LocalizationPatch")
BACK = os.path.join(REPO, "backups")

# --- 1. DLL -------------------------------------------------------------
new = os.path.join(REPO, r"plugin\bin\Release\LocalizationPatch.dll")
dst = os.path.join(PLUG, "LocalizationPatch.dll")
stamp = time.strftime("%H%M%S")
shutil.copy2(dst, dst + ".bak_" + stamp)
shutil.copy2(new, dst)
shutil.copy2(new, os.path.join(REPO, r"plugin\build\LocalizationPatch.dll"))
print("DLL:", os.path.getsize(dst), "байт (бэкап .bak_%s)" % stamp)

# --- 2. Конфиг ----------------------------------------------------------
cfg = os.path.join(GAME, r"BepInEx\config\com.noms.localizationpatch.cfg")
if os.path.isfile(cfg):
    raw = open(cfg, "rb").read()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig").replace("\r\n", "\n").rstrip("\n")
    adds = []
    if "ShowDebugWindow" not in text:
        adds += ["", "## Показывать окно отладки (переключение по F9/F10). Игрокам не нужно.",
                 "# Setting type: Boolean", "# Default value: false", "ShowDebugWindow = false"]
    if "VerboseLog" not in text:
        adds += ["", "## Подробные [TRACE] логи и периодическая выгрузка untranslated.txt (для доработки перевода).",
                 "# Setting type: Boolean", "# Default value: false", "VerboseLog = true"]
    if adds:
        open(cfg, "wb").write((b"\xef\xbb\xbf" if bom else b"") + (text + "\n" + "\n".join(adds) + "\n").encode("utf-8"))
        print("конфиг дополнен:", [a for a in adds if "=" in a])
    else:
        print("конфиг уже содержит нужные ключи")
else:
    print("нет файла конфига — BepInEx создаст его сам при запуске")

# --- 3. Уборка в папке плагина -----------------------------------------
os.makedirs(BACK, exist_ok=True)
junk = ["final.txt", "final_u.txt", "rd.txt", "rd_u.txt"]
for f in junk:
    p = os.path.join(PLUG, f)
    if os.path.isfile(p):
        os.remove(p)
        print("удалён мусорный файл:", f)

def archive(pattern, keep):
    files = sorted(glob.glob(os.path.join(PLUG, pattern)), key=os.path.getmtime)
    for p in files[:-keep]:
        target = os.path.join(BACK, os.path.basename(p))
        if os.path.exists(target):
            os.remove(p)
        else:
            shutil.move(p, target)
        print("в архив:", os.path.basename(p))

archive("ru.backup_*.json", 2)
archive("LocalizationPatch.dll.bak_*", 1)

print()
print("в папке плагина осталось:")
for f in sorted(os.listdir(PLUG)):
    p = os.path.join(PLUG, f)
    print("  {:42s} {:>10s}".format(f, "{:,} Б".format(os.path.getsize(p)) if os.path.isfile(p) else "<папка>"))
print("в backups:", len(os.listdir(BACK)), "файлов")
