# -*- coding: utf-8 -*-
"""Финальный отбор переводимых строк из дампа: игровые описания + UI.
Исключаем: настройки KnockPush/aryx, Rewired-геймпады, служебный мусор.
Результат: tools\\round19_candidates.txt + сверка с dict\\ru.json."""
import io, json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUMP = os.path.join(BASE, "tools", "dump_keys.txt")
DICT = os.path.join(BASE, "dict", "ru.json")
OUT = os.path.join(BASE, "tools", "round19_candidates.txt")

dict_raw = io.open(DICT, encoding="utf-8-sig").read()
# ru.json — JSONC: вычищаем // комментарии вне строк перед json.loads
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
ru = json.loads(strip_comments(dict_raw), strict=False)
lines = io.open(DUMP, encoding="utf-8").read().splitlines()

# исключения: конфиг-описания модов и системный мусор
skip_pat = re.compile(
    r"(?i)^v\d+\.\d|×native|aryx|knockout|rotor|swashplate|pusher|wing\b.*AeroPart|"
    r"\.dll|\.exe|\.json|BepInEx|Harmony|Assembly|Unity|System\.|Stack|^\(|"
    r"is already|controller|Do you want|Pro Flight|AimTrak|placeholder|MaterialSymbols|"
    r"\\u[0-9a-f]{4}|Font|font=|RuntimeUnity|manifest|NOMM|SMBios|input rate|"
    r"^LEFT |^UP elevation|azimuth limit|elevation limit|Default|diagnostic|Live\.|Range:|"
    r"seconds between|local X position|local-|LIVE\.|chicane|Ibis|mast radar|radar local|"
    r"census|plug offset|IwbRack|GaugeOffset|MASS label| TacScreen|gauge"
)
keep = []
seen = set()
for l in lines:
    s = l.strip()
    if not s or s in seen:
        continue
    seen.add(s)
    if skip_pat.search(s):
        continue
    letters = sum(c.isalpha() for c in s)
    if letters < 5 or letters / max(len(s), 1) < 0.5:
        continue
    keep.append(s)

new = [s for s in keep if s not in ru]
with io.open(OUT, "w", encoding="utf-8") as f:
    for s in new:
        f.write(s.replace("\n", "\\n") + "\n")
print("отобрано:", len(keep), "| новых (нет в словаре):", len(new))
print("уже переведено из дампа:", len(keep) - len(new))
