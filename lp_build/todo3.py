# -*- coding: utf-8 -*-
"""Формирует todo3.json — оставшиеся английские UI-строки (редактор миссий, настройки, HUD-редактор)."""
import io, re, sys, json

sys.stdout.reconfigure(encoding="utf-8")
base = r"C:\Users\user\Desktop\NuclearOption_0.34.2\BepInEx\plugins\LocalizationPatch"
T = r"C:\Users\user\AppData\Local\Temp\lp_build"

def parse(p):
    raw = io.open(p, encoding="utf-8-sig").read()
    ls = [l for l in raw.split("\n") if not l.strip().startswith("//")]
    return json.loads(re.sub(r",\s*([}\]])", r"\1", "\n".join(ls)), strict=False)

ru = parse(base + r"\ru.json")
raw = io.open(base + r"\extracted_strings.txt", encoding="utf-8", errors="replace").read()
raw = raw.split("// ========== RAW LONG STRINGS")[0]

SRC = ("TextMeshProUGUI.m_text", "Text.m_Text", "StyleLabel.displayLabel")
SKIP = ("Lorem ipsum", "According to all known laws", "Navy Seals", "Test Error Message", "IndexNotFoundException",
        "placeholder", "Long description about some stuff", "This is how wide the text box",
        "Score 0,0", "What the fuck", "long file name", "Long Mission Name", "Test Error")
CYR = re.compile(r"[А-Яа-яЁё]")

cur, items = "?", []
for line in raw.split("\n"):
    s = line.strip()
    if s.startswith("//"):
        x = s[2:].strip()
        if x and "===" not in x:
            cur = x
        continue
    m = re.match(r'^"((?:[^"\\]|\\.)*)": ""', s)
    if not m or cur not in SRC:
        continue
    try:
        t = json.loads('"' + m.group(1) + '"')
    except Exception:
        continue
    if len(t) < 12 or t in ru or CYR.search(t):
        continue
    if "{" in t or "}" in t:          # шаблоны с подстановкой
        continue
    if any(k.lower() in t.lower() for k in SKIP):
        continue
    items.append({"i": len(items) + 1, "src": cur, "en": t})

io.open(T + r"\todo3.json", "w", encoding="utf-8").write(json.dumps(items, ensure_ascii=False, indent=1))
print("к переводу:", len(items))
out = []
for it in items:
    out.append(f"{it['i']}|{json.dumps(it['en'], ensure_ascii=False)}")
io.open(T + r"\todo3_escaped.txt", "w", encoding="utf-8").write("\n".join(out))
print("файлы: todo3.json, todo3_escaped.txt")
