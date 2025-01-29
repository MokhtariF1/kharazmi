import requests
import streamlit as st

with open("style.css") as css:
    st.markdown("<style>" + css.read() + "</style>", unsafe_allow_html=True)
st.markdown('<div class="right-header">دریافت اطلاعات</div>', unsafe_allow_html=True)

def send_message():
    url = "http://127.0.0.1:8000/get-me/"
    response = requests.post(url)
    info = response.json()
    if info["status"] == 200:
        st.info(f'نام: {info["first_name"]}\nنام خانوادگی: {info["last_name"]}\nبیوگرافی: {info["bio"]}')
    # st.success("پیام در صف ارسال قرار گرفت!")

with st.form("GetMe") as form:
    # st.markdown('<div class="header">دریافت اطلاعات</div>', unsafe_allow_html=True)
    # text = st.text_area("متن", placeholder="این یک پیام تست است")
    # channel_id = st.text_area("پیر آیدی", placeholder="-1234567890")
    # peer_id = channel_id
    # msg_text = text
    st.write("با کلیک کردن روی دکمه زیر، میتوانید اطلاعات حسابی که ربات در حال حاضر روی آن اجرا هست را دریافت کنید")
    button = st.form_submit_button("دریافت اطلاعات", on_click=send_message)