import streamlit as st
import streamlit_authenticator as stauth
import art
from PIL import Image
from config import credentials
# در این بخش با شخصی سازی اطلاعات صفحه روی سئو کار شده است
favicon = Image.open("favicon.png")
st.set_page_config(page_title="EitaaPublisher", page_icon=favicon,
                   initial_sidebar_state="auto")
authenticator = stauth.Authenticate(
    credentials=credentials, cookie_name='EitaaPublisher', cookie_key='EitaaPublisher', cookie_expiry_days=1)
try:
    # استایل دادن به صفحات از فایل style.css
    with open("style.css") as css:
        st.markdown("<style>" + css.read() +
                    "</style>", unsafe_allow_html=True)
    authenticator.login(captcha=True, fields={'Form name': 'ورود', 'Username': 'نام کاربری', 'Password': 'رمز عبور',
                                              'Login': 'ورود', 'Captcha': 'کپچا'})

    if st.session_state.get('authentication_status'):
        # تنظیم کردن منو ها با نام دلخواه فارسی
        send_message = st.Page(
            "pages/send_message.py", title="ارسال پیام", icon="✍🏻")
        get_me = st.Page("pages/get_me.py", title="پروفایل من", icon="👤")
        get_chat_members = st.Page(
            "pages/get_chat_members.py", title="اعضای گروه", icon="💎")
        get_chat_info = st.Page("pages/get_chat_info.py",
                                title="اطلاعات چت", icon="💬")
        change_account_info = st.Page(
            "pages/change_account_info.py", title="تغییر اطلاعات اکانت", icon="✏")
        pg = st.navigation(
            [send_message, get_me, get_chat_members, get_chat_info, change_account_info])
        pg.run()
        authenticator.logout(button_name="خروج", location="sidebar")
        # تکه کد زیر برای حذف کردن دکمه deploy پیشفرض streamlit است
        st.markdown("""
            <style>
                .stAppDeployButton{
                display: none
                    }
                ul.st-emotion-cache-1d2la04.e8lvnlb3:last-child {
                    display: none}
                ul.st-emotion-cache-1d2la04.e8lvnlb3:nth-child(4) {
                    display: none}
                ul.st-emotion-cache-1d2la04.e8lvnlb3:nth-child(5) {
                    display: none}
                ul.st-emotion-cache-1d2la04.e8lvnlb3:nth-child(1) {
                display: none}
                div[data-testid=stMainMenuDivider]{
                    display:none}
            </style>
            <script>
                document.getElementsByClassName(
                    "span.st-emotion-cache-6mv2k3.e8lvnlb6").innerText = 'تنظیمات';
            </script>
        """, unsafe_allow_html=True)
        # -------
        # چاپ اسم برنامه به صورت بزرگ در کنسول
        art.tprint("EitaaPublisher")
    elif st.session_state.get('authentication_status') is False:
        st.error('نام کاربری یا رمز عبور اشتباه است')
    elif st.session_state.get('authentication_status') is None:
        st.warning('لطفا نام کاربری و پسورد خود را وارد کنید')
except Exception as e:
    st.error(e)
