# -*- coding: utf-8 -*-
"""Поиск аллокаций строк в горячем пути LocalizationPatch (KoreanPatch/Plugin.cs)."""
import io, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"C:\Users\user\Documents\NuclearOption_Rus\plugin\KoreanPatch\Plugin.cs"
lines = io.open(p, encoding="utf-8-sig", errors="replace").read().splitlines()
print("строк:", len(lines))

pat = re.compile(r'String\.|\.Split|Concat|\.Format|\$"|\.Replace\(|\.Substring|\.ToLower|\.ToUpper|\.Trim\(|new string|\.ToArray\(|\.ToList\(|StringBuilder')
hits = [(i, l) for i, l in enumerate(lines, 1) if pat.search(l)]
print("совпадений:", len(hits))
for i, l in hits[:60]:
    print(i, "|", l.strip()[:160])
