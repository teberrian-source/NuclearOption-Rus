# -*- coding: utf-8 -*-
"""Проверка целостности Plugin.cs после PowerShell-правки (юникод не побился)."""
import io, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"C:\Users\user\AppData\Local\Temp\lp_build\KoreanPatch\Plugin.cs"
s = io.open(p, encoding="utf-8").read()
print("длина:", len(s))
print("em dash:", s.count("\u2014"))
print("мохибейк 'Р¤':", s.count("\u0420\u00a4"), "| 'РА':", s.count("\u0420\u0410"))
print("кириллица:", sum(1 for c in s if "\u0400" <= c <= "\u04ff"))
print("BOM:", s.startswith("\ufeff"))
i = s.find("v3.2.3")
print(repr(s[i - 30:i + 40]))
