import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64
from io import BytesIO

# محاولة استيراد weasyprint أو استخدام بديل
try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False
    st.warning("⚠️ لم يتم تثبيت WeasyPrint - سيتم استخدام HTML بدلاً من PDF")

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

# دالة إنشاء التقرير بالعربية
def create_arabic_report(user_type, city, property_type, area, rooms, status, count, chosen_pkg, total_price):
    # إنشاء محتوى HTML عربي
    html_content = f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                line-height: 1.8;
                color: #333;
                margin: 40px;
                background: linear-gradient(135deg, #f5f5f5, #e0e0e0);
            }}
            .header {{
                text-align: center;
                background: linear-gradient(135deg, #d4af37, #b8941f);
                color: white;
                padding: 30px;
                border-radius: 15px;
                margin-bottom: 30px;
            }}
            .content {{
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }}
            .section {{
                margin-bottom: 25px;
                padding: 20px;
                border-right: 5px solid #d4af37;
                background: #f9f9f9;
                border-radius: 10px;
            }}
            .gold-text {{
                color: #d4af37;
                font-weight: bold;
            }}
            .footer {{
                text-align: center;
                margin-top: 40px;
                padding: 20px;
                background: #333;
                color: white;
                border-radius: 10px;
            }}
            h1, h2, h3 {{
                color: #d4af37;
            }}
            .info-item {{
                margin: 10px 0;
                padding: 8px;
                background: #fff;
                border-radius: 5px;
                border: 1px solid #ddd;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🏙️ تقرير التحليل العقاري الذهبي</h1>
            <h3>منصة Warda Intelligence - تحليلات عقارية ذكية</h3>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>👤 معلومات العميل</h2>
                <div class="info-item"><strong>الفئة:</strong> {user_type}</div>
                <div class="info-item"><strong>المدينة:</strong> {city}</div>
                <div class="info-item"><strong>نوع العقار:</strong> {property_type}</div>
                <div class="info-item"><strong>المساحة:</strong> {area} م²</div>
                <div class="info-item"><strong>عدد الغرف:</strong> {rooms}</div>
                <div class="info-item"><strong>الحالة:</strong> {status}</div>
                <div class="info-item"><strong>عدد العقارات المحللة:</strong> {count}</div>
            </div>
            
            <div class="section">
                <h2>💎 تفاصيل الباقة</h2>
                <div class="info-item"><strong>الباقة المختارة:</strong> {chosen_pkg}</div>
                <div class="info-item"><strong>السعر الإجمالي:</strong> {total_price} دولار</div>
                <div class="info-item"><strong>مميزات الباقة:</strong> {packages[chosen_pkg]['features']}</div>
            </div>
            
            <div class="section">
                <h2>📈 ملخص التحليل</h2>
                <p>هذا التقرير يقدم تحليلاً شاملاً لسوق العقارات في <span class="gold-text">{city}</span> بناءً على:</p>
                <ul>
                    <li>تحليل بيانات السوق الحالية</li>
                    <li>تنبؤات بالذكاء الاصطناعي</li>
                    <li>مقارنة مع المشاريع المماثلة</li>
                    <li>نصائح استثمارية مخصصة</li>
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <p>🕒 تاريخ الإنشاء: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>📞 للاستفسار: +213779888140</p>
            <p>© 2024 Warda Intelligence - جميع الحقوق محفوظة</p>
        </div>
    </body>
    </html>
    """
    
    return html_content

# زر تحميل التقرير
if st.button("📥 تحميل التقرير (PDF)"):
    try:
        with st.spinner("🔄 جاري إنشاء التقرير العربي..."):
            html_content = create_arabic_report(user_type, city, property_type, area, rooms, status, count, chosen_pkg, total_price)
            
            if WEASYPRINT_AVAILABLE:
                # إنشاء PDF باستخدام weasyprint
                pdf_bytes = HTML(string=html_content).write_pdf()
                
                st.download_button(
                    label="🎯 اضغط لتحميل التقرير العربي PDF",
                    data=pdf_bytes,
                    file_name=f"تقرير_عقاري_{city}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
            else:
                # عرض التقرير كHTML إذا لم يكن weasyprint متاحاً
                st.markdown("### 📄 معاينة التقرير العربي")
                st.components.v1.html(html_content, height=800, scrolling=True)
                
                st.info("""
                💡 **لتحميل التقرير كPDF:**
                1. اضغط على زر التحميل أدناه لتحميل ملف HTML
                2. افتح الملف في متصفحك
                3. اختر "طباعة" ثم "حفظ كPDF"
                """)
                
                st.download_button(
                    label="📄 تحميل التقرير كملف HTML",
                    data=html_content,
                    file_name=f"تقرير_عقاري_{city}.html",
                    mime="text/html"
                )
        
        st.success("✅ تم إنشاء التقرير العربي بنجاح!")
        st.balloons()
        
    except Exception as e:
        st.error(f"❌ حدث خطأ: {str(e)}")
        st.info("📞 يرجى التواصل مع الدعم الفني لحل المشكلة")

# رابط المؤثرين
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
