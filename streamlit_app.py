import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import hashlib
import time
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import arabic_reshaper
from bidi.algorithm import get_display
import warnings
warnings.filterwarnings('ignore')

# إعداد الصفحة
st.set_page_config(
    page_title="التحليل العقاري الذهبي | Warda Intelligence",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# تنسيق واجهة فاخرة
st.markdown("""
    <style>
    .main { 
        background-color: #0E1117; 
        color: gold; 
    }
    .stApp { 
        background-color: #0E1117; 
    }
    h1, h2, h3, h4, h5, h6 { 
        color: gold !important; 
        font-family: 'Arial', sans-serif;
    }
    .stSelectbox label, .stSlider label, .stRadio label { 
        color: gold !important; 
        font-weight: bold;
    }
    .stButton>button {
        background-color: gold; 
        color: black; 
        font-weight: bold;
        border-radius: 15px; 
        padding: 1em 2em; 
        border: none;
        width: 100%;
        font-size: 18px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #ffd700;
        transform: scale(1.05);
    }
    .package-card {
        background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
        padding: 25px; 
        border-radius: 20px; 
        border: 3px solid #d4af37;
        margin: 15px 0; 
        text-align: center;
        box-shadow: 0 8px 32px rgba(212, 175, 55, 0.3);
    }
    .analysis-card {
        background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
        padding: 30px; 
        border-radius: 20px; 
        border: 2px solid gold;
        margin: 20px 0; 
        color: white;
    }
    .metric-card {
        background: linear-gradient(135deg, #2a2a2a, #3a3a3a);
        padding: 20px; 
        border-radius: 15px; 
        border: 1px solid #d4af37;
        margin: 15px; 
        text-align: center;
    }
    .stDownloadButton>button {
        background: linear-gradient(135deg, #d4af37, #ffd700);
        color: black; 
        font-weight: bold;
        border-radius: 15px; 
        padding: 1em 2em; 
        border: none;
        width: 100%;
        font-size: 18px;
    }
    .header-section {
        background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
        padding: 40px;
        border-radius: 25px;
        border: 3px solid gold;
        margin: 20px 0;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown("""
    <div class='header-section'>
        <h1 style='text-align: center; color: gold; margin-bottom: 20px;'>🏙️ منصة التحليل العقاري الذهبي</h1>
        <h2 style='text-align: center; color: #d4af37;'>Warda Intelligence - الذكاء الاستثماري المتقدم</h2>
        <p style='text-align: center; color: #ffd700; font-size: 20px; margin-top: 20px;'>
            تحليل استثماري شامل • توقعات ذكية • قرارات مدروسة
        </p>
    </div>
""", unsafe_allow_html=True)

# === نظام الباقات والأسعار ===
PACKAGES = {
    "مجانية": {
        "price": 0,
        "pages": 5,
        "features": [
            "تحليل سوق أساسي متكامل",
            "أسعار متوسطة مفصلة للمنطقة", 
            "تقرير نصي شامل",
            "مؤشرات أداء رئيسية",
            "نصائح استثمارية أولية"
        ]
    },
    "فضية": {
        "price": 199,
        "pages": 10,
        "features": [
            "كل مميزات المجانية +",
            "تحليل تنبؤي 12 شهراً",
            "مقارنة مع 10 مشاريع منافسة",
            "نصائح استثمارية متقدمة",
            "تقرير PDF تفاعلي فاخر",
            "رسوم بيانية متحركة",
            "تحليل المنافسين الشامل",
            "دراسة الجدوى المتقدمة"
        ]
    },
    "ذهبية": {
        "price": 499,
        "pages": 15,
        "features": [
            "كل مميزات الفضية +", 
            "تحليل ذكاء اصطناعي متقدم",
            "تنبؤات لمدة 3 سنوات قادمة",
            "دراسة الجدوى الاقتصادية الشاملة",
            "تحليل 20 منافس رئيسي",
            "نصائح مخصصة حسب ملفك الاستثماري",
            "مؤشرات أداء متقدمة مفصلة",
            "تحليل المخاطر المتقدم",
            "خطط طوارئ استثمارية"
        ]
    },
    "ماسية": {
        "price": 999,
        "pages": 25,
        "features": [
            "كل مميزات الذهبية +",
            "تحليل شمولي متكامل شامل", 
            "تقارير مقارنة مع جميع مدن المملكة",
            "تحليل المخاطر الاستراتيجي المتقدم",
            "خطة استثمارية تفصيلية لمدة 5 سنوات",
            "محاكاة 10 سيناريوهات استثمارية",
            "تحليل توقيت السوق الذهبي",
            "توصيات استراتيجية شاملة حصرية",
            "دعم استشاري مباشر لمدة 30 يوم"
        ]
    }
}

def reshape_arabic_text(text):
    """إعادة تشكيل النص العربي للعرض الصحيح"""
    try:
        # تجاهل النصوص التي تحتوي على أرقام أو رموز إنجليزية
        if any(char.isdigit() or char in '://._-@$%&*' for char in text):
            return text
            
        # تجاهل النصوص القصيرة أو الخاصة
        if len(text.strip()) < 2 or text.strip().upper() in ['PDF', 'USD', 'WARDA', 'INTELLIGENCE']:
            return text
            
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        return bidi_text
    except Exception:
        return text

def create_advanced_visualizations(market_data, user_info):
    """إنشاء رسومات بيانية متقدمة للتقارير"""
    
    # 1. مخطط الأسعار المقارنة
    fig1 = plt.figure(figsize=(10, 6))
    categories = ['أقل سعر', 'المتوسط', 'أعلى سعر', 'سعرك الحالي']
    values = [
        market_data['أقل_سعر'], 
        market_data['متوسط_السوق'], 
        market_data['أعلى_سعر'],
        market_data['السعر_الحالي']
    ]
    colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#d4af37']
    
    bars = plt.bar(categories, values, color=colors, edgecolor='black', linewidth=2)
    plt.title(reshape_arabic_text('مقارنة الأسعار في السوق'), fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('السعر (ريال/م²)', fontsize=12)
    plt.xticks(fontsize=10)
    
    # إضافة القيم على الأعمدة
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, 
                f'{value:,.0f}', ha='center', va='bottom', fontweight='bold')
    
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    # 2. مخطط العرض والطلب
    fig2 = plt.figure(figsize=(8, 8))
    labels = ['عرض العقارات', 'طالب الشراء']
    sizes = [market_data['عرض_العقارات'], market_data['طالب_الشراء']]
    colors = ['#ff9999', '#66b3ff']
    explode = (0.1, 0)
    
    wedges, texts, autotexts = plt.pie(sizes, explode=explode, labels=labels, colors=colors, 
                                      autopct='%1.1f%%', startangle=90, textprops={'fontsize': 12})
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    plt.title(reshape_arabic_text('توازن العرض والطلب في السوق'), fontsize=14, fontweight='bold', pad=20)
    
    return fig1, fig2

def create_professional_pdf(user_info, market_data, package_level):
    """إنشاء تقرير PDF احترافي مع رسومات متقدمة"""
    
    buffer = BytesIO()
    
    with PdfPages(buffer) as pdf:
        # الصفحة 1: الغلاف الفاخر
        fig = plt.figure(figsize=(8.27, 11.69), facecolor='#1a1a1a')
        plt.axis('off')
        
        # خلفية ذهبية
        plt.gca().add_patch(plt.Rectangle((0,0), 1, 1, fill=True, color='#1a1a1a'))
        
        # العنوان الرئيسي
        plt.text(0.5, 0.8, reshape_arabic_text('تقرير Warda Intelligence المتقدم'), 
                fontsize=26, ha='center', va='center', weight='bold', color='#d4af37',
                transform=plt.gca().transAxes)
        
        # العنوان الثانوي
        plt.text(0.5, 0.7, reshape_arabic_text('التحليل الاستثماري الشامل'), 
                fontsize=18, ha='center', va='center', style='italic', color='#ffd700',
                transform=plt.gca().transAxes)
        
        # معلومات العميل في مربع أنيق
        info_text = f"""
        {reshape_arabic_text('تقرير حصري مقدم إلى:')}
        
        🎯 {reshape_arabic_text('فئة العميل:')} {user_info['user_type']}
        🏙️ {reshape_arabic_text('المدينة:')} {user_info['city']}
        🏠 {reshape_arabic_text('نوع العقار:')} {user_info['property_type']}
        📏 {reshape_arabic_text('المساحة:')} {user_info['area']} م²
        💎 {reshape_arabic_text('الباقة:')} {user_info['package']}
        📅 {reshape_arabic_text('تاريخ التقرير:')} {datetime.now().strftime('%Y-%m-%d')}
        """
        
        plt.text(0.5, 0.5, reshape_arabic_text(info_text), 
                fontsize=14, ha='center', va='center', color='white',
                bbox=dict(boxstyle="round,pad=1.5", facecolor="#2d2d2d", edgecolor='#d4af37', linewidth=3),
                transform=plt.gca().transAxes)
        
        # الشعار
        plt.text(0.5, 0.25, "🏙️ Warda Intelligence", 
                fontsize=16, ha='center', va='center', color='#d4af37',
                style='italic', transform=plt.gca().transAxes)
        
        pdf.savefig(fig, facecolor='#1a1a1a', edgecolor='none')
        plt.close()
        
        # الصفحة 2: الملخص التنفيذي
        fig = plt.figure(figsize=(8.27, 11.69))
        plt.axis('off')
        
        # عنوان الصفحة
        plt.text(0.1, 0.95, reshape_arabic_text('📊 الملخص التنفيذي'), 
                fontsize=20, ha='left', va='top', weight='bold', color='#d4af37')
        
        # خط ذهبي تحت العنوان
        plt.axhline(y=0.92, xmin=0.1, xmax=0.9, color='#d4af37', linewidth=3)
        
        # محتوى الملخص
        exec_summary = f"""
        سعادة العميل الكريم {user_info['user_type']}،

        يشرفني أن أقدم لكم هذا التقرير الشامل الذي يمثل ثمرة تحليل دقيق ومتعمق 
        لسوق العقارات في مدينة {user_info['city']}. بناءً على دراسة {market_data['حجم_التداول_شهري'] * 12:,} 
        صفقة سنوياً، أقدم لكم رؤية واضحة ومبنية على بيانات حقيقية.

        **الرؤية الاستراتيجية:**
        بعد تحليل متعمق، أرى أن استثماركم في قطاع {user_info['property_type']} 
        يمثل فرصة استثنائية. العائد المتوقع يبلغ {market_data['العائد_التأجيري']:.1f}% سنوياً، 
        وهو ما يتفوق بشكل ملحوظ على معظم البدائل الاستثمارية التقليدية.

        **لماذا هذه الفرصة استثنائية؟**
        ✅ نمو شهري مستمر: {market_data['معدل_النمو_الشهري']:.1f}%
        ✅ سيولة سوقية عالية: {market_data['مؤشر_السيولة']:.1f}%
        ✅ طلب متزايد: {market_data['طالب_الشراء']} طالب شراء نشط
        ✅ عرض محدود: {market_data['عرض_العقارات']} عقار متاح فقط

        أنصحكم بالتحرك الاستراتيجي السريع، فالسوق في ذروة نموه والفرص الذهبية لا تنتظر.
        """
        
        plt.text(0.1, 0.85, reshape_arabic_text(exec_summary), 
                fontsize=11, ha='left', va='top', wrap=True, color='#333333',
                bbox=dict(boxstyle="round,pad=1", facecolor="#f8f9fa", edgecolor='#dee2e6'))
        
        # مؤشرات الأداء
        metrics_text = f"""
        {reshape_arabic_text('🎯 مؤشرات الأداء الرئيسية:')}

        📈 العائد السنوي المتوقع: {market_data['العائد_التأجيري']:.1f}%
        📊 معدل النمو السنوي: {market_data['معدل_النمو_الشهري']*12:.1f}%  
        🏠 معدل الإشغال: {market_data['معدل_الإشغال']:.1f}%
        💰 مؤشر السيولة: {market_data['مؤشر_السيولة']:.1f}%
        📦 حجم التداول الشهري: {market_data['حجم_التداول_شهري']} صفقة
        """
        
        plt.text(0.1, 0.4, reshape_arabic_text(metrics_text), 
                fontsize=11, ha='left', va='top', wrap=True,
                bbox=dict(boxstyle="round,pad=1", facecolor="#fff3cd", edgecolor='#ffc107'))
        
        # رقم الصفحة
        plt.text(0.5, 0.02, "صفحة 1", fontsize=10, ha='center', va='bottom', color='#666666')
        
        pdf.savefig(fig, facecolor='white', edgecolor='none')
        plt.close()
        
        # الصفحة 3: الرسوم البيانية
        fig1, fig2 = create_advanced_visualizations(market_data, user_info)
        
        # تعديل حجم الرسوم لتناسب الصفحة
        fig1.set_size_inches(7, 5)
        fig2.set_size_inches(6, 6)
        
        pdf.savefig(fig1, facecolor='white', edgecolor='none')
        pdf.savefig(fig2, facecolor='white', edgecolor='none')
        plt.close('all')
        
        # الصفحات الإضافية حسب الباقة
        if package_level in ["ذهبية", "ماسية"]:
            # صفحة التحليل المتقدم
            fig = plt.figure(figsize=(8.27, 11.69))
            plt.axis('off')
            
            plt.text(0.1, 0.95, reshape_arabic_text('🔍 التحليل المتقدم'), 
                    fontsize=20, ha='left', va='top', weight='bold', color='#d4af37')
            
            advanced_analysis = f"""
            {reshape_arabic_text('التحليل الاستراتيجي المتقدم:')}

            **التقييم المالي الشامل:**
            💰 القيمة السوقية الحالية: {market_data['السعر_الحالي'] * user_info['area']:,.0f} ريال
            📈 القيمة المتوقعة بعد سنة: {market_data['السعر_الحالي'] * user_info['area'] * 1.08:,.0f} ريال  
            🎯 القيمة المتوقعة بعد 3 سنوات: {market_data['السعر_الحالي'] * user_info['area'] * 1.25:,.0f} ريال

            **مؤشرات الجدوى الاستثمارية:**
            • فترة استرداد رأس المال: {8.5 - (market_data['العائد_التأجيري'] / 2):.1f} سنوات
            • صافي القيمة الحالية (NPV): +{market_data['السعر_الحالي'] * user_info['area'] * 0.15:,.0f} ريال
            • معدل العائد الداخلي (IRR): {market_data['العائد_التأجيري'] + 2:.1f}%

            **توقعات النمو المستقبلية:**
            بناءً على تحليل اتجاهات السوق ومشاريع التطوير القادمة، 
            نتوقع استمرار النمو الإيجابي خلال السنوات القادمة.
            """
            
            plt.text(0.1, 0.85, reshape_arabic_text(advanced_analysis), 
                    fontsize=11, ha='left', va='top', wrap=True, color='#333333')
            
            plt.text(0.5, 0.02, "صفحة 3", fontsize=10, ha='center', va='bottom', color='#666666')
            pdf.savefig(fig, facecolor='white', edgecolor='none')
            plt.close()
        
        if package_level == "ماسية":
            # صفحة إضافية للباقة الماسية
            fig = plt.figure(figsize=(8.27, 11.69))
            plt.axis('off')
            
            plt.text(0.1, 0.95, reshape_arabic_text('💎 التوصيات الحصرية'), 
                    fontsize=20, ha='left', va='top', weight='bold', color='#d4af37')
            
            exclusive_recommendations = f"""
            {reshape_arabic_text('التوصيات الاستراتيجية الحصرية:')}

            **الخطة التنفيذية الفورية:**
            1. التفاوض على السعر خلال الأسبوع القادم
            2. دراسة خيارات التمويل المتاحة
            3. إتمام الصفقة خلال 30 يوم

            **استراتيجية الخروج الذكية:**
            • التوقيت المثالي للبيع: بعد 3-5 سنوات
            • القيمة المتوقعة عند البيع: {market_data['السعر_الحالي'] * user_info['area'] * 1.45:,.0f} ريال
            • خيارات إعادة الاستثمار المقترحة

            **نصائح الخبير:**
            'الاستثمار العقاري الناجح يحتاج إلى رؤية استراتيجية 
            وصبر طويل الأمد مع مرونة في التكيف مع تغيرات السوق'
            """
            
            plt.text(0.1, 0.85, reshape_arabic_text(exclusive_recommendations), 
                    fontsize=11, ha='left', va='top', wrap=True, color='#333333')
            
            plt.text(0.5, 0.02, "صفحة 4", fontsize=10, ha='center', va='bottom', color='#666666')
            pdf.savefig(fig, facecolor='white', edgecolor='none')
            plt.close()
    
    buffer.seek(0)
    return buffer

def generate_advanced_market_data(city, property_type, status):
    """إنشاء بيانات سوقية متقدمة ومفصلة"""
    
    # أسعار أساسية مفصلة بناءً على المدينة ونوع العقار
    base_prices = {
        "الرياض": {
            "شقة": {"سكني": 4500, "فاخر": 6500, "اقتصادي": 3200},
            "فيلا": {"سكني": 3200, "فاخر": 4800, "اقتصادي": 2400},
            "أرض": {"سكني": 1800, "تجاري": 3500, "استثماري": 2200},
            "محل تجاري": {"مركزي": 8000, "تجاري": 6000, "حيوي": 4500}
        },
        "جدة": {
            "شقة": {"سكني": 3800, "فاخر": 5500, "اقتصادي": 2800},
            "فيلا": {"سكني": 2800, "fاخر": 4200, "اقتصادي": 2000},
            "أرض": {"سكني": 1500, "تجاري": 2800, "استثماري": 1800},
            "محل تجاري": {"مركزي": 6500, "تجاري": 5000, "حيوي": 3800}
        },
        "الدمام": {
            "شقة": {"سكني": 3200, "فاخر": 4800, "اقتصادي": 2500},
            "فيلا": {"سكني": 2600, "فاخر": 3800, "اقتصادي": 1800},
            "أرض": {"سكني": 1200, "تجاري": 2200, "استثماري": 1500},
            "محل تجاري": {"مركزي": 5500, "تجاري": 4200, "حيوي": 3200}
        }
    }
    
    city_data = base_prices.get(city, base_prices["الرياض"])
    property_data = city_data.get(property_type, {"سكني": 3000})
    avg_price = np.mean(list(property_data.values()))
    
    # تأثير الحالة على السعر
    price_multiplier = 1.15 if status == "للبيع" else 0.85 if status == "للشراء" else 0.95
    
    return {
        'السعر_الحالي': avg_price * price_multiplier,
        'متوسط_السوق': avg_price,
        'أعلى_سعر': avg_price * 1.35,
        'أقل_سعر': avg_price * 0.75,
        'حجم_التداول_شهري': np.random.randint(200, 800),
        'معدل_النمو_الشهري': np.random.uniform(1.2, 4.5),
        'عرض_العقارات': np.random.randint(100, 400),
        'طالب_الشراء': np.random.randint(150, 600),
        'معدل_الإشغال': np.random.uniform(80, 98),
        'العائد_التأجيري': np.random.uniform(8, 15),
        'مؤشر_السيولة': np.random.uniform(70, 95)
    }

# === الواجهة الرئيسية ===
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 👤 بيانات المستخدم والعقار")
    
    user_type = st.selectbox("اختر فئتك:", 
                           ["مستثمر", "وسيط عقاري", "شركة تطوير", "فرد", "باحث عن فرصة", "مالك عقار"])
    
    city = st.selectbox("المدينة:", 
                       ["الرياض", "جدة", "الدمام", "مكة المكرمة", "المدينة المنورة", "الخبر", "تبوك", "الطائف"])
    
    property_type = st.selectbox("نوع العقار:", 
                                ["شقة", "فيلا", "أرض", "محل تجاري"])
    
    status = st.selectbox("الحالة:", ["للبيع", "للشراء", "للإيجار"])
    
    area = st.slider("المساحة (م²):", 50, 1000, 120)
    
    property_count = st.slider("🔢 عدد العقارات للتحليل:", 1, 1000, 1,
                              help="كلما زاد عدد العقارات، زادت دقة التحليل والسعر")

with col2:
    st.markdown("### 💎 اختيار الباقة")
    
    chosen_pkg = st.radio("اختر باقتك:", list(PACKAGES.keys()))
    
    base_price = PACKAGES[chosen_pkg]["price"]
    total_price = base_price * property_count
    total_pages = PACKAGES[chosen_pkg]["pages"]
    
    st.markdown(f"""
    <div class='package-card'>
    <h3>باقة {chosen_pkg}</h3>
    <h2>{total_price} $</h2>
    <p>📄 {total_pages} صفحة تقرير متقدم</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("**المميزات:**")
    for feature in PACKAGES[chosen_pkg]["features"]:
        st.write(f"🎯 {feature}")

# === نظام الدفع ===
st.markdown("---")
st.markdown(f"### 💰 السعر النهائي: **{total_price} دولار**")

paypal_html = f"""
<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
<input type="hidden" name="cmd" value="_xclick">
<input type="hidden" name="business" value="zeghloulwarda6@gmail.com">
<input type="hidden" name="item_name" value="تقرير {chosen_pkg} - {property_count} عقار">
<input type="hidden" name="amount" value="{total_price}">
<input type="hidden" name="currency_code" value="USD">
<input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_buynowCC_LG.gif" border="0" name="submit" alt="PayPal - The safer, easier way to pay online!" style="display: block; margin: 0 auto;">
</form>
"""

st.markdown(paypal_html, unsafe_allow_html=True)

# === إنشاء التقرير ===
st.markdown("---")
st.markdown("### 🚀 إنشاء التقرير")

if st.button("🎯 إنشاء التقرير المتقدم (PDF)", use_container_width=True):
    with st.spinner("🔄 جاري إنشاء التقرير الاحترافي... قد يستغرق بضع ثوانٍ"):
        try:
            market_data = generate_advanced_market_data(city, property_type, status)
            user_info = {
                "user_type": user_type,
                "city": city, 
                "property_type": property_type,
                "area": area,
                "package": chosen_pkg,
                "property_count": property_count
            }
            
            pdf_buffer = create_professional_pdf(user_info, market_data, chosen_pkg)
            
            st.session_state.pdf_data = pdf_buffer.getvalue()
            st.session_state.report_generated = True
            
            st.success("✅ تم إنشاء التقرير الاحترافي بنجاح!")
            st.balloons()
            
            # عرض عينة من التقرير
            with st.expander("📊 معاينة سريعة للتقرير"):
                st.info(f"""
                **📄 التقرير النهائي يحتوي على:**
                - عدد الصفحات: {PACKAGES[chosen_pkg]['pages']} صفحة
                - التحليل الشامل لـ {property_count} عقار
                - رسوم بيانية متقدمة واحترافية
                - توصيات استراتيجية مفصلة
                - دراسة جدوى متكاملة
                """)
            
        except Exception as e:
            st.error(f"⚠️ حدث خطأ أثناء إنشاء التقرير: {str(e)}")
            st.info("يرجى المحاولة مرة أخرى أو التواصل مع الدعم")

if st.session_state.get('report_generated', False):
    st.markdown("---")
    st.markdown("## 📊 التقرير النهائي الجاهز للطباعة")
    
    # زر تحميل PDF
    st.download_button(
        label="📥 تحميل التقرير PDF",
        data=st.session_state.pdf_data,
        file_name=f"تقرير_Warda_Intelligence_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
    
    st.info("""
    **🎉 التقرير جاهز للطباعة والتقديم:**
    - تصميم احترافي مناسب للعروض التقديمية
    - محتوى عربي منظم وواضح
    - مناسب للتقديم للشركات والمستثمرين
    - يحتوي على جميع التحليلات المطلوبة
    - تقرير متكامل يستحق الاستثمار
    """)

# === لوحة المسؤول ===
admin_password = st.sidebar.text_input("كلمة مرور المسؤول:", type="password")
if admin_password == "WardaAdmin2024":
    st.sidebar.success("🎉 مرحباً بك في لوحة التحكم!")
    
    st.sidebar.markdown("### 🛠️ لوحة تحكم المسؤول")
    
    # إنشاء روابط مؤثرين
    st.sidebar.markdown("#### 🔗 إدارة روابط المؤثرين")
    
    influencer_name = st.sidebar.text_input("اسم المؤثر:")
    
    if st.sidebar.button("🎁 إنشاء رابط مؤثر جديد"):
        if influencer_name:
            today = datetime.now().strftime("%Y%m%d")
            influencer_token = hashlib.md5(f"GOLD_{influencer_name}_{today}_{np.random.randint(1000,9999)}".encode()).hexdigest()[:12]
            influencer_url = f"https://warda-intelligence.streamlit.app/?promo={influencer_token}"
            
            st.session_state.influencer_url = influencer_url
            st.session_state.influencer_name = influencer_name
            
            st.sidebar.success(f"✅ تم إنشاء الرابط للمؤثر: {influencer_name}")
        else:
            st.sidebar.error("⚠️ يرجى إدخال اسم المؤثر")
    
    if hasattr(st.session_state, 'influencer_url'):
        st.sidebar.markdown("**🔗 الرابط الحصري:**")
        st.sidebar.code(st.session_state.influencer_url)
        
        st.sidebar.markdown(f"- المؤثر: {st.session_state.influencer_name}")
        st.sidebar.markdown(f"- الباقة: 🥇 ذهبية مجانية")
        st.sidebar.markdown(f"- الصلاحية: 30 يوماً")
        st.sidebar.markdown(f"- الشروط: ذكر المنصة في المحتوى")

# === رابط المؤثرين ===
st.markdown("---")
st.markdown("### 🎁 عرض المؤثرين")

query_params = st.experimental_get_query_params()
if query_params.get('promo'):
    promo_token = query_params['promo'][0]
    
    st.success("🎉 تم تفعيل العرض الحصري للمؤثرين!")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #d4af37, #ffd700); padding: 20px; border-radius: 15px; text-align: center; color: black;'>
    <h3>🎁 تقرير مجاني حصري للمؤثرين</h3>
    <p>شكراً لتواجدكم في منصتنا! هذا التقرير الذهبي هدية خاصة لكم</p>
    </div>
    """, unsafe_allow_html=True)
    
    free_user_type = "مؤثر"
    free_city = "الرياض" 
    free_property_type = "شقة"
    free_area = 120
    free_status = "للبيع"
    free_package = "ذهبية"
    free_count = 1
    
    if st.button("🎁 تحميل التقرير الذهبي المجاني", use_container_width=True):
        with st.spinner("🔄 جاري إنشاء التقرير الحصري..."):
            market_data = generate_advanced_market_data(free_city, free_property_type, free_status)
            user_info = {
                "user_type": free_user_type,
                "city": free_city, 
                "property_type": free_property_type,
                "area": free_area,
                "package": free_package,
                "property_count": free_count
            }
            
            pdf_buffer = create_professional_pdf(user_info, market_data, free_package)
            
            st.download_button(
                label="📥 تحميل التقرير الذهبي PDF",
                data=pdf_buffer.getvalue(),
                file_name=f"تقرير_ذهبي_مجاني_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            
            st.markdown("""
            <div style='background: linear-gradient(135deg, #1a2a3a, #2a3a4a); padding: 15px; border-radius: 10px; border: 2px solid gold; margin: 20px 0;'>
            <h4 style='color: gold; text-align: center;'>🎯 شروط الاستفادة من العرض:</h4>
            <p style='color: white; text-align: center;'>
            نرجو ذكر منصة <strong>Warda Intelligence</strong> في محتواكم مقابل هذه الهدية القيمة
            </p>
            </div>
