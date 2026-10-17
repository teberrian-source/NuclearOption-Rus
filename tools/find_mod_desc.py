# -*- coding: utf-8 -*-
"""Ищет, где лежат описания модового оружия (по фразе 'flare-resistant')."""
import sys, os, re

sys.stdout.reconfigure(encoding="utf-8")
root = r"C:\Users\user\Desktop\NuclearOption_0.34.2"
q = "flare-resistant"
hits = []
for dirpath, dirnames, filenames in os.walk(root):
    for name in filenames:
        p = os.path.join(dirpath, name)
        if os.path.basename(p) in ("LogOutput.log", "untranslated.txt", "Player.log"):
            continue
        try:
            if os.path.getsize(p) > 600_000_000:
                continue
            data = open(p, "rb").read()
        except Exception:
            continue
        for enc in ("utf-8", "utf-16-le"):
            i = data.find(q.encode(enc))
            if i >= 0:
                txt = data[max(0, i - 250) : i + 250].decode(enc, "ignore")
                txt = re.sub(r"[\x00-\x08\x0b-\x1f]+", " | ", txt)
                hits.append((p, enc, txt))
                break
print("совпадений:", len(hits))
for p, enc, txt in hits:
    print("=" * 70)
    print(f"{p} ({enc})")
    print(txt)
