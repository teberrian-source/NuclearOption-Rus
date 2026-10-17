# -*- coding: utf-8 -*-
"""Из untranslated.txt отбирает только похожее на связный текст (описания/подсказки/UI), без названий."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

def parse(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse(base + r"\ru.json")
raw_u = io.open(base + r"\untranslated.txt", encoding="utf-8", errors="replace").read()

CYR = re.compile(r"[А-Яа-яЁё]")
entries = []
for m in re.finditer(r'^"((?:[^"\\]|\\.)*)":', raw_u, re.M):
    try:
        s = json.loads('"' + m.group(1) + '"')
    except Exception:
        continue
    if s not in ru:
        entries.append(s)

def bucket(s):
    if "<" in s and ">" in s:
        return "markup"
    if "\n" in s:
        return "multi"
    words = re.findall(r"[A-Za-z']+", s)
    if not words:
        return "nonlatin"
    low = [w for w in words if w.islower() and len(w) >= 3]
    caps = [w for w in words if w[0].isupper()]
    if len(words) >= 5 and len(low) >= 2 and len(low) >= len(caps):
        return "sentence"
    if len(words) >= 3 and len(low) == 0:
        return "name"
    return "other"

buckets = {}
for s in entries:
    buckets.setdefault(bucket(s), []).append(s)

print("всего непереведённых:", len(entries))
for k, v in sorted(buckets.items(), key=lambda x: -len(x[1])):
    print(f"  {k}: {len(v)}")

with io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\untr_candidates.txt", "w", encoding="utf-8") as f:
    for k in ("sentence", "multi", "other"):
        f.write(f"########## {k} ({len(buckets.get(k, []))}) ##########\n")
        for s in sorted(set(buckets.get(k, []))):
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
print("файл: untr_candidates.txt")
