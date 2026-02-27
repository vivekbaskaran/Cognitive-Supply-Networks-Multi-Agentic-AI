@echo off
REM Navigate to the agent directory
cd /d "%~dp0\..\backend" || exit /b 1

uv sync
