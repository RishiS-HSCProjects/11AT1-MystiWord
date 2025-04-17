@echo off

:: Set app title
python -c "from GlobalAssets import set_title; set_title('Starting')"

:: Print fancy title
python -c "from GlobalAssets import getTitle; print(getTitle())"

:: Announce setup
echo Setting up application. Please wait.
echo Application will start automatically.

:: Print empty line and info line
echo.
echo Installing python libraries...
:: Install all required libraries for the project (suppress output unless there's an error)
pip install nltk >nul 2>&1 || (
    echo Library installation failed. Exiting...
    goto ERROR_TITLE
)

:: Run the script (module)
python -m Main || (
    echo Python script failed. Exiting...
    goto ERROR_TITLE
)

:: Exit on quit
exit /b 0

:: Define error title
:ERROR_TITLE
python -c "from GlobalAssets import set_title; set_title('Error')"
pause
exit /b 1