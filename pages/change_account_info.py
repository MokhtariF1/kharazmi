import streamlit as st
import requests

with open("style.css") as css:
    st.markdown("<style>" + css.read() + "</style>", unsafe_allow_html=True)
st.markdown('<div class="header">تغییر اطلاعات اکانت</div>',
            unsafe_allow_html=True)


def change_account_info(first_name, last_name, bio):
    if first_name == "" and last_name == "" and bio == "":
        st.error("حداقل یکی از فرم ها را پر کنید")
        return None
    first_name = None if first_name == "" else first_name
    last_name = None if last_name == "" else last_name
    bio = None if bio == "" else bio
    url = f"http://127.0.0.1:8000/change_account_info/?"
    if first_name != None:
        url += f"first_name={first_name}&"
    if last_name != None:
        url += f"last_name={last_name}&"
    if bio != None:
        url += f"bio={bio}"
    response = requests.put(url)
    info = response.json()

    if info["status"] == 200:
        return info
    else:
        st.error(f"خطایی رخ داده است!")
        return None


with st.form("ChangeAccountInfo"):
    first_name = st.text_input("نام", placeholder="حسین")
    last_name = st.text_input("نام خانوادگی", placeholder="مختاری")
    bio = st.text_input("بیوگرافی", placeholder="تست")
    submitted = st.form_submit_button("تغییر اطلاعات اکانت")

    if submitted:
        st.info("درحال تغییر اطلاعات اکانت...")
        result = change_account_info(
            first_name=first_name, last_name=last_name, bio=bio)
        if result:
            st.success("اطلاعات اکانت با موفقیت تغییر کرد!")