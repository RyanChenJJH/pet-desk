$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$themeRoot = Join-Path $projectRoot "theme"
$zipPath = Join-Path $projectRoot "shinchan.zip"

if (-not (Test-Path -LiteralPath $themeRoot)) {
  throw "Theme directory not found: $themeRoot"
}

if (Test-Path -LiteralPath $zipPath) {
  Remove-Item -LiteralPath $zipPath -Force
}

Compress-Archive -LiteralPath (Join-Path $themeRoot "theme.json"), (Join-Path $themeRoot "assets") -DestinationPath $zipPath -Force
Write-Host "Successfully packaged theme to $zipPath"
