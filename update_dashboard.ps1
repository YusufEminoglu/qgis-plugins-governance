# QGIS Plugins Analytics & Governance Dashboard Updater
# Author: Yusuf Eminoğlu

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " QGIS Plugin Analytics & Governance Dashboard Updater " -ForegroundColor Yellow -BackgroundColor Black
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Run Python Script
Write-Host "[1/3] Fetching live metrics & updating audit history..." -ForegroundColor Gray
if (Get-Command "py" -ErrorAction SilentlyContinue) {
    & py generate_dashboard.py
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Python script execution failed!"
        Exit 1
    }
} elseif (Get-Command "python" -ErrorAction SilentlyContinue) {
    & python generate_dashboard.py
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Python script execution failed!"
        Exit 1
    }
} else {
    Write-Error "Python executable ('py' or 'python') was not found in system PATH!"
    Exit 1
}

# Step 2: Verify HTML was generated
$HtmlFile = Join-Path $ScriptDir "qgis_plugins_dashboard.html"
if (-Not (Test-Path $HtmlFile)) {
    Write-Error "Dashboard HTML file could not be generated!"
    Exit 1
}

# Step 3: Copy to User's Downloads Directory
Write-Host "[2/3] Exporting latest dashboard to Downloads directory..." -ForegroundColor Gray
$DownloadsDir = [System.IO.Path]::Combine([System.Environment]::GetFolderPath('UserProfile'), 'Downloads')
$DestinationPath = Join-Path $DownloadsDir "qgis_plugins_dashboard.html"

try {
    Copy-Item -Path $HtmlFile -Destination $DestinationPath -Force
    Write-Host "[3/3] Export Successful!" -ForegroundColor Green
    Write-Host ""
    Write-Host "==========================================================" -ForegroundColor Green
    Write-Host " SYNCHRONIZATION COMPLETE! " -ForegroundColor Green -BackgroundColor Black
    Write-Host "==========================================================" -ForegroundColor Green
    Write-Host "Updated Dashboard File Path:" -ForegroundColor Gray
    Write-Host "$DestinationPath" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To launch the dashboard in your browser, run:" -ForegroundColor Gray
    Write-Host "Start-Process `"$DestinationPath`"" -ForegroundColor Cyan
    Write-Host "==========================================================" -ForegroundColor Green
} catch {
    Write-Error "Failed to copy file to Downloads directory: $_"
    Exit 1
}
