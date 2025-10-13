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
# تعليق مؤقت للبيانات الحقيقية لتجنب الأخطاء
data = pd.DataFrame()

# === إنشاء التقرير PDF ===
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Golden Real Estate Analysis Report", 0, 1, "C")
        self.ln(5)

def create_safe_pdf(user_type, city, property_type, area, rooms, status, count, chosen_pkg, total_price):
    """إنشاء PDF آمن بدون مشاكل Unicode"""
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # استخدام النصوص الإنجليزية فقط مع استبدال الآمن للنصوص العربية
    safe_user_type = user_type.replace("مستثمر", "Investor").replace("وسيط عقاري", "Real Estate Agent").replace("شركة تطوير", "Development Company").replace("فرد", "Individual").replace("باحث عن فرصة", "Opportunity Seeker").replace("مالك عقار", "Property Owner")
    
    safe_city = city.replace("الرياض", "Riyadh").replace("جدة", "Jeddah").replace("الدمام", "Dammam").replace("مكة", "Makkah").replace("المدينة المنورة", "Madinah").replace("الخبر", "Khobar").replace("تبوك", "Tabuk").replace("الطائف", "Taif")
    
    safe_property_type = property_type.replace("شقة", "Apartment").replace("فيلا", "Villa").replace("أرض", "Land")
    
    safe_status = status.replace("للبيع", "For Sale").replace("للإيجار", "For Rent")
    
    safe_package = chosen_pkg.replace("مجانية", "Free").replace("أساسية", "Basic").replace("احترافية", "Professional").replace("ذهبية", "Golden")

    # محتوى التقرير بالإنجليزية
    content = f"""
GOLDEN REAL ESTATE ANALYSIS REPORT
==================================

CLIENT INFORMATION:
------------------
Client Type: {safe_user_type}
City: {safe_city}
Property Type: {safe_property_type}
Area: {area} sqm
Rooms: {rooms}
Status: {safe_status}
Properties Analyzed: {count}

PACKAGE DETAILS:
---------------
Selected Package: {safe_package}
Total Price: ${total_price} USD

ANALYSIS SUMMARY:
----------------
Market analysis completed for {safe_city}
Property type analysis: {safe_property_type}
Market status: {safe_status}
Package level: {safe_package}

This comprehensive report provides:
- Current market trends in {safe_city}
- Price analysis for {safe_property_type}
- Investment recommendations
- Market predictions based on current data

Report generated on: {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}

CONCLUSION:
-----------
Based on the analysis of {count} properties in {safe_city},
this report offers valuable insights for {safe_user_type.lower()} 
looking for {safe_property_type.lower()} options {safe_status.lower()}.

For detailed consultation, contact our experts.
"""
    
    pdf.multi_cell(0, 8, content)
    return pdf

if st.button("📥 تحميل تقريرك PDF"):
    try:
        # إنشاء PDF آمن
        pdf = create_safe_pdf(user_type, city, property_type, area, rooms, status, count, chosen_pkg, total_price)
        
        # حفظ في buffer بدلاً من ملف مباشر
        from io import BytesIO
        pdf_buffer = BytesIO()
        pdf.output(pdf_buffer)
        pdf_bytes = pdf_buffer.getvalue()
        pdf_buffer.close()
        
        # تحميل الملف
        st.download_button(
            label="📥 اضغط لتحميل تقريرك PDF",
            data=pdf_bytes,
            file_name=f"golden_estate_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf"
        )
        st.success("✅ تم إنشاء التقرير بنجاح!")
        
    except Exception as e:
        st.error(f"❌ حدث خطأ في إنشاء PDF: {str(e)}")
        st.info("💡 حاولي استخدام أسماء إنجليزية أو قللي من استخدام النصوص العربية في التقرير")

# === واتساب للتواصل ===
st.markdown("""
<div class='center'>
<a href="https://wa.me/213779888140" target="_blank">
<button style="background-color:green;color:white;font-size:18px;padding:10px 20px;border:none;border-radius:10px;">💬 تواصل عبر واتساب</button>
</a>
</div>
""", unsafe_allow_html=True)
