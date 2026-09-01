@echo off
title Nalanda University Faculty Directory - Data Pipeline
cd /d "%~dp0"
echo ================================================================
echo   Running Nalanda University Faculty Data Pipeline...
echo ================================================================
echo.
".venv\Scripts\python.exe" -m src.pipeline
echo.
echo Pipeline completed!
pause
