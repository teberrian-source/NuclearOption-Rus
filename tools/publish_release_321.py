# -*- coding: utf-8 -*-
"""Создание GitHub Release v3.3.2.1 с zip-ассетом через API (токен из git credential)."""
import base64, io, json, os, subprocess, sys, urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OWNER_REPO = "teberrian-source/NuclearOption-Rus"
TAG = "v3.3.2.1"
ZIP = os.path.join(REPO, "dist", "NuclearOption-Rus-v3.3.2.1.zip")

# токен из хранилища учётных данных git
inp = subprocess.run(["git", "-C", REPO, "credential", "fill"],
                     input="protocol=https\nhost=github.com\n\n",
                     capture_output=True, text=True).stdout
token = None
for line in inp.splitlines():
    if line.startswith("password="):
        token = line[len("password="):]
assert token, "токен не найден в git credential"
print("токен получен (длина", len(token), ")")

def api(url, data=None, method=None, ctype="application/json", tok=token):
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + tok)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "rus-uploader")
    if ctype:
        req.add_header("Content-Type", ctype)
    return urllib.request.urlopen(req).read()

# существует ли уже релиз с этим тегом
try:
    api(f"https://api.github.com/repos/{OWNER_REPO}/releases/tags/{TAG}")
    print("релиз с тегом уже существует — выходим")
    sys.exit(0)
except urllib.error.HTTPError as e:
    assert e.code == 404, e

body = json.dumps({
    "tag_name": TAG,
    "target_commitish": "main",
    "name": "v3.3.2.1 — словарь 4297 (0.34.6)",
    "body": ("Плагин 3.3.2 без изменений. Что нового:\n\n"
             "- Словарь 4256 → **4297**: дословные описания миссий 0.34.6 (Escalation / Escalation North, "
             "Ostrin Confrontation, Port Ansel Defence, Sill Strike, Icebreaker, SAM Hunt, KR-33 01. Dustbowl, "
             "Swiss Alps Free Flight) и **полное описание Cascadia Falling**\n"
             "- Описания ракет R-60M и R-73, бака PTB-1500, пушки GSh-30-1, радара AWACS\n"
             "- UI: метки пилонов/отсеков, «Недавние», Esc/Select/Navigate, «Найдено: 1», «Команды», «История», «Нет результатов»\n"
             "- «ЭПР» расшифровано: **«Радиозаметность»**\n"
             "- Укорочены строки, вылезавшие за кнопки (перезапуск миссии, дорожная карта, сообщество, «Следующий самолёт»)\n\n"
             "Установка: распаковать, запустить «Установить.cmd» (нужен BepInEx 5.x x64). Подробности — в «ПРОЧТИ МЕНЯ.txt»."),
    "draft": False,
    "prerelease": False,
}).encode()
rel = json.loads(api(f"https://api.github.com/repos/{OWNER_REPO}/releases", body, method="POST"))
print("релиз создан:", rel["html_url"])

# загрузка zip-ассета
up_url = rel["upload_url"].split("{")[0] + "?name=NuclearOption-Rus-v3.3.2.1.zip"
data = open(ZIP, "rb").read()
up = json.loads(api(up_url, data, method="POST", ctype="application/zip"))
print("ассет загружен:", up["browser_download_url"], f"({up['size']} Б)")
