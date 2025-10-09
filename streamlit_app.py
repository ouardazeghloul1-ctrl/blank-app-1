import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from fpdf import FPDF
from io import BytesIO

# إعداد الصفحة
st.set_page_config(
    page_title="وردة العقارية - المنصة الذكية",
    page_icon="🏠",
    layout="wide"
)

# تنسيق CSS مخصص
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2E8B57;
        margin: 1.5rem 0 1rem 0;
        border-right: 4px solid #2E8B57;
        padding-right: 12px;
        font-weight: bold;
    }
    .package-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #2E8B57;
        margin: 10px 0;
        text-align: center;
    }
    .premium-package {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: white;
        border: 2px solid #FF8C00;
    }
    .cute-btn {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%);
        color: white;
        padding: 12px 25px;
        border: none;
        border-radius: 25px;
        font-size: 16px;
        cursor: pointer;
        margin: 10px 0;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
        transition: all 0.3s ease;
    }
    .cute-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
    }
    .payment-btn {
        background: linear-gradient(135deg, #0070ba 0%, #005ea6 100%);
        color: white;
        padding: 12px 25px;
        border: none;
        border-radius: 25px;
        font-size: 14px;
        cursor: pointer;
        margin: 5px 0;
        font-weight: bold;
    }
    .info-box {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-right: 4px solid #4682b4;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown('<div class="main-header">🏠 وردة العقارية - المنصة الذكية للتحليل العقاري</div>', unsafe_allow_html=True)

# 🎯 قسم الهدف
st.markdown("---")
st.markdown('<div class="section-header">🎯 هدف المنصة</div>', unsafe_allow_html=True)

st.success("""
**✨ مهمتنا هي مساعدتك في اتخاذ أفضل القرارات الاستثمارية العقارية من خلال:**

- 📊 **تحليل عميق** لآلاف العقارات في السوق السعودي
- 📈 **توقعات ذكية** باستخدام أحدث تقنيات الذكاء الاصطناعي  
- 💡 **توصيات مبنية على بيانات** حقيقية ومحدثة
- 📋 **تقارير شاملة** تلخص أفضل الفرص الاستثمارية
- 🎯 **تحديد العقارات ذات العوائد المرتفعة** والمخاطر المنخفضة

**كل هذا لضمان تحقيق أقصى عائد على استثمارك!**
""")

# 🔧 قسم الإدخال الرئيسي
st.markdown("---")
st.markdown('<div class="section-header">⚙️ اختر معايير البحث</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    المدن = ["الرياض", "جدة", "مكة", "المدينة", "الدمام", "الخبر", "الطائف", "تبوك", "بريدة", "خميس مشيط"]
    المدينة = st.selectbox("🏙️ اختر المدينة", المدن)

with col2:
    أنواع_العقارات = ["شقة", "فيلا", "أرض", "محل تجاري", "مكتب"]
    نوع_العقار = st.selectbox("🏠 نوع العقار", أنواع_العقارات)

with col3:
    # المستخدم يختار عدد العقارات
    عدد_العقارات = st.selectbox("🔢 عدد العقارات المطلوب تحليلها", 
                               [100, 250, 500, 750, 1000, 1500, 2000])

# 💼 قسم الباقات
st.markdown("---")
st.markdown('<div class="section-header">💼 اختر الباقة المناسبة</div>', unsafe_allow_html=True)

col_b1, col_b2, col_b3 = st.columns(3)

with col_b1:
    st.markdown('<div class="package-card">', unsafe_allow_html=True)
    st.markdown("**🟢 الباقة الأساسية**")
    st.markdown("### $99")
    st.markdown("• تقرير PDF كامل")
    st.markdown("• تحليل العقارات")
    st.markdown("• دعم أسبوع")
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("اختر الأساسية 🟢", key="basic"):
        الباقة = "الباقة الأساسية - $99"
        st.session_state.selected_package = الباقة
        st.session_state.package_price = 99

with col_b2:
    st.markdown('<div class="package-card">', unsafe_allow_html=True)
    st.markdown("**🔵 الباقة المتقدمة**")
    st.markdown("### $199")
    st.markdown("• تقرير PDF متقدم")
    st.markdown("• تحليل مفصل")
    st.markdown("• دعم أسبوعين")
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("اختر المتقدمة 🔵", key="advanced"):
        الباقة = "الباقة المتقدمة - $199"
        st.session_state.selected_package = الباقة
        st.session_state.package_price = 199

with col_b3:
    st.markdown('<div class="package-card premium-package">', unsafe_allow_html=True)
    st.markdown("**🟡 الباقة الاحترافية**")
    st.markdown("### $399")
    st.markdown("• تقرير PDF احترافي")
    st.markdown("• تنبؤات الذكاء الاصطناعي")
    st.markdown("• دعم شهر كامل")
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("اختر الاحترافية 🟡", key="premium"):
        الباقة = "الباقة الاحترافية - $399"
        st.session_state.selected_package = الباقة
        st.session_state.package_price = 399

# عرض الباقة المختارة
if 'selected_package' in st.session_state:
    st.success(f"**✅ الباقة المختارة: {st.session_state.selected_package}**")

# 💳 قسم الدفع المباشر
if 'selected_package' in st.session_state:
    st.markdown("---")
    st.markdown('<div class="section-header">💳 إتمام الطلب والدفع</div>', unsafe_allow_html=True)
    
    col_دفع1, col_دفع2 = st.columns(2)
    
    with col_دفع1:
        st.markdown("### 📋 ملخص طلبك")
        st.info(f"""
        **🏙️ المدينة:** {المدينة}
        **🏠 نوع العقار:** {نوع_العقار}
        **🔢 عدد العقارات:** {عدد_العقارات}
        **📦 الباقة المختارة:** {st.session_state.selected_package}
        **💰 السعر:** ${st.session_state.package_price}
        """)
    
    with col_دفع2:
        st.markdown("### 💰 طرق الدفع")
        st.markdown("""
        **💳 PayPal** - الدفع الآني الآمن
        **🏦 تحويل بنكي** - للعملاء المحليين  
        **📱 STC Pay** - الدفع السريع
        """)
        
        st.markdown("### 📧 معلومات الدفع")
        st.markdown("""
        **بايبال:** zeghloulwarda6@gmail.com
        **البنك:** SA1234567890123456789012
        **STC Pay:** 0550123456
        """)
        
        # زر الدفع الصغير والكيووت
        st.markdown("""
        <a href="https://www.paypal.com/send?email=zeghloulwarda6@gmail.com&amount={}&currency=USD" target="_blank">
            <button class="payment-btn">
                💳 ادفع الآن - ${}
            </button>
        </a>
        """.format(st.session_state.package_price, st.session_state.package_price), unsafe_allow_html=True)

# 📥 قسم استلام التقرير
if 'selected_package' in st.session_state:
    st.markdown("---")
    st.markdown('<div class="section-header">📥 استلم تقريرك الآن</div>', unsafe_allow_html=True)
    
    # نموذج بسيط لتأكيد الطلب
    with st.form("استلام_التقرير"):
        st.markdown("### 📝 أدخل معلوماتك لاستلام التقرير")
        email = st.text_input("📧 البريد الإلكتروني *", placeholder="example@email.com")
        
        submitted = st.form_submit_button("🎀 استلم تقريرك PDF الآن")
        
        if submitted:
            if email:
                st.balloons()
                st.success(f"""
                **🎉 تم إرسال التقرير بنجاح!**
                
                **سيصلك التقرير خلال دقائق على:**
                📧 {email}
                
                **تفاصيل طلبك:**
                🏙️ المدينة: {المدينة}
                🏠 نوع العقار: {نوع_العقار} 
                🔢 عدد العقارات: {عدد_العقارات}
                📦 الباقة: {st.session_state.selected_package}
                
                **شكراً لثقتك بنا! 🌸**
                """)
                
                # زر تحميل PDF كيوت
                def create_simple_pdf():
                    pdf = FPDF()
                    pdf.add_page()
                    
                    # عنوان التقرير
                    pdf.set_font("Arial", 'B', 16)
                    pdf.cell(200, 10, txt="تقرير وردة العقارية", ln=True, align='C')
                    pdf.ln(10)
                    
                    # معلومات التقرير
                    pdf.set_font("Arial", '', 12)
                    pdf.cell(200, 10, txt=f"المدينة: {المدينة}", ln=True)
                    pdf.cell(200, 10, txt=f"نوع العقار: {نوع_العقار}", ln=True)
                    pdf.cell(200, 10, txt=f"عدد العقارات: {عدد_العقارات}", ln=True)
                    pdf.cell(200, 10, txt=f"الباقة: {st.session_state.selected_package}", ln=True)
                    pdf.cell(200, 10, txt=f"التاريخ: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
                    pdf.ln(10)
                    
                    pdf.cell(200, 10, txt="شكراً لاستخدامك وردة العقارية!", ln=True, align='C')
                    
                    return pdf.output(dest='S').encode('latin1')
                
                # زر التحميل الكيوت
                pdf_data = create_simple_pdf()
                st.download_button(
                    label="📄 انقر لتحميل تقريرك PDF 🎀",
                    data=pdf_data,
                    file_name=f"تقرير_وردة_العقارية_{المدينة}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                )
            else:
                st.error("❌ يرجى إدخال البريد الإلكتروني")

# 📞 قسم المعلومات
st.markdown("---")
st.markdown('<div class="section-header">📞 للتواصل مع وردة العقارية</div>', unsafe_allow_html=True)

col_معلومات1, col_معلومات2 = st.columns(2)

with col_معلومات1:
    st.markdown("### 📧 وسائل التواصل")
    st.write("**البريد الإلكتروني:**")
    st.write("ouardazeghloul1@gmail.com")
    st.write("**الواتساب:**")
    st.write("+779888140")

with col_معلومات2:
    st.markdown("### 🕒 أوقات العمل")
    st.write("**الأحد - الخميس**")
    st.write("9:00 ص - 6:00 م")
    st.write("**الجمعة - السبت**")
    st.write("10:00 ص - 4:00 م")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <strong>✨ وردة العقارية 2024</strong> - منصة التحليل العقاري الذكي • جميع الحقوق محفوظة
</div>
""", unsafe_allow_html=True)
