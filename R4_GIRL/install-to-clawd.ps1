$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$themeRoot = Join-Path $projectRoot "theme"
$targetRoot = "E:\Work2\AI_Work\tool\clawd-on-desk\clawd-on-desk\themes\r4-girl"

if (-not (Test-Path -LiteralPath $themeRoot)) {
  throw "Theme directory not found: $themeRoot"
}

if (-not (Test-Path -LiteralPath (Split-Path -Parent $targetRoot))) {
  throw "Clawd themes directory not found: $(Split-Path -Parent $targetRoot)"
}

if (Test-Path -LiteralPath $targetRoot) {
  Remove-Item -LiteralPath $targetRoot -Recurse -Force
}

New-Item -ItemType Directory -Path $targetRoot | Out-Null
Copy-Item -LiteralPath (Join-Path $themeRoot "theme.json") -Destination $targetRoot
Copy-Item -LiteralPath (Join-Path $themeRoot "assets") -Destination $targetRoot -Recurse

Write-Host "Installed R4 Girl theme to $targetRoot"

