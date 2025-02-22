import streamlit as st
import requests


with open("style.css") as css:
    st.markdown("<style>" + css.read() + "</style>", unsafe_allow_html=True)
st.markdown('<div class="header">ارسال پیام</div>', unsafe_allow_html=True)

def send_message(peer_id, text):
    if peer_id == "" or text == "":
        st.error("لطفا فرم ها را پر کنید!")
        return
    url = f"http://127.0.0.1:8000/send-message/?peer_id={peer_id}&text={text}"
    response = requests.post(url)
    info = response.json()
    if info["status"] == 200:
        st.info(f'پیر آیدی: {info["peer_id"]}\nآیدی پیام: {info["msg_id"]}\nزمان ارسال: {info["timestamp"]}\nدیتا مید: {info["data_mid"]}')
    elif info["status"] == 522:
        st.error(f"به دلیل باگ موجود در ایتا گاهی ارسال پیام ها بیش از حد طول میکشد و مربوط به برنامه ما نیست!\nاما در اصل پیام ارسال شده است\nاما به دلیل همان باگ تنها اطلاعات زیر موجود است و قادر به دریافت لینک پیام نیستیم\nپیر آیدی: {info["peer_id"]}\nزمان ارسال: {info["timestamp"]}\nدیتا مید: {info["data_mid"]}")
    else:
        st.error(f"خطایی رخ داده است!")
    # st.success("پیام در صف ارسال قرار گرفت!")

with st.form("SendMessage") as form:
    # st.title("ارسال پیام")
    text = st.text_area("متن", placeholder="این یک پیام تست است")
    channel_id = st.text_area("پیر آیدی", placeholder="-1234567890")
    # peer_id = channel_id
    # msg_text = text
    button = st.form_submit_button("ارسال پیام", on_click=send_message(channel_id, text))