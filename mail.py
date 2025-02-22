import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


password="app_passwords"
sender_email = "Your_email"
receiver_email = "Your_email"
def send_mail(text):
    subject = "یک نظر جدید در ایتا پابلیشر"
    body = text

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("ایمیل با موفقیت ارسال شد!")
            return 200
    except Exception as e:
        print(f"خطا در ارسال ایمیل: {e}")
        return 500