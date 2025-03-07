:: Marker Disclaimer: All contents of this file have been AI-generated
:: Updates the required APIs directly from GitHub.

@echo off
setlocal enabledelayedexpansion

:: Check if Git is installed
where git >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Git is not installed or not in the system PATH. Please install Git before running this script. >&2
    exit /b 1
)

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
    echo Git clone failed for %1. Please check you have Git installed and permissions. >&2
    exit /b 1
)
exit /b 0