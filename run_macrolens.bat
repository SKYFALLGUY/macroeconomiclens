@echo off
title MacroLens - Indian Macroeconomic Assistant
echo ========================================================
echo        Starting MacroLens Indian Macro Assistant
echo ========================================================
echo.

cd /d "%~dp0"

if not exist ".venv\Scripts\streamlit.exe" (
    echo [ERROR] Virtual environment not found!
    echo Please make sure the .venv folder exists.
    pause
    exit /b 1
)

echo Launching MacroLens Dashboard in your web browser...
echo.
echo URL: http://localhost:8501
echo (Press Ctrl+C in this window to stop the server)
echo.

.\.venv\Scripts\streamlit.exe run app.py

pause
