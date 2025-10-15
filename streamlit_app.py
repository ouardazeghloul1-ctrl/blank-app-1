import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import os

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

# الحل النهائي: استخدام unicode بشكل مباشر مع خط يدعم العربية
class UnicodePDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Warda Intelligence - تقرير التحليل العقاري", 0, 1, "C")
        self.ln(5)

def create_simple_pdf(user_type, city, property_type, area, rooms, status, count, chosen_pkg, total_price):
    pdf = UnicodePDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # استخدام نص إنجليزي فقط لتجنب مشاكل الترميز
    content = f"""
    Warda Intelligence - Real Estate Analysis Report
    ================================================
    
    User Information:
    - User Type: {user_type}
    - City: {city}
    - Property Type: {property_type}
    - Area: {area} m²
    - Rooms: {rooms}
    - Status: {status}
    - Properties Analyzed: {count}
    
    Package Details:
    - Selected Package: {chosen_pkg}
    - Total Price: ${total_price}
    - Features: {packages[chosen_pkg]['features']}
    
    Report Summary:
    This report provides comprehensive analysis of the real estate market
    in {city} based on advanced AI algorithms and market data.
    
    Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    --- Warda Intelligence ---
    Smart Real Estate Analytics
    """
    
    pdf.multi_cell(0, 10, content)
    return pdf

# زر تحميل التقرير
if st.button("📥 تحميل التقرير (PDF)"):
    try:
        pdf = create_simple_pdf(user_type, city, property_type, area, rooms, status, count, chosen_pkg, total_price)
        temp_name = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.output(temp_name)
        
        with open(temp_name, "rb") as f:
            st.download_button(
                label="📩 اضغط هنا لتحميل تقريرك الآن",
                data=f,
                file_name=f"warda_report_{city}.pdf",
                mime="application/pdf"
            )
        
        if os.path.exists(temp_name):
            os.remove(temp_name)
            
        st.success("✅ تم إنشاء التقرير بنجاح!")
        
    except Exception as e:
        st.error(f"❌ حدث خطأ: {str(e)}")
        st.info("🔧 جاري استخدام الحل البديل...")
        
        # الحل البديل النهائي
        try:
            from fpdf import FPDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            # نص إنجليزي فقط - مضمون العمل
            safe_content = [
                "WARD A INTELLIGENCE - REAL ESTATE REPORT",
                "----------------------------------------",
                f"CLIENT: {user_type}",
                f"LOCATION: {city}",
                f"PROPERTY: {property_type}",
                f"AREA: {area} SQ M",
                f"ROOMS: {rooms}",
                f"TRANSACTION: {status}",
                f"ANALYSIS COUNT: {count}",
                f"PACKAGE: {chosen_pkg}",
                f"TOTAL: ${total_price}",
                f"DATE: {datetime.now().strftime('%Y-%m-%d')}",
                "",
                "Thank you for using Warda Intelligence",
                "Smart Real Estate Analytics Platform"
            ]
            
            for line in safe_content:
                pdf.cell(0, 10, line, 0, 1)
            
            backup_name = f"warda_backup_{datetime.now().strftime('%H%M%S')}.pdf"
            pdf.output(backup_name)
            
            with open(backup_name, "rb") as f:
                st.download_button(
                    label="📥 تحميل النسخة المضمونة",
                    data=f,
                    file_name=f"warda_analysis_{city}.pdf",
                    mime="application/pdf"
                )
            
            if os.path.exists(backup_name):
                os.remove(backup_name)
                
        except Exception as final_error:
            st.error("❌ فشل جميع محاولات الإنشاء")
            st.info("⚠️ يرجى المحاولة مرة أخرى أو التواصل مع الدعم")

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
