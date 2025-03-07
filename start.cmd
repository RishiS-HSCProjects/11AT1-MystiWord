:: Marker Disclaimer: All contents of this file have been AI-generated
:: Starts project.

@echo off

:: Announce setup
echo Setting up application. Please wait.
echo Application will start automatically.

:: Print empty line and info line
echo.
echo Updating libraries...
@echo off

:: Install the project in editable mode (suppress output unless there's an error)
pip install -e . >nul 2>&1 || (
    echo Installation failed. Exiting...
    pause
    exit /b
)

:: Clear console so it stays clean
cls

:: Run the script (module) fol2.fol3.Class2
python -m GTWAssets.GameManager || (
    echo Python script failed. Exiting...
    pause
    exit /b
)

:: Pause to keep the terminal open (only if everything ran successfully)
pause