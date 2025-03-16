@echo off
echo [%date% %time%] INFO: Updating requirements.txt file...

echo [%date% %time%] INFO: Checking for virtual environment...
if not exist venv\ (
    echo [%date% %time%] ERROR: Virtual environment not found. Please run packages.bat or install.py first.
    exit /b 1
)

echo [%date% %time%] INFO: Activating virtual environment...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo [%date% %time%] ERROR: Failed to activate virtual environment.
    exit /b 1
)

echo [%date% %time%] INFO: Generating updated requirements.txt...
pip freeze > requirements.txt
if %errorlevel% neq 0 (
    echo [%date% %time%] ERROR: Failed to update requirements.txt.
    exit /b 1
)

echo [%date% %time%] INFO: requirements.txt has been updated successfully.
echo [%date% %time%] INFO: The file now contains all currently installed packages.
exit /b 0