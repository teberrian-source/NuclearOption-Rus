# -*- coding: utf-8 -*-
"""Сравнивает строку описания обтекателя РЛС из бандла с ключами ru.json."""
import io, json, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

def parse_json(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse_json(base + r"\ru.json")
data = io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\radome_objs.txt", encoding="utf-8").read()
line = [l for l in data.split("\n") if "An extremely powerful" in l][0]
s = line.split("| RADAR | ")[1].strip()
print("строка из бандла:", repr(s))
print("длина:", len(s))
print("точное совпадение с ключом:", s in ru)
cand = [k for k in ru if k.startswith("An extremely powerful")]
if cand:
    k = cand[0]
    print("ключ ru.json:", repr(k), len(k))
    print("равны:", k == s)
    diff = [(i, repr(k[i]), repr(s[i])) for i in range(min(len(k), len(s))) if k[i] != s[i]]
    print("отличия:", diff[:10])
