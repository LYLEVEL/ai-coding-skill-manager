# PowerShell 启动脚本
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  🚀 AI Coding Skill Manager (AI Coding 技能管理器)" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan

if (-not (Test-Path ".venv")) {
    Write-Host "[提示] 正在使用 uv 创建虚拟环境并安装依赖..." -ForegroundColor Yellow
    if (Get-Command uv -ErrorAction SilentlyContinue) {
        uv venv .venv
        uv pip install --python .venv\Scripts\python.exe -r requirements.txt
    } else {
        python -m venv .venv
        .\.venv\Scripts\pip install -r requirements.txt
    }
}

Start-Process "http://127.0.0.1:8765"
& ".\.venv\Scripts\python.exe" run.py
