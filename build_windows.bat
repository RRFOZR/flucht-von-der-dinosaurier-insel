@echo off
REM Build script for Windows
REM Creates standalone .exe file

echo ====================================
echo Building Dinosaur Island for Windows
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Clean previous builds
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

REM Build executable
echo.
echo Building executable...
pyinstaller DinosaurIsland.spec

REM Check if build succeeded
if exist "dist\DinosaurIsland.exe" (
    echo.
    echo ====================================
    echo SUCCESS! Executable created:
    echo dist\DinosaurIsland.exe
    echo ====================================
    echo.
    echo You can now distribute dist\DinosaurIsland.exe
    echo No Python installation needed on target machine!
) else (
    echo.
    echo ERROR: Build failed!
    echo Check error messages above
)

pause
