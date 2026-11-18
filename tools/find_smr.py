# -*- coding: utf-8 -*-
"""Поиск SMR/NOSMR в дампе манифестов NOMNOM."""
import io, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"C:\Users\user\.local\share\opencode\tool-output\tool_1eaefcbc2001YJ7tME9DszKehU"
t = io.open(p, encoding="utf-8", errors="replace").read()
hits = sorted(set(re.findall(r'[\w./-]*SMR[\w./-]*', t)))
print("совпадения SMR:", len(hits))
for h in hits[:20]:
    print(" -", h)
