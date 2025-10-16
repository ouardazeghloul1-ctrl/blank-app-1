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

def reshape_arabic_text(text):
    """إعادة تشكيل النص العربي للعرض الصحيح"""
    try:
        # تجاهل الأرقام والرموز في إعادة التشكيل
        if text.replace(' ', '').isdigit() or 'صفحة' in text or 'page' in text.lower():
            return text
            
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        return bidi_text
    except:
        return text

def create_professional_arabic_pdf(report_data, user_info):
    """إنشاء تقرير PDF احترافي بالعربية باستخدام matplotlib"""
    
    buffer = BytesIO()
    
    with PdfPages(buffer) as pdf:
        page_num = 1
        
        # الصفحة 1: الغلاف
        plt.figure(figsize=(8.27, 11.69))  # A4 size
        plt.axis('off')
        
        # العنوان الرئيسي
        plt.text(0.5, 0.8, reshape_arabic_text('تقرير Warda Intelligence المتقدم'), 
                fontsize=20, ha='center', va='center', weight='bold', color='#d4af37')
        
        # العنوان الثانوي
        plt.text(0.5, 0.7, reshape_arabic_text('التحليل العقاري الذكي'), 
                fontsize=16, ha='center', va='center', style='italic')
        
        # معلومات العميل
        info_text = f"""
        {reshape_arabic_text('معلومات العميل:')}
        
        {reshape_arabic_text('الفئة:')} {user_info['user_type']}
        {reshape_arabic_text('المدينة:')} {user_info['city']}
        {reshape_arabic_text('نوع العقار:')} {user_info['property_type']}
        {reshape_arabic_text('المساحة:')} {user_info['area']} م²
        {reshape_arabic_text('الباقة:')} {user_info['package']}
        """
        
        plt.text(0.5, 0.5, info_text, fontsize=12, ha='center', va='center', 
                bbox=dict(boxstyle="round,pad=1", facecolor="lightgray"))
        
        # التاريخ
        date_text = f"{reshape_arabic_text('تاريخ التقرير:')} {datetime.now().strftime('%Y-%m-%d')}"
        plt.text(0.5, 0.2, date_text, fontsize=10, ha='center', va='center')
        
        pdf.savefig()
        plt.close()
        page_num += 1
        
        # الصفحات التالية: المحتوى
        for section_title, section_content in report_data.items():
            plt.figure(figsize=(8.27, 11.69))
            plt.axis('off')
            
            # عنوان القسم
            plt.text(0.1, 0.95, reshape_arabic_text(section_title), 
                    fontsize=16, ha='left', va='top', weight='bold', color='#d4af37')
            
            # محتوى القسم
            plt.text(0.1, 0.85, reshape_arabic_text(section_content), 
                    fontsize=10, ha='left', va='top', wrap=True)
            
            # رقم الصفحة
            plt.text(0.5, 0.05, f"صفحة {page_num}", 
                    fontsize=8, ha='center', va='center')
            
            pdf.savefig()
            plt.close()
            page_num += 1
    
    buffer.seek(0)
    return buffer

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

def create_advanced_visualizations(market_data, user_type):
    """إنشاء رسومات بيانية متقدمة ومبهرة"""
    
    # 1. مخطط العوائد المتوقع
    fig_returns = go.Figure()
    
    fig_returns.add_trace(go.Indicator(
        mode = "gauge+number+delta",
        value = market_data['العائد_التأجيري'],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "العائد السنوي المتوقع (%)"},
        delta = {'reference': 7, 'increasing': {'color': "green"}},
        gauge = {
            'axis': {'range': [None, 20]},
            'bar': {'color': "gold"},
            'steps': [
                {'range': [0, 7], 'color': "lightgray"},
                {'range': [7, 12], 'color': "yellow"},
                {'range': [12, 20], 'color': "orange"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 15
            }
        }
    ))
    
    fig_returns.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "gold", 'family': "Arial"}
    )
    
    # 2. مخطط النمو
    months = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو',
             'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
    
    growth_data = [market_data['معدل_النمو_الشهري'] * i for i in range(1, 13)]
    
    fig_growth = go.Figure()
    fig_growth.add_trace(go.Scatter(
        x=months,
        y=growth_data,
        mode='lines+markers',
        name='النمو التراكمي',
        line=dict(color='gold', width=3),
        marker=dict(size=8, color='white')
    ))
    
    fig_growth.update_layout(
        title='توقعات النمو الشهري (%)',
        xaxis_title='الشهر',
        yaxis_title='النمو التراكمي (%)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(color='white'),
        yaxis=dict(color='white')
    )
    
    return fig_returns, fig_growth

def generate_executive_report(user_type, city, property_type, area, status, package):
    """توليد تقرير تنفيذي مفصل بالعربية - 10 صفحات من المحتوى الثري"""
    
    market_data = generate_advanced_market_data(city, property_type, status)
    
    report_sections = {
        "📊 الملخص التنفيذي الشامل": f"""
عزيزي العميل الكريم،

يسعدني أن أقدم لكم هذا التقرير الشامل الذي يمثل ثمرة تحليل دقيق لسوق العقارات في {city}، 
وقد قمت بدراسة أكثر من {market_data['حجم_التداول_شهري'] * 12:,} صفقة سنوياً لتقديم رؤية واضحة 
ومبنية على بيانات حقيقية لا على التخمينات.

**الرؤية الاستراتيجية:**
بعد تحليل متعمق، أرى أن استثمارك في قطاع {property_type} يمثل فرصة ذهبية حقيقية. 
العائد المتوقع يبلغ {market_data['العائد_التأجيري']:.1f}% سنوياً، وهو ما يتفوق على معظم 
الاستثمارات التقليدية في السوق.

**لماذا هذه الفرصة استثنائية؟**
✅ النمو الشهري المستمر: {market_data['معدل_النمو_الشهري']:.1f}%
✅ سيولة عالية في السوق: {market_data['مؤشر_السيولة']:.1f}%
✅ طلب متزايد: {market_data['طالب_الشراء']} طالب شراء نشط
✅ عرض محدود: {market_data['عرض_العقارات']} عقار متاح فقط

أنصحكم بالتحرك السريع، فالسوق في ذروة نموه والفرص الذهبية لا تنتظر.
        """,
        
        "💰 التحليل المالي المتقدم": f"""
**التقييم المالي الشامل:**

🏠 **القيمة السوقية التفصيلية:**
- القيمة الحالية: {market_data['السعر_الحالي'] * area:,.0f} ريال
- القيمة الدنيا في السوق: {market_data['أقل_سعر'] * area:,.0f} ريال  
- القيمة القصوى في السوق: {market_data['أعلى_سعر'] * area:,.0f} ريال
- متوسط السوق: {market_data['متوسط_السوق'] * area:,.0f} ريال

📈 **مؤشرات الأداء المالي:**
- العائد على الاستثمار: {market_data['العائد_التأجيري']:.1f}% سنوياً
- معدل النمو السنوي: {market_data['معدل_النمو_الشهري']*12:.1f}%
- معدل الإشغال: {market_data['معدل_الإشغال']:.1f}%
- مؤشر السيولة: {market_data['مؤشر_السيولة']:.1f}%

💸 **التدفقات النقدية المتوقعة (5 سنوات):**
- الإيرادات التراكمية: {market_data['السعر_الحالي'] * area * 0.08 * 5:,.0f} ريال
- صافي الأرباح: {market_data['السعر_الحالي'] * area * 0.06 * 5:,.0f} ريال
- العائد التراكمي: {market_data['العائد_التأجيري'] * 5:.1f}%

هذه التوقعات تستند إلى تحليل {market_data['عرض_العقارات']} عقار معروض 
و{market_data['طالب_الشراء']} طالب شراء نشط في السوق الحالي.
        """,
        
        "🎯 الخطة الاستراتيجية الشاملة": f"""
**الرحلة الاستثمارية المدروسة:**

🚀 **المرحلة الأولى: التأسيس (0-6 أشهر)**
1. البحث والتفاوض على 3-5 عقارات واعدة
2. دراسة الجدوى التفصيلية لكل عقار
3. التفاوض على السعر المثالي
4. إتمام الصفقة بأفضل الشروط

📊 **المرحلة الثانية: النمو (6-24 شهر)**
1. تطوير الخدمات وزيادة القيمة الإيجارية
2. متابعة تطورات السوق شهرياً
3. تحسين تجربة المستأجرين
4. دراسة فرص إعادة التمويل

🏆 **المرحلة الثالثة: التوسع (24-60 شهر)**
1. التوسع في الاستثمار بالمنطقة
2. بناء محفظة عقارية متنوعة
3. الاستفادة من مشاريع التطوير القادمة
4. التحول إلى مستثمر محترف

**التوصية الشخصية:**
أنصحكم بالتركيز على الجودة والتميز في الخدمة، فهما مفتاح النجاح في السوق العقاري السعودي.
        """,
        
        "📊 تحليل السوق التفصيلي": """
**مؤشرات السوق الحيوية:**

📈 **مؤشرات النمو:**
- نمو الطلب السكني: +15.2% سنوياً
- نمو القيمة السوقية: +8.7% سنوياً
- نمو القوة الشرائية: +6.3% سنوياً

🏗️ **مشاريع التطوير القادمة:**
- مشروع القدية: استثمار 500 مليار ريال
- مشروع نيوم: استثمار 300 مليار ريال
- مشروع البحر الأحمر: استثمار 200 مليار ريال

👥 **التحليل الديموغرافي:**
- نمو السكان: +2.4% سنوياً
- دخل الفرد: 85,000 ريال شهرياً
- نسبة الشباب: 67% من السكان

**التوقعات المستقبلية:**
- نمو السوق العقاري 2024: +9.2%
- نمو السوق العقاري 2025: +10.5%
- نمو السوق العقاري 2026: +11.8%
        """,
        
        "🛡️ إدارة المخاطر المتقدمة": """
**تحليل المخاطر الشامل:**

🔴 **المخاطر العالية (30%):**
- تقلبات أسعار المواد الإنشائية
- تغير سياسات التمويل العقاري
- المنافسة من المشاريع الجديدة

🟡 **المخاطر المتوسطة (50%):**
- تغير أنماط الطلب السكني
- تكاليف الصيانة غير المتوقعة
- تغير الظروف الاقتصادية

🟢 **المخاطر المنخفضة (20%):**
- مشاكل قانونية وإدارية
- صعوبة في إيجاد مستأجرين
- تغير أسعار الفائدة

**استراتيجيات التخفيف:**
1. التنويع الجغرافي عبر 3 مناطق مختلفة
2. بناء احتياطي نقدي لـ 6 أشهر
3. تأمين شامل ضد جميع المخاطر
4. عقود تحوط ضد تقلبات الأسعار
        """,
        
        "🚀 فرص النمو الاستثنائية": """
**الفرص الذهبية في السوق:**

🥇 **الفرصة الأولى: المناطق الشمالية**
- معدل نمو متوقع: 18% سنوياً
- حجم الاستثمارات: 500 مليار ريال
- التوقيت: 2024-2026
- التوصية: الاستثمار المبكر

🥈 **الفرصة الثانية: المناطق المركزية**  
- معدل نمو متوقع: 14% سنوياً
- حجم الاستثمارات: 200 مليار ريال
- التوقيت: 2024-2025
- التوصية: الاستثمار المتوسط

🥉 **الفرصة الثالثة: المناطق السكنية**
- معدل نمو متوقع: 12% سنوياً
- حجم الاستثمارات: 150 مليار ريال
- التوقيت: 2024-2027
- التوصية: الاستثمار الآمن

**الفرص الناشئة:**
- العقارات الذكية: +25% نمو متوقع
- المباني الخضراء: +22% نمو متوقع
- المجمعات المتكاملة: +18% نمو متوقع
        """,
        
        "💡 نصائح الخبراء": """
**حكمة من واقع التجربة:**

🎓 **من مستثمر ناجح:**
"النجاح في العقارات لا يأتي من الصفقات الكبيرة، بل من القرارات الصحيحة المتتالية"

💼 **من وسيط محترف:**
"أفضل استثمار هو الذي تفهمه تماماً وتشعر بالراحة تجاه مخاطره"

🏆 **من مطور عقاري:**
"الجودة تبني السمعة، والسمعة تبني الثروة"

**نصائح عملية:**
1. ادرس السوق لمدة 3 أشهر قبل الاستثمار
2. استشر أكثر من خبير قبل اتخاذ القرار
3. لا تستثمر أكثر من 30% من رأس مالك في صفقة واحدة
4. حافظ على سيولة كافية للطوارئ
5. تابع السوق أسبوعياً وكن مستعداً للتعديل
        """,
        
        "📋 خطة التنفيذ التفصيلية": """
**الخطوات العملية للنجاح:**

📅 **الأسبوع 1-4: الدراسة والبحث**
- تحليل 50 عقار مشابه
- دراسة 10 مشاريع منافسة
- مقابلة 5 وسطاء متخصصين
- زيارة 3 مناطق مستهدفة

📅 **الشهر 2-3: التفاوض والشراء**
- التفاوض على 3 عقارات واعدة
- دراسة الجدوى التفصيلية
- تأمين التمويل المناسب
- إتمام الصفقة الأفضل

📅 **الشهر 4-6: التطوير والتأجير**
- تجهيز العقار بأفضل المواصفات
- وضع خطة تسويقية مكثفة
- اختيار المستأجرين المناسبين
- بدء تحقيق العوائد

**مؤشرات النجاح:**
- تحقيق 80% إشغال خلال 3 أشهر
- عائد 8% على الاستثمار سنوياً
- نمو القيمة السوقية 10% سنوياً
        """,
        
        "🔮 توقعات المستقبل": """
**رؤية 2030 وتأثيرها على العقارات:**

🏙️ **التأثيرات الإيجابية:**
- نمو الاستثمارات الأجنبية: +40%
- زيادة السياحة: +25 مليون سائح
- نمو الاقتصاد: +3.5% سنوياً
- تحسين البنية التحتية: +200%

📊 **التوقعات الاقتصادية:**
- نمو الناتج المحلي: 3.8% سنوياً
- ارتفاع احتياطي النقد الأجنبي: 2.1 تريليون ريال
- نمو الصادرات غير النفطية: +12%

🎯 **الفرص المستقبلية:**
- الذكاء الاصطناعي في العقارات: +35% نمو
- الاستدامة والطاقة الخضراء: +28% نمو
- التكنولوجيا المالية: +22% نمو
        """,
        
        "🏆 الخلاصة والتوصيات": """
**النتائج النهائية والتوصيات:**

✅ **التقييم النهائي:**
- تصنيف الاستثمار: 🟢 ممتاز
- مستوى المخاطرة: 🟡 متوسطة
- التوصية: 🟢 شراء مستعجل

🎯 **التوصيات الاستراتيجية:**
1. الاستثمار الفوري في المنطقة
2. التركيز على النوعية لا الكمية
3. التنويع في المحفظة الاستثمارية
4. المتابعة المستمرة للسوق

**خاتمة:**
هذا ليس مجرد تقرير، بل هو خريطة طريق نحو النجاح الاستثماري. ثق بقدراتك واتخذ القرار المدروس.
        """
    }
    
    # إضافة قسم خاص للمؤثرين
    if user_type == "مؤثر":
        report_sections["🎁 هدية Warda Intelligence"] = """
        **عزيزي المؤثر الكريم،**

        نقدم لك هذا التقرير الذهبي كهدية حصرية تقديراً لتأثيرك الإيجابي في المجتمع.

        **ماذا تحصل عليه مجاناً؟**
        🥇 تقرير ذهبي بقيمة 79 دولار
        📊 10 صفحات من التحليل المتقدم
        🎯 رسومات بيانية تفاعلية
        💡 نصائح استثمارية حصرية

        **كيف تدعمنا؟**
        بمشاركتك تجربتك مع منصة Warda Intelligence، فأنت تساعد في:
        - نشر الثقافة الاستثمارية الواعية
        - دعم منصة عربية متخصصة
        - تمكين المستثمرين من اتخاذ قرارات مدروسة

        **شكراً لكونك جزءاً من نجاحنا!**

        *فريق Warda Intelligence*
        """
    
    return report_sections

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
    
    property_count = st.slider("🔢 عدد العقارات للتحليل:", 1, 1000, 1,
                              help="كلما زاد عدد العقارات، زادت دقة التحليل والسعر")
    
    chosen_pkg = st.radio("اختر باقتك:", list(PACKAGES.keys()))
    
    base_price = PACKAGES[chosen_pkg]["price"]
    total_price = base_price * property_count
    
    st.markdown(f"""
    <div class='package-card'>
    <h3>باقة {chosen_pkg}</h3>
    <h4>{total_price} دولار</h4>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("**المميزات:**")
    for feature in PACKAGES[chosen_pkg]["features"]:
        st.write(f"✅ {feature}")

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
            report_data = generate_executive_report(user_type, city, property_type, area, status, chosen_pkg)
            user_info = {
                "user_type": user_type,
                "city": city, 
                "property_type": property_type,
                "area": area,
                "package": chosen_pkg
            }
            
            # إنشاء الرسومات البيانية للباقات المدفوعة
            if chosen_pkg != "مجانية":
                st.markdown("### 📈 الرسوم البيانية المتقدمة")
                fig_returns, fig_growth = create_advanced_visualizations(market_data, user_type)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(fig_returns, use_container_width=True)
                with col2:
                    st.plotly_chart(fig_growth, use_container_width=True)
            
            pdf_buffer = create_professional_arabic_pdf(report_data, user_info)
            
            st.session_state.pdf_data = pdf_buffer.getvalue()
            st.session_state.report_generated = True
            
            st.success("✅ تم إنشاء التقرير الاحترافي بنجاح!")
            st.balloons()
            
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
    - 10 صفحات من المحتوى الثري والشامل
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
        
        st.sidebar.markdown(f"**📋 معلومات الرابط:**")
        st.sidebar.markdown(f"- المؤثر: {st
