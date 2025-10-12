# ====================== Warda Smart Real Estate - Streamlit App ======================
import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
from io import BytesIO
from fpdf import FPDF
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from data_scraper import RealEstateScraper  # تأكدي من وجود هذا الملف مع دالة get_real_data

# ------------------ إعداد الصفحة ------------------
st.set_page_config(page_title="Warda Smart Real Estate", page_icon="🏠", layout="wide")

# ------------------ ستايل أسود وذهبي ------------------
st.markdown("""
<style>
    body { background-color: #050505; color: #f0f0f0; }
    .gold { color: #D4AF37; font-weight:700; }
    .card { background:#0f0f0f; padding:20px; border-radius:12px; border:1px solid rgba(212,175,55,0.25); text-align:center; }
    .btn-gold > button { background: linear-gradient(90deg,#D4AF37,#c9a833); color:#0a0a0a; font-weight:700; border-radius:12px; padding:12px 20px; font-size:16px; }
    .small-muted { color:#bfbfbf; font-size:13px; }
    .package-title { font-size:18px; font-weight:700; margin-bottom:6px; }
    .package-desc { font-size:14px; color:#ddd; margin-bottom:10px; }
    .btn-paypal { background:#ffc439; color:#050505; padding:10px 16px; border-radius:10px; font-weight:700; text-decoration:none; }
</style>
""", unsafe_allow_html=True)

# ------------------ عنوان المنصة ------------------
st.markdown("<h1 style='text-align:center' class='gold'>🏠 Warda Smart Real Estate</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#ddd; margin-top:-10px'>✨ ذكاء عقاري، تحليل شامل، تقارير فخمة</p>", unsafe_allow_html=True)
st.markdown("---")

# ------------------ اختيار فئة العميل ------------------
st.header("🎯 أخبرنا من أنت")
client_types = [
    "مستثمر فردي", "وسيط عقاري", "شركة تطوير", "باحث عن سكن",
    "ممول عقاري", "مستشار عقاري", "مالك عقار", "مستأجر",
    "مطور صغير", "مدير صندوق استثمار", "خبير تقييم", "طالب دراسة جدوى"
]

cols = st.columns(4)
selected_client = None
for idx, client in enumerate(client_types):
    if cols[idx%4].button(f"أنا {client}", key=f"client_{idx}"):
        selected_client = client

if selected_client is None:
    selected_client = client_types[0]
    st.info(f"تم افتراض نوع العميل: **{selected_client}** — يمكنك تغييره بالضغط على بطاقة أخرى.", icon="ℹ️")

# ------------------ اختيار الباقة ------------------
st.header("📦 اختر باقتك المفضلة")
packages = {
    "مجانية": {
        "description": [
            "تحليل سريع لموقع واحد",
            "مؤشرات سعرية أساسية",
            "مخطط رسوم بيانية مبسط",
            "تقرير PDF مختصر"
        ],
        "price_sar": 0
    },
    "متوسطة": {
        "description": [
            "تحليل 3 مواقع",
            "مؤشرات سعرية وتوصيات أولية",
            "تنبؤ 30 يوم لأسعار العقارات",
            "تقرير PDF مفصل"
        ],
        "price_sar": 150
    },
    "جيدة": {
        "description": [
            "تحليل شامل 5 مواقع",
            "توصيات استثمارية دقيقة",
            "تنبؤ 30 و90 يوم",
            "تقرير PDF مصمم بالهوية الذهبية"
        ],
        "price_sar": 300
    },
    "ممتازة": {
        "description": [
            "تحليل شامل لكل المواقع المطلوبة",
            "توصيات استثمارية + مقارنة عروض المنافسين",
            "تنبؤ مفصل 30 و90 يوم مع توقعات النمو",
            "تقرير PDF شامل، جاهز للتحميل"
        ],
        "price_sar": 500
    }
}

package_cols = st.columns(4)
selected_package = None
for idx, (pkg, info) in enumerate(packages.items()):
    with package_cols[idx]:
        st.markdown(f"<div class='card'><div class='package-title'>{pkg}</div>"
                    f"<div class='package-desc'>{'<br>'.join(info['description'])}</div>"
                    f"<p class='gold'>السعر: {info['price_sar']} ريال</p></div>", unsafe_allow_html=True)
        if st.button(f"اختر {pkg}", key=f"pkg_{idx}"):
            selected_package = pkg

if selected_package is None:
    selected_package = "مجانية"

st.info(f"لقد اخترت الباقة: **{selected_package}**", icon="✨")

# ------------------ إعدادات البحث ------------------
st.header("🔍 إعدادات التحليل")
city = st.selectbox("💠 اختر المدينة", ["الرياض", "جدة", "الدمام", "مكة", "المدينة", "الخبر", "الطائف"])
property_type = st.selectbox("🏷️ نوع العقار", [
    "شقة", "فيلا", "أرض", "دوبلكس", "محل تجاري", "مكتب", "استوديو", "عمارة", "مزرعة", "مستودع", "شاليه"
])
num_properties = st.slider("📊 عدد العقارات في التحليل", min_value=100, max_value=5000, value=500, step=100)

# ------------------ زر جلب البيانات ------------------
scraper = RealEstateScraper()
df_placeholder = st.empty()
info_placeholder = st.empty()

if st.button("💎 اطلب التحليل الآن", key="fetch_analysis"):
    start_time = time.time()
    with st.spinner("⏳ جاري جلب البيانات ومعالجة التحليل..."):
        df = scraper.get_real_data(city=city, property_type=property_type, num_properties=num_properties)
    duration = time.time() - start_time

    total_count = len(df)
    avg_price = int(df['السعر'].dropna().astype(float).mean()) if 'السعر' in df.columns else 0

    # ------------------ نموذج تنبؤ مبسط ------------------
    predictions_30, predictions_90 = None, None
    ai_message = "نموذج التنبؤ لم يُفعّل (بيانات غير كافية)."
    numeric_cols = ['المساحة', 'غرف', 'حمامات', 'عمر_العقار']
    available_cols = [c for c in numeric_cols if c in df.columns]
    try:
        if 'السعر' in df.columns and len(df) >= 50 and len(available_cols) >= 2:
            X = df[available_cols].apply(pd.to_numeric, errors='coerce').fillna(1)
            y = pd.to_numeric(df['السعر'], errors='coerce')
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            base_x = X_test.median().to_frame().T
            pred_now = model.predict(base_x)[0]
            predictions_30 = int(pred_now * 1.03)
            predictions_90 = int(pred_now * 1.08)
            ai_message = "✅ تم تدريب نموذج تنبؤ وعرض النتائج (محاكاة)."
    except:
        ai_message = "⚠️ فشل تدريب نموذج التنبؤ."

    info_html = f"""
    <div class='card'>
        <h3 class='gold'>🛰️ ملخص التحليل</h3>
        <p class='small-muted'>المدينة: <b>{city}</b> · نوع العقار: <b>{property_type}</b></p>
        <p>عدد السجلات: <b>{total_count}</b> · متوسط السعر: <b>{avg_price:,.0f} ريال</b></p>
        <p class='small-muted'>{ai_message}</p>
    </div>
    """
    info_placeholder.markdown(info_html, unsafe_allow_html=True)
    df_placeholder.dataframe(df.head(50))

    # ------------------ إنشاء PDF ------------------
    def create_pdf(client, package, city, df, pred30, pred90):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, f"Warda Smart Real Estate - {client}", ln=True, align='C')
        pdf.ln(5)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 8, f"الباقة: {package}", ln=True)
        pdf.cell(0, 8, f"المدينة: {city}", ln=True)
        pdf.ln(5)
        if pred30 and pred90:
            pdf.cell(0, 8, f"توقع سعر العقار خلال 30 يوم: {pred30:,.0f} ريال", ln=True)
            pdf.cell(0, 8, f"توقع سعر العقار خلال 90 يوم: {pred90:,.0f} ريال", ln=True)
        pdf.ln(5)
        pdf.cell(0, 8, f"ملخص أول 10 سجلات:", ln=True)
        for i, row in df.head(10).iterrows():
            pdf.multi_cell(0, 6, str(row.to_dict()))
        pdf_output = BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)
        return pdf_output

    pdf_file = create_pdf(selected_client, selected_package, city, df, predictions_30, predictions_90)

    st.download_button(
        label="📥 حمل تقريرك الآن",
        data=pdf_file,
        file_name=f"warda_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
        mime="application/pdf"
    )

    # ------------------ زر PayPal ------------------
    paypal_email = "zeghloulwarda6@gmail.com"
    price_sar = packages[selected_package]['price_sar']
    paypal_link = f"https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business={paypal_email}&currency_code=SAR&amount={price_sar}&item_name=Warda+Smart+Real+Estate+{selected_package}"
    st.markdown(f"<a class='btn-paypal' href='{paypal_link}' target='_blank'>💳 ادفع الآن عبر PayPal</a>", unsafe_allow_html=True)

    # ------------------ زر WhatsApp ------------------
    st.markdown("<br>")
    st.markdown("<a class='btn-paypal' style='background:#25D366;' href='https://wa.me/213000000000' target='_blank'>💬 تواصل معنا عبر WhatsApp</a>", unsafe_allow_html=True)
