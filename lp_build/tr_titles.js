// Перевод коротких заголовков подсказок обучения.
// Сохраняет отступы выравнивания и счётчики без изменений.
const fs = require('fs');

const SRC = 'C:\\Users\\user\\AppData\\Local\\Temp\\lp_build\\todo_titles.txt';
const OUT = 'C:\\Users\\user\\AppData\\Local\\Temp\\lp_build\\tr_titles.json';

const MAP = {
  'Infrared Countermeasures': 'ИК-противодействие',
  'Flare Usage': 'Применение ловушек',
  'Not dangerous enough': 'Недостаточно опасно',
  'Escape': 'Уход',
  'Evasion Complete': 'Уклонение выполнено',
  'Prepare for Landing': 'Подготовка к посадке',
  'Deploy Gear': 'Выпустить шасси',
  'Landing Assist': 'Помощь при посадке',
  'Glideslope indicator': 'Указатель глиссады',
  'Angle of Attack Indexer': 'Указатель угла атаки',
  'Wheel Brakes': 'Колёсные тормоза',
  'Successful Landing': 'Посадка выполнена',
  'Landing Complete': 'Посадка завершена',
  'Brakes': 'Тормоза',
  'Centered on runway': 'По оси ВПП',
  'Full Throttle': 'Полный газ',
  'Successful Takeoff': 'Взлёт выполнен',
  'Enemy Radar': 'РЛС противника',
  'Radar Range': 'Дальность РЛС',
  'Notching': 'Противофазный манёвр',
  'Defending': 'Оборона',
  'Escaped Successfully': 'Уход выполнен',
  'Helmet Mounted Display': 'Нашлемный дисплей',
  'Target Designation': 'Целеуказание',
  'Weapon Usage': 'Применение оружия',
  'Aerial Targets': 'Воздушные цели',
  'Fratricide': 'Огонь по своим',
};

const raw = fs.readFileSync(SRC, 'utf8');
const lines = raw.split(/\r?\n/);

const result = {};
let num = null;
let count = 0;

for (const line of lines) {
  const head = line.match(/^###\s*(\d+)\s*$/);
  if (head) { num = head[1]; continue; }
  if (num === null || line.trim() === '') continue;

  // Текст + (необязательно) отступ и счётчик вида 1/2
  const m = line.match(/^(.+?)(\s{2,}\d+\/\d+)$/);
  const text = (m ? m[1] : line).trimEnd();
  const tail = m ? m[2] : '';
  const tr = MAP[text];
  if (!tr) throw new Error('Нет перевода для: "' + text + '"');
  result[num] = tr + tail;
  count++;
  num = null;
}

fs.writeFileSync(OUT, JSON.stringify(result, null, 1), 'utf8');
console.log('translated=' + count);
