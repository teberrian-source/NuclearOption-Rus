# -*- coding: utf-8 -*-
"""Добавляет переводы из свежей сессии: описания, настройки HeadTrack, UI Wing Command."""
import json, re, io, sys

base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
sys.stdout.reconfigure(encoding="utf-8")

# ---- roadmap (полные ключи взяты из untranslated.txt: реальный \n + литеральный \n) ----
RM1 = ("• Additional Boats / Ships\n\\n• PALA Landing ship\n\\n• Additional high-end SAMs\n\\n"
       "• Additional ground units\n\\n• More infantry mechanics\n\\n• Missile mechanic changes\n\\n"
       "• Further development on Ignus Archipelago\n\\n• More destructible/interactible environment\n\\n"
       "• AI improvements for aircraft, ships, and ground units\n\\n• Additional control customization\n\\n"
       "• Menu UI improvements")
RM1_RU = ("• Дополнительные катера / корабли\n\\n• Десантный корабль PALA\n\\n• Дополнительные высокотехнологичные ЗРК\n\\n"
          "• Дополнительные наземные юниты\n\\n• Больше механики пехоты\n\\n• Изменения механики ракет\n\\n"
          "• Дальнейшее развитие Ignus Archipelago\n\\n• Больше разрушаемого и интерактивного окружения\n\\n"
          "• Улучшения ИИ самолётов, кораблей и наземных юнитов\n\\n• Дополнительные настройки управления\n\\n"
          "• Улучшения интерфейса меню")
RM2 = ("• Additional low-rank aircraft\n\\n• Existing aircraft remasters\n\\n• Light utility VTOL\n\\n"
       "• Aerial drones\n\\n• Additional helicopters\n\\n• Additional nuclear weapon types\n\\n"
       "• Additional conventional weapon types\n\\n• Terrain and runway cratering\n\\n• Campaign system\n\\n"
       "• VR implementation\n\\n• Console version\n\\n• Localization")
RM2_RU = ("• Самолёты низших рангов\n\\n• Переработка существующих самолётов\n\\n• Лёгкий многоцелевой ВЗС\n\\n"
          "• Аэродронные БПЛА\n\\n• Дополнительные вертолёты\n\\n• Дополнительные типы ядерного оружия\n\\n"
          "• Дополнительные типы обычного оружия\n\\n• Воронки на рельефе и взлётных полосах\n\\n• Система кампаний\n\\n"
          "• Поддержка VR\n\\n• Версия для консолей\n\\n• Локализация")
RM3 = ("• New large landlocked map\n\\n• Heavy cargo plane\\n• Continued development and detailing of existing maps\n\\n"
       "• More props and buildings\n\\n• Logistics and economy changes\n\\n• Graphics improvements\n\\n"
       "• Sound improvements\n\\n• Expanded modding support\n\\n• More destructible/interactible environment and props\n\\n"
       "• Expanded Mission Editor functionality\n\\n• Dynamic music")
RM3_RU = ("• Новая большая континентальная карта\n\\n• Тяжёлый грузовой самолёт\n• Дальнейшее развитие и детализация существующих карт\n\\n"
          "• Больше объектов и построек\n\\n• Изменения логистики и экономики\n\\n• Улучшения графики\n\\n"
          "• Улучшения звука\n\\n• Расширенная поддержка моддинга\n\\n• Ещё больше разрушаемого и интерактивного окружения\n\\n"
          "• Расширенный функционал редактора миссий\n\\n• Динамическая музыка")

NEW = {
    RM1: RM1_RU,
    RM2: RM2_RU,
    RM3: RM3_RU,
    # ---- описания из магазина / подсказки ----
    "Small emplacements can remain hidden until they fire, giving them the ability to ambush low flying aircraft.":
        "Малые укрепления могут оставаться незамеченными до первого выстрела, позволяя устраивать засады на самолёты, летящие на малой высоте.",
    "Units that can store nuclear warheads include Munitions Bunkers, Hardened Shelters, and Aircraft Carriers. Destroy these to deny the enemy the ability to use nukes.":
        "Ядерные боеголовки хранятся в складах боеприпасов, укреплённых укрытиях и на авианосцах. Разрушьте их, чтобы лишить противника возможности применять ядерное оружие.",
    "The ARAD-45 uses the same body as the RAM-45 missile, but with an anti-radiation seeker, which will lock on to radar emissions after launch, making it ideal for attacking SAM sites at medium range.":
        "ARAD-45 использует корпус ракеты RAM-45, но оснащён головкой самонаведения по радиоизлучению — после пуска она захватывает излучение радаров, что делает ракету идеальной для атак ЗРК на средней дистанции.",
    "Air-launched low-observable jet attack drone; 68 kg shaped-charge/HE warhead. Selected surface target required.":
        "Авиабазированный малозаметный реактивный ударный БПЛА; 68-кг кумулятивно-фугасная боевая часть. Требуется выбранная наземная цель.",
    "Externally-mounted IR countermeasure dispenser for improving survivability":
        "Внешний блок ИК-ловушек для повышения выживаемости.",
    # ---- настройки слежения за головой ----
    "Eye VS Head Tracking Ratio (1,00)": "Отношение взгляда к повороту головы (1,00)",
    "Eye Tracking Responsiveness (1,00)": "Отклик отслеживания взгляда (1,00)",
    "Head Tracking Pitch & Yaw Sensitivity (1,00)": "Чувствительность тангажа и рыскания головы (1,00)",
    "Center Stabilization (1,00)": "Стабилизация центра (1,00)",
    "Head Tracking Roll Sensitivity (1,00)": "Чувствительность крена головы (1,00)",
    "Head Tracking Position Sensitivity (1,00)": "Чувствительность смещения головы (1,00)",
    # ---- HUD / мелочи ----
    "Radar Altitude": "Радиовысота",
    "CAPACITOR 90%": "КОНДЕНСАТОР 90%",
    "FLIGHT FUEL": "ТОПЛИВО ПОЛЁТА",
    "SQUADRON FUNDS": "СРЕДСТВА ЭСКАДРИЛЬИ",
    "Available for Mission": "Доступно для миссии",
    "Anti-Armor Missile": "Противобронная ракета",
    "Chase": "Преследование",
    "Free": "Свободная",
    "PREV": "ПРЕД.",
    "NEXT": "СЛЕД.",
    "NO": "НЕТ",
    "BUY": "КУПИТЬ",
    "Are you sure you want to leave ?": "Вы уверены, что хотите выйти?",
    # ---- Wing Command: общие ----
    "SQUADRON": "ЭСКАДРИЛЬЯ",
    "WING": "КРЫЛО",
    "SUPPLY": "СНАБЖЕНИЕ",
    "FLIGHT [+]": "ЗВЕНО [+]",
    "PAIR 1-2": "ПАРА 1-2",
    "PAIR 3-4": "ПАРА 3-4",
    "WHOLE WING": "ВСЁ КРЫЛО",
    "PLANE": "САМОЛЁТ",
    "CALLSIGN": "ПОЗЫВНОЙ",
    "STATE": "СОСТОЯНИЕ",
    "No wingmen. Requisition on SUPPLY, or assign friendly AI from the map.":
        "Ведомых нет. Запросите их через «СНАБЖЕНИЕ» или назначьте дружественный ИИ на карте.",
    # ---- Wing Command: группы ----
    "GROUPS - OPTIONAL / SELECTED AIRCRAFT": "ГРУППЫ — НЕОБЯЗАТЕЛЬНО / ВЫБРАННЫЕ САМОЛЁТЫ",
    "CREATE GROUP": "СОЗДАТЬ ГРУППУ",
    "EDIT GROUP": "ИЗМЕНИТЬ ГРУППУ",
    "DELETE GROUP": "УДАЛИТЬ ГРУППУ",
    "Select aircraft, then CREATE GROUP.": "Выберите самолёты, затем «СОЗДАТЬ ГРУППУ».",
    "GROUP NAME": "ИМЯ ГРУППЫ",
    "SAVE": "СОХРАНИТЬ",
    "SAVE uses the current command selection.": "«СОХРАНИТЬ» использует текущий набор приказов.",
    # ---- Wing Command: директивы ----
    "DIRECTIVES": "ДИРЕКТИВЫ",
    "GEOMETRY": "ГЕОМЕТРИЯ",
    "ROUTE / NODES": "МАРШРУТ / ТОЧКИ",
    "FIRE POLICY": "ПОЛИТИКА ОГНЯ",
    "HOLD": "УДЕРЖИВАТЬ",
    "TIGHT": "ПЛОТНО",
    "FREE": "СВОБОДНО",
    "WEAPON PREFERENCE": "ПРЕДПОЧТЕНИЕ ПО СРЕДСТВАМ",
    "SELECTED AIRCRAFT": "ВЫБРАННЫЕ САМОЛЁТЫ",
    "AUTO": "АВТО",
    "GUNS": "ПУШКИ",
    "ATTACK": "АТАКА",
    "ATTACK TARGET\n<size=85%>LOCK / MAP TARGET</size>":
        "АТАКОВАТЬ ЦЕЛЬ\n<size=85%>ЗАХВАТ / ЦЕЛЬ НА КАРТЕ</size>",
    "SPLASH\n<size=85%>LOCK / MAP TARGET</size>":
        "СБИТЬ\n<size=85%>ЗАХВАТ / ЦЕЛЬ НА КАРТЕ</size>",
    "ENGAGE\n<size=85%>HUNT / ROE FREE</size>":
        "В БОЙ\n<size=85%>ОХОТА / СВОБОДА ОГНЯ</size>",
    "SEEK / DESTROY\n<size=85%>MAP AREA</size>":
        "НАЙТИ И УНИЧТОЖИТЬ\n<size=85%>РАЙОН НА КАРТЕ</size>",
    "MANEUVER": "МАНЁВР",
    "FORM UP\n<size=85%>REJOIN</size>":
        "СТРОЙ\n<size=85%>СБОР</size>",
    "DISENGAGE\n<size=85%>BREAK CONTACT</size>":
        "ОТОРВАТЬСЯ\n<size=85%>ОБОРВАТЬ КОНТАКТ</size>",
    "HOLD HERE\n<size=85%>MAP POINT</size>":
        "ДЕРЖАТЬСЯ ЗДЕСЬ\n<size=85%>ТОЧКА НА КАРТЕ</size>",
    "JAM\n<size=85%>CURRENT TARGET</size>":
        "ГЛОШИТЬ\n<size=85%>ТЕКУЩАЯ ЦЕЛЬ</size>",
    "SUPPORT": "ПОДДЕРЖКА",
    "REFIT\n<size=85%>RESUPPLY / RESUME</size>":
        "ДООБОРУДОВАНИЕ\n<size=85%>ПОПОЛНИТЬ / ПРОДОЛЖИТЬ</size>",
    "STAND DOWN\n<size=85%>LOITER NEAR BASE</size>":
        "ОЖИДАНИЕ\n<size=85%>КРУЖЕНИЕ У БАЗЫ</size>",
    "CARGO\n<size=85%>MAP POINT</size>":
        "ГРУЗ\n<size=85%>ТОЧКА НА КАРТЕ</size>",
    "LAND\n<size=85%>MAP POINT</size>":
        "ПОСАДКА\n<size=85%>ТОЧКА НА КАРТЕ</size>",
    # ---- Wing Command: обстановка ----
    "COMBAT SITUATION & STORES": "БОЕВАЯ ОБСТАНОВКА И СРЕДСТВА",
    "NO TARGET DESIGNATED": "ЦЕЛЬ НЕ НАЗНАЧЕНА",
    "SCANNING SECTOR": "СКАНИРОВАНИЕ СЕКТОРА",
    "THREAT: CLEAR": "УГРОЗА: НЕТ",
    "STORES ABOARD": "СРЕДСТВА НА БОРТУ",
    "ALT: —": "ВЫС: —",
    "SPD: —": "СКР: —",
    "FORM: —": "СТРОЙ: —",
    "FUEL: —": "ТОП: —",
    "HULL: —": "КОРПУС: —",
    "SLOTS 1–4 · [ ] SELECTED\nDOT: LIVE · EDGE: OFF SCALE":
        "СЛОТЫ 1–4 · [ ] ВЫБРАН\nТОЧКА: В СЕТИ · КРАЙ: ВНЕ ШКАЛЫ",
    # ---- Wing Command: строй ----
    "FORMATION": "СТРОЙ",
    "Echelon R": "Клин справа",
    "Echelon L": "Клин слева",
    "Abreast": "В шеренгу",
    "Trail": "Вслед",
    "Spread": "Рассыпной",
    "Finger Four": "Пальцевое звено",
    "Vic": "Клиновидное",
    "Diamond": "Ромб",
    "Ladder": "Лестница",
    "Wall": "Стена",
    # ---- Wing Command: манёвры ----
    "MANEUVERS": "МАНЁВРЫ",
    "Barrel Roll\n<size=85%>MIN 500 m AGL</size>":
        "Бочка\n<size=85%>МИН 500 м над землёй</size>",
    "Aileron Roll\n<size=85%>MIN 350 m AGL</size>":
        "Ролл на элеронах\n<size=85%>МИН 350 м над землёй</size>",
    "Loop\n<size=85%>MIN 900 m AGL</size>":
        "Петля\n<size=85%>МИН 900 м над землёй</size>",
    "Wing Waggle\n<size=85%>MIN 60 m AGL</size>":
        "Покачивание крыльями\n<size=85%>МИН 60 м над землёй</size>",
    "Immelmann\n<size=85%>MIN 400 m AGL</size>":
        "Иммельман\n<size=85%>МИН 400 м над землёй</size>",
    "Split-S\n<size=85%>MIN 1400 m AGL</size>":
        "Сплит-С\n<size=85%>МИН 1400 м над землёй</size>",
    "Break Left\n<size=85%>MIN 120 m AGL</size>":
        "Резкий уход влево\n<size=85%>МИН 120 м над землёй</size>",
    "Break Right\n<size=85%>MIN 120 m AGL</size>":
        "Резкий уход вправо\n<size=85%>МИН 120 м над землёй</size>",
    "Notch Threat\n<size=85%>MIN 80 m AGL</size>":
        "Срез угрозы\n<size=85%>МИН 80 м над землёй</size>",
    "Terrain Mask\n<size=85%>MIN 40 m AGL</size>":
        "Укрытие за рельефом\n<size=85%>МИН 40 м над землёй</size>",
    "MIN = entry altitude above ground. Aircraft and speed limits still apply.":
        "МИН — высота входа над землёй. Ограничения по самолёту и скорости продолжают действовать.",
    # ---- Wing Command: маршрут ----
    "ROUTE / SELECTED AIRCRAFT": "МАРШРУТ / ВЫБРАННЫЙ САМОЛЁТ",
    "ALT +": "ВЫС +",
    "SPD +": "СКР +",
    "SPD -": "СКР −",
    "PATROL OFF": "ПАТРУЛЬ ВЫКЛ",
    "AUTO REFIT OFF": "АВТО-ДООБОРУД. ВЫКЛ",
    "Right-click: replace route. Shift-right-click: append a node.":
        "Правый клик: заменить маршрут. Shift + правый клик: добавить точку.",
    "QUEUED NODES / CURRENT LEG FIRST": "ОЧЕРЕДЬ ТОЧЕК / ТЕКУЩИЙ УЧАСТОК ПЕРВЫЙ",
    "SKIP CURRENT": "ПРОПУСТИТЬ ТЕКУЩУЮ",
    "CLEAR / FORM UP": "СБРОС / СТРОЙ",
    "NEXT PILOT": "СЛЕДУЮЩИЙ ПИЛОТ",
    # ---- Wing Command: запрос борта ----
    "AIRFRAME REQUISITION": "ЗАПРОС САМОЛЁТА",
    "FIT": "ПРИМЕНИТЬ",
    "LAUNCH FROM": "СТАРТ ИЗ",
    "ONLY NEAREST": "ТОЛЬКО БЛИЖАЙШАЯ",
    "ANY": "ЛЮБАЯ",
    "NEXT DISPATCH": "СЛЕДУЮЩИЙ ВЫЛЕТ",
    "ACTIVE AIRCRAFT ASSIGNMENT": "НАЗНАЧЕНИЕ АКТИВНЫХ САМОЛЁТОВ",
    "ASSIGN SELECTED": "НАЗНАЧИТЬ ВЫБРАННЫЕ",
    # ---- Wing Command: выкладка ----
    "AIRFRAME": "САМОЛЁТ",
    "TEMPLATE": "ШАБЛОН",
    "COPY": "КОПИРОВАТЬ",
    "DEL": "УДАЛИТЬ",
    "NAME": "ИМЯ",
    "LIVERY": "ОКРАСКА",
    "PYLONS": "ПИЛОНЫ",
    "PYLON": "ПИЛОН",
    "STORE": "СРЕДСТВО",
    "NO HARDPOINTS DETECTED ON AIRFRAME": "На самолёте не обнаружено узлов подвески",
    "LOADOUT PROFILE": "ПРОФИЛЬ ВЫКЛАДКИ",
    # ---- Wing Command: пилотская студия ----
    "PILOT STUDIO": "СТУДИЯ ПИЛОТА",
    "< SQUADRON": "< ЭСКАДРИЛЬЯ",
    "IMPORT ALL": "ИМПОРТИРОВАТЬ ВСЁ",
    "EXPORT ALL": "ЭКСПОРТИРОВАТЬ ВСЁ",
    "OPEN FOLDER": "ОТКРЫТЬ ПАПКУ",
    "RECRUIT ALL": "ЗАЧИСЛИТЬ ВСЕХ",
    "CALL": "ПОЗЫВНОЙ",
    "STATUS": "СТАТУС",
    "No custom pilots found in folder.": "В папке не найдено собственных пилотов.",
    "+ NEW": "+ НОВЫЙ",
    "CLONE": "КЛОНИРОВАТЬ",
    "DELETE": "УДАЛИТЬ",
    "RECRUIT": "ЗАЧИСЛИТЬ",
    "REROLL LOOKS": "ПЕРЕБРАТЬ ВНЕШНОСТЬ",
    "APPEARANCE": "ВНЕШНОСТЬ",
    "RND": "СЛУЧ",
    "STYLE": "СТИЛЬ",
    "BACKGROUND / LORE": "ПРОШЛОЕ / БИОГРАФИЯ",
    "Enter pilot background notes or military history...":
        "Введите заметки о прошлом пилота или его боевой биографии...",
    "GENERATE BIO": "СГЕНЕРИРОВАТЬ БИО",
    "RANDOMIZE ALL": "СЛУЧАЙНО ВСЁ",
    "SAVE PILOT": "СОХРАНИТЬ ПИЛОТА",
    "RECRUIT TO SQUADRON": "ЗАЧИСЛИТЬ В ЭСКАДРИЛЬЮ",
    "No pilots in the squadron yet.": "В эскадрилье пока нет пилотов.",
    "RECRUIT RANDOM": "ЗАЧИСЛИТЬ СЛУЧАЙНОГО",
    "CUSTOM PILOTS": "СОБСТВЕННЫЕ ПИЛОТЫ",
    "PILOT DOSSIER": "ДОСЬЕ ПИЛОТА",
    "PILOT SKILLS & PERKS": "НАВЫКИ И СПОСОБНОСТИ ПИЛОТА",
    "NO ABILITIES EARNED YET\nCombat sorties and promotions unlock tactical perks & survival skills.":
        "СПОСОБНОСТЕЙ ПОКА НЕТ\nБоевые вылеты и повышения в звании открывают тактические привилегии и навыки выживания.",
    "AIRFRAME ASSIGNMENT": "НАЗНАЧЕНИЕ САМОЛЁТА",
}

p = base + r"\ru.json"
raw = io.open(p, encoding="utf-8-sig").read()
ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
data = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)
before = len(data)

idx = raw.rfind("\n}")
head, tail = raw[:idx], raw[idx:]
if not head.rstrip().endswith(","):
    head = head.rstrip() + ","

new_entries = []
skipped = []
for k, v in NEW.items():
    if k in data:
        skipped.append(k[:60])
        continue
    new_entries.append("    " + json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False))
if new_entries:
    raw = head + "\n" + ",\n".join(new_entries) + tail

ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
data2 = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)
print(f"записей: {before} -> {len(data2)} (+{len(new_entries)})")
if skipped:
    print("уже были:", skipped)
io.open(p, "w", encoding="utf-8", newline="").write(raw)
print("СОХРАНЕНО, JSON валиден")
