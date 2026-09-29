# install-to-clawd.ps1
# 将机械少女桌面宠物主题一键安装到 Clawd-on-desk 用户主题目录

$targetDir = "$env:APPDATA\clawd-on-desk\themes\mechanical-girl1"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " Installing Mechanical Girl Theme to Clawd-on-Desk" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

New-Item -ItemType Directory -Force -Path $targetDir | Out-Null

$themeSource = Join-Path $PSScriptRoot "theme\*"
Copy-Item -Path $themeSource -Destination $targetDir -Recurse -Force

Write-Host "`n✓ 成功安装/同步机械少女主题至:" -ForegroundColor Green
Write-Host "  $targetDir" -ForegroundColor White

Write-Host "`n[操作指引]:" -ForegroundColor Yellow
Write-Host "1. 打开或重启 Clawd-on-desk"
Write-Host "2. 打开 设置 (Settings...) -> 主题 (Theme)"
Write-Host "3. 在主题下拉列表中选择 'Mechanical Girl' 即可与机械少女一同敲代码！`n"
