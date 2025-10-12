import streamlit as st
from fpdf import FPDF
from io import BytesIO

# ====== تصميم الصفحة ======
st.set_page_config(page_title="منصة تحليل العقارات", page_icon="🏠", layout="wide")
st.markdown("""
<style>
body {
    background-color: #000000;
    color: #FFD700;
    font-family: 'Arial', sans-serif;
}
.stButton>button {
    background-color: #FFD700;
    color: #000000;
    font-weight: bold;
    border-radius: 10px;
    padding: 10px 20px;
    margin: 5px 0px;
}
.stDownloadButton>button {
    background-color: #FFD700;
    color: #000000;
    font-weight: bold;
    border-radius: 10px;
    padding: 10px 20px;
    margin: 5px 0px;
}
.stTextInput>div>input {
    background-color: #333333;
    color: #FFD700;
}
</style>
""", unsafe_allow_html=True)

st.title("🏠 منصة تحليل العقارات – تقريرك في دقائق")
st.subheader("اختر هويتك لتبدأ التحليل:")

# ====== فئات متعددة ======
factions = [
    "أنا مستشار عقاري",
    "أنا فرد يبحث عن عقار",
    "أنا صاحب عقار",
    "أنا مستثمر",
    "أنا مطور عقاري",
    "أنا شركة عقارات",
    "أنا مستأجر",
    "أنا باحث عن فرص استثمارية",
    "أنا طالب دراسة سوق العقارات",
    "أنا مستثمر دولي"
]
selected_faction = st.radio("من أنت؟", factions)

st.markdown("---")
st.subheader("اختر الباقة:")

# ====== باقات مع أسعار وتفاصيل ======
packages = {
    "باقة أساسية": {"price": 50, "details": "تحليل أساسي لكل العقارات مع النصائح الأولية"},
    "باقة متقدمة": {"price": 100, "details": "تحليل متعمق مع توقعات الأسعار ومستقبل السوق"},
    "باقة احترافية": {"price": 200, "details": "تقرير كامل + توقعات دقيقة + نصائح استثمارية مخصصة"}
}
selected_package = st.selectbox(
    "اختر الباقة التي تناسبك",
    list(packages.keys())
)
st.write(f"💰 السعر: {packages[selected_package]['price']}$")
st.write(f"📄 التفاصيل: {packages[selected_package]['details']}")

st.markdown("---")
st.subheader("أدخل معلوماتك الأساسية لإصدار التقرير:")
client_name = st.text_input("الاسم الكامل")
client_email = st.text_input("البريد الإلكتروني")

# ====== زر إنشاء التقرير ======
if st.button("حمل تقريرك الآن 📄"):

    # إنشاء PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("ArialUnicode", "", "arial.ttf", uni=True)
    pdf.set_font("ArialUnicode", '', 14)

    pdf.cell(0, 10, f"تقرير تحليل العقارات", ln=True)
    pdf.cell(0, 10, f"العميل: {client_name}", ln=True)
    pdf.cell(0, 10, f"البريد: {client_email}", ln=True)
    pdf.cell(0, 10, f"الفئة: {selected_faction}", ln=True)
    pdf.cell(0, 10, f"الباقة: {selected_package}", ln=True)
    pdf.multi_cell(0, 10, f"تفاصيل التحليل: {packages[selected_package]['details']}\n\nتوقعات السوق والنصائح الاستثمارية: هذا القسم يتضمن كل ما تحتاجه لتنجح في استثماراتك العقارية بطريقة ذكية واحترافية.")

    # حفظ PDF في الذاكرة
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)

    st.download_button(
        label="تحميل التقرير الآن PDF",
        data=pdf_buffer,
        file_name="تقرير_العقارات.pdf",
        mime="application/pdf"
    )

# ====== زر بايبال ======
st.markdown("---")
paypal_email = "zeghloulwarda6@gmail.com"
st.markdown(f"""
<a href="https://www.paypal.com/paypalme/{paypal_email}" target="_blank">
<button>💳 دفع عبر PayPal</button>
</a>
""", unsafe_allow_html=True)

# ====== زر واتساب ======
whatsapp_number = "0000000000"  # ضع رقمك هنا بصيغة 966xxxxxxxxx بدون +
st.markdown(f"""
<a href="https://wa.me/{whatsapp_number}" target="_blank">
<button>💬 تواصل معنا عبر WhatsApp</button>
</a>
""", unsafe_allow_html=True)
