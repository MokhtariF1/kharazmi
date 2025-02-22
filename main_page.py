import streamlit as st
import art
with open("style.css") as css:
    st.markdown("<style>" + css.read() + "</style>", unsafe_allow_html=True)
st.markdown('<div class="header">دسترسی سریع</div>', unsafe_allow_html=True)
left_column, right_column = st.columns([1, 1], border=True)
right_column.page_link("pages/information.py", label="اطلاعات کاربری")
left_column.page_link("pages/send_message.py", label="ارسال پیام")
left_column.page_link("pages/get_me.py", label="دریافت اطلاعات")
right_column.page_link("pages/comments.py", label="نظرات")
left_column.page_link("pages/settings.py", label="تنظیمات")
right_column.page_link("pages/statistics.py", label="آمار وب سرویس")
art.tprint("EitaaPublisher")