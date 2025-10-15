import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import os
import base64

# إعداد الصفحة
st.set_page_config(page_title="التحليل العقاري الذهبي | Warda Intelligence", layout="centered")

# تنسيق واجهة فاخرة
st.markdown("""
    <style>
        body { background-color: black; color: gold; }
        .stApp { background-color: black; color: gold; }
        h1, h2, h3, h4, p, label { color: gold !important; }
        .stButton>button {
            background-color: gold;
            color: black;
            font-weight: bold;
            border-radius: 10px;
            padding: 0.6em 1.2em;
            transition: 0.3s;
        }
        .stButton>button:hover { background-color: #d4af37; color: white; }
        .gold-box {
            border: 2px solid gold;
            padding: 15px;
            border-radius: 12px;
            background-color: #111;
            margin-bottom: 15px;
        }
        .center { text-align: center; }
    </style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown("<h1 class='center'>🏙️ منصة التحليل العقاري الذهبي</h1>", unsafe_allow_html=True)
st.markdown("<p class='center'>تحليل ذكي مدعوم بالذكاء الاصطناعي من منصة Warda Intelligence</p>", unsafe_allow_html=True)

# إدخال بيانات المستخدم
user_type = st.selectbox("👤 اختر(ي) فئتك:", ["مستثمر", "وسيط عقاري", "شركة تطوير", "فرد", "باحث عن فرصة", "مالك عقار"])
city = st.selectbox("🏙️ المدينة:", ["الرياض", "جدة", "الدمام", "مكة المكرمة", "المدينة المنورة", "الخبر", "تبوك", "الطائف"])
property_type = st.selectbox("🏠 نوع العقار:", ["شقة", "فيلا", "أرض", "محل تجاري"])
status = st.selectbox("📌 الحالة:", ["للبيع", "للشراء"])
count = st.slider("🔢 عدد العقارات للتحليل:", 1, 1000, 5)
area = st.slider("📏 متوسط مساحة العقار (م²):", 50, 1000, 150)
rooms = st.slider("🚪 عدد الغرف (تقريبي):", 1, 10, 3)

# الباقات
packages = {
    "مجانية": {"price": 0, "features": "تحليل سريع لعقار واحد، بدون تفاصيل مالية دقيقة."},
    "فضية": {"price": 10, "features": "تحليل دقيق + متوسط الأسعار في المنطقة + نصائح استثمارية."},
    "ذهبية": {"price": 30, "features": "كل ما سبق + تنبؤ بالسعر المستقبلي + تحليل ذكي بالذكاء الاصطناعي + اقتراح أفضل وقت للبيع."},
    "ماسية": {"price": 60, "features": "تحليل شامل + مقارنة مع مشاريع مماثلة + تحليل ذكي بالذكاء الاصطناعي + تقرير PDF فاخر."}
}

# اختيار الباقة
chosen_pkg = st.radio("💎 اختر(ي) باقتك:", list(packages.keys()), horizontal=True)

# حساب السعر
base_price = packages[chosen_pkg]["price"]
total_price = base_price * count

# عرض السعر والمميزات
st.markdown(f"""
<div class='gold-box'>
<h3>💰 السعر الإجمالي: {total_price} دولار</h3>
<p><b>مميزات الباقة ({chosen_pkg}):</b><br>{packages[chosen_pkg]['features']}</p>
</div>
""", unsafe_allow_html=True)

# توليد التقرير PDF مع دعم العربية
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Warda Intelligence Real Estate Report", 0, 1, "C")
        self.ln(5)
    
    def add_arabic_text(self, text, size=12):
        # تحويل النص العربي إلى ترميز صالح لـ PDF
        self.set_font("Arial", size=size)
        # استخدام encoding مناسب للنص العربي
        try:
            self.cell(0, 10, text.encode('latin-1', 'replace').decode('latin-1'), 0, 1)
        except:
            self.cell(0, 10, text, 0, 1)

def create_pdf(user_type, city, property_type, area, rooms, status, count, chosen_pkg, total_price):
    pdf = PDF()
    pdf.add_page()
    
    # إضافة محتوى PDF بالعربية
    pdf.set_font("Arial", size=14)
    pdf.cell(0, 10, "Real Estate Analysis Report - تقرير التحليل العقاري", 0, 1, 'C')
    pdf.ln(10)
    
    # بيانات المستخدم بالعربية والإنجليزية
    pdf.set_font("Arial", size=12)
    
    # استخدام طريقة آمنة للنص العربي
    user_data = [
        f"User Type / الفئة: {user_type}",
        f"City / المدينة: {city}",
        f"Property Type / نوع العقار: {property_type}",
        f"Area / المساحة: {area} m²",
        f"Rooms / عدد الغرف: {rooms}",
        f"Status / الحالة: {status}",
        f"Properties Count / عدد العقارات: {count}",
        f"Package / الباقة: {chosen_pkg}",
        f"Total Price / السعر الإجمالي: {total_price} $"
    ]
    
    for data in user_data:
        pdf.cell(0, 10, data, 0, 1)
        pdf.ln(2)
    
    pdf.ln(5)
    pdf.cell(0, 10, "Analysis Features / مميزات التحليل:", 0, 1)
    pdf.multi_cell(0, 8, packages[chosen_pkg]['features'])
    pdf.ln(5)
    
    pdf.multi_cell(0, 8, f"This report provides accurate insights into the {city} market based on real data and AI predictions.")
    pdf.multi_cell(0, 8, f"هذا التقرير يقدم نظرة دقيقة عن سوق {city} بناءً على بيانات واقعية وتنبؤات بالذكاء الاصطناعي.")
    pdf.ln(5)
    
    pdf.cell(0, 10, f"Creation Date / تاريخ الإنشاء: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1)
    pdf.ln(10)
    
    pdf.cell(0, 10, "Warda Intelligence - Accurate Real Estate Analysis", 0, 1, 'C')
    pdf.cell(0, 10, "منصة Warda Intelligence — تحليلات عقارية دقيقة", 0, 1, 'C')
    
    return pdf

# زر تحميل التقرير
if st.button("📥 تحميل التقرير (PDF)"):
    try:
        pdf = create_pdf(user_type, city, property_type, area, rooms, status, count, chosen_pkg, total_price)
        temp_name = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.output(temp_name)
        
        with open(temp_name, "rb") as f:
            st.download_button(
                label="📩 اضغط هنا لتحميل تقريرك الآن",
                data=f,
                file_name=f"report_{chosen_pkg}_{city}.pdf",
                mime="application/pdf"
            )
        
        # تنظيف الملف المؤقت
        if os.path.exists(temp_name):
            os.remove(temp_name)
            
        st.success("✅ تم إنشاء التقرير بنجاح!")
        
    except Exception as e:
        st.error(f"❌ حدث خطأ في إنشاء التقرير: {str(e)}")
        st.info("💡 جارٍ إنشاء نسخة بديلة...")
        
        # نسخة بديلة إذا فشلت الأولى
        try:
            from fpdf import FPDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            # بيانات بسيطة بدون أحرف عربية مشكلة
            content = f"""
            Warda Intelligence Report
            User: {user_type}
            City: {city}
            Property: {property_type}
            Area: {area}m2
            Rooms: {rooms}
            Status: {status}
            Count: {count}
            Package: {chosen_pkg}
            Price: {total_price}$
            Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            pdf.multi_cell(0, 10, content)
            temp_name = f"report_simple_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf.output(temp_name)
            
            with open(temp_name, "rb") as f:
                st.download_button(
                    label="📥 تحميل النسخة المبسطة",
                    data=f,
                    file_name=f"report_simple_{city}.pdf",
                    mime="application/pdf"
                )
            
            if os.path.exists(temp_name):
                os.remove(temp_name)
                
        except Exception as e2:
            st.error(f"❌ فشل الإنشاء: {str(e2)}")

# رابط المؤثرين - يمنح تقرير مجاني لمرة واحدة
st.markdown("""
<div class='center'>
<h4>🎁 رابط خاص بالمؤثرين</h4>
<p>يمكنك منح هذا الرابط لأي مؤثر ليستفيد من تقرير مجاني لمرة واحدة فقط:</p>
<a href="https://warda-intelligence.streamlit.app/?promo=FREE1" target="_blank">
<button style="background-color:green;color:white;font-size:18px;padding:10px 20px;border:none;border-radius:10px;">🎯 رابط المؤثرين المجاني</button>
</a>
</div>
""", unsafe_allow_html=True)

# واتساب
st.markdown("""
<div class='center'>
<a href="https://wa.me/213779888140" target="_blank">
<button style="background-color:green;color:white;font-size:18px;padding:10px 20px;border:none;border-radius:10px;">💬 تواصل مع Warda Intelligence عبر واتساب</button>
</a>
</div>
""", unsafe_allow_html=True)
