mport streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import hashlib
import time

# إعداد الصفحة
st.set_page_config(page_title="التحليل العقاري الذهبي | Warda Intelligence", layout="wide")

# تنسيق واجهة فاخرة
st.markdown("""
    <style>
    .main { background-color: #0E1117; color: gold; }
    .stApp { background-color: #0E1117; }
    h1, h2, h3, h4, h5, h6 { color: gold !important; }
    .stSelectbox label, .stSlider label, .stRadio label { color: gold !important; }
    .stButton>button {
        background-color: gold; color: black; font-weight: bold;
        border-radius: 10px; padding: 0.6em 1.2em; border: none;
        width: 100%;
    }
    .analysis-card {
        background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
        padding: 20px; border-radius: 15px; border: 1px solid gold;
        margin: 10px 0; color: white;
    }
    .price-up { color: #00ff00; font-weight: bold; }
    .price-down { color: #ff4444; font-weight: bold; }
    .package-card {
        background: linear-gradient(135deg, #2d2d2d, #1a1a1a);
        padding: 15px; border-radius: 10px; border: 2px solid #d4af37;
        margin: 10px 0; text-align: center;
    }
    .admin-panel {
        background: linear-gradient(135deg, #1a2a3a, #2a3a4a);
        padding: 20px; border-radius: 15px; border: 2px solid #00ff00;
        margin: 10px 0;
    }
    .report-section {
        background: linear-gradient(135deg, #1e1e1e, #2a2a2a);
        padding: 25px; border-radius: 15px; border-left: 5px solid gold;
        margin: 15px 0; color: white;
    }
    .metric-card {
        background: linear-gradient(135deg, #2a2a2a, #3a3a3a);
        padding: 15px; border-radius: 10px; border: 1px solid #d4af37;
        margin: 10px; text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown("<h1 style='text-align: center; color: gold;'>🏙️ منصة التحليل العقاري الذهبي - Warda Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #d4af37;'>تحليل ذكي مخصص لكل فئة - قرارات استثمارية مدروسة</p>", unsafe_allow_html=True)

# === نظام الباقات والأسعار ===
PACKAGES = {
    "مجانية": {
        "price": 0,
        "features": [
            "تحليل سوق أساسي",
            "أسعار متوسطة للمنطقة", 
            "تقرير نصي بسيط",
            "صالح لعقار واحد"
        ]
    },
    "فضية": {
        "price": 29,
        "features": [
            "كل مميزات المجانية +",
            "تحليل تنبؤي 6 أشهر",
            "مقارنة مع 5 مشاريع مشابهة",
            "نصائح استثمارية متقدمة",
            "تقرير PDF تفاعلي",
            "رسوم بيانية متحركة",
            "تحليل المنافسين",
            "دراسة الجدوى المبدئية"
        ]
    },
    "ذهبية": {
        "price": 79,
        "features": [
            "كل مميزات الفضية +", 
            "تحليل ذكاء اصطناعي متقدم",
            "تنبؤات لمدة سنة كاملة",
            "دراسة الجدوى الاقتصادية الشاملة",
            "تحليل 10 منافسين رئيسيين",
            "نصائح مخصصة حسب الفئة",
            "مؤشرات أداء مفصلة",
            "تحليل المخاطر المتقدم"
        ]
    },
    "ماسية": {
        "price": 149,
        "features": [
            "كل مميزات الذهبية +",
            "تحليل شمولي متكامل", 
            "تقارير مقارنة مع كل المدن",
            "تحليل المخاطرة المتقدم",
            "خطة استثمارية تفصيلية",
            "محاكاة سيناريوهات متعددة",
            "تحليل توقيت السوق",
            "توصيات استراتيجية شاملة"
        ]
    }
}

# === بيانات سوقية متقدمة ===
def generate_advanced_market_data(city, property_type, status):
    """إنشاء بيانات سوقية متقدمة ومفصلة"""
    
    # أسعار أساسية مفصلة
    base_prices = {
        "الرياض": {
            "شقة": {"سكني": 4500, "فاخر": 6500, "اقتصادي": 3200},
            "فيلا": {"سكني": 3200, "فاخر": 4800, "اقتصادي": 2400},
            "أرض": {"سكني": 1800, "تجاري": 3500, "استثماري": 2200},
            "محل تجاري": {"مركزي": 8000, "تجاري": 6000, "حيوي": 4500}
        },
        "جدة": {
            "شقة": {"سكني": 3800, "فاخر": 5500, "اقتصادي": 2800},
            "فيلا": {"سكني": 2800, "فاخر": 4200, "اقتصادي": 2000},
            "أرض": {"سكني": 1500, "تجاري": 2800, "استثماري": 1800},
            "محل تجاري": {"مركزي": 6500, "تجاري": 5000, "حيوي": 3800}
        }
    }
    
    city_data = base_prices.get(city, base_prices["الرياض"])
    property_data = city_data.get(property_type, {"سكني": 3000})
    avg_price = np.mean(list(property_data.values()))
    
    # تأثير الحالة على السعر
    price_multiplier = 1.12 if status == "للبيع" else 0.88 if status == "للشراء" else 0.95
    
    return {
        'السعر_الحالي': avg_price * price_multiplier,
        'متوسط_السوق': avg_price,
        'أعلى_سعر': avg_price * 1.35,
        'أقل_سعر': avg_price * 0.75,
        'حجم_التداول_شهري': np.random.randint(150, 600),
        'معدل_النمو_الشهري': np.random.uniform(0.8, 3.5),
        'عرض_العقارات': np.random.randint(80, 250),
        'طالب_الشراء': np.random.randint(120, 400),
        'معدل_الإشغال': np.random.uniform(75, 95),
        'العائد_التأجيري': np.random.uniform(6, 12),
        'مؤشر_السيولة': np.random.uniform(60, 90)
    }

# === تحليلات متقدمة لكل فئة ===
def get_advanced_analysis_by_user_type(user_type, city, property_type, area, status):
    """تحليل متقدم ومفصل حسب فئة المستخدم"""
    
    analyses = {
        "مستثمر": {
            "title": "📊 التحليل الاستثماري الشامل",
            "sections": {
                "التحليل_المالي": """
                ## 💰 التحليل المالي المتقدم
                
                ### 📈 مؤشرات الأداء الرئيسية (KPIs)
                | المؤشر | القيمة | التقييم |
                |---------|--------|----------|
                | العائد على الاستثمار (ROI) | 9.5% سنوياً | 🟢 ممتاز |
                | صافي القيمة الحالية (NPV) | +$45,000 | 🟢 إيجابي |
                | معدل العائد الداخلي (IRR) | 11.2% | 🟢 جيد |
                | فترة استرداد رأس المال | 8.2 سنة | 🟡 متوسطة |
                | نسبة الدين إلى الحقوق | 65% | 🟢 مقبولة |
                
                ### 💸 تحليل التدفقات النقدية
                **السنة الأولى:**
                - الإيرادات الشهرية المتوقعة: $2,800
                - المصروفات التشغيلية: $1,200  
                - صافي التدفق الشهري: $1,600
                - صافي التدفق السنوي: $19,200
                
                **توقعات 5 سنوات:**
                - إجمالي الإيرادات: $168,000
                - إجمالي المصروفات: $72,000
                - صافي الربح التراكمي: $96,000
                """,
                
                "استراتيجيات_الاستثمار": """
                ## 🎯 استراتيجيات الاستثمار المتقدمة
                
                ### 🏆 الاستراتيجية المثلى: الشراء والتأجير طويل الأجل
                
                **المزايا:**
                ✅ تدفقات نقدية شهرية ثابتة
                ✅ ارتفاع القيمة السوقية مع الوقت  
                ✅ حماية من التضخم
                ✅ إعفاءات ضريبية محتملة
                
                **خطة التنفيذ:**
                1. **الشهر 1-3:** البحث والتفاوض على 3-5 عقارات
                2. **الشهر 4-6:** التمويل والتجهيزات
                3. **الشهر 7-9:** التأجير وإدارة الممتلكات
                4. **الشهر 10-12:** التقييم والتعديل
                
                ### 📊 محفظة الاستثمار المقترحة
                | نوع العقار | النسبة | المبلغ | العائد المتوقع |
                |-------------|---------|---------|-----------------|
                | شقق سكنية | 40% | $200,000 | 8-10% |
                | محلات تجارية | 30% | $150,000 | 10-12% |
                | فيلات | 20% | $100,000 | 7-9% |
                | أراضي | 10% | $50,000 | 12-15% |
                """,
                
                "إدارة_المخاطر": """
                ## 🛡️ إدارة المخاطر المتقدمة
                
                ### ⚠️ تحليل المخاطر الرئيسية
                
                **مخاطر السوق (30%)**
                - تقلبات أسعار العقارات
                - تغير ظروف الاقتصاد الكلي
                - منافسة جديدة في المنطقة
                
                **مخاطر التشغيل (25%)**  
                - صعوبة في إيجاد مستأجرين
                - تكاليف صيانة غير متوقعة
                - مشاكل قانونية وإدارية
                
                **مخاطر التمويل (20%)**
                - ارتفاع أسعار الفائدة
                - صعوبة إعادة التمويل
                - تغير شروط القروض
                
                ### 🛡️ استراتيجيات التخفيف
                1. **التنويع الجغرافي:** الاستثمار في 3 مناطق مختلفة
                2. **تحوط سعري:** عقود خيارات للبيع
                3. **احتياطي نقدي:** 6 أشهر من المصروفات
                4. **تأمين شامل:** ضد جميع المخاطر
                """,
                
                "الفرص_المستقبلية": """
                ## 🚀 الفرص الاستثمارية المستقبلية
                
                ### 🎯 المناطق الواعدة في الرياض
                
                **🔝 المنطقة الشمالية (مشروع القدية)**
                - معدل نمو متوقع: 15% سنوياً
                - مشاريع تطوير كبرى قيد الإنشاء
                - طلب متزايد على الوحدات السكنية
                
                **🏙️ المنطقة المركزية (المربع)**
                - أسعار مستقرة ومضمونة
                - طلب دائم من الموظفين الحكوميين
                - إشغال مرتفع على مدار السنة
                
                **📈 توقعات الذكاء الاصطناعي**
                - نمو السوق العقاري: 7.8% خلال 2024
                - ارتفاع أسعار المواد: 4.2% 
                - زيادة الطلب السكني: 12.5%
                """
            }
        }
    }
    
    return analyses.get(user_type, analyses["مستثمر"])

# === توليد تقرير متقدم مع صفحات متعددة ===
def generate_advanced_report(user_type, city, property_type, area, status, package, property_count):
    """توليد تقرير متقدم مع صفحات وجداول ومؤشرات مبهرة"""
    
    # حساب السعر
    base_price = PACKAGES[package]["price"]
    total_price = base_price * property_count
    
    # بيانات السوق المتقدمة
    market_data = generate_advanced_market_data(city, property_type, status)
    
    # التحليل المتقدم
    advanced_analysis = get_advanced_analysis_by_user_type(user_type, city, property_type, area, status)
    
    # إنشاء التقرير المتعدد الصفحات
    report_content = []
    
    # الصفحة 1: الغلاف والمقدمة
    cover_page = f"""
    🏙️ تقرير Warda Intelligence المتقدم
    {'=' * 60}
    
    📊 **التقرير الاستثماري الشامل**
    🎯 مخصص لفئة: {user_type}
    🏙️ المنطقة: {city}
    🏠 نوع العقار: {property_type}
    
    📅 تاريخ الإصدار: {datetime.now().strftime('%Y-%m-%d')}
    ⏰ وقت الإنشاء: {datetime.now().strftime('%H:%M')}
    🔢 رقم التقرير: WR-{datetime.now().strftime('%Y%m%d%H%M')}
    
    💼 **معلومات العميل:**
    ┌─ 🏷️ الفئة: {user_type}
    ├─ 🏙️ المدينة: {city} 
    ├─ 🏠 نوع العقار: {property_type}
    ├─ 📏 المساحة: {area} م²
    ├─ 📌 الحالة: {status}
    ├─ 🔢 عدد العقارات: {property_count}
    ├─ 💎 الباقة: {package}
    └─ 💰 القيمة: {total_price} دولار
    
    📈 **ملخص الأداء:**
    ├─ 📊 تصنيف الاستثمار: {'🟢 ممتاز' if market_data['العائد_التأجيري'] > 8 else '🟡 جيد'}
    ├─ 💸 العائد المتوقع: {market_data['العائد_التأجيري']:.1f}% سنوياً
    ├─ 📈 نمو رأس المال: {market_data['معدل_النمو_الشهري']*12:.1f}% سنوياً
    ├─ 🛡️ مستوى المخاطرة: {np.random.randint(15, 35)}%
    └─ ⭐ التوصية: {'🟢 شراء مستعجل' if market_data['معدل_النمو_الشهري'] > 2 else '🟡 شراء مدروس'}
    
    {'=' * 60}
    """
    report_content.append(cover_page)
    
    # الصفحة 2: التحليل المالي
    financial_page = f"""
    📑 الصفحة 2: التحليل المالي المتقدم
    {'=' * 60}
    
    {advanced_analysis['sections']['التحليل_المالي']}
    
    💹 **مؤشرات السوق المالية:**
    
    📊 **مقارنة الأداء مع المؤشرات القياسية:**
    | المؤشر | أداؤك | متوسط السوق | التصنيف |
    |---------|--------|-------------|----------|
    | العائد على الاستثمار | {market_data['العائد_التأجيري']:.1f}% | 7.2% | 🟢 +{market_data['العائد_التأجيري']-7.2:.1f}% |
    | معدل النمو | {market_data['معدل_النمو_الشهري']*12:.1f}% | 6.5% | 🟢 +{(market_data['معدل_النمو_الشهري']*12)-6.5:.1f}% |
    | السيولة | {market_data['مؤشر_السيولة']:.0f}% | 70% | 🟢 +{market_data['مؤشر_السيولة']-70:.0f}% |
    | الإشغال | {market_data['معدل_الإشغال']:.1f}% | 82% | 🟢 +{market_data['معدل_الإشغال']-82:.1f}% |
    
    💰 **تحليل القيمة السوقية:**
    ├─ 💵 القيمة الحالية: {market_data['السعر_الحالي'] * area:,.0f} ريال
    ├─ 📈 القيمة بعد سنة: {market_data['السعر_الحالي'] * area * 1.08:,.0f} ريال
    ├─ 🎯 القيمة بعد 3 سنوات: {market_data['السعر_الحالي'] * area * 1.25:,.0f} ريال
    └─ 🚀 القيمة بعد 5 سنوات: {market_data['السعر_الحالي'] * area * 1.45:,.0f} ريال
    
    {'=' * 60}
    """
    report_content.append(financial_page)
    
    # الصفحة 3: استراتيجيات الاستثمار
    strategy_page = f"""
    📑 الصفحة 3: استراتيجيات الاستثمار المتقدمة  
    {'=' * 60}
    
    {advanced_analysis['sections']['استراتيجيات_الاستثمار']}
    
    🎲 **سيناريوهات الاستثمار:**
    
    **📈 السيناريو المتفائل (+15%):**
    ├─ نمو السوق: 12% سنوياً
    ├─ العوائد: 11-14% 
    ├─ السيولة: عالية جداً
    └─ التوصية: زيادة الاستثمار 20%
    
    **⚖️ السيناريو المتوسط (+8%):**
    ├─ نمو السوق: 7% سنوياً
    ├─ العوائد: 8-10%
    ├─ السيولة: متوسطة
    └─ التوصية: الحفاظ على المستوى الحالي
    
    **📉 السيناريو المتحفظ (+3%):**
    ├─ نمو السوق: 2% سنوياً  
    ├─ العوائد: 5-7%
    ├─ السيولة: منخفضة
    └─ التوصية: تقليل التعرض 15%
    
    {'=' * 60}
    """
    report_content.append(strategy_page)
    
    # الصفحة 4: إدارة المخاطر
    risk_page = f"""
    📑 الصفحة 4: إدارة المخاطر المتقدمة
    {'=' * 60}
    
    {advanced_analysis['sections']['إدارة_المخاطر']}
    
    🎯 **مصفوفة المخاطر والعائد:**
    
    **🟢 منطقة الخضراء (مخاطرة منخفضة - عائد متوسط)**
    ├─ العقارات السكنية في الأحياء الراقية
    ├─ المحلات التجارية في المراكز الرئيسية
    ├─ متوسط العائد: 6-8% سنوياً
    └─ التوصية: 60% من المحفظة
    
    **🟡 منطقة الصفراء (مخاطرة متوسطة - عائد جيد)**
    ├─ الأراضي في مناطق التطوير
    ├─ المشاريع تحت الإنشاء
    ├─ متوسط العائد: 8-12% سنوياً  
    └─ التوصية: 30% من المحفظة
    
    **🔴 منطقة الحمراء (مخاطرة عالية - عائد مرتفع)**
    ├─ العقارات المتخصصة
    ├─ المناطق النامية حديثاً
    ├─ متوسط العائد: 12-18% سنوياً
    └─ التوصية: 10% من المحفظة
    
    {'=' * 60}
    """
    report_content.append(risk_page)
    
    # الصفحة 5: الفرص المستقبلية
    opportunities_page = f"""
    📑 الصفحة 5: الفرص الاستثمارية المستقبلية
    {'=' * 60}
    
    {advanced_analysis['sections']['الفرص_المستقبلية']}
    
    🏆 **أفضل 5 فرص استثمارية في {city}:**
    
    **🥇 الفرصة الأولى: مشروع نيوم (المنطقة الشمالية)**
    ├─ 📈 معدل النمو المتوقع: 18% سنوياً
    ├─ 💰 حجم الاستثمارات: $500 مليار
    ├─ 🎯 التوقيت: 2024-2026
    ├─ ⚠️ المخاطرة: متوسطة
    └─ 💡 التوصية: الاستثمار المبكر
    
    **🥈 الفرصة الثانية: الدرعية التاريخية**
    ├─ 📈 معدل النمو المتوقع: 14% سنوياً  
    ├─ 💰 حجم الاستثمارات: $50 مليار
    ├─ 🎯 التوقيت: 2024-2025
    ├─ ⚠️ المخاطرة: منخفضة
    └─ 💡 التوصية: الاستثمار المتوسط
    
    **🥉 الفرصة الثالثة: القطاع المالي (المركز المالي)**
    ├─ 📈 معدل النمو المتوقع: 12% سنوياً
    ├─ 💰 حجم الاستثمارات: $30 مليار
    ├─ 🎯 التوقيت: 2024-2027
    ├─ ⚠️ المخاطرة: منخفضة
    └─ 💡 التوصية: الاستثمار الآمن
    
    **📊 الفرصة الرابعة: القطاع التعليمي (مدينة الجامعات)**
    ├─ 📈 معدل النمو المتوقع: 10% سنوياً
    ├─ 💰 حجم الاستثمارات: $20 مليار
    ├─ 🎯 التوقيت: 2024-2028
    ├─ ⚠️ المخاطرة: منخفضة جداً
    └─ 💡 التوصية: الاستثمار طويل الأجل
    
    **🏘️ الفرصة الخامسة: الإسكان الاقتصادي**
    ├─ 📈 معدل النمو المتوقع: 9% سنوياً
    ├─ 💰 حجم الاستثمارات: $40 مليار
    ├─ 🎯 التوقيت: 2024-2026
    ├─ ⚠️ المخاطرة: منخفضة
    └─ 💡 التوصية: الاستثمار الجماعي
    
    {'=' * 60}
    """
    report_content.append(opportunities_page)
    
    return "\n\n".join(report_content), total_price

# === الواجهة الرئيسية ===
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 👤 بيانات المستخدم")
    
    user_type = st.selectbox("اختر فئتك:", 
                           ["مستثمر", "وسيط عقاري", "شركة تطوير", "فرد", "باحث عن فرصة", "مالك عقار"])
    
    city = st.selectbox("المدينة:", 
                       ["الرياض", "جدة", "الدمام", "مكة المكرمة", "المدينة المنورة", "الخبر", "تبوك", "الطائف"])
    
    property_type = st.selectbox("نوع العقار:", 
                                ["شقة", "فيلا", "أرض", "محل تجاري"])
    
    status = st.selectbox("الحالة:", ["للبيع", "للشراء", "للإيجار"])
    
    area = st.slider("المساحة (م²):", 50, 1000, 120)

with col2:
    st.markdown("### 💎 اختيار الباقة")
    
    # عدد العقارات مع تحديث السعر تلقائياً
    property_count = st.slider("🔢 عدد العقارات للتحليل:", 1, 50, 1,
                              help="كلما زاد عدد العقارات، زادت دقة التحليل والسعر")
    
    # عرض الباقات
    chosen_pkg = st.radio("اختر باقتك:", list(PACKAGES.keys()))
    
    # حساب السعر الديناميكي
    base_price = PACKAGES[chosen_pkg]["price"]
    total_price = base_price * property_count
    
    # عرض تفاصيل الباقة
    st.markdown(f"""
    <div class='package-card'>
    <h3>باقة {chosen_pkg}</h3>
    <h4>{total_price} دولار</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # عرض المميزات
    st.markdown("**المميزات:**")
    for feature in PACKAGES[chosen_pkg]["features"]:
        st.write(f"✅ {feature}")

# === نظام الدفع ===
st.markdown("---")
st.markdown(f"### 💰 السعر النهائي: **{total_price} دولار**")

# زر الدفع باي بال
paypal_html = f"""
<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
<input type="hidden" name="cmd" value="_xclick">
<input type="hidden" name="business" value="warda.intelligence@gmail.com">
<input type="hidden" name="item_name" value="تقرير {chosen_pkg} - {property_count} عقار">
<input type="hidden" name="amount" value="{total_price}">
<input type="hidden" name="currency_code" value="USD">
<input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_buynowCC_LG.gif" border="0" name="submit" alt="PayPal - The safer, easier way to pay online!" style="display: block; margin: 0 auto;">
</form>
"""

st.markdown(paypal_html, unsafe_allow_html=True)

# === زر واحد لإنشاء التقرير ===
st.markdown("---")
st.markdown("### 🚀 إنشاء التقرير")

col1, col2 = st.columns(2)

with col1:
    # زر للمسؤول (بدون دفع)
    if st.button("🎯 إنشاء التقرير (للمسؤول)", use_container_width=True):
        with st.spinner("🔄 جاري إنشاء التقرير المتقدم..."):
            time.sleep(3)
            
            # إنشاء التقرير المتقدم
            report, final_price = generate_advanced_report(
                user_type, city, property_type, area, status, chosen_pkg, property_count
            )
            
            # حفظ التقرير في الجلسة
            st.session_state.current_report = report
            st.session_state.report_generated = True
            st.success("✅ تم إنشاء التقرير المتقدم!")

with col2:
    # زر للعميل (بعد الدفع)
    if st.button("📥 تحميل التقرير (بعد الدفع)", use_container_width=True):
        if hasattr(st.session_state, 'current_report'):
            st.success("✅ تم تحميل التقرير")
        else:
            st.warning("⚠️ يرجى إتمام عملية الدفع أولاً")

# === عرض التقرير وزر التحميل ===
if st.session_state.get('report_generated', False):
    st.markdown("---")
    st.markdown("## 📊 التقرير النهائي المتقدم")
    
    # عرض التقرير
    st.text_area("محتوى التقرير:", st.session_state.current_report, height=600)
    
    # زر تحميل التقرير
    st.download_button(
        label="📥 تحميل التقرير الكامل (PDF)",
        data=st.session_state.current_report,
        file_name=f"تقرير_متقدم_{user_type}_{city}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    st.success("🎉 تم إنشاء التقرير المتقدم بنجاح! يحتوي على 5 صفحات من التحليل الشامل")
    st.balloons()

# === لوحة المسؤول ===
admin_password = st.sidebar.text_input("كلمة مرور المسؤول:", type="password")
if admin_password == "WardaAdmin2024":
    st.sidebar.success("🎉 مرحباً بك في لوحة التحكم!")
    
    # لوحة تحكم المسؤول
    st.sidebar.markdown("### 🛠️ لوحة تحكم المسؤول")
    
    if st.sidebar.button("🔗 إنشاء رابط مؤثرين جديد"):
        today = datetime.now().strftime("%Y%m%d")
        influencer_token = hashlib.md5(f"FREE1_{today}_{np.random.randint(1000,9999)}".encode()).hexdigest()[:10]
        st.session_state.influencer_url = f"https://warda-intelligence.streamlit.app/?promo={influencer_token}"
        st.sidebar.success("✅ تم إنشاء الرابط الجديد")
    
    if hasattr(st.session_state, 'influencer_url'):
        st.sidebar.markdown(f"**رابط المؤثرين:**")
        st.sidebar.code(st.session_state.influencer_url)

# === رابط المؤثرين (للزوار العاديين) ===
st.markdown("---")
st.markdown("### 🎁 عرض المؤثرين")

# التحقق من رابط المؤثرين
query_params = st.experimental_get_query_params()
if query_params.get('promo'):
    promo_token = query_params['promo'][0]
    st.success("🎉 تم تفعيل العرض المجاني للمؤثرين!")
    
    # استخدام بيانات افتراضية للتقرير المجاني
    free_user_type = "مؤثر"
    free_city = "الرياض" 
    free_property_type = "شقة"
    free_area = 120
    free_status = "للبيع"
    free_package = "ذهبية"
    free_count = 1
    
    if st.button("🎁 الحصول على التقرير المجاني", use_container_width=True):
        report, _ = generate_advanced_report(
            free_user_type, free_city, free_property_type, free_area, free_status, free_package, free_count
        )
        
        st.download_button(
            label="📥 تحميل التقرير المجاني",
            data=report,
            file_name=f"تقرير_مجاني_لمؤثر_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )
else:
    st.info("""
    **للمؤثرين:** 
    للحصول على تقرير مجاني، يرجى استخدام الرابط الخاص الذي تم توفيره من إدارة المنصة.
    """)

# === معلومات الاتصال ===
st.markdown("---")
st.markdown("### 📞 للتواصل مع Warda Intelligence")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **💬 واتساب:**
    +213779888140
    
    **📧 البريد:**
    info@warda-intelligence.com
    """)

with col2:
    st.markdown("""
    **🌐 الموقع:**
    www.warda-intelligence.com
    
    **🕒 ساعات العمل:**
    9:00 ص - 6:00 م
    """)
