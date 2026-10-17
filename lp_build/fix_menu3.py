# -*- coding: utf-8 -*-
"""Фикс roadmap-ключей (убирает лишние литеральные \n) + новые переводы из свежего экспорта."""
import json, re, io, sys

base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
sys.stdout.reconfigure(encoding="utf-8")
p = base + r"\ru.json"

raw = io.open(p, encoding="utf-8-sig").read()

# 1) в roadmap-записях был лишний литеральный "\n" перед каждой пулей — удаляем
before_cnt = raw.count("\\\\n\u2022")
raw = raw.replace("\\\\n\u2022", "\u2022")
print("исправлено лишних \\n:", before_cnt)

# 2) новые переводы из свежего untranslated.txt (18:09)
NEW = {
    "Internal Guns": "Внутренние пушки",
    "Advanced and flare-resistant medium range infrared air to air missile effective at ranges up to 20km.":
        "Улучшенная помехозащищённая ракета средней дальности класса «воздух-воздух» с ИК-наведением, эффективна на дальностях до 20 км.",
    "A GPO-N has a delay fuse that only lasts for up to 16 seconds, but creates radioactive residue that lasts for years.":
        "У GPO-N взрыватель с задержкой всего до 16 секунд, но остаётся радиоактивный след, сохраняющийся годами.",
    "Although an older design, this light supersonic fighter is exceptionally agile and highly suited to air superiority missions with options for limited low-level ground attack. Twin engines provide an incredible TWR and top speed whilst a centreline internal weapon bay reduces payload drag.":
        "Хотя это и устаревшая конструкция, лёгкий сверхзвуковой истребитель исключительно манёвренный и отлично подходит для миссий на господство в воздухе с возможностью ограниченных ударов по земле на малой высоте. Два двигателя обеспечивают невероятную тяговооружённость и скорость, а внутренний отсек вооружения по оси фюзеляжа снижает аэродинамическое сопротивление.",
    "Newly produced nuclear warheads will be distributed amongst storage bunkers and hardened shelters at each airbase.":
        "Новые ядерные боеголовки будут распределены по хранилищам и укреплённым укрытиям на каждой авиабазе.",
    "Block": "Заблокировать",
    "LABEL": "МЕТКА",
}

ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
data = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)
before = len(data)

idx = raw.rfind("\n}")
head, tail = raw[:idx], raw[idx:]
if not head.rstrip().endswith(","):
    head = head.rstrip() + ","

entries = []
for k, v in NEW.items():
    if k in data:
        print("уже есть:", k[:50])
        continue
    entries.append("    " + json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False))
if entries:
    raw = head + "\n" + ",\n".join(entries) + tail

ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
data2 = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)
print(f"записей: {before} -> {len(data2)} (+{len(entries)})")
io.open(p, "w", encoding="utf-8", newline="").write(raw)
print("СОХРАНЕНО, JSON валиден")
