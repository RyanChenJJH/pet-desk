# install-to-clawd.ps1
# Sync Shin-chan (蜡笔小新) theme to Clawd-on-desk and create clean import zip

$ErrorActionPreference = "Stop"
$ThemeDir = Join-Path $PSScriptRoot "theme"
$ZipOut = Join-Path $PSScriptRoot "shinchan.zip"
$UserThemesDir = "$env:APPDATA\clawd-on-desk\themes\shinchan"
$BuiltinThemesDir = "E:\Work2\AI_Work\tool\clawd-on-desk\clawd-on-desk\clawd-on-desk\themes\shinchan"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " Syncing Shin-chan Theme to Clawd-on-Desk" -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan

# 1. Ensure theme.json is UTF-8 without BOM
$jsonPath = Join-Path $ThemeDir "theme.json"
if (Test-Path $jsonPath) {
    $bytes = [System.IO.File]::ReadAllBytes($jsonPath)
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        Write-Host "Stripping UTF-8 BOM from theme.json..." -ForegroundColor Yellow
        $cleanBytes = $bytes[3..($bytes.Length - 1)]
        [System.IO.File]::WriteAllBytes($jsonPath, $cleanBytes)
    }
}

# 2. Sync to User Themes Directory (%APPDATA%\clawd-on-desk\themes\shinchan)
if (-not (Test-Path $UserThemesDir)) {
    New-Item -ItemType Directory -Force -Path $UserThemesDir | Out-Null
}
Copy-Item -Path "$ThemeDir\*" -Destination $UserThemesDir -Recurse -Force
Write-Host "[OK] Synced to User Themes: $UserThemesDir" -ForegroundColor Green

# 3. Sync to Built-in Themes Directory (for dev runtime if present)
if (Test-Path (Split-Path -Parent $BuiltinThemesDir)) {
    if (-not (Test-Path $BuiltinThemesDir)) {
        New-Item -ItemType Directory -Force -Path $BuiltinThemesDir | Out-Null
    }
    Copy-Item -Path "$ThemeDir\*" -Destination $BuiltinThemesDir -Recurse -Force
    Write-Host "[OK] Synced to Built-in Themes: $BuiltinThemesDir" -ForegroundColor Green
}

# 4. Generate clean shinchan.zip for manual UI import
if (Test-Path $ZipOut) {
    Remove-Item -Path $ZipOut -Force
}
Compress-Archive -Path (Join-Path $ThemeDir "theme.json"), (Join-Path $ThemeDir "assets") -DestinationPath $ZipOut -Force
Write-Host "[OK] Generated Import Package: $ZipOut" -ForegroundColor Green

Write-Host "`n[Instructions]:" -ForegroundColor Yellow
Write-Host '1. Restart or focus Clawd-on-desk.'
Write-Host '2. Open Settings -> Theme.'
Write-Host "3. Select 'ShinChan' to enjoy working with Shin-chan!`n"
