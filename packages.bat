@echo off
echo [%date% %time%] INFO: Starting installation process...

echo [%date% %time%] INFO: Checking for Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [%date% %time%] ERROR: Python is not installed.
    exit /b 1
)

echo [%date% %time%] INFO: Python is installed, continuing...

echo [%date% %time%] INFO: Checking for requirements.txt file...
if not exist requirements.txt (
    echo [%date% %time%] ERROR: requirements.txt file not found.
    exit /b 1
)

echo [%date% %time%] INFO: requirements.txt found, continuing...
echo [%date% %time%] INFO: Checking for virtual environment...
if not exist venv\ (
    echo [%date% %time%] INFO: Virtual environment not found, creating...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [%date% %time%] ERROR: Failed to create virtual environment.
        exit /b 1
    )
    echo [%date% %time%] INFO: Virtual environment created successfully.
) else (
    echo [%date% %time%] INFO: Virtual environment already exists.
)

echo [%date% %time%] INFO: Activating virtual environment...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo [%date% %time%] ERROR: Failed to activate virtual environment.
    exit /b 1
)

echo [%date% %time%] INFO: Installing/Updating requirements...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [%date% %time%] ERROR: Failed to install requirements.
    exit /b 1
)

echo [%date% %time%] INFO: Verifying package installations...
for /f "tokens=*" %%i in (requirements.txt) do (
    for /f "tokens=1,2 delims== " %%a in ("%%i") do (
        call :check_package %%a %%b
    )
)

echo [%date% %time%] INFO: Checking for .env file...
if not exist .env (
    echo [%date% %time%] WARNING: No .env file found. Creating template...
    echo # Environment Variables > .env
    echo OPENAI_API_KEY=your_api_key_here >> .env
    echo [%date% %time%] INFO: Created .env template. Please edit with your API keys.
)

echo [%date% %time%] INFO: Installation completed successfully.
echo [%date% %time%] INFO: To activate the environment, run: venv\Scripts\activate
echo [%date% %time%] INFO: To run the application, run: python main.py
exit /b 0

:check_package
set package=%1
set required_version=%2
pip show %package% | findstr /r "^Version" >nul
if %errorlevel% neq 0 (
    echo [%date% %time%] ERROR: Package %package% is not installed correctly.
    echo [%date% %time%] INFO: Attempting to reinstall %package%...
    pip install %package%==%required_version% --force-reinstall
    if %errorlevel% neq 0 (
        echo [%date% %time%] ERROR: Failed to reinstall %package%.
        exit /b 1
    )
)
exit /b 0