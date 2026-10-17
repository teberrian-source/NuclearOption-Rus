# -*- coding: utf-8 -*-
"""Раунд 12: брифинги/туториал, описания миссий, статусы HUD, дорожная карта.
Каждый ключ сверяется с дампом untranslated.txt (защита от опечаток)."""
import io, re, sys, json, shutil, datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
p = base + r"\ru.json"

PAIRS = [
    # --- брифинг/туториал (построчно) ---
    ("The BDF is on the run, and trying to evacuate as much fuel from the area as they can.",
     "BDF отступает и пытается вывезти из района как можно больше топлива."),
    ("A large convoy of fuel trucks was last spotted about 5km north of Dustbowl. We're headed to the convoy's last known position.",
     "Большой конвой топливозаправщиков в последний раз видели примерно в 5km к северу от Dustbowl. Мы идём к последнему известному положению конвоя."),
    ("Your aircraft's visual sensors can detect ground vehicles within a range of 6km. We are to locate and destroy the convoy.",
     "Бортовые оптические датчики самолёта обнаруживают наземную технику в радиусе 6km. Наша задача — найти и уничтожить конвой."),
    ("Convoy has been spotted. Lets get to work.",
     "Конвой обнаружен. Приступаем к работе."),
    ("Headed to the target now.",
     "Направляюсь к цели."),
    ("Form up on me and I'll lead us to the target.",
     "Стройтесь за мной, я выведу нас на цель."),
    ("The vehicles should be targetable now. Select them as targets.",
     "Теперь технику можно взять в качестве цели. Выберите их целями."),
    ("Drop the bombs when the countdown reaches zero and the arrows on your HUD converge.",
     "Сбрасывайте бомбы, когда отсчёт дойдёт до нуля и стрелки на ИЛС сойдутся."),
    ("Good hits. We'll finish off any remaining vehicles with our guns. Remember to pull up. Don't get so fixated on shooting that you forget the terrain exists.",
     "Хорошие попадания. Оставшуюся технику добьём из пушек. Не забывайте уходить вверх. Не увлекайтесь стрельбой так, чтобы забыть о рельефе."),
    ("... and remember, they can still shoot back. Don't make it easy for them.",
     "... и помните, они ещё могут отстреливаться. Не давайте им лёгкой цели."),
    ("Good shooting. That's the last of them. We should clear out before any response comes our way.",
     "Отличная стрельба. Это был последний. Уходим, пока не пришёл ответный удар."),
    ("Excellent work, every convoy vehicle has been destroyed.",
     "Отличная работа, вся техника конвоя уничтожена."),
    ("Enemy planes are after us! Stay near our base, our anti-air will protect us!",
     "Нас преследуют вражеские самолёты! Держитесь у нашей базы, ПВО нас прикроет!"),
    # --- описания миссий ---
    ("Back to basics with bombs & guns on a CI-22 Cricket in a low-intensity engagement.",
     "Возвращение к основам: бомбы и пушки на CI-22 Cricket в бою низкой интенсивности."),
    ("Fly a T/A-30 Compass on a ground attack mission. Use missiles, rockets, bombs and guns to destroy a BDF convoy of lightly defended vehicles.",
     "Полетайте на T/A-30 Compass в миссии по удару по земле. Ракетами, НАР, бомбами и пушками уничтожьте конвой BDF из слабо защищённой техники."),
    ("Escalation co-op as BDF", "Эскалация, кооператив за BDF"),
    # --- UI ---
    ("End Game for Everyone", "Завершить игру для всех"),
    ("No reserve CI-22 Crickets currently available. You are first in queue for this airframe",
     "Резервных CI-22 Cricket сейчас нет. Вы первый в очереди на этот борт"),
    ("Cleared for landing on Runway 16", "Разрешение на посадку, ВПП 16"),
    ("Cleared to taxi to Runway 34", "Разрешение на руление, ВПП 34"),
    # --- статусы с <b> ---
    ("Stability Assist <b>Enabled</b>", "Стабилизация <b>включена</b>"),
    ("Weapon safety lock <b>Enabled</b>", "Блокировка оружия <b>включена</b>"),
    ("Weapon safety lock <b>Disabled</b>", "Блокировка оружия <b>выключена</b>"),
    ("Nav Lights <b>On</b>", "АНО <b>вкл</b>"),
    ("Nav Lights <b>Off</b>", "АНО <b>выкл</b>"),
    # --- предупреждения HUD ---
    ("STALL WARNING", "СВАЛИВАНИЕ"),
    ("INOPERABLE", "НЕРАБОТОСПОСОБНО"),
    ("NO SIGNAL", "НЕТ СИГНАЛА"),
    ("LOWER GEAR", "ВЫПУСТИТЬ ШАССИ"),
    ("L ENG FIRE", "ПОЖАР ЛЕВ. ДВ."),
    ("R ENG FIRE", "ПОЖАР ПРАВ. ДВ."),
    ("MISSILE CAMERA", "КАМЕРА РАКЕТЫ"),
    ("FAULT", "ОТКАЗ"),
    # --- дорожная карта ---
    ("• Additional Boats / Ships", "• Дополнительные лодки / корабли"),
    ("• PALA Landing ship", "• Десантный корабль PALA"),
    ("• Additional high-end SAMs", "• Дополнительные ЗРК высокого класса"),
    ("• Additional ground units", "• Дополнительные наземные юниты"),
    ("• More infantry mechanics", "• Больше механик пехоты"),
    ("• Missile mechanic changes", "• Изменения механики ракет"),
    ("• Further development on Ignus Archipelago", "• Дальнейшая разработка Ignus Archipelago"),
    ("• More destructible/interactible environment", "• Больше разрушаемого/интерактивного окружения"),
    ("• AI improvements for aircraft, ships, and ground units", "• Улучшение ИИ самолётов, кораблей и наземной техники"),
    ("• Additional control customization", "• Дополнительная настройка управления"),
    ("• Menu UI improvements", "• Улучшения интерфейса меню"),
    ("• Additional low-rank aircraft", "• Дополнительные самолёты низкого ранга"),
    ("• Existing aircraft remasters", "• Ремастеры существующих самолётов"),
    ("• Light utility VTOL", "• Лёгкий вспомогательный VTOL"),
    ("• Aerial drones", "• Воздушные дроны"),
    ("• Additional helicopters", "• Дополнительные вертолёты"),
    ("• Additional nuclear weapon types", "• Дополнительные типы ядерного оружия"),
    ("• Additional conventional weapon types", "• Дополнительные типы обычного вооружения"),
    ("• Terrain and runway cratering", "• Воронки на рельефе и ВПП"),
    ("• Campaign system", "• Система кампании"),
    ("• VR implementation", "• Поддержка VR"),
    ("• Console version", "• Консольная версия"),
    ("• Localization", "• Локализация"),
    ("• New large landlocked map", "• Новая большая континентальная карта"),
    ("• Heavy cargo plane", "• Тяжёлый грузовой самолёт"),
    ("• Continued development and detailing of existing maps", "• Продолжение разработки и детализация существующих карт"),
    ("• More props and buildings", "• Больше объектов и строений"),
    ("• Logistics and economy changes", "• Изменения логистики и экономики"),
    ("• Graphics improvements", "• Улучшения графики"),
    ("• Sound improvements", "• Улучшения звука"),
    ("• Expanded modding support", "• Расширенная поддержка модов"),
    ("• More destructible/interactible environment and props", "• Больше разрушаемого/интерактивного окружения и объектов"),
    ("• Expanded Mission Editor functionality", "• Расширенная функциональность редактора миссий"),
    ("• Dynamic music", "• Динамическая музыка"),
]

def parse_json(path):
    raw = io.open(path, encoding="utf-8-sig").read()
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(l for l in raw.split("\n") if not l.strip().startswith("//"))), strict=False)

ru = parse_json(p)
before = len(ru)

# текст дампа, приведённый к «нормальному» виду (экранированные \n -> перевод строки)
dump = io.open(base + r"\untranslated.txt", encoding="utf-8", errors="replace").read()
norm = dump.replace("\\n", "\n").replace("\\'", "'").replace('\\"', '"').replace("\\\\", "\\")
print("размер дампа:", len(dump))

add, already, notfound = {}, [], []
for k, v in PAIRS:
    if k in ru:
        already.append(k)
    elif k not in norm:
        notfound.append(k)
    else:
        add[k] = v

print("новых:", len(add), "| уже были:", len(already), "| НЕ найдено в дампе:", len(notfound))
for k in notfound:
    print("   ОПЕЧАТКА?:", repr(k[:100]))
for k in already:
    print("   уже было:", repr(k[:80]))

if add:
    backup = base + r"\ru.backup_" + datetime.datetime.now().strftime("%H%M%S") + ".json"
    shutil.copy2(p, backup)
    raw = io.open(p, encoding="utf-8-sig").read()
    idx = raw.rfind("\n}")
    head, tail = raw[:idx], raw[idx:]
    if not head.rstrip().endswith(","):
        head = head.rstrip() + ","
    lines = ["    " + json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False) for k, v in add.items()]
    io.open(p, "w", encoding="utf-8", newline="").write(head + "\n" + ",\n".join(lines) + tail)
    ru2 = parse_json(p)
    print(f"записей: {before} -> {len(ru2)}")
    for k, v in add.items():
        assert ru2[k] == v, k
    shutil.copy2(p, r"C:\Users\user\Documents\NuclearOption_Rus\ru.json")
    shutil.copy2(p, r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\config\LocalizationPatch\ru.json")
    print("копии обновлены; бэкап:", backup)
