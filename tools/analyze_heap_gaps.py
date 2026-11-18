# -*- coding: utf-8 -*-
"""Анализ таймингов [HEAP t=...]: дырки > 3 с = фризы; статистика мусора и GC."""
import io, os, re, sys, time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
L = r"C:\Users\user\Desktop\Nuclear.Option.v0.34.6\BepInEx\LogOutput.log"
print("изменён:", time.strftime("%d.%m %H:%M:%S", time.localtime(os.path.getmtime(L))))
lines = io.open(L, encoding="utf-8", errors="replace").read().splitlines()

heap = []
for l in lines:
    if "[HEAP" not in l:
        continue
    t = re.search(r"t=([\d.,]+)s", l)
    mb = re.search(r"mono=([\d,]+) MB \(\+([\d,]+) KB/2s\)", l)
    gc = re.search(r"GC gen0=(\d+) gen1=(\d+) gen2=(\d+)", l)
    fps = re.search(r"fps=(\d+)", l)
    if not (t and mb and gc and fps):
        continue
    heap.append((float(t.group(1).replace(",", ".")),
                 int(mb.group(2).replace(",", "")),
                 int(gc.group(1)), int(gc.group(2)), int(gc.group(3)),
                 int(fps.group(1)), l[22:150]))

print("HEAP-строк с t:", len(heap))
if heap:
    print("диапазон t: %.1f ... %.1f с" % (heap[0][0], heap[-1][0]))
print()
print("=== дырки между окнами > 3 с (фризы/паузы логгера) ===")
for a, b in zip(heap, heap[1:]):
    gap = b[0] - a[0]
    if gap > 3.0:
        print("  %.1f -> %.1f (дырка %.1f с) | fps %d -> %d | мусор %d KB" % (a[0], b[0], gap, a[5], b[5], b[1]))
print()
print("=== окна с суммарными сборками GC >= 8 (GC-шторм) ===")
for h in heap:
    g = h[2] + h[3] + h[4]
    if g >= 8:
        print("  t=%.1f | GC=%d (g0=%d g1=%d g2=%d) | мусор %d KB/2s | fps=%d" % (h[0], g, h[2], h[3], h[4], h[1], h[5]))
print()
print("=== последние 12 окон ===")
for h in heap[-12:]:
    print("  t=%6.1f | +%6d KB/2s | GC=%d | fps=%3d" % (h[0], h[1], h[2] + h[3] + h[4], h[5]))
