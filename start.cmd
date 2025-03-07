@echo off

:: Announce setup
echo Setting up application. Please wait.
echo Application will start automatically.

:: Install the project in editable mode (suppress output unless there's an error)
pip install -e . >nul 2>&1 || (
    echo ""
    echo Installation failed. Exiting...
    pause
    exit /b
)

:: Clear console so it stays clean
cls

:: Run the main script
python -m REPLACE_THIS_FOR_SCRIPT || (
    echo Python script failed. Exiting...
    pause
    exit /b
)

:: Pause to keep the terminal open (only if everything ran successfully)
pause