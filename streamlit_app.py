import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from fpdf import FPDF
from datetime import datetime
from data_scraper import RealEstateScraper

# === إعداد الصفحة ===
st.set_page_config(page_title="التحليل العقاري الذهبي | Golden Real Estate Analysis", layout="centered")

# === تصميم واجهة أسود وذهبي فاخر ===
st.markdown("""
    <style>
        body { background-color: black; color: gold; }
        .stApp { background-color: black; color: gold; }
        h1, h2, h3, h4, p, label { color: gold !important; }
        .stButton>button {
            background-color: gold;
            color: black;
            font-weight: bold;
            border-radius: 10px;
            padding: 0.6em 1.2em;
            transition: 0.3s;
        }
        .stButton>button:hover { background-color: #d4af37; color: white; }
        .gold-box {
            border: 2px solid gold;
            padding: 15px;
            border-radius: 12px;
            background-color: #111;
            margin-bottom: 15px;
        }
        .center { text-align: center; }
    </style>
""", unsafe_allow_html=True)

# === العنوان الرئيسي ===
st.markdown("<h1 class='center'>🏙️ منصة التحليل العقاري الذهبي</h1>", unsafe_allow_html=True)
st.markdown("<p class='center'>تحليل حقيقي مبني على بيانات من السوق السعودي (عقار - بيوت)</p>", unsafe_allow_html=True)

# === إدخال بيانات المستخدم ===
user_type = st.selectbox("👤 اختر فئتك:", [
    "مستثمر", "وسيط عقاري", "شركة تطوير", "فرد", "باحث عن فرصة", "مالك عقار"
])
city = st.selectbox("🏙️ المدينة:", [
    "الرياض", "جدة", "الدمام", "مكة", "المدينة المنورة", "الخبر", "تبوك", "الطائف"
])
property_type = st.selectbox("🏠 نوع العقار:", ["شقة", "فيلا", "أرض"])
status = st.selectbox("📌 الحالة:", ["للبيع", "للإيجار"])
count = st.slider("🔢 عدد العقارات للتحليل:", 1, 1000, 10)
area = st.slider("📏 مساحة العقار (م²):", 50, 1000, 150)
rooms = st.slider("🚪 عدد الغرف:", 1, 10, 3)

# === الباقات ===
packages = {
    "مجانية": {"price": 0, "desc": "تحليل أساسي لعقار واحد فقط بدون تنبؤات."},
    "أساسية": {"price": 10, "desc": "تحليل متقدم يشمل الموقع والسوق المحلي."},
    "احترافية": {"price": 25, "desc": "تحليل احترافي مع مؤشرات السوق."},
    "ذهبية": {"price": 50, "desc": "تحليل فاخر مع تنبؤات دقيقة وتوصيات استثمارية."}
}
chosen_pkg = st.radio("💎 اختر باقتك:", list(packages.keys()))
total_price = packages[chosen_pkg]["price"] * count

st.markdown(f"""
<div class='gold-box'>
<h3>💰 السعر الإجمالي: {total_price} دولار</h3>
<p>{packages[chosen_pkg]['desc']}</p>
</div>
""", unsafe_allow_html=True)

# === تحليل البيانات ===
scraper = RealEstateScraper()
data = scraper.get_real_data(city, property_type, count)

if not data.empty:
    st.success(f"تم جلب {len(data)} عقار من مواقع حقيقية.")
    st.dataframe(data.head())

    # رسم بياني لتوزيع الأسعار
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.hist(data['السعر'], bins=15)
    ax.set_title("توزيع أسعار العقارات")
    st.pyplot(fig)

# === إنشاء التقرير PDF ===
class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "🏙️ تقرير التحليل العقاري الذهبي", 0, 1, "C")

if st.button("📥 تحميل تقريرك PDF"):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "", 12)

    analysis_text_ar = f"""
👤 الفئة: {user_type}
🏙️ المدينة: {city}
🏠 نوع العقار: {property_type}
📏 المساحة: {area} م²
🚪 عدد الغرف: {rooms}
📌 الحالة: {status}
🔢 عدد العقارات للتحليل: {count}
💎 الباقة: {chosen_pkg}
💰 السعر الإجمالي: {total_price} دولار

📈 تم تحليل العقارات في {city} بناءً على أحدث البيانات من مواقع "عقار" و"بيوت".
"""
    analysis_text_en = f"""
👤 Category: {user_type}
🏙️ City: {city}
🏠 Property Type: {property_type}
📏 Area: {area} sqm
🚪 Rooms: {rooms}
📌 Status: {status}
🔢 Properties Analyzed: {count}
💎 Package: {chosen_pkg}
💰 Total Price: {total_price} USD

📈 Real estate analysis based on real data from Saudi property platforms.
"""

    pdf.multi_cell(0, 10, analysis_text_ar)
    pdf.multi_cell(0, 10, analysis_text_en)

    # حفظ التقرير
    os.makedirs("reports", exist_ok=True)
    file_name = f"reports/warda_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(file_name)
    with open(file_name, "rb") as f:
        st.download_button("📥 اضغط لتحميل تقريرك PDF", data=f, file_name="تقرير_التحليل_الذهبي.pdf", mime="application/pdf")

# === واتساب للتواصل ===
st.markdown("""
<div class='center'>
<a href="https://wa.me/213779888140" target="_blank">
<button style="background-color:green;color:white;font-size:18px;padding:10px 20px;border:none;border-radius:10px;">💬 تواصل عبر واتساب</button>
</a>
</div>
""", unsafe_allow_html=True)
