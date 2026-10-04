@echo off
chcp 65001 > nul
title AI Coding Skill Manager

echo ========================================================
echo   🚀 AI Coding Skill Manager (AI Coding 技能管理器)
echo ========================================================
echo 正在检查运行环境...

if not exist ".venv" (
    echo [提示] 正在创建虚拟环境并安装依赖...
    where uv >nul 2>nul
    if %errorlevel% equ 0 (
        uv venv --python python .venv
        uv pip install --python .venv\Scripts\python.exe -r requirements.txt
    ) else (
        python -m venv .venv
        .\.venv\Scripts\pip install -r requirements.txt
    )
)

echo [提示] 正在启动管理服务...
start "" "http://127.0.0.1:8765"
.\.venv\Scripts\python.exe run.py
pause
