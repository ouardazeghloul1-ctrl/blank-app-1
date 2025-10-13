import streamlit as st
from fpdf import FPDF

# إعداد واجهة التطبيق
st.set_page_config(page_title="تحليل عقاري ذهبي", layout="centered")

# CSS لتصميم أسود وذهبي فاخر
st.markdown("""
    <style>
        body { background-color: black; color: gold; }
        .stApp { background-color: black; color: gold; }
        .stTextInput, .stSelectbox, .stNumberInput, .stSlider { color: gold !important; }
        .css-1d391kg, .css-1cpxqw2 { background-color: #111 !important; color: gold !important; }
        .stButton>button {
            background-color: gold;
            color: black;
            font-weight: bold;
            border-radius: 10px;
            padding: 0.6em 1.2em;
            transition: 0.3s;
        }
        .stButton>button:hover { background-color: #d4af37; color: white; }
        h1, h2, h3, h4 { color: gold; text-align: center; }
        .gold-box {
            border: 2px solid gold;
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 15px;
            background-color: #111;
        }
        .center { text-align: center; }
    </style>
""", unsafe_allow_html=True)

# عنوان المنصة
st.markdown("<h1>🏙️ منصة التحليل العقاري الذهبي</h1>", unsafe_allow_html=True)
st.markdown("<p class='center'>حلّل عقارك بدقة واحترافية، واحصل على تقرير PDF فاخر 🔍</p>", unsafe_allow_html=True)

# فئة المستخدم
st.markdown("### من أنت؟")
user_type = st.selectbox("اختر الفئة التي تمثلك:", [
    "مستشار", "مستثمر", "فرد", "شركة تطوير", "وسيط عقاري", "خبير تسويق", "مالك عقار", "باحث عن فرصة"
])

# بيانات العقار
st.markdown("### بيانات العقار 📋")
city = st.text_input("المدينة:")
property_type = st.selectbox("نوع العقار:", ["شقة", "فيلا", "أرض", "محل تجاري", "مبنى إداري", "مزرعة", "شاليه"])
status = st.selectbox("الحالة:", ["للبيع", "للإيجار", "كلاهما"])
count = st.slider("عدد العقارات للتحليل:", 1, 20, 1)

# الباقات
st.markdown("### اختر باقتك 💎")

packages = {
    "مجانية": {"price": 0, "desc": "تحليل أساسي لعقار واحد فقط بدون تنبؤات."},
    "أساسية": {"price": 10, "desc": "تحليل متقدم يشمل الموقع والسوق المحلي."},
    "احترافية": {"price": 25, "desc": "تحليل احترافي مع تنبؤات الأسعار المستقبلية ومؤشرات السوق."},
    "ذهبية": {"price": 50, "desc": "تقرير فاخر PDF يشمل تحليل كامل، تنبؤات دقيقة، وتوصيات استثمارية خاصة."}
}

chosen_pkg = st.radio("اختر باقتك:", list(packages.keys()))
base_price = packages[chosen_pkg]["price"]
total_price = base_price * count

st.markdown(f"""
<div class='gold-box'>
<h3>💰 السعر الإجمالي: {total_price} دولار</h3>
<p>{packages[chosen_pkg]['desc']}</p>
</div>
""", unsafe_allow_html=True)

# زر الدفع (بايبال)
paypal_email = "zeghloulwarda6@gmail.com"
st.markdown(f"""
<div class='center'>
<a href="https://www.paypal.com/paypalme/{paypal_email}/{total_price}" target="_blank">
<button style="background-color:gold;color:black;font-size:18px;padding:10px 20px;border:none;border-radius:10px;">💳 الدفع عبر PayPal</button>
</a>
</div>
""", unsafe_allow_html=True)

# بعد الدفع
st.markdown("### ✅ بعد الدفع يمكنك تحميل تقريرك:")

if st.button("📄 تحميل التقرير الآن"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "تقرير التحليل العقاري الذهبي", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"""
الفئة: {user_type}
المدينة: {city}
نوع العقار: {property_type}
الحالة: {status}
عدد العقارات: {count}
الباقة المختارة: {chosen_pkg}
السعر الإجمالي: {total_price} دولار

📈 يشمل هذا التقرير تحليلاً دقيقاً للعقار بناءً على السوق المحلي، مع تنبؤات الأسعار المستقبلية وفرص الاستثمار المحتملة.
""")

    pdf_file = "تقرير_التحليل_الذهبي.pdf"
    pdf.output(pdf_file)
    with open(pdf_file, "rb") as f:
        st.download_button("📥 اضغط لتحميل تقريرك PDF", data=f, file_name=pdf_file, mime="application/pdf")

# زر واتساب للتواصل
st.markdown("""
<br>
<div class='center'>
<a href="https://wa.me/213000000000" target="_blank">
<button style="background-color:green;color:white;font-size:18px;padding:10px 20px;border:none;border-radius:10px;">💬 تواصل عبر واتساب</button>
</a>
</div>
""", unsafe_allow_html=True)
