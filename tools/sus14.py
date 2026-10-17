# -*- coding: utf-8 -*-
"""Поиск подозрительных (недо)переводов: доля латинских слов в русском тексте."""
import io, re, sys, json

base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
raw = io.open(base + r"\ru.json", encoding="utf-8-sig").read()
ru = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in raw.split("\n") if not l.strip().startswith("//"))), strict=False)

idx = json.load(io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\todo_index.json", encoding="utf-8"))
keys = {m["en"].strip() for m in idx.values()}

sus = []
for k in keys:
    v = ru.get(k)
    if not v:
        continue
    we = re.findall(r"[A-Za-z][A-Za-z'\-]{2,}", k)
    wv = re.findall(r"[A-Za-z][A-Za-z'\-]{2,}", v)
    if not we:
        continue
    ratio = len(wv) / len(we)
    if ratio > 0.5 and len(we) >= 4:
        sus.append((round(ratio, 2), len(we), len(wv), k[:70], v[:90]))

sus.sort(reverse=True)
out = [f"подозрительных: {len(sus)}"]
for s in sus[:60]:
    out.append(str(s))
io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\sus14.txt", "w", encoding="utf-8", newline="\n").write("\n".join(out))
print("подозрительных:", len(sus))
