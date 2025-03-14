@echo off

:: Announce setup
echo Setting up application. Please wait.
echo Application will start automatically.

:: Print empty line and info line
echo.
echo Updating project libraries...

:: Check if updater.cmd exists at the correct location
if not exist "lib\updater.cmd" (
    echo updater.cmd not found in lib directory.
    exit /b
) 

cd lib

:: If updater.cmd exists, run it and show the output in the console
call updater.cmd || (
    echo Updater failed. Check the output above for details.
    echo Skipping to next steps...
)

:: Print empty line and info line
echo.
echo Installing packages...

cd ..

:: Install the project in editable mode (suppress output unless there's an error)
pip install -e . >nul 2>&1 || (
    echo Installation failed. Please try again. Exiting...
    pause
    exit /b
)

:: Print empty line and info line
echo.
echo Installing python libraries...
:: Install all required libraries for the project (suppress output unless there's an error)
pip install nltk >nul 2>&1 || (
    echo Library installation failed. Exiting...
    pause
    exit /b
)

:: Clear console so it stays clean
python -c "from GlobalAssets import clear_console; clear_console()"

:: Run the script (module) fol2.fol3.Class2
python -m GTWAssets.GameManager || (
    echo Python script failed. Exiting...
    pause
    exit /b
)

:: Pause to keep the terminal open (only if everything ran successfully)
pause