import streamlit as st
import time

def main():
    st.set_page_config(page_title="User Panel", layout="wide")

    # Header Section
    st.markdown("""
        <style>
        .header {
            font-size: 30px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="header">مشخصات کا‌ر‌بر</div>', unsafe_allow_html=True)

    # Status Section
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.subheader("وضعیت")
        st.success("فعال")

    with col2:
        st.subheader("نام سرویس")
        st.info("TEST")

    with col3:
        st.subheader("لوکیشن")
        st.write(":iran:")

    st.markdown("---")

    # Progress and Consumption Section
    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("وضعیت انقضاء")
        end_time = "22:10:36 1403-07-29"
        st.text(f"تا پایان انقضاء: {end_time}")
        progress = st.progress(0)

        for percent in range(0, 101, 20):
            time.sleep(0.1)
            progress.progress(percent)

        st.text("0 بایت از 100 گیگ")
        st.write("0 روز باقی مانده")

    with col2:
        st.subheader("حجم مصرف شده")
        st.text("0% بایت")
        st.progress(0)

    # Emergency Section
    st.markdown("---")
    st.subheader("دریافت حجم اضطراری")
    st.button("دریافت")

    # Chart Section
    st.markdown("---")
    st.subheader("نمودار مصرف")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.button("دانلود")
        st.button("آپلود")

    with col2:
        st.write("آپلود: 0 بایت")
        st.write("دانلود: 0 بایت")

    # Speed Test Section
    st.markdown("---")
    st.subheader("تست سرعت کانکشن")
    if st.button("تست سرعت کانکشن"):
        st.write("سرعت تست انجام شد!")

    # Footer Section
    st.markdown("---")
    col1, col2 = st.columns([1, 1])

    with col1:
        st.write("محدودیت کاربر: 2")

    with col2:
        st.write("لینک نام کاربری: King-B34M")

if __name__ == "__main__":
    main()
