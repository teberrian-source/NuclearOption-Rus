# NOMM Manifest Switch - toggles NOMM manifest between ORIGINAL and RUSSIAN.
# ORIGINAL  : kopterbuzz.github.io/NOMNOM  (default from NOMM 5.4.0 sources)
# RUSSIAN   : teberrian-source/nomm-ru-manifest
# Run while NOMM is CLOSED (otherwise NOMM overwrites config on exit).

$cfg = Join-Path $env:APPDATA 'NOMM\config.json'
if (-not (Test-Path $cfg)) { Write-Host "Config not found: $cfg"; pause; exit 1 }

$orig = @{
    manifestUrl        = 'https://kopterbuzz.github.io/NOMNOM/manifest/manifest.json'
    manifestVersionUrl = 'https://kopterbuzz.github.io/NOMNOM/manifest/version.json'
    name = 'ORIGINAL (NOMNOM)'
}
$ru = @{
    manifestUrl        = 'https://raw.githubusercontent.com/teberrian-source/nomm-ru-manifest/main/dist/manifest.json'
    manifestVersionUrl = 'https://raw.githubusercontent.com/teberrian-source/nomm-ru-manifest/main/dist/version.json'
    name = 'RUSSIAN (teberrian-source)'
}

$json = Get-Content $cfg -Raw
$isRu = $json -match 'nomm-ru-manifest'
$fromName = if ($isRu) { 'RUSSIAN' } else { 'ORIGINAL' }
$target = if ($isRu) { $orig } else { $ru }

Copy-Item $cfg "$cfg.bak" -Force
$json = $json -replace '"manifestUrl"\s*:\s*"[^"]*"', ('"manifestUrl":"' + $target.manifestUrl + '"')
$json = $json -replace '"manifestVersionUrl"\s*:\s*"[^"]*"', ('"manifestVersionUrl":"' + $target.manifestVersionUrl + '"')
Set-Content $cfg $json -Encoding UTF8

$check = Get-Content $cfg -Raw
$now = if ($check -match 'nomm-ru-manifest') { 'RUSSIAN' } elseif ($check -match 'NOMNOM') { 'ORIGINAL' } else { 'UNKNOWN' }

Write-Host ''
Write-Host "Switched: $fromName  ->  $now"
Write-Host ''
Write-Host ('  manifest URL        : ' + $target.manifestUrl)
Write-Host ('  manifestVersion URL : ' + $target.manifestVersionUrl)
Write-Host ''
Write-Host 'Backup saved as config.json.bak. Start NOMM and refresh Library.'
pause
