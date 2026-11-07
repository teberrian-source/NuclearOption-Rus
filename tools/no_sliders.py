# -*- coding: utf-8 -*-
"""Убрать пустые отступные строки после удаления ползунков; копия словаря в игры."""
import io, json, re, os, shutil, sys, subprocess

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_dict import parse_plugin_style

DICT = r"C:\Users\user\Documents\NuclearOption_Rus\dict\ru.json"
t = io.open(DICT, encoding="utf-8-sig").read()
# хвостовые "    \n" линии вокруг места бывших ползунков
t = re.sub(r"\n(?:[ \t]+\n)+", "\n", t)
io.open(DICT, "w", encoding="utf-8", newline="\n").write(t)
d = parse_plugin_style(io.open(DICT, encoding="utf-8-sig").read())
print("словарь: записей =", len(d), "| ползунок в словаре =", "Center Stabilization" in d)

# игра должна быть закрыта
out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq NuclearOption.exe"], capture_output=True).stdout.decode("cp1251", "replace")
assert "NuclearOption.exe" not in out, "ИГРА ЗАПУЩЕНА — закрой, потом перезапусти"
for game in [r"C:\Users\user\Desktop\Nuclear.Option.v0.34.3"]:
    if not os.path.isdir(game):
        print("папка игры не найдена, пропускаю:", game)
        continue
    dst = os.path.join(game, "BepInEx", "plugins", "LocalizationPatch", "ru.json")
    shutil.copy2(DICT, dst)
    gd = parse_plugin_style(io.open(dst, encoding="utf-8-sig").read())
    print("скопирован в:", game, "| записей в копии:", len(gd), "| ползунок:", "Center Stabilization" in gd)
