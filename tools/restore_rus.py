# -*- coding: utf-8 -*-
"""Возврат русификатора в игру из папки отката + сверка хэшей."""
import hashlib, io, json, os, re, shutil, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq NuclearOption.exe"], capture_output=True).stdout.decode("cp1251", "replace")
assert "NuclearOption.exe" not in out, "ИГРА ЗАПУЩЕНА — закрой игру и повтори"

desk = os.path.join(os.environ["USERPROFILE"], "Desktop")
store = next(os.path.join(desk, d) for d in os.listdir(desk) if d.startswith("NuclearOption_Rus_"))
src = os.path.join(store, "из_игры")
game = os.path.join(desk, "Nuclear.Option.v0.34.3", "BepInEx")

moves = [
    (os.path.join(src, "LocalizationPatch"), os.path.join(game, "plugins", "LocalizationPatch")),
    (os.path.join(src, "com.noms.localizationpatch.cfg"), os.path.join(game, "config", "com.noms.localizationpatch.cfg")),
]
for s, d in moves:
    if os.path.isdir(s):
        shutil.move(s, d)
    elif os.path.isfile(s) and not os.path.exists(d):
        shutil.move(s, d)
    print("перемещено:", s, "->", d, "| целиком:", os.path.exists(d))

base = os.path.join(game, "plugins", "LocalizationPatch")
for f in ("LocalizationPatch.dll", "ru.json", "LocalizationPatchDropdown.dll", "WDXLLubrifontSC-Regular.ttf"):
    p = os.path.join(base, f)
    print(f, os.path.getsize(p), "sha16:", hashlib.sha256(open(p, "rb").read()).hexdigest()[:16].upper())
t = io.open(os.path.join(base, "ru.json"), encoding="utf-8-sig").read()
clean = "\n".join(re.sub(r"(?<!:)//.*", "", l) for l in t.splitlines())
print("записей в словаре:", len(json.loads(clean, strict=False)))
print("осталось в хранилище (из_игры):", os.listdir(src))
