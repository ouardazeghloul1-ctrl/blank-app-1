import streamlit as st
from fpdf import FPDF
import os
import uuid

# إعداد الصفحة
st.set_page_config(page_title="منصتك العقارية الذكية", layout="centered")

# تحميل الخط العربي
if not os.path.exists("Amiri-Regular.ttf"):
    st.error("❌ ملف الخط Amiri-Regular.ttf غير موجود في مجلد المشروع.")
else:
    pdf_font = "Amiri-Regular.ttf"

# تنسيق الواجهة
st.markdown("""
    <style>
        body { background-color: black; color: gold; }
        .stApp { background-color: black; color: gold; }
        div[data-testid="stForm"] { background-color: #111; padding: 30px; border-radius: 20px; }
        h1, h2, h3, h4 { color: gold; text-align: center; }
        .stButton>button {
            background-color: gold;
            color: black;
            font-weight: bold;
            border-radius: 10px;
            border: none;
            padding: 10px 25px;
        }
        .stButton>button:hover {
            background-color: #b8860b;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# بيانات الباقات
plans = {
    "مجانية": {
        "price": 0,
        "features": [
            "تحليل سريع لعقار واحد بدون تفاصيل مالية دقيقة"
        ]
    },
    "فضية": {
        "price": 10,
        "features": [
            "تحليل دقيق",
            "متوسط الأسعار في المنطقة",
            "نصائح استثمارية"
        ]
    },
    "ذهبية": {
        "price": 30,
        "features": [
            "تحليل دقيق + كل مزايا الباقة الفضية",
            "تحليل ذكي بالذكاء الاصطناعي",
            "تنبؤ بالسعر المستقبلي",
            "اقتراح أفضل وقت للبيع"
        ]
    },
    "ماسية": {
        "price": 60,
        "features": [
            "كل مزايا الباقة الذهبية",
            "تحليل ذكي بالذكاء الاصطناعي متطور",
            "مقارنة مع مشاريع مماثلة",
            "تقرير فاخر بتصميم مميز"
        ]
    }
}

# عنوان التطبيق
st.title("🏡 منصتك العقارية الذكية")
st.write("اختار(ي) الباقة التي تناسبك لتحليل عقارك بدقة واحترافية")

# قسم رابط المؤثرين
st.write("---")
st.subheader("🎁 رابط المؤثرين (تجربة مجانية لمرة واحدة فقط)")

if "used_free_link" not in st.session_state:
    st.session_state.used_free_link = False

if not st.session_state.used_free_link:
    if st.button("🔗 إنشاء رابط مجاني"):
        unique_link = str(uuid.uuid4())[:8]
        st.session_state.free_link = f"https://example.com/free-access/{unique_link}"
        st.session_state.used_free_link = True
        st.success(f"✅ تم إنشاء الرابط المجاني لمرة واحدة فقط:\n\n{st.session_state.free_link}")
else:
    st.info("🔒 لقد استخدمت الرابط المجاني بالفعل.")

st.write("---")

# اختيار الباقة
plan_name = st.selectbox("🎯 اختر(ي) الباقة:", list(plans.keys()))
selected_plan = plans[plan_name]

st.subheader(f"💰 السعر: {selected_plan['price']} دولار")
st.write("### ⭐ مميزات الباقة:")
for feature in selected_plan["features"]:
    st.markdown(f"- {feature}")

# إدخال معلومات العقار
st.write("---")
st.subheader("📋 أدخل(ي) تفاصيل العقار:")
property_name = st.text_input("اسم العقار:")
property_location = st.text_input("الموقع:")
property_size = st.text_input("المساحة (م²):")
property_price = st.text_input("السعر الحالي (بالدولار):")

# زر التحليل
if st.button("🔍 تحليل العقار"):
    if not property_name or not property_location or not property_size or not property_price:
        st.error("❗ الرجاء إدخال جميع المعلومات قبل التحليل.")
    else:
        # إنشاء تقرير PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font("Amiri", "", pdf_font, uni=True)
        pdf.set_font("Amiri", "", 14)

        pdf.cell(0, 10, txt="تقرير التحليل العقاري", ln=True, align="C")
        pdf.cell(0, 10, txt=f"اسم العقار: {property_name}", ln=True)
        pdf.cell(0, 10, txt=f"الموقع: {property_location}", ln=True)
        pdf.cell(0, 10, txt=f"المساحة: {property_size} م²", ln=True)
        pdf.cell(0, 10, txt=f"السعر الحالي: {property_price} دولار", ln=True)
        pdf.cell(0, 10, txt=f"الباقة المختارة: {plan_name}", ln=True)

        pdf.ln(10)
        pdf.cell(0, 10, txt="مميزات التحليل:", ln=True)
        for f in selected_plan["features"]:
            pdf.cell(0, 10, txt=f"• {f}", ln=True)

        pdf_file = f"تقرير_{property_name}.pdf"
        pdf.output(pdf_file)
        with open(pdf_file, "rb") as f:
            st.download_button(
                label="📥 تحميل التقرير (PDF)",
                data=f,
                file_name=pdf_file,
                mime="application/pdf"
            )

        st.success("✅ تم تحليل العقار وإنشاء التقرير بنجاح!")

# حقوق المنصة
st.write("---")
st.markdown("👑 **© جميع الحقوق محفوظة لـ Warda Intelligence**")
st.caption("منصة تحليل واستشارات عقارية مدعومة بالذكاء الاصطناعي.")
