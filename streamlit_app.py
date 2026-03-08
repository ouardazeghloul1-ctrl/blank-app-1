import streamlit as st
from government_data_provider import load_government_data

st.set_page_config(
    page_title="التحليل العقاري الذهبي | Warda Intelligence",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

df_raw = load_government_data(selected_city=None, selected_property_type=None)

# ===== التحقق من أن البيانات تم تحميلها بشكل صحيح =====
if df_raw is None or df_raw.empty:
    st.error("❌ فشل تحميل بيانات السوق من الملف الحكومي")
    st.write("📌 الرجاء التأكد من:")
    st.write("1. وجود ملف market_transactions.csv في المجلد")
    st.write("2. أن الملف يحتوي على بيانات صالحة")
    st.write("3. أن ترميز الملف UTF-8")
    st.stop()

# ===== التحقق من الأعمدة الأساسية =====
required_cols = ["city", "district", "price"]
missing_cols = []
for col in required_cols:
    if col not in df_raw.columns:
        missing_cols.append(col)

if missing_cols:
    st.error(f"❌ الأعمدة التالية غير موجودة في البيانات: {missing_cols}")
    st.write("📌 الأعمدة الموجودة في الملف:")
    st.write(list(df_raw.columns))
    st.write("\n📌 أول 3 صفوف من الملف (للتشخيص):")
    st.write(df_raw.head(3))
    st.stop()

st.write("📊 عدد كل الصفقات بدون أي فلترة:", len(df_raw))

st.write("📋 أول 5 صفوف من الملف:")
st.write(df_raw.head())

st.write("📌 أسماء الأعمدة النهائية:")
st.write(df_raw.columns.tolist())

st.write("🔍 اختبار مباشر لمزود البيانات")

test_df = load_government_data(selected_city="الرياض", selected_property_type="شقة")
st.write("عدد شقق الرياض:", len(test_df))

test_df2 = load_government_data(selected_city="جدة", selected_property_type="شقة")
st.write("عدد شقق جدة:", len(test_df2))

test_df3 = load_government_data(selected_city="الرياض", selected_property_type="محل تجاري")
st.write("عدد المحلات التجارية في الرياض:", len(test_df3))

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import hashlib
import time
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import rcParams
import warnings
warnings.filterwarnings('ignore')
import arabic_reshaper
from bidi.algorithm import get_display
import paypalrestsdk
from dotenv import load_dotenv
import os
import streamlit.components.v1 as components

# ✅ المصدر الوحيد للبيانات الحقيقية (تم حذف الاستيراد المكرر)
import pandas as pd
import os

# ===== Robo Chat System (النسخة الموحدة) =====
from robo_advisor import handle_robo_question, RoboGuard, RoboKnowledge

# ✅ استيراد نظام التنبيهات الموحد (ملف واحد فقط) - الإصدار النهائي
try:
    from alerts_system import (
        get_today_alerts,
        get_alerts_by_city,
        format_alert_for_display,
        refresh_alerts,
        get_alerts_stats,
        update_market_and_check_alerts
    )
    ALERTS_AVAILABLE = True
    print("✅ نظام التنبيهات الموحد متصل بنجاح")
except ImportError as e:
    ALERTS_AVAILABLE = False
    print(f"⚠️ تحذير: نظام التنبيهات غير متوفر: {e}")
    
    # دوال بديلة في حالة عدم وجود النظام
    def get_today_alerts(force_refresh=False):
        return []
    
    def get_alerts_by_city(city):
        return []
    
    def format_alert_for_display(alert):
        return {}
    
    def refresh_alerts():
        return []
    
    def get_alerts_stats():
        return {
            "total": 0,
            "by_city": {},
            "by_confidence": {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        }
    
    def update_market_and_check_alerts(city, property_type):
        st.error("⚠️ نظام التنبيهات غير متوفر")
        return []

# ✅ استيراد الأنماط والخطوط لـ ReportLab
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ✅ استيراد الأنظمة المتخصصة
from ultimate_report_system import UltimateReportSystem
from premium_content_generator import PremiumContentGenerator
from advanced_charts import AdvancedCharts

# ✅ النظام الموحد لإنشاء PDF
from report_pdf_generator import create_pdf_from_content

# 🔧 استيراد النظام الذكي للتقارير - الإصدار المحسّن
try:
    from smart_report_system import SmartReportSystem
    SMART_SYSTEM_LOADED = True
except ImportError as e:
    SMART_SYSTEM_LOADED = False
    
    class SmartReportSystem:
        def __init__(self, user_data):
            self.user_data = user_data
        
        def generate_smart_report(self, user_info, market_data, real_data, chosen_pkg):
            return f"📊 تقرير ذكي تجريبي - {user_info.get('city', 'غير محدد')} - {chosen_pkg}"
        
        def generate_extended_report(self, user_info, market_data, real_data, chosen_pkg):
            return self.generate_smart_report(user_info, market_data, real_data, chosen_pkg)

# استيراد الأنظمة الجديدة
try:
    from smart_opportunities import SmartOpportunityFinder
    from finance_comparison import FinanceComparator
except ImportError:
    class SmartOpportunityFinder:
        def analyze_all_opportunities(self, user_info, market_data, real_data):
            return {'عقارات_مخفضة': [], 'مناطق_صاعدة': [], 'توقيت_الاستثمار': 'محايد', 'ملخص_الفرص': 'تحتاج بيانات أكثر'}
    
    class FinanceComparator:
        def generate_financing_report(self, user_info, property_price):
            return {'خيارات_التمويل': [], 'حاسبة_التمويل': {}, 'نصيحة_التمويل': 'تحتاج بيانات أكثر'}

try:
    from market_intelligence import MarketIntelligence
except ImportError:
    class MarketIntelligence:
        pass


# ===============================
# 📱 PWA – ربط manifest (تطبيق الهاتف) بعد set_page_config مباشرة
# ===============================
st.markdown("""
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#FFD700">
""", unsafe_allow_html=True)

# إعداد الدفع
load_dotenv()
for folder in ["outputs", "logs", "models"]:
    os.makedirs(folder, exist_ok=True)

paypalrestsdk.configure({
    "mode": os.getenv("PAYPAL_MODE", "sandbox"),
    "client_id": os.getenv("PAYPAL_CLIENT_ID"),
    "client_secret": os.getenv("PAYPAL_CLIENT_SECRET")
})

# ========== دعم العربية ==========
def arabic_text(text):
    return get_display(arabic_reshaper.reshape(text))

rcParams['font.family'] = 'DejaVu Sans'
rcParams['font.sans-serif'] = ['DejaVu Sans']
rcParams['axes.unicode_minus'] = False

# ========== الإصلاح الكامل للغة العربية مع إزالة المربع الأبيض ==========
def setup_arabic_support():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&display=swap');
    
    * {
        font-family: 'Tajawal', 'Arial', sans-serif !important;
    }
    
    html, body, .main .block-container {
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
        color: #FFD700 !important;
    }
    
    p, div, span {
        direction: rtl !important;
        text-align: right !important;
        unicode-bidi: embed !important;
        color: #EAEAEA !important;
    }
    
    strong {
        color: #00FFD1 !important;
    }
    
    .stTextInput label, .stNumberInput label, .stSelectbox label, 
    .stTextArea label, .stRadio label {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Tajawal', 'Arial', sans-serif !important;
        color: gold !important;
        font-weight: bold !important;
    }
    
    .stButton button {
        font-family: 'Tajawal', 'Arial', sans-serif !important;
        direction: rtl !important;
        background-color: gold !important;
        font-weight: bold !important;
        border-radius: 15px !important;
        padding: 1em 2em !important;
        border: none !important;
        width: 100% !important;
        font-size: 18px !important;
        transition: all 0.3s ease !important;
    }
    
    /* ✅ إصلاح لون النص في الأزرار الصفراء فقط */
    .stButton button,
    .stButton button span {
        color: #000000 !important;   /* أسود واضح */
        text-shadow: none !important;
        font-weight: 800 !important;
    }
    
    .stButton button:hover {
        background-color: #ffd700 !important;
        transform: scale(1.05) !important;
    }
    
    table {
        direction: rtl !important;
        text-align: right !important;
    }
    
    .stAlert {
        direction: rtl !important;
        text-align: right !important;
    }
    
    [data-testid="stMarkdownContainer"] {
        direction: rtl !important;
        text-align: right !important;
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
    
    /* ===== إصلاح المربع الأبيض بشكل نهائي ===== */
    .streamlit-expanderHeader {
        background-color: #1a1a1a !important;
        color: #FFD700 !important;
        border-radius: 10px !important;
        border: 1px solid #333 !important;
        padding: 10px !important;
        margin: 5px 0 !important;
        font-weight: bold !important;
        direction: rtl !important;
        text-align: right !important;
    }
    
    .streamlit-expanderContent {
        background-color: #0E1117 !important;
        color: #EAEAEA !important;
        border: 1px solid #333 !important;
        border-radius: 0 0 10px 10px !important;
        padding: 15px !important;
        margin-top: -1px !important;
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* إزالة أي خلفيات بيضاء غير مرغوب فيها */
    div[data-testid="stExpander"] {
        background-color: transparent !important;
        border: none !important;
    }
    
    div[data-testid="stExpander"] > div {
        background-color: transparent !important;
    }
    
    /* تنسيق الـ Expander عند التوسيع */
    .streamlit-expanderHeader:hover {
        background-color: #2a2a2a !important;
        border-color: #FFD700 !important;
    }
    
    /* إزالة أي مربعات بيضاء جانبية */
    .css-1kyxreq, .css-1r6slb0, .css-12w0qpk {
        background-color: transparent !important;
    }
    
    .element-container {
        background-color: transparent !important;
    }
    
    .stMarkdown {
        background-color: transparent !important;
    }
    
    /* ===== تنسيق التنبيهات ===== */
    .alert-golden {
        background: linear-gradient(135deg, #1a3a1a, #0a2a0a) !important;
        border-right: 5px solid gold !important;
        padding: 15px !important;
        border-radius: 10px !important;
        margin: 10px 0 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
    }
    
    .alert-shift {
        background: linear-gradient(135deg, #1a3a4a, #0a2a3a) !important;
        border-right: 5px solid #00a8ff !important;
        padding: 15px !important;
        border-radius: 10px !important;
        margin: 10px 0 !important;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #4a1a1a, #3a0a0a) !important;
        border-right: 5px solid #ff4444 !important;
        padding: 15px !important;
        border-radius: 10px !important;
        margin: 10px 0 !important;
    }
    
    .alert-timing {
        background: linear-gradient(135deg, #4a3a1a, #3a2a0a) !important;
        border-right: 5px solid #ffaa00 !important;
        padding: 15px !important;
        border-radius: 10px !important;
        margin: 10px 0 !important;
    }
    
    .alert-header {
        font-size: 18px !important;
        font-weight: bold !important;
        color: gold !important;
        margin-bottom: 10px !important;
    }
    
    .alert-meta {
        font-size: 14px !important;
        color: #888 !important;
        margin-top: 10px !important;
        border-top: 1px solid #333 !important;
        padding-top: 10px !important;
    }
    
    .alert-confidence-high {
        color: #00FFD1 !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

setup_arabic_support()

# ========== نظام الباقات ==========
PACKAGES = {
    "مجانية": {
        "price": 0,
        "data_scope": "50",
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
        "data_scope": "200",
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
        "data_scope": "400",
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
        "data_scope": "800",
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
        "data_scope": "1000+",
        "features": [
            "كل مميزات الماسية +",
            "📊 تقرير استثماري شبه استشاري شامل",
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

# ========== خريطة تصنيف المستخدمين ==========
USER_CATEGORIES = {
    "مستثمر": "investor",
    "وسيط عقاري": "broker", 
    "شركة تطوير": "developer",
    "فرد": "individual",
    "باحث عن فرصة": "opportunity",
    "مالك عقار": "owner"
}

# ========== نظام الذكاء الاصطناعي (بدون عشوائية) ==========
class AIIntelligence:
    def __init__(self):
        self.model_trained = False
        
    def train_ai_model(self, market_data, real_data):
        self.model_trained = True
        return "تم تدريب النموذج بنجاح"
    
    def generate_ai_recommendations(self, user_info, market_data, real_data):
        if market_data is None or real_data is None or real_data.empty:
            return {
                'ملف_المخاطر': "غير متوفر – يحتاج بيانات كافية",
                'استراتيجية_الاستثمار': "غير متوفر – يحتاج بيانات كافية",
                'التوقيت_المثالي': "غير متوفر – يحتاج بيانات كافية",
                'مؤشرات_الثقة': {
                    'جودة_البيانات': "غير متوفرة",
                    'استقرار_السوق': "غير متوفر",
                    'اتجاه_النمو': "غير متوفر",
                    'مستوى_الثقة': "0%"
                }
            }
        
        # تحليل المخاطر بناءً على البيانات الحقيقية فقط
        risk_factors = []
        
        # سيولة السوق
        if market_data.get('حجم_السيولة', 0) > 80:
            risk_factors.append("منخفض")
        elif market_data.get('حجم_السيولة', 0) > 50:
            risk_factors.append("متوسط")
        else:
            risk_factors.append("مرتفع")
        
        # تنوع الأحياء
        if 'district' in real_data.columns:
            unique_districts = real_data['district'].nunique()
            if unique_districts > 10:
                risk_factors.append("منخفض")
            elif unique_districts > 5:
                risk_factors.append("متوسط")
            else:
                risk_factors.append("مرتفع")
        
        # تحديد ملف المخاطر النهائي
        if "مرتفع" in risk_factors:
            risk_profile = "مرتفع المخاطر"
        elif "منخفض" in risk_factors and len([r for r in risk_factors if r == "منخفض"]) >= 2:
            risk_profile = "منخفض المخاطر"
        else:
            risk_profile = "متوسط المخاطر"
        
        return {
            'ملف_المخاطر': risk_profile,
            'استراتيجية_الاستثمار': "استراتيجية متوسطة - تحتاج دراسة إضافية",
            'التوقيت_المثالي': "يحتاج مقارنة زمنية (تحتاج لقطتين)",
            'مؤشرات_الثقة': {
                'جودة_البيانات': f"{len(real_data)} عقار حقيقي",
                'استقرار_السوق': "يحتاج مقارنة زمنية",
                'اتجاه_النمو': "يحتاج مقارنة زمنية",
                'مستوى_الثقة': "متوسطة"
            }
        }
    
    def analyze_risk_profile(self, user_info, market_data):
        if not market_data:
            return "غير متوفر – يحتاج بيانات"
        
        risk_factors = []
        
        if market_data.get('حجم_السيولة', 0) > 80:
            risk_factors.append("منخفض")
        elif market_data.get('حجم_السيولة', 0) > 50:
            risk_factors.append("متوسط")
        else:
            risk_factors.append("مرتفع")
        
        if "مرتفع" in risk_factors:
            return "مرتفع المخاطر – يحتاج دراسة متأنية"
        elif "منخفض" in risk_factors and len(risk_factors) >= 2:
            return "منخفض المخاطر"
        else:
            return "متوسط المخاطر"
    
    def generate_investment_strategy(self, risk_profile, market_data):
        return "استراتيجية متوسطة - تحتاج بيانات زمنية"
    
    def optimal_timing(self, market_data):
        return "يحتاج مقارنة زمنية بين لقطتين"
    
    def confidence_indicators(self, market_data, real_data):
        data_quality = f"{len(real_data)} عقار حقيقي" if not real_data.empty else "غير متوفرة"
        market_stability = "يحتاج مقارنة زمنية"
        growth_trend = "يحتاج مقارنة زمنية"
        
        return {
            'جودة_البيانات': data_quality,
            'استقرار_السوق': market_stability,
            'اتجاه_النمو': growth_trend,
            'مستوى_الثقة': "يحتاج بيانات تاريخية"
        }

# ========== توليد بيانات السوق (نسخة نظيفة بدون عشوائية) ==========
def generate_advanced_market_data(city, property_type, status, real_data):
    """
    توليد مؤشرات سوق مبنية فقط على بيانات حقيقية
    بدون random – بدون افتراضات وهمية
    """
    if real_data is None or real_data.empty:
        raise Exception("❌ لا توجد بيانات حقيقية لبناء مؤشرات السوق")

    df = real_data.copy()

    # تنظيف - استخدام الأعمدة الإنجليزية
    df = df.dropna(subset=["price", "area"])
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["area"] = pd.to_numeric(df["area"], errors="coerce")
    df = df.dropna()

    if df.empty:
        raise Exception("❌ البيانات غير صالحة للتحليل")

    # مؤشرات حقيقية
    df['سعر_المتر'] = df["price"] / df["area"]
    avg_price_per_m2 = df['سعر_المتر'].mean()
    min_price_per_m2 = df['سعر_المتر'].min()
    max_price_per_m2 = df['سعر_المتر'].max()

    property_count = len(df)

    # حجم السيولة = عدد العقارات الحالية
    liquidity_volume = property_count

    # عائد تأجيري (إن وجد)
    if "rental_yield" in df.columns:
        rental_yield = df["rental_yield"].mean()
    else:
        rental_yield = None

    # عرض وطلب
    supply = property_count
    demand = len(df[df['سعر_المتر'] < avg_price_per_m2]) if len(df) > 0 else 0

    return {
        "متوسط_سعر_المتر": round(avg_price_per_m2, 2),
        "أعلى_سعر_متر": round(max_price_per_m2, 2),
        "أقل_سعر_متر": round(min_price_per_m2, 2),
        "عدد_العقارات_الحقيقية": property_count,
        "حجم_السيولة": liquidity_volume,
        "العائد_التأجيري": round(rental_yield, 2) if rental_yield else "غير متوفر",
        "عرض_العقارات": supply,
        "طالب_الشراء": demand,
        "المصدر": "government_data_provider"
    }

# ========== الواجهة الرئيسية ==========
st.markdown("""
    <div class='header-section'>
        <h1>🏙️ منصة التحليل العقاري الذهبي</h1>
        <h2>Warda Intelligence - الذكاء الاستثماري المتقدم</h2>
        <p>تحليل استثماري شامل • مؤشرات ذكية • قرارات مدروسة</p>
        <div class='real-data-badge'>
            🎯 بيانات حقيقية من السوق • تحديث عند الطلب • مصداقية 100%
        </div>
        <div class='ai-badge'>
            🤖 مدعوم بالذكاء الاصطناعي المتقدم • تحليل تنبؤي • توقعات ذكية
        </div>
    </div>
""", unsafe_allow_html=True)

# ========== رسالة توجيه ذكية للمستشار ==========
st.info("🧠 لديك مستشار ذكي يجيبك حسب باقتك — انتقل إلى المستشار الذكي")

# ========== نظام التنقل (بديل عن التبويبات) ==========
page = st.radio(
    "التنقل",
    ["📊 التحليل الكامل", "🧠 المستشار الذكي"],
    horizontal=True,
    label_visibility="collapsed"
)

# ========== صفحة التحليل الكامل ==========
if page == "📊 التحليل الكامل":
    
    # ===== إضافة نظام تنقل داخلي للتحليل الكامل =====
    analysis_mode = st.radio(
        "نوع التحليل",
        ["🏙️ تقارير المدن", "📍 تقارير الأحياء"],
        horizontal=True
    )
    
    # ===== قسم تقارير المدن =====
    if analysis_mode == "🏙️ تقارير المدن":
        # ========== التنبيهات الحية (باستخدام النظام الموحد) ==========
        st.markdown("---")
        st.markdown("## 🔔 التنبيهات الاستثمارية الحية (اليوم)")

        # عناصر الاختيار للمدينة ونوع العقار (لزر التحديث)
        col_city, col_type = st.columns(2)
        with col_city:
            city_select = st.selectbox(
                "اختر المدينة",
                ["الرياض", "جدة", "مكة المكرمة", "المدينة المنورة", "الدمام"],
                key="city_select_alerts"
            )
        with col_type:
            property_type_select = st.selectbox(
                "اختر نوع العقار",
                ["شقة", "فيلا", "أرض"],
                key="property_type_select_alerts"
            )
        
        # زر التحديث الرسمي (القلب) - الحقيقي (تم إصلاحه)
        col_btn, col_info = st.columns([1, 3])
        with col_btn:
            if st.button("🔄 تحديث بيانات السوق (حقيقي)", key="market_update_btn", use_container_width=True):
                if not city_select:
                    st.error("❌ الرجاء اختيار المدينة أولاً")
                else:
                    with st.spinner("جاري جلب بيانات حقيقية وتحليل السوق..."):
                        try:
                            # 🔥 جلب البيانات مع الفلترة من المصدر نفسه
                            real_df = load_government_data(
                                selected_city=city_select,
                                selected_property_type=property_type_select
                            )

                            if real_df.empty:
                                st.error(f"❌ لا توجد بيانات للمدينة {city_select}")
                            else:
                                # تشغيل التنبيهات
                                alerts = update_market_and_check_alerts(
                                    city_select,
                                    property_type_select
                                )

                                st.session_state.daily_alerts = alerts
                                st.session_state.last_alert_refresh = datetime.now()

                                st.success(f"✅ تم تحديث السوق بـ {len(real_df)} صفقة")

                        except Exception as e:
                            st.error(f"❌ حدث خطأ: {str(e)}")

        with col_info:
            last_refresh = st.session_state.get('last_alert_refresh', datetime.now())
            refresh_time = last_refresh.strftime('%H:%M:%S') if isinstance(last_refresh, datetime) else str(last_refresh)
            st.caption(f"🕒 آخر تحديث: {refresh_time}")

        # جلب التنبيهات مرة واحدة فقط في الجلسة
        if "daily_alerts" not in st.session_state:
            with st.spinner("🔄 جاري تحليل السوق ورصد الفرص..."):
                if ALERTS_AVAILABLE:
                    st.session_state.daily_alerts = get_today_alerts()
                    st.session_state.last_alert_refresh = datetime.now()
                else:
                    st.session_state.daily_alerts = []
                    st.session_state.last_alert_refresh = datetime.now()
                    st.info("⚠️ نظام التنبيهات قيد التفعيل قريبًا")

        # فلترة التنبيهات حسب المدن المستهدفة
        TARGET_CITIES = ["الرياض", "جدة", "مكة المكرمة", "المدينة المنورة", "الدمام"]
        filtered_alerts = [
            alert for alert in st.session_state.daily_alerts
            if alert.get("city") in TARGET_CITIES
        ]

        # الحصول على إحصائيات التنبيهات
        alert_stats = get_alerts_stats() if ALERTS_AVAILABLE else {"total": 0, "by_confidence": {"HIGH": 0, "MEDIUM": 0, "LOW": 0}}

        # عرض إحصائيات سريعة
        if filtered_alerts:
            col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
            with col_stat1:
                st.metric("📊 إجمالي", len(filtered_alerts))
            with col_stat2:
                st.metric("🔴 قوية", alert_stats["by_confidence"].get("HIGH", 0))
            with col_stat3:
                st.metric("🟡 متوسطة", alert_stats["by_confidence"].get("MEDIUM", 0))
            with col_stat4:
                st.metric("🟢 خفيفة", alert_stats["by_confidence"].get("LOW", 0))

        # عرض عدد التنبيهات وآخر تحديث
        col_refresh, col_info = st.columns([1, 3])
        with col_refresh:
            if st.button("🔄 تحديث", key="refresh_alerts"):
                with st.spinner("جاري تحديث السوق..."):
                    try:
                        alerts = update_market_and_check_alerts(city_select, property_type_select)
                        st.session_state.daily_alerts = alerts
                        st.session_state.last_alert_refresh = datetime.now()
                        st.rerun()
                    except Exception as e:
                        st.info("ℹ️ لا توجد بيانات أحدث من آخر لقطة محفوظة. التحليل يعتمد على آخر بيانات موثوقة.")

        with col_info:
            last_refresh = st.session_state.get('last_alert_refresh', datetime.now())
            refresh_time = last_refresh.strftime('%H:%M:%S') if isinstance(last_refresh, datetime) else str(last_refresh)
            st.caption(f"🔒 عدد التنبيهات اليوم: {len(st.session_state.daily_alerts)} | 🕒 آخر تحديث: {refresh_time}")

        # عرض التنبيهات باستخدام دالة التنسيق من النظام الموحد
        if filtered_alerts:
            # تحديد عدد الأعمدة بناءً على عدد التنبيهات
            cols = st.columns(2) if len(filtered_alerts) > 1 else [st.container()]
            
            for i, alert in enumerate(filtered_alerts):
                with cols[i % 2] if len(filtered_alerts) > 1 else cols[0]:
                    # استخدام دالة التنسيق من النظام الموحد
                    formatted = format_alert_for_display(alert)
                    
                    # تحديد اللون حسب نوع التنبيه
                    alert_class = "alert-golden"
                    if alert.get("type") == "MARKET_SHIFT":
                        alert_class = "alert-shift"
                    elif alert.get("type") == "RISK_WARNING":
                        alert_class = "alert-warning"
                    elif alert.get("type") == "TIMING_SIGNAL":
                        alert_class = "alert-timing"
                    
                    confidence_class = "alert-confidence-high" if alert.get("confidence") == "HIGH" else ""
                    
                    # اقتطاع الوصف الطويل إذا لزم الأمر
                    description = formatted['description']
                    if len(description) > 300:
                        description = description[:300] + "..."
                    
                    # أيقونة مستوى الثقة
                    confidence_icon = formatted.get('confidence_icon', '💰')
                    
                    # بناء HTML التنبيه
                    html_content = f"""
                    <div class='{alert_class}'>
                        <div class='alert-header'>
                            {confidence_icon} {alert['city']} – {formatted['title']}
                        </div>
                        <div>
                            <p style='color: #EAEAEA;'>{description}</p>
                            <p><strong>النوع:</strong> {alert.get('type', 'GOLDEN_OPPORTUNITY')}</p>
                    """
                    
                    # إضافة الخصم إذا كان موجودًا (حتى لو كان 0)
                    discount = alert.get("signal", {}).get("discount_percent")
                    if discount is not None:
                        html_content += f"<p><strong>الخصم:</strong> {discount}%</p>"
                    
                    html_content += f"""
                            <p><strong>الثقة:</strong> <span class='{confidence_class}'>{formatted['confidence']}</span></p>
                        </div>
                        <div class='alert-meta'>
                            🕒 {formatted['time']}
                        </div>
                    </div>
                    """
                    
                    st.markdown(html_content, unsafe_allow_html=True)
        else:
            st.info("🔍 لا توجد تنبيهات جديدة الآن. استخدم زر 'تحديث بيانات السوق (حقيقي)' لجلب أحدث البيانات.")

        # ========== بيانات المستخدم ==========
        st.markdown("---")
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("### 👤 بيانات المستخدم والعقار")
            user_type = st.selectbox("اختر فئتك:", 
                                   ["مستثمر", "وسيط عقاري", "شركة تطوير", "فرد", "باحث عن فرصة", "مالك عقار"])
            city = st.selectbox("المدينة:", 
                               ["الرياض", "جدة", "الدمام", "مكة المكرمة", "المدينة المنورة"])
            
            # ===== تم حذف اختيار الحي من تقارير المدن =====
            
            property_type = st.selectbox("نوع العقار:", 
                                        ["شقة", "فيلا", "أرض", "محل تجاري"])
            status = st.selectbox("الحالة:", ["للبيع", "للشراء", "للإيجار"])
            
            # 🔄 استبدال السلايدر بـ Selectbox (حل نهائي لمشكلة السهم)
            area_options = [80, 100, 120, 150, 180, 200, 250, 300, 400, 500, 600, 800, 1000]
            area_index = st.selectbox(
                "📐 المساحة المستهدفة (م²)",
                range(len(area_options)),
                format_func=lambda i: f"{area_options[i]} م²",
                key="area_select"
            )
            area = area_options[area_index]
            st.markdown(f"**المساحة المختارة:** {area} م²")
            
            property_count_options = [50, 75, 100, 150, 200, 250, 300, 400, 500, 600, 700, 800, 900, 1000]
            count_index = st.selectbox(
                "🔢 عدد العقارات للتحليل",
                range(len(property_count_options)),
                format_func=lambda i: f"{property_count_options[i]} عقار",
                key="count_select"
            )
            property_count = property_count_options[count_index]
            st.markdown(f"**عدد العقارات المختارة:** {property_count}")

            # ✅ حفظ معلومات المستخدم فور اختياره للمدينة
            st.session_state["user_info"] = {
                "city": city,
                "district": None,  # لا يوجد حي في تقارير المدن
                "property_type": property_type,
                "status": status,
                "user_type": user_type,
                "package": st.session_state.get("chosen_pkg", "مجانية")
            }

        with col2:
            st.markdown("### 💎 اختيار الباقة")
            chosen_pkg = st.radio("اختر باقتك:", list(PACKAGES.keys()))
            base_price = PACKAGES[chosen_pkg]["price"]
            
            # حفظ الباقة في session_state
            st.session_state["chosen_pkg"] = chosen_pkg
            
            # تحديث user_info بالباقة الجديدة
            if "user_info" in st.session_state:
                st.session_state["user_info"]["package"] = chosen_pkg
            
            # ========== معادلة التسعير الديناميكي الذكية ==========
            extra_price = 0
            
            # إضافة تكلفة للعقارات الإضافية فوق الـ 50
            if property_count > 50:
                extra_price += (property_count - 50) * 2.5
            
            # إضافة تكلفة للمساحات الكبيرة فوق الـ 150 متر
            if area > 150:
                extra_price += ((area - 150) / 10) * 0.5
            
            total_price = base_price + round(extra_price, 2)
            
            st.markdown(f"""
            <div class='package-card'>
            <h3>باقة {chosen_pkg}</h3>
            <h2>{total_price} $</h2>
            <p>📊 تقرير تحليلي ديناميكي حسب البيانات</p>
            <p>🏠 تحليل {PACKAGES[chosen_pkg]['data_scope']} عقار حقيقي</p>
            </div>
            """, unsafe_allow_html=True)
            
            # نص قصير يشرح التسعير (غير مخيف)
            st.caption("التسعير ديناميكي ويعتمد على حجم التحليل، وليس عدد الصفحات.")
            
            st.markdown("**المميزات الحصرية:**")
            for i, feature in enumerate(PACKAGES[chosen_pkg]["features"][:8]):
                st.write(f"🎯 {feature}")

        # ===============================
        # 🧠 تغذية ذكية مبكرة للروبو (مُحسّنة) مع تحسين الأداء
        # ===============================

        # التحقق مما إذا كان التحديث مطلوبًا
        robo_needs_update = False
        
        if (
            st.session_state.get("last_city") != city
            or st.session_state.get("last_property_type") != property_type
            or st.session_state.get("last_status") != status
            or st.session_state.get("last_chosen_pkg") != chosen_pkg
        ):
            robo_needs_update = True
            # تحديث آخر القيم
            st.session_state["last_city"] = city
            st.session_state["last_property_type"] = property_type
            st.session_state["last_status"] = status
            st.session_state["last_chosen_pkg"] = chosen_pkg

        # تحديث معرفة الروبو فقط إذا لزم الأمر
        if robo_needs_update or "robo_knowledge" not in st.session_state:
            with st.spinner("🧠 تحديث المستشار الذكي..."):
                try:
                    # 1️⃣ تحميل بيانات حقيقية مباشرة من المصدر
                    real_data = load_government_data(
                        selected_city=city,
                        selected_property_type=property_type
                    )

                    if real_data is None or real_data.empty:
                        raise Exception("❌ لا توجد بيانات حقيقية من السوق لهذه المدينة.")

                    st.session_state["real_data"] = real_data

                    # 2️⃣ توليد بيانات السوق
                    market_data = generate_advanced_market_data(
                        city, property_type, status, real_data
                    )

                    # 3️⃣ حفظها في الجلسة
                    st.session_state["market_data"] = market_data
                    
                    # 4️⃣ تجهيز الفرص الذكية
                    opportunity_finder = SmartOpportunityFinder()
                    opportunities = opportunity_finder.analyze_all_opportunities(
                        user_info=st.session_state.get("user_info", {}),
                        market_data=st.session_state.get("market_data", {}),
                        real_data=st.session_state.get("real_data", pd.DataFrame())
                    )
                    
                    # 5️⃣ تحديث معرفة الروبو
                    st.session_state.robo_knowledge = RoboKnowledge(
                        real_data=st.session_state.get("real_data", pd.DataFrame()),
                        opportunities=opportunities,
                        alerts=st.session_state.get("daily_alerts", []),
                        market_data=st.session_state.get("market_data", {})
                    )

                except Exception as e:
                    st.warning(f"⚠️ لم يتم تحميل البيانات الذكية: {str(e)}")

        # ========== حاسبة الأثر المالي الذكية ==========
        st.markdown("---")
        st.markdown("### 📈 احسب العائد المتوقع من التقرير")

        col3, col4 = st.columns([1, 1])

        with col3:
            investment_value = st.number_input(
                "💰 قيمة الاستثمار المتوقع ($)",
                min_value=50000,
                max_value=5000000,
                step=50000,
                value=300000,
                format="%d"
            )
            
            # إظهار مؤشر المخاطر فقط للباقات المدفوعة
            if chosen_pkg != "مجانية":
                risk_level = st.select_slider(
                    "مستوى المخاطر المقبول",
                    options=["منخفض", "متوسط", "مرتفع"],
                    value="متوسط"
                )
            else:
                risk_level = "متوسط"  # قيمة افتراضية للمجانية
                st.info("🔍 للباقات المدفوعة: تحليل متقدم لمستوى المخاطر")

        with col4:
            st.markdown("#### نسب التحسين الاستثماري")
            
            # ===== التمييز الذكي بين المجاني والمدفوع =====
            if chosen_pkg == "مجانية":
                # المجاني: نسب منخفضة جداً - مجرد لمحة (أقل من 2% إجمالي)
                risk_avoidance = 0.01      # 1% فقط
                pricing_optimization = 0.005 # 0.5% فقط
                timing_advantage = 0.005     # 0.5% فقط
                analysis_type = "تقدير مبدئي مبني على تحليل أساسي"
                result_color = "#FFA500"  # برتقالي للمجانية
            else:
                # المدفوع: نسب كاملة حسب مستوى المخاطر
                if risk_level == "منخفض":
                    risk_avoidance = 0.08
                    pricing_optimization = 0.05
                    timing_advantage = 0.03
                elif risk_level == "متوسط":
                    risk_avoidance = 0.12
                    pricing_optimization = 0.08
                    timing_advantage = 0.05
                else:  # مرتفع
                    risk_avoidance = 0.15
                    pricing_optimization = 0.10
                    timing_advantage = 0.07
                analysis_type = "الأثر الاستثماري المتوقع"
                result_color = "#00d8a4"  # أخضر للمدفوع
            
            # حساب الأثر المالي
            gain_from_risk = investment_value * risk_avoidance
            gain_from_pricing = investment_value * pricing_optimization
            gain_from_timing = investment_value * timing_advantage
            
            total_estimated_gain = gain_from_risk + gain_from_pricing + gain_from_timing
            net_benefit = total_estimated_gain - total_price
            
            # عرض النتائج بشكل أنيق
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #1a1a1a, #2d2d2d); padding: 20px; border-radius: 15px; border: 2px solid #d4af37;'>
                <p style='color: gold; font-size: 14px; margin: 5px 0;'>{analysis_type}</p>
                <p style='color: gold; font-size: 16px; margin: 5px 0;'>📉 تجنب خسائر القرارات العشوائية: <strong style='color: white;'>{int(gain_from_risk):,} $</strong></p>
                <p style='color: gold; font-size: 16px; margin: 5px 0;'>💎 تحسين سعر الشراء: <strong style='color: white;'>{int(gain_from_pricing):,} $</strong></p>
                <p style='color: gold; font-size: 16px; margin: 5px 0;'>⏱️ استغلال توقيت السوق: <strong style='color: white;'>{int(gain_from_timing):,} $</strong></p>
                <hr style='border: 1px solid #d4af37; margin: 15px 0;'>
                <p style='color: gold; font-size: 18px; font-weight: bold;'>✅ {analysis_type}: <strong style='color: {result_color};'>{int(net_benefit):,} $</strong></p>
                <p style='color: #888; font-size: 14px;'>مقابل استثمار في التقرير بقيمة <strong>{int(total_price)} $</strong></p>
                <p style='color: #666; font-size: 12px; margin-top: 10px;'>الأرقام تقديرية مبنية على نماذج تحليلية ولا تمثل ضمانًا للعائد.</p>
            </div>
            """, unsafe_allow_html=True)

        # ========== الآلة الحاسبة العالمية النهائية ==========
        st.markdown("---")
        st.markdown("### 🧠 محاكاة القرار: بدون تقرير مقابل تقرير Warda")

        # التحقق من وجود بيانات السوق
        if 'market_data' in st.session_state and st.session_state.market_data:
            market_data = st.session_state.market_data
        else:
            st.warning("⚠️ لا توجد بيانات سوق كافية، يرجى تحديث البيانات أولاً")
            market_data = {
                'حجم_السيولة': 0,
                'أعلى_سعر_متر': 0,
                'أقل_سعر_متر': 0,
                'متوسط_سعر_المتر': 0,
                'عدد_العقارات_الحقيقية': 0
            }

        # ===== مؤشرات سوق حقيقية =====
        liquidity_volume = market_data["حجم_السيولة"] if market_data["حجم_السيولة"] > 0 else 1
        
        price_dispersion = 0
        if market_data["متوسط_سعر_المتر"] > 0:
            price_dispersion = abs(
                market_data["أعلى_سعر_متر"] - market_data["أقل_سعر_متر"]
            ) / market_data["متوسط_سعر_المتر"]
        
        growth_factor = 0  # إلى أن نربطه بلقطتين زمنيتين
        
        # 🔥 تعديل منطق المخاطرة ليكون أكثر واقعية
        if liquidity_volume > 0:
            decision_uncertainty = min(1 / math.sqrt(liquidity_volume), 0.15)
        else:
            decision_uncertainty = 0.15

        # ===== سيناريو بدون تقرير =====
        loss_wrong_pricing = investment_value * price_dispersion * 0.6 if price_dispersion > 0 else 0
        loss_bad_timing = investment_value * growth_factor * 0.4
        loss_risk_blindness = investment_value * decision_uncertainty * 0.5

        total_loss_without_report = (
            loss_wrong_pricing +
            loss_bad_timing +
            loss_risk_blindness
        )

        # ===== سيناريو مع تقرير Warda =====
        risk_reduction = total_loss_without_report * 0.65
        pricing_gain = investment_value * price_dispersion * 0.5 if price_dispersion > 0 else 0
        timing_gain = investment_value * growth_factor * 0.6

        total_benefit_with_report = (
            risk_reduction +
            pricing_gain +
            timing_gain
        )

        net_decision_advantage = total_benefit_with_report - total_price

        # ===== عرض المقارنة باستخدام components.html =====
        components.html(f"""
        <div style='display:flex; gap:20px; margin-top:20px; font-family: Tajawal, Arial, sans-serif; direction: rtl;'>
            <div style='flex:1; background:#1a1a1a; padding:25px; border-radius:15px; border:1px solid #444;'>
                <h4 style='color:#ff4d4d; text-align:center; margin:0 0 15px 0;'>❌ بدون تقرير</h4>
                <p style='margin:10px 0; color:#EAEAEA;'>• تسعير غير دقيق: <strong style='color:#00FFD1;'>{int(loss_wrong_pricing):,}$</strong></p>
                <p style='margin:10px 0; color:#EAEAEA;'>• توقيت خاطئ: <strong style='color:#00FFD1;'>{int(loss_bad_timing):,}$</strong></p>
                <p style='margin:10px 0; color:#EAEAEA;'>• تجاهل المخاطر: <strong style='color:#00FFD1;'>{int(loss_risk_blindness):,}$</strong></p>
                <hr style='border:1px solid #444; margin:15px 0;'>
                <p style='font-size:18px; margin:0; color:#EAEAEA;'><strong style='color:#ff4d4d;'>تكلفة القرار غير المدروس:</strong> {int(total_loss_without_report):,}$</p>
            </div>

            <div style='flex:1; background:#1a1a1a; padding:25px; border-radius:15px; border:2px solid #00FFD1;'>
                <h4 style='color:#00FFD1; text-align:center; margin:0 0 15px 0;'>✅ مع تقرير Warda</h4>
                <p style='margin:10px 0; color:#EAEAEA;'>• تقليل المخاطر: <strong style='color:#00FFD1;'>{int(risk_reduction):,}$</strong></p>
                <p style='margin:10px 0; color:#EAEAEA;'>• تحسين سعر الدخول: <strong style='color:#00FFD1;'>{int(pricing_gain):,}$</strong></p>
                <p style='margin:10px 0; color:#EAEAEA;'>• تحسين التوقيت: <strong style='color:#00FFD1;'>{int(timing_gain):,}$</strong></p>
                <hr style='border:1px solid #00FFD1; margin:15px 0;'>
                <p style='font-size:18px; margin:0; color:#EAEAEA;'><strong style='color:#00FFD1;'>ميزة القرار:</strong> {int(net_decision_advantage):,}$</p>
                <p style='font-size:13px; color:#888; margin:5px 0 0 0;'>ناتجة عن تحليل السوق + توقيت الدخول + إدارة المخاطر</p>
            </div>
        </div>
        """, height=350)

        # ===== الدليل والحسابات =====
        with st.expander("🔍 لماذا هذه الأرقام واقعية؟ (اضغط لرؤية الحسابات)"):
            st.markdown(f"""
            **مؤشرات السوق الحقيقية المستخدمة في المحاكاة:**
            
            • التحليل مبني على **{market_data['عدد_العقارات_الحقيقية']} عقار حقيقي** تم تحليله في السوق
            • فجوة سعرية فعلية في السوق: **{round(price_dispersion*100,1) if price_dispersion > 0 else 0}%** (الفرق بين أعلى وأقل سعر)
            • حجم السيولة الحالي: **{liquidity_volume}** (عدد العقارات المتاحة)
            • معدل النمو: **غير متاح (يتطلب مقارنة زمنية)**

            **كيف حسبنا الأرقام؟**
            
            • خسارة التسعير الخاطئ = قيمة الاستثمار × الفجوة السعرية × 0.6
            • خسارة التوقيت السيئ = قيمة الاستثمار × معدل النمو × 0.4 (مؤقتاً 0) 
            • خسارة تجاهل المخاطر = قيمة الاستثمار × (الحد الأدنى 15% أو 1/جذر حجم السيولة) × 0.5
            
            **لماذا هذه الطريقة؟**
            
            هذه الآلة لا تحسب الربح المتوقع،
            بل **تحسب تكلفة اتخاذ قرار أعمى مقابل قرار مدروس**.
            الأرقام تستند إلى أنماط حقيقية في السوق العقاري السعودي.
            """, unsafe_allow_html=True)

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
                    # ✅ تحميل بيانات حقيقية مباشرة من المصدر (تم إزالة snapshot)
                    real_data = load_government_data(
                        selected_city=city,
                        selected_property_type=property_type
                    )

                    if real_data is None or real_data.empty:
                        st.error("❌ لا توجد بيانات حقيقية من السوق لهذه المدينة.")
                        st.stop()

                    st.session_state.real_data = real_data
                    st.success(f"✅ تم تحميل {len(real_data)} عقار حقيقي من المصدر مباشرة")

                    market_data = generate_advanced_market_data(
                        city, property_type, status, real_data
                    )

                    user_info = {
                        "user_type": user_type,
                        "city": city,
                        "district": None,  # لا يوجد حي في تقارير المدن
                        "property_type": property_type,
                        "area": area,
                        "package": chosen_pkg,
                        "chosen_pkg": chosen_pkg,
                        "باقة": chosen_pkg,
                        "property_count": property_count,
                        "status": status
                    }
                    
                    # حفظ user_info في session_state
                    st.session_state["user_info"] = user_info
                    st.session_state["market_data"] = market_data
                    st.session_state["real_data"] = real_data

                    # 🔧 إنشاء التقرير الذكي (للعرض فقط)
                    user_category = USER_CATEGORIES.get(user_type, "investor")
                    user_data = {
                        "city": city,
                        "plan": chosen_pkg,
                        "category": user_category,
                        "user_type": user_type,
                        "user_category_ar": user_type,
                        "property_type": property_type,
                        "area": area
                    }
                    
                    smart_system = SmartReportSystem(user_data)
                    st.session_state.smart_report_content = smart_system.generate_extended_report(
                        user_info, market_data, real_data, chosen_pkg
                    )

                    if chosen_pkg in ["ذهبية", "ماسية", "ماسية متميزة"]:
                        ai_engine = AIIntelligence()
                        st.session_state.ai_recommendations = ai_engine.generate_ai_recommendations(
                            user_info, market_data, real_data
                        )

                    # ✅ نظام PDF الموحد والمضمون - الإصدار المحسن
                    try:
                        # =====================================
                        # 🧠 استخدام نظام البناء الذكي الجديد مع تمرير البيانات مباشرة
                        # =====================================
                        from report_orchestrator import build_report_story

                        # بناء التقرير الذكي مع تمرير البيانات مباشرة
                        story = build_report_story(
                            user_info,
                            provided_dataframe=real_data  # ✅ تمرير البيانات لمنع جلب بيانات مختلفة
                        )
                        
                        # 🔍 التحقق الإلزامي من محتوى التقرير
                        final_content_text = story.get("content_text", "")
                        executive_decision = story.get("executive_decision", "")

                        if not final_content_text or final_content_text.strip() == "":
                            st.error("❌ خطأ حرج: محتوى التقرير النصي فارغ.")
                            st.stop()

                        if not executive_decision or not executive_decision.strip():
                            st.error("❌ خطأ حرج: القرار التنفيذي غير موجود.")
                            st.stop()

                        st.success(f"✅ المحتوى سليم ({len(final_content_text)} حرف)")
                        st.success(f"✅ القرار التنفيذي جاهز ({len(executive_decision)} حرف)")
                        
                        charts_by_chapter = story.get("charts", {})
                        
                        # ✅ هذا السطر هو الأهم - حفظ الرسومات
                        st.session_state["charts_by_chapter"] = charts_by_chapter
                        
                        # =====================================
                        # 💎 إنشاء PDF بالمحتوى الكامل
                        # =====================================
                        pdf_buffer = create_pdf_from_content(
                            user_info=user_info,
                            content_text=final_content_text,
                            executive_decision=executive_decision,
                            charts_by_chapter=charts_by_chapter,
                            package_level=chosen_pkg
                        )
                        
                    except Exception as e:
                        st.error(f"❌ خطأ في إنشاء التقرير الكامل: {str(e)[:200]}")
                        import traceback
                        st.code(traceback.format_exc())
                        # خطة طوارئ: PDF بسيط
                        from io import BytesIO
                        buffer = BytesIO()
                        buffer.write(st.session_state.smart_report_content.encode('utf-8'))
                        buffer.seek(0)
                        pdf_buffer = buffer

                    st.session_state.pdf_data = pdf_buffer.getvalue()
                    st.session_state.report_generated = True

                    st.success("✅ تم إنشاء التقرير بنجاح!")
                    st.balloons()

                except Exception as e:
                    st.error(f"⚠️ خطأ أثناء إنشاء التقرير: {str(e)[:200]}")
                    import traceback
                    st.code(traceback.format_exc())

        # ========== عرض النتائج ==========
        if st.session_state.get('report_generated', False):
            st.markdown("---")
            st.markdown("## 📊 التقرير النهائي الجاهز للطباعة")
            
            with st.expander("📊 معاينة سريعة للتحليل", expanded=True):
                user_info = st.session_state.get('user_info', {})
                st.write("### 👤 تحليل احتياجاتك")
                st.write(f"**الفئة:** {user_info.get('user_type', 'غير محدد')}")
                st.write(f"**المدينة:** {user_info.get('city', 'غير محدد')}")
                st.write(f"**الحي:** {user_info.get('district', 'غير محدد')}")
                st.write(f"**الباقة:** {user_info.get('package', 'غير محدد')}")
                
                ai_recommendations = st.session_state.get('ai_recommendations', {})
                if ai_recommendations:
                    st.write("### 🎯 أبرز التوصيات")
                    st.write(f"**ملف المخاطر:** {ai_recommendations.get('ملف_المخاطر', 'غير محدد')}")
                    st.write(f"**استراتيجية الاستثمار:** {ai_recommendations.get('استراتيجية_الاستثمار', 'غير محدد')}")
            
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
    
    # ===== قسم تقارير الأحياء =====
    elif analysis_mode == "📍 تقارير الأحياء":
        st.markdown("## 📍 تحليل الأحياء")
        
        col1, col2 = st.columns(2)
        with col1:
            city = st.selectbox(
                "اختر المدينة",
                ["الرياض", "جدة", "مكة المكرمة", "المدينة المنورة", "الدمام"],
                key="district_city_select"
            )
        
        # ===== فلترة المدينة باستخدام contains (محسّن) =====
        city_data = df_raw[
            df_raw["city"].astype(str).str.contains(city, case=False, na=False)
        ].copy()
        
        # ===== تنظيف أسماء الأحياء بشكل قوي مع إزالة المسافات المكررة =====
        city_data["district"] = (
            city_data["district"]
            .astype(str)
            .str.lower()
            .str.replace("الحي", "", regex=False)
            .str.replace("حي", "", regex=False)
            .str.replace("حى", "", regex=False)
            .str.replace("District", "", regex=False)
            .str.split("/")
            .str[-1]
            .str.replace(r"\s+", " ", regex=True)  # إزالة المسافات المكررة
            .str.strip()
        )
        
        # ===== قائمة الأسماء غير الصالحة (مع تعديل None إلى none) =====
        invalid_names = [
            "", " ", "منطقة", "الرياض", "جدة", "مكة", "المدينة", "الدمام",
            "منطقة الرياض", "منطقة مكة المكرمة", "منطقة المدينة المنورة",
            "منطقة جدة", "منطقة الدمام", "السعودية", "غير محدد", "nan", "none"
        ]
        city_data = city_data[~city_data["district"].isin(invalid_names)]
        
        # ===== تحويل السعر إلى numeric قبل الحسابات =====
        city_data["price"] = pd.to_numeric(city_data["price"], errors="coerce")
        
        # ===== حساب الأحياء الأكثر نشاطاً =====
        district_counts = city_data.groupby("district").size()
        district_counts = district_counts[district_counts > 5]
        top_districts = district_counts.sort_values(ascending=False).head(5)
        districts = top_districts.index.tolist()
        
        if not districts:
            st.warning(f"⚠️ لا توجد أحياء نشطة للمدينة {city}")
            st.stop()
        
        with col2:
            district = st.selectbox("اختر الحي", districts, key="district_select")
        
        st.success(f"📊 تحليل حي: {district}")
        
        # ===== تحليل الحي (مع strip للمقارنة) =====
        district_data = city_data[
            city_data["district"].str.strip() == district.strip()
        ].copy()
        
        # ===== عرض مؤشرات سريعة =====
        col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
        
        with col_metrics1:
            st.metric("عدد الصفقات", len(district_data))
        
        with col_metrics2:
            avg_price = district_data["price"].mean()
            if pd.notna(avg_price):
                st.metric("متوسط السعر", f"{avg_price:,.0f} ريال")
            else:
                st.metric("متوسط السعر", "غير متوفر")
        
        with col_metrics3:
            # حساب متوسط سعر المتر باستخدام المساحات الصالحة فقط
            valid_area = district_data[district_data["area"] > 0]
            if not valid_area.empty:
                avg_price_per_sqm = (valid_area["price"] / valid_area["area"]).mean()
                st.metric("متوسط سعر المتر", f"{avg_price_per_sqm:,.0f} ريال")
            else:
                st.metric("متوسط سعر المتر", "غير متوفر")
        
        # عرض أول الصفقات - مع تحديد الأعمدة المهمة فقط
        st.write("### أول الصفقات في الحي")
        display_columns = ["price", "area", "city"]
        if "price_per_sqm" in district_data.columns:
            display_columns.append("price_per_sqm")
        st.dataframe(district_data[display_columns].head(10))
        
        # زر إنشاء تقرير الحي (مؤقت)
        if st.button("📥 إنشاء تقرير الحي", use_container_width=True):
            district_real_data = district_data.copy()
            if district_real_data.empty:
                st.error("❌ لا توجد بيانات كافية لهذا الحي")
                st.stop()
            
            # توليد بيانات السوق للحي
            market_data = generate_advanced_market_data(
                city,
                "شقة",
                "للبيع",
                district_real_data
            )
            st.success(f"✅ تم تحليل {len(district_real_data)} صفقة في الحي")

# ========== صفحة المستشار الذكي ==========
if page == "🧠 المستشار الذكي":
    st.markdown("## 🧠 مستشارك الذكي")
    
    # زر مسح المحادثة مع تأكيد
    col_chat1, col_chat2 = st.columns([3, 1])
    with col_chat2:
        if st.button("🗑️ مسح المحادثة"):
            # تأكيد قبل المسح
            st.session_state.confirm_clear = True
    
    # إذا طلب المستخدم المسح، نطلب تأكيد
    if st.session_state.get("confirm_clear", False):
        st.warning("هل أنت متأكد من مسح المحادثة؟")
        col_confirm1, col_confirm2 = st.columns(2)
        with col_confirm1:
            if st.button("✅ نعم، امسح"):
                st.session_state.robo_chat_history = []
                st.session_state.confirm_clear = False
                st.rerun()
        with col_confirm2:
            if st.button("❌ إلغاء"):
                st.session_state.confirm_clear = False
                st.rerun()
    
    with col_chat1:
        st.caption("اسأل عن السوق، الفرص، أو التوقيت — وسيجيبك حسب باقتك")

    if "robo_chat_history" not in st.session_state:
        st.session_state.robo_chat_history = []

    # عرض المحادثة
    for msg in st.session_state.robo_chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # إذا كانت المحادثة فارغة، عرض رسالة ترحيب ذكية حسب الباقة
    if not st.session_state.robo_chat_history:
        with st.chat_message("assistant"):
            current_pkg = st.session_state.get("chosen_pkg", "مجانية")
            user_info = st.session_state.get("user_info", {})
            city = user_info.get("city", "مدينتك")
            district = user_info.get("district", "حي")
            
            if current_pkg == "مجانية":
                welcome_msg = f"👋 **مرحبًا بك في المستشار الذكي**\n\nهل تحب أن أشرح لك وضع السوق العام في {city}؟"
            elif current_pkg in ["فضية", "ذهبية"]:
                welcome_msg = f"👋 **أهلاً بك**\n\nهل تريد تحليل فرص استثمارية محددة في {district} بـ {city} الآن؟"
            else:  # ماسية أو ماسية متميزة
                welcome_msg = f"👋 **تشرفنا بخدمتك**\n\nأستطيع تحليل الفرص النادرة والتوقيت المثالي للاستثمار في {district} بـ {city}. ماذا تريد أن تعرف؟"
            
            st.markdown(welcome_msg)

    # ===============================
    # 🧠 Chat Input داخل صفحة المستشار فقط
    # ===============================
    user_input = st.chat_input("اكتب سؤالك هنا...")
    
    # إضافة Hint تحت الإدخال
    st.caption("💡 مثال: وش وضع السوق في الرياض؟ أو هل الوقت مناسب للشراء؟")

    if user_input:
        # حماية من الأسئلة القصيرة جدًا
        if len(user_input.strip()) < 3:
            st.warning("✋ اكتب سؤالًا أوضح قليلًا.")
            st.stop()
        
        # التحقق من وجود معرفة الروبو
        if st.session_state.robo_knowledge is None:
            st.warning("⏳ المستشار الذكي يتم تحميله الآن، أعد المحاولة بعد لحظة.")
            st.stop()
        
        # رسالة المستخدم
        st.session_state.robo_chat_history.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.markdown(user_input)

        # إنشاء الروبو (من النظام الجديد) - استخدام user_info من session_state
        user_info = st.session_state.get("user_info", {})
        current_pkg = st.session_state.get("chosen_pkg", "مجانية")

        robo_response = handle_robo_question(
            user_profile={
                "city": user_info.get("city"),
                "district": user_info.get("district"),
                "package": current_pkg,
                "user_type": user_info.get("user_type")
            },
            knowledge=st.session_state.robo_knowledge,
            guard=RoboGuard(package=current_pkg),
            question=user_input
        )

        # رد الروبو
        st.session_state.robo_chat_history.append({
            "role": "assistant",
            "content": robo_response
        })

        with st.chat_message("assistant"):
            st.markdown(robo_response)

# ========== تهيئة حالة الجلسة ==========
if 'report_generated' not in st.session_state:
    st.session_state.report_generated = False
if 'pdf_data' not in st.session_state:
    st.session_state.pdf_data = None
if 'real_data' not in st.session_state:
    st.session_state.real_data = pd.DataFrame()
if 'market_data' not in st.session_state:
    st.session_state.market_data = {}
if 'ai_recommendations' not in st.session_state:
    st.session_state.ai_recommendations = None
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'smart_report_content' not in st.session_state:
    st.session_state.smart_report_content = None
if 'charts_by_chapter' not in st.session_state:
    st.session_state.charts_by_chapter = {}
if 'paid' not in st.session_state:
    st.session_state.paid = False
if 'robo_knowledge' not in st.session_state:
    st.session_state.robo_knowledge = None
if 'chosen_pkg' not in st.session_state:
    st.session_state.chosen_pkg = "مجانية"
if 'last_city' not in st.session_state:
    st.session_state.last_city = None
if 'last_property_type' not in st.session_state:
    st.session_state.last_property_type = None
if 'last_status' not in st.session_state:
    st.session_state.last_status = None
if 'last_chosen_pkg' not in st.session_state:
    st.session_state.last_chosen_pkg = None
if 'last_alert_refresh' not in st.session_state:
    st.session_state.last_alert_refresh = datetime.now()
if 'confirm_clear' not in st.session_state:
    st.session_state.confirm_clear = False
if 'daily_alerts' not in st.session_state:
    st.session_state.daily_alerts = []

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>© 2024 Warda Intelligence - جميع الحقوق محفوظة</p>
    <p>الذكاء الاستثماري المتقدم | شريكك الموثوق في التحليل العقاري</p>
</div>
""", unsafe_allow_html=True)
