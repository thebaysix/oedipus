# Oedipus React Frontend Startup Script
# This script checks prerequisites and starts the React development server

param(
    [switch]$SkipNodeCheck,
    [switch]$Install,
    [switch]$Build
)

Write-Host "=== Oedipus React Frontend Starter ===" -ForegroundColor Green
Write-Host ""

# Get the script directory and construct the frontend path dynamically
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$frontendPath = Join-Path $scriptDir "react-frontend"

# Check if frontend directory exists
if (-not (Test-Path $frontendPath)) {
    Write-Host "Error: React frontend directory not found at $frontendPath" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please ensure you're running this script from the Oedipus project root directory." -ForegroundColor Yellow
    Write-Host "The project root should contain:" -ForegroundColor Yellow
    Write-Host "  - react-frontend/ directory" -ForegroundColor White
    Write-Host "  - requirements.txt" -ForegroundColor White
    Write-Host "  - docker-compose.yml" -ForegroundColor White
    Write-Host ""
    Write-Host "Current script location: $scriptDir" -ForegroundColor Gray
    exit 1
}

Set-Location $frontendPath

# Check Node.js installation
if (-not $SkipNodeCheck) {
    try {
        $nodeVersion = & node --version 2>$null
        $npmVersion = & npm --version 2>$null
        
        if ($nodeVersion -and $npmVersion) {
            Write-Host "✓ Node.js: $nodeVersion" -ForegroundColor Green
            Write-Host "✓ npm: $npmVersion" -ForegroundColor Green
        } else {
            throw "Node.js not found"
        }
    } catch {
        Write-Host "✗ Node.js not detected in PATH" -ForegroundColor Yellow
        Write-Host ""
        
        # Try to detect Node.js in common locations
        $commonPaths = @(
            "${env:ProgramFiles}\nodejs\node.exe",
            "${env:ProgramFiles(x86)}\nodejs\node.exe",
            "$env:APPDATA\npm\node.exe"
        )
        
        $nodeFound = $false
        foreach ($path in $commonPaths) {
            if (Test-Path $path) {
                Write-Host "Found Node.js at: $path" -ForegroundColor Green
                Write-Host "This might be a PATH environment variable issue." -ForegroundColor Yellow
                $nodeFound = $true
                break
            }
        }
        
        if (-not $nodeFound) {
            Write-Host "Node.js not found. Please install Node.js:" -ForegroundColor Red
            Write-Host "1. Visit https://nodejs.org/" -ForegroundColor White
            Write-Host "2. Download and install the LTS version" -ForegroundColor White
            Write-Host "3. Restart PowerShell and try again" -ForegroundColor White
            Write-Host ""
            Write-Host "Or run the setup script: .\setup.ps1" -ForegroundColor Cyan
        } else {
            Write-Host ""
            Write-Host "To fix the PATH issue:" -ForegroundColor Yellow
            Write-Host "1. Close and reopen PowerShell as Administrator" -ForegroundColor White
            Write-Host "2. Run: .\setup.ps1" -ForegroundColor White  
            Write-Host "3. Or restart your computer to refresh environment variables" -ForegroundColor White
            Write-Host ""
            Write-Host "To bypass this check (if Node.js is working): .\start_react_frontend.ps1 -SkipNodeCheck" -ForegroundColor Cyan
        }
        exit 1
    }
}

# Install dependencies if requested or package-lock.json doesn't exist
if ($Install -or -not (Test-Path "node_modules") -or -not (Test-Path "package-lock.json")) {
    Write-Host ""
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    try {
        npm install
        Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
}

# Build if requested
if ($Build) {
    Write-Host ""
    Write-Host "Building application..." -ForegroundColor Yellow
    try {
        npm run build
        Write-Host "✓ Build completed successfully" -ForegroundColor Green
        Write-Host "Build output available in: $frontendPath\dist" -ForegroundColor Cyan
    } catch {
        Write-Host "✗ Build failed" -ForegroundColor Red
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
    exit 0
}

# Check if backend is running
Write-Host ""
Write-Host "Checking backend connection..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Backend is running at http://localhost:8000" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠ Backend not responding at http://localhost:8000" -ForegroundColor Yellow
    Write-Host "Make sure to start the Oedipus backend before using the frontend" -ForegroundColor White
    Write-Host ""
    Write-Host "To start the backend:" -ForegroundColor Cyan
    Write-Host "  cd $scriptDir" -ForegroundColor White
    Write-Host "  python scripts\start_backend.py" -ForegroundColor White
}

# Start development server
Write-Host ""
Write-Host "Starting React development server..." -ForegroundColor Green
Write-Host "The application will open at http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

try {
    npm run dev
} catch {
    Write-Host "✗ Failed to start development server" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Make sure port 3000 is not in use" -ForegroundColor White
    Write-Host "2. Try deleting node_modules and running with -Install flag" -ForegroundColor White
    Write-Host "3. Check if all dependencies installed correctly" -ForegroundColor White
    
    exit 1
}
