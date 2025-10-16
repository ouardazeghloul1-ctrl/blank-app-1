import streamlit as st
import numpy as np
from datetime import datetime
import plotly.express as px
import time
from fpdf import FPDF
import io
import base64
from arabic_reshaper import reshape
from bidi.algorithm import get_display
import kaleido

# إعداد الصفحة
st.set_page_config(page_title="Warda Smart Real Estate", layout="wide")

# تنسيق واجهة
st.markdown("""
    <style>
    .main { background-color: #0E1117; color: gold; }
    .stApp { background-color: #0E1117; }
    h1 { color: gold !important; text-align: center; }
    .stButton>button { background-color: gold; color: black; border-radius: 10px; padding: 10px; }
    .package-card { background: #2d2d2d; padding: 15px; border-radius: 10px; border: 2px solid #d4af37; text-align: center; margin: 10px 0; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🏙️ Warda Smart Real Estate - التحليل العقاري</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #d4af37;'>تحليل ذكي لقرارات استثمارية متميزة</p>", unsafe_allow_html=True)

# بيانات الباقات
PACKAGES = {
    "مجانية": {"price": 0, "features": ["تحليل أساسي", "سعر متوسط", "تقرير نصي"]},
    "فضية": {"price": 29, "features": ["تحليل 6 أشهر", "5 مقارنات", "PDF مع رسوم"]},
    "ذهبية": {"price": 79, "features": ["تحليل سنة", "10 مقارنات", "نصائح مخصصة"]}
}

# بيانات السوق
def generate_market_data(city, property_type):
    prices = {"الرياض": {"شقة": 4500, "فيلا": 3200}, "جدة": {"شقة": 3800, "فيلا": 2800}}
    avg_price = prices.get(city, prices["الرياض"]).get(property_type, 3000)
    return {
        'السعر': avg_price,
        'العائد': np.random.uniform(6, 12),
        'النمو': np.random.uniform(0.8, 3.5)
    }

# توليد التقرير
def generate_report(user_type, city, property_type, area, package, count):
    price = PACKAGES[package]["price"] * count
    market_data = generate_market_data(city, property_type)
    content = f"""
    تقرير Warda Smart Real Estate
    تاريخ: {datetime.now().strftime('%Y-%m-%d')}
    فئة: {user_type}
    مدينة: {city}
    نوع العقار: {property_type}
    مساحة: {area} m²
    باقة: {package}
    السعر: {price} دولار
    العائد: {market_data['العائد']:.1f}%
    تحليل: استثمر الآن لتحقيق أرباح مستدامة.
    """
    # 5 رسوم بيانية
    fig1 = px.line(x=[2024, 2025, 2026], y=[market_data['السعر']*0.9, market_data['السعر'], market_data['السعر']*1.1], title="نمو الأسعار")
    fig2 = px.pie(values=[market_data['العائد'], 100-market_data['العائد']], names=['عائد', 'مخاطر'])
    fig3 = px.bar(x=['شقق', 'فيلات'], y=[50, 50], title="توزيع الاستثمار")
    fig4 = px.scatter(x=[1, 2, 3], y=[market_data['النمو']*i for i in [1, 2, 3]], title="نمو متوقع")
    fig5 = px.area(x=[2024, 2025], y=[market_data['السعر'], market_data['السعر']*1.2], title="توقعات السوق")
    return content, price, [fig1, fig2, fig3, fig4, fig5]

# إنشاء PDF
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "تقرير Warda Smart Real Estate", 0, 1, "C")
        self.ln(10)

    def chapter_body(self, body):
        self.set_font("Arial", "", 12)
        reshaped_text = get_display(reshape(body))
        self.multi_cell(0, 10, reshaped_text)
        self.ln()

    def add_image(self, img_buffer):
        self.image(img_buffer, x=10, y=self.get_y(), w=190)
        self.ln(20)

# توليد PDF
def create_pdf(report_text, figs):
    buffer = io.BytesIO()
    pdf = PDF()
    pdf.add_page()
    pdf.chapter_body(report_text)
    for fig in figs:
        img_buffer = io.BytesIO()
        fig.write_image(img_buffer, format='png', width=600, height=400)
        img_buffer.seek(0)
        pdf.add_page()
        pdf.add_image(img_buffer)
    buffer.write(pdf.output(dest='S').encode('latin1'))
    buffer.seek(0)
    return buffer

# الواجهة
with st.form("input_form"):
    user_type = st.selectbox("فئتك:", ["مستثمر", "وسيط"])
    city = st.selectbox("المدينة:", ["الرياض", "جدة"])
    property_type = st.selectbox("نوع العقار:", ["شقة", "فيلا"])
    area = st.slider("المساحة (m²):", 50, 1000, 120)
    package = st.radio("الباقة:", list(PACKAGES.keys()))
    count = st.slider("عدد العقارات:", 1, 5, 1)
    submit = st.form_submit_button("إنشاء التقرير")

if submit:
    with st.spinner("جاري الإنشاء..."):
        time.sleep(2)
        report, price, figs = generate_report(user_type, city, property_type, area, package, count)
        pdf_buffer = create_pdf(report, figs)
        st.session_state.report = report
        st.session_state.pdf = pdf_buffer
        st.success("تم إنشاء التقرير!")

if st.session_state.get('report'):
    st.text_area("التقرير:", st.session_state.report, height=200)
    st.download_button("تحميل PDF", data=st.session_state.pdf, file_name="Warda_Report.pdf", mime="application/pdf")

st.markdown("---")
st.markdown("**واتساب:** +213779888140 | **بريد:** info@warda-intelligence.com")
