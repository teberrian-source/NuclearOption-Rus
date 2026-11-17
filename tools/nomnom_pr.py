# -*- coding: utf-8 -*-
"""PR в KopterBuzz/NOMNOM: обновление modManifests/LocalizationPatch.Russian.json
до v3.3.3 (teberrian-source/NuclearOption-Rus, game 0.34.6, 4343 записи)."""
import io, json, os, subprocess, sys, tempfile, time, urllib.request, urllib.error

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
REPO_DIR = r"C:\Users\user\Documents\NuclearOption_Rus"
UPSTREAM = "KopterBuzz/NOMNOM"
FORK = "teberrian-source/NOMNOM"
PATH = "modManifests/LocalizationPatch.Russian.json"

# ---- токен (как в publish_release_333) ----
def token_via_git_credential():
    inp = subprocess.run(["git", "-C", REPO_DIR, "credential", "fill"],
                         input="protocol=https\nhost=github.com\n\n",
                         capture_output=True, text=True).stdout
    for line in inp.splitlines():
        if line.startswith("password="):
            return line[len("password="):].strip()
    return None

token = token_via_git_credential()
assert token, "нет токена"

def api(url, data=None, method=None):
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "nomnom-pr")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    return urllib.request.urlopen(req).read()

# 1. форк (идемпотентно)
try:
    api(f"https://api.github.com/repos/{FORK}")
    print("форк уже существует")
except urllib.error.HTTPError as e:
    assert e.code == 404, e
    api(f"https://api.github.com/repos/{UPSTREAM}/forks", b"{}", method="POST")
    print("форк создан, ждём готовности")
    for _ in range(30):
        time.sleep(3)
        try:
            api(f"https://api.github.com/repos/{FORK}")
            break
        except urllib.error.HTTPError:
            continue

# 2. свежий манифест из upstream
cur = json.loads(urllib.request.urlopen(
    f"https://raw.githubusercontent.com/{UPSTREAM}/main/{PATH}").read())

# 3. правки
cur["description"] = ("Russian (Русский) translation for Nuclear Option 0.34.6. "
                      "Translates UI, encyclopedia, briefings, hints, tooltips and "
                      "modded equipment descriptions — 4,343 entries. Actively "
                      "maintained continuation of 9138noms' Russian patch.")
cur["urls"] = [
    {"name": "info", "url": "https://github.com/teberrian-source/NuclearOption-Rus"},
    {"name": "original", "url": "https://github.com/9138noms/NuclearOption-RussianPatch"},
]
if "teberrian-source" not in cur["authors"]:
    cur["authors"] = ["9138noms", "teberrian-source"]
cur["githubOwner"] = "teberrian-source"
cur["githubRepoName"] = "NuclearOption-Rus"
cur["autoUpdateArtifacts"] = "True"
cur["isAiAssisted"] = "True"

incompat = cur["artifacts"][0].get("incompatibilities", [])
new_artifact = {
    "fileName": "NuclearOption-Rus-v3.3.3.zip",
    "version": "3.3.3",
    "category": "release",
    "type": "plugin",
    "gameVersion": "0.34.6",
    "downloadUrl": "https://github.com/teberrian-source/NuclearOption-Rus/releases/download/v3.3.3/NuclearOption-Rus-v3.3.3.zip",
    "hash": "sha256:395d7a317f7774f7e28ea6ae71756fa79acceb4dbbb6386e691db3ca9e13d344",
}
if incompat:
    new_artifact["incompatibilities"] = incompat
cur["artifacts"].insert(0, new_artifact)

content = json.dumps(cur, indent=2, ensure_ascii=False) + "\n"
io.open(os.path.join(tempfile.gettempdir(), "nomnom_ru.json"), "w",
        encoding="utf-8").write(content)

# 4. коммит в форк (contents API)
sha_resp = json.loads(urllib.request.urlopen(
    f"https://api.github.com/repos/{FORK}/contents/{PATH}?ref=main").read())
put = json.dumps({
    "message": "Update LocalizationPatch.Russian to v3.3.3 (game 0.34.6, 4343 entries)",
    "content": __import__("base64").b64encode(content.encode("utf-8")).decode("ascii"),
    "sha": sha_resp["sha"],
    "branch": "main",
}).encode()
api(f"https://api.github.com/repos/{FORK}/contents/{PATH}", put, method="PUT")
print("манифест обновлён в форке")

# 5. PR
pr_body = """## What this PR does

Updates `modManifests/LocalizationPatch.Russian` — the Russian Localization Patch has been actively maintained as a continuation of 9138noms' original patch, and is now published from **teberrian-source/NuclearOption-Rus**.

## Changes

- **New artifact v3.3.3** (on top): game **0.34.6**, dictionary grew **1,427 → 4,343 entries**, plugin **3.3.3**
  - plugin 3.3.3 adds an on-demand full rescan (Ctrl+F5) — no periodic background scanning, zero added load
  - covers vanilla 0.34.6 content plus descriptions of popular modded aircraft/weapons (AH-31 Kukri, Su-30VXN, SR-31R Halberd, VK-24M Striga, MC-260 Chimera, R-27R/R-27T/R-60M/R-73, ground turrets, etc.)
- `githubOwner`/`githubRepoName` → `teberrian-source/NuclearOption-Rus` (releases are auto-discoverable: tag `v3.3.3`, single zip asset `NuclearOption-Rus-v3.3.3.zip`)
- `urls.info` → new repository; original author's repo kept as `urls.original`
- `authors`: **9138noms** (original) + **teberrian-source** (maintainer)
- `isAiAssisted`: declared **"True"** per policy §1.2 (translation dictionary and plugin code were created with substantial AI assistance; the DLL is source-available in the repo, no obfuscation)
- Previous artifacts of 9138noms kept untouched as history
- `incompatibilities` with other LocalizationPatch language packs preserved

## Acceptance policy notes

- Custom DLL (LocalizationPatch.dll) is a derivative of 9138noms/NuclearOption-LocalizationPatch; full source is in the repository (`plugin/` folder), unobfuscated, attribution included in the release notes and `ПРОЧТИ МЕНЯ.txt`
- Font: WDXL Lubrifont SC (bundled, as in previous releases of this patch)
- Release zip sha256: `395d7a317f7774f7e28ea6ae71756fa79acceb4dbbb6386e691db3ca9e13d344`

Release: https://github.com/teberrian-source/NuclearOption-Rus/releases/tag/v3.3.3
"""

pr = json.dumps({
    "title": "Update LocalizationPatch.Russian to v3.3.3 (game 0.34.6, 4343 entries)",
    "head": "teberrian-source:main",
    "base": "main",
    "body": pr_body,
}).encode()
resp = json.loads(api(f"https://api.github.com/repos/{UPSTREAM}/pulls", pr, method="POST"))
print("PR создан:", resp["html_url"])
