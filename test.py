import streamlit as st
with open("style.css") as css:
    st.markdown("<style>" + css.read() + "</style>", unsafe_allow_html=True)

st.markdown('<div class="header">Quick access</div>', unsafe_allow_html=True)
left_column, right_column = st.columns([1, 1], border=True)
left_column.page_link("pages/send_message.py", label="SendMessage")
left_column.page_link("pages/settings.py", label="Settings")
left_column.page_link("pages/get_me.py", label="Get Info")
# right_column.text("Your panel statistics:\nAPI requests: 5\nChannels count: 4\n")
right_column.page_link("pages/add_user.py", label="Add user")
right_column.page_link("pages/channels.py", label="Edit Channels")
right_column.page_link("pages/statistics.py", label="Api Statistics")
st.markdown('<div class="header" id="owner">Ho3einMokhtari</div>', unsafe_allow_html=True)
