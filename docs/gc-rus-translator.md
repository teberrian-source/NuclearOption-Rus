# Русификатор Ground Control (RTS) — стороннее решение

## Что установлено
- **Rusifikator-NuclearOption-GroundControl 1.0.1** (автор Tatarok / Ilyasik2001, лицензия MIT).
- Источник: https://github.com/Ilyasik2001/Russian-Nuclear-Option-Ground-Control-RTS. (точка в конце имени!)
- Релиз: v1.0.1, zip сохранён в `vendor/gc-rus/`.
- Установлен в `BepInEx/plugins/Rusifikator-NuclearOption-GroundControl 1.0.1/`.

## Почему чужой плагин, а не словарь в ru.json
Ground Control рисует интерфейс через **IMGUI** (GUIContent/GUI.Label), а строковые
литералы зашиты прямо в DLL мода. Наш LocalizationPatch переводит через TMP/UGUI
хуки и эти строки не видит. У стороннего плагина два нужных механизма:
- `LiteralPatcher` — подмена литералов в IL сборки GroundControlRts (до её запуска);
- `ImguiPatches` — перевод в момент отрисовки IMGUI (+ FitText — уменьшение шрифта).

## Конфигурация (`BepInEx/config/com.gcru.russian.cfg`)
- `TranslateGame = false` — базовую игру переводит наш LocalizationPatch (иначе
  конфликт двух переводчиков одних и тех же строк);
- `TranslateGroundControl/TranslateImgui/FitText = true`;
- `GameFont =` пусто — их TMP-шрифт не подключаем (у нас свой WDXLL);
- IMGUI-шрифты: Barlow → Arial Narrow (система).

## Правила именования (политика проекта)
Из `translations/` установленный копии УДАЛЕНЫ (имена не переводим):
- `names_units.json`, `names_world.json`, `names_keys.json`, `names_presets.json`,
  `names_tutorial.json` — названия техники/локаций;
- `game_missions.json` — названия миссий.
Оставлены: все `gc_*`, `display_*`, `game_hints`, `game_misc`, `game_ui`,
`game_tutorial*`, `game_patterns`, `base_game.json` (используется IMGUI-экраном
для имён из игры), `shared_units.json` (описания техники — их переводим).

## Конфликт/кооперация с LocalizationPatch
- Их плагин при обнаружении `com.noms.localizationpatch` пишет warning — это
  ожидаемо и безопасно при `TranslateGame=false`.
- Оба плагина патчат `FontEngine.LoadFontFace(Font,…)`, но каждый подменяет
  только СВОЙ proxy-шрифт — не мешают друг другу.

## Обновление
Новые версии брать с релизов репозитория, повторить удаление имён-файлов и
конфиг. Их fork-патч рассчитан на GC 1.0.0.0; при обновлении GroundControlRts
сверять переводы (могут появиться новые литералы → untranslated.txt).
