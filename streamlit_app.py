# streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
from io import BytesIO
from fpdf import FPDF
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from data_scraper import RealEstateScraper  # ملفك الذي جهزته

# ---------------------- إعداد الصفحة ----------------------
st.set_page_config(page_title="Warda Smart Real Estate", page_icon="🏠", layout="wide")

# ---------------------- ستايل داكن وذهبي ----------------------
st.markdown("""
<style>
    body { background-color: #050505; color: #f0f0f0; }
    .gold { color: #D4AF37; font-weight:700; }
    .card { background:#0f0f0f; padding:14px; border-radius:12px; border:1px solid rgba(212,175,55,0.12); }
    .btn-gold > button { background: linear-gradient(90deg,#D4AF37,#c9a833); color:#0a0a0a; font-weight:700; border-radius:8px; padding:8px 16px; }
    .small-muted { color:#bfbfbf; font-size:13px; }
</style>
""", unsafe_allow_html=True)

# ---------------------- العنوان والشعار ----------------------
st.markdown("<h1 style='text-align:center' class='gold'>🏠 Warda Smart Real Estate</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#ddd; margin-top:-10px'>✨ هيا أنجز! — ذكاء عقاري، تقارير فخمة</p>", unsafe_allow_html=True)
st.markdown("---")

# ---------------------- إعدادات عامة قابلة للتعديل ----------------------
EXCHANGE_RATE_SAR_PER_USD = 3.75  # ضبط قابل للتعديل (ريال لكل دولار)
MAX_PROPERTIES_ALLOWED = 5000

# ---------------------- لوحة الإدخال الرئيسية (خطوات) ----------------------
st.header("ابدأ تحليل السوق — اختر إعداداتك")
with st.container():
    c1, c2 = st.columns([2, 1])
    with c1:
        # اختيار نوع العميل كبطاقات
        st.write("**من أنت؟ اختر ملفك الشخصي**")
        client_types = [
            ("مستثمر فردي", "🔎 أبحث عن أفضل فرص استثمارية"),
            ("وسيط عقاري", "🤝 أدوات تسويق وتسعير للصفقات السريعة"),
            ("شركة تطوير", "🏗️ دراسات جدوى ومواقع للتطوير"),
            ("باحث عن سكن", "🏠 مناطق مناسبة للأسرة"),
            ("ممول عقاري", "💼 تقارير مخاطرة وقيمة ضمان"),
            ("مستشار عقاري", "📊 أدوات تقييم متقدمة")
        ]
        cols = st.columns(len(client_types))
        client_type = None
        for idx, (ct, subtitle) in enumerate(client_types):
            if cols[idx].button(f"{ct}\n\n{subtitle}", key=f"client_{idx}"):
                client_type = ct
        # إن لم يختَر أحد، أعرض الخيار الأول افتراضياً
        if client_type is None:
            client_type = client_types[0][0]
            st.info(f"تم افتراض نوع العميل: **{client_type}** — يمكنك تغييره باختيار بطاقة أخرى.", icon="ℹ️")

    with c2:
        # اختيارات المدينة، النوع، الحالة
        st.write("**إعدادات البحث**")
        city = st.selectbox("💠 اختر المدينة", ["الرياض", "جدة", "الدمام", "مكة", "المدينة", "الخبر", "الطائف"])
        property_type = st.selectbox("🏷️ نوع العقار", [
            "شقة", "فيلا", "أرض", "دوبلكس", "محل تجاري", "مكتب", "استوديو", "عمارة", "مزرعة", "مستودع", "شاليه"
        ])
        listing_status = st.selectbox("📌 الحالة", ["للبيع", "للإيجار", "كلاهما"])
        num_properties = st.slider("📊 عدد العقارات في التحليل", min_value=100, max_value=MAX_PROPERTIES_ALLOWED, value=1000, step=100)

# ---------------------- دالة تقدير السعر (ريال + دولار) ----------------------
def estimate_market_price(city, property_type, num_properties):
    # قواعد أساسية (قابلة للتعديل لاحقاً) — تعطي رقم متوسط للسوق
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
    # مضاعف يعتمد على عدد العقارات (كل 500 عقار يزيد 3%)
    multiplier = 1 + (num_properties / 5000) * 0.15  # حتى +15% عند 5000
    estimated_sar = int(base_price * multiplier)
    estimated_usd = round(estimated_sar / EXCHANGE_RATE_SAR_PER_USD, 2)
    return estimated_sar, estimated_usd

est_sar, est_usd = estimate_market_price(city, property_type, num_properties)

# ---------------------- عرض السعر التقديري ----------------------
st.markdown("---")
st.subheader("💰 السعر التقديري قبل جلب البيانات")
colp = st.columns([2, 1])[0]
st.markdown(f"<div class='card' style='text-align:center'><h2 class='gold'>{est_sar:,.0f} ريال</h2><p class='small-muted'>≈ ${est_usd:,.2f} (تحويل بسعر {EXCHANGE_RATE_SAR_PER_USD} SAR = 1 USD)</p></div>", unsafe_allow_html=True)

st.markdown("---")

# ---------------------- منطقة معلومات الجلب (ستتعبأ بعد الجلب) ----------------------
info_placeholder = st.empty()
results_placeholder = st.empty()

# ---------------------- زر جلب البيانات الحقيقية ----------------------
scraper = RealEstateScraper()

if st.button("🔍 جلب البيانات الحقيقية الآن", key="fetch_real_data"):
    start_time = time.time()
    with st.spinner("⏳ جاري جلب البيانات من المصادر (عقار + بيوت)... يرجى الانتظار — العملية قد تستغرق وقتاً للكم الكبير من السجلات"):
        df = scraper.get_real_data(city=city, property_type=property_type, num_properties=num_properties)
    duration = time.time() - start_time

    # حساب عدد السجلات من كل مصدر لو وجد عمود 'المصدر'
    source_counts = {}
    if not df.empty and 'المصدر' in df.columns:
        source_counts = df['المصدر'].value_counts().to_dict()

    # إحصائيات سريعة
    total_count = len(df)
    avg_price = int(df['السعر'].dropna().astype(float).mean()) if 'السعر' in df.columns and not df['السعر'].dropna().empty else 0
    avg_price_usd = round(avg_price / EXCHANGE_RATE_SAR_PER_USD, 2)

    # تدريب نموذج تنبؤ بسيط (إن أمكن)
    ai_message = "نموذج الذكاء الاصطناعي لم يُدَرَّب (بيانات غير كافية) — سيتم تفعيله إن كانت البيانات مناسبة."
    predictions_30 = None
    predictions_90 = None
    try:
        # تجهيز ميزات إن وجدت: نحاول استخراج الأعمدة الرقمية المستخدمة
        numeric_cols = []
        for col in ['المساحة', 'غرف', 'حمامات', 'عمر_العقار', 'قرب_مراكز', 'السعر']:
            if col in df.columns:
                numeric_cols.append(col)
        # إذا كان لدينا سعر وميزات عددية كافية:
        if 'السعر' in df.columns and len(df) >= 50 and len(numeric_cols) >= 3:
            # تحويل القيم إلى أرقام (تنظيف)
            dfn = df.copy()
            # إزالة النصوص من المساحة إن كانت '### م²'
            if 'المساحة' in dfn.columns:
                dfn['مساحة_num'] = dfn['المساحة'].astype(str).str.extract(r'(\d+)').astype(float, errors='ignore')
            # تجهيز X, y
            features = []
            if 'مساحة_num' in dfn.columns:
                features.append('مساحة_num')
            if 'غرف' in dfn.columns:
                dfn['غرف'] = pd.to_numeric(dfn['غرف'], errors='coerce').fillna(1)
                features.append('غرف')
            if 'حمامات' in dfn.columns:
                dfn['حمامات'] = pd.to_numeric(dfn['حمامات'], errors='coerce').fillna(1)
                features.append('حمامات')
            if 'عمر_العقار' in dfn.columns:
                dfn['عمر_العقار'] = pd.to_numeric(dfn['عمر_العقار'], errors='coerce').fillna(5)
                features.append('عمر_العقار')
            # dropna
            dfn = dfn.dropna(subset=features + ['السعر'])
            if len(dfn) >= 40:
                X = dfn[features]
                y = pd.to_numeric(dfn['السعر'], errors='coerce')
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                model = RandomForestRegressor(n_estimators=100, random_state=42)
                model.fit(X_train, y_train)
                # نستخدم متوسط X_test لتوقعات مستقبلية (محاكاة)
                base_x = X_test.median().to_frame().T
                pred_now = model.predict(base_x)[0]
                # نفترض نمو بسيط: نضرب في عوامل لمحاكاة 30/90 يوم
                predictions_30 = int(pred_now * 1.03)  # توقع نمو 3% خلال 30 يوم (محاكاة)
                predictions_90 = int(pred_now * 1.08)  # توقع نمو 8% خلال 90 يوم (محاكاة)
                ai_message = "✅ تم تدريب نموذج مبدئي للتنبؤ وعرض النتائج (محاكاة تعتمد على بيانات السحب)."
    except Exception as e:
        ai_message = f"⚠️ فشل تدريب نموذج الذكاء الاصطناعي: {e}"

    # عرض معلومات الجلب بشكل أنيق
    info_html = f"""
    <div class='card'>
        <h3 class='gold'>🛰️ تفاصيل عملية الجلب</h3>
        <p class='small-muted'>المدينة: <b>{city}</b> · نوع العقار: <b>{property_type}</b> · الحالة: <b>{listing_status}</b></p>
        <p>⏱️ زمن التنفيذ: <b>{duration:.1f} ثانية</b> · 📦 إجمالي السجلات: <b>{total_count}</b></p>
        <p>📊 متوسط سعر السجلات: <b>{avg_price:,.0f} ريال</b> ≈ <b>${avg_price_usd:,}</b></p>
        <p>📥 مصادر الجلب: {', '.join([f"{k}: {v}" for k,v in source_counts.items()]) if source_counts else 'غير متوفرة'}</p>
        <p class='small-muted'>{ai_message}</p>
    </div>
    """
    info_placeholder.markdown(info_html, unsafe_allow_html=True)

    # عرض الجدول
    if not df.empty:
        results_placeholder.dataframe(df.head(100))  # نعرض أول 100 للعرض السريع

    # زر إنشاء تقرير PDF مخصص حسب نوع العميل
    def create_pdf(report_title, report_data, ai30, ai90):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, report_title, ln=True, align='C')
        pdf.ln(6)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 8, f"العميل: {client_type}", ln=True)
        pdf.cell(0, 8, f"المدينة: {city} | نوع العقار: {property_type}", ln=True)
        pdf.cell(0, 8, f"عدد السجلات: {total_count}", ln=True)
        pdf.cell(0, 8, f"متوسط السعر: {avg_price:,.0f} ريال (≈ ${avg_price_usd})", ln=True)
        pdf.ln(6)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 8, "التحليل والتوصيات:", ln=True)
        pdf.set_font("Arial", '', 12)
        for line in report_data:
            pdf.multi_cell(0, 7, f"• {line}")
        pdf.ln(6)
        if ai30 and ai90:
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 8, f"تنبؤ 30 يوم (محاكاة): {ai30:,.0f} ريال", ln=True)
            pdf.cell(0, 8, f"تنبؤ 90 يوم (محاكاة): {ai90:,.0f} ريال", ln=True)
        pdf.ln(8)
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(0, 6, f"تولد التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        return pdf.output(dest='S').encode('latin1')

    # إعداد التحليل المخصص لكل نوع عميل
    analysis_by_client = {
        "مستثمر فردي": [
            f"قائمة بأفضل 5 عقارات حسب العائد المتوقع في {city}",
            "مقارنة شراء vs إيجار للعقارات المشمولة",
            "استراتيجيات تفاوض لخفض السعر"
        ],
        "وسيط عقاري": [
            "قائمة أسعار المنافسين في نفس المنطقة",
            "اقتراحات تسعير سريع لبيع خلال 30 يوم",
            "قوالب عرض جاهزة للعملاء"
        ],
        "شركة تطوير": [
            "تحديد مواقع ملائمة للتطوير بناءً على السعر والمساحة",
            "تقدير تكلفة أولية ودراسة جدوى مبدئية",
            "تحليل فجوة العرض والطلب"
        ],
        "باحث عن سكن": [
            "أفضل 5 مناطق مناسبة للسكن العائلي",
            "مقارنة الخدمات التعليمية والصحية قرب العقارات",
            "نصائح لاختيار العقار حسب الميزانية"
        ],
        "ممول عقاري": [
            "تقرير مخاطر يعتمد على متغيرات الضمان والسعر",
            "تقدير القيمة السوقية للضمانات",
            "توصيات شروط التمويل"
        ],
        "مستشار عقاري": [
            "تحليل اتجاهات السوق والبيانات التاريخية",
            "نماذج تقييم آلي للعقارات",
            "قوالب تقارير جاهزة للعرض للعملاء"
        ]
    }

    report_lines = analysis_by_client.get(client_type, ["تحليل شامل للسوق العقاري حسب الطلب"])
    pdf_bytes = create_pdf(f"تقرير Warda Smart Real Estate - {client_type}", report_lines, predictions_30, predictions_90)

    st.download_button(label="📥 تحميل التقرير PDF المخصص", data=pdf_bytes,
                       file_name=f"تقرير_Warda_{client_type}_{city}_{datetime.now().strftime('%Y%m%d')}.pdf",
                       mime="application/pdf")

    # إظهار تنبؤات الذكاء الاصطناعي إذا كانت متاحة
    if predictions_30 and predictions_90:
        st.markdown("---")
        st.subheader("🔮 تنبؤات الذكاء الاصطناعي (محاكاة)")
        st.write(f"تنبؤ السعر النموذجي خلال 30 يوم: **{predictions_30:,.0f} ريال**")
        st.write(f"تنبؤ السعر النموذجي خلال 90 يوم: **{predictions_90:,.0f} ريال**")

# ---------------------- تذييل بسيط مع واتساب ----------------------
st.markdown("---")
st.markdown("<div style='text-align:center' class='small-muted'>تواصل معنا على WhatsApp: <b>00779888140</b></div>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; color:#888; padding:10px;'>© Warda Smart Real Estate</div>", unsafe_allow_html=True)
