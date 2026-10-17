# Nuclear Option — русификатор: состояние проекта

Дата слепка: **17.10.2026**. Папка проекта (постоянная, вне TEMP):
`C:\Users\user\Documents\NuclearOption_Rus\`

Этот файл — точка восстановления: что сделано, где лежит, как пересобрать и
что осталось. Если что-то потеряется — по нему проект поднимается заново.

---

## 1. Что это

Плагин `LocalizationPatch` (BepInEx 5.x) для игры **Nuclear Option 0.34.2**.
Переводит интерфейс, подсказки, брифинги, описания техники/оружия, тексты миссий.
Названия оружия, техники, миссий, ливрей и локаций остаются английскими.

| Параметр | Значение |
|---|---|
| Версия плагина | **3.2.4** |
| Записей в словаре `ru.json` | **4256** |
| Размер `ru.json` | 680 797 байт |
| SHA-256 (первые 16) | `6D3E6F67370B8E2B` |
| Язык | `ru` (автоопределение по файлу `ru.json`) |

## 2. Где что лежит

**Игра (рабочая копия — только эта!):** `C:\Users\user\Desktop\NuclearOption_0.34.2\`

| Файл | Назначение |
|---|---|
| `BepInEx\plugins\LocalizationPatch\LocalizationPatch.dll` | сам плагин (61 440 Б) |
| `BepInEx\plugins\LocalizationPatch\ru.json` | словарь перевода (4256 записей) |
| `BepInEx\plugins\LocalizationPatch\LocalizationPatchDropdown.dll` | аддон выпадающих списков (штатный, не трогать) |
| `BepInEx\plugins\LocalizationPatch\WDXLLubrifontSC-Regular.ttf` | шрифт с кириллицей (штатный, не трогать) |
| `BepInEx\plugins\LocalizationPatch\README.md` | документация плагина (для пользователей) |
| `BepInEx\LogOutput.log` | лог игры: строки `[TRACE] miss:`/`hit:` плагина, `[HB]` — пульс раз в 10 с |

**Репозиторий проекта** (git, публикуется на GitHub как `NuclearOption-Rus`):
`C:\Users\user\Documents\NuclearOption_Rus\`

| Папка/файл | Назначение |
|---|---|
| `dict\ru.json` | словарь перевода (4256 записей) |
| `plugin\KoreanPatch\Plugin.cs` | исходник плагина (BOM + CRLF, ~2636 строк) |
| `plugin\KoreanPatch\*.cs` | остальные исходники (патчи Harmony и пр.) |
| `plugin\LocalizationPatch.csproj` | сборка net472 (ссылки на BepInEx из папки игры) |
| `plugin\Properties\AssemblyInfo.cs` | атрибуты сборки |
| `plugin\build\LocalizationPatch.dll` | собранный плагин v3.2.4 |
| `plugin\regex_test\` | мини-проект: проверка шаблонов/регулярок |
| `tools\*.py` | скрипты раундов: сбор строк, слияние в `ru.json`, правки `Plugin.cs` |
| `tools\restructure_repo.py` | раскладка репозитория по папкам + чистка мусора |
| `data\` | рабочие выгрузки (`untranslated.txt`, `extracted_*`) и пакеты перевода (`tr*.json`, `todo*.json`, `r15*`) |
| `README.md` | описание проекта (для GitHub) |
| `PROJECT_STATE.md` | этот файл |

Рабочая копия тех же файлов лежит в `%TEMP%\lp_build\` — её может стереть система,
поэтому постоянная копия здесь.

**Три копии словаря** (синхронизировать после каждой правки!):
1. `<игра>\BepInEx\plugins\LocalizationPatch\ru.json` — рабочий
2. `<игра>\BepInEx\config\LocalizationPatch\ru.json` — бэкап
3. `C:\Users\user\Documents\NuclearOption_Rus\ru.json` — бэкап

Бэкапы `ru.backup_*.json` лежат в папке плагина; бэкапы DLL — `LocalizationPatch.dll.bak_*`.

## 3. Сборка и установка плагина

```powershell
cd C:\Users\user\Documents\NuclearOption_Rus\plugin
dotnet build LocalizationPatch.csproj -c Release
```
Затем (игра должна быть **закрыта**):
```powershell
$dst = 'C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch'
Copy-Item "$dst\LocalizationPatch.dll" "$dst\LocalizationPatch.dll.bak_$(Get-Date -Format HHmmss)" -Force
Copy-Item 'C:\Users\user\Documents\NuclearOption_Rus\plugin\bin\Release\LocalizationPatch.dll' "$dst\LocalizationPatch.dll" -Force
(Get-FileHash "$dst\LocalizationPatch.dll").Hash   # сверить с bin\Release
```
Важно: если сборка ругается на «Повторяющийся атрибут … regex_test\obj\…» — в csproj уже
стоит исключение `<Compile Remove="regex_test/**" />`; повторять не нужно.

Исходник править только через инструменты write/edit (PowerShell портит кодировку).
Файл — UTF-8 **с BOM** и **CRLF**; при правках скриптом нормализовать `\r\n`→`\n`,
писать обратно с `\r\n` и BOM. Проверка после правки: `3.2.4` в 3 местах, `CtrlHeld` есть,
белый список `LabelWithValueKeys` цел, кириллица на месте, «мохибейки» нет.

## 4. Горячие клавиши плагина

| Клавиши | Действие |
|---|---|
| `Ctrl+F5` | перезагрузить `ru.json` без перезапуска игры (старое `Ctrl+F10` тоже работает) |
| `Ctrl+F4` | выгрузить `extracted_gamedata.txt` (старое `Ctrl+F11`) |
| `Ctrl+F6` | выгрузить `extracted_strings.txt` (старое `Ctrl+F12`) |
| `F9`/`F10` | окно плагина со статистикой |

## 5. Правила перевода (согласованы с пользователем)

- Переводим: интерфейс, подсказки, брифинги, описания техники/оружия, тексты и названия задач.
- **Не переводим**: названия оружия, техники, миссий, ливрей, локаций (внутри фраз — тоже,
  например `Оборонять Maris Airport`).
- Не трогаем: деньги, дистанции, единицы, таймеры, координаты сетки (`$60,0k`, `R: 20km`,
  `HDG 184°`, `RNG`, `ALT`, `V`).
- Мусор/заглушки не переводим: `ConfigDescription.*`, база джойстиков Rewired, Lorem ipsum,
  Navy Seals copypasta, placeholder-строки.

## 6. Как добавлять новые строки

1. Взять непереведённые строки: `untranslated.txt` в папке плагина (пишется раз в 60 с),
   выгрузки `extracted_*.txt`, либо напрямую из ресурсов игры
   (`NuclearOption_Data\resources.assets`, `level0…level5`: поля JSON `Message`, `message`,
   `description`, `body`, `title`, `objectives[].DisplayName`) и из миссий
   (`%APPDATA%\..\LocalLow\Shockfront\NuclearOption\Missions\*.json`).
2. Отфильтровать мусор и служебные идентификаторы (`IsJunkForTranslation` в плагине,
   скрипты `prep*.py`).
3. Перевести (пакетами, при необходимости — субагентами), сложить в `tr*.json`.
4. Влить в `ru.json` скриптом по образцу `merge15b.py`: **не перезаписывать файл целиком**
   (`dict` → json давал дубли ключей!). Правильно: взять сырой текст, обрезать по последнему
   `\n}`, добавить запятую, дописать новые строки, проверить `json.loads(..., strict=False)`
   и количество, только потом записывать. Бэкап делать всегда.
5. Синхронизировать 3 копии словаря и сверить хэши.
6. Если строка — подпись задачи с числом/дистанцией, добавить её в белый список
   `LabelWithValueKeys` (`Plugin.cs`) и пересобрать DLL.
7. Обновить `README.md` и этот файл (журнал раунда).

Особенности чтения `ru.json` из Python: `json.loads(..., strict=False)` (в ключах есть сырые
control-символы), предварительно убрать строки-комментарии `//` и висячие запятые.

Чтение вывода PowerShell: `>` пишет UTF-16, консоль — cp1251. Поэтому результаты скриптов
складывать в файл и декодировать: `io.open(f,'rb').read().decode('utf-16')`.

## 7. История раундов (кратко)

| Раунд | Что сделано | Записей |
|---|---|---|
| 11 | trim-версии ключей (плагин сравнивает текст после `Trim()`) | +149 |
| 12 | брифинги/туториал, описания миссий, статусы HUD `<b>`, предупреждения | +67 |
| 13 | подписи задач для шаблона «подпись + число/единица» + шаблоны в плагине | +14 |
| 14 | полный разбор `resources.assets`/`level0…5`: все брифинги в чате, описания миссий, подсказки | +225 → 3978 |
| 14b | возврат 7 названий на английский (`Radome`, `Ammo box`, `Cursor Class LFD`, `Argus Class Frigate`, `4xS1 Turret`, `MSV LADS`, `MSV MRAP`) | −7 |
| 15 | 15 миссий Ironjaw Sound (описания, `outcomes[].Message`, имена целей) + описания FS-41/KAR/Carrier Duel Lite + имена целей/точек базовых миссий | +278 → **4256** |

Раунд 15 закрыл жалобу: `Ingress Via Mountains` → **«Вход в район через горы»**
(было единственной непереведённой точкой маршрута; лежит в `objectives[].DisplayName`
в `resources.assets`, offset ≈ 116 835 288).

В версии 3.2.4 в `Plugin.cs` дополнительно: хоткей `Ctrl+F5` (перезагрузка словаря),
метод `CtrlHeld()`, окно переключается только без Ctrl, белый список подписей расширен
с 14 до **151** записи (имена задач и точек маршрута, чтобы работал шаблон
«подпись + дистанция», например `Вход в район через горы 1,2km`).

## 8. Отложенные задачи

### 8.1. Зависания при запуске игры (~2 раза по 10 с) — ЖДЁТ КОМАНДЫ «убери зависания»
Диагноз (проверен по логу сессии 17.10 21:32):
- Причина — **авто-выгрузки плагина**: `Plugin.cs`, условие `autoDumpCount < 3 && Time.time >= nextAutoDumpTime`
  (`nextAutoDumpTime = 25f`, далее +60 и +120 с) вызывает `ExtractGameData()` + `ExtractAllStrings()`.
- `ExtractAllStrings()` → `CollectFromObject()` рекурсивно читает **рефлексией все поля** у всех
  `ScriptableObject` и `MonoBehaviour` (глубина 3, списки до 5000 элементов). При 33 модах это
  десятки тысяч объектов — синхронная работа в главном потоке.
- Доказательство: `extracted_gamedata.txt` записан 21:32:41, `extracted_strings.txt` — 21:32:58,
  т.е. один проход ≈ 17 с непрерывной работы; в логе ровно 3 пары `Extracted 101 hint lines` +
  `ExtractAllStrings: N text`.
- Побочно: `[TRACE] miss:` пишет 1500+ строк на диск в главном потоке (мелкие подёргивания).

Готовые варианты фикса (выбрать и применить, нужна пересборка DLL):
1. Отключить авто-выгрузки, оставить только `Ctrl+F4` / `Ctrl+F6` (минимальная правка, рекомендуется).
2. То же + флаг `AutoDump` в BepInEx-конфиге плагина (по умолчанию `false`).
3. Дополнительно разбить сбор строк по кадрам (корутина), чтобы и ручные выгрузки не фризили.
4. Отдельно: приглушить `[TRACE]` логи (`untranslated.txt` при этом остаётся работать).

Решение пользователя (17.10.2026): **пока русификатор не доделан — оставить как есть**,
фикс применить позже по команде.

### 8.2. Прочее
- `untranslated.txt` местами «поехал»: внутри ключей встречаются переводы строк.
- Авто-выгрузка `untranslated.txt` раз в 60 с идёт всегда — она дешёвая, её трогать не нужно.
- Остались непереведёнными служебные/мемные строки и часть модовых описаний — при
  необходимости собрать новый `untranslated.txt` (запустить игру, подождать, `Ctrl+F4`/`Ctrl+F6`).

## 9. Как восстановить проект «с нуля»

1. Скопировать постоянную копию инструментов (см. §2) на место.
2. Взять `ru.json` из `C:\Users\user\Documents\NuclearOption_Rus\ru.json` и положить в
   `<игра>\BepInEx\plugins\LocalizationPatch\` (+ копию в `BepInEx\config\LocalizationPatch\`).
3. Собрать плагин (§3) или взять готовый `plugin\build\LocalizationPatch.dll`.
4. Приложить штатные `LocalizationPatchDropdown.dll` и `WDXLLubrifontSC-Regular.ttf`
   (если папка плагина пуста — их можно взять со страницы релизов плагина).
5. Проверить в логе после запуска: `Loaded 4256 translations from ru.json`,
   `Localization Patch v3.2.4 loaded`.

Ссылки проекта: https://github.com/9138noms/NuclearOption-LocalizationInstaller
