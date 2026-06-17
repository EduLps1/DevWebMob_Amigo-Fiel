$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $repoRoot ".venv\Scripts\python.exe"
$managePyDir = Join-Path $repoRoot "sistema"

if (-not (Test-Path $python)) {
    throw "Python da .venv nao encontrado em $python"
}

if (-not (Test-Path (Join-Path $repoRoot ".env"))) {
    Write-Host "Aviso: arquivo .env nao encontrado na raiz do projeto." -ForegroundColor Yellow
    Write-Host "Crie um .env baseado em .env.example antes de rodar migrate/runserver." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Django vai escutar em 0.0.0.0:8000" -ForegroundColor Cyan
Write-Host "Abra no PC:      http://127.0.0.1:8000/" -ForegroundColor Green
Write-Host "Abra pela rede:  http://10.90.8.79:8000/" -ForegroundColor Green
Write-Host ""

Set-Location $managePyDir
& $python manage.py runserver 0.0.0.0:8000
