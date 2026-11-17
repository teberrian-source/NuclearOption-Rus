# -*- coding: utf-8 -*-
"""Разбор [ALLOC] лога AllocProbe: агрегаты, хвост, ошибки."""
import io, os, re, sys, time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
L = r"C:\Users\user\Desktop\Nuclear.Option.v0.34.6\BepInEx\LogOutput.log"
print("изменён:", time.strftime("%d.%m %H:%M:%S", time.localtime(os.path.getmtime(L))))
lines = io.open(L, encoding="utf-8", errors="replace").read().splitlines()
hdr = [(i, l) for i, l in enumerate(lines) if "BepInEx 5.4.23.4 - NuclearOption" in l]
print("сессий в логе:", len(hdr))
if hdr:
    print("последняя:", hdr[-1][1][22:])

for l in lines:
    if re.search(r"AllocProbe 1\.\d", l):
        print(" ", l[22:110])

alloc = [l for l in lines if "[ALLOC]" in l]
print("ALLOC-строк:", len(alloc))

errs = [l for l in lines if "[Error" in l or "Exception" in l]
print("ошибок/исключений:", len(errs))
for l in errs[:8]:
    print("  !", l[22:180])


def stats(win, label, top=14):
    agg = {}
    tot = res = n = 0
    for l in win:
        m = re.search(r"total=(-?\d+) KB/2s", l)
        r = re.search(r"residual=(-?\d+) KB/2s", l)
        if not m:
            continue
        n += 1
        tot += max(0, int(m.group(1)))
        res += max(0, int(r.group(1)))
        body = l.split("|", 1)[1] if "|" in l else ""
        for sm in re.finditer(r"([^;|=]+)=(\d+) KB", body):
            agg[sm.group(1).strip()] = agg.get(sm.group(1).strip(), 0) + int(sm.group(2))
    print("===", label, "-", n, "окон ===")
    print(" total %.0f | residual %.0f KB/2s" % (tot / n, res / n))
    for k, v in sorted(agg.items(), key=lambda x: -x[1])[:top]:
        if v > 0:
            print("   %-52s %6.0f" % (k, v / n))


stats(alloc, "ВСЯ сессия")
print()
stats(alloc[-40:], "ХВОСТ (посл.40)")
