# -*- coding: utf-8 -*-
"""1) Точное сравнение текста CI-22 из игры с ключом ru.json.
2) Поиск TextAsset с описаниями узлов (Tusko-B и т.п.) → Radome."""
import sys, json, re, io
import UnityPy

root = r"C:\Users\user\Desktop\Nuclear Option\NuclearOption_Data"
sys.stdout.reconfigure(encoding='utf-8')

# --- 1) точный текст CI-22 из игры ---
env = UnityPy.load(root + r"\resources.assets")
ci_game = None
tusko_asset = None
for obj in env.objects:
    if obj.type.name != "TextAsset":
        continue
    try:
        d = obj.read()
        s = d.m_Script if hasattr(d, 'm_Script') else None
    except Exception:
        continue
    if not s:
        continue
    if 'counter insurgency' in s:
        m = re.search(r'AircraftDefinition;CI-22 Cricket;CI-22;(.*?);\d', s)
        if m:
            ci_game = m.group(1)
    if 'Tusko-B is a supersonic' in s and tusko_asset is None:
        tusko_asset = s

# --- ключ из ru.json ---
p = r"C:\Users\user\Desktop\Nuclear Option\BepInEx\plugins\LocalizationPatch\ru.json"
raw = io.open(p, encoding='utf-8-sig').read()
lines = [l for l in raw.split('\n') if not l.strip().startswith('//')]
clean = re.sub(r',\s*([}\]])', r'\1', '\n'.join(lines))
data = json.loads(clean, strict=False)

key_ru = None
for k in data:
    if 'counter insurgency' in k.lower():
        key_ru = k
        break

print("=== СРАВНЕНИЕ CI-22 ===")
if ci_game and key_ru:
    print("game len:", len(ci_game), "| json len:", len(key_ru))
    print("equal:", ci_game == key_ru)
    if ci_game != key_ru:
        # найти первое различие
        for i, (a, b) in enumerate(zip(ci_game, key_ru)):
            if a != b:
                print(f"diff at {i}: game={a!r} json={b!r}")
                print("game ctx:", repr(ci_game[max(0,i-30):i+40]))
                print("json ctx:", repr(key_ru[max(0,i-30):i+40]))
                break
        else:
            print("одинаковый префикс, разная длина")
            print("game tail:", repr(ci_game[len(key_ru):]))
            print("json tail:", repr(key_ru[len(ci_game):]))
    print("game repr:", repr(ci_game))
else:
    print("ci_game found:", ci_game is not None, "| key found:", key_ru is not None)

# --- 2) описания узлов ---
print("\n=== ИСТОЧНИК ОПИСАНИЙ УЗЛОВ ===")
if tusko_asset:
    print("asset len:", len(tusko_asset))
    # показать где Radome встречается как описание
    for m in re.finditer(r'.{0,200}Radome.{0,300}', tusko_asset, re.I):
        print("...", repr(m.group(0))[:500], "\n")
    # формат: показать начало секции описаний
    i = tusko_asset.find('Tusko-B is a supersonic')
    print("CONTEXT around Tusko desc:")
    print(repr(tusko_asset[max(0, i-500):i+200]))
else:
    print("Tusko asset не найден в resources.assets — ищу в других")
