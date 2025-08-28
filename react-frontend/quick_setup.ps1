# Quick Setup Script - Bypasses Node.js detection issues
# Use this if the main setup script has PATH detection issues

param(
    [switch]$Force
)

Write-Host "=== Quick Setup for Oedipus React Frontend ===" -ForegroundColor Green
Write-Host ""

$frontendPath = "c:\Code\oedipus\react-frontend"

# Ensure we're in the right directory
if (-not (Test-Path $frontendPath)) {
    Write-Host "Error: Frontend directory not found at $frontendPath" -ForegroundColor Red
    exit 1
}

Set-Location $frontendPath

# Try to run node directly (assuming it's in PATH or will work)
Write-Host "Testing Node.js accessibility..." -ForegroundColor Yellow
try {
    $nodeTest = node --version
    Write-Host "✓ Node.js is accessible: $nodeTest" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not accessible via 'node' command" -ForegroundColor Red
    Write-Host ""
    Write-Host "Possible solutions:" -ForegroundColor Yellow
    Write-Host "1. Restart PowerShell as Administrator" -ForegroundColor White
    Write-Host "2. Add Node.js to PATH manually:" -ForegroundColor White
    Write-Host "   - Usually: C:\Program Files\nodejs" -ForegroundColor Gray
    Write-Host "3. Reinstall Node.js from https://nodejs.org/" -ForegroundColor White
    exit 1
}

# Install dependencies
Write-Host ""
Write-Host "Installing project dependencies..." -ForegroundColor Yellow

if ($Force -or -not (Test-Path "node_modules") -or -not (Test-Path "package-lock.json")) {
    try {
        npm install
        Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host ""
        Write-Host "Try running manually:" -ForegroundColor Yellow
        Write-Host "  npm cache clean --force" -ForegroundColor White
        Write-Host "  npm install" -ForegroundColor White
        exit 1
    }
} else {
    Write-Host "✓ Dependencies already installed (use -Force to reinstall)" -ForegroundColor Green
}

# Check if package.json exists and show available scripts
if (Test-Path "package.json") {
    Write-Host ""
    Write-Host "✓ Setup completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "To start the development server:" -ForegroundColor Cyan
    Write-Host "  npm run dev" -ForegroundColor White
    Write-Host ""
    Write-Host "Or use the startup script:" -ForegroundColor Cyan
    Write-Host "  .\start_react_frontend.ps1 -SkipNodeCheck" -ForegroundColor White
    Write-Host ""
    Write-Host "Available scripts:" -ForegroundColor Yellow
    Write-Host "  npm run dev      - Start development server" -ForegroundColor White
    Write-Host "  npm run build    - Build for production" -ForegroundColor White
    Write-Host "  npm run preview  - Preview production build" -ForegroundColor White
} else {
    Write-Host "✗ package.json not found - something went wrong" -ForegroundColor Red
    exit 1
}