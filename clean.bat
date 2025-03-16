@echo off
echo [%date% %time%] INFO: Starting cleanup process...

echo [%date% %time%] INFO: Are you sure you want to remove the virtual environment?
echo This will delete the venv directory and all installed packages.
set /p CONFIRM=Type 'yes' to confirm: 

if /i not "%CONFIRM%"=="yes" (
    echo [%date% %time%] INFO: Cleanup cancelled.
    exit /b 0
)

echo [%date% %time%] INFO: Removing virtual environment...
if exist venv\ (
    rmdir /s /q venv
    echo [%date% %time%] INFO: Virtual environment removed.
) else (
    echo [%date% %time%] INFO: No virtual environment found.
)

echo [%date% %time%] INFO: Cleaning up cache files...
if exist __pycache__\ rmdir /s /q __pycache__
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"

echo [%date% %time%] INFO: Cleanup completed.
echo [%date% %time%] INFO: To reinstall, run install.bat
exit /b 0