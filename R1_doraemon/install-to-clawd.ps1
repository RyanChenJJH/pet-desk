# install-to-clawd.ps1
# 将机器猫桌面宠物主题一键安装到 Clawd-on-desk 用户主题目录

$targetDir = "$env:APPDATA\clawd-on-desk\themes\doraemon"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " Installing Doraemon Theme to Clawd-on-Desk" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# 确保目标目录存在
New-Item -ItemType Directory -Force -Path $targetDir | Out-Null

# 复制 theme.json 与 assets 目录
$themeSource = Join-Path $PSScriptRoot "theme\*"
Copy-Item -Path $themeSource -Destination $targetDir -Recurse -Force

Write-Host "`n✓ 成功安装/同步主题至:" -ForegroundColor Green
Write-Host "  $targetDir" -ForegroundColor White

Write-Host "`n[操作指引]:" -ForegroundColor Yellow
Write-Host "1. 打开或重启 Clawd-on-desk"
Write-Host "2. 打开 设置 (Settings...) -> 主题 (Theme)"
Write-Host "3. 在主题下拉列表中选择 'Doraemon' 即可与机器猫一同工作！`n"
