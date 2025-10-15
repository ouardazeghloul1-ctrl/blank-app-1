import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import random

# === الإعداد العام للتصميم ===
st.set_page_config(page_title="تحليل عقاري ذكي - وردة", layout="centered")

st.markdown("""
    <style>
        body { background-color: black; color: gold; }
        .stApp { background-color: black; color: gold; }
        h1, h2, h3, h4, h5 { color: gold; text-align: center; }
        .stButton button {
            background-color: gold; color: black; border-radius: 12px;
            padding: 10px 20px; font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.title("💎 منصة وردة للتحليل العقاري الذكي")

# === بيانات أولية ===
cities = ["الرياض", "جدة", "الدمام", "مكة", "المدينة المنورة"]
property_types = ["شقة", "فيلا", "أرض", "عمارة", "مكتب", "محل تجاري"]
status_options = ["بيع", "شراء", "إيجار"]

packages = {
    "مجانية": {"price": 0, "features": "تحليل سريع لعقار واحد + تقرير PDF"},
    "فضية": {"price": 10, "features": "تحليل دقيق + متوسط الأسعار + نصائح استثمارية + تقرير PDF"},
    "ذهبية": {"price": 30, "features": "كل ما سبق + تنبؤ ذكي بالسعر + اقتراح أفضل وقت للبيع + تقرير PDF"},
    "ماسية": {"price": 60, "features": "تحليل شامل + مقارنة مشاريع مماثلة + تنبؤ ذكي + تقرير PDF فاخر"},
}

# === اختيار الفئة ===
st.subheader("اختار(ي) فئتك")
selected_package = st.selectbox("اختر الباقة:", list(packages.keys()))
package_info = packages[selected_package]
st.markdown(f"**مميزات الباقة:** {package_info['features']}")

# === اختيار التفاصيل ===
st.subheader("تفاصيل العقار")

city = st.selectbox("المدينة:", cities)
property_type = st.selectbox("نوع العقار:", property_types)
status = st.selectbox("الحالة:", status_options)
num_properties = st.slider("عدد العقارات:", 1, 1000, 1)

# حساب السعر الإجمالي
total_price = package_info["price"] * num_properties
st.markdown(f"### 💰 السعر الإجمالي: {total_price} دولار")

# === زر تحميل التقرير ===
if st.button("📄 تحميل التقرير"):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('Amiri', '', 'Amiri-Regular.ttf', uni=True)
    pdf.set_font('Amiri', '', 14)
    pdf.cell(0, 10, txt="تقرير التحليل العقاري الذكي", ln=True, align='C')
    pdf.cell(0, 10, txt=f"الباقة: {selected_package}", ln=True)
    pdf.cell(0, 10, txt=f"المدينة: {city}", ln=True)
    pdf.cell(0, 10, txt=f"نوع العقار: {property_type}", ln=True)
    pdf.cell(0, 10, txt=f"الحالة: {status}", ln=True)
    pdf.cell(0, 10, txt=f"عدد العقارات: {num_properties}", ln=True)
    pdf.cell(0, 10, txt=f"السعر الإجمالي: {total_price} دولار", ln=True)
    pdf.output("report.pdf")
    with open("report.pdf", "rb") as f:
        st.download_button("⬇️ تحميل التقرير PDF", f, file_name="real_estate_report.pdf")

# === وضع الإدارة السري ===
params = st.experimental_get_query_params()
if "admin" in params and params["admin"][0].lower() == "true":
    st.markdown("### 🔐 وضع الإدارة (خاص بوردة فقط)")
    password = st.text_input("أدخلي الرمز السري:", type="password")

    if password == "Warda2025":
        st.success("تم الدخول بنجاح ✅")
        st.markdown("#### 🎁 إنشاء رابط مؤثر مجاني ليوم واحد")

        if st.button("🔗 إنشاء رابط مؤقت"):
            token = random.randint(100000, 999999)
            expiry = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
            influencer_link = f"https://منصتك.com/?free_access={token}"
            st.write(f"🔗 الرابط المجاني (صالح حتى {expiry}):")
            st.code(influencer_link, language="text")
    else:
        if password:
            st.error("الرمز السري غير صحيح ❌")
