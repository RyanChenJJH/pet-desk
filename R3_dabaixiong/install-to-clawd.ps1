# install-to-clawd.ps1
# Sync Dabaixiong theme to Clawd-on-desk and create clean import zip

$ErrorActionPreference = "Stop"
$ThemeDir = Join-Path $PSScriptRoot "theme"
$ZipOut = Join-Path $PSScriptRoot "dabaixiong.zip"
$UserThemesDir = "$env:APPDATA\clawd-on-desk\themes\dabaixiong"
$BuiltinThemesDir = "E:\Work2\AI_Work\tool\clawd-on-desk\clawd-on-desk\clawd-on-desk\themes\dabaixiong"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " Syncing Dabaixiong Theme to Clawd" -ForegroundColor Yellow
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

# 2. Sync to User Themes Directory (%APPDATA%\clawd-on-desk\themes\dabaixiong)
if (-not (Test-Path $UserThemesDir)) {
    New-Item -ItemType Directory -Force -Path $UserThemesDir | Out-Null
}
Copy-Item -Path "$ThemeDir\*" -Destination $UserThemesDir -Recurse -Force
Write-Host "[OK] Synced to User Themes: $UserThemesDir" -ForegroundColor Green

# 3. Sync to Built-in Themes Directory (for dev runtime)
if (-not (Test-Path $BuiltinThemesDir)) {
    New-Item -ItemType Directory -Force -Path $BuiltinThemesDir | Out-Null
}
Copy-Item -Path "$ThemeDir\*" -Destination $BuiltinThemesDir -Recurse -Force
Write-Host "[OK] Synced to Built-in Themes: $BuiltinThemesDir" -ForegroundColor Green

# 4. Generate clean dabaixiong.zip for manual UI import
if (Test-Path $ZipOut) {
    Remove-Item $ZipOut -Force
}
Compress-Archive -Path "$ThemeDir\*" -DestinationPath $ZipOut -Force
Write-Host "[OK] Created clean package: $ZipOut" -ForegroundColor Green

Write-Host "`nAll synced successfully! You can switch to 'Dabaixiong' in Clawd-on-desk now." -ForegroundColor Cyan
