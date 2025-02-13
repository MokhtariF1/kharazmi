import subprocess
import sys
import time
import os
import platform


def install_requirements():
    print("Installing dependencies from requirements.txt...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def open_chrome():
    print("Opening Google Chrome with remote-debugging-port=9222...")
    
    # Detect platform and set the appropriate path to Chrome executable
    system_platform = platform.system()
    
    if system_platform == "Windows":
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Update path if needed
    elif system_platform == "Darwin":  # macOS
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    elif system_platform == "Linux":
        chrome_path = "/usr/bin/google-chrome"  # Or "/usr/bin/chromium-browser", depending on your system setup
    else:
        raise Exception(f"Unsupported platform: {system_platform}")
    
    # Run Chrome with remote-debugging-port
    subprocess.Popen([chrome_path, "--remote-debugging-port=9222"])

def run_celery_worker():
    print("Starting Celery worker...")
    # Change to the 'workers' folder before running the command
    os.chdir("workers")
    subprocess.Popen(["celery", "-A", "methods", "worker", "--loglevel=info", "--pool=solo"])

def run_fastapi():
    print("Starting FastAPI server...")
    # Make sure we are still in the 'workers' folder for the FastAPI command
    subprocess.Popen(["uvicorn", "api:app"])

def run_streamlit():
    print("Starting Streamlit panel...")
    # After finishing the workers commands, go back to the main folder to run Streamlit
    os.chdir("..")  # Go back to the main directory (assuming Streamlit is in the root directory)
    subprocess.Popen(["streamlit", "run", "main_page.py"])

def main():
    # Install dependencies
    install_requirements()

    # Open Google Chrome
    open_chrome()

    # Wait a bit before starting the services to ensure Chrome is ready
    time.sleep(5)

    # Run Celery worker in the 'workers' folder
    run_celery_worker()

    # Run FastAPI server in the 'workers' folder
    run_fastapi()

    # Run Streamlit panel from the main folder
    run_streamlit()
    
    print("All services are up and running!")

if __name__ == "__main__":
    main()
