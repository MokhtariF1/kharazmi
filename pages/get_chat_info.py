import streamlit as st
import requests

with open("style.css") as css:
    st.markdown("<style>" + css.read() + "</style>", unsafe_allow_html=True)
st.markdown('<div class="header">دریافت اطلاعات چت</div>', unsafe_allow_html=True)

def get_chat_info(peer_id):
    if peer_id == "":
        st.error("لطفا آیدی چت را وارد کنید!")
        return None
    
    url = f"http://127.0.0.1:8000/get_chat_info/?peer_id={peer_id}"
    response = requests.post(url)
    info = response.json()
    
    if info["status"] == 200:
        return info
    else:
        st.error(f"خطایی رخ داده است!")
        return None
    
def display_chat_info(info):
    if not info:
        return
    username = "ثبت نشده" if info['username'] is None else info["username"]
    phone = "ثبت نشده" if info['phone'] is None else info["phone"]
    name = "ثبت نشده" if info['name'] is None else info["name"]
    bio = "ثبت نشده" if info['bio'] is None else info["bio"]
    text = f"نام کاربری: {username}\nنام: {name}\nشماره تلفن: {phone}\nبیوگرافی: {bio}"
    st.info(text)
with st.form("GetChatInfo"):
    chat_id = st.text_input("شناسه چت", placeholder="-1234567890")
    submitted = st.form_submit_button("دریافت اطلاعات")
    
    if submitted:
        st.info("درحال دریافت اطلاعات...")
        chat_info = get_chat_info(chat_id)
        if chat_info:
            display_chat_info(chat_info)