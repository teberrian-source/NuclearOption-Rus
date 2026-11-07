# -*- coding: utf-8 -*-
"""Создание релиза v3.3.2 на GitHub + загрузка ZIP-ассета (токен не печатается)."""
import io, json, os, subprocess, sys, tempfile, urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = "teberrian-source/NuclearOption-Rus"
ZIP = r"C:\Users\user\Documents\NuclearOption_Rus\dist\NuclearOption-Rus-v3.3.2.zip"

# credential manager не отдаёт токен в python-пайп — helper-ps1 создаётся и удаляется на ходу
token_file = os.path.join(tempfile.gettempdir(), "gh_token.tmp")
helper_content = """
param([Parameter(Mandatory = $true)][string]$OutFile)
$probe = "protocol=https`nhost=github.com`n"
$info = $probe | git credential fill 2>$null
if (-not $info) { exit 1 }
$token = ($info | Select-String -Pattern '^password=').Line -replace '^password=', ''
$token = ($token -split "`n")[0].Trim()
[IO.File]::WriteAllText($OutFile, $token)
"""
helper = os.path.join(tempfile.gettempdir(), "gh_token_export_tmp.ps1")
try:
    io.open(helper, "w", encoding="utf-8-sig", newline="\r\n").write(helper_content)
    subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", helper, token_file],
        check=False,
        capture_output=True,
    )
finally:
    try:
        os.remove(helper)
    except OSError:
        pass
token = io.open(token_file, encoding="utf-8", errors="replace").read().strip().splitlines()[0].strip() if os.path.exists(token_file) else None
try:
    os.remove(token_file)
except OSError:
    pass
if not token:
    raise SystemExit("нет токена")

HEADER = {"Accept": "application/vnd.github+json", "User-Agent": "release-script", "Authorization": "Bearer " + token}

BODY = """Русификатор Nuclear Option — v3.3.2

## Что нового
- Исправлено наложение строк в меню управления: русские подписи действий
  (на 30–80% шире английских) переносились на вторую строку при фиксированной
  высоте ряда и наезжали друг на друга. Для 110 строк меню перенос строк
  отключён — подписи выводятся одной строкой.
- Релизная чистка сохранена: отладочное окно, `[TRACE]`-логи и авто-выгрузки
  выключены по умолчанию (флаги в конфиге).

## Известная проблема (не русификатор)
При включённом моде **Boscali Ocean Training Exercise (BOTE)** назначение
vanilla-действий (например «Apply Brakes») в меню управления может не работать:
это конфликт ввода самого BOTE, подтверждено A/B-тестом на чистой игре.
Обходной путь: назначить клавиши при выключенном BOTE и включить его обратно
(настройки не теряются), либо нажать «Reset Maps» в BepInEx ConfigManager (F1)
→ BoscaliOceanTrainingExercise_Inputs.

## Установка
1. В папке игры должен быть BepInEx 5.x (x64).
2. Распакуйте архив и запустите `Установить.cmd` (сам найдёт папку игры).
Подробности в `ПРОЧТИ МЕНЯ.txt`.

## Атрибуция
Плагин — производная от 9138noms/NuclearOption-LocalizationPatch. Шрифт WDXL Lubrifont SC.
sha256 (целый): 8977a311f2976e34424330d6a94fd1e5ccf5d1a274c55e1f53a3d13645de8454
"""

body = json.dumps({"tag_name": "v3.3.2", "target_commitish": "main", "name": "v3.3.2", "body": BODY, "draft": False, "prerelease": False}).encode()
req = urllib.request.Request(f"https://api.github.com/repos/{REPO}/releases", data=body, headers={**HEADER, "Content-Type": "application/json"}, method="POST")
with urllib.request.urlopen(req, timeout=60) as r:
    rel = json.loads(r.read())
rid = rel["id"]
print("release id:", rid, "url:", rel["html_url"])

# сюда больше 100 МБ нельзя, но размер меньше
asset_name = "NuclearOption-Rus-v3.3.2.zip"
uploads = "https://uploads.github.com/repos/%s/releases/%d/assets?name=%s" % (REPO, rid, asset_name)
data = open(ZIP, "rb").read()
ureq = urllib.request.Request(uploads, data=data, headers={**HEADER, "Content-Type": "application/zip"}, method="POST")
with urllib.request.urlopen(ureq, timeout=600) as r:
    a = json.loads(r.read())
print("asset:", a["name"], a["size"], "байт, download:", a["browser_download_url"])
