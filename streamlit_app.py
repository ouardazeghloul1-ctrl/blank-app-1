import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# إعدادات العربية
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="وردة العقارية", page_icon="🏠", layout="wide")

# العنوان الرئيسي
st.title("🏠 وردة العقارية - التحليل العقاري الذكي")
st.markdown("---")

# نموذج إدخال البيانات
col1, col2 = st.columns(2)
with col1:
    المدينة = st.selectbox("🏙️ اختر المدينة", ["الرياض", "جدة", "الدمام", "مكة", "المدينة"])
with col2:
    اسم_العميل = st.text_input("👤 اسم العميل", placeholder="أدخل اسم العميل")

col3, col4 = st.columns(2)
with col3:
    نوع_العقار = st.selectbox("🏠 نوع العقار", ["شقق", "فلل", "مكاتب", "محلات"])
with col4:
    عدد_العقارات = st.slider("📊 عدد العقارات", 10, 200, 50)

# زر التشغيل
if st.button("🚀 إنشاء التقرير المتطور", type="primary"):
    with st.spinner("جاري إنشاء التقرير..."):
        # محاكاة إنشاء البيانات
        data = {
            'العقار': [f'عقار {i+1} في {المدينة}' for i in range(عدد_العقارات)],
            'السعر': np.random.randint(300000, 2000000, عدد_العقارات),
            'المساحة': np.random.randint(80, 400, عدد_العقارات),
            'الحي': np.random.choice(['السلام', 'الروضة', 'النخيل', 'الصفا', 'الزهراء'], عدد_العقارات),
            'نوع_العقار': np.random.choice([نوع_العقار, 'شقة', 'فيلا'], عدد_العقارات)
        }
        
        df = pd.DataFrame(data)
        
        # عرض النتائج
        st.success("✅ تم إنشاء التقرير بنجاح!")
        
        # الإحصائيات
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💰 متوسط السعر", f"{df['السعر'].mean():,.0f} ريال")
        with col2:
            st.metric("📐 متوسط المساحة", f"{df['المساحة'].mean():.0f} م²")
        with col3:
            st.metric("🏠 عدد العقارات", len(df))
        
        # الرسم البياني
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df, x='المساحة', y='السعر', hue='الحي', alpha=0.7, s=100)
        plt.title(f'العلاقة بين المساحة والسعر في {المدينة}')
        plt.xlabel('المساحة (م²)')
        plt.ylabel('السعر (ريال)')
        st.pyplot(fig)
        
        # عرض البيانات
        st.subheader("📋 البيانات التفصيلية")
        st.dataframe(df)

st.markdown("---")
st.markdown("📞 للتواصل: warda@realestate.com | 💰 الأسعار تبدأ من 100$")
