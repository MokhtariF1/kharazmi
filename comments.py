import streamlit as st
from pymongo import MongoClient
from mail import send_mail
client = MongoClient("127.0.0.1:27017")
db = client["eitaa"]
users_collection = db["users"]


def send_email(text):
    if text == "":
        st.error("لطفا یک نظر بنویسید!")
    else:
        find_user = users_collection.find_one()
        texth = """<!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>نظر جدید در ایتا پابلیشر</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                color: #333;
            }}
            .email-container {{
                max-width: 600px;
                margin: 20px auto;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }}
            .header {{
                background-color: #4CAF50;
                color: white;
                padding: 20px;
                text-align: center;
                font-size: 24px;
                font-weight: bold;
            }}
            .content {{
                padding: 20px;
                font-size: 16px;
                line-height: 1.6;
            }}
            .content h2 {{
                color: #4CAF50;
                font-size: 20px;
                margin-bottom: 10px;
            }}
            .content p {{
                margin: 10px 0;
            }}
            .content .label {{
                font-weight: bold;
                color: #4CAF50;
            }}
            .footer {{
                background-color: #f1f1f1;
                padding: 10px;
                text-align: center;
                font-size: 14px;
                color: #777;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                نظر جدید در ایتا پابلیشر
            </div>
            <div class="content">
                <h2>نظر جدید از طرف {name}</h2>
                <p><span class="label">متن نظر:</span></p>
                <p>{text}</p>
                <p><span class="label">نام:</span> {name}</p>
                <p><span class="label">نام خانوادگی:</span> {last_name}</p>
                <p><span class="label">شماره تلفن:</span> {phone}</p>
                <p><span class="label">ایمیل:</span> {email}</p>
            </div>
            <div class="footer">
                این ایمیل به صورت خودکار ارسال شده است. لطفاً به آن پاسخ ندهید.
            </div>
        </div>
    </body>
    </html>""".format(name=find_user["name"], text=text, last_name=find_user["last_name"], phone=find_user["phone"], email=find_user["email"])
        status = send_mail(texth)
        if status == 200:
            st.info("نظر شما با موفقیت ارسال شد!")
        else:
            st.error("خطا")
with open("style.css") as css:
    st.markdown("<style>" + css.read() + "</style>", unsafe_allow_html=True)
find_user = users_collection.find_one()
if find_user is None or find_user["name"] is None:
    st.error("کاربر عزیز برای ارسال نظر لطفااول در بخش اطلاعات، ثبت نام خود را کامل کنید!")
else:
    with st.form("comments") as form:
        text = st.text_area("متن نظر", placeholder="یک نظر بنویسید")
        st.form_submit_button("ارسال نظر", on_click=send_email(text))