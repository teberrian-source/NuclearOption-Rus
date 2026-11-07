# -*- coding: utf-8 -*-
"""Проверка целостности ru.json: сравнение HEAD/работа, по парсеру плагина и по json."""
import io, json, re, sys, tempfile, os

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def parse_plugin_style(text):
    """Парсер, имитирующий лоадер плагина: убирает //-комментарии вне кавычек."""
    out = []
    in_str = False
    esc = False
    i = 0
    while i < len(text):
        c = text[i]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
            out.append(c)
        else:
            if c == '"':
                in_str = True
                out.append(c)
            elif c == "/" and i + 1 < len(text) and text[i + 1] == "/":
                while i < len(text) and text[i] != "\n":
                    i += 1
                continue
            else:
                out.append(c)
        i += 1
    return json.loads("".join(out), strict=False)

t = io.open(r"C:\Users\user\Documents\NuclearOption_Rus\dict\ru.json", encoding="utf-8-sig").read()
data = parse_plugin_style(t)
print("работа (парсер плагина):", len(data))

head_path = os.path.join(tempfile.gettempdir(), "ru_head.json")
raw = io.open(head_path, encoding="utf-8-sig").read()
data_head = parse_plugin_style(raw)
print("HEAD   (парсер плагина):", len(data_head))

new_keys = [k for k in data if k not in data_head]
lost_keys = [k for k in data_head if k not in data]
print("добавлено:", len(new_keys))
print("потеряно :", len(lost_keys))
for k in lost_keys[:10]:
    print("  LOST:", repr(k[:80]))
# сверить значения пересекающихся ключей
diff = [k for k in data_head if k in data and data[k] != data_head[k]]
print("изменились:", len(diff))
