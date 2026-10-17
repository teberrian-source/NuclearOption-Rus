# -*- coding: utf-8 -*-
"""Находит полные тексты обрезанных miss-строк по префиксу в ассетах/модах."""
import sys, os, re, glob

sys.stdout.reconfigure(encoding="utf-8")

PREFIXES = [
    "Additional Boats / Ships",
    "Additional low-rank aircraft",
    "New large landlocked map",
    "What the fuck did you just",
    "This is how wide the text box",
    "Launching aircraft must aim at the target",
]

roots = [
    r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data",
    r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins",
]
files = []
for r0 in roots:
    for ext in ("*.assets", "*.resource", "*.dll", "*.textasset"):
        files += glob.glob(os.path.join(r0, "**", ext), recursive=True)

pat = re.compile(rb"[\x20-\x7E\r\n]{20,1200}")
found = {}
for f in files:
    try:
        data = open(f, "rb").read()
    except Exception:
        continue
    # ascii
    for m in pat.finditer(data):
        s = m.group().decode("ascii", "ignore")
        for p in PREFIXES:
            if p in s and p not in found:
                found[p] = (os.path.basename(f), s)
    # utf-16le
    for m in pat.finditer(data.replace(b"\x00", b"")):
        pass  # пропущено: замена ломает границы, ниже отдельно
    if len(found) == len(PREFIXES):
        break

for p in [x for x in PREFIXES if x not in found]:
    print("НЕ НАЙДЕН:", p)

for p, (src, s) in found.items():
    print("=" * 70)
    print(f"[{src}]")
    # фрагмент вокруг префикса
    i = s.find(p)
    print(s[max(0, i - 50) : i + 700])
