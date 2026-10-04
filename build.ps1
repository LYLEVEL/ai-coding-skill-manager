# PowerShell build script for Antigravity Skill Manager
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " [*] AI Coding Skill Manager Build Script" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$ScriptDir = $PSScriptRoot
if (-not $ScriptDir) {
    $ScriptDir = (Get-Location).Path
}
Set-Location $ScriptDir

$PyInstaller = Join-Path $ScriptDir ".venv\Scripts\pyinstaller.exe"
if (-not (Test-Path $PyInstaller)) {
    $PyInstaller = (Get-Command pyinstaller -ErrorAction SilentlyContinue).Source
}

if (-not $PyInstaller) {
    Write-Error "PyInstaller not found in virtualenv or PATH!"
    exit 1
}

Write-Host "`n[1/3] Compiling application with PyInstaller..." -ForegroundColor Yellow
& $PyInstaller AICodingSkillManager.spec --clean -y
if ($LASTEXITCODE -ne 0) {
    Write-Error "PyInstaller build failed!"
    exit $LASTEXITCODE
}
Write-Host " PyInstaller completed: dist\AICodingSkillManager" -ForegroundColor Green

Write-Host "`n[2/3] Checking Inno Setup compiler..." -ForegroundColor Yellow
$ISCC = $null
$ISCC_Paths = @(
    "ISCC.exe",
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
    "C:\Program Files\Inno Setup 6\ISCC.exe",
    "C:\ProgramData\chocolatey\bin\ISCC.exe"
)

foreach ($p in $ISCC_Paths) {
    if (Get-Command $p -ErrorAction SilentlyContinue) {
        $ISCC = (Get-Command $p).Source
        break
    } elseif (Test-Path $p) {
        $ISCC = $p
        break
    }
}

if (-not $ISCC) {
    Write-Warning "ISCC.exe not found, skipping installer creation."
    exit 0
}

Write-Host " Found Inno Setup: $ISCC" -ForegroundColor Green
Write-Host "`n[3/3] Generating Windows Installer (Setup.exe)..." -ForegroundColor Yellow

$IssPath = Join-Path $ScriptDir "installer\setup.iss"
& $ISCC $IssPath
if ($LASTEXITCODE -ne 0) {
    Write-Error "Inno Setup compilation failed!"
    exit $LASTEXITCODE
}

$DistInstaller = Join-Path $ScriptDir "dist_installer"
$SetupFiles = Get-ChildItem -Path $DistInstaller -Filter "*.exe" -ErrorAction SilentlyContinue

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host " BUILD SUCCESSFUL!" -ForegroundColor Green
foreach ($f in $SetupFiles) {
    $size = [math]::Round($f.Length / 1MB, 2)
    Write-Host (" Installer: " + $f.FullName + " (" + $size + " MB)") -ForegroundColor Cyan
}
Write-Host "==========================================================" -ForegroundColor Green
