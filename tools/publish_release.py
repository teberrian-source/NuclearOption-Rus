# -*- coding: utf-8 -*-
"""Публикация релиза v3.3.1 на GitHub: создаёт релиз и прикладывает ZIP-пакет.

Токен берётся из хранилища Windows (git credential fill) и на экран не выводится.
"""
import io, json, os, subprocess, sys, urllib.error, urllib.parse, urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OWNER = "teberrian-source"
REPO = "NuclearOption-Rus"
TAG = "v3.3.1"
ZIP = r"C:\Users\user\Documents\NuclearOption_Rus\dist\NuclearOption-Rus-v3.3.1.zip"
NOTES = """Русификатор Nuclear Option 0.34.2 — версия 3.3.1.

**Что в архиве:** словарь перевода (4256 записей), плагин LocalizationPatch 3.3.1,
аддон выпадающих списков, шрифт с кириллицей, установщик `Установить.cmd` и инструкция.

**Установка:** дважды щёлкнуть `Установить.cmd` (сам находит папку игры) — или скопировать
папку `BepInEx` из архива в папку игры. Нужен BepInEx 5.x (x64).

**Главное в 3.3.1:** из релиза убрано всё отладочное — окно статистики больше не всплывает
(включается флагом `ShowDebugWindow = true`), подробные `[TRACE]` логи и выгрузка
`untranslated.txt` по умолчанию отключены (`VerboseLog = true` — включить), подпись кнопки
исправлена на `Ctrl+F5`. Игроку в логе теперь достаются только строки о загрузке перевода.

**Ранее в 3.3.0:** убраны подвесы игры на ~10 секунд при каждом запуске — авто-выгрузка
определений больше не запускается сама (только по `Ctrl+F4`/`Ctrl+F6` или `AutoDump = true`
в конфиге).
"""

if not os.path.isfile(ZIP):
    print("НЕТ ZIP:", ZIP)
    sys.exit(1)

CRED = subprocess.run(["git", "credential", "fill"], input=b"protocol=https\nhost=github.com\n\n", capture_output=True)
token = None
for line in CRED.stdout.decode("utf-8", "replace").splitlines():
    if line.startswith("password="):
        token = line[len("password="):].strip()
if not token:
    print("ОШИБКА: нет сохранённых кредов github.com")
    sys.exit(1)

HEAD = {"Authorization": "Bearer " + token, "User-Agent": "opencode-localization", "Accept": "application/vnd.github+json"}
API = "https://api.github.com/repos/{}/{}".format(OWNER, REPO)


def call(url, payload=None, method=None, raw=None, ctype=None):
    data = raw if raw is not None else (json.dumps(payload).encode() if payload is not None else None)
    headers = dict(HEAD)
    if ctype:
        headers["Content-Type"] = ctype
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            body = resp.read()
            try:
                return resp.status, json.loads(body)
            except Exception:
                return resp.status, body
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        try:
            body = json.loads(body)
        except Exception:
            pass
        return exc.code, body


# релиз (если уже есть — берём существующий)
status, rel = call(API + "/releases", {"tag_name": TAG, "name": "Русификатор Nuclear Option 3.3.1", "body": NOTES, "draft": False, "prerelease": False})
if status not in (200, 201):
    status, rel = call(API + "/releases/tags/" + TAG)
    if status != 200:
        print("ОШИБКА создания релиза:", status, str(rel)[:300])
        sys.exit(1)
print("релиз:", rel["html_url"])

# вложение (загрузка идёт на uploads.github.com, а не на api.github.com)
name = os.path.basename(ZIP)
with open(ZIP, "rb") as f:
    blob = f.read()
upload_url = "https://uploads.github.com/repos/{}/{}/releases/{}/assets?name={}".format(
    OWNER, REPO, rel["id"], urllib.parse.quote(name))
status, asset = call(upload_url, raw=blob, ctype="application/zip")
if status in (200, 201):
    print("вложение загружено: {} ({:,} Б)".format(asset["name"], asset["size"]))
    print("ссылка на скачивание:", asset["browser_download_url"])
else:
    print("ОШИБКА загрузки вложения:", status, str(asset)[:300])
    sys.exit(1)
