# -*- coding: utf-8 -*-
"""Ищет UTF-16LE подстроки в DLL и расширяет контекст."""
import sys

dll = r"C:\Users\user\Desktop\Nuclear Option\NuclearOption_Data\Managed\Assembly-CSharp.dll"
data = open(dll, 'rb').read()
sys.stdout.reconfigure(encoding='utf-8')

def find_utf16(nd):
    pat = nd.encode('utf-16-le')
    out = []
    start = 0
    while True:
        i = data.find(pat, start)
        if i < 0:
            break
        out.append(i)
        start = i + 1
    return out

def expand(i):
    # выравниваем к паре (i должно быть уже чётно относительно строки)
    # назад до непечатного символа (двойного 0x00 0x00 или мусора)
    lo = i
    while lo - 2 >= 0:
        c = data[lo-2] | (data[lo-1] << 8)
        if not (0x20 <= c < 0xD800 or c in (0x0A, 0x0D, 0x09)):
            break
        lo -= 2
    hi = i
    while hi + 2 <= len(data):
        c = data[hi] | (data[hi+1] << 8)
        if not (0x20 <= c < 0xD800 or c in (0x0A, 0x0D, 0x09)):
            break
        hi += 2
    return data[lo:hi].decode('utf-16-le', errors='replace')

for nd in ['counter insurgency', 'radome', 'Radome', 'weapon types']:
    pos = find_utf16(nd)
    print(f"=== {nd!r}: {len(pos)} hits ===")
    for i in pos[:6]:
        print(repr(expand(i))[:700])
        print()
