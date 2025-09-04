# Oedipus React Frontend Setup Script
# This script sets up the React frontend with Node.js dependencies

Write-Host "=== Oedipus React Frontend Setup ===" -ForegroundColor Green
Write-Host ""

# Auto-detect project root and frontend path
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = $scriptDir
$frontendPath = Join-Path $projectRoot "react-frontend"

# Check if frontend directory exists
if (-not (Test-Path $frontendPath)) {
    Write-Host "React frontend directory not found at $frontendPath" -ForegroundColor Red
    Write-Host "Please run this script from the Oedipus project root directory." -ForegroundColor Yellow
    exit 1
}

Write-Host "Frontend path: $frontendPath" -ForegroundColor Green
Write-Host ""

# Set working directory to frontend
Set-Location $frontendPath

# Check Node.js installation
function Test-NodeInstallation {
    try {
        $nodeVersion = & node --version 2>$null
        $npmVersion = & npm --version 2>$null
        
        if ($nodeVersion -and $npmVersion) {
            $nodeVersion = $nodeVersion.Trim()
            $npmVersion = $npmVersion.Trim()
            if ($nodeVersion -and $npmVersion) {
                Write-Host "Node.js: $nodeVersion" -ForegroundColor Green
                Write-Host "npm: $npmVersion" -ForegroundColor Green
                return $true
            }
        }
    }
    catch {
    }
    
    # Try to find Node.js in common locations
    try {
        $nodePaths = @(
            "${env:ProgramFiles}\nodejs\node.exe",
            "${env:ProgramFiles(x86)}\nodejs\node.exe"
        )
        
        foreach ($nodePath in $nodePaths) {
            if (Test-Path $nodePath) {
                $testVersion = & $nodePath --version 2>$null
                if ($testVersion) {
                    $testVersion = $testVersion.Trim()
                    Write-Host "Node.js found at: $nodePath ($testVersion)" -ForegroundColor Green
                    $nodeDir = Split-Path $nodePath
                    if ($env:Path -notlike "*$nodeDir*") {
                        $env:Path = $nodeDir + ";" + $env:Path
                        Write-Host "Added Node.js to PATH for this session" -ForegroundColor Yellow
                    }
                    return $true
                }
            }
        }
    }
    catch {
    }
    
    return $false
}

$nodeInstalled = Test-NodeInstallation

if (-not $nodeInstalled) {
    Write-Host "Node.js not found. Please install Node.js:" -ForegroundColor Red
    Write-Host "1. Go to https://nodejs.org/" -ForegroundColor White
    Write-Host "2. Download and install the LTS version" -ForegroundColor White
    Write-Host "3. Restart PowerShell and run this script again" -ForegroundColor White
    exit 1
}

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow

try {
    npm install
    Write-Host "Dependencies installed successfully!" -ForegroundColor Green
}
catch {
    Write-Host "Failed to install dependencies. Please check your internet connection and try again." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Frontend setup completed!" -ForegroundColor Green
Write-Host ""
Write-Host "To start the frontend:" -ForegroundColor Cyan
Write-Host "  npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "Or from project root:" -ForegroundColor Cyan
Write-Host "  .\start_react_frontend.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Frontend will be available at: http://localhost:3000" -ForegroundColor White
Write-Host "Make sure the backend is running at: http://localhost:8000" -ForegroundColor Yellow