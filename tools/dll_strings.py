# -*- coding: utf-8 -*-
"""Извлекает UTF-16 строки из Assembly-CSharp.dll по подстрокам."""
import sys, re

dll = r"C:\Users\user\Desktop\Nuclear Option\NuclearOption_Data\Managed\Assembly-CSharp.dll"
data = open(dll, 'rb').read()
sys.stdout.reconfigure(encoding='utf-8')

# UTF-16LE строки: последовательности printable char (>0x20, <0x10000) длиной >= 30
strings = []
cur = []
i = 0
n = len(data)
while i + 1 < n:
    c = data[i] | (data[i+1] << 8)
    if 0x20 <= c < 0xD800 or c in (0x0A, 0x0D, 0x09):
        if c == 0x0A or c == 0x0D or c == 0x09:
            # контролы только внутри строк — допускаем
            pass
        cur.append(chr(c))
        i += 2
    else:
        if len(cur) >= 30:
            strings.append(''.join(cur))
        cur = []
        i += 1
if len(cur) >= 30:
    strings.append(''.join(cur))

print("total long strings:", len(strings))
needles = ['counter insurgency', 'radome', 'Radome']
for s in strings:
    low = s.lower()
    for nd in needles:
        if nd.lower() in low:
            print("----")
            print(repr(s[:600]))
            break
