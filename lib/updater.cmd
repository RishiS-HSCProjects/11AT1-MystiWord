:: Marker Disclaimer: All contents of this file have been AI-generated
:: Updates the required APIs directly from GitHub.

:: ignore script
exit /b 0 
@echo off
setlocal enabledelayedexpansion

:: Function to check if there is an active internet connection (WiFi)
:CheckWiFi
ping -n 1 google.com >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo No internet connection detected. Please ensure your WiFi is connected. >&2
    exit /b 1
)
exit /b 0

:: Function to check if the script has write permissions in the current directory
:CheckPermissions
echo Checking write permissions...
echo Test > test_permission.txt
if exist test_permission.txt (
    del test_permission.txt
) else (
    echo Insufficient permissions to write in this directory. Please check your permissions. >&2
    exit /b 1
)
exit /b 0

:: Check if Git is installed
where git >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Git is not installed or not in the system PATH. Please install Git before running this script. >&2
    exit /b 1
)

:: Check WiFi connection and permissions before proceeding
call :CheckWiFi
call :CheckPermissions

:: Define the base directory where the repositories will be cloned

:: Clone repositories and retain only necessary files
call :CloneAndClean "https://github.com/PyAPIs/libData" "libData" "DataManager.py"
call :CloneAndClean "https://github.com/PyAPIs/libForms" "libForms" "Form.py"
exit /b 0

:: Function to delete, clone, and clean a repository
:CloneAndClean
:: Delete existing folder if it exists
if exist %2 (
    rd /s /q %2
)

:: Clone the repository
git clone %1 %2 >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Git clone failed for %1. Please check if Git installed, you have an active connection, and this program has permission to create and remove files. >&2
    exit /b 1
)
exit /b 0