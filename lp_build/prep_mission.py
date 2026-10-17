# -*- coding: utf-8 -*-
"""Готовит задания на перевод: брифинги (Message/message), описания миссий (description),
подсказки обучения (body), заголовки подсказок (title)."""
import io, os, re, sys, json, collections

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
root = r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data"
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

ru_raw = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in ru_raw.split("\n") if not l.strip().startswith("//"))), strict=False)

pair_re = re.compile(rb'"([A-Za-z][A-Za-z0-9_]{1,24})"\s*:\s*"((?:[^"\\]|\\.){1,6000})"')
WANT = ("Message", "message", "description", "body", "title", "objectiveName")

fields = collections.defaultdict(list)
seen = collections.defaultdict(set)
for fn in ["resources.assets", "level0", "level1", "level2", "level3", "level4", "level5"]:
    p = os.path.join(root, fn)
    if not os.path.exists(p):
        continue
    data = open(p, "rb").read()
    for m in pair_re.finditer(data):
        k = m.group(1).decode("ascii")
        if k not in WANT:
            continue
        raw = m.group(2).decode("utf-8", "replace")
        try:
            val = json.loads('"' + raw + '"')
        except Exception:
            continue
        if val in seen[k]:
            continue
        seen[k].add(val)
        fields[k].append(val)

ws_re = re.compile(r"[ \t\x0b\f\r]*\n[ \t\x0b\f\r]*")

def normalize(s):
    """Приводит текст к читаемому виду: абзацы -> \\n\\n, перенос -> \\n, лишние пробелы -> 1."""
    s = s.replace("\x0b", "\n")
    parts = [p.strip() for p in re.split(r"\n+", s)]
    parts = [re.sub(r"[ \t]{2,}", " ", p) for p in parts if p]
    return "\n\n".join(parts)

def is_junk(s):
    if len(s) < 3:
        return True
    if re.fullmatch(r"[A-Za-z%^$*&\-0-9 ]{1,20}", s) and not re.search(r"[aeiou]{2}", s.lower()):
        return True
    if s in ("Waypoint",):
        return False
    return False

idx = {}
out_msgs, out_bodies, out_titles = [], [], []
n = 0
for k in ("Message", "message", "description"):
    for v in fields[k]:
        if v in ru:
            continue
        if is_junk(v):
            print("пропуск (мусор):", repr(v))
            continue
        n += 1
        idx[str(n)] = {"field": k, "en": v}
        out_msgs.append(f"### {n}\n{normalize(v)}\n")
for v in fields["body"]:
    if v in ru:
        continue
    n += 1
    idx[str(n)] = {"field": "body", "en": v}
    out_bodies.append(f"### {n}\n{normalize(v)}\n")
for v in fields["title"]:
    if v in ru:
        continue
    n += 1
    idx[str(n)] = {"field": "title", "en": v}
    out_titles.append(f"### {n}\n{v}\n")
for v in fields["objectiveName"]:
    if v in ru:
        continue
    print("objectiveName (уже в словаре или нет):", repr(v))

with io.open("todo_msgs.txt", "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(out_msgs))
with io.open("todo_bodies.txt", "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(out_bodies))
with io.open("todo_titles.txt", "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(out_titles))
with io.open("todo_index.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump(idx, f, ensure_ascii=False, indent=1)

print("всего к переводу:", n)
print("  брифинги/описания:", len(out_msgs), "-> todo_msgs.txt")
print("  подсказки (body):", len(out_bodies), "-> todo_bodies.txt")
print("  заголовки (title):", len(out_titles), "-> todo_titles.txt")
