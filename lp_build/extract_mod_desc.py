# -*- coding: utf-8 -*-
"""Извлекает английские описания (UTF-8/UTF-16) из DLL модов 0.34.2."""
import sys, os, re, glob, json, io

sys.stdout.reconfigure(encoding="utf-8")
plug = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins"

# паттерн "похоже на описание": начинается с заглавной, есть " is a/the ", " designed ", " features " и т.п.
DESC = re.compile(
    r"[A-Z][A-Za-z0-9 ,\.\-'\"()/&:;]+$"
)
HINT = re.compile(
    r"\b(is a|is an|are a|designed|features|allows|capable|provides|comes|includes|mounted|used for|can be|makes it)\b",
    re.I,
)

def strings_u16(data):
    # UTF-16LE непрерывные строки >= 25 символов
    for m in re.finditer(rb"(?:[\x20-\x7E]\x00){25,}", data):
        yield m.group().replace(b"\x00", b"").decode("ascii", "ignore")

def strings_u8(data):
    for m in re.finditer(rb"[\x20-\x7E]{25,}", data):
        yield m.group().decode("ascii", "ignore")

found = {}
for dll in glob.glob(os.path.join(plug, "**", "*.dll"), recursive=True):
    try:
        data = open(dll, "rb").read()
    except Exception:
        continue
    for s in list(strings_u16(data)) + list(strings_u8(data)):
        s = s.strip()
        if len(s) < 40 or len(s) > 600:
            continue
        if not DESC.match(s) or not HINT.search(s):
            continue
        found.setdefault(s, os.path.basename(dll))

print("найдено описаний:", len(found))
out = io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\mod_desc.jsonl", "w", encoding="utf-8")
for s, src in sorted(found.items()):
    out.write(json.dumps({"src": src, "text": s}, ensure_ascii=False) + "\n")
out.close()
for s, src in sorted(found.items())[:60]:
    print(f"[{src}] {s[:160]}")
