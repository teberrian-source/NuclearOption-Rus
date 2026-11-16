# -*- coding: utf-8 -*-
"""Дописывает раздел 11 (диагностика подфризов) в PROJECT_STATE.md."""
import io, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(REPO, "PROJECT_STATE.md")

TEXT = """
## 11. Диагностика подфризов (17.11.2026) — ЗАКРЫТО

Симптом: ритмичные подфризы каждые 2-3 с в игре 0.34.6 при большом числе модов.

Механизм (подтверждён кастомным плагином HeapWatch, `plugin\\HeapWatch\\`,
установлен в игру как `BepInEx\\plugins\\HeapWatch`): GC Mono собирает накопленный
мусор большой сборкой раз в ~40 с; длительность паузы растёт с размером кучи.
Мусор создают сами моды (+0.5-1.3 МБ/2с на пиле), а объём кучи — тяжёлые
самолёт-моды (F-117A 441 МБ, centurion 46 МБ и т.д.). Чистая ваниль тоже даёт
пики до ~7 мс, но они незаметны; с модами 1% low CPU доходил до 20+ мс.

Решение пользователя: отключены (в `disabledPlugins`) Apex-6, baanish.centurion,
blacknight2u.f117a.nighthawk, aryx.mig15, aryx.f22e, 1509_PalaFighter1; удалена
карта Cascadia (1.6 ГБ) и миссия «Cascadia Falling» (бэкап:
`backups\\missions_cascadia`). Подфризы пропали (fps 1% low 70 при AVG 171).

Важные факты:
- Русификатор НЕ виноват (проверено отключением — фриз оставался).
- Системные причины (Game Input / Synthetic Gamepad код 22, Kaspersky)
  исключены: на чистой ванили фризов нет.
- **NOMapLoader 1.0.6 оставлен в plugins**: нужен для загрузки 14 бандлов
  Blueprinter и карты IronjawSound (TerrainLab 1.1.3).
- Конфликт: swissalps грузят оба загрузчика, NOMapLoader валится на
  cm.swissalps.3363c1ec (карту держит NOCustomMaps) — одна ошибка на старте.
- ThirdFaction 1.6.3: DLL == последний релиз GitHub; тег OUTDATED в NOMM —
  только метаданные (gameVersion 0.33 не обновлён автором).
"""

with io.open(P, "a", encoding="utf-8") as f:
    f.write(TEXT)
print("раздел 11 дописан")
