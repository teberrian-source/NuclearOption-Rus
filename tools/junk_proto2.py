# -*- coding: utf-8 -*-
"""Фильтр v2: финальный набор паттернов (проверка на реальном экспорте)."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
raw_un = open(base + r"\untranslated.txt", "rb").read().decode("utf-8", "replace")
keys = []
for m in re.finditer(r'"((?:[^"\\]|\\.)*)": ""', raw_un):
    try:
        keys.append(json.loads('"' + m.group(1) + '"'))
    except Exception:
        pass

L = r"[^\W\d_]"  # буква (любой алфавит)
JUNK = [
    r"^\s*[\d.,]+\s*(kg|km|km/h|kt|t|s|ms|%|h|g|G|k|m|b|m/s|kW/kg|kN|MW|m2|ft|nm)?\s*$",
    r"^\s*[\d.,]+\s*t?\s*/\s*[\d.,]+\s*t?\s*$",
    rf"^\s*[$€£][\d.,]+\s*[kmb]?\s*$",
    rf"^\s*[$€£]?[\d.,]+\s*[mMbB]\s*\(\s*\+[\d.,]+\s*[mMbB]\s*\)\s*$",
    rf"^\s*[A-Z]{{0,4}}\s*:?\s*[$€£][\d.,]+\s*[kmb]?\s*$",
    rf"^\s*[\d.,]+\s*[mMbB]?\s*\$\s*$",
    rf"^\s*\S{{1,4}}\s*:\s*[\d.,]+\s*[\w%]{{0,6}}\s*$",
    rf"^\s*%?\s*{L}{{1,6}}\s*:?\s*[\d.,]+\s*%?\s*$",
    r"^\s*\d+\s+[A-Z]{2,4}\s*$",
    r"^\s*x\s+\d+\s*$",
    r"^\s*[A-Z][a-z]\d{2,3}\s*$",
    r"^\s*Time\b.*\d.*Duration\b.*$",
    r"^\s*Score\b.*\d.*$",
    r"^\s*Pass\s*:\s*\d+\s*$",
    r"^\s*RANK\s+\d+.*$",
    rf"^\s*[\d.,]+\s*{L}{{1,4}}/{L}{{1,4}}\s*$",
    r"^\s*\(?(kb|KB|kB|ms|us|fps|FPS|Hz|kHz)\)?\s*$",
    r"^\s*(cpu|gpu|Cpu|Gpu|CPU|GPU)\s*$",
    rf"^\s*%\s*{L}{{1,6}}\s*$",
]

dropped, kept = [], []
for k in keys:
    (dropped if any(re.match(p, k) for p in JUNK) else kept).append(k)
print(f"всего {len(keys)}  |  отсеяно {len(dropped)}  |  остаётся {len(kept)}")

print("\n--- отсеяно (примеры) ---")
for k in dropped[:12]:
    print("  ", json.dumps(k, ensure_ascii=False)[:70])

print("\n--- остаётся: короткие/без цифр (реально спорные) ---")
for k in kept:
    if len(k) <= 14:
        print("  ", json.dumps(k, ensure_ascii=False))
