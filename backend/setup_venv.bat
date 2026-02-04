@echo off
REM AI Native 研发平台 - Virtual Environment Setup Script for Windows

echo Creating virtual environment...
python -m venv .venv

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo Virtual environment setup complete!
echo ========================================
echo.
echo To activate the virtual environment:
echo   .venv\Scripts\activate.bat
echo.
echo To deactivate:
echo   deactivate
echo.
