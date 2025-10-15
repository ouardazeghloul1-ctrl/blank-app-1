import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime
import plotly.express as px
import io
import zipfile

# إعداد الصفحة
st.set_page_config(page_title="Warda Intelligence", layout="wide")

# تنسيق فاخر
st.markdown("""
<style>
.main {background-color: #0E1117; color: gold;}
h1,h2,h3,h4,h5,h6 {color: gold !important;}
.stButton>button {background-color: gold; color: black; font-weight: bold; border-radius: 10px; width: 100%;}
.package-card {background: linear-gradient(135deg, #2d2d2d, #1a1a1a); padding: 15px; border-radius: 10px; border: 2px solid #d4af37; text-align: center;}
</style>
""", unsafe_allow_html=True)

# العنوان
st.markdown("<h1 style='text-align: center; color: gold;'>🏙️ Warda Intelligence - التحليل العقاري الذهبي</h1>", unsafe_allow_html=True)

# الباقات
PACKAGES = {
    "مجانية": {"price": 0, "features": ["تحليل أساسي", "أسعار متوسطة", "تقرير TXT", "عقار واحد"]},
    "فضية": {"price": 29, "features": ["كل المجانية +", "تنبؤ 6 أشهر", "PDF", "رسوم بيانية", "5 منافسين"]},
    "ذهبية": {"price": 79, "features": ["كل الفضية +", "AI متقدم", "تنبؤ سنة", "10 منافسين", "مخاطر متقدمة"]},
    "ماسية": {"price": 149, "features": ["كل الذهبية +", "تحليل شامل", "كل المدن", "خطة استثمارية"]}
}

# قراءة بيانات السكريبر
@st.cache_data(ttl=604800)
def load_real_data(city, property_type):
    try:
        if os.path.exists("outputs"):
            files = [f for f in os.listdir("outputs") if f.startswith(f"{city}_")]
            if files:
                latest = max(files, key=lambda x: os.path.getctime(f"outputs/{x}"))
                return pd.read_csv(f"outputs/{latest}")
    except:
        pass
    return pd.DataFrame()

# بيانات السوق
def get_market_data(city, property_type):
    df = load_real_data(city, property_type)
    if not df.empty:
        price_col = next((c for c in ['price', 'Price', 'السعر'] if c in df.columns), None)
        if price_col:
            avg = df[price_col].mean()
            vol = len(df)
            hist = pd.DataFrame({'year': [2024, 2025], 'price': [avg*0.92, avg]})
            model = LinearRegression().fit(hist[['year']], hist['price'])
            return {
                'price': avg, 'high': df[price_col].max(), 'low': df[price_col].min(),
                'volume': vol, 'roi': 8.5, 'growth': 0.65, 'hist': hist,
                'future1': model.predict([[2026]])[0],
                'future3': model.predict([[2028]])[0],
                'future5': model.predict([[2030]])[0],
                'source': f"بيانات حية | {datetime.now().strftime('%Y-%m-%d')} | {vol} عقار"
            }
    return {
        'price': 4500, 'high': 6000, 'low': 3000, 'volume': 150, 'roi': 8.5, 'growth': 0.65,
        'hist': pd.DataFrame({'year': [2024, 2025], 'price': [4200, 4500] }),
        'future1': 4800, 'future3': 5200, 'future5': 5800,
        'source': "بيانات Warda Intelligence"
    }

# PDF نصي بسيط
def create_pdf(report, sources):
    buffer = io.BytesIO()
    buffer.write(f"Warda Intelligence - تقرير احترافي\n{sources}\n\n".encode('utf-8'))
    buffer.write(report.encode('utf-8'))
    buffer.seek(0)
    return buffer

# إنشاء رسوم كـ PNG باستخدام plotly
def create_figs(figs_data):
    img_buffers = []
    for i, (title, data) in enumerate(figs_data):
        if 'year' in data:
            fig = px.line(x=data['year'], y=data['price'], title=title, template='plotly_dark', color_discrete_sequence=['gold'])
        elif 'values' in data:
            fig = px.pie(values=data['values'], names=data['labels'], title=title, template='plotly_dark', color_discrete_sequence=['gold', 'gray'])
        elif 'x' in data:
            fig = px.bar(x=data['x'], y=data['y'], title=title, template='plotly_dark', color_discrete_sequence=['gold'])
        img_buffer = io.BytesIO()
        fig.write_image(img_buffer, format='png', width=800, height=400)
        img_buffer.seek(0)
        img_buffers.append((f"رسم_{i+1}.png", img_buffer.getvalue()))
    return img_buffers

# التحليل
def get_analysis(user_type):
    return {
        "التحليل المالي": "ROI: 9.5% | NPV: +45K$ | تدفق سنة 1: $19,200",
        "الاستراتيجية": "شقق 40% | محلات 30% | فيلات 20% | أراضي 10%",
        "المخاطر": "منخفضة 60% | متوسطة 30% | عالية 10%",
        "الفرص": "نيوم 18% | الدرعية 14% | المالي 12%"
    }

# تقرير كامل
def generate_report(user_type, city, prop_type, area, status, pkg, count):
    price = PACKAGES[pkg]["price"] * count
    data = get_market_data(city, prop_type)
    analysis = get_analysis(user_type)
    
    report = f"""🏙️ تقرير Warda Intelligence
فئة: {user_type} | {city} | {prop_type}
تاريخ: {datetime.now().strftime('%Y-%m-%d')}
سعر: ${price} | مساحة: {area}م²

📈 ملخص:
ROI: {data['roi']}% | نمو: {data['growth']*12:.1f}%
سعر: {data['price']:,.0f}ر

💰 {analysis['التحليل المالي']}
🎯 {analysis['الاستراتيجية']}
🛡️ {analysis['المخاطر']}
🚀 {analysis['الفرص']}

{data['source']}"""
    
    # بيانات الرسوم
    figs_data = [
        ('نمو الأسعار', {'year': data['hist']['year'], 'price': data['hist']['price']}),
        ('العوائد', {'values': [data['roi'], 100-data['roi']], 'labels': ['عائد', 'مخاطر']}),
        ('المحفظة', {'x': ['شقق', 'محلات', 'فيلات', 'أراضي'], 'y': [40, 30, 20, 10]}),
        ('المخاطر', {'values': [30, 25, 20], 'labels': ['سوق', 'تشغيل', 'تمويل']}),
        ('الفرص', {'x': ['نيوم', 'الدرعية', 'المالي'], 'y': [18, 14, 12]})
    ]
    
    return report, price, figs_data, data['source']

# === الواجهة ===
col1, col2 = st.columns(2)

with col1:
    st.header("👤 البيانات")
    user_type = st.selectbox("الفئة", ["مستثمر", "وسيط", "شركة", "فرد"])
    city = st.selectbox("المدينة", ["الرياض", "جدة", "الدمام"])
    prop_type = st.selectbox("النوع", ["شقة", "فيلا", "أرض", "محل"])
    status = st.selectbox("الحالة", ["للبيع", "للشراء"])
    area = st.slider("المساحة", 50, 1000, 120)

with col2:
    st.header("💎 الباقة")
    count = st.slider("عدد العقارات", 1, 10, 1)
    pkg = st.radio("الباقة", list(PACKAGES))
    total = PACKAGES[pkg]["price"] * count
    
    st.markdown(f"""
    <div class='package-card'>
    <h3>{pkg}</h3><h2>${total}</h2>
    </div>
    """, unsafe_allow_html=True)
    for f in PACKAGES[pkg]["features"]:
        st.write(f"✅ {f}")

# الدفع
st.markdown("---")
st.markdown(f"### 💰 **الإجمالي: ${total}**")
st.markdown(f"""
<form action="https://www.paypal.com/cgi-bin/webscr" method="post">
<input type="hidden" name="cmd" value="_xclick">
<input type="hidden" name="business" value="warda.intelligence@gmail.com">
<input type="hidden" name="item_name" value="تقرير {pkg}">
<input type="hidden" name="amount" value="{total}">
<input type="hidden" name="currency_code" value="USD">
<input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_buynow_LG.gif" style="display:block;margin:0 auto;">
</form>
""", unsafe_allow_html=True)

# إنشاء التقرير
if st.button("🎯 إنشاء التقرير", use_container_width=True):
    with st.spinner("جاري الإنشاء..."):
        time.sleep(2)
        report, price, figs_data, source = generate_report(user_type, city, prop_type, area, status, pkg, count)
        st.session_state.report = report
        st.session_state.figs_data = figs_data
        st.session_state.source = source
        st.session_state.ready = True
        st.success("✅ تم!")

# عرض التقرير
if st.session_state.get('ready', False):
    st.markdown("---")
    st.markdown("## 📊 التقرير الكامل")
    st.text_area("", st.session_state.report, height=300)
    
    # تحميل TXT
    st.download_button("📥 TXT", st.session_state.report, f"تقرير_{city}_{datetime.now().strftime('%Y%m%d')}.txt")
    
    # تحميل PDF نصي
    pdf_buffer = create_pdf(st.session_state.report, st.session_state.source)
    st.download_button("📥 PDF نصي", pdf_buffer, f"تقرير_{city}_{datetime.now().strftime('%Y%m%d')}.pdf", "application/pdf")
    
    # تحميل ZIP مع رسوم
    img_buffers = create_figs(st.session_state.figs_data)
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('تقرير.txt', st.session_state.report)
        for filename, img_data in img_buffers:
            zf.writestr(filename, img_data)
    zip_buffer.seek(0)
    st.download_button("📦 ZIP (نص + 5 رسوم)", zip_buffer, f"تقرير_كامل_{city}_{datetime.now().strftime('%Y%m%d')}.zip", "application/zip")
    
    st.markdown("[📤 مشاركة على X](https://x.com/intent/tweet?text=تقرير عقاري رائع من Warda! #عقارات_السعودية)")
    st.balloons()

# Sidebar المسؤول
admin = st.sidebar.text_input("كلمة المرور", type="password")
if admin == "Warda2024":
    if st.sidebar.button("🔄 تحديث البيانات"):
        st.sidebar.success("✅ جاري...")

# المؤثرين
if st.query_params.get('promo'):
    st.success("🎁 عرض المؤثرين!")
    if st.button("تقرير مجاني"):
        if not st.session_state.get('used', False):
            report, _, figs_data, source = generate_report("مؤثر", "الرياض", "شقة", 120, "للبيع", "ذهبية", 1)
            st.session_state.used = True
            st.download_button("📥 مجاني", report, "مجاني_مؤثر.txt")

# اتصال
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**واتساب:** +213779888140<br>**بريد:** info@warda-intelligence.com")
with col2:
    st.markdown("**موقع:** www.warda-intelligence.com<br>**ساعات:** 9ص-6م")
