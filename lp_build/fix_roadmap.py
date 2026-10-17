# -*- coding: utf-8 -*-
"""Строит точные roadmap-ключи (CR/LF как в игре) и правит ru.json."""
import json, re, io, sys

base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
sys.stdout.reconfigure(encoding="utf-8")

RAW = open(base + r"\untranslated.txt", "rb").read().decode("utf-8", "replace")

# --- карта пунктов: английский -> русский ---
BULLETS = {
    "• Additional Boats / Ships": "• Дополнительные катера / корабли",
    "• PALA Landing ship": "• Десантный корабль PALA",
    "• Additional high-end SAMs": "• Дополнительные высокотехнологичные ЗРК",
    "• Additional ground units": "• Дополнительные наземные юниты",
    "• More infantry mechanics": "• Больше механики пехоты",
    "• Missile mechanic changes": "• Изменения механики ракет",
    "• Further development on Ignus Archipelago": "• Дальнейшее развитие Ignus Archipelago",
    "• More destructible/interactible environment": "• Больше разрушаемого и интерактивного окружения",
    "• AI improvements for aircraft, ships, and ground units": "• Улучшения ИИ самолётов, кораблей и наземных юнитов",
    "• Additional control customization": "• Дополнительные настройки управления",
    "• Menu UI improvements": "• Улучшения интерфейса меню",
    "• Additional low-rank aircraft": "• Самолёты низших рангов",
    "• Existing aircraft remasters": "• Переработка существующих самолётов",
    "• Light utility VTOL": "• Лёгкий многоцелевой ВЗС",
    "• Aerial drones": "• Аэродинамические дроны",
    "• Additional helicopters": "• Дополнительные вертолёты",
    "• Additional nuclear weapon types": "• Дополнительные типы ядерного оружия",
    "• Additional conventional weapon types": "• Дополнительные типы обычного оружия",
    "• Terrain and runway cratering": "• Воронки на рельефе и взлётных полосах",
    "• Campaign system": "• Система кампаний",
    "• VR implementation": "• Поддержка VR",
    "• Console version": "• Версия для консолей",
    "• Localization": "• Локализация",
    "• New large landlocked map": "• Новая большая континентальная карта",
    "• Heavy cargo plane": "• Тяжёлый грузовой самолёт",
    "• Continued development and detailing of existing maps": "• Дальнейшее развитие и детализация существующих карт",
    "• More props and buildings": "• Больше объектов и построек",
    "• Logistics and economy changes": "• Изменения логистики и экономики",
    "• Graphics improvements": "• Улучшения графики",
    "• Sound improvements": "• Улучшения звука",
    "• Expanded modding support": "• Расширенная поддержка моддинга",
    "• More destructible/interactible environment and props": "• Ещё больше разрушаемого и интерактивного окружения и объектов",
    "• Expanded Mission Editor functionality": "• Расширенный функционал редактора миссий",
    "• Dynamic music": "• Динамическая музыка",
}

ANCHORS = ("Additional Boats / Ships", "Additional low-rank aircraft", "New large landlocked map")


def unescape(s):
    out, i = [], 0
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s):
            nxt = s[i + 1]
            out.append({"n": "\n", "r": "\r", "t": "\t", '"': '"', "\\": "\\"}.get(nxt, nxt))
            i += 2
        else:
            out.append(ch)
            i += 1
    return "".join(out)


RU_KEYS = []
for a in ANCHORS:
    i = RAW.find(a)
    start = RAW.rfind('"', 0, i) + 1
    end = RAW.find('": ""', i)
    key = unescape(RAW[start:end])
    segs = key.split("\n")
    ru_segs = []
    for seg in segs:
        cr = seg.endswith("\r")
        body = seg[:-1] if cr else seg
        if body not in BULLETS:
            print("!!! нет перевода пункта:", repr(body))
            sys.exit(1)
        ru_segs.append(BULLETS[body] + ("\r" if cr else ""))
    ru_key = "\n".join(ru_segs)
    RU_KEYS.append((key, ru_key))
    print("ключ собран:", len(key), "символов, разделитель CRLF:", key.count("\r"), "| пунктов:", len(segs))

    # оставляем только русские пункты (порядок сохраняется)
    ru_val = "\n".join(s[:-1] + ("\r" if s.endswith("\r") else "") for s in ru_segs)

p = base + r"\ru.json"
raw = io.open(p, encoding="utf-8-sig").read()

# убираем старые мёртвые roadmap-записи (строки, начинающиеся с "• )
lines = raw.split("\n")
kept = []
removed = 0
for ln in lines:
    if ln.lstrip().startswith('"\u2022 '):
        removed += 1
        continue
    kept.append(ln)
raw = "\n".join(kept)
print("удалено старых roadmap-записей:", removed)

ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
data = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)
before = len(data)

idx = raw.rfind("\n}")
head, tail = raw[:idx], raw[idx:]
if not head.rstrip().endswith(","):
    head = head.rstrip() + ","

entries = []
for k, v in RU_KEYS:
    if k in data:
        print("уже есть")
        continue
    entries.append("    " + json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False))
raw = head + "\n" + ",\n".join(entries) + tail

ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
data2 = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)
print(f"записей: {before} -> {len(data2)} (+{len(entries)})")
io.open(p, "w", encoding="utf-8", newline="").write(raw)

# --- проверка: ключи из экспорта должны найтись ---
ok = 0
for k, v in RU_KEYS:
    hit = k in data2
    ok += hit
    print("проверка:", "СОВПАЛ" if hit else "НЕ СОВПАЛ")
print(f"итог: {ok}/{len(RU_KEYS)}")
