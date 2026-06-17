$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$mobileDir = Join-Path $repoRoot "mobile"

Write-Host ""
Write-Host "Ionic vai escutar em 0.0.0.0:8100" -ForegroundColor Cyan
Write-Host "Abra no PC:      http://localhost:8100/" -ForegroundColor Green
Write-Host "Abra no celular: http://10.90.8.79:8100/" -ForegroundColor Green
Write-Host ""

Set-Location $mobileDir
& npm.cmd start
