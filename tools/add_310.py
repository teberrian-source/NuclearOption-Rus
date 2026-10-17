# -*- coding: utf-8 -*-
"""Добавляет новые переводы 3.1.0: описания из ассетов + UI-лейблы отсеков/пилонов/турелей."""
import json, re, io, sys

base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
sys.stdout.reconfigure(encoding="utf-8")

NEW = {
    # ---- описания из ассетов (16 реальных) ----
    "A concealed front line fighting position of an infantry team armed with light machine guns, grenades, and rocket launchers. Capable of ambushing unsuspecting vehicles that enter its field of fire.":
        "Скрытая передовая огневая точка пехотного отделения с лёгкими пулемётами, гранатами и ракётницами. Способна устраивать засады на технику, въезжающую в сектор обстрела.",
    "A controller that allows up to 6-degrees of freedom: Translate X, Y, Z and rotate X, Y, Z.":
        "Контроллер с поддержкой шести степеней свободы: перемещение по X, Y, Z и вращение вокруг X, Y, Z.",
    "A single 10-ton ammo container. When placed on the ground, allows weapon rearmament for units within 100m. Avoid subjecting the containers to large impact forces, as they may detonate.":
        "Одиночный контейнер с боеприпасами массой 10 тонн. При размещении на земле обеспечивает перевооружение техники в радиусе 100 м. Не подвергайте контейнер сильным ударам — он может взорваться.",
    "A single 10-ton container for replenishing a warship's ammunition stores. Has floatation devices and can be picked up by ships within 200m after being placed in the water. Avoid subjecting the containers to large impact forces, as they may detonate.":
        "Одиночный контейнер массой 10 тонн для пополнения боезапаса боевых кораблей. Имеет средства плавучести и может быть подобран кораблями в радиусе 200 м после сброса в воду. Не подвергайте контейнер сильным ударам — он может взорваться.",
    "A small pallet carrying 1.5 tons of munitions. When placed on the ground, allows rearmament of units within 100m. Volatile.":
        "Небольшая паллета с 1,5 тоннами боеприпасов. При размещении на земле обеспечивает перевооружение техники в радиусе 100 м. Взрывоопасна.",
    "A small, remote-controlled, air-transportable combat engineering unit designed for light role forces. Combat engineering units are able to facilitate the repair and reconstruction of destroyed hangars, helipads and vehicle depots.":
        "Небольшая дистанционно управляемая и транспортируемая по воздуху инженерная машина для лёгких подразделений. Инженерные машины помогают чинить и восстанавливать разрушенные ангары, вертолётные площадки и склады техники.",
    "A subsonic anti-ship missile with a very low altitude cruise profile and pop-up terminal attack mode designed to penetrate ship defenses. Can be deployed from aircraft or launched from an Argus Class Frigate.":
        "Дозвуковая противокорабельная ракета с полётом на предельно малой высоте и конечной атакой с подъёмом для преодоления ПВО корабля. Может запускаться с самолётов или фрегатов класса Argus.",
    "Featuring a unique 3-post ducted thrust system, this trainer doubles as an affordable attack aircraft with VTOL capability. The Vagrant is highly maneuverable and capable of transonic speeds, while also featuring a radar to allow engagement of air targets at beyond visual range. Although lacking advanced stealth features, the VT-7 continues to serve as the backbone of BDF naval aviation.":
        "Благодаря уникальной трёхопорной системе сдувной тяги этот учебный самолёт заодно служит доступным штурмовиком с возможностью вертикального взлёта и посадки. Vagrant очень маневренен и способен летать на дозвуковых скоростях, а установленный радар позволяет вести бой с воздушными целями на большой дальности. Хотя продвинутых средств снижения заметности у него нет, VT-7 по-прежнему остаётся основой морской авиации BDF.",
    "Ideal for attacking SAM sites at beyond visual range, this anti-radiation missile is capable of high range and speed and specifically targets radar emission sources. If not provided a target, it will identify its own from incoming radar signals.":
        "Идеален для атак на позиции ЗРК с большой дальности: эта противорадиолокационная ракета обладает большой дальностью и скоростью и выбирает цели по источникам радиоизлучения. Если цель не задана, она определяет её самостоятельно по входящим сигналам радара.",
    "Long range artillery rocket with inertial navigation and terminal laser guidance to improve accuracy. A thermobaric warhead provides enhanced blast effects, ideal for demolishing buildings and defensive structures.":
        "Дальняя артиллерийская ракета с инерциальной навигацией и лазерным наведением на конечном участке для повышения точности. Термобарическая боевая часть усиливает взрывное действие — идеальна для сноса зданий и оборонительных сооружений.",
    "Point-defence laser designed to intercept approaching missiles from within 2km.":
        "Лазер ПВО ближнего действия для перехвата приближающихся ракет с дистанции до 2 км.",
    "Point-defence laser designed to intercept approaching missiles from within 8km.":
        "Лазер ПВО ближнего действия для перехвата приближающихся ракет с дистанции до 8 км.",
    "The Surf Class is an inshore patrol vessel, nominally used for border protection and anti-piracy duties. While it lacks the staying power of larger ships, its speed and complement of vertically launched AGM-48s can make it a credible threat to them. The 30mm main gun has proximity fused shells and provides some amount of self-protection against missile attack.":
        "Катер класса Surf — прибрежный патрульный корабль, предназначенный в основном для охраны границ и борьбы с пиратством. Уступая крупным кораблям в живучести, он благодаря скорости и вертикально запускаемым AGM-48 может представлять для них реальную угрозу. 30-мм орудие со снарядами дистанционного подрыва даёт некоторую защиту от ракетных атак.",
    "This 400kg cluster bomb dispenses 8 GS25 submunitions capable of independently finding and targeting hostile units in the vicinity.":
        "Кассетная бомба массой 400 кг, сбрасывающая 8 суббоеприпасов GS25, способных самостоятельно обнаруживать и поражать цели поблизости.",
    "This anti-ship cruise missile can be launched from aircraft or vertically by the Dynamo class Destroyer. It uses a low altitude sea-skimming flight profile and supersonic speeds to penetrate enemy air defense systems.":
        "Эта противокорабельная крылатая ракета может запускаться с самолётов или вертикально с эсминца класса Dynamo. Она летит на малой высоте над водой и на сверхзвуковой скорости, преодолевая ПВО противника.",
    "This heavy machine gun mounted on a tripod is low-cost means of defending point targets from light vehicles and low flying helicopters. Its small size and low profile make it difficult to spot from a distance.":
        "Этот крупнокалиберный пулемёт на треноге — недорогое средство защиты точечных целей от лёгкой техники и низко летящих вертолётов. Небольшие размеры и низкий силуэт затрудняют его обнаружение издалека.",
    # ---- описания со скриншотов (моды/новое оружие) ----
    "The Hexhound is a remote controlled drone with various weapon options.":
        "Hexhound — дистанционно управляемый беспилотник с различными вариантами вооружения.",
    "A smaller offensive jammer designed to provide a broader range of aircraft with EWAR capability. Maximum range of 30km, can only jam radar bands used by ships and ground vehicles.":
        "Компактная наступательная станция РЭБ, обеспечивающая более широкий круг самолётов возможностями радиоэлектронной борьбы. Максимальная дальность — 30 км, глушит только диапазоны радаров, применяемые кораблями и наземной техникой.",
    "Advanced short-range air to air missile featuring extreme manoeuverability and high TWR, perfect for close-in knife fights.":
        "Продвинутая малорадиусная ракета «воздух-воздух» с исключительной маневренностью и высокой тяговооружённостью — идеальна для ближнего манёвренного боя.",
    "The AGM-27 Pyre is a compact air-to-ground missile designed to provide high-end supersonic aircraft with short-range anti-armour capability. It is comparable to the AGM-48 in stature and capability, however is much better suited for high speed aircraft and can be carried internally.":
        "AGM-27 Pyre — компактная ракета «воздух-земля», предназначенная для обеспечения современных сверхзвуковых самолётов средствами поражения бронетехники на малой дальности. По размерам и характеристикам она сопоставима с AGM-48, однако лучше подходит для высокоскоростных самолётов и может нестись во внутренних отсеках.",
    # ---- UI-лейблы отсеков / пилонов / турелей ----
    "Internal Cannon": "Внутренняя пушка",
    "Left Internal Cannons": "Левые внутренние пушки",
    "Right Internal Cannon": "Правая внутренняя пушка",
    "Left Bay": "Левый отсек",
    "Right Bay": "Правый отсек",
    "Left Internal Bay": "Левый внутренний отсек",
    "Right Internal Bay": "Правый внутренний отсек",
    "Cargo Bay Front": "Передний грузовой отсек",
    "Cargo Bay Rear": "Задний грузовой отсек",
    "Rear Mount": "Заднее крепление",
    "Main Turret": "Основная турель",
    "Front Turret": "Передняя турель",
    "Rear Turret": "Задняя турель",
    "Rear Turrets": "Задние турели",
    "Turret Left": "Турель слева",
    "Turret Right": "Турель справа",
    "4xS1 Turret": "Турель 4xS1",
    "30mm Autocannon Turret under pilot control": "30-мм автоматическая турель под управлением пилота",
    "Left Pylon": "Левый пилон",
    "Right Pylon": "Правый пилон",
    "Inner Left Pylon": "Внутренний левый пилон",
    "Inner Right Pylon": "Внутренний правый пилон",
    "Outer Left Pylon": "Внешний левый пилон",
    "Outer Right Pylon": "Внешний правый пилон",
    "Inner Pylons": "Внутренние пилоны",
    "Outer Pylons": "Внешние пилоны",
    "Wing Glove Pylons": "Пилоны на законцовках крыла",
    "Toggle Left Panel": "Переключить левую панель",
    # ---- кнопки / подсказки магазина ----
    "Purchase for": "Купить за",
    "Next aircraft:": "Следующий самолёт:",
    "Rank:": "Ранг:",
    "Owned:": "Куплено:",
    "Faction:": "Фракция:",
    "Not available here": "Недоступно здесь",
    "YES": "ДА",
    "YES [F9]": "ДА [F9]",
    "NO [F10]": "НЕТ [F10]",
    "NO LOCK": "НЕТ ЗАХВАТА",
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
for k, v in NEW.items():
    if k in data:
        continue
    new_entries.append("    " + json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False))
if new_entries:
    raw = head + "\n" + ",\n".join(new_entries) + tail

ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
data2 = json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)
print(f"записей: {before} -> {len(data2)} (+{len(new_entries)})")
io.open(p, "w", encoding="utf-8", newline="").write(raw)
print("СОХРАНЕНО, JSON валиден")
