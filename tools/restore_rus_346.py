# -*- coding: utf-8 -*-
"""Русификатор (хук-плагин 3.3.2) -> актуальная игра 0.34.6; + ключ версии 0.34.6 в словарь."""
import hashlib, io, json, os, re, shutil, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq NuclearOption.exe"], capture_output=True).stdout.decode("cp1251", "replace")
assert "NuclearOption.exe" not in out, "ИГРА ЗАПУЩЕНА — закрой игру и повтори"

desk = os.path.join(os.environ["USERPROFILE"], "Desktop")
store = os.path.join(desk, "NuclearOption_Rus_откат")
old_plug = os.path.join(desk, "Nuclear.Option.v0.34.3", "BepInEx", "plugins", "LocalizationPatch")
new_game = os.path.join(desk, "Nuclear.Option.v0.34.6", "BepInEx")
dst_plug = os.path.join(new_game, "plugins", "LocalizationPatch")
dst_cfg = os.path.join(new_game, "config", "com.noms.localizationpatch.cfg")

assert os.path.isdir(old_plug), "плагин не найден в старой 0.34.3"
shutil.move(old_plug, dst_plug)
print("плагин перемещён в 0.34.6:", dst_plug)

cfg_src = os.path.join(store, "из_игры", "com.noms.localizationpatch.cfg")
if os.path.isfile(cfg_src):
    shutil.move(cfg_src, dst_cfg)
print("конфиг установлен:", os.path.isfile(dst_cfg))

# ключ строки версии под новую игру
ru = os.path.join(dst_plug, "ru.json")
t = io.open(ru, encoding="utf-8-sig").read()
key = json.dumps("Early Access Version 0.34.6", ensure_ascii=False)
val = json.dumps("Ранний доступ, версия 0.34.6", ensure_ascii=False)
if key + ": " + val not in t:
    anchor = key.replace("0.34.6", "0.34.2") + ": " + val.replace("0.34.6", "0.34.2")
    assert anchor in t, "якорь версии 0.34.2 не найден"
    t = t.replace(anchor, anchor + ",\n    " + key + ": " + val, 1)
    io.open(ru, "w", encoding="utf-8", newline="\n").write(t)

# проверка как в валидаторе (//-комменты вне кавычек)
def parse_plugin_style(text):
    outl, in_str, esc, i = [], False, False, 0
    while i < len(text):
        c = text[i]
        if in_str:
            if esc: esc = False
            elif c == "\\": esc = True
            elif c == '"': in_str = False
            outl.append(c)
        else:
            if c == '"': in_str = True; outl.append(c)
            elif c == "/" and i + 1 < len(text) and text[i + 1] == "/":
                while i < len(text) and text[i] != "\n": i += 1
                continue
            else: outl.append(c)
        i += 1
    return json.loads("".join(outl), strict=False)

d = parse_plugin_style(io.open(ru, encoding="utf-8-sig").read())
print("словарь в 0.34.6:", len(d), "записей | ключ 0.34.6:", "Early Access Version 0.34.6" in d)
for f in ("LocalizationPatch.dll", "LocalizationPatchDropdown.dll", "WDXLLubrifontSC-Regular.ttf"):
    p = os.path.join(dst_plug, f)
    print(f, os.path.getsize(p), "Б sha16:", hashlib.sha256(open(p, "rb").read()).hexdigest()[:16].upper())
print("в старой 0.34.3 плагина больше нет:", not os.path.isdir(old_plug))
