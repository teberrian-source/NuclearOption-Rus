# -*- coding: utf-8 -*-
"""Полный разбор сессии: тайминги HEAP + атрибуция ALLOC (совместно)."""
import io, os, re, sys, time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
L = r"C:\Users\user\Desktop\Nuclear.Option.v0.34.6\BepInEx\LogOutput.log"
print("изменён:", time.strftime("%d.%m %H:%M:%S", time.localtime(os.path.getmtime(L))))
lines = io.open(L, encoding="utf-8", errors="replace").read().splitlines()

for l in lines:
    if re.search(r"AllocProbe 1\.\d", l):
        print(" ", l[22:110])

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
    heap.append((float(t.group(1).replace(",", ".")), int(mb.group(2).replace(",", "")),
                 int(gc.group(1)) + int(gc.group(2)) + int(gc.group(3)),
                 int(fps.group(1))))

print("HEAP-строк с t:", len(heap))
if heap:
    print()
    print("=== дырки > 3 с ===")
    for a, b in zip(heap, heap[1:]):
        gap = b[0] - a[0]
        if gap > 3.0:
            print("  %.1f -> %.1f (дырка %.1f с) | мусор в окне после: %d KB | GC=%d | fps=%d" % (a[0], b[0], gap, b[1], b[2], b[3]))
    print()
    print("=== GC-штормы (GC>=8) ===")
    for h in heap:
        if h[2] >= 8:
            print("  t=%.1f | GC=%d | мусор %d KB/2s | fps=%d" % (h[0], h[2], h[1], h[3]))
    print()
    print("=== последние 10 окон ===")
    for h in heap[-10:]:
        print("  t=%6.1f | +%7d KB/2s | GC=%d | fps=%3d" % (h[0], h[1], h[2], h[3]))

# ALLOC: окна с t-меткой нет, но порядковый номер окна ~ 2с шаг; сопоставим по суммам
alloc = [l for l in lines if "[ALLOC]" in l]
print()
print("ALLOC-строк:", len(alloc))


def stats(win, label, top=12):
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
            print("   %-56s %6.0f" % (k, v / n))


if alloc:
    stats(alloc, "ВСЯ сессия")
    print()
    stats(alloc[-30:], "ХВОСТ (посл.30)")
    print()
    # самые тяжёлые одиночные окна
    heavy = []
    for l in alloc:
        m = re.search(r"total=(\d+) KB/2s", l)
        if m:
            heavy.append((int(m.group(1)), l[22:260]))
    heavy.sort(reverse=True)
    print("=== 5 самых тяжёлых окон ===")
    for v, l in heavy[:5]:
        print(" +%d KB/2s" % v)
        print("   ", l)
