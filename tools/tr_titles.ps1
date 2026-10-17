# Перевод коротких заголовков подсказок обучения.
# Сохраняет отступы выравнивания и счётчики без изменений.
$ErrorActionPreference = 'Stop'

$src = 'C:\Users\user\AppData\Local\Temp\lp_build\todo_titles.txt'
$out = 'C:\Users\user\AppData\Local\Temp\lp_build\tr_titles.json'

$map = @{
  'Infrared Countermeasures' = 'ИК-противодействие'
  'Flare Usage'              = 'Применение ловушек'
  'Not dangerous enough'     = 'Недостаточно опасно'
  'Escape'                   = 'Уход'
  'Evasion Complete'         = 'Уклонение выполнено'
  'Prepare for Landing'      = 'Подготовка к посадке'
  'Deploy Gear'              = 'Выпустить шасси'
  'Landing Assist'           = 'Помощь при посадке'
  'Glideslope indicator'     = 'Указатель глиссады'
  'Angle of Attack Indexer'  = 'Указатель угла атаки'
  'Wheel Brakes'             = 'Колёсные тормоза'
  'Successful Landing'       = 'Посадка выполнена'
  'Landing Complete'         = 'Посадка завершена'
  'Brakes'                   = 'Тормоза'
  'Centered on runway'       = 'По оси ВПП'
  'Full Throttle'            = 'Полный газ'
  'Successful Takeoff'       = 'Взлёт выполнен'
  'Enemy Radar'              = 'РЛС противника'
  'Radar Range'              = 'Дальность РЛС'
  'Notching'                 = 'Противофазный манёвр'
  'Defending'                = 'Оборона'
  'Escaped Successfully'     = 'Уход выполнен'
  'Helmet Mounted Display'   = 'Нашлемный дисплей'
  'Target Designation'       = 'Целеуказание'
  'Weapon Usage'             = 'Применение оружия'
  'Aerial Targets'           = 'Воздушные цели'
  'Fratricide'               = 'Огонь по своим'
}

$lines = [System.IO.File]::ReadAllLines($src, [System.Text.Encoding]::UTF8)
$result = [ordered]@{}
$num = $null
$count = 0

foreach ($line in $lines) {
  $head = [regex]::Match($line, '^###\s*(\d+)\s*$')
  if ($head.Success) { $num = $head.Groups[1].Value; continue }
  if (-not $num -or $line.Trim() -eq '') { continue }

  # Текст + (необязательно) отступ и счётчик вида 1/2
  $m = [regex]::Match($line, '^(.+?)(\s{2,}\d+/\d+)$')
  if ($m.Success) { $text = $m.Groups[1].Value.TrimEnd(); $tail = $m.Groups[2].Value }
  else { $text = $line.TrimEnd(); $tail = '' }

  if (-not $map.ContainsKey($text)) { throw "Нет перевода для: `"$text`"" }
  $result[$num] = $map[$text] + $tail
  $count++
  $num = $null
}

# UTF-8 без BOM, с обычными пробелами
$json = $result | ConvertTo-Json -Depth 3
$enc = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($out, $json, $enc)
Write-Output "translated=$count"
