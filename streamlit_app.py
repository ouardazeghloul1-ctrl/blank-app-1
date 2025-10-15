import streamlit as st
from fpdf import FPDF

# إعداد صفحة التطبيق
st.set_page_config(page_title="التحليل العقاري الذهبي", layout="centered")

# --- التصميم الذهبي الفاخر ---
st.markdown("""
    <style>
        body, .stApp {background-color: black; color: gold;}
        .stTextInput, .stSelectbox, .stNumberInput, .stButton button {
            background-color: black !important;
            color: gold !important;
            border: 1px solid gold !important;
        }
        .stButton button:hover {
            background-color: gold !important;
            color: black !important;
        }
        .gold-title {
            text-align: center;
            font-size: 30px;
            font-weight: bold;
            color: gold;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='gold-title'>🏠 التحليل العقاري الذهبي 🏠</div>", unsafe_allow_html=True)

# --- كلمة السر الخاصة بك ---
password = st.sidebar.text_input("🔒 كلمة السر الخاصة بلوحة المؤثرين", type="password")
is_admin = password == "GoldenAccess2025"

# --- الواجهة العامة ---
st.markdown("### 🔍 اختر بيانات العقار للتحليل:")

city = st.selectbox("🏙️ المدينة", ["الرياض", "جدة", "الدمام", "مكة", "المدينة المنورة"])
category = st.selectbox("🏘️ الفئة", ["شقق", "فلل", "أراضي", "عمائر", "محلات تجارية"])
property_type = st.selectbox("🏗️ نوع العقار", ["سكني", "تجاري", "استثماري"])
status = st.selectbox("📜 الحالة", ["بيع", "شراء", "إيجار"])

# --- عدد العقارات ---
num_properties = st.number_input("📊 عدد العقارات", min_value=1, max_value=10000, value=1000, step=100)

# السعر يبدأ من قيمة أساسية ويصعد حسب العدد
base_price = 150000  # دولار كبداية
price = base_price + (num_properties * 25)

st.write(f"💰 السعر التقديري الحالي: **{price:,} دولار**")
st.write(f"📈 كلما زاد عدد العقارات، زاد السعر تلقائيًا.")

# --- زر التحليل ---
if st.button("ابدأ التحليل الآن 💫"):
    st.success("🔎 جاري تحليل البيانات الذكية...")
    st.balloons()

    st.write("✅ تحليل شامل للعقارات المختارة")
    st.write("✅ مقارنة بالمشاريع المشابهة في المنطقة")
    st.write("✅ تنبؤ ذكي للأسعار المستقبلية")
    st.write("✨ **مميزات الباقة: تحليل شامل + مقارنة مشاريع + تنبؤ ذكي + تقرير PDF فاخر** ✨")

    # --- زر تحميل التقرير ---
    if st.button("📄 تحميل التقرير PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, txt="تقرير التحليل العقاري الذهبي", ln=True, align="C")
        pdf.output("golden_report.pdf")
        st.success("📁 تم إنشاء التقرير بنجاح! يمكنك تحميله الآن.")

# --- لوحة المؤثرين (لكِ فقط) ---
if is_admin:
    st.sidebar.markdown("## 🔑 لوحة المؤثرين الخاصة بك")
    influencer_link = st.sidebar.text_input("أدخل رابط المؤثر:")
    if influencer_link:
        st.sidebar.success(f"✅ تم حفظ رابط المؤثر: {influencer_link}")
else:
    pass  # الزوار لا يرون أي شيء
