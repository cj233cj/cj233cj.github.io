@echo off
REM Double-click launcher for timeline_post_tui.py on Windows.
REM Keeps the console window open so you can read any error messages.

cd /d "%~dp0"

where uv >nul 2>nul
if errorlevel 1 (
    echo uv was not found on your PATH.
    echo Install it from https://docs.astral.sh/uv/getting-started/installation/
    echo then run this file again.
    pause
    exit /b 1
)

uv run timeline_post_tui.py

echo.
echo (window closed - press any key to exit)
pause >nul
