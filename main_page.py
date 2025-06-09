import streamlit as st
import art
with open("style.css") as css:
    st.markdown("<style>" + css.read() + "</style>", unsafe_allow_html=True)
send_message = st.Page("send_message.py", title="ارسال پیام", icon="✍🏻")
get_me = st.Page("get_me.py", title="پروفایل من", icon="👤")
pg = st.navigation([send_message, get_me,])
pg.run()
art.tprint("EitaaPublisher")