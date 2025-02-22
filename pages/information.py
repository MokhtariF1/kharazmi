import streamlit as st
from pymongo import MongoClient

client = MongoClient("127.0.0.1:27017")
db = client["eitaa"]
users_collection = db["users"]


find_user = users_collection.find_one()
name, last_name, phone, email = None, None, None, None
if find_user is None:
    user = {
        "name": name,
        "last_name": last_name,
        "phone": phone,
        "email": email,
    }
    users_collection.insert_one(user)
else:
    name = find_user["name"]
    last_name = find_user["last_name"]
    phone = find_user["phone"]
    email = find_user["email"]
def update_user_info(name, last_name, phone, email):
    if name == "" or last_name == "" or phone == "" or email == "":
        st.error("لطفا تمام فیلد ها را کامل کنید!")
    else:
        user = {
            "name": name,
            "last_name": last_name,
            "phone": phone,
            "email": email,
        }
        print(users_collection.count_documents({}))
        users_collection.delete_many({})
        print(users_collection.count_documents({}))
        users_collection.insert_one(user)
        st.info("اطلاعات با موفقیت ثبت شد!")
with open("style.css") as css:
    st.markdown("<style>" + css.read() + "</style>", unsafe_allow_html=True)
st.markdown('<div class="header">ویرایش اطلاعات حساب</div>', unsafe_allow_html=True)
with st.form("Info") as form:
    left_column, right_column = st.columns([1, 1], border=True)
    name_f = left_column.text_input("نام", "", placeholder="ثبت نشده" if name is None else name)
    last_name_f = right_column.text_input("نام خانوادگی", "", placeholder="ثبت نشده" if last_name is None else last_name)
    phone_f = left_column.text_input("شماره تلفن", "", placeholder="ثبت نشده" if phone is None else phone)
    email_f = right_column.text_input("ایمیل", "", placeholder="ثبت نشده" if email is None else email)
    st.form_submit_button(label="ثبت اطلاعات", on_click=update_user_info(name_f, last_name_f, phone_f, email_f))