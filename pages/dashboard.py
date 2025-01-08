import streamlit as st
import time
from datetime import datetime
import plotly.graph_objects as go

# Set page config for dark theme
st.set_page_config(
    page_title="مشخصات کانفیگ",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for RTL and dark theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    
    .stApp {
        background-color: #1a1a1a;
        color: white;
        direction: rtl;
        font-family: 'Vazirmatn', sans-serif;
    }
    
    .status-active {
        background-color: #2e7d32;
        color: white;
        padding: 5px 15px;
        border-radius: 15px;
        display: inline-block;
    }
    
    .metric-box {
        background-color: #2d2d2d;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .center-text {
        text-align: center;
    }
    
    .button-container {
        display: flex;
        justify-content: center;
        gap: 10px;
    }
    
    .custom-button {
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        color: white;
        cursor: pointer;
    }
    
    .green-button { background-color: #2e7d32; }
    .orange-button { background-color: #f57c00; }
    .purple-button { background-color: #7b1fa2; }
    </style>
    """, unsafe_allow_html=True)

# Header section
col1, col2, col3 = st.columns([1,2,1])
with col1:
    st.markdown("🇮🇷")
with col2:
    st.markdown("<h1 class='center-text'>مشخصات کانفیگ</h1>", unsafe_allow_html=True)
with col3:
    st.markdown("🌞")

# Status section
status_col1, status_col2, status_col3 = st.columns(3)
with status_col1:
    st.markdown("<div class='status-active'>وضعیت: فعال</div>", unsafe_allow_html=True)
with status_col2:
    st.markdown("لوکیشن: چک")
with status_col3:
    st.markdown("نام سرویس: TEST")

# Create two columns for metrics
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
    st.markdown("وضعیت انقضا")
    expiry_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"تا پایان انقضا: {expiry_date}")
    st.progress(0)
    st.markdown("0 روز باقی مانده")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
    st.markdown("حجم مصرف شده")
    
    # Create circular progress chart using plotly
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = 0,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "#2196f3"},
            'bgcolor': "gray",
        }
    ))
    
    fig.update_layout(
        paper_bgcolor = '#2d2d2d',
        plot_bgcolor = '#2d2d2d',
        font = {'color': "white"},
        height = 250
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Emergency volume section
st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
st.markdown("<h3 class='center-text'>دریافت حجم اضطراری</h3>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Usage chart
st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
st.markdown("<h3 class='center-text'>نمودار مصرف</h3>", unsafe_allow_html=True)

# Create circular progress chart
fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = 75,
    domain = {'x': [0, 1], 'y': [0, 1]},
    gauge = {
        'axis': {'range': [None, 100]},
        'bar': {'color': "#4caf50"},
        'bgcolor': "gray",
    }
))

fig.update_layout(
    paper_bgcolor = '#2d2d2d',
    plot_bgcolor = '#2d2d2d',
    font = {'color': "white"},
    height = 300
)

st.plotly_chart(fig, use_container_width=True)

# Buttons
st.markdown("""
    <div class='button-container'>
        <button class='custom-button green-button'>باقی مانده</button>
        <button class='custom-button orange-button'>آپلود</button>
        <button class='custom-button purple-button'>دانلود</button>
    </div>
""", unsafe_allow_html=True)

# Speed test section
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='metric-box center-text'>", unsafe_allow_html=True)
    st.markdown("تست سرعت")
    if st.button("تست سرعت کانکشن"):
        with st.spinner('در حال تست...'):
            time.sleep(2)
            st.success('تست کامل شد!')
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='metric-box center-text'>", unsafe_allow_html=True)
    st.markdown("نمودار آپلود")
    st.markdown("0 بایت")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='metric-box center-text'>", unsafe_allow_html=True)
    st.markdown("نمودار دانلود")
    st.markdown("0 بایت")
    st.markdown("</div>", unsafe_allow_html=True)

# User info table
st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
data = {
    "لینک": ["VLESS"],
    "نام کاربری": ["King-B34M"],
    "محدودیت کاربر": ["2"]
}

st.table(data)
st.markdown("</div>", unsafe_allow_html=True)