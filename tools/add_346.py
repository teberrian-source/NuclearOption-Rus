# -*- coding: utf-8 -*-
"""Добавление переводов со скринов 0.34.6: пилоны/отсеки, Recent, описания самолётов.
Правка кривого 'Форвард Бэй'. Обновляет dict/ru.json в репо и копирует в игру 0.34.6."""
import io, json, os, re, shutil, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT = os.path.join(REPO, "dict", "ru.json")
desk = os.path.join(os.environ["USERPROFILE"], "Desktop")
GAME_RU = os.path.join(desk, "Nuclear.Option.v0.34.6", "BepInEx", "plugins", "LocalizationPatch", "ru.json")

NEW = {
    # --- подписи точек подвески / отсеков ---
    "Centreline": "Центральный пилон",
    "CenterLine Pylon": "Центральный пилон",
    "Middle Pylons": "Средние пилоны",
    "Wingtips": "Законцовки крыла",
    "Wingtip": "Законцовка крыла",
    "Aft Bay": "Кормовой отсек",
    "Laser C-RAM": "Лазерный C-RAM",
    # --- браузер миссий ---
    "Recent": "Недавние",
    # --- описания самолётов ---
    "A twin-engine, fourth-generation air superiority fighter. The MiG-29 Fulcrum trades range and payload for agility: a high thrust-to-weight ratio and a blended lifting body give it superb low-speed handling in close-range dogfights.":
        "Двухдвигательный истребитель четвёртого поколения для завоевания превосходства в воздухе. MiG-29 Fulcrum жертвует дальностью и полезной нагрузкой ради манёвренности: высокая тяговооружённость и интегральный несущий корпус дают отличную управляемость на малых скоростях в ближнем бою.",
    "An older but proven design dating back to the Primevan revolution. The Agni is a single engine all-weather fighter featuring a large array of hardpoints for flexibility. Without any internal weapon bays the aircraft is easier to detect than more modern designs.":
        "Более старая, но проверенная разработка времён Примеванской революции. Agni — всепогодный истребитель с одним двигателем и большим набором точек подвески для гибкости. Без внутренних оружейных отсеков самолёт заметнее, чем более современные машины.",
    "Long-endurance multirole bomber with a telescoping high wing, two geared turbofans, nose and tail radars, and a laser point-defence turret. Carries bombs or cruise missiles in two internal bays, or an AWACS radome.":
        "Многоцелевой бомбардировщик большой продолжительности полёта с телескопическим верхним крылом, двумя редукторными турбовентиляторными двигателями, носовой и хвостовой РЛС и лазерной турелью ближней обороны. Возит бомбы или крылатые ракеты в двух внутренних отсеках, либо радом ДРЛО.",
    "MiG-15s in the big '85 :wilt: :sob:":
        "МиГ-15 в большом '85 :wilt: :sob:",
}

# правка старого кривого перевода
FIX = {"Forward Bay": ("Форвард Бэй", "Передний отсек")}

t = io.open(DICT, encoding="utf-8-sig").read()
added = []
for k, v in NEW.items():
    if json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False) in t:
        continue
    added.append((k, v))
print("новых ключей к вставке:", len(added))
for k, (old, new) in FIX.items():
    frag = json.dumps(k, ensure_ascii=False) + ": " + json.dumps(old, ensure_ascii=False)
    if frag in t:
        t = t.replace(frag, json.dumps(k, ensure_ascii=False) + ": " + json.dumps(new, ensure_ascii=False), 1)
        print("исправлено:", k, "->", new)

# ключ версии 0.34.6 (если нет) — после 0.34.2
vkey = json.dumps("Early Access Version 0.34.6", ensure_ascii=False)
vval = json.dumps("Ранний доступ, версия 0.34.6", ensure_ascii=False)
if vkey + ": " + vval not in t:
    a = json.dumps("Early Access Version 0.34.2", ensure_ascii=False) + ": " + json.dumps("Ранний доступ, версия 0.34.2", ensure_ascii=False)
    assert a in t, "нет якоря 0.34.2"
    t = t.replace(a, a + ",\n    " + vkey + ": " + vval, 1)
    print("добавлен ключ версии 0.34.6")

# вставка новых записей в конец словаря (перед закрывающей скобкой)
if added:
    m = re.search(r'"West Coast Landing": "Посадка на западном побережье"\s*\n\}', t)
    assert m, "не найден хвост словаря"
    block = ",\n".join("    " + json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False) for k, v in added)
    t = t[:m.end(0) - 1] + block + "\n" + t[m.end(0):]

io.open(DICT, "w", encoding="utf-8", newline="\n").write(t)

def parse_plugin_style(text):
    """Парсер, имитирующий лоадер плагина: убирает //-комментарии вне кавычек."""
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

d = parse_plugin_style(io.open(DICT, encoding="utf-8-sig").read())
missing = [k for k in list(NEW) + list(FIX) if k not in d]
print("словарь репо:", len(d), "записей | не нашлось после вставки:", missing if missing else "нет")

shutil.copy2(DICT, GAME_RU)
gd = parse_plugin_style(io.open(GAME_RU, encoding="utf-8-sig").read())
print("словарь в игре 0.34.6:", len(gd), "записей")
