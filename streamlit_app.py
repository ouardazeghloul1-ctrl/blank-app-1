import streamlit as st
from fpdf import FPDF

# إعداد الصفحة
st.set_page_config(page_title="منصة وردة الذكية للعقارات", layout="centered")

# تصميم الواجهة (أسود وذهبي)
st.markdown("""
    <style>
    body { background-color: black; color: gold; }
    .stApp { background-color: black; color: gold; }
    .stTextInput, .stSelectbox, .stNumberInput, .stButton > button {
        background-color: #111;
        color: gold;
        border: 1px solid gold;
        border-radius: 10px;
    }
    .stButton > button:hover {
        background-color: gold;
        color: black;
    }
    .password-button {
        position: fixed;
        bottom: 15px;
        right: 15px;
        background-color: #111;
        color: gold;
        border: 1px solid gold;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        text-align: center;
        font-size: 22px;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# عنوان التطبيق
st.markdown("<h1 style='text-align:center; color:gold;'>🏡 منصة وردة الذكية للعقارات</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#bbb;'>اختر(ي) مدينتك، نوع العقار، وعدد العقارات لتحليل ذكي دقيق 🔍</p>", unsafe_allow_html=True)

# واجهة اختيار البيانات
st.subheader("🔍 اختر المدينة والفئة لتحليل العقارات:")

col1, col2 = st.columns(2)
with col1:
    city = st.selectbox("🏙️ المدينة", ["الرياض", "جدة", "الدمام", "مكة", "المدينة"])
with col2:
    category = st.selectbox("🏘️ الفئة", ["شقق", "فلل", "أراضي", "مكاتب", "محلات"])

col3, col4 = st.columns(2)
with col3:
    property_type = st.selectbox("🏗️ نوع العقار", ["سكني", "تجاري", "استثماري"])
with col4:
    status = st.selectbox("📈 الحالة", ["بيع", "شراء", "إيجار"])

num_properties = st.slider("🏢 عدد العقارات للتحليل", 100, 1000, 500)

# اختيار الباقة
st.subheader("💎 اختر الباقة المناسبة لك:")
packages = {
    "مجانية": {"price": 0, "features": "تحليل سريع لعقار واحد + تقرير PDF"},
    "فضية": {"price": 12, "features": "تحليل دقيق + متوسط الأسعار + نصائح + تقرير PDF"},
    "ذهبية": {"price": 28, "features": "تحليل متقدم + تنبؤ ذكي + أفضل وقت للبيع + تقرير PDF"},
    "ماسية": {"price": 55, "features": "تحليل شامل + مقارنة مشاريع + تنبؤ ذكي + تقرير PDF فاخر"}
}
selected_package = st.selectbox("💼 الباقة", list(packages.keys()))
price = packages[selected_package]["price"]
features = packages[selected_package]["features"]

st.markdown(f"""
<div style='background-color:#111; padding:10px; border-radius:10px; border:1px solid gold;'>
<strong>💰 السعر:</strong> {price} دولار<br>
<strong>✨ مميزات الباقة:</strong> {features}
</div>
""", unsafe_allow_html=True)

# زر إنشاء التقرير
if st.button("📄 تحميل تقريرك PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('Amiri', '', 'Amiri-Regular.ttf', uni=True)
    pdf.set_font('Amiri', '', 14)
    pdf.cell(0, 10, txt="تقرير التحليل العقاري", ln=True, align='C')
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"""
    المدينة: {city}
    الفئة: {category}
    نوع العقار: {property_type}
    الحالة: {status}
    عدد العقارات: {num_properties}
    الباقة المختارة: {selected_package}
    السعر بالدولار: {price}
    المميزات: {features}
    """)
    pdf.output("تقرير_وردة.pdf")
    st.success("تم إنشاء التقرير بنجاح ✅")
    st.download_button("⬇️ تحميل التقرير PDF", data=open("تقرير_وردة.pdf", "rb"), file_name="تقرير_وردة.pdf")

# زر المؤثرين (سري)
st.markdown("<div class='password-button'>🔑</div>", unsafe_allow_html=True)

# إدخال كلمة السر عند الضغط
show_panel = st.text_input("كلمة السر (خاصة بالمؤثرين):", type="password")

if show_panel == "Warda2025":
    st.success("تم فتح لوحة المؤثرين ✅")
    st.markdown("""
        ### 🎯 لوحة المؤثرين
        يمكنك توليد روابط خاصة تمنح المستخدمين تقارير مجانية ليوم واحد فقط.
        """)
    influencer_name = st.text_input("اسم المؤثر:")
    if st.button("🔗 إنشاء رابط مؤقت"):
        st.success(f"✅ تم إنشاء رابط خاص لـ {influencer_name} صالح لمدة 24 ساعة.")
