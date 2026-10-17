
$ErrorActionPreference = 'Stop'
$dll = 'C:\Users\user\Desktop\Nuclear Option\NuclearOption_Data\Managed\Unity.TextMeshPro.dll'
$asm = [System.Reflection.Assembly]::LoadFrom($dll)

function Dump-Type($name) {
  $t = $asm.GetType($name)
  if (-not $t) { Write-Output "$name : TYPE NOT FOUND"; return }
  Write-Output "=== $name ==="
  # свойство text
  $p = $t.GetProperty('text', [Reflection.BindingFlags]'Public,Instance,DeclaredOnly')
  if ($p) {
    $s = $p.GetSetMethod($true)
    if ($s) { Write-Output ("  text.set: virtual={0} final={1} abstract={2} decl={3}" -f $s.IsVirtual, $s.IsFinal, $s.IsAbstract, $s.DeclaringType.Name) }
  } else { Write-Output "  text property: no DeclaredOnly" }
  # SetText
  foreach ($m in $t.GetMethods([Reflection.BindingFlags]'Public,Instance,DeclaredOnly')) {
    if ($m.Name -eq 'SetText' -or $m.Name -eq 'OnEnable' -or $m.Name -eq 'Awake' -or $m.Name -eq 'OnDisable') {
      $parms = ($m.GetParameters() | ForEach-Object { $_.ParameterType.Name }) -join ','
      Write-Output ("  {0}({1}): virtual={2} final={3} decl={4}" -f $m.Name, $parms, $m.IsVirtual, $m.IsFinal, $t.Name)
    }
  }
}

# наследники: ищем всех кто наследует TMP_Text
$tmp = $asm.GetType('TMPro.TMP_Text')
$subs = $asm.GetTypes() | Where-Object { $_.BaseType -and $_.BaseType.FullName -eq 'TMPro.TMP_Text' }
Write-Output ("TMP_Text subclasses: " + (($subs | ForEach-Object { $_.Name }) -join ', '))

Dump-Type 'TMPro.TMP_Text'
foreach ($s in $subs) { Dump-Type $s.FullName }

# текстовый setter базового класса: virtual?
$bt = $asm.GetType('TMPro.TMP_Text')
$sp = $bt.GetProperty('text')
$sm = $sp.GetSetMethod($true)
Write-Output ("BASE TMP_Text.text.set: virtual={0} final={1} abstract={2}" -f $sm.IsVirtual, $sm.IsFinal, $sm.IsAbstract)
