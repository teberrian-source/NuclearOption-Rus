# -*- coding: utf-8 -*-
"""Раунд 16 (0.34.6): добавление переводов с новой сессии 16.11.
Ключи берутся ДОСЛОВНО из untranslated.txt (тексты миссий обновились в 0.34.6),
правильный unescape -> json.dumps при записи. Полная перезапись словаря валидным JSON."""
import io, json, os, re, shutil, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT = os.path.join(REPO, "dict", "ru.json")
GAME_RU = os.path.join(os.environ["USERPROFILE"], "Desktop", "Nuclear.Option.v0.34.6",
                       "BepInEx", "plugins", "LocalizationPatch", "ru.json")
DUMP = os.path.join(os.environ["USERPROFILE"], "Desktop", "Nuclear.Option.v0.34.6",
                    "BepInEx", "plugins", "LocalizationPatch", "untranslated.txt")

# --- 1. разобрать дамп: raw-строки между кавычками ---
raw = []
for l in io.open(DUMP, encoding="utf-8").read().splitlines():
    m = re.match(r'^"(.+)": ""[,]?$', l)
    if m:
        raw.append(m.group(1))

def real(raw_s):
    """raw-тело JSON-строки из дампа -> реальная строка времени исполнения."""
    return json.loads('"' + raw_s + '"')

dump_real = [real(r) for r in raw]

# --- 2. переводы: ключ -> готовый перевод ---
TWO_FRONTS = ("The whole of Ironjaw Sound at war, built like the stock Escalation, with two fronts")
SOUTH_HOLD = ("The whole of Ironjaw Sound at war, built like the stock Escalation. Boscali hold the south")

LONG = {
TWO_FRONTS:
"Весь Ironjaw Sound в состоянии войны, построено как стандартная Escalation, но с двумя фронтами. "
"На западе бронетехника сражается за Cinder Range: Боскали наступают на север от склада Delta Gate, "
"Примева — на юг от Cinder Gate, а вертолёты с передовых площадок Dunmore West и Dunmore East дерутся "
"за Dunmore Crossing. В центре, над Halvard Arm, сходятся реактивные самолёты: Боскали летают с Fenwick Field "
"и авианосца у Ostrin Isles, Примева — с Graylock South. У каждой стороны есть авиазаводы и завод обогащения "
"в тылу и автозаводы, снабжающие её передовой склад. Заводы достраивают новые самолёты в течение всего матча, "
"поэтому тяжёлые реактивные машины прибывают поздно. Подкрепления идут по дороге Cinder Notch и западной дороге "
"через Hollin Mine. Ostrin Isles, Dunmore Crossing и Hollin Mine начинаются нейтральными и становятся передовыми "
"точками высадки для тех, кто их возьмёт; Примева может потерять Skerry и Graylock South, Боскали — Fenwick после "
"падения склада Delta Gate. Каждый захват добавляет самолётов в воздух, а разбитый склад — ещё больше. "
"Чтобы победить: взломайте передовой склад противника, затем уничтожьте его авиазаводы. Все начинают с рангом 0; "
"ядерное оружие открывается на эскалации 256.",

SOUTH_HOLD:
"Весь Ironjaw Sound в состоянии войны, построено как стандартная Escalation. Боскали держат юг: Sorrel Field, "
"Rook Island, FARP Kittiwake и FARP Delta Gate. Примева держат фьорды и северо-восток: Tarn Head Strip, "
"Graylock Strip, Graylock South, Brekka Hills и FARP Cinder Gate. У Боскали два комплекса авиазаводов и завод "
"обогащения рядом с Sorrel Field; Примева строят свои самолёты далеко на северо-востоке, на равнине Graylock и "
"в Brekka Hills, с заводом обогащения в вершине Graylock Fjord и автозаводами, снабжающими склад на их передовом "
"FARP. Заводы достраивают новые самолёты в течение всего матча, поэтому тяжёлые реактивные машины прибывают поздно. "
"Бронетехника начинает наступление с первых минут, а колонны подкреплений идут по дороге Cinder Notch и западной "
"дороге через Hollin Mine. Пять зон высадки между ними начинаются нейтральными и становятся передовыми точками "
"высадки для тех, кто их возьмёт. Чтобы победить: взломайте передовой склад противника, затем уничтожьте его "
"авиазаводы. Все начинают с рангом 0; ядерное оружие открывается на эскалации 256.",

"A Confrontation-style war":
"Война в стиле Confrontation за восточную половину карты. Боскали летают с авианосной группы к югу от Kittiwake "
"и с зон высадки Fenwick и Kittiwake; Примева — с Graylock Strip, Graylock South и Brekka Hills. Авиазаводы к "
"западу от Fenwick и на полуострове Graylock достраивают новые машины. Ostrin Isles и Skerry Island начинаются "
"нейтральными; их занимают вертолётные войска. Чтобы победить, уничтожьте авиазаводы противника. Все начинают "
"с рангом 0.",

"A Primeva amphibious fleet is massing":
"Амфибийный флот Примевы накапливается восточнее Ansel Reach, чтобы захватить Port Ansel, а вторая волна позже "
"подойдёт по Gannet Sound. Боскали должны потопить оба флота, пока те не сожгли портовые топливные баки; Примева "
"побеждает, если склад баков горит. За обе стороны летает ИИ-авиация.",

"A small, Altercation-size strike":
"Небольшой удар в масштабах Altercation вверх по Graylock Fjord. Авианосная группа Боскали ждёт далеко к югу от "
"устья фьорда, с передовой площадкой на Skerry Island. Примева держат фьорд корветами, позициями SAM, дальнобойной "
"батареей и бронетехникой, охраняющей склад снабжения у Sill — узкой переправы в глубине фьорда. Боскали должны "
"уничтожить склад и его охрану; Примева побеждает, если продержится 45 минут или потопит авианосец.",

"Primeva has walled off the Lower Ice":
"Примева отрезала Нижний лёд. Между Fenwick и заводом обогащения Col Works стоят три рубежа. Первый — "
"радиолокационный дозор у Gate на северном берегу внутренней бухты, в 11 км: он видит всё, что покидает Fenwick. "
"Уничтожьте его — и их истребители ослепнут наполовину. Дальше — склад и парк бронетехники на леднике. "
"Радиолокационный SAM, SAM-A1, стоит на открытом льду в 5 км дальше и включается в момент падения Gate. Хребты "
"прячут его от Fenwick, но он смотрит прямо вдоль льда, поэтому заходите над хребтами, а не вверх по леднику. "
"Последний — Col Works, под вторым радиолокационным SAM на хребте севернее завода. К тому моменту вам откроют "
"тактическое оружие. Уничтожьте любой из двух его обогатительных заводов — и реактор никогда не запустится. "
"Все известные SAM у вас на карте. Ожидайте их истребители в первые две минуты, а также удары по топливному "
"складу Fenwick, в 2 км за северо-восточным торцом полосы, — с северо-востока. Пушки и ПЗРК стоят кольцом вокруг "
"полосы и схемы набора высоты, но до склада не дотягиваются: склад защищаете вы и две пары прикрытия. Потеряем "
"склад — или истечёт 60-минутный таймер — и мы проиграли.",

"Primeva have spread seven long-range SAM sites":
"Примева раскидала семь дальнобойных позиций SAM по фьордовым землям, а мобильный SAM патрулирует дорогу "
"Cinder Notch. Боскали должны уничтожить все радары SAM в течение часа; Примева побеждает, если «зонт» уцелеет. "
"За обе стороны летает ИИ-авиация.",

"Take part in a PALA operation":
"Примите участие в операции PALA: выманить и окружить наземные силы BDF, а затем методично уничтожить их — "
"на устаревшей машине, выжатой на предел её возможностей.",

"Welcome to the beautiful Swiss Alps":
"Добро пожаловать в прекрасные Швейцарские Альпы! Это свободный полёт, так что врагов поблизости не ждите.\n\n"
"Внимание! Для работы миссии нужен следующий мод с картой Swiss Alps. Подробности смотрите в описании в мастерской.",

"NEEDS: NOCustomMaps 1.4+":
"ТРЕБУЕТСЯ: NOCustomMaps 1.4+ и карта Cascadia, сборка cm.cascadia.2546c698 (установите «Cascadia Falling» через "
"Nuclear Option Mod Manager или положите cascadia-0.1.0.nomapz в BepInEx\\plugins\\NOCustomMaps\\maps). У всех в "
"сессии должна быть та же сборка карты. Опционально: NOGridLetters для читаемых обозначений квадратов.\n\n"
"Cascadia Falling. PALA атакует Puget Sound со стороны Тихого океана и Strait of Georgia; BDF обороняет Такому. "
"PvP: за обе стороны можно играть.\n\n"
"BDF стартует почти со всем: 9 аэродромов, 4 FOB, 7 площадок, 4 поля шахт, два авианосца Hyperion на трёх "
"военно-морских базах и пары пикетов по всему проливу. PALA держит CFB Comox и с T+0 имеет в море две авианосные "
"группы, каждая — 1 Hyperion, 2 Argus, 2 Dynamo, 4 корвета и один Annex: одна входит в Strait of Juan de Fuca со "
"стороны океана (квадрат P8) и идёт на восток, вторая стоит у вершины Strait of Georgia (квадрат E12) и идёт на юг "
"через Rosario Strait. Они встречаются у Port Townsend, затем кильватерной колонной проходят Admiralty Inlet и "
"спускаются вниз по проливу: западная сила — к Commencement Bay у Такомы, северная — к Elliott Bay у Сиэтла. "
"Новая группа входит на каждом направлении каждые десять минут с T+20 до T+120, каждая чуть дальше предыдущей, "
"и идёт тем же маршрутом: снова авианосные группы на T+30 и T+70, между ними — надводные группы из четырёх "
"кораблей, и авианосцы всю миссию поднимают ИИ-самолёты. Затем идут высотные противокорабельные удары Alkyon и "
"пакеты Darkreach, десантные катера у Port Angeles и Birch Bay, колонны по I-5 и горным дорогам, подъёмы "
"Tarantula, высаживающие 6x6 ПВО на площадки под прикрытием Brawler и Revoker, а с T+95 — ядерные ударные пакеты "
"по полям шахт. Всё, что захватывает PALA, работает на PALA.\n\n"
"BDF побеждает, потопив все 6 десантных авианосцев (последний прибывает на T+70) или удерживая JBLM, FOB Fort "
"Lewis, порт Такомы и Narrows до T+150. PALA побеждает, взяв эти четыре точки; все прочие аэродромы, FOB, "
"площадки и военно-морские базы BDF — цели PALA на пути, и каждое поле шахт надо вывести из строя. Стратегический "
"релиз наступает на T+90 и активирует 24 шахтные пусковые.\n\n"
"Ключ карты cm.cascadia.2546c698. Карта и плагин: github.com/netmaster296/CascadiaFalling.",

"Light short-range infrared missile":
"Лёгкая малодальняя ракета с ИК-головкой самонаведения. Очень манёвренная; лучше всего внутри 6 км.",

"Short-range infrared missile. Thrust vectoring":
"Малодальняя ракета с ИК-головкой самонаведения. Управление вектором тяги и ГСН с захватом на 45° от оси; "
"лучше всего внутри 15 км.",
}

UI = {
"<b>Esc</b> Close": "<b>Esc</b> Закрыть",
"1 Found": "Найдено: 1",
"Aircraft : AA-nn": "Самолёт : AA-nn",
"Aircraft:": "Самолёт:",
"Commands": "Команды",
"Cursor : AA-nn": "Курсор : AA-nn",
"History": "История",
"Initiates a vote-kick or kick if local player is host or administator":
    "Запускает голосование за исключение игрока или исключает сразу, если локальный игрок — хост или администратор",
"No Results": "Нет результатов",
"Hardened Aircraft Shelter": "Укреплённое самолётное укрытие",
}

# --- 3. собрать пары (реальный ключ, реальное значение) ---
entries = {}
for prefix, ru in LONG.items():
    src = next((s for s in dump_real if s.startswith(prefix)), None)
    if src is None:
        print("[!!] не найдено в дампе:", prefix[:60]); continue
    entries[src] = ru

for key, val in UI.items():
    src = next((s for s in dump_real if s == key), None)
    if src is None:
        print("[!!] нет в дампе (всё равно добавляю):", key)
    entries[key] = val

# строки Select / Navigate с тегами шрифта — правкой хвоста
for probe, word in [("Select", "Выбрать"), ("Navigate", "Навигация")]:
    src = next((s for s in dump_real if "MaterialSymbolsSharp" in s and s.endswith(probe)), None)
    if src:
        entries[src] = src[: -len(probe)] + word
    else:
        print("[!!] строка", probe, "не найдена")

# --- 4. разобрать словарь, добавить, перезаписать валидным JSON ---
t = io.open(DICT, encoding="utf-8-sig").read()
outl, in_str, esc, i = [], False, False, 0
while i < len(t):
    c = t[i]
    if in_str:
        if esc: esc = False
        elif c == "\\": esc = True
        elif c == '"': in_str = False
        outl.append(c)
    else:
        if c == '"': in_str = True; outl.append(c)
        elif c == "/" and i + 1 < len(t) and t[i + 1] == "/":
            while i < len(t) and t[i] != "\n": i += 1
            continue
        else: outl.append(c)
    i += 1
d = json.loads("".join(outl), strict=False)
print("словарь до:", len(d))

added, skipped = 0, 0
new_items = []
for k, v in entries.items():
    if k in d and d[k] == v:
        skipped += 1; continue
    d[k] = v; added += 1
    new_items.append((k, v))
print("добавлено:", added, "| уже были:", skipped)

# текстовая вставка перед закрывающей скобкой (//-комментарии сохраняются)
j = t.rstrip().rfind("}")
assert j > 0, "не найдена закрывающая скобка"
head, tail = t[:j], t[j:]
head = head.rstrip()
assert head.endswith('"') or head.endswith(","), "неожиданный конец словаря: " + repr(head[-30:])
if not head.endswith(","):
    head += ","
block = ",\n".join("    " + json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False)
                  for k, v in new_items)
text = head + "\n" + block + "\n" + tail
io.open(DICT, "w", encoding="utf-8", newline="\n").write(text)

# --- 5. валидация (парсером стиля плагина) и раскатка в игру ---
t2 = io.open(DICT, encoding="utf-8-sig").read()
outl2, in_str2, esc2, i2 = [], False, False, 0
while i2 < len(t2):
    c = t2[i2]
    if in_str2:
        if esc2: esc2 = False
        elif c == "\\": esc2 = True
        elif c == '"': in_str2 = False
        outl2.append(c)
    else:
        if c == '"': in_str2 = True; outl2.append(c)
        elif c == "/" and i2 + 1 < len(t2) and t2[i2 + 1] == "/":
            while i2 < len(t2) and t2[i2] != "\n": i2 += 1
            continue
        else: outl2.append(c)
    i2 += 1
d2 = json.loads("".join(outl2), strict=False)
missing = [k[:60] for k in entries if k not in d2]
print("словарь после:", len(d2), "| отсутствуют:", missing if missing else "нет")
shutil.copy2(DICT, GAME_RU)
same = open(DICT, "rb").read() == open(GAME_RU, "rb").read()
print("репо и игра совпадают побайтово:", same)
