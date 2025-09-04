# Oedipus Backend Setup Script
# This script sets up the Python backend with Docker services

param(
    [switch]$SkipDocker
)

Write-Host "=== Oedipus Backend Setup ===" -ForegroundColor Green
Write-Host ""

# Auto-detect project root
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = $scriptDir

# Verify we're in the correct directory
$requiredFiles = @("requirements.txt", "alembic.ini")
$missingFiles = @()

foreach ($file in $requiredFiles) {
    if (-not (Test-Path (Join-Path $projectRoot $file))) {
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host "Project root not detected correctly." -ForegroundColor Red
    Write-Host "Missing files: $($missingFiles -join ', ')" -ForegroundColor Red
    Write-Host "Please run this script from the Oedipus project root directory." -ForegroundColor Yellow
    exit 1
}

Write-Host "Project root detected: $projectRoot" -ForegroundColor Green
Write-Host ""

# Set working directory to project root
Set-Location $projectRoot

# Check Python
$pythonCheck = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCheck) {
    $pythonVersion = & python --version
    Write-Host "Python: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "Python not found. Please install Python 3.11+ and add to PATH" -ForegroundColor Red
    exit 1
}

# Install Python dependencies
Write-Host ""
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
try {
    & pip install -r requirements.txt
    Write-Host "Python dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "Failed to install Python dependencies" -ForegroundColor Red
    exit 1
}

if (-not $SkipDocker) {
    # Check Docker
    Write-Host ""
    Write-Host "Checking Docker..." -ForegroundColor Yellow
    $dockerCheck = Get-Command docker -ErrorAction SilentlyContinue
    if ($dockerCheck) {
        $dockerVersion = & docker --version
        Write-Host "Docker: $dockerVersion" -ForegroundColor Green
        
        # Start Docker services
        Write-Host ""
        Write-Host "Starting Docker services..." -ForegroundColor Yellow
        try {
            & docker compose up -d
            Write-Host "Docker services started" -ForegroundColor Green
            
            # Wait for services to be ready
            Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
            Start-Sleep -Seconds 10
            
            # Initialize database
            Write-Host ""
            Write-Host "Initializing database..." -ForegroundColor Yellow
            & alembic upgrade head
            Write-Host "Database initialized" -ForegroundColor Green
        } catch {
            Write-Host "Failed to start Docker services or initialize database" -ForegroundColor Red
            Write-Host "You may need to start Docker Desktop and try again" -ForegroundColor Yellow
        }
    } else {
        Write-Host "Docker not found" -ForegroundColor Red
        Write-Host "Please install Docker Desktop: https://www.docker.com/products/docker-desktop" -ForegroundColor Cyan
        Write-Host "Or run with -SkipDocker flag to setup without Docker" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Backend setup completed!" -ForegroundColor Green
Write-Host ""
Write-Host "To start the backend:" -ForegroundColor Cyan
Write-Host "  python scripts\start_backend.py" -ForegroundColor White
Write-Host ""
Write-Host "To start the worker (in another terminal):" -ForegroundColor Cyan
Write-Host "  python scripts\start_worker.py" -ForegroundColor White
Write-Host ""
Write-Host "API will be available at: http://localhost:8000" -ForegroundColor White
Write-Host "API docs at: http://localhost:8000/docs" -ForegroundColor White