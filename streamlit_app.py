import streamlit as st
import pandas as pd
from data_scraper import RealEstateScraper

# تفعيل إعدادات الصفحة
st.set_page_config(page_title="Warda Smart Real Estate", page_icon="🏠", layout="wide")

# تنسيق أسود وذهبي فاخر
st.markdown("""
    <style>
    body {
        background-color: #0d0d0d;
        color: #f5f5f5;
    }
    .stApp {
        background-color: #0d0d0d;
    }
    h1, h2, h3, h4 {
        color: #D4AF37;
        text-align: center;
        font-family: 'Cairo', sans-serif;
    }
    .gold-text {
        color: #D4AF37;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #D4AF37;
        color: black;
        border: none;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
        padding: 10px 30px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #bfa135;
        transform: scale(1.03);
    }
    .metric-box {
        background-color: #1c1c1c;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 0 10px #D4AF37;
    }
    </style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown("<h1>🏠 Warda Smart Real Estate</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='gold-text'>✨ هيا أنجز! المنصة الذكية لعقارات المستقبل ✨</h3>", unsafe_allow_html=True)

st.write("")

# نموذج الإدخال
st.subheader("اختر إعدادات البحث الذكية")

col1, col2, col3 = st.columns(3)
with col1:
    city = st.selectbox("🌆 اختر المدينة", ["الرياض", "جدة", "الدمام"])
with col2:
    property_type = st.selectbox("🏠 نوع العقار", ["شقة", "فيلا", "أرض"])
with col3:
    num_properties = st.slider("📊 عدد العقارات التي تريد عرضها", 10, 100, 50)

# دالة تقدير السعر المبدئي
def estimate_price(city, property_type, num_properties):
    base = {
        "الرياض": {"شقة": 750000, "فيلا": 2000000, "أرض": 1200000},
        "جدة": {"شقة": 950000, "فيلا": 2300000, "أرض": 1500000},
        "الدمام": {"شقة": 600000, "فيلا": 1700000, "أرض": 1000000}
    }
    multiplier = 1 + (num_properties / 300)
    return int(base.get(city, {}).get(property_type, 800000) * multiplier)

estimated_price = estimate_price(city, property_type, num_properties)

st.markdown("### 💰 التقدير المبدئي لسعر السوق")
st.markdown(f"<div class='metric-box'><h2>{estimated_price:,.0f} ريال سعودي</h2></div>", unsafe_allow_html=True)

st.write("")
st.write("")

# زر جلب البيانات الحقيقية
scraper = RealEstateScraper()

if st.button("🔍 جلب البيانات الحقيقية الآن"):
    with st.spinner("⏳ يتم الآن جلب البيانات من المواقع العقارية..."):
        data = scraper.get_real_data(city, property_type, num_properties)
        if not data.empty:
            st.success(f"✅ تم جلب {len(data)} عقار من الإنترنت بنجاح!")
            st.dataframe(data)
        else:
            st.warning("⚠️ لم يتم العثور على بيانات حالياً، حاول مجدداً بعد قليل.")

st.write("")
st.markdown("<h4 class='gold-text'>🚀 Warda Smart Real Estate – الذكاء العقاري يبدأ من هنا!</h4>", unsafe_allow_html=True)
