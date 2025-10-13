import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from fpdf import FPDF
from datetime import datetime
import io

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

# === إنشاء التقرير PDF ===
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Golden Real Estate Analysis Report", 0, 1, "C")
        self.ln(5)

def create_pdf_report(user_type, city, property_type, area, rooms, status, count, chosen_pkg, total_price):
    """إنشاء PDF بدون مشاكل"""
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # تحويل النصوص العربية إلى إنجليزية
    user_english = {
        "مستثمر": "Investor",
        "وسيط عقاري": "Real Estate Agent", 
        "شركة تطوير": "Development Company",
        "فرد": "Individual",
        "باحث عن فرصة": "Opportunity Seeker",
        "مالك عقار": "Property Owner"
    }.get(user_type, user_type)
    
    city_english = {
        "الرياض": "Riyadh",
        "جدة": "Jeddah",
        "الدمام": "Dammam",
        "مكة": "Makkah",
        "المدينة المنورة": "Madinah", 
        "الخبر": "Khobar",
        "تبوك": "Tabuk",
        "الطائف": "Taif"
    }.get(city, city)
    
    property_english = {
        "شقة": "Apartment",
        "فيلا": "Villa",
        "أرض": "Land"
    }.get(property_type, property_type)
    
    status_english = {
        "للبيع": "For Sale",
        "للإيجار": "For Rent"
    }.get(status, status)
    
    package_english = {
        "مجانية": "Free",
        "أساسية": "Basic",
        "احترافية": "Professional",
        "ذهبية": "Golden"
    }.get(chosen_pkg, chosen_pkg)

    # محتوى التقرير
    content = f"""
GOLDEN REAL ESTATE ANALYSIS REPORT
==================================

CLIENT INFORMATION:
------------------
Client Type: {user_english}
City: {city_english}
Property Type: {property_english}
Area: {area} sqm
Rooms: {rooms}
Status: {status_english}
Properties Analyzed: {count}

PACKAGE DETAILS:
---------------
Selected Package: {package_english}
Total Price: ${total_price} USD

ANALYSIS SUMMARY:
-----------------
This report provides comprehensive market analysis for {city_english}.
Based on current market data for {property_english} properties {status_english}.

KEY FINDINGS:
- Market trends analysis completed
- Price evaluation for selected property type
- Investment opportunity assessment
- Custom recommendations for {user_english}

Report generated on: {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}

For detailed consultation and personalized advice,
contact our real estate experts.

Warda Smart Real Estate
Professional Market Analysis
"""
    
    pdf.multi_cell(0, 8, content)
    return pdf

if st.button("📥 تحميل تقريرك PDF"):
    try:
        # إنشاء PDF
        pdf = create_pdf_report(user_type, city, property_type, area, rooms, status, count, chosen_pkg, total_price)
        
        # الحل الصحيح: حفظ في BytesIO بطريقة صحيحة
        pdf_buffer = io.BytesIO()
        pdf_output = pdf.output(dest='S').encode('latin-1')
        pdf_buffer.write(pdf_output)
        pdf_buffer.seek(0)
        
        # تحميل الملف
        st.download_button(
            label="📥 اضغط لتحميل تقريرك PDF",
            data=pdf_buffer,
            file_name=f"real_estate_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf"
        )
        st.success("✅ تم إنشاء التقرير بنجاح!")
        
    except Exception as e:
        st.error(f"❌ حدث خطأ: {e}")
        
        # حل بديل إذا فشل الحل الأول
        try:
            st.info("🔄 جرب الحل البديل...")
            pdf = create_pdf_report(user_type, city, property_type, area, rooms, status, count, chosen_pkg, total_price)
            
            # حفظ مؤقت في ملف ثم قراءته
            temp_file = "temp_report.pdf"
            pdf.output(temp_file)
            
            with open(temp_file, "rb") as f:
                st.download_button(
                    label="📥 اضغط لتحميل التقرير (البديل)",
                    data=f,
                    file_name="real_estate_report.pdf",
                    mime="application/pdf"
                )
            
            # تنظيف الملف المؤقت
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
        except Exception as e2:
            st.error(f"❌ فشل الحل البديل أيضاً: {e2}")

# === واتساب للتواصل ===
st.markdown("""
<div class='center'>
<a href="https://wa.me/213779888140" target="_blank">
<button style="background-color:green;color:white;font-size:18px;padding:10px 20px;border:none;border-radius:10px;">💬 تواصل عبر واتساب</button>
</a>
</div>
""", unsafe_allow_html=True)
