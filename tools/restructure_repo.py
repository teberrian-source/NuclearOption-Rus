# -*- coding: utf-8 -*-
"""Раскладка репозитория русификатора по папкам + удаление сборного мусора."""
import io, os, sys, shutil

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
root = r"C:\Users\user\Documents\NuclearOption_Rus"
lp = os.path.join(root, "lp_build")

# 1. Мусор: пустые файлы, .bak-копии, артефакты сборки
removed = []
for base, dirs, files in os.walk(root):
    if ".git" in base.split(os.sep):
        continue
    for d in list(dirs):
        if d in ("obj", "bin", "unpack"):
            p = os.path.join(base, d)
            if d == "unpack":
                shutil.rmtree(p, ignore_errors=True)
                removed.append(p + " (папка, 328 МБ распакованных ассетов)")
                continue
            shutil.rmtree(p, ignore_errors=True)
            removed.append(p + " (папка сборки)")
    for f in files:
        p = os.path.join(base, f)
        try:
            empty = os.path.getsize(p) == 0
        except OSError:
            continue
        if empty or ".bak_" in f:
            os.remove(p)
            removed.append(p + (" (пустой)" if empty else " (бэкап)"))

# 2. Новые папки
for d in ("dict", "plugin", "tools", "data"):
    os.makedirs(os.path.join(root, d), exist_ok=True)

def move(path, dest_dir):
    if not os.path.exists(path):
        return
    shutil.move(path, os.path.join(dest_dir, os.path.basename(path)))

# 3. Плагин
for name in ("KoreanPatch", "LocalizationPatch.csproj", "Properties", "regex_test", "build"):
    move(os.path.join(lp, name), os.path.join(root, "plugin"))

# 4. Скрипты
for base, dirs, files in os.walk(lp):
    for f in files:
        if f.endswith((".py", ".ps1", ".js")):
            move(os.path.join(base, f), os.path.join(root, "tools"))

# 5. Данные (выгрузки, пакеты перевода)
ext_data = (".txt", ".jsonl", ".json", ".csv", ".xml")
for base, dirs, files in os.walk(lp):
    for f in files:
        if f.endswith(ext_data):
            move(os.path.join(base, f), os.path.join(root, "data"))

# 6. Словарь
move(os.path.join(root, "ru.json"), os.path.join(root, "dict"))

# 7. Если lp_build опустел — убрать
left = []
for base, dirs, files in os.walk(lp):
    left += [os.path.join(base, f) for f in files]
if not left:
    shutil.rmtree(lp, ignore_errors=True)
else:
    print("В lp_build осталось файлов:", len(left))

print("удалено мусора:", len(removed))
for r in removed[:10]:
    print("  ", r.replace(root + "\\", ""))
print()
for d in ("dict", "plugin", "tools", "data"):
    n = sum(len(f) for _, _, f in os.walk(os.path.join(root, d)))
    print("{:8s} файлов: {}".format(d, n))
