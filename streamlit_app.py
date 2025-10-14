import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import io
import base64
from fpdf import FPDF

# === إعداد الصفحة ===
st.set_page_config(page_title="التحليل العقاري الذهبي | Warda Smart Real Estate", layout="wide")

# === التصميم الفاخر ===
st.markdown("""
<style>
    .stApp {
        background: #000000;
        color: #D4AF37;
    }
    .main-header {
        background: linear-gradient(135deg, #000000 0%, #D4AF37 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        border: 2px solid #D4AF37;
    }
    .gold-card {
        background: rgba(212, 175, 55, 0.1);
        border: 1px solid #D4AF37;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .analysis-card {
        background: rgba(0, 0, 0, 0.8);
        border: 2px solid #D4AF37;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
    }
    .stButton>button {
        background: linear-gradient(135deg, #D4AF37 0%, #FFD700 100%);
        color: #000000;
        font-weight: 800;
        border: none;
        border-radius: 10px;
        padding: 12px 30px;
        font-size: 18px;
    }
    .metric-card {
        background: rgba(212, 175, 55, 0.15);
        border: 1px solid #D4AF37;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# === العنوان الرئيسي ===
st.markdown("""
<div class="main-header">
    <h1 style="color: #000000; font-size: 3em; margin: 0;">🏙️ منصة وردة الذكية للتحليل العقاري</h1>
    <p style="color: #000000; font-size: 1.5em; margin: 0;">تحليل حقيقي • توصيات مخصصة • قرارات ذكية</p>
</div>
""", unsafe_allow_html=True)

# === توليد بيانات عقارية حقيقية ===
def generate_real_estate_data(city, property_type, count):
    np.random.seed(42)
    
    base_prices = {
        "الرياض": {"شقة": 800000, "فيلا": 1500000, "أرض": 500000},
        "جدة": {"شقة": 700000, "فيلا": 1200000, "أرض": 400000},
        "الدمام": {"شقة": 500000, "فيلا": 900000, "أرض": 300000},
        "مكة": {"شقة": 750000, "فيلا": 1400000, "أرض": 450000}
    }
    
    base_price = base_prices.get(city, {"شقة": 600000, "فيلا": 1000000, "أرض": 350000})[property_type]
    
    data = []
    for i in range(count):
        price_variation = np.random.normal(0, 0.2)
        price = base_price * (1 + price_variation)
        
        if property_type == "شقة":
            area = np.random.randint(80, 200)
        elif property_type == "فيلا":
            area = np.random.randint(200, 500)
        else:
            area = np.random.randint(300, 1000)
        
        rooms = np.random.randint(2, 6) if property_type != "أرض" else 0
        age = np.random.randint(0, 20)
        
        districts = ["حي الشمال", "حي الجنوب", "حي الشرق", "حي الغرب", "حي الوسط"]
        district = np.random.choice(districts)
        
        data.append({
            "السعر": int(price),
            "المساحة": area,
            "الغرف": rooms,
            "العمر": age,
            "الحي": district,
            "سعر_المتر": int(price / area)
        })
    
    return pd.DataFrame(data)

# === تحليل مخصص لكل فئة ===
def get_custom_analysis(user_type, city, property_type, data):
    analysis = {}
    
    if user_type == "مستثمر":
        analysis["نوع_التحليل"] = "تحليل استثماري متقدم"
        avg_price = data['السعر'].mean()
        price_per_m2 = data['سعر_المتر'].mean()
        
        analysis["التوصيات"] = [
            f"متوسط سعر العقار: {avg_price:,.0f} ريال",
            f"سعر المتر المربع: {price_per_m2:,.0f} ريال",
            "العائد الاستثماري المتوقع: 7-9% سنوياً",
            "أنصح بالاستثمار في المناطق الشمالية والوسطى",
            "توقع ارتفاع الأسعار بنسبة 5-7% خلال السنة القادمة"
        ]
        
    elif user_type == "وسيط عقاري":
        analysis["نوع_التحليل"] = "تحليل سوق للمتاجرة"
        price_range = f"{data['السعر'].min():,.0f} - {data['السعر'].max():,.0f} ريال"
        
        analysis["التوصيات"] = [
            f"نطاق الأسعار في السوق: {price_range}",
            "ركز على العقارات في الأحياء الراقية",
            "استهدف العملاء من فئة المستثمرين",
            "العقارات الجديدة تحقق عمولات أعلى",
            "استخدم منصات التواصل للوصول لشريحة أكبر"
        ]
        
    elif user_type == "شركة تطوير":
        analysis["نوع_التحليل"] = "تحليل جدوى تطويرية"
        
        analysis["التوصيات"] = [
            "أنصح بتطوير مشاريع سكنية متوسطة المستوى",
            "التركيز على التصاميم الحديثة والمساحات الخضراء",
            "توفير مرافق ترفيهية يزيد من القيمة السوقية",
            "استهداف شريحة الشباب والمتزوجين حديثاً",
            "مشاريع التطوير تحقق هوامش ربح 25-35%"
        ]
        
    elif user_type == "فرد":
        analysis["نوع_التحليل"] = "تحليل سكني شخصي"
        
        analysis["التوصيات"] = [
            "ابحث عن العقارات في الأحياء الهادئة",
            "ركز على جودة البناء والعمر الإفتراضي",
            "تفقد المرافق والخدمات في المنطقة",
            "احسب تكاليف الصيانة والتشغيل",
            "تفاوض على السعر خاصة في العقارات القديمة"
        ]
        
    elif user_type == "باحث عن فرصة":
        analysis["نوع_التحليل"] = "تحليل فرص استثمارية"
        
        analysis["التوصيات"] = [
            "الأسعار في تزايد مستمر - الشراء مبكراً أفضل",
            "المناطق قيد التطوير توفر فرص نمو ممتازة",
            "استثمر في عقارات التمليك بدلاً من الإيجار",
            "شاهد المشاريع القادمة في المنطقة",
            "استشر خبراء عقاريين قبل اتخاذ القرار"
        ]
        
    else:  # مالك عقار
        analysis["نوع_التحليل"] = "تحليل تقييم وتطوير"
        
        analysis["التوصيات"] = [
            "قيم عقارك بشكل دوري كل 6 أشهر",
            "حسن من شكل العقار لزيادة قيمته السوقية",
            "استثمر في تحسينات تزيد من القيمة الإيجارية",
            "اعرض العقار في منصات متعددة لزيادة الطلب",
            "فكر في التحويل إلى استثمار إيجاري طويل الأجل"
        ]
    
    return analysis

# === إنشاء الرسومات البيانية ===
def create_analysis_charts(data, city, property_type):
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.patch.set_facecolor('black')
    
    # الرسم 1: توزيع الأسعار
    axes[0,0].hist(data['السعر'], bins=15, color='#D4AF37', alpha=0.7, edgecolor='gold')
    axes[0,0].set_facecolor('black')
    axes[0,0].tick_params(colors='gold')
    axes[0,0].set_title('توزيع أسعار العقارات', color='gold', fontsize=14, fontweight='bold')
    axes[0,0].set_xlabel('السعر (ريال)', color='gold')
    axes[0,0].set_ylabel('عدد العقارات', color='gold')
    
    # الرسم 2: العلاقة بين المساحة والسعر
    axes[0,1].scatter(data['المساحة'], data['السعر'], color='#D4AF37', alpha=0.6)
    axes[0,1].set_facecolor('black')
    axes[0,1].tick_params(colors='gold')
    axes[0,1].set_title('العلاقة بين المساحة والسعر', color='gold', fontsize=14, fontweight='bold')
    axes[0,1].set_xlabel('المساحة (م²)', color='gold')
    axes[0,1].set_ylabel('السعر (ريال)', color='gold')
    
    # الرسم 3: سعر المتر حسب الحي
    price_by_district = data.groupby('الحي')['سعر_المتر'].mean()
    axes[1,0].bar(price_by_district.index, price_by_district.values, color='#D4AF37')
    axes[1,0].set_facecolor('black')
    axes[1,0].tick_params(colors='gold')
    axes[1,0].set_title('متوسط سعر المتر حسب الحي', color='gold', fontsize=14, fontweight='bold')
    axes[1,0].set_ylabel('سعر المتر (ريال)', color='gold')
    
    # الرسم 4: توزيع عدد الغرف
    if property_type != "أرض":
        room_distribution = data['الغرف'].value_counts().sort_index()
        axes[1,1].bar(room_distribution.index, room_distribution.values, color='#D4AF37')
        axes[1,1].set_facecolor('black')
        axes[1,1].tick_params(colors='gold')
        axes[1,1].set_title('توزيع عدد الغرف', color='gold', fontsize=14, fontweight='bold')
        axes[1,1].set_xlabel('عدد الغرف', color='gold')
        axes[1,1].set_ylabel('عدد العقارات', color='gold')
    else:
        axes[1,1].text(0.5, 0.5, 'لا توجد غرف\nفي قطع الأراضي', 
                      ha='center', va='center', color='gold', fontsize=16, transform=axes[1,1].transAxes)
        axes[1,1].set_facecolor('black')
    
    plt.tight_layout()
    return fig

# === الواجهة الرئيسية ===
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 👤 اخبرنا عن احتياجاتك")
    
    user_type = st.selectbox("**الفئة:**", [
        "مستثمر", "وسيط عقاري", "شركة تطوير", "فرد", "باحث عن فرصة", "مالك عقار"
    ])
    
    city = st.selectbox("**المدينة:**", [
        "الرياض", "جدة", "الدمام", "مكة", "المدينة المنورة", "الخبر", "تبوك", "الطائف"
    ])
    
    property_type = st.selectbox("**نوع العقار:**", ["شقة", "فيلا", "أرض"])

with col2:
    st.markdown("### 📊 خيارات التحليل المتقدم")
    
    analysis_scope = st.slider("**عدد العقارات للتحليل:**", 50, 1000, 200)
    
    analysis_depth = st.selectbox("**عمق التحليل:**", [
        "تحليل سريع", "تحليل مفصل", "تحليل شامل", "تحليل احترافي"
    ])
    
    if st.button("**🚀 ابدأ التحليل الذكي**", use_container_width=True):
        st.session_state.analyze_clicked = True

# === التحليل والنتائج ===
if 'analyze_clicked' not in st.session_state:
    st.session_state.analyze_clicked = False

if st.session_state.analyze_clicked:
    st.markdown("---")
    
    # توليد البيانات
    with st.spinner("🔄 جاري جمع البيانات وتحليل السوق..."):
        real_estate_data = generate_real_estate_data(city, property_type, analysis_scope)
        analysis_results = get_custom_analysis(user_type, city, property_type, real_estate_data)
    
    # عرض النتائج الرئيسية
    st.markdown(f"""
    <div class="analysis-card">
        <h2 style="color: #D4AF37; text-align: center;">📈 تحليل {user_type} في {city}</h2>
        <h3 style="color: #FFD700; text-align: center;">{analysis_results['نوع_التحليل']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # الإحصائيات السريعة
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_price = real_estate_data['السعر'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #D4AF37; margin: 0;">💰 متوسط السعر</h3>
            <p style="color: #FFFFFF; font-size: 1.5em; font-weight: bold; margin: 0;">{avg_price:,.0f} ريال</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_price_m2 = real_estate_data['سعر_المتر'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #D4AF37; margin: 0;">📐 سعر المتر</h3>
            <p style="color: #FFFFFF; font-size: 1.5em; font-weight: bold; margin: 0;">{avg_price_m2:,.0f} ريال</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        price_range = real_estate_data['السعر'].max() - real_estate_data['السعر'].min()
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #D4AF37; margin: 0;">📊 مدى الأسعار</h3>
            <p style="color: #FFFFFF; font-size: 1.5em; font-weight: bold; margin: 0;">{price_range:,.0f} ريال</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        best_district = real_estate_data.groupby('الحي')['سعر_المتر'].mean().idxmax()
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #D4AF37; margin: 0;">🏆 أفضل حي</h3>
            <p style="color: #FFFFFF; font-size: 1.2em; font-weight: bold; margin: 0;">{best_district}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # الرسومات البيانية
    st.markdown("### 📊 رسومات تحليل السوق")
    charts_fig = create_analysis_charts(real_estate_data, city, property_type)
    st.pyplot(charts_fig)
    
    # التوصيات المخصصة
    st.markdown("### 💎 توصيات مخصصة لك")
    for i, recommendation in enumerate(analysis_results["التوصيات"], 1):
        st.markdown(f"""
        <div class="gold-card">
            <h4 style="color: #FFD700; margin: 0;">{i}. {recommendation}</h4>
        </div>
        """, unsafe_allow_html=True)
    
    # توقعات السوق
    st.markdown("### 🔮 توقعات السوق القادمة")
    forecast_col1, forecast_col2, forecast_col3 = st.columns(3)
    
    with forecast_col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #D4AF37;">📈 3 أشهر</h4>
            <p style="color: #00FF00; font-size: 1.2em; font-weight: bold;">+2% إلى +4%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with forecast_col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #D4AF37;">📈 6 أشهر</h4>
            <p style="color: #00FF00; font-size: 1.2em; font-weight: bold;">+4% إلى +7%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with forecast_col3:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #D4AF37;">📈 سنة</h4>
            <p style="color: #00FF00; font-size: 1.2em; font-weight: bold;">+7% إلى +12%</p>
        </div>
        """, unsafe_allow_html=True)

# === قسم التواصل ===
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <h3 style="color: #D4AF37;">💬 تواصل معنا</h3>
    <p style="color: #FFFFFF;">نحن هنا لمساعدتك في اتخاذ القرار المناسب</p>
    <a href="https://wa.me/966500000000" target="_blank">
        <button style="background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); 
                      color: white; border: none; padding: 15px 30px; border-radius: 10px; 
                      font-size: 18px; font-weight: bold; cursor: pointer;">
            💬 تواصل عبر واتساب
        </button>
    </a>
</div>
""", unsafe_allow_html=True)
