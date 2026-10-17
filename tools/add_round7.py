# -*- coding: utf-8 -*-
"""+2 описания из энциклопедии (Helion, Andromeda), затем показывает непереведённое из untranslated.txt."""
import io, re, sys, json, shutil, datetime, os

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
p = base + r"\ru.json"

NEW = {
 "Coming in at 20,000 tonnes and common with mid-tier regional powers on a budget, the Helion-class is amongst the smallest aircraft carriers in the world, and amongst the few capital ships available on the export market. This light carrier is built on the same hull as the Devotion-class albeit equipped with a CATOBAR facelift, sporting two steam catapults on a flat deck and improved defences. It is well defended with 56 RAM-45 anti-air missiles, two IRM-S2 launcher turrets, two 30mm CIWS and an 80kW laser defence system. It can handle a range of aircraft thanks to its catapults and offers arrested landing capability with three wires to the stern.":
 "Водоизмещением 20 000 тонн и популярный у региональных держав среднего уровня с ограниченным бюджетом, авианосец класса Helion — один из самых малых авианосцев в мире и один из немногих крупных кораблей, доступных на экспортном рынке. Этот лёгкий авианосец построен на том же корпусе, что и класс Devotion, но получил модернизацию по схеме CATOBAR: две паровые катапульты на плоской палубе и улучшенную оборону. Он хорошо защищён: 56 зенитных ракет RAM-45, две пусковые турели IRM-S2, две 30-мм системы ближней обороны и 80-кВт лазерная система обороны. Благодаря катапультам он принимает разные самолёты и обеспечивает посадку с зацеплением за три троса в корме.",
 "The Andromeda-class Aviation Missile Cruiser is a hulking heavy cruiser designed to sidestep treaties regarding high tonnage carriers on the Mainland's straits, and for the BDF to equalise the playing field in the large surface combatant role against PALA's Dynamo-class. This massive cruiser is armed with two 203mm deck guns and is able to launch huge AGM-99 volleys and lock down airspace with its long-range R-9 SAMs, and launch V/STOVL aircraft to attain air superiority. It is heavily armoured and can hold its own against larger groups of vessels. Once the Strategic threshold is reached, it can launch a devastating wave of SLND-9 nuclear missiles at high value targets.":
 "Авиационный ракетный крейсер класса Andromeda — громоздкий тяжёлый крейсер, спроектированный в обход договоров о крупнотоннажных авианосцах в проливах Мейнленда, чтобы BDF мог уравнять шансы в роли крупного надводного боевого корабля против класса Dynamo у PALA. Этот огромный крейсер вооружён двумя 203-мм палубными орудиями, способен выпускать огромные залпы AGM-99, запирать воздушное пространство своими дальнобойными ЗУР R-9 и поднимать самолёты V/STOL для завоевания превосходства в воздухе. Он тяжело бронирован и способен противостоять более крупным группировкам кораблей. При достижении стратегического порога он может выпустить сокрушительную волну ядерных ракет SLND-9 по ценным целям.",
}

raw = io.open(p, encoding="utf-8-sig").read()
shutil.copy2(p, base + r"\ru.backup_" + datetime.datetime.now().strftime("%H%M%S") + ".json")

def parse(txt):
    ls = [l for l in txt.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse(raw)
before = len(ru)
pairs = [(k, v) for k, v in NEW.items() if k not in ru]
if pairs:
    idx = raw.rfind("\n}")
    head, tail = raw[:idx], raw[idx:]
    if not head.rstrip().endswith(","):
        head = head.rstrip() + ","
    lines = ["    " + json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False) for k, v in pairs]
    io.open(p, "w", encoding="utf-8", newline="").write(head + "\n" + ",\n".join(lines) + tail)
ru2 = parse(io.open(p, encoding="utf-8-sig").read())
print(f"записей: {before} -> {len(ru2)} (+{len(pairs)})")
for k, v in NEW.items():
    assert ru2[k] == v, k[:50]
print("JSON валиден")
shutil.copy2(p, r"C:\Users\user\Documents\NuclearOption_Rus\ru.json")
shutil.copy2(p, r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\config\LocalizationPatch\ru.json")

# --- свежий untranslated.txt: что ещё не переведено и похоже на текст интерфейса ---
u = base + r"\untranslated.txt"
print("\nuntranslated.txt:", os.path.getsize(u), "б")
CYR = re.compile(r"[А-Яа-яЁё]")
def looks_real(s):
    if not (12 <= len(s) <= 700) or CYR.search(s):
        return False
    if not re.search(r"[A-Za-z]{2,}\s+[A-Za-z]{2,}", s):
        return False
    letters = sum(1 for c in s if c.isalpha())
    if letters * 100 // max(1, len(s)) < 55:
        return False
    return True
raw_u = io.open(u, encoding="utf-8", errors="replace").read()
cand, junk = [], 0
for m in re.finditer(r'^"((?:[^"\\]|\\.)*)":', raw_u, re.M):
    try:
        s = json.loads('"' + m.group(1) + '"')
    except Exception:
        continue
    if s in ru2:
        continue
    (cand if looks_real(s) else [None])
    if looks_real(s):
        cand.append(s)
    else:
        junk += 1
print("не переведено (отфильтровано как мусор):", junk, "| похожих на текст:", len(cand))
for s in sorted(set(cand))[:40]:
    print("   -", json.dumps(s, ensure_ascii=False)[:160])
