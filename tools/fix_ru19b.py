# -*- coding: utf-8 -*-
"""Ремонт ru.json: пропущенная запятая перед блоком Round 19b + валидация."""
import io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
DICT = r"C:\Users\user\Documents\NuclearOption_Rus\dict\ru.json"

raw = io.open(DICT, encoding="utf-8-sig").read()


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


# найти строку с комментарием 19b; у предыдущей строки нет запятой — добавить
marker = "    // ==== Round 19b:"
idx = raw.find(marker)
assert idx != -1, "блок 19b не найден"
prev_line_end = raw.rfind("\n", 0, idx)
prev_line = raw[prev_line_end + 1 : idx].rstrip()
print("строка перед 19b:", prev_line[-60:])
if not prev_line.endswith(",") and prev_line.endswith('"'):
    fixed = raw[: prev_line_end + 1] + prev_line + ",\n" + raw[idx:]
    io.open(DICT, "w", encoding="utf-8", newline="").write(fixed)
    print("запятая добавлена")
else:
    print("запятая уже есть / не нужен ремонт")
    fixed = raw

d = json.loads(strip_comments(fixed), strict=False)
print("словарь валиден, записей:", len(d))
