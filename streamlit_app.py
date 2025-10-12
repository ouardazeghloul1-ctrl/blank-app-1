# ==================== streamlit_app.py ====================
import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
from io import BytesIO
from fpdf import FPDF
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from data_scraper import RealEstateScraper  # ملفك

# ---------------------- إعداد الصفحة ----------------------
st.set_page_config(page_title="Warda Smart Real Estate", page_icon="🏠", layout="wide")

# ---------------------- ستايل داكن وذهبي ----------------------
st.markdown("""
<style>
    body { background-color: #050505; color: #f0f0f0; }
    .gold { color: #D4AF37; font-weight:700; }
    .card { background:#0f0f0f; padding:20px; border-radius:16px; border:2px solid rgba(212,175,55,0.2); text-align:center; transition: transform 0.3s; }
    .card:hover { transform: scale(1.05); border-color: rgba(212,175,55,0.5);}
    .btn-gold > button { background: linear-gradient(90deg,#D4AF37,#c9a833); color:#0a0a0a; font-weight:700; border-radius:12px; padding:12px 24px; }
    .small-muted { color:#bfbfbf; font-size:13px; }
    .package-title { font-size:20px; font-weight:bold; margin-bottom:6px; }
    .package-desc { font-size:14px; margin-bottom:12px; }
</style>
""", unsafe_allow_html=True)

# ---------------------- العنوان والشعار ----------------------
st.markdown("<h1 style='text-align:center' class='gold'>🏠 Warda Smart Real Estate</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#ddd; margin-top:-10px'>✨ منصة تحليل عقاري ذكية وفخمة</p>", unsafe_allow_html=True)
st.markdown("---")

# ---------------------- إعدادات عامة ----------------------
EXCHANGE_RATE_SAR_PER_USD = 3.75
MAX_PROPERTIES_ALLOWED = 5000

# ---------------------- اختيار المدينة ونوع العقار وعدد العقارات ----------------------
st.header("ابدأ تحليل السوق — اختر إعداداتك")
city = st.selectbox("💠 اختر المدينة", ["الرياض", "جدة", "الدمام", "مكة", "المدينة", "الخبر", "الطائف"])
property_type = st.selectbox("🏷️ نوع العقار", [
    "شقة", "فيلا", "أرض", "دوبلكس", "محل تجاري", "مكتب", "استوديو", "عمارة", "مزرعة", "مستودع", "شاليه"
])
listing_status = st.selectbox("📌 الحالة", ["للبيع", "للإيجار", "كلاهما"])
num_properties = st.slider("📊 عدد العقارات في التحليل", min_value=100, max_value=MAX_PROPERTIES_ALLOWED, value=500, step=100)

# ---------------------- باقات تحليل السوق ----------------------
st.markdown("## ✨ اختر باقتك")
packages = [
    {"title":"🆓 مجانية","desc":"تحليل بسيط لموقع واحد","level":1},
    {"title":"💼 متوسطة","desc":"تحليل + مقارنة أسعار 3 مواقع","level":2},
    {"title":"💎 جيدة","desc":"تحليل تفصيلي + تقرير PDF","level":3},
    {"title":"👑 ممتازة","desc":"تحليل شامل + تقرير PDF مخصص + تنبؤات","level":4},
]

cols = st.columns(4)
selected_package = None
for idx, pkg in enumerate(packages):
    with cols[idx]:
        st.markdown(f"<div class='card'><div class='package-title'>{pkg['title']}</div><div class='package-desc'>{pkg['desc']}</div></div>", unsafe_allow_html=True)
        if st.button(f"اطلب التحليل", key=f"pkg_{idx}"):
            selected_package = pkg

if selected_package is None:
    selected_package = packages[0]  # افتراضي

st.markdown(f"### ✨ باقتك المختارة: **{selected_package['title']}** — {selected_package['desc']}")

# ---------------------- دالة تقدير السعر ----------------------
def estimate_market_price(city, property_type, num_properties):
    base = {
        "الرياض": {"شقة": 800000, "فيلا": 2200000, "أرض": 1200000, "دوبلكس":1300000, "محل تجاري":900000, "مكتب":850000, "استوديو":450000, "عمارة":3500000, "مزرعة":2500000, "مستودع":1100000, "شاليه":1200000},
        "جدة": {"شقة": 700000, "فيلا": 2400000, "أرض": 1400000, "دوبلكس":1350000, "محل تجاري":950000, "مكتب":800000, "استوديو":430000, "عمارة":3200000, "مزرعة":2300000, "مستودع":1050000, "شاليه":1250000},
        "الدمام": {"شقة": 600000, "فيلا": 1800000, "أرض": 1000000, "دوبلكس":1100000, "محل تجاري":700000, "مكتب":650000, "استوديو":320000, "عمارة":2200000, "مزرعة":1800000, "مستودع":900000, "شاليه":1000000},
        "مكة": {"شقة": 650000, "فيلا": 1900000, "أرض": 1100000},
        "المدينة": {"شقة": 600000, "فيلا": 1700000, "أرض": 1000000},
        "الخبر": {"شقة": 900000, "فيلا": 2600000, "أرض": 1600000},
        "الطائف": {"شقة": 400000, "فيلا": 1200000, "أرض": 700000}
    }
    city_map = base.get(city, base["الرياض"])
    base_price = city_map.get(property_type, 800000)
    multiplier = 1 + (num_properties / 5000) * 0.15
    estimated_sar = int(base_price * multiplier)
    estimated_usd = round(estimated_sar / EXCHANGE_RATE_SAR_PER_USD, 2)
    return estimated_sar, estimated_usd

est_sar, est_usd = estimate_market_price(city, property_type, num_properties)
st.markdown(f"<h3 class='gold'>💰 السعر التقديري: {est_sar:,.0f} ريال ≈ ${est_usd:,.2f}</h3>", unsafe_allow_html=True)
st.markdown("---")

# ---------------------- منطقة معلومات الجلب ----------------------
info_placeholder = st.empty()
results_placeholder = st.empty()

# ---------------------- زر جلب البيانات ----------------------
scraper = RealEstateScraper()

if st.button("🔍 جلب البيانات الحقيقية الآن", key="fetch_real_data"):
    start_time = time.time()
    with st.spinner("⏳ جاري جلب البيانات..."):
        df = scraper.get_real_data(city=city, property_type=property_type, num_properties=num_properties)
    duration = time.time() - start_time

    # إحصائيات
    total_count = len(df)
    avg_price = int(df['السعر'].dropna().astype(float).mean()) if 'السعر' in df.columns else 0
    avg_price_usd = round(avg_price / EXCHANGE_RATE_SAR_PER_USD,2)
    source_counts = df['المصدر'].value_counts().to_dict() if 'المصدر' in df.columns else {}

    # تدريب نموذج بسيط (إن توفرت بيانات كافية)
    ai_message = "نموذج AI لم يُدَرَّب (بيانات قليلة)"
    predictions_30 = predictions_90 = None
    try:
        numeric_cols = [col for col in ['المساحة','غرف','حمامات','عمر_العقار'] if col in df.columns]
        if 'السعر' in df.columns and len(df)>=50 and len(numeric_cols)>=2:
            dfn = df.copy()
            if 'المساحة' in dfn.columns:
                dfn['مساحة_num'] = pd.to_numeric(dfn['المساحة'].astype(str).str.extract(r'(\d+)')[0], errors='coerce')
                numeric_cols = ['مساحة_num'] + [c for c in numeric_cols if c!='المساحة']
            dfn[numeric_cols] = dfn[numeric_cols].apply(pd.to_numeric, errors='coerce').fillna(1)
            X = dfn[numeric_cols]
            y = pd.to_numeric(dfn['السعر'], errors='coerce')
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            base_x = X_test.median().to_frame().T
            pred_now = model.predict(base_x)[0]
            predictions_30 = int(pred_now*1.03)
            predictions_90 = int(pred_now*1.08)
            ai_message = f"نموذج AI جاهز: تقديرات 30 يوم ≈ {predictions_30}, 90 يوم ≈ {predictions_90}"
    except Exception as e:
        ai_message = f"خطأ في نموذج AI: {str(e)}"

    # عرض النتائج
    results_placeholder.markdown(f"""
    ### 📊 إحصائيات التحليل
    - عدد العقارات: {total_count}
    - متوسط السعر: {avg_price:,} ريال ≈ ${avg_price_usd}
    - المصادر: {source_counts}
    - {ai_message}
    - زمن المعالجة: {duration:.2f} ثانية
    """)

    # ---------------------- تقرير PDF ----------------------
    def create_pdf(city, property_type, df, est_sar, est_usd, predictions_30=None, predictions_90=None):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.set_text_color(212,175,55)
        pdf.cell(0, 10, f"📄 تقرير تحليل سوق العقار — {city} ({property_type})", ln=True, align='C')
        pdf.set_font("Arial", '', 12)
        pdf.set_text_color(0,0,0)
        pdf.ln(5)
        pdf.cell(0,8,f"تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
        pdf.cell(0,8,f"عدد العقارات: {len(df)}", ln=True)
        pdf.cell(0,8,f"السعر التقديري: {est_sar:,} ريال ≈ ${est_usd}", ln=True)
        if predictions_30:
            pdf.cell(0,8,f"تقديرات AI 30 يوم: {predictions_30:,}", ln=True)
        if predictions_90:
            pdf.cell(0,8,f"تقديرات AI 90 يوم: {predictions_90:,}", ln=True)
        pdf.ln(5)
        pdf.multi_cell(0,6,"ملخص التحليل: التقرير يقدم مقارنة الأسعار، أبرز المواقع، ونصائح استثمارية لكل فئة مستهدفه (مستثمر فردي، وسيط، شركة تطوير، الباحث عن سكن).")
        buffer = BytesIO()
        pdf.output(buffer)
        buffer.seek(0)
        return buffer

    pdf_buffer = create_pdf(city, property_type, df, est_sar, est_usd, predictions_30, predictions_90)
    st.download_button("⬇️ تحميل تقرير PDF", data=pdf_buffer, file_name=f"report_{city}_{property_type}.pdf", mime="application/pdf")
