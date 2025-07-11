import streamlit as st
import requests

with open("style.css") as css:
    st.markdown("<style>" + css.read() + "</style>", unsafe_allow_html=True)
st.markdown('<div class="header">دریافت اعضای گروه</div>', unsafe_allow_html=True)

def get_members(peer_id):
    if peer_id == "":
        st.error("لطفا آیدی گروه را وارد کنید!")
        return None
    
    url = f"http://127.0.0.1:8000/get_chat_memebers/?peer_id={peer_id}"
    response = requests.post(url)
    info = response.json()
    
    if info["status"] == 200:
        st.info(f"تعداد اعضای گروه: {info['count']}")
        return info["members"]
    else:
        st.error(f"خطایی رخ داده است!")
        return None
    
def display_members_grid(members):
    if not members:
        return
    cols = st.columns(3)
    for i, member in enumerate(members):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="member-card">
                    <div class="member-name">{member['name']}</div>
                    <div class="member-id">شناسه: {member['peer_id']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

with st.form("GetChatMembers"):
    channel_id = st.text_input("شناسه گروه", placeholder="-1234567890")
    submitted = st.form_submit_button("دریافت اعضا")
    
    if submitted:
        members = get_members(channel_id)
        if members:
            display_members_grid(members)