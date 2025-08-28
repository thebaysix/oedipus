# Oedipus React Frontend Setup Script
Write-Host "=== Oedipus React Frontend Setup ===" -ForegroundColor Green
Write-Host ""

function Test-NodeInstallation {
    try {
        $nodeVersion = & node --version 2>$null
        $npmVersion = & npm --version 2>$null
        
        if ($nodeVersion -and $npmVersion) {
            $nodeVersion = $nodeVersion.Trim()
            $npmVersion = $npmVersion.Trim()
            if ($nodeVersion -and $npmVersion) {
                Write-Host "✓ Node.js: $nodeVersion" -ForegroundColor Green
                Write-Host "✓ npm: $npmVersion" -ForegroundColor Green
                return $true
            }
        }
    }
    catch {
    }
    
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
                    Write-Host "✓ Node.js found at: $nodePath ($testVersion)" -ForegroundColor Green
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
    Write-Host "Node.js not found. Installing Node.js..." -ForegroundColor Yellow
    
    try {
        choco --version | Out-Null
        Write-Host "Installing Node.js via Chocolatey..." -ForegroundColor Yellow
        $chocoResult = choco install nodejs -y 2>&1
        
        if ($LASTEXITCODE -eq 0 -or $chocoResult -match "already installed") {
            Write-Host "Node.js installation completed or was already present." -ForegroundColor Green
            Write-Host "Refreshing environment variables..." -ForegroundColor Yellow
            $machinePath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
            $userPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
            $env:Path = $machinePath + ";" + $userPath
            Start-Sleep -Seconds 2
        }
        else {
            Write-Host "Chocolatey installation returned an error, but continuing..." -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "Chocolatey not found. Please install Node.js manually:" -ForegroundColor Red
        Write-Host "1. Go to https://nodejs.org/" -ForegroundColor White
        Write-Host "2. Download and install the LTS version" -ForegroundColor White
        exit 1
    }
}

Write-Host "Verifying Node.js installation..." -ForegroundColor Yellow
$maxAttempts = 3
$attempt = 1

while ($attempt -le $maxAttempts) {
    if (Test-NodeInstallation) {
        $nodeInstalled = $true
        break
    }
    else {
        Write-Host "Attempt $attempt of $maxAttempts - Node.js not detected, waiting..." -ForegroundColor Yellow
        Start-Sleep -Seconds 3
        $machinePath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
        $userPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
        $env:Path = $machinePath + ";" + $userPath
        $attempt++
    }
}

if (-not $nodeInstalled) {
    Write-Host "Node.js installation verification failed after $maxAttempts attempts." -ForegroundColor Red
    Write-Host "This might be a PATH issue. Please try:" -ForegroundColor Yellow
    Write-Host "1. Close and reopen PowerShell" -ForegroundColor White
    Write-Host "2. Run node --version manually to verify" -ForegroundColor White
    exit 1
}

Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
Set-Location "c:\Code\oedipus\react-frontend"

try {
    npm install
    Write-Host "Dependencies installed successfully!" -ForegroundColor Green
}
catch {
    Write-Host "Failed to install dependencies. Please check your internet connection and try again." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Green
Write-Host "To start: npm run dev" -ForegroundColor Cyan
Write-Host "Available at: http://localhost:3000" -ForegroundColor White
Write-Host "Backend needed: http://localhost:8000" -ForegroundColor Yellow
