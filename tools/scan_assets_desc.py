# -*- coding: utf-8 -*-
"""Скан ассетов игры на английские описания (длина 40-600, заглавная, хинт-слова)."""
import sys, os, re, json, io, glob

sys.stdout.reconfigure(encoding="utf-8")
data_dir = r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data"

DESC = re.compile(r"[A-Z][A-Za-z0-9 ,\.\-'\"()/&:;]+$")
HINT = re.compile(
    r"\b(is a|is an|are a|designed|features|allows|capable|provides|comes|includes|mounted|used for|can be|makes it|advanced|compact)\b",
    re.I,
)
SKIP = ("Json.NET", "Korean", "FLIGHT-ASSIST", "PHYSICS NOTE", "ConfigurationManager")

def scan(data):
    out = set()
    for m in re.finditer(rb"[\x20-\x7E]{40,600}", data):
        s = m.group().decode("ascii", "ignore").strip()
        if DESC.match(s) and HINT.search(s) and not any(k in s for k in SKIP):
            out.add(s)
    for m in re.finditer(rb"(?:[\x20-\x7E]\x00){40,600}", data):
        s = m.group().replace(b"\x00", b"").decode("ascii", "ignore").strip()
        if DESC.match(s) and HINT.search(s) and not any(k in s for k in SKIP):
            out.add(s)
    return out

found = {}
files = glob.glob(os.path.join(data_dir, "*.assets")) + glob.glob(os.path.join(data_dir, "*.resource"))
for f in files:
    data = open(f, "rb").read()
    for s in scan(data):
        found.setdefault(s, os.path.basename(f))

print("найдено описаний в ассетах:", len(found))
out = io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\asset_desc.jsonl", "w", encoding="utf-8")
for s, src in sorted(found.items()):
    out.write(json.dumps({"src": src, "text": s}, ensure_ascii=False) + "\n")
out.close()
for s, src in sorted(found.items()):
    print(f"[{src}] {s[:130]}")
