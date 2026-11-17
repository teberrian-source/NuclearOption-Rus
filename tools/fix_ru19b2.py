# -*- coding: utf-8 -*-
"""Ремонт ru.json v2: точечная запятая на стыке блоков 19/19b + валидация + деплой."""
import io, json, shutil, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
DICT = r"C:\Users\user\Documents\NuclearOption_Rus\dict\ru.json"
GAME = r"C:\Users\user\Desktop\Nuclear.Option.v0.34.6\BepInEx\plugins\LocalizationPatch\ru.json"


def strip_comments(s: str) -> str:
    out, i, n, in_str = [], 0, len(s), False
    while i < n:
        c = s[i]
        if in_str:
            out.append(c)
            if c == "\\":
                out.append(s[i + 1] if i + 1 < n else "")
                i += 2
                continue
            if c == '"':
                in_str = False
            i += 1
            continue
        if c == '"':
            in_str = True
            out.append(c)
            i += 1
            continue
        if c == "/" and i + 1 < n and s[i + 1] == "/":
            while i < n and s[i] != "\n":
                i += 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


raw = io.open(DICT, encoding="utf-8-sig").read()
bad = "\"\n    // ==== Round 19b:"
good = "\",\n    // ==== Round 19b:"
assert bad in raw, "стык не найден (возможно, уже починен)"
raw = raw.replace(bad, good, 1)
io.open(DICT, "w", encoding="utf-8", newline="").write(raw)

d = json.loads(strip_comments(raw), strict=False)
print("словарь валиден, записей:", len(d))
shutil.copy2(DICT, GAME)
print("развёрнуто в игру OK,", len(raw), "символов")
