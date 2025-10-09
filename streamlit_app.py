import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from fpdf import FPDF

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
    .payment-btn {
        background: linear-gradient(135deg, #0070ba 0%, #005ea6 100%);
        color: white;
        padding: 15px 25px;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        cursor: pointer;
        width: 100%;
        margin: 10px 0;
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
    st.markdown("### 💼 اختر الباقة المناسبة")
    
    # عرض الباقات بشكل جميل
    col_b1, col_b2, col_b3 = st.columns(3)
    
    with col_b1:
        st.markdown('<div class="package-card">', unsafe_allow_html=True)
        st.markdown("**🟢 الباقة الأساسية**")
        st.markdown("### $99")
        st.markdown("• تحليل 500 عقار")
        st.markdown("• تقرير PDF")
        st.markdown("• دعم أسبوع")
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("اختر الأساسية", key="basic"):
            الباقة = "الباقة الأساسية - $99 (تحليل 500 عقار)"
            st.session_state.selected_package = الباقة
    
    with col_b2:
        st.markdown('<div class="package-card">', unsafe_allow_html=True)
        st.markdown("**🔵 الباقة المتقدمة**")
        st.markdown("### $199")
        st.markdown("• تحليل 1000 عقار")
        st.markdown("• تقرير PDF متقدم")
        st.markdown("• دعم أسبوعين")
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("اختر المتقدمة", key="advanced"):
            الباقة = "الباقة المتقدمة - $199 (تحليل 1000 عقار)"
            st.session_state.selected_package = الباقة
    
    with col_b3:
        st.markdown('<div class="package-card premium-package">', unsafe_allow_html=True)
        st.markdown("**🟡 الباقة الاحترافية**")
        st.markdown("### $399")
        st.markdown("• تحليل 2000 عقار")
        st.markdown("• تقرير PDF كامل")
        st.markdown("• تنبؤات الذكاء الاصطناعي")
        st.markdown("• دعم شهر كامل")
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("اختر الاحترافية", key="premium"):
            الباقة = "الباقة الاحترافية - $399 (تحليل 2000 عقار + الذكاء الاصطناعي)"
            st.session_state.selected_package = الباقة

# عرض الباقة المختارة
if 'selected_package' in st.session_state:
    الباقة = st.session_state.selected_package
    st.success(f"**✅ الباقة المختارة: {الباقة}**")

# 💳 قسم الدفع المباشر
if 'selected_package' in st.session_state:
    st.markdown("---")
    st.markdown('<div class="section-header">💳 إتمام الطلب والدفع</div>', unsafe_allow_html=True)
    
    col_دفع1, col_دفع2 = st.columns(2)
    
    with col_دفع1:
        st.markdown("### 📋 ملخص طلبك")
        st.info(f"""
        **المدينة:** {المدينة}
        **نوع العقار:** {نوع_العقار}
        **الباقة المختارة:** {الباقة}
        **السعر:** ${الباقة.split('$')[1].split(' ')[0]}
        """)
        
        # مزايا الباقة
        st.markdown("### ✨ المزايا المشمولة:")
        if "أساسية" in الباقة:
            st.write("✅ تحليل 500 عقار")
            st.write("✅ تقرير PDF كامل")
            st.write("✅ دعم فني لمدة أسبوع")
            st.write("✅ توصيات استثمارية")
        elif "متقدمة" in الباقة:
            st.write("✅ تحليل 1000 عقار")
            st.write("✅ تقرير PDF متقدم")
            st.write("✅ دعم فني لمدة أسبوعين")
            st.write("✅ توصيات استثمارية مفصلة")
        else:
            st.write("✅ تحليل 2000 عقار")
            st.write("✅ تقرير PDF احترافي")
            st.write("✅ تنبؤات الذكاء الاصطناعي 🤖")
            st.write("✅ دعم فني لمدة شهر")
            st.write("✅ خطط استثمارية مخصصة")
    
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
        
        # زر الدفع
        st.markdown("""
        <a href="https://www.paypal.com/send?email=zeghloulwarda6@gmail.com&amount={}&currency=USD" target="_blank">
            <button class="payment-btn">
                💳 الدفع الآمن عبر PayPal - ${}
            </button>
        </a>
        """.format(الباقة.split('$')[1].split(' ')[0], الباقة.split('$')[1].split(' ')[0]), unsafe_allow_html=True)
        
        st.warning("**⚠️ بعد الدفع، ستصلك تفاصيل التقرير على بريدك الإلكتروني**")

# 🤖 قسم الذكاء الاصطناعي (للباقة الاحترافية فقط)
if 'selected_package' in st.session_state and "احترافية" in الباقة:
    st.markdown("---")
    st.markdown('<div class="section-header">🤖 تنبؤات الذكاء الاصطناعي المتقدمة</div>', unsafe_allow_html=True)
    
    st.success("""
    **🎯 مع الباقة الاحترافية، ستحصل على:**
    
    - 📈 **تنبؤات أسعار** لـ 30 يوم قادم
    - 🔮 **تحليل اتجاهات السوق** الذكي
    - 🎯 **خطط استثمارية** مخصصة
    - 📊 **مقارنات متقدمة** بين المناطق
    - 💡 **توصيات ذكية** بناءً على تحليل البيانات
    """)
    
    col_ai1, col_ai2 = st.columns(2)
    
    with col_ai1:
        st.markdown("### 📈 نماذج التنبؤ:")
        st.write("• تحليل الانحدار المتقدم")
        st.write("• شبكات عصبية للتنبؤ")
        st.write("• تحليل السلاسل الزمنية")
        st.write("• نماذج التعلم الآلي")
    
    with col_ai2:
        st.markdown("### 🎯 مخرجات الذكاء الاصطناعي:")
        st.write("• تقارير تنبؤية شهرية")
        st.write("• تحليل المخاطر والفرص")
        st.write("• مؤشرات أداء مخصصة")
        st.write("• إنذارات مبكرة للتغيرات")

# 📥 قسم تأكيد الطلب
if 'selected_package' in st.session_state:
    st.markdown("---")
    st.markdown('<div class="section-header">📥 تأكيد الطلب واستلام التقرير</div>', unsafe_allow_html=True)
    
    with st.form("تأكيد_الطلب"):
        st.markdown("### 📝 معلومات التواصل")
        email = st.text_input("📧 البريد الإلكتروني *", placeholder="example@email.com")
        phone = st.text_input("📱 رقم الجوال *", placeholder="+966 XXX XXX XXX")
        transaction_id = st.text_input("🔢 رقم العملية (إن وجد)", placeholder="اختياري - للمتابعة")
        
        submitted = st.form_submit_button("✅ تأكيد الطلب وإرسال التقرير")
        
        if submitted:
            if email and phone:
                st.balloons()
                st.success(f"""
                **🎉 تم تأكيد طلبك بنجاح!**
                
                **سيصلك التقرير خلال 24 ساعة على:**
                📧 {email}
                
                **تفاصيل الطلب:**
                🏙️ المدينة: {المدينة}
                🏠 نوع العقار: {نوع_العقار}
                📦 الباقة: {الباقة}
                
                **للتواصل أو الاستفسار:**
                📧 ouardazeghloul1@gmail.com
                📱 +779888140
                """)
                
                # زر تحميل رمزي (في الواقع سيتم الإرسال بالبريد)
                st.markdown("""
                <div style='text-align: center; padding: 20px;'>
                    <h4>📄 سيتم إرسال التقرير PDF إلى بريدك الإلكتروني</h4>
                    <p>يمكنك التواصل معنا لأي استفسار</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("❌ يرجى تعبئة جميع الحقول المطلوبة")

# 📞 قسم المعلومات
st.markdown("---")
st.markdown('<div class="section-header">📞 للتواصل مع وردة العقارية</div>', unsafe_allow_html=True)

col_معلومات1, col_معلومات2, col_معلومات3 = st.columns(3)

with col_معلومات1:
    st.markdown("### 📍 معلومات الشركة")
    st.write("**المملكة العربية السعودية**")
    st.write("منصة تحليل عقاري متكاملة")

with col_معلومات2:
    st.markdown("### 📧 وسائل التواصل")
    st.write("**البريد الإلكتروني:**")
    st.write("ouardazeghloul1@gmail.com")
    st.write("**الواتساب:**")
    st.write("+779888140")

with col_معلومات3:
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
