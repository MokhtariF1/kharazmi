# 🚀 ایتا پابلیشر  

📝 هدف پروژه: ایتا پابلیشر وب سرویس های متفاوتی برای ارتباط با پیام رسان ایتا فراهم میکند

---

## 📦 راه‌اندازی پروژه

ابتدا پیش نیاز ها را روی سیستم خود نصب کنید:  
- Python  
- RabbitMQ  
- MongoDB  
- Google Chrome  
___
کلون کردن ریپوزیتوری:      
```bash
git clone https://github.com/MokhtariF1/kharazmi.git  
```
___
اجرای آسان پروژه:  
```bash
cd Kharazmi  
python3 run.py  
```
___
اجرای پنل کاربر در صورت نیاز:  
```bash
pip install streamlit  
streamlit run main_page.py  
```
___
# 🔥 کانفیگ بخش نظرات   
شما برای اینکه بتوانید بخش نظرات را کانفیگ کنید تا نظرات کاربران به ایمیل شما ارسال شود باید مراحل زیر را طی کنید:
- ابتدا باید تایید دو مرحله ای اکانت گوگل خود را فعال کنید
- بروید **app passwords** سپس به
- یک نام دلخواه برای برنامه انتخاب کنید
- سپس دکمه ساخت را بزنید و رمزی که گوگل به شما میدهد را در جایی ذخیره کنید
- بروید mail.py به فایل  
- متغیر پسورد را ویرایش کنید، و همچنین دو ایمیل ارسال کننده و دریافت کننده را ایمیل خودتان تنظیم کنید که با آن این رمز را دریافت کرده اید
- و تمام! اگر تنظیمات درست باشد نظرات کاربران به ایمیل شما ارسال خواهد شد
___
# 🏃 ارسال درخواست به وب سرویس ها
```python
import requests

# ارسال درخواست به وب سرویس ارسال پیام
url = "http://localhost:8000/send-message?peer_id={peer_id}&text={text}"

response = requests.post(url)

if response.status_code == 200:
    result = response.json()
    print(result)
else:
    print(f"Error: {response.status_code}")

# ارسال درخواست به وب سرویس دریافت اطلاعات اکانت
url = "http://localhost:8000/get-me"

response = requests.post(url)

if response.status_code == 200:
    result = response.json()
    print(result)
else:
    print(f"Error: {response.status_code}")
