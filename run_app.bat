@echo off
title RAG Document Assistant Launcher
cls
echo ============================================================
echo   Starting Streamlit RAG Document Assistant UI...
echo ============================================================
echo.

cd /d "%~dp0"

if exist "venv\Scripts\streamlit.exe" (
    echo [OK] Using virtual environment Streamlit...
    "venv\Scripts\streamlit.exe" run app.py
) else if exist "venv\Scripts\python.exe" (
    echo [OK] Using virtual environment Python...
    "venv\Scripts\python.exe" -m streamlit run app.py
) else (
    echo [WARNING] venv not found, using system Python...
    python -m streamlit run app.py
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Failed to start Streamlit. Please ensure dependencies are installed.
    pause
)
