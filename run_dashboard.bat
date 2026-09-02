@echo off
title Nalanda University Faculty Directory - Streamlit App
cd /d "%~dp0"
echo ================================================================
echo   Launching Nalanda University Academic Faculty Directory...
echo ================================================================
echo.
".venv\Scripts\streamlit.exe" run streamlit_app.py
pause
