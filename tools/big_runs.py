# -*- coding: utf-8 -*-
"""Ищет в resources.assets большие печатные блоки (JSON миссий) и сохраняет их."""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
root = r"C:\Users\user\Desktop\NuclearOption_0.34.2\NuclearOption_Data"
run_re = re.compile(rb"[\x20-\x7E\xC2-\xF4][\x20-\x7E\x80-\xBF\xC2-\xF4]*")
needle = b"engineer team is currently trying"

for fn in ["resources.assets", "level0", "level1", "level2", "level3", "level4", "level5"]:
    p = os.path.join(root, fn)
    if not os.path.exists(p):
        continue
    data = open(p, "rb").read()
    runs = []
    for m in run_re.finditer(data):
        if m.end() - m.start() >= 300:
            try:
                s = m.group(0).decode("utf-8")
            except UnicodeDecodeError:
                continue
            runs.append((m.start(), s))
    big = [(off, s) for off, s in runs if needle.decode() in s]
    print(f"{fn}: блоков >=300 симв.: {len(runs)}, с брифингом: {len(big)}")
    if big:
        with io.open(f"big_{fn}.txt", "w", encoding="utf-8", newline="\n") as f:
            for off, s in big:
                f.write(f"### offset {off} len {len(s)}\n{s}\n\n")
        print("   ->", f"big_{fn}.txt", "len:", [len(s) for _, s in big])
