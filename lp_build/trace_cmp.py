# -*- coding: utf-8 -*-
"""Сравнивает строки из [TRACE] miss в логе с ключами ru.json (ищет отличие)."""
import io, json, re, sys

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

def parse_json(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse_json(base + r"\ru.json")
log = io.open(r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\LogOutput.log", encoding="utf-8", errors="replace").read()

pat = re.compile(r'\[TRACE\] (hit|miss): "(.*)"$', re.M)
want = ["RAH-72 is a recon", "largest aircraft so far", "extremely powerful long-range", "recon and light attack"]
for m in pat.finditer(log):
    kind, body = m.group(1), m.group(2)
    if not any(w in body for w in want):
        continue
    try:
        s = json.loads('"' + body + '"')
    except Exception:
        s = body.replace('\\"', '"').replace("\\n", "\n")
    print("=" * 90)
    print(kind.upper(), "длина:", len(s))
    print("  первые 120:", repr(s[:120]))
    print("  последние 60:", repr(s[-60:]))
    inru = s in ru
    print("  точно в ru.json:", inru)
    if not inru:
        st = s.strip()
        print("  после strip в ru.json:", st in ru)
        # ищем ближайший ключ
        for k in ru:
            if k[:40] == s[:40]:
                print("  похожий ключ:", repr(k[:80]), "| длина", len(k))
                print("   отличия:", [(i, k[i:i+12], s[i:i+12]) for i in range(min(len(k), len(s))) if k[i] != s[i]][:6])
                print("   хвост ключа:", repr(k[-40:]))
                break
