import subprocess
import sys
import time
import os
import platform

def install_requirements():
    print("درحال نصب نیازمندی ها...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def open_chrome():
    print("در حال باز کردن مرورگر کروم...")
    system_platform = platform.system()
    
    if system_platform == "Windows":
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    elif system_platform == "Darwin":
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    elif system_platform == "Linux":
        chrome_path = "/usr/bin/google-chrome"
    else:
        raise Exception(f"Unsupported platform: {system_platform}")
    
    subprocess.Popen([chrome_path, "--remote-debugging-port=9222"])

def run_celery_worker():
    print("در حال اجرای سلری...")
    os.chdir("workers")
    subprocess.Popen(["celery", "-A", "methods", "worker", "--loglevel=info", "--pool=solo"])

def run_fastapi():
    print("در حال اجرای وب سرویس...")
    subprocess.Popen(["uvicorn", "api:app"])

def run_streamlit():
    print("درحال اجرای پنل مدیریت...")
    os.chdir("..")
    subprocess.Popen(["streamlit", "run", "main_page.py"])

def main():
    # نصب نیازمندی ها
    install_requirements()

    # باز کردن کروم
    open_chrome()
    # مقداری صبر بعد از باز شدن کروم
    time.sleep(1)

    # اجرای سلری
    run_celery_worker()

    # اجرای fastApi
    run_fastapi()

    # اجرای پنل مدیریت
    run_streamlit()
    
    print("تمام سرویس ها با موفقیت اجرا شد!")

if __name__ == "__main__":
    main()
