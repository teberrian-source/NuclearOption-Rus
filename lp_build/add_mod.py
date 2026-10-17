# -*- coding: utf-8 -*-
"""Добавляет переводы строк 0.34.2 в ru.json посегментно (составные \n-ключи собираются из сегментов)."""
import json, re, io, sys

base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
sys.stdout.reconfigure(encoding="utf-8")

# ---------- словарь сегментов (точные тексты из игры) ----------
SEG = {
    # цветные префиксы
    "<color=#C8C8C8>Static emplacement: turret control only, transported by helicopter sling</color>":
        "<color=#C8C8C8>Статичная установка: только управление башней, транспортируется вертолётом на внешней подвеске</color>",
    "<color=#C8C8C8>Static emplacement: turret control only</color>":
        "<color=#C8C8C8>Статичная установка: только управление башней</color>",
    "<color=#FF8080>Insufficient funds</color>":
        "<color=#FF8080>Недостаточно средств</color>",
    "<color=#FF8080>Requires tactical nuclear escalation</color>":
        "<color=#FF8080>Требуется тактическая ядерная эскалация</color>",
    # описания (полные сегменты)
    "A Laser Air Defence System capable of destroying small calibre aerial munitions.":
        "Лазерная система ПВО, способная уничтожать малокалиберные воздушные боеприпасы.",
    "An air-deployable Fire Control system for improving the targeting of air defence batteries.":
        "Десантируемая по воздуху система управления огнём для повышения точности наведения батарей ПВО.",
    "An air-transportable, self-contained anti-air 35mm gun turret and optical tracking system. Fully self-sufficient once deployed with a range of 5km. For best results, pair with an ammo container to keep it topped up.":
        "Транспортируемая по воздуху автономная зенитная установка с 35-мм пушкой и оптической системой слежения. После развёртывания полностью автономна, дальность — 5 км. Для лучших результатов разместите рядом контейнер с боеприпасами, чтобы пополнять боезапас.",
    "Long range air defense trailer capable of engaging aerial targets detected by nearby radar trucks":
        "Дальнобойный зенитный прицеп, способный поражать воздушные цели, обнаруженные ближайшими радарными машинами.",
    "This trailer is equipped with a 20mm rotary gun to provide point defence against shells, missiles, bombs, and low flying aircraft within a range of approximately 3km.":
        "Этот прицеп оснащён 20-мм вращающейся пушкой для защиты от снарядов, ракет, бомб и низколетящих самолётов в радиусе примерно 3 км.",
    "This transportable air defense missile launcher capable of engaging aerial targets within 15km. It can be deployed by a utility aircraft and obtains target info from a nearby radar.":
        "Транспортируемая зенитная ракетная пусковая, поражающая воздушные цели в радиусе до 15 км. Может быть развернута транспортным самолётом и получает данные о цели от ближайшего радара.",
    "A compact, somewhat non-euclidean deployable helipad for deployment and rearmament of rotary-wing aviation. Armed with IRM-S1 and 12.7mm machine gun turrets for self defence.":
        "Компактная, отчасти неевклидова разворачиваемая вертолётная площадка для развёртывания и перевооружения вертолётов. Вооружена башнями с IRM-S1 и 12,7-мм пулемётом для самообороны.",
    "Long range launcher armed with a nuclear-tipped hypersonic missile. Will deploy and fire automatically on known datalinked targets once the strategic escalation threshold is met.":
        "Дальнобойная пусковая с гиперзвуковой ракетой с ядерной боевой частью. Автоматически разворачивается и открывает огонь по известным целям в даталинке после достижения порога стратегической эскалации.",
    "Long range launcher armed with a pair of 20kt Nuclear Piledrivers. Will deploy and fire automatically on known datalinked targets once the strategic escalation threshold is met.":
        "Дальнобойная пусковая с парой ядерных ракет «Nuclear Piledriver» калибра 20 кт. Автоматически разворачивается и открывает огонь по известным целям в даталинке после достижения порога стратегической эскалации.",
    "Long range launcher armed with a pair of HE Piledrivers. Will deploy and fire automatically on known datalinked targets once the strategic escalation threshold is met.":
        "Дальнобойная пусковая с парой ракет «Piledriver» с фугасной боевой частью. Автоматически разворачивается и открывает огонь по известным целям в даталинке после достижения порога стратегической эскалации.",
    "Long range launcher armed with a HE hypersonic missile. Will deploy and fire automatically on known datalinked targets once the strategic escalation threshold is met.":
        "Дальнобойная пусковая с гиперзвуковой ракетой с фугасной боевой частью. Автоматически разворачивается и открывает огонь по известным целям в даталинке после достижения порога стратегической эскалации.",
    "18-tube Multiple Launch Rocket System installed on an MSV chassis, providing mobile rocket artillery.":
        "18-трубная реактивная система залпового огня на шасси MSV — мобильная реактивная артиллерия.",
    "A Modular Support Vehicle equipped with a 20mm rotary gun to provide point defence against shells, missiles, bombs, and low flying aircraft within a range of approximately 3km.":
        "Модульная поддерживающая машина с 20-мм вращающейся пушкой для защиты от снарядов, ракет, бомб и низколетящих самолётов в радиусе примерно 3 км.",
    "Although over 100 years old, the F-16 remains a mainstay in air forces worldwide, with the latest Block 165 variants in service with both the BDAF and PALAAF. Upgrade packages and competitive lobbying have kept it in the game; The Viper truly is eternal.":
        "Хотя ему и больше 100 лет, F-16 по-прежнему остаётся основой ВВС по всему миру; новейшие варианты Block 165 состоят на вооружении BDAF и PALAAF. Пакеты модернизации и активное лоббирование сохранили его в строю; Viper поистине бессмертен.",
    "An upfit of the Force Reconnaissance Combat Vehicle chassis, the FRCV-SPG forgoes its usual 105mm gun in exchange for a 152mm L/40 howitzer firing guided rounds. The rounds fired by this unit sport their own optical scanners and datalink their imagery back to the unit to spot enemy targets and confirm hits from safe distances. Like the HLT MART, the FRCV-SPG operates on a shoot-and-scoot profile and is air-deployable by the MC-260 Chimera":
        "На базе шасси Force Reconnaissance Combat Vehicle: FRCV-SPG вместо обычной 105-мм пушки получил 152-мм гаубицу L/40, стреляющую управляемыми снарядами. Эти снаряды несут собственные оптические сканеры и передают изображение обратно машине для обнаружения целей и подтверждения попаданий с безопасного расстояния. Как и HLT MART, FRCV-SPG действует по тактике «выстрелил — скрылся» и может десантироваться с MC-260 Chimera.",
    "`The Combat Reconnaissance Vehicle (Light) / Serval is an 8-tonne armoured fighting vehicle designed for use as a scout and expeditionary warfare platform. The CRV-L offers high cross-country performance and high modularity for a variety of missions. The Recon variant is equipped with a 25mm autocannon for taking on medium armoured targets from flanks, and has excellent stealth & optics.`":
        "`Боевая машина разведки (лёгкая) / Serval — 8-тонная бронированная машина, спроектированная для разведки и экспедиционных операций. CRV-L обладает высокой проходимостью и широкой модульностью для выполнения различных задач. Разведывательная версия оснащена 25-мм автоматической пушкой для поражения среднебронированных целей с флангов и отличными скрытностью и оптикой.`",
    "The Combat Reconnaissance Vehicle (Light) / Serval is an 8-tonne armoured fighting vehicle designed for use as a scout and expeditionary warfare platform. The CRV-L offers high cross-country performance and high modularity for a variety of missions. This variant is equipped with a rapid-fire 81mm mortar for short to medium range light artillery.":
        "Боевая машина разведки (лёгкая) / Serval — 8-тонная бронированная машина, спроектированная для разведки и экспедиционных операций. CRV-L обладает высокой проходимостью и широкой модульностью для выполнения различных задач. Эта версия оснащена скорострельным 81-мм миномётом для лёгкой артиллерии малой и средней дальности.",
    "The Force Reconnaissance Combat Vehicle is a 27T deployable light tank and force-recon vehicle. Armed with a 105mm high velocity cannon and 12.7mm coaxial, the FRCV is designed to be deployed behind enemy lines to wreak havoc on supply lines, less protected airstrips and spot targets.":
        "Force Reconnaissance Combat Vehicle — разворачиваемый лёгкий танк и машина силовой разведки массой 27 т. Вооружён 105-мм пушкой высокой скорострельности и спаренным 12,7-мм пулемётом; предназначен для развёртывания за линией противника с целью подрыва снабжения, уничтожения слабо защищённых аэродромов и разведки целей.",
    "The M12 jackknife, despite only weighing 6 tons, is able to punch well above its weight as an earthmover by using its internal capacity as ballast.":
        "M12 Jackknife, несмотря на массу всего 6 тонн, работает гораздо продуктивнее своего веса в роли землеройной машины, используя внутренний объём в качестве балласта.",
    "The Medusa's laser's effectiveness is affected by distance, and its maximum effective range is 15km. Using it at short range delivers more energy to a target, even burning aircraft at very short range.":
        "Эффективность лазера Medusa зависит от расстояния, максимальная эффективная дальность — 15 км. Использование на малой дистанции доставляет цели больше энергии, позволяя даже поджигать самолёты вблизи.",
    "This advanced and highly mobile long-range artillery system fires 155mm laser guided shells. Capable of bombarding targets 40km away at a sustained 5 rounds per minute, the HLT Mobile Artillery will frequently relocate to avoid return fire.":
        "Эта продвинутая высокомобильная артиллерийская система дальнего действия стреляет 155-мм управляемыми снарядами. Способная обстреливать цели на расстоянии 40 км с устойчивой скорострельностью 5 выстрелов в минуту, HLT Mobile Artillery часто меняет позиции, чтобы избежать ответного огня.",
    "This beefy bit of kit on the 10-wheeler HLT variant sports four launch tubes for the R-100N Zenith Strategic Interceptor, a high altitude interceptor missile designed to destroy dangerous threats like the Piledriver TBM and Starfall HSM. Firing exclusively on high value, high altitude, high speed threats, it features a 0.5 kiloton nuclear warhead to all but guarantee the destruction of the target.":
        "Эта внушительная установка на десятиколёсном шасси HLT несёт четыре пусковые трубы для R-100N Zenith Strategic Interceptor — ракеты перехвата большой высоты, предназначенной для уничтожения таких угроз, как Piledriver TBM и Starfall HSM. Поражая исключительно ценные, высокоидущие и быстрые цели, она несёт 0,5-килотонную ядерную боевую часть, практически гарантирующую уничтожение цели.",
    "This small yet nimble unmanned combat drone offers an  unparalleled thrust-to-weight ratio and G-tolerance,  at the expense of less capable countermeasures, sensor systems, and endurance.  Originally designed for full autonomy, its systems were not intended for  remote piloting and may therefore exhibit unusual flight characteristics.":
        "Этот небольшой, но проворный беспилотный боевой аппарат отличается непревзойдённым соотношением тяги к массе и запасом по перегрузкам — ценой менее совершенных средств противодействия, сенсорных систем и автономности. Изначально созданный для полной автономии, он не был предназначен для дистанционного пилотирования и может демонстрировать необычное поведение в полёте.",
    "Using the afterburner will increase your infrared signature and greatly reduces the relative effectiveness of flares.":
        "Использование форсажа увеличивает ваш инфракрасный след и значительно снижает относительную эффективность ловушек.",
    "Vortex Ring State is a dangerous aerodynamic condition where a rotor disc stops producing lift due to ingesting its own downwash. It can be escaped from by applying full power and moving laterally.":
        "Кольцевой вихрь (Vortex Ring State) — опасное аэродинамическое состояние, при котором диск винта перестаёт создавать подъёмную силу, поглощая собственную струю. Из него можно выйти, применив полную тягу и перемещаясь вбок.",
    "Target enemy units in sector A9, beware of SAM sites defenses and air patrols.":
        "Поражайте вражеские юниты в секторе A9, остерегайтесь ПВО и воздушных патрулей.",
    "Vehicle Depot\nSelect + [F7]: purchase vehicles":
        "Склад техники\nSelect + [F7]: покупка техники",
    "The Chicane can be taken down with a Nuke":
        "Chicane можно сбить ядерным зарядом",
    "this vehicle can't capture":
        "эта техника не может захватывать",
    "Welcome to Nuclear Option Early Access 0.34!":
        "Добро пожаловать в Nuclear Option, ранний доступ 0.34!",
}

# ---------- короткие UI-лейблы (точное совпадение ключа) ----------
SHORT = {
    "(toggle F3)": "(переключить F3)",
    "(toggle F4)": "(переключить F4)",
    "Acceleration": "Разгон",
    "Airspeed": "Скорость",
    "Allies": "Союзники",
    "ANGLE": "УГОЛ",
    "CAMERA CONTROLS": "УПРАВЛЕНИЕ КАМЕРОЙ",
    "CAMERA TRANSFORM": "ТРАНСФОРМАЦИЯ КАМЕРЫ",
    "Cargo Options >": "Опции груза >",
    "Cargo Value :": "Стоимость груза :",
    "Centreline Pylon": "Фюзеляжный пилон",
    "Cockpit": "Кабина",
    "COMING SOON": "СКОРО",
    "CONCEPT STAGE": "СТАДИЯ КОНЦЕПЦИИ",
    "Connections": "Соединения",
    "Control": "Управление",
    "Cooldown :": "Перезарядка :",
    "Current": "Текущая",
    "Current Target": "Текущая цель",
    "DEPLOY >": "РАЗВЕРНУТЬ >",
    "DEVELOPMENT ROADMAP": "ПЛАН РАЗРАБОТКИ",
    "Did you know ?": "А знаете ли вы?",
    "Driving to Restock": "Едет на пополнение",
    "Early Access Version 0.34.2": "Ранний доступ, версия 0.34.2",
    "FACTION NAME": "НАЗВАНИЕ ФРАКЦИИ",
    "FIELD OF VIEW": "ПОЛЕ ЗРЕНИЯ",
    "Flyby": "Пролёт",
    "GROUND": "ЗЕМЛЯ",
    "HULL": "КОРПУС",
    "IN DEVELOPMENT": "В РАЗРАБОТКЕ",
    "IN RANGE": "В ДАЛЬНОСТИ",
    "Incoming Missiles": "Входящие ракеты",
    "INERTIA": "ИНЕРЦИЯ",
    "Info Text": "Информационный текст",
    "INPUTS": "ВХОДЫ",
    "INSUFFICIENT FUNDS": "НЕДОСТАТОЧНО СРЕДСТВ",
    "Internal Weapons Bay": "Внутренний отсек вооружения",
    "IR Flares": "ИК-ловушки",
    "JOIN FACTION": "ВСТУПИТЬ В ФРАКЦИЮ",
    "LOOK": "ОБЗОР",
    "LOOK AT": "СМОТРЕТЬ НА",
    "MAXIMIZE": "РАЗВЕРНУТЬ",
    "Main": "Основной",
    "Merch Store": "Магазин мерча",
    "Mid Wing Pylons": "Пилоны средней секции",
    "MIN 500m": "МИН 500 м",
    "MISSION INFO": "ИНФОРМАЦИЯ О МИССИИ",
    "MOVEMENT": "ДВИЖЕНИЕ",
    "none": "нет",
    "OBJECTIVE": "ЗАДАЧА",
    "Orbit": "Орбита",
    "PITCH": "ТАНГАЖ",
    "PIVOT": "ПОВОРОТ",
    "PLAYER": "ИГРОК",
    "POS": "ПОЗ",
    "Position": "Позиция",
    "Price :": "Цена :",
    "RANK": "ЗВАНИЕ",
    "Received": "Получено",
    "Remaining :": "Осталось :",
    "Render": "Рендер",
    "REQUISITION": "ЗАПРОС",
    "RNG": "ДАЛЬН",
    "ROLL": "КРЕН",
    "SELECT": "ВЫБРАТЬ",
    "SELECT VEHICLE": "ВЫБРАТЬ ТЕХНИКУ",
    "Select Vehicle Depot...": "Выберите склад техники...",
    "SELL": "ПРОДАТЬ",
    "Sent": "Отправлено",
    "State": "Состояние",
    "STATES": "СОСТОЯНИЯ",
    "Steam Profile": "Профиль Steam",
    "Strafing": "Стрельба с бреющего",
    "Sync\nDelta": "Синк\nДельта",
    "Target": "Цель",
    "TIME": "ВРЕМЯ",
    "Toggle": "Переключить",
    "Type :": "Тип :",
    "UNAVAILABLE": "НЕДОСТУПНО",
    "UNIT": "ЮНИТ",
    "VEHICLE DEPOT": "СКЛАД ТЕХНИКИ",
    "VOTE KICK": "ГОЛОСОВАНИЕ ЗА КИК",
    "Wait": "Ожидание",
    "Wing Pylon": "Крыльевой пилон",
}

# ---------- статблоки: замена лейблов (числа и оружие не трогаем) ----------
BLOCK_REPL = [
    ("Self-deploying, Sling load", "Самоустанавливающаяся, подвеска"),
    ("Deployable, Sling load", "Разворачиваемая, подвеска"),
    ("Self-deploying", "Самоустанавливающаяся"),
    ("Sling load", "Подвеска"),
    ("Mobility :", "Мобильность :"),
    ("Road :", "Дорога :"),
    ("Off-road :", "Бездорожье :"),
    ("Mass :", "Масса :"),
    ("Armor :", "Броня :"),
    (">Static<", ">Статичная<"),
    (">Static\n", ">Статичная\n"),
]

def make_block(k):
    """Характеристики юнитов: заменяет лейблы, оставляя числа и названия оружия."""
    if not (k.startswith("Mobility :") or k.startswith("Road :")):
        return None
    if "<pos=50%>" not in k:
        return None
    v = k
    for a, b in BLOCK_REPL:
        v = v.replace(a, b)
    v = re.sub(r"(\d),(\d)t\b", r"\1,\2 т", v)
    return v if v != k else None

# ---------- сбор ключей untranslated ----------
u = base + r"\untranslated.txt"
keys = []
for line in io.open(u, encoding="utf-8-sig").read().split("\n"):
    line = line.strip()
    if not line.startswith('"'):
        continue
    try:
        obj = json.loads("{" + line.rstrip(",") + "}")
    except Exception:
        continue
    keys.append(next(iter(obj)))

full = {}
for k in keys:
    if k in SEG:
        full[k] = SEG[k]
        continue
    if k in SHORT:
        full[k] = SHORT[k]
        continue
    # составной: все \n-сегменты известны
    if "\n" in k:
        segs = k.split("\n")
        if all(s in SEG or s in SHORT for s in segs):
            full[k] = "\n".join(SEG.get(s, SHORT.get(s)) for s in segs)
            continue
    v = make_block(k)
    if v:
        full[k] = v

print("кандидатов в словаре:", len(full))

# ---------- запись в ru.json ----------
p = base + r"\ru.json"
raw = io.open(p, encoding="utf-8-sig").read()
ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
data = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)
before = len(data)
skip = [k for k in full if k in data]
print("уже есть:", len(skip))

idx = raw.rfind("\n}")
head, tail = raw[:idx], raw[idx:]
if not head.rstrip().endswith(","):
    head = head.rstrip() + ","

new_entries = []
for k, v in full.items():
    if k in data:
        continue
    new_entries.append("    " + json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False))
if new_entries:
    raw = head + "\n" + ",\n".join(new_entries) + tail

ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
data2 = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)
print(f"записей: {before} -> {len(data2)} (+{len(new_entries)})")
io.open(p, "w", encoding="utf-8", newline="").write(raw)
print("СОХРАНЕНО")
