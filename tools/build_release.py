# -*- coding: utf-8 -*-
"""Сборка пакета русификатора для передачи: dist/NuclearOption-Rus-<версия>/ + zip."""
import hashlib, io, os, shutil, sys, zipfile

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VER = "3.3.1"
REPO = r"C:\Users\user\Documents\NuclearOption_Rus"
GAME = r"C:\Users\user\Desktop\NuclearOption_0.34.2"
PLUG = os.path.join(GAME, r"BepInEx\plugins\LocalizationPatch")
DIST = os.path.join(REPO, "dist")
PKG = os.path.join(DIST, "NuclearOption-Rus-v" + VER)

# ---------- 1. файлы -------------
files = {
    r"BepInEx\plugins\LocalizationPatch\ru.json": os.path.join(REPO, r"dict\ru.json"),
    r"BepInEx\plugins\LocalizationPatch\LocalizationPatch.dll": os.path.join(REPO, r"plugin\build\LocalizationPatch.dll"),
    r"BepInEx\plugins\LocalizationPatch\LocalizationPatchDropdown.dll": os.path.join(PLUG, "LocalizationPatchDropdown.dll"),
    r"BepInEx\plugins\LocalizationPatch\WDXLLubrifontSC-Regular.ttf": os.path.join(PLUG, "WDXLLubrifontSC-Regular.ttf"),
}

if os.path.isdir(PKG):
    shutil.rmtree(PKG)
for rel, src in files.items():
    if not os.path.isfile(src):
        print("НЕТ ФАЙЛА:", src)
        sys.exit(1)
    dst = os.path.join(PKG, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    print("+ {:60s} {:>9s}".format(rel, "{:,} Б".format(os.path.getsize(dst))))

# ---------- 2. установщик и инструкция -------------
INSTALL_PS1 = r'''# Установка русификатора Nuclear Option (v{V})
param([string]$GamePath)

$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$src  = Join-Path $here 'BepInEx\plugins\LocalizationPatch'

function Say($t) {{ Write-Host $t }}
function Test-Game($p) {{ return (Test-Path (Join-Path $p 'NuclearOption.exe')) }}

Say ''
Say '=== Русификатор Nuclear Option, установка ==='
Say ''

if (-not (Test-Path $src)) {{ Say "Не нашёл файлы русификатора: $src"; Say 'Распакуйте архив целиком и запустите установщик заново.'; exit 1 }}

if ($GamePath) {{ $game = $GamePath.Trim('"') }} else {{ $game = $null }}

# поиск игры через библиотеки Steam
if (-not $game) {{
    $steamKeys = @('HKCU:\Software\Valve\Steam', 'HKLM:\SOFTWARE\WOW6432Node\Valve\Steam', 'HKLM:\SOFTWARE\Valve\Steam')
    $libs = @()
    foreach ($k in $steamKeys) {{
        try {{
            $p = Get-ItemProperty -Path $k -ErrorAction Stop
            foreach ($n in @('SteamPath', 'InstallPath')) {{ if ($p.$n) {{ $libs += ($p.$n -replace '/', '\') }} }}
        }} catch {{ }}
    }}
    foreach ($l in @($libs | Sort-Object -Unique)) {{
        $vdf = Join-Path $l 'steamapps\libraryfolders.vdf'
        if (Test-Path $vdf) {{
            foreach ($m in [regex]::Matches((Get-Content $vdf -Raw), '"path"\s+"([^"]+)"')) {{
                $libs += ($m.Groups[1].Value -replace '\\\\', '\')
            }}
        }}
    }}
    foreach ($l in @($libs | Sort-Object -Unique)) {{
        foreach ($sub in @('steamapps\common\Nuclear Option', 'steamapps\common\NuclearOption')) {{
            $cand = Join-Path $l $sub
            if (Test-Game $cand) {{ $game = $cand; break }}
        }}
        if ($game) {{ break }}
    }}
}}

if (-not $game) {{
    Say 'Не смог найти игру автоматически.'
    Say 'Вставьте путь к папке, где лежит NuclearOption.exe, и нажмите Enter.'
    Say 'Например: D:\Steam\steamapps\common\Nuclear Option'
    $game = (Read-Host 'Папка игры').Trim('"', ' ')
}}

if (-not (Test-Game $game)) {{ Say "В этой папке нет NuclearOption.exe: $game"; exit 1 }}

$dst = Join-Path $game 'BepInEx\plugins\LocalizationPatch'
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Copy-Item (Join-Path $src '*') $dst -Recurse -Force

$langDir = Join-Path $game 'BepInEx\config\LocalizationPatch'
try {{
    New-Item -ItemType Directory -Force -Path $langDir | Out-Null
    Copy-Item (Join-Path $src 'ru.json') (Join-Path $langDir 'ru.json') -Force
}} catch {{ Say "Бэкап словаря не скопирован (не критично)." }}

Say ''
Say "Файлы установлены в: $dst"

if (-not (Test-Path (Join-Path $game 'BepInEx\core\BepInEx.dll'))) {{
    Say ''
    Say 'ВНИМАНИЕ: в игре нет BepInEx — без него плагин не запустится.'
    Say 'Поставьте BepInEx 5.x (x64): https://github.com/BepInEx/BepInEx/releases'
    Say 'Нужен архив вида BepInEx_win_x64_5.4.x.zip — распакуйте его в папку игры и запустите игру один раз.'
}} else {{
    Say 'BepInEx на месте.'
}}

Say ''
Say 'Готово! Запускайте игру — русский язык включится автоматически.'
Say 'Словарь можно править на ходу: Ctrl+F5 в игре = перечитать ru.json.'
'''.replace("{V}", VER)

INSTALL_CMD = r'''@echo off
chcp 65001 >nul
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1" %*
echo.
pause
'''

README_TXT = r'''РУСИФИКАТОР NUCLEAR OPTION (v{V})
================================

Что это
-------
Перевод интерфейса, подсказок, брифингов и описаний техники/оружия.
Названия оружия, техники, миссий и локаций остаются английскими — так задумано.

Как поставить
-------------
1. Нужен BepInEx 5.x (x64) в папке игры:
   https://github.com/BepInEx/BepInEx/releases
   скачайте BepInEx_win_x64_5.4.x.zip и распакуйте в папку игры,
   затем запустите игру один раз и выйдите (BepInEx создаст свои папки).
   Если BepInEx уже стоит — шаг пропускаем.
2. Дважды щёлкните "Установить.cmd" — он сам найдёт папку игры.
   Если не найдёт, вставьте путь вручную, например:
   D:\Steam\steamapps\common\Nuclear Option
3. Запустите игру.

Ручная установка (если установщик не понравился): скопируйте папку
BepInEx из архива в папку игры, подтвердив замену файлов.

Горячие клавиши в игре
----------------------
Ничего нажимать не нужно — перевод включается сам. Клавиши ниже — только
для доработки перевода, в обычной игре они не требуются.

Ctrl+F5 — перечитать словарь ru.json (правки видны без перезапуска)
Ctrl+F4 — выгрузить подсказки/энциклопедию (для перевода)
Ctrl+F6 — выгрузить длинные строки из памяти игры

Настройки
---------
<игра>\BepInEx\config\com.noms.localizationpatch.cfg
  Language = auto        (язык определяется по файлу ru.json)
  AutoDump = false       (авто-выгрузка при запуске; трогать не нужно — она подвешивает игру)
  ShowDebugWindow = false (окно отладки по F9/F10; игроку не нужно)
  VerboseLog = false     ([TRACE] логи и выгрузка untranslated.txt; игроку не нужно)

Все четыре параметра по умолчанию — "для игрока": ничего лишнего не пишется
и никакие окна не всплывают.

Если что-то не работает
-----------------------
1. Посмотрите лог: <игра>\BepInEx\LogOutput.log
   Ищите строки "Localization Patch v{V} loaded" и "Loaded N translations from ru.json".
2. Если перевод не подхватился — убедитесь, что рядом с плагином лежит ru.json.
3. Если игра не запускается — удалите папку
   <игра>\BepInEx\plugins\LocalizationPatch и проверьте игру без неё.

Атрибуция
---------
Плагин — производная от NuclearOption-LocalizationPatch (автор 9138noms),
лицензия исходного проекта не заявлена, права принадлежат его автору.
Перевод и обёртка — вклад автора русификатора. Шрифт WDXL Lubrifont SC.
'''.replace("{V}", VER)

# install.ps1 и txt — UTF-8 с BOM (так Windows PowerShell верно читает кириллицу),
# .cmd — UTF-8 без BOM (cmd.exe с chcp 65001 не переваривает BOM)
INSTALL_PS1 = INSTALL_PS1.replace("{{", "{").replace("}}", "}")  # в шаблоне скобки удвоены
for name, body, enc in (("install.ps1", INSTALL_PS1, "utf-8-sig"),
                        ("Установить.cmd", INSTALL_CMD, "utf-8"),
                        ("ПРОЧТИ МЕНЯ.txt", README_TXT, "utf-8-sig")):
    p = os.path.join(PKG, name)
    io.open(p, "w", encoding=enc, newline="\r\n").write(body)
    print("+ {:60s} {:>9s}".format(name, "{:,} Б".format(os.path.getsize(p))))

# ---------- 3. zip -------------
zip_path = os.path.join(DIST, "NuclearOption-Rus-v" + VER + ".zip")
if os.path.exists(zip_path):
    os.remove(zip_path)
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for base, dirs, fs in os.walk(PKG):
        for f in fs:
            full = os.path.join(base, f)
            z.write(full, os.path.join("NuclearOption-Rus-v" + VER, os.path.relpath(full, PKG)))

size = os.path.getsize(zip_path)
sha = hashlib.sha256(open(zip_path, "rb").read()).hexdigest()
print()
print("ZIP :", zip_path)
print("размер: {:.1f} МБ".format(size / 1048576))
print("sha256:", sha)
print("файлов в пакете:", sum(len(f) for _, _, f in os.walk(PKG)))
