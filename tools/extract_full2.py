# -*- coding: utf-8 -*-
"""Полные строки (с \n и типографикой) из бандлов модов: что отсутствует в ru.json
и какие есть почти-совпадения (ключ отличается хвостом/пробелами)."""
import io, os, re, sys, json

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import UnityPy
UnityPy.config.FALLBACK_UNITY_VERSION = "2022.3.62f1"

base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
unpack = r"C:\Users\user\AppData\Local\Temp\lp_build\unpack"

def parse_json(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse_json(base + r"\ru.json")
SPLIT = re.compile(rb"[\x00-\x08\x0B-\x1F\x7F]")

def prose(t):
    if len(t) < 50 or len(t) > 4000:
        return False
    if ";" in t or t.startswith("{") or t.startswith('"') or t.startswith("|"):
        return False
    words = t.split()
    if len(words) < 9:
        return False
    bad = sum(1 for c in t if not (c.isalnum() or c in " .,;:!?'\"()[]-–—/%+&*=#$@_<>|\\~`^"))
    return bad / len(t) < 0.02 and t.count(" ") > 8

found = {}
for f in sorted(os.listdir(unpack)):
    p = os.path.join(unpack, f)
    try:
        env = UnityPy.load(p)
    except Exception as e:
        print("!!", f, e, flush=True)
        continue
    for o in env.objects:
        try:
            raw = o.get_raw_data()
        except Exception:
            continue
        if len(raw) > 80000:
            continue
        for chunk in SPLIT.split(raw):
            if len(chunk) < 50:
                continue
            t = chunk.decode("utf-8", "replace")
            if "\ufffd" in t:
                continue
            t = t.strip()
            if prose(t):
                found.setdefault(t, set()).add(f)
    print(f, "->", len(found), flush=True)

missing, near = [], []
for t in sorted(found):
    if t in ru:
        continue
    missing.append(t)
    pref = t[:120]
    for k in ru:
        if k[:120] == pref:
            near.append((t, k))
            break

print("\nвсего длинных:", len(found), "| нет в ru.json:", len(missing), "| почти-совпадений:", len(near))
json.dump({"missing": missing, "near": [{"data": a, "key": b} for a, b in near]},
          io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\desc_final.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\desc_final.txt", "w", encoding="utf-8").write(
    "=== НЕТ В СЛОВАРЕ ===\n\n" + "\n\n".join(missing) +
    "\n\n=== ПОЧТИ-СОВПАДЕНИЯ (данные | ключ) ===\n\n" +
    "\n\n".join(f"ДАННЫЕ: {a}\nКЛЮЧ  : {b}" for a, b in near))
for t in missing:
    print("|", t[:400])
print("\n--- почти-совпадения ---")
for a, b in near:
    i = next((j for j in range(min(len(a), len(b))) if a[j] != b[j]), min(len(a), len(b)))
    print("ДАННЫЕ:", repr(a[max(0, i - 30):i + 40]))
    print("КЛЮЧ  :", repr(b[max(0, i - 30):i + 40]))
