# -*- coding: utf-8 -*-
"""Создание GitHub Release v3.3.3 с zip-ассетом через API (токен из git credential)."""
import io, json, os, subprocess, sys, tempfile, urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
REPO_DIR = r"C:\Users\user\Documents\NuclearOption_Rus"
OWNER_REPO = "teberrian-source/NuclearOption-Rus"
TAG = "v3.3.3"
ZIP = os.path.join(REPO_DIR, "dist", "NuclearOption-Rus-v3.3.3.zip")

# токен: git credential fill напрямую, при неудаче — через ps1-helper (как в 3.3.2)
def token_via_git_credential():
    inp = subprocess.run(["git", "-C", REPO_DIR, "credential", "fill"],
                         input="protocol=https\nhost=github.com\n\n",
                         capture_output=True, text=True).stdout
    for line in inp.splitlines():
        if line.startswith("password="):
            return line[len("password="):].strip()
    return None

def token_via_helper():
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
    token_file = os.path.join(tempfile.gettempdir(), "gh_token.tmp")
    try:
        io.open(helper, "w", encoding="utf-8-sig", newline="\r\n").write(helper_content)
        subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", helper, token_file],
                       check=False, capture_output=True)
    finally:
        try:
            os.remove(helper)
        except OSError:
            pass
    if os.path.exists(token_file):
        t = io.open(token_file, encoding="utf-8", errors="replace").read().strip().splitlines()[0].strip()
        try:
            os.remove(token_file)
        except OSError:
            pass
        return t
    return None

token = token_via_git_credential() or token_via_helper()
assert token, "токен не найден"
print("токен получен (длина", len(token), ")")

def api(url, data=None, method=None, ctype="application/json"):
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "rus-uploader")
    if ctype:
        req.add_header("Content-Type", ctype)
    return urllib.request.urlopen(req).read()

# релиз с этим тегом уже существует?
try:
    api(f"https://api.github.com/repos/{OWNER_REPO}/releases/tags/{TAG}")
    print("релиз с тегом уже существует — выходим")
    sys.exit(0)
except urllib.error.HTTPError as e:
    assert e.code == 404, e

BODY = """Русификатор Nuclear Option — v3.3.3 (для игры 0.34.6)

## Что нового
- **Плагин 3.3.3: рескан по Ctrl+F5.** Ctrl+F5 теперь не только перечитывает словарь,
  но и один раз переводит все уже видимые надписи, которые не прошли через хуки
  (например, описания модовой техники в ангаре). Постоянного фонового сканирования
  нет — в игре без нажатия клавиши плагин не добавляет никакой нагрузки.
- **Словарь 4297 → 4343**: модовый контент 0.34.6 —
  описания AH-31 Kukri (включая лазер 80 кВт и 20-мм HEI), Su-30VXN,
  SR-31R Halberd, VK-24M Striga, MC-260 Chimera;
  ракеты R-27R / R-27T / R-60M / R-73 (MiG-29), туррели .50 и миномёт 76-мм;
  UI: подсказки привязки управления, списки банов/мутов мультиплеера, чат,
  «Ожидание загрузки рельефа», диалог удаления миссии, метки пилонных групп.
- Названия техники/оружия/миссий по-прежнему не переводятся (так задумано).

## Установка
1. В папке игры должен быть BepInEx 5.x (x64).
2. Распакуйте архив и запустите `Установить.cmd` (сам найдёт папку игры).
Подробности — в `ПРОЧТИ МЕНЯ.txt`.

## Атрибуция
Плагин — производная от 9138noms/NuclearOption-LocalizationPatch. Шрифт WDXL Lubrifont SC.

sha256 (zip): 395d7a317f7774f7e28ea6ae71756fa79acceb4dbbb6386e691db3ca9e13d344
sha256 (dll): 33a7cc21a6059cb4f591a795915dd4b22ab84898b0504911430bab0583d34068
"""

body = json.dumps({
    "tag_name": TAG,
    "target_commitish": "main",
    "name": "v3.3.3 — плагин с ресканом Ctrl+F5, словарь 4343 (0.34.6)",
    "body": BODY,
    "draft": False,
    "prerelease": False,
}).encode()
rel = json.loads(api(f"https://api.github.com/repos/{OWNER_REPO}/releases", body, method="POST"))
print("релиз создан:", rel["html_url"])

up_url = rel["upload_url"].split("{")[0] + "?name=NuclearOption-Rus-v3.3.3.zip"
data = open(ZIP, "rb").read()
up = json.loads(api(up_url, data, method="POST", ctype="application/zip"))
print("ассет загружен:", up["browser_download_url"], f"({up['size']} Б)")
