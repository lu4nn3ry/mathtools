#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Start the FastAPI backend in development mode for Tauri sidecar.
.DESCRIPTION
    This script is used by Tauri in dev mode (--dev-sidecar flag).
    It launches uvicorn directly from the Python source so you get
    hot-reload during development. Run this instead of the PyInstaller
    binary when working locally.
.EXAMPLE
    .\scripts\dev-sidecar.ps1
#>

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSCommandPath)

Write-Host "[sidecar-dev] Starting FastAPI backend on http://localhost:8080" -ForegroundColor Cyan

# Ensure dependencies are installed
pip install -q -r "$ProjectRoot\backend\requirements.txt"

# Add Lean/elan to PATH if available
$elanBin = "$env:USERPROFILE\.elan\bin"
if (Test-Path $elanBin) {
    $env:PATH = "$elanBin;$env:PATH"
}

# Add Typst to PATH if available (winget installs here)
$typstDir = "$env:LOCALAPPDATA\Microsoft\WinGet\Packages\Typst.Typst_Microsoft.Winget.Source_8wekyb3d8bbwe\typst-x86_64-pc-windows-msvc"
if (Test-Path $typstDir) {
    $env:PATH = "$typstDir;$env:PATH"
}

# Launch uvicorn with reload enabled
& python -m uvicorn backend.main:app `
    --host 127.0.0.1 `
    --port 8080 `
    --reload `
    --log-level info

if ($LASTEXITCODE -ne 0) {
    Write-Error "[sidecar-dev] Backend exited with code $LASTEXITCODE"
    exit $LASTEXITCODE
}
