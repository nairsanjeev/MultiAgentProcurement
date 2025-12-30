# Setup Script for Procurement Agent System
# This script helps automate the initial setup process

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Procurement Agent System - Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.10 or higher." -ForegroundColor Red
    exit 1
}

# Check Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found. Please install Node.js 18 or higher." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setting up Backend..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Setup Backend
Set-Location backend

Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host "Installing Python dependencies (with --pre flag)..." -ForegroundColor Yellow
pip install -r requirements.txt --pre

Write-Host "Creating .env file from template..." -ForegroundColor Yellow
if (!(Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "✓ Created .env file. Please edit it with your Azure credentials." -ForegroundColor Green
} else {
    Write-Host "! .env file already exists. Skipping..." -ForegroundColor Yellow
}

Write-Host "✓ Backend setup complete!" -ForegroundColor Green
Write-Host ""

# Setup Frontend
Set-Location ../frontend

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setting up Frontend..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
npm install

Write-Host "Creating .env.local file from template..." -ForegroundColor Yellow
if (!(Test-Path .env.local)) {
    Copy-Item .env.local.example .env.local
    Write-Host "✓ Created .env.local file." -ForegroundColor Green
} else {
    Write-Host "! .env.local file already exists. Skipping..." -ForegroundColor Yellow
}

Write-Host "✓ Frontend setup complete!" -ForegroundColor Green
Write-Host ""

# Return to root
Set-Location ..

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Edit backend/.env with your Azure OpenAI credentials" -ForegroundColor White
Write-Host "2. Start the backend: cd backend && python main.py" -ForegroundColor White
Write-Host "3. In a new terminal, start the frontend: cd frontend && npm run dev" -ForegroundColor White
Write-Host "4. Open http://localhost:3000 in your browser" -ForegroundColor White
Write-Host ""
Write-Host "For detailed instructions, see:" -ForegroundColor Yellow
Write-Host "  - README.md for full documentation" -ForegroundColor White
Write-Host "  - QUICKSTART.md for quick start guide" -ForegroundColor White
Write-Host ""
Write-Host "Happy coding! 🚀" -ForegroundColor Cyan
