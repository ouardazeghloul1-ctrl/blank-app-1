import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="تحليل عقاري ذهبي", layout="centered")

# ===== واجهة سوداء وذهبية فخمة =====
st.markdown("""
    <style>
        body, .stApp { background-color: black; color: gold; font-family: 'Amiri', serif; }
        .title { color: gold; text-align: center; font-size: 32px; font-weight: bold; margin-bottom: 20px; }
        .stButton>button { background-color: gold; color: black; border-radius: 12px; font-weight: bold; }
        .stSelectbox label, .stTextInput label, .stNumberInput label { color: gold !important; }
        .hidden {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>💎 منصة التحليل العقاري الذكي</div>", unsafe_allow_html=True)

# ========== كلمة سر الإدارة ==========
admin_mode = False
password = st.text_input("🔒 إدخال كلمة السر (خاص بصاحبة المنصة):", type="password")
if password == "adminWarda123":
    admin_mode = True
    st.success("تم الدخول إلى وضع الإدارة ✅")

# ========== اختيار المدينة ==========
city = st.selectbox("🏙️ اختر(ي) المدينة:", ["الرياض", "جدة", "الدمام"])

# ========== نوع العقار ==========
property_type = st.selectbox("🏠 نوع العقار:", ["شقة", "فيلا", "أرض", "عمارة", "محل تجاري"])

# ========== حالة العقار ==========
status = st.selectbox("📊 الحالة:", ["بيع", "شراء", "إيجار"])

# ========== عدد العقارات ==========
property_count = st.number_input("🔢 عدد العقارات للتحليل:", min_value=1, max_value=50, value=1)

# ========== اختيار الباقة ==========
st.subheader("💼 اختر(ي) الباقة:")
plans = {
    "مجانية": {"price": 0, "features": "تحليل سريع لعقار واحد بدون تفاصيل مالية دقيقة + تقرير PDF"},
    "فضية": {"price": 10, "features": "تحليل دقيق + متوسط الأسعار + نصائح استثمارية + تقرير PDF"},
    "ذهبية": {"price": 30, "features": "كل ما سبق + تنبؤ ذكي بالأسعار + اقتراح وقت البيع + تقرير PDF"},
    "ماسية": {"price": 55, "features": "تحليل شامل + مقارنة مشاريع + تنبؤ ذكي + تقرير PDF فاخر"}
}

plan = st.selectbox("📦 الباقة:", list(plans.keys()))

# ===== السعر الإجمالي =====
total_price = plans[plan]["price"] * property_count
st.write(f"💰 **السعر الإجمالي:** {total_price} دولار")

# ===== عرض المميزات =====
st.markdown(f"📝 **مميزات الباقة:** {plans[plan]['features']}")

# ===== زر التحليل =====
if st.button("🚀 تحليل العقار الآن"):
    st.success("✅ تم توليد التقرير بنجاح!")
    st.download_button("📄 تحميل التقرير (PDF)", "تقرير_عقاري.pdf")

# ===== قسم خاص بالمؤثرين (يظهر فقط للإدارة) =====
if admin_mode:
    st.markdown("---")
    st.markdown("🎯 **رابط خاص للمؤثرين** — صالح لمدة 24 ساعة ولمرة واحدة فقط")

    if st.button("🔗 إنشاء رابط مؤثر جديد"):
        unique_code = random.randint(100000, 999999)
        expiry = datetime.now() + timedelta(hours=24)
        influencer_link = f"https://yourapp.streamlit.app/?token={unique_code}"
        st.info(f"رابط مؤقت للمؤثر: {influencer_link}\n⏰ صالح حتى: {expiry.strftime('%Y-%m-%d %H:%M:%S')}")

st.markdown("<hr>", unsafe_allow_html=True)
st.caption("© منصة التحليل العقاري الذكي - بإدارة الاسم العملي لصاحبة المنصة 🌟")
