@echo off
setlocal enabledelayedexpansion

echo ============================================
echo Network Kill Switch - Installer Build Script
echo ============================================
echo.

:: Check for Python
echo [1/6] Checking for Python...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python and try again.
    echo.
    pause
    exit /b 1
)
echo Python found.
echo.

:: Install/Upgrade PyInstaller
echo [2/6] Installing/Upgrading PyInstaller...
pip install --upgrade pyinstaller
if %errorLevel% neq 0 (
    echo ERROR: Failed to install PyInstaller!
    echo.
    pause
    exit /b 1
)
echo PyInstaller ready.
echo.

:: Install dependencies (just in case)
echo [3/6] Installing application dependencies...
pip install -r requirements.txt
if %errorLevel% neq 0 (
    echo WARNING: Failed to install some dependencies, continuing anyway...
)
echo.

:: Build executable with PyInstaller
echo [4/6] Building standalone executable with PyInstaller...
echo This may take a few minutes...
echo.

:: Check if spec file exists
if exist NetworkKillSwitch.spec (
    echo Using existing spec file: NetworkKillSwitch.spec
    pyinstaller --clean NetworkKillSwitch.spec
) else (
    :: Fallback to basic build if spec file is missing
    if exist icon.ico (
        echo Using icon file: icon.ico
        pyinstaller --onefile --windowed --name "NetworkKillSwitch" --icon="icon.ico" --add-data "icons/status_on.ico;icons" --add-data "icons/status_off.ico;icons" network_kill_switch.py
    ) else (
        echo No icon file found, building without icon...
        pyinstaller --onefile --windowed --name "NetworkKillSwitch" --add-data "icons/status_on.ico;icons" --add-data "icons/status_off.ico;icons" network_kill_switch.py
    )
)

if %errorLevel% neq 0 (
    echo ERROR: PyInstaller build failed!
    echo.
    pause
    exit /b 1
)

if not exist "dist\NetworkKillSwitch.exe" (
    echo ERROR: NetworkKillSwitch.exe was not created!
    echo.
    pause
    exit /b 1
)

echo Executable built successfully: dist\NetworkKillSwitch.exe
echo.

:: Check for Inno Setup
echo [5/6] Checking for Inno Setup...
set ISCC_PATH=

:: Check common Inno Setup installation paths
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    set "ISCC_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    set "ISCC_PATH=C:\Program Files\Inno Setup 6\ISCC.exe"
) else if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" (
    set "ISCC_PATH=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
) else if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" (
    set "ISCC_PATH=%ProgramFiles%\Inno Setup 6\ISCC.exe"
)

if "!ISCC_PATH!"=="" (
    echo WARNING: Inno Setup not found!
    echo.
    echo Inno Setup is required to create the installer.
    echo Please download and install it from: https://jrsoftware.org/isinfo.php
    echo.
    echo The standalone executable has been created in the 'dist' folder.
    echo You can distribute dist\NetworkKillSwitch.exe directly, but it won't have
    echo an installer wizard or automatic uninstall capability.
    echo.
    pause
    exit /b 0
)

echo Found Inno Setup at: !ISCC_PATH!
echo.

:: Build installer with Inno Setup
echo [6/6] Building installer with Inno Setup...
"!ISCC_PATH!" installer.iss

if %errorLevel% neq 0 (
    echo ERROR: Inno Setup compilation failed!
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo BUILD SUCCESSFUL!
echo ============================================
echo.
echo Standalone executable: dist\NetworkKillSwitch.exe
echo Installer package:     Output\NetworkKillSwitch-Setup.exe
echo.
echo You can distribute the installer to users.
echo The installer is approximately 20-30 MB and includes everything needed.
echo.
pause
