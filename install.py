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

def log_warning(message):
    timestamp = time.strftime("%H:%M:%S")
    print(f"{YELLOW}[{timestamp} WARNING]{RESET} {message}")

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
    log_info("Starting installation process...")

    log_info("Checking Python version...")
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        log_error(f"Python 3.8+ is required. Found {python_version.major}.{python_version.minor}")
        sys.exit(1)
    log_info(f"Python {python_version.major}.{python_version.minor}.{python_version.micro} detected")

    log_info("Checking for requirements.txt...")
    if not os.path.exists("requirements.txt"):
        log_error("requirements.txt file not found.")
        sys.exit(1)
    log_info("requirements.txt found")

    venv_dir = "venv"
    if platform.system() == "Windows":
        python_cmd = "python"
        venv_activate = os.path.join(venv_dir, "Scripts", "activate")
    else:
        python_cmd = "python3"
        venv_activate = os.path.join(venv_dir, "bin", "activate")

    if not os.path.exists(venv_dir):
        log_info("Creating virtual environment...")
        run_command(f"{python_cmd} -m venv {venv_dir}", "Failed to create virtual environment")
    else:
        log_info("Virtual environment already exists")

    if platform.system() == "Windows":
        pip_cmd = f"{venv_dir}\\Scripts\\pip"
    else:
        pip_cmd = f"{venv_dir}/bin/pip"

    log_info("Updating pip...")
    run_command(f"{pip_cmd} install --upgrade pip", "Failed to upgrade pip")

    log_info("Installing requirements...")
    run_command(f"{pip_cmd} install -r requirements.txt", "Failed to install requirements")


    if not os.path.exists(".env"):
        log_warning("No .env file found. Creating template...")
        with open(".env", "w") as env_file:
            env_file.write("# Environment Variables\n")
            env_file.write("OPENAI_API_KEY=your_api_key_here\n")
        log_info("Created .env template. Please edit with your API keys.")

    try:
        import pyttsx3
    except ImportError:
        log_warning("pyttsx3 package is required but not in requirements.txt")
        run_command(f"{pip_cmd} install pyttsx3", "Failed to install pyttsx3")

    log_info("Installation completed successfully!")
    
    if platform.system() == "Windows":
        log_info("To activate the environment, run: .\\venv\\Scripts\\activate")
    else:
        log_info("To activate the environment, run: source ./venv/bin/activate")
    
    log_info("To run the application, run: python main.py")

if __name__ == "__main__":
    main()