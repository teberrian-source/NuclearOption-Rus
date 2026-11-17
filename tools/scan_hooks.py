# -*- coding: utf-8 -*-
"""Контекст методов перевода: Translate, Prefix/Postfix set_text, FrameHelper."""
import io, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"C:\Users\user\Documents\NuclearOption_Rus\plugin\KoreanPatch\Plugin.cs"
lines = io.open(p, encoding="utf-8-sig", errors="replace").read().splitlines()

# найти объявления методов-хуков и Translate
decl = [(i, l) for i, l in enumerate(lines, 1)
        if re.search(r'static (string|void|bool) (Translate|Trans\w*)\(|Postfix|Prefix', l)]
print("объявления:")
for i, l in decl[:40]:
    print(i, "|", l.strip()[:150])
