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

st.set_page_config(page_title="Warda Realty", page_icon="🏠", layout="wide")

# العنوان الرئيسي المحسن
st.markdown(
    """
    <style>
    .big-title { 
        font-size: 32px; 
        color: #0b3d91; 
        font-weight: 700; 
        text-align: center;
        margin-bottom: 10px;
    }
    .sub { 
        color: #b8860b; 
        font-weight: 600; 
        text-align: center;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown('<div class="big-title">🏡 Warda Realty | وردة العقارية</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Smart AI-Powered Real Estate Insights | تحليلات عقارية ذكية</div>', unsafe_allow_html=True)
st.markdown("---")

# محاولة استيراد نظام Scraping
try:
    from scraper_engine import WardaScraper
    from data_cleaner import DataCleaner
    REAL_DATA_AVAILABLE = True
except ImportError as e:
    st.sidebar.warning("⚠️ نظام البيانات الحية غير متوفر حالياً")
    REAL_DATA_AVAILABLE = False

# اختيار اللغة
col_lang1, col_lang2 = st.columns([1, 1])
with col_lang1:
    lang = st.selectbox("اللغة / Language:", ["عربي", "English"])

# واجهة المستخدم
if lang == "عربي":
    st.header("📊 نظام التحليل العقاري المتقدم")
    city_label = "المدينة"
    district_label = "الحي (اختياري)"
    property_label = "نوع العقار"
    package_label = "اختر الباقة"
    days_label = "أيام التنبؤ"
    real_data_label = "استخدام بيانات حية من السوق"
    generate_report = "إنشاء التقرير"
else:
    st.header("📊 Advanced Real Estate Analysis System")
    city_label = "City"
    district_label = "District (optional)"
    property_label = "Property Type"
    package_label = "Choose Package"
    days_label = "Prediction Days"
    real_data_label = "Use live market data"
    generate_report = "Generate Report"

# نموذج الإدخال
col1, col2 = st.columns(2)
with col1:
    city = st.selectbox(city_label, ["الرياض", "جدة", "الدمام", "مكة", "المدينة"])
    property_type = st.selectbox(property_label, ["شقة", "فيلا", "أرض"])
    
with col2:
    district = st.text_input(district_label, placeholder="أدخل اسم الحي إن أردت")
    prediction_days = st.selectbox(days_label, [14, 30, 60])

# خيار البيانات الحية
use_real_data = False
if REAL_DATA_AVAILABLE:
    use_real_data = st.checkbox(real_data_label, value=False)
    if use_real_data:
        st.info("🔄 سيتم جمع أحدث البيانات من منصات العقار مباشرة")

# زر التشغيل
if st.button(f"🚀 {generate_report}", type="primary", use_container_width=True):
    
    with st.spinner("جاري معالجة طلبك..." if lang == "عربي" else "Processing your request..."):
        
        # جمع البيانات
        if use_real_data and REAL_DATA_AVAILABLE:
            with st.spinner("جاري جمع أحدث البيانات من السوق..." if lang == "عربي" else "Collecting latest market data..."):
                scraper = WardaScraper()
                scraper.scrape_aqar(city, property_type)
                scraper.scrape_bayut(city, property_type)
                
                if scraper.data:
                    df = pd.DataFrame(scraper.data)
                    cleaner = DataCleaner(df)
                    data = cleaner.clean_data()
                    st.success(f"✅ تم جمع {len(data)} عقار من السوق الحقيقي")
                else:
                    st.warning("⚠️ استخدام البيانات التجريبية مؤقتاً")
                    data = _get_sample_data(city, property_type)
        else:
            data = _get_sample_data(city, property_type)
            st.info("📊 استخدام بيانات تجريبية - لبيانات حقيقية شغل خيار البيانات الحية")
        
        if data is not None and not data.empty:
            # عرض النتائج
            st.subheader("📈 نتائج التحليل" if lang == "عربي" else "Analysis Results")
            
            # الإحصائيات
            col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
            with col_stat1:
                avg_price = data['Price'].mean()
                st.metric("💰 متوسط السعر" if lang == "عربي" else "Average Price", 
                         f"{avg_price:,.0f} ريال" if lang == "عربي" else f"{avg_price:,.0f} SAR")
            
            with col_stat2:
                avg_area = data['Area'].mean()
                st.metric("📐 متوسط المساحة" if lang == "عربي" else "Average Area", 
                         f"{avg_area:.0f} م²" if lang == "عربي" else f"{avg_area:.0f} m²")
            
            with col_stat3:
                price_per_sqm = avg_price / avg_area
                st.metric("📊 سعر المتر" if lang == "عربي" else "Price per SQM", 
                         f"{price_per_sqm:,.0f} ريال" if lang == "عربي" else f"{price_per_sqm:,.0f} SAR")
            
            with col_stat4:
                total_properties = len(data)
                st.metric("🏠 عدد العقارات" if lang == "عربي" else "Total Properties", 
                         f"{total_properties} عقار" if lang == "عربي" else f"{total_properties}")
            
            # الرسم البياني
            st.subheader("📊 توزيع الأسعار والمساحات" if lang == "عربي" else "Price & Area Distribution")
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
            
            # توزيع الأسعار
            ax1.hist(data['Price'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
            ax1.set_xlabel('السعر (ريال)' if lang == "عربي" else 'Price (SAR)')
            ax1.set_ylabel('التكرار' if lang == "عربي" else 'Frequency')
            ax1.set_title('توزيع الأسعار' if lang == "عربي" else 'Price Distribution')
            ax1.ticklabel_format(style='plain', axis='x')
            
            # العلاقة بين المساحة والسعر
            ax2.scatter(data['Area'], data['Price'], alpha=0.6, color='coral')
            ax2.set_xlabel('المساحة (م²)' if lang == "عربي" else 'Area (m²)')
            ax2.set_ylabel('السعر (ريال)' if lang == "عربي" else 'Price (SAR)')
            ax2.set_title('العلاقة بين المساحة والسعر' if lang == "عربي" else 'Area vs Price')
            ax2.ticklabel_format(style='plain', axis='y')
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # أفضل العروض
            st.subheader("🏆 أفضل العروض" if lang == "عربي" else "Best Offers")
            data['Price_Per_SQM'] = data['Price'] / data['Area']
            best_offers = data.nsmallest(5, 'Price_Per_SQM')
            st.dataframe(best_offers[['Title', 'District', 'Price', 'Area', 'Price_Per_SQM']])
            
        else:
            st.error("❌ لا توجد بيانات متاحة للعرض" if lang == "عربي" else "No data available")

# قسم المعلومات
st.markdown("---")
st.subheader("💡 معلومات عن الخدمة" if lang == "عربي" else "Service Information")

col_info1, col_info2 = st.columns(2)
with col_info1:
    st.markdown("""
    **مميزات وردة العقارية:**
    - تحليل أسعار حقيقي من السوق
    - بيانات محدثة يومياً
    - تنبؤات ذكية بالأسعار
    - تقارير PDF مفصلة
    - واجهة عربية وإنجليزية
    """ if lang == "عربي" else """
    **Warda Realty Features:**
    - Real market price analysis
    - Daily updated data
    - AI-powered price predictions
    - Detailed PDF reports
    - Arabic & English interface
    """)

with col_info2:
    st.markdown("""
    **الباقات المتاحة:**
    - 🟢 باقة أساسية: تحليل سريع
    - 🟡 باقة متقدمة: تحليل مفصل
    - 🔴 باقة متميزة: دراسة شاملة
    """ if lang == "عربي" else """
    **Available Packages:**
    - 🟢 Basic: Quick analysis
    - 🟡 Advanced: Detailed analysis
    - 🔴 Premium: Comprehensive study
    """)

# وظيفة البيانات التجريبية
def _get_sample_data(city, property_type):
    """إرجاع بيانات تجريبية"""
    np.random.seed(42)
    sample_size = 50
    
    # أسعار واقعية بناءً على المدينة ونوع العقار
    price_ranges = {
        'الرياض': {'شقة': (600000, 1500000), 'فيلا': (2000000, 5000000), 'أرض': (800000, 3000000)},
        'جدة': {'شقة': (500000, 1200000), 'فيلا': (1500000, 4000000), 'أرض': (600000, 2500000)},
        'الدمام': {'شقة': (400000, 1000000), 'فيلا': (1200000, 3000000), 'أرض': (500000, 2000000)},
    }
    
    price_range = price_ranges.get(city, price_ranges['الرياض']).get(property_type, (500000, 2000000))
    
    data = {
        'Title': [f'{property_type} {i+1} في {city}' for i in range(sample_size)],
        'City': [city] * sample_size,
        'District': [np.random.choice(['النخيل', 'الروضة', 'الصفا', 'الزهراء', 'الربوة']) for _ in range(sample_size)],
        'Property_Type': [property_type] * sample_size,
        'Price': np.random.randint(price_range[0], price_range[1], sample_size),
        'Area': np.random.randint(80, 400, sample_size),
        'Source': ['Sample Data'] * sample_size,
        'Date': [datetime.now().strftime('%Y-%m-%d')] * sample_size
    }
    
    return pd.DataFrame(data)

# تذييل الصفحة
st.markdown("---")
st.markdown(
    "✨ **Warda Realty 2024** | تواصل معنا: info@wardarealty.com" if lang == "عربي" 
    else "✨ **Warda Realty 2024** | Contact: info@wardarealty.com"
)
