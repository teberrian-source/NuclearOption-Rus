# -*- coding: utf-8 -*-
"""Свежий дамп untranslated.txt: что ещё не переведено (кроме мусора)."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
text = io.open(base + r"\untranslated.txt", encoding="utf-8", errors="replace").read().replace("\\n", "\n")

ru_raw = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in ru_raw.split("\n") if not l.strip().startswith("//"))), strict=False)

entries = []
cur = None
for line in text.split("\n"):
    if cur is None:
        s = line.lstrip()
        if s.startswith('"'):
            cur = s[1:]
            m = re.search(r'"\s*:\s*""\s*,?\s*$', cur)
            if m:
                entries.append(cur[:m.start()])
                cur = None
    else:
        m = re.search(r'"\s*:\s*""\s*,?\s*$', line)
        if m:
            entries.append(cur + "\n" + line[:m.start()])
            cur = None
        else:
            cur += "\n" + line

def unesc(s):
    return s.replace("\\'", "'").replace('\\"', '"').replace("\\\\", "\\")

entries = sorted({unesc(e).strip() for e in entries if e.strip()})

junk_pat = re.compile(r"^(?:8[Bb]it|Buffalo|CH PRODUCTS|Thrustmaster|Logitech|Saitek|Fantech|Sony|Microsoft|Xbox|Generic|Steam|Logitech|Mad Catz|Hori|Nacon|PDP|Razer|Betop|Gamepad|Controller|USB|Wireless|HID|VID_|0fcc0|167669|3de2fc|9ec45b|47b2af4b)", re.I)
junk_words = ("Lorem ipsum", "According to all known laws of aviation", "What the fuck", "Test Error Message", "VERyLONG_PLAYER_NAME", "This is how wide the text box", "placeholder", "Navy Seals")

new = []
for e in entries:
    if e in ru:
        continue
    if len(e) < 3:
        continue
    if any(w.lower() in e.lower() for w in junk_words):
        continue
    if junk_pat.match(e):
        continue
    words = re.findall(r"[A-Za-z]{2,}", e)
    if len(words) < 2:
        continue
    new.append(e)

print("кандидатов:", len(new))
with io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\pending15.txt", "w", encoding="utf-8", newline="\n") as f:
    for e in new:
        f.write(e + "\n====\n")
