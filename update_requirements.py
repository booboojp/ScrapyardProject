#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
import time

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def log_info(message):
    timestamp = time.strftime("%H:%M:%S")
    print(f"{GREEN}[{timestamp} INFO]{RESET} {message}")

def log_error(message):
    timestamp = time.strftime("%H:%M:%S")
    print(f"{RED}[{timestamp} ERROR]{RESET} {message}")

def run_command(command, error_message):
    try:
        result = subprocess.run(command, check=True, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        log_error(f"{error_message}: {e}")
        log_error(f"Command output: {e.stderr}")
        sys.exit(1)

def main():
    log_info("Updating requirements.txt file...")


    venv_dir = "venv"
    if not os.path.exists(venv_dir):
        log_error("Virtual environment not found. Please run install.py or packages.bat first.")
        sys.exit(1)

    if platform.system() == "Windows":
        pip_cmd = f"{venv_dir}\\Scripts\\pip"
    else:
        pip_cmd = f"{venv_dir}/bin/pip"

    log_info("Generating updated requirements.txt...")
    run_command(f"{pip_cmd} freeze > requirements.txt", "Failed to update requirements.txt")

    log_info("requirements.txt has been updated successfully.")
    log_info("The file now contains all currently installed packages.")

if __name__ == "__main__":
    main()