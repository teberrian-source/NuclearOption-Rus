# -*- coding: utf-8 -*-
"""Раунд 19b: добор пропущенного — главное описание AH-31 Kukri (с words-фильтр
пропустил из-за 'Chicane'), шуточное описание MC-260 Chimera, названия пилонных
групп Wingtip Rails / Belly (с экрана ангара, точный текст)."""
import io, json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUMP = os.path.join(BASE, "tools", "dump_keys.txt")
DICT = os.path.join(BASE, "dict", "ru.json")

lines = io.open(DUMP, encoding="utf-8").read().splitlines()
kukri = lines[369].strip()      # строка 370
chimera = lines[53].strip()     # строка 54
assert kukri.startswith("The AH-31 Kukri is a 6.2-tonne")
assert chimera.startswith("According to all known laws")

add = {
    kukri: "AH-31 Kukri — двухдвигательный средний ударный вертолёт массой 6,2 т, стоящий на вооружении главным образом у сил обороны Боскали для обороны страны и непосредственной авиационной поддержки. Сочетает продвинутую носовую сенсорную платформу с малой многоцелевой РЛС и 20-мм вращающуюся пушку с магазином на 1100 снарядов и темпом 1200 выстрелов в минуту. По соотношению цена/эффективность это результативная и мощная платформа, но она полагается на крепкую броню и чистую огневую мощь, а не на малозаметность таких машин, как Chicane.",
    chimera: "Согласно всем известным законам аэродинамики и надоедливым людям на сабреддите, MC-260 Chimera летать не должен никак. Его малюсенькие крылья слишком малы, чтобы оторвать от земли его упитанное тельце. Разумеется, Chimera всё равно летает — потому что Aryx плевать, что думает аэродинамика.",
    "Wingtip Rails": "Направляющие на законцовках",
    "Belly": "Подфюзеляжный",
}
print("новых записей:", len(add))

raw = io.open(DICT, encoding="utf-8-sig").read()
for k in add:
    assert k not in raw, f"уже есть: {k[:60]}"
assert raw.rstrip().endswith("}"), "неожиданный конец файла"
block = "    // ==== Round 19b: Kukri (гл. описание), MC-260 Chimera, пилонные группы ====\n"
for k, v in add.items():
    block += f"    {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)},\n"
new_raw = raw.rstrip()[:-1] + block.rstrip().rstrip(",") + "\n}\n"
io.open(DICT, "w", encoding="utf-8", newline="").write(new_raw)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from round19_filter import strip_comments  # noqa: E402
d = json.loads(strip_comments(new_raw), strict=False)
print("словарь валиден, записей:", len(d))
