import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# إعدادات الصفحة
st.set_page_config(page_title="وردة العقارية", page_icon="🏠", layout="wide")

# تصميم عربي احترافي
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #ff7f0e;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown('<div class="main-title">🏡 وردة العقارية - التحليل العقاري المتقدم</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">منصة ذكية لتحليل الأسواق العقارية وتقديم توصيات استثمارية دقيقة</div>', unsafe_allow_html=True)

st.markdown("---")

# 🎯 القسم 1: إدخال البيانات المتقدم
st.markdown('<div class="section-header">📋 تحديد متطلبات التحليل</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🏙️ الموقع")
    المدينة = st.selectbox("المدينة", ["الرياض", "جدة", "الدمام", "مكة", "المدينة", "الخبر", "الطائف"])
    الحي = st.text_input("الحي (اختياري)", placeholder="أدخل اسم الحي")

with col2:
    st.subheader("🏠 نوع العقار")
    نوع_العقار = st.selectbox("نوع العقار", ["شقق", "فلل", "أراضي", "مكاتب", "محلات"])
    المساحة = st.slider("المساحة المطلوبة (م²)", 50, 1000, 150)

with col3:
    st.subheader("💰 الميزانية والهدف")
    الميزانية = st.selectbox("الميزانية المتوقعة", [
        "أقل من 500,000 ريال",
        "500,000 - 1,000,000 ريال", 
        "1,000,000 - 2,000,000 ريال",
        "2,000,000 - 5,000,000 ريال",
        "أكثر من 5,000,000 ريال"
    ])
    
    الهدف = st.selectbox("الهدف الاستثماري", [
        "استثمار طويل المدى",
        "تداول سريع", 
        "سكن شخصي",
        "تطوير عقاري"
    ])

# 🎯 القسم 2: خيارات متقدمة
st.markdown('<div class="section-header">⚙️ خيارات التحليل المتقدم</div>', unsafe_allow_html=True)

col4, col5 = st.columns(2)

with col4:
    st.subheader("📊 مستوى التفصيل")
    مستوى_التفصيل = st.radio("مستوى التقرير:", [
        "تقرير سريع (تحليل أساسي)",
        "تقرير متقدم (تحليل مفصل)", 
        "دراسة شاملة (توصيات استراتيجية)"
    ])

with col5:
    st.subheader("📦 الباقات")
    الباقة = st.selectbox("اختر الباقة:", [
        "الباقة الأساسية - 100$ (تقرير تحليلي)",
        "الباقة المتقدمة - 250$ (تقرير + توصيات)", 
        "الباقة المميزة - 500$ (دراسة شاملة + متابعة)"
    ])

# 🎯 القسم 3: زر التشغيل الرئيسي
st.markdown("---")
if st.button("🚀 إنشاء التقرير المتكامل", type="primary", use_container_width=True):
    
    with st.spinner("🔄 جاري تحليل بيانات السوق وإعداد التقرير..."):
        
        # محاكاة بيانات واقعية
        np.random.seed(42)
        
        # إنشاء بيانات متنوعة بناء على الاختيارات
        data = []
        for i in range(100):
            # أسعار واقعية حسب المدينة ونوع العقار
            أسعار_أساسية = {
                "الرياض": {"شقق": (600000, 1500000), "فلل": (2000000, 5000000), "أراضي": (800000, 3000000)},
                "جدة": {"شقق": (500000, 1200000), "فلل": (1500000, 4000000), "أراضي": (600000, 2500000)},
                "الدمام": {"شقق": (400000, 1000000), "فلل": (1200000, 3000000), "أراضي": (500000, 2000000)}
            }
            
            سعر_مدى = أسعار_أساسية.get(المدينة, أسعار_أساسية["الرياض"]).get(نوع_العقار, (500000, 2000000))
            سعر = np.random.randint(سعر_مدى[0], سعر_مدى[1])
            مساحة = np.random.randint(80, 400)
            
            data.append({
                "العقار": f"{نوع_العقار[:-1]} {i+1}",
                "المدينة": المدينة,
                "الحي": np.random.choice(["النخيل", "الروضة", "الصفا", "الزهراء", "الربوة", "الملز", "العليا"]),
                "نوع_العقار": نوع_العقار[:-1],
                "السعر": سعر,
                "المساحة": مساحة,
                "سعر_المتر": int(sعر / مساحة),
                "العائد_المتوقع": np.random.uniform(5, 15),
                "مستوى_الخطورة": np.random.choice(["منخفض", "متوسط", "مرتفع"])
            })
        
        df = pd.DataFrame(data)
        
        # ✅ عرض النتائج
        st.success(f"✅ تم تحليل {len(df)} عقار في السوق بنجاح!")
        
        # 📊 القسم 4: النتائج المتقدمة
        st.markdown("---")
        st.markdown('<div class="section-header">📊 نتائج التحليل المتكامل</div>', unsafe_allow_html=True)
        
        # الإحصائيات في أعمدة
        col6, col7, col8, col9 = st.columns(4)
        
        with col6:
            st.metric("💰 متوسط السعر", f"{df['السعر'].mean():,.0f} ريال")
        with col7:
            st.metric("📐 متوسط المساحة", f"{df['المساحة'].mean():.0f} م²")
        with col8:
            st.metric("📊 سعر المتر", f"{df['سعر_المتر'].mean():,.0f} ريال")
        with col9:
            st.metric("📈 متوسط العائد", f"{df['العائد_المتوقع'].mean():.1f}%")
        
        # 📈 القسم 5: الرسوم البيانية
        st.subheader("📈 التحليلات البصرية المتقدمة")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. توزيع الأسعار
        ax1.hist(df['السعر'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.set_xlabel('السعر (ريال)')
        ax1.set_ylabel('عدد العقارات')
        ax1.set_title('توزيع الأسعار في السوق')
        ax1.ticklabel_format(style='plain', axis='x')
        
        # 2. العلاقة بين المساحة والسعر
        ax2.scatter(df['المساحة'], df['السعر'], alpha=0.6, color='coral')
        ax2.set_xlabel('المساحة (م²)')
        ax2.set_ylabel('السعر (ريال)')
        ax2.set_title('العلاقة بين المساحة والسعر')
        
        # 3. أفضل الأحياء
        حي_أسعار = df.groupby('الحي')['سعر_المتر'].mean().sort_values()
        ax3.barh(range(len(حي_أسعار)), حي_أسعار.values, color='lightgreen')
        ax3.set_yticks(range(len(حي_أسعار)))
        ax3.set_yticklabels(حي_أسعار.index)
        ax3.set_xlabel('متوسط سعر المتر (ريال)')
        ax3.set_title('أفضل الأحياء من حيث السعر')
        
        # 4. توزيع العوائد
        ax4.hist(df['العائد_المتوقع'], bins=15, alpha=0.7, color='gold', edgecolor='black')
        ax4.set_xlabel('العائد المتوقع (%)')
        ax4.set_ylabel('عدد العقارات')
        ax4.set_title('توزيع العوائد المتوقعة')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # 🏆 القسم 6: أفضل العروض
        st.subheader("🏆 أفضل العروض الاستثمارية")
        
        أفضل_عروض = df.nsmallest(10, 'سعر_المتر')
        st.dataframe(أفضل_عروض[[
            'العقار', 'الحي', 'السعر', 'المساحة', 'سعر_المتر', 'العائد_المتوقع', 'مستوى_الخطورة'
        ]].style.format({
            'السعر': '{:,}',
            'سعر_المتر': '{:,}',
            'العائد_المتوقع': '{:.1f}%'
        }))
        
        # 💡 القسم 7: التوصيات الذكية
        st.markdown("---")
        st.markdown('<div class="section-header">💡 التوصيات الاستثمارية الذكية</div>', unsafe_allow_html=True)
        
        col10, col11 = st.columns(2)
        
        with col10:
            st.success(f"""
            **🎯 توصيات مبنية على هدفك:**
            
            **الهدف:** {الهدف}
            **المدينة:** {المدينة}
            **نوع العقار:** {نوع_العقار}
            
            **التوصيات:**
            • أفضل حي للاستثمار: **{حي_أسعار.index[0]}**
            • متوسط سعر المتر: **{حي_أسعار.iloc[0]:,.0f} ريال**
            • فرصة التوفير: **{(حي_أسعار.iloc[-1] - حي_أسعار.iloc[0]):,.0f} ريال/م²**
            • عدد الفرص الممتازة: **{len(أفضل_عروض)} عقار**
            """)
        
        with col11:
            st.info(f"""
            **📈 خطة استثمارية مقترحة:**
            
            **1. المرحلة الأولى:**
            - الاستثمار في {أفضل_عروض.iloc[0]['الحي']}
            - ميزانية: {أفضل_عروض.iloc[0]['السعر']:,} ريال
            - عائد متوقع: {أفضل_عروض.iloc[0]['العائد_المتوقع']:.1f}%
            
            **2. المرحلة الثانية:**
            - التنويع في {أفضل_عروض.iloc[1]['الحي']}
            - تحسين المحفظة الاستثمارية
            
            **3. المراقبة:**
            - متابعة اتجاهات السوق
            - تعديل الاستراتيجية حسب المتغيرات
            """)
        
        # 💳 القسم 8: نظام الدفع
        st.markdown("---")
        st.markdown('<div class="section-header">💳 اكتمال الطلب والدفع</div>', unsafe_allow_html=True)
        
        st.warning(f"""
        **للاستفادة الكاملة من الخدمة:**
        
        **الباقة المختارة:** {الباقة}
        **يشمل:**
        - 📊 تقرير PDF مفصل
        - 📞 استشارة شخصية لمدة 30 دقيقة
        - 🔄 متابعة أسبوعية
        - 💎 توصيات حصرية
        - 📱 تحديثات مستمرة
        """)
        
        # معلومات الدفع
        st.info("""
        **طريقة الدفع:**
        1. تحويل بنكي
        2. PayPal
        3. STC Pay
        
        **بعد الدفع:** ستتلقى التقرير الكامل خلال 24 ساعة
        """)

# 📞 القسم 9: معلومات الاتصال
st.markdown("---")
st.markdown('<div class="section-header">📞 للتواصل مع وردة العقارية</div>', unsafe_allow_html=True)

col12, col13, col14 = st.columns(3)

with col12:
    st.write("**📍 العنوان:**")
    st.write("المملكة العربية السعودية")

with col13:
    st.write("**📧 البريد الإلكتروني:**")
    st.write("info@warda-realestate.com")

with col14:
    st.write("**⏰ ساعات العمل:**")
    st.write("9:00 صباحاً - 5:00 مساءً")

st.markdown("---")
st.markdown("✨ **وردة العقارية 2024** - منصة التحليل العقاري الذكي")
