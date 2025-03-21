@REM :: Marker Disclaimer: All contents of this file have been AI-generated
@REM :: Updates the required APIs directly from GitHub.

@REM @echo off
@REM setlocal enabledelayedexpansion

@REM :: Check if there is an active internet connection (WiFi)
@REM ping -n 1 google.com >nul 2>&1
@REM if %ERRORLEVEL% neq 0 (
@REM     echo No internet connection detected. Please ensure your WiFi is connected. >&2
@REM     exit /b 1
@REM )

@REM :: Check if the script has write permissions in the current directory
@REM echo Test > test_permission.txt
@REM if exist test_permission.txt (
@REM     del test_permission.txt
@REM ) else (
@REM     echo Insufficient permissions to write in this directory. Please check your permissions. >&2
@REM     exit /b 1
@REM )

@REM :: Check if Git is installed
@REM where git >nul 2>nul
@REM if %ERRORLEVEL% neq 0 (
@REM     echo Git is not installed or not in the system PATH. Please install Git before running this script. >&2
@REM     exit /b 1
@REM )

@REM :: Clone repositories and retain only necessary files
@REM call :CloneAndClean "https://github.com/PyAPIs/libData" "libData" "DataManager.py"
@REM call :CloneAndClean "https://github.com/PyAPIs/libForms" "libForms" "Form.py"

@REM :: Exits the script here on success
@REM exit /b

@REM :: Function to delete, clone, and clean a repository
@REM :CloneAndClean
@REM :: Check if a folder already exists and delete it
@REM if exist %2 (
@REM     rd /s /q %2
@REM )

@REM :: Clone the repository
@REM git clone %1 %2 >nul 2>&1
@REM if %ERRORLEVEL% neq 0 (
@REM     echo Git clone failed for %1. Exiting function.
@REM     exit /b 1
@REM )