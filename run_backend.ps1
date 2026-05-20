Write-Host "Starting Movie Recommender Backend..." -ForegroundColor Green

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Python is not installed" -ForegroundColor Red
    exit 1
}

Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)

if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

& .\venv\Scripts\Activate.ps1

Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -q -r requirements.txt

Write-Host "Backend starting on http://localhost:8000" -ForegroundColor Green

python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
