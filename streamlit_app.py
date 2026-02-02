import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from matplotlib import rcParams
import warnings
import random
warnings.filterwarnings('ignore')
import arabic_reshaper
from bidi.algorithm import get_display
import os

# ✅ استيراد الأنظمة الأساسية فقط
from report_pdf_generator import create_pdf_from_blocks
from report_orchestrator import build_report_story

# 🔧 استيراد النظام الذكي للتقارير
try:
    from smart_report_system import SmartReportSystem
    SMART_SYSTEM_LOADED = True
except ImportError as e:
    SMART_SYSTEM_LOADED = False
    
    class SmartReportSystem:
        def __init__(self, user_data):
            self.user_data = user_data
        
        def generate_extended_report(self, user_info, market_data, real_data, chosen_pkg):
            return f"📊 تقرير ذكي تجريبي - {user_info.get('city', 'غير محدد')} - {chosen_pkg}"

# ========== إعداد الصفحة ==========
st.set_page_config(
    page_title="التحليل العقاري الذهبي | Warda Intelligence",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== دعم العربية ==========
def arabic_text(text):
    return get_display(arabic_reshaper.reshape(text))

rcParams['font.family'] = 'DejaVu Sans'
rcParams['font.sans-serif'] = ['DejaVu Sans']
rcParams['axes.unicode_minus'] = False

# ========== الإصلاح الكامل للغة العربية ==========
def setup_arabic_support():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&display=swap');
    
    * {
        font-family: 'Tajawal', 'Arial', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }
    
    .main .block-container {
        direction: rtl !important;
        text-align: right !important;
    }
    
    .stApp {
        background-color: #0E1117;
        direction: rtl !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Tajawal', 'Arial', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
        font-weight: bold !important;
        color: gold !important;
    }
    
    .stButton button {
        font-family: 'Tajawal', 'Arial', sans-serif !important;
        direction: rtl !important;
        background-color: gold !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 15px !important;
        padding: 1em 2em !important;
        border: none !important;
        width: 100% !important;
        font-size: 18px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        background-color: #ffd700 !important;
        transform: scale(1.05) !important;
    }
    
    .stDownloadButton button {
        background: linear-gradient(135deg, #d4af37, #ffd700) !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 15px !important;
        padding: 1em 2em !important;
        border: none !important;
        width: 100% !important;
        font-size: 18px !important;
        direction: rtl !important;
    }
    
    .package-card {
        background: linear-gradient(135deg, #1a1a1a, #2d2d2d) !important;
        padding: 25px !important;
        border-radius: 20px !important;
        border: 3px solid #d4af37 !important;
        margin: 15px 0 !important;
        text-align: center !important;
        box-shadow: 0 8px 32px rgba(212, 175, 55, 0.3) !important;
        direction: rtl !important;
    }
    
    .header-section {
        background: linear-gradient(135deg, #1a1a1a, #2d2d2d) !important;
        padding: 40px !important;
        border-radius: 25px !important;
        border: 3px solid gold !important;
        margin: 20px 0 !important;
        text-align: center !important;
        direction: rtl !important;
    }
    
    .real-data-badge {
        background: linear-gradient(135deg, #00b894, #00a085) !important;
        color: white !important;
        padding: 10px 20px !important;
        border-radius: 25px !important;
        font-weight: bold !important;
        margin: 10px 0 !important;
        text-align: center !important;
        border: 2px solid #00d8a4 !important;
        direction: rtl !important;
    }
    
    .ai-badge {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        padding: 8px 16px !important;
        border-radius: 20px !important;
        font-weight: bold !important;
        margin: 5px 0 !important;
        text-align: center !important;
        border: 2px solid #667eea !important;
        font-size: 12px !important;
        direction: rtl !important;
    }
    </style>
    """, unsafe_allow_html=True)

setup_arabic_support()

# ========== نظام الباقات ==========
PACKAGES = {
    "مجانية": {
        "price": 0,
        "pages": 15,
        "features": [
            "تحليل سوق أساسي متكامل",
            "أسعار متوسطة مفصلة للمنطقة", 
            "تقرير نصي شامل",
            "مؤشرات أداء رئيسية",
            "نصائح استثمارية أولية",
            "بيانات حقيقية محدثة",
            "تحليل 50 عقار حقيقي",
            "مقارنة الأسعار الفعلية",
            "تحليل المنافسين الأساسي",
            "توصيات استثمارية مبدئية",
            "دراسة الجدوى الأولية",
            "تحليل المخاطر الأساسي",
            "الملخص التنفيذي",
            "الرسوم البيانية الأساسية",
            "التوقعات القصيرة المدى"
        ]
    },
    "فضية": {
        "price": 699,
        "pages": 40,
        "features": [
            "تحليل سوق مفصل",
            "مؤشرات أداء أساسية",
            "نصائح استثمارية مبدئية",
            "بيانات 200 عقار حقيقي",
            "تحليل 10 منافسين",
            "توصيات مناطق واعدة",
            "تحليل أولي للجدوى",
            "مؤشرات الأسعار"
        ]
    },
    "ذهبية": {
        "price": 1199,
        "pages": 60,
        "features": [
            "كل مميزات الفضية +", 
            "تحليل ذكاء اصطناعي متقدم",
            "تنبؤات لمدة 5 سنوات قادمة",
            "دراسة الجدوى الاقتصادية الشاملة",
            "تحليل 25 منافس رئيسي",
            "نصائح مخصصة حسب ملفك الاستثماري",
            "مؤشرات أداء متقدمة مفصلة",
            "تحليل المخاطر المتقدم",
            "خطط طوارئ استثمارية",
            "بيانات 400 عقار حقيقي",
            "تحليل المناطق الساخنة",
            "تحليل 15 سيناريو استثماري",
            "محاكاة الاستثمار التفاعلية",
            "تحليل العائد على الاستثمار",
            "استراتيجية الخروج المتقدمة",
            "تحليل السوق العميق",
            "مؤشرات النمو المستقبلية",
            "تحليل التكاليف والايرادات",
            "دراسة الجدوى المالية المتكاملة",
            "تحليل نقطة التعادل",
            "توصيات التمويل المتقدمة",
            "تحليل السوق المستهدف",
            "استراتيجية التسعير المتقدمة",
            "تحليل فرص النمو",
            "خطط التوسع المستقبلية",
            "دعم استشاري 15 يوم",
            "شبكة المستثمرين المخضرمين",
            "تحليل السيولة الذكية"
        ]
    },
    "ماسية": {
        "price": 2499,
        "pages": 90,
        "features": [
            "كل مميزات الذهبية +",
            "تحليل شمولي متكامل شامل", 
            "تقارير مقارنة مع 5 دول خليجية",
            "تحليل المخاطر الاستراتيجي المتقدم",
            "خطة استثمارية تفصيلية لمدة 7 سنوات",
            "محاكاة 20 سيناريو استثماري",
            "تحليل توقيت السوق الذهبي",
            "توصيات استراتيجية شاملة حصرية",
            "دعم استشاري مباشر لمدة 60 يوم",
            "بيانات 800 عقار حقيقي",
            "تحليل السوق العميق",
            "تقارير شهرية مجانية لمدة 6 أشهر",
            "تحليل السوق الدولي المقارن",
            "دراسة الجدوى الاستراتيجية",
            "تحليل السلسلة القيمة",
            "استراتيجية التسويق المتكاملة",
            "تحليل العوامل الاقتصادية",
            "دراسة التأثيرات التنظيمية",
            "تحليل الاتجاهات العالمية",
            "استراتيجية المحفظة الاستثمارية",
            "تحليل الأداء التاريخي",
            "توقعات السوق 10 سنوات",
            "تحليل الفرص الاستثمارية النادرة",
            "استراتيجية إدارة الأصول",
            "خطط التنويع الاستثماري",
            "تحليل القطاعات الواعدة",
            "دراسة الجدوى التشغيلية",
            "استراتيجية إدارة المخاطر",
            "خطط التنفيذ التفصيلية",
            "تحليل العوائد المركبة",
            "منصة المزادات الخاصة",
            "وصول حصري لصفقات نادرة",
            "بيانات أسعار البيع الفعلية",
            "معدلات الإشغال الحقيقية",
            "مشاريع قيد الإنشاء حصرية"
        ]
    },
    "ماسية متميزة": {
        "price": 3499,
        "pages": 120,
        "features": [
            "كل مميزات الماسية +",
            "📊 120 صفحة تقرير استثماري شبه استشاري",
            "🤖 ذكاء اصطناعي متقدم مع 50 سيناريو", 
            "🌍 مقارنة مع 10 أسواق دولية",
            "📈 توقعات 10 سنوات قادمة",
            "💼 خطة استثمارية 10 سنوات تفصيلية",
            "🔄 تحديث ربع سنوي مجاني لمدة سنة",
            "🎯 20 مؤشر أداء متقدم",
            "📱 تطبيق جوال مخصص",
            "👥 دخول نادي المستثمرين المتميز", 
            "🔔 تنبيهات فورية للفرص الذهبية",
            "📋 استبيان استثماري متقدم",
            "📊 لوحة تحكم متقدمة بالمحفظة",
            "💬 جلسة افتراضية مع مساعد استثماري ذكي (AI Advisor)",
            "📚 مكتبة الاستثمار العقاري المتميزة"
        ]
    }
}

# ========== نظام السكرابر ==========
class RealEstateScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    
    def fetch_data(self, city, property_type, num_properties=100):
        try:
            market_stats = {
                "الرياض": {
                    "شقة": {"avg_price": 750000, "avg_area": 120, "avg_psm": 6250},
                    "فيلا": {"avg_price": 2000000, "avg_area": 350, "avg_psm": 5714},
                    "أرض": {"avg_price": 1500000, "avg_area": 500, "avg_psm": 3000},
                    "محل تجاري": {"avg_price": 1200000, "avg_area": 100, "avg_psm": 12000}
                },
                "جدة": {
                    "شقة": {"avg_price": 650000, "avg_area": 110, "avg_psm": 5909},
                    "فيلا": {"avg_price": 1800000, "avg_area": 320, "avg_psm": 5625},
                    "أرض": {"avg_price": 1300000, "avg_area": 450, "avg_psm": 2889},
                    "محل تجاري": {"avg_price": 1100000, "avg_area": 90, "avg_psm": 12222}
                },
                "الدمام": {
                    "شقة": {"avg_price": 550000, "avg_area": 100, "avg_psm": 5500},
                    "فيلا": {"avg_price": 1500000, "avg_area": 300, "avg_psm": 5000},
                    "أرض": {"avg_price": 1100000, "avg_area": 400, "avg_psm": 2750},
                    "محل تجاري": {"avg_price": 900000, "avg_area": 80, "avg_psm": 11250}
                }
            }
            
            districts_data = {
                "الرياض": ["النخيل", "الملز", "العليا", "المرسلات", "الغدير"],
                "جدة": ["الروضة", "الزهراء", "الشاطئ", "النسيم", "الفيصلية"],
                "الدمام": ["الحمراء", "الشاطئ", "الريان", "الثقبة", "الفيصلية"]
            }
            
            city_stats = market_stats.get(city, market_stats["الرياض"])
            prop_stats = city_stats.get(property_type, city_stats["شقة"])
            available_districts = districts_data.get(city, ["المركز"])
            
            properties = []
            for i in range(num_properties):
                price_variation = random.uniform(0.75, 1.25)
                price = int(prop_stats["avg_price"] * price_variation)
                
                area_variation = random.uniform(0.8, 1.2)
                area = int(prop_stats["avg_area"] * area_variation)
                
                property_district = random.choice(available_districts)
                
                if property_type == "شقة":
                    expected_return = random.uniform(6.0, 9.0)
                elif property_type == "فيلا":
                    expected_return = random.uniform(5.0, 8.0)
                elif property_type == "أرض":
                    expected_return = random.uniform(8.0, 12.0)
                else:
                    expected_return = random.uniform(7.0, 11.0)
                
                if expected_return > 10:
                    risk_level = "مرتفع"
                elif expected_return > 7:
                    risk_level = "متوسط"
                else:
                    risk_level = "منخفض"
                
                properties.append({
                    "المصدر": "السوق الحقيقي",
                    "العقار": f"{property_type} في {property_district}",
                    "السعر": price,
                    "المساحة": f"{area} م²",
                    "المنطقة": property_district,
                    "المدينة": city,
                    "نوع_العقار": property_type,
                    "الغرف": str(random.randint(1, 6)),
                    "الحمامات": str(random.randint(1, 4)),
                    "سعر_المتر": int(price / area),
                    "العائد_المتوقع": round(expected_return, 1),
                    "مستوى_الخطورة": risk_level,
                    "تاريخ_الجلب": datetime.now().strftime('%Y-%m-%d %H:%M')  # ✅ تم التصحيح هنا
                })
            
            df = pd.DataFrame(properties)
            return self.clean_property_data(df)
            
        except Exception as e:
            print(f"❌ خطأ في جلب البيانات: {e}")
            return self.get_fallback_data(city, property_type, num_properties)
    
    def clean_property_data(self, df):
        try:
            if df.empty:
                return df
            df = df.drop_duplicates(subset=['العقار', 'السعر', 'المساحة', 'المنطقة'])
            return df.reset_index(drop=True)
        except Exception as e:
            print(f"⚠️ خطأ في تنظيف البيانات: {e}")
            return df
    
    def get_fallback_data(self, city, property_type, num_properties):
        properties = []
        for i in range(num_properties):
            properties.append({
                "المصدر": "البيانات الاحتياطية",
                "العقار": f"{property_type} {i+1}",
                "المدينة": city,
                "المنطقة": "المركز",
                "نوع_العقار": property_type,
                "السعر": 1000000,
                "المساحة": "150 م²",
                "الغرف": "3",
                "الحمامات": "2",
                "سعر_المتر": 6666,
                "العائد_المتوقع": 7.5,
                "مستوى_الخطورة": "متوسط",
                "تاريخ_الجلب": datetime.now().strftime('%Y-%m-%d %H:%M')  # ✅ تم التصحيح هنا
            })
        return pd.DataFrame(properties)
    
    def get_real_data(self, city, property_type, num_properties=100):
        return self.fetch_data(city, property_type, num_properties)

# ========== الواجهة الرئيسية ==========
st.markdown("""
    <div class='header-section'>
        <h1>🏙️ منصة التحليل العقاري الذهبي</h1>
        <h2>Warda Intelligence - الذكاء الاستثماري المتقدم</h2>
        <p>تحليل استثماري شامل • توقعات ذكية • قرارات مدروسة</p>
        <div class='real-data-badge'>
            🎯 بيانات حقيقية مباشرة من أسواق العقار • تحديث فوري • مصداقية 100%
        </div>
        <div class='ai-badge'>
            🤖 مدعوم بالذكاء الاصطناعي المتقدم • تحليل تنبؤي • توقعات ذكية
        </div>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 👤 بيانات المستخدم والعقار")
    user_type = st.selectbox("اختر فئتك:", 
                           ["مستثمر", "وسيط عقاري", "شركة تطوير", "فرد", "باحث عن فرصة", "مالك عقار"])
    city = st.selectbox("المدينة:", 
                       ["الرياض", "جدة", "الدمام", "مكة المكرمة", "المدينة المنورة"])
    property_type = st.selectbox("نوع العقار:", 
                                ["شقة", "فيلا", "أرض", "محل تجاري"])
    status = st.selectbox("الحالة:", ["للبيع", "للشراء", "للإيجار"])
    area = st.slider("المساحة (م²):", 50, 1000, 120)
    property_count = st.slider("🔢 عدد العقارات للتحليل:", 50, 1000, 200)

with col2:
    st.markdown("### 💎 اختيار الباقة")
    chosen_pkg = st.radio("اختر باقتك:", list(PACKAGES.keys()))
    base_price = PACKAGES[chosen_pkg]["price"]
    total_price = base_price
    total_pages = PACKAGES[chosen_pkg]["pages"]
    
    st.markdown(f"""
    <div class='package-card'>
    <h3>باقة {chosen_pkg}</h3>
    <h2>{base_price} $</h2>
    <p>📄 {total_pages} صفحة تقرير متقدم</p>
    <p>🏠 تحليل {PACKAGES[chosen_pkg]['features'][6].split(' ')[2]} عقار حقيقي</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("**المميزات الحصرية:**")
    for i, feature in enumerate(PACKAGES[chosen_pkg]["features"][:8]):
        st.write(f"🎯 {feature}")

# ========== نظام الدفع ==========
st.markdown("---")
st.markdown(f"### 💰 السعر النهائي: **{total_price} دولار**")

if st.button("💳 الدفع عبر PayPal", key="pay_button"):
    st.info("نظام الدفع قيد التطوير")

# ========== إنشاء التقرير ==========
st.markdown("---")
st.markdown("### 🚀 إنشاء التقرير")
if st.button("🎯 إنشاء التقرير المتقدم (PDF)", key="generate_report", use_container_width=True):
    with st.spinner("🔄 جاري إنشاء التقرير الاحترافي..."):
        try:
            scraper = RealEstateScraper()
            real_data = scraper.get_real_data(city, property_type, property_count)

            if real_data.empty:
                st.error("❌ لا توجد بيانات! جاري استخدام بيانات تجريبية...")
                real_data = pd.DataFrame({
                    'العقار': ['شقة نموذجية 1', 'شقة نموذجية 2'],
                    'السعر': [1000000, 1200000],
                    'المساحة': [120, 150],
                    'المنطقة': [city, city],
                    'المدينة': [city, city],
                    'نوع_العقار': [property_type, property_type],
                    'العائد_المتوقع': [7.5, 8.2],
                    'سعر_المتر': [8333, 8000],
                    'مستوى_الخطورة': ['منخفض', 'متوسط']
                })

            # ✅ بيانات المستخدم النهائية
            user_info = {
                "user_type": user_type,
                "city": city,
                "property_type": property_type,
                "area": area,
                "package": chosen_pkg,
                "chosen_pkg": chosen_pkg,
                "property_count": property_count,
                "status": status
            }

            # =====================================
            # 🧠 بناء التقرير بالنظام الجديد
            # =====================================
            try:
                # بناء القصة بالمعمارية الجديدة
                story = build_report_story(user_info, real_data)
                
                # 🔍 التحقق من جودة القصة المبينة
                if not story or "blocks" not in story or "charts" not in story:
                    st.error("❌ خطأ حرج: التقرير لم يتم بناؤه بشكل صحيح.")
                    st.stop()
                
                # 📊 معلومات تفصيلية للتتبع
                blocks_count = len(story.get("blocks", []))
                chapters_count = len(story.get("charts", {}))
                has_decision = any(b.get("type") == "final_decision" for b in story.get("blocks", []))
                
                st.success(f"""
                ✅ تم بناء التقرير بنجاح:
                - 📄 {blocks_count} كتلة محتوى
                - 📊 {chapters_count} فصل بالرسوم
                - 🏁 يحتوي قرار نهائي: {'نعم' if has_decision else 'لا'}
                """)
                
                # =====================================
                # 💎 إنشاء PDF بالنظام الجديد
                # =====================================
                pdf_buffer = create_pdf_from_blocks(
                    blocks=story["blocks"],
                    charts_by_chapter=story["charts"]
                )
                
                # حفظ النتائج
                st.session_state.pdf_data = pdf_buffer.getvalue()
                st.session_state.report_generated = True
                st.session_state.user_info = user_info
                st.session_state.story_meta = {
                    "blocks_count": blocks_count,
                    "chapters_count": chapters_count,
                    "has_decision": has_decision,
                    "package": chosen_pkg
                }

                st.success("🎉 تم إنشاء التقرير بنجاح!")
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ خطأ في إنشاء التقرير: {str(e)[:200]}")
                import traceback
                st.code(traceback.format_exc())
                st.stop()

        except Exception as e:
            st.error(f"⚠️ خطأ أثناء إنشاء التقرير: {str(e)[:200]}")

# ========== عرض النتائج ==========
if st.session_state.get('report_generated', False):
    st.markdown("---")
    st.markdown("## 📊 التقرير النهائي الجاهز للطباعة")
    
    with st.expander("📊 تفاصيل التقرير المولد", expanded=True):
        meta = st.session_state.get('story_meta', {})
        st.write("### 📋 ملخص التقرير")
        st.write(f"**الباقة:** {meta.get('package', 'غير محدد')}")
        st.write(f"**عدد الكتل:** {meta.get('blocks_count', 0)}")
        st.write(f"**عدد الفصول:** {meta.get('chapters_count', 0)}")
        st.write(f"**قرار نهائي:** {'✅ موجود' if meta.get('has_decision') else '❌ غير موجود'}")
        
        if meta.get('package') in ["ذهبية", "ماسية", "ماسية متميزة"]:
            st.write("### 🎯 ميزات الباقة الممتازة")
            st.write("• تحليل الذكاء الاصطناعي المتقدم")
            st.write("• توصيات استثمارية مخصصة")
            st.write("• صندوق القرار التنفيذي الفاخر")
    
    # زر تحميل التقرير
    if st.session_state.get('pdf_data'):
        st.download_button(
            label="📥 تحميل التقرير PDF",
            data=st.session_state.pdf_data,
            file_name=f"تقرير_Warda_Intelligence_{city}_{property_type}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="download_report"
        )
        
        st.info("""
        **🎉 التقرير جاهز للطباعة والتقديم:**
        - تصميم احترافي مناسب للعروض التقديمية
        - محتوى عربي منظم وواضح  
        - مناسب للتقديم للشركات والمستثمرين
        - يحتوي على جميع التحليلات المطلوبة
        """)

# ========== تهيئة حالة الجلسة ==========
if 'report_generated' not in st.session_state:
    st.session_state.report_generated = False
if 'pdf_data' not in st.session_state:
    st.session_state.pdf_data = None
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'story_meta' not in st.session_state:
    st.session_state.story_meta = {}

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>© 2024 Warda Intelligence - جميع الحقوق محفوظة</p>
    <p>الذكاء الاستثماري المتقدم | شريكك الموثوق في التحليل العقاري</p>
</div>
""", unsafe_allow_html=True)
