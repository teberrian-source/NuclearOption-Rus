# -*- coding: utf-8 -*-
"""Выбирает из дампа untranslated.txt реальный английский текст (не имена, не динамика, не цветные строки)."""
import io, json, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"

raw = io.open(base + r"\untranslated.txt", encoding="utf-8", errors="replace").read()
out = []
for m in re.finditer(r'^\s*"((?:[^"\\]|\\.)*)"\s*:\s*""\s*,?\s*$', raw, re.M):
    s = m.group(1).replace('\\"', '"').replace("\\n", "\n").replace("\\\\", "\\")
    out.append(s)
uniq = sorted(set(out))

def real_text(t):
    if "<color=" in t or "<size=" in t or "<font" in t or "<link" in t or "<b>" in t:
        return False
    if t.count("•") or t.startswith("•"):
        return True  # дорожная карта — оставляем
    if re.search(r"\d[\d,]{3,}", t):
        return False
    if "@" in t or "http" in t:
        return False
    words = re.findall(r"[A-Za-z]{2,}", t)
    if len(words) < 4:
        return False
    letters = sum(c.isalpha() or c in " .,'!?-\n:;()/%" for c in t)
    if letters / max(1, len(t)) < 0.85:
        return False
    # отсев заведомого мусора
    junk = ["According to all known laws", "This is how wide the text box", "Navy Seals",
            "A great place for new players", "VERyLONG_PLAYER_NAME", "Lorem ipsum",
            "Line1", "Text type", "Test Error", "Test\n", "A long username", "AAAHGRPL"]
    if any(j in t for j in junk):
        return False
    return True

cand = [t for t in uniq if real_text(t)]
print("кандидатов:", len(cand))
io.open(r"C:\Users\user\AppData\Local\Temp\lp_build\untr_cand.txt", "w", encoding="utf-8").write("\n\n=====\n\n".join(cand))
for i, t in enumerate(cand, 1):
    print(f"--- {i} ---")
    print(t.strip())
