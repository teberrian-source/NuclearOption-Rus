# -*- coding: utf-8 -*-
"""Раунд 17 (0.34.6, скрины ангара): описания PTB-1500, GSh-30-1, радара AWACS Beam, метка Dorsal."""
import io, json, os, shutil, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT = os.path.join(REPO, "dict", "ru.json")
GAME_RU = os.path.join(os.environ["USERPROFILE"], "Desktop", "Nuclear.Option.v0.34.6",
                       "BepInEx", "plugins", "LocalizationPatch", "ru.json")

ENTRIES = {
"PTB-1500 centreline drop tank: 1,500 litres (about 1,180 kg) of fuel, used before the internal fuel. Select it and fire to drop it, or press the jettison key (Ctrl+J by default).":
"Подвесной бак PTB-1500 на центральном пилоне: 1500 литров (около 1180 кг) топлива, расходуется до внутренних "
"баков. Выберите его и произведите выстрел, чтобы сбросить, или нажмите клавишу аварийного сброса "
"(по умолчанию Ctrl+J).",

"GSh-30-1: single-barrel 30 mm recoil-operated cannon in the left wing root, 150 rounds. Fires about 1,650 rounds per minute; a one-second burst is a sixth of the magazine, so fire short bursts.":
"GSh-30-1: одноствольная 30-мм пушка с откатом ствола в корне левого крыла, 150 снарядов. Темп около 1650 "
"выстрелов в минуту; секундная очередь — шестая часть боекомплекта, поэтому стреляйте короткими очередями.",

"Long-range radar on a two-stage mast that rises out of the spine. It lies flush in its well on the ground near a hangar and deploys clear of it.":
"Дальнобойный радар на двухсекционной мачте, поднимающейся из хребта фюзеляжа. На земле лежит заподлицо в своём "
"колодце рядом с ангаром, при развёртывании выступает из него целиком.",

"Dorsal": "Спинной",
}

t = io.open(DICT, encoding="utf-8-sig").read()

def parse(text):
    outl, in_str, esc, i = [], False, False, 0
    while i < len(text):
        c = text[i]
        if in_str:
            if esc: esc = False
            elif c == "\\": esc = True
            elif c == '"': in_str = False
            outl.append(c)
        else:
            if c == '"': in_str = True; outl.append(c)
            elif c == "/" and i + 1 < len(text) and text[i + 1] == "/":
                while i < len(text) and text[i] != "\n": i += 1
                continue
            else: outl.append(c)
        i += 1
    return json.loads("".join(outl), strict=False)

d = parse(t)
print("словарь до:", len(d))
for k in ENTRIES:
    if k in d:
        print("УЖЕ ЕСТЬ:", k[:70], "->", d[k][:60])

new_items = []
for k, v in ENTRIES.items():
    if k in d:
        continue
    d[k] = v
    new_items.append((k, v))
print("новых:", len(new_items))

j = t.rstrip().rfind("}")
head, tail = t[:j], t[j:]
head = head.rstrip()
if not head.endswith(","):
    head += ","
block = ",\n".join("    " + json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False)
                  for k, v in new_items)
io.open(DICT, "w", encoding="utf-8", newline="\n").write(head + "\n" + block + "\n" + tail)

d2 = parse(io.open(DICT, encoding="utf-8-sig").read())
missing = [k[:60] for k in ENTRIES if k not in d2]
print("словарь после:", len(d2), "| отсутствуют:", missing if missing else "нет")
shutil.copy2(DICT, GAME_RU)
same = open(DICT, "rb").read() == open(GAME_RU, "rb").read()
print("репо и игра совпадают побайтово:", same)
