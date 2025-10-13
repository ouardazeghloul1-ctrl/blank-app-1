import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

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

# === إنشاء التقرير PDF بالعربية ===
class PDF(FPDF):
    def header(self):
        self.add_font("Amiri", "", "Amiri-Regular.ttf", uni=True)
        self.set_font("Amiri", "B", 16)
        self.cell(0, 10, "🏙️ تقرير التحليل العقاري الذهبي", 0, 1, "C")
        self.ln(5)

def create_arabic_pdf(user_type, city, property_type, area, rooms, status, count, chosen_pkg, total_price):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Amiri", "", 14)
    
    content = f"""
معلومات العميل:
نوع العميل: {user_type}
المدينة: {city}
نوع العقار: {property_type}
المساحة: {area} متر مربع
عدد الغرف: {rooms}
الحالة: {status}
عدد العقارات المحللة: {count}

تفاصيل الباقة:
الباقة المختارة: {chosen_pkg}
السعر الإجمالي: {total_price} دولار

ملخص التحليل:
- تحليل سوق العقارات في مدينة {city}.
- تقييم الأسعار لنوع العقار {property_type}.
- تقييم فرص الاستثمار.
- توصيات مخصصة لـ {user_type}.

تم إنشاء التقرير في: {datetime.now().strftime('%Y-%m-%d الساعة %H:%M:%S')}
"""
    
    pdf.multi_cell(0, 10, content)
    return pdf

if st.button("📥 تحميل تقريرك PDF بالعربية"):
    try:
        pdf = create_arabic_pdf(user_type, city, property_type, area, rooms, status, count, chosen_pkg, total_price)
        filename = f"تقرير_عقاري_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.output(filename)
        with open(filename, "rb") as f:
            st.download_button(
                label="📥 اضغط لتحميل التقرير بالعربية",
                data=f,
                file_name=filename,
                mime="application/pdf"
            )
        st.success("✅ تم إنشاء التقرير بالعربية بنجاح!")
        os.remove(filename)
    except Exception as e:
        st.error(f"❌ حدث خطأ أثناء إنشاء التقرير: {e}")

# === واتساب للتواصل ===
st.markdown("""
<div class='center'>
<a href="https://wa.me/213779888140" target="_blank">
<button style="background-color:green;color:white;font-size:18px;padding:10px 20px;border:none;border-radius:10px;">💬 تواصل عبر واتساب</button>
</a>
</div>
""", unsafe_allow_html=True)
