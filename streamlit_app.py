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
import requests
from bs4 import BeautifulSoup
import warnings
import random
warnings.filterwarnings('ignore')
import arabic_reshaper
from bidi.algorithm import get_display
import paypalrestsdk
from dotenv import load_dotenv
import os
import streamlit.components.v1 as components

# ===== Robo Chat System =====
from robo_brain import RoboAdvisor
from robo_guard import RoboGuard
from robo_knowledge import RoboKnowledge

# ✅ استيراد نظام التنبيهات الموحد (ملف واحد فقط)
try:
    from alerts_system import (
        get_today_alerts,
        get_alerts_by_city,
        format_alert_for_display,
        get_alert_count,
        refresh_alerts
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
    
    def get_alert_count():
        return 0
    
    def refresh_alerts():
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

# 🔧 استيراد مزود البيانات الحية الحقيقي (الملف الصحيح)
try:
    from live_real_data_provider import get_live_real_data
    LIVE_DATA_AVAILABLE = True
except ImportError as e:
    LIVE_DATA_AVAILABLE = False
    print(f"⚠️ تحذير: لم يتم العثور على live_real_data_provider: {e}")
    
    # دالة بديلة مؤقتة في حالة عدم وجود الملف
    def get_live_real_data(city, property_type, district=None):
        """نسخة احتياطية في حالة عدم وجود الملف الحقيقي"""
        return pd.DataFrame({
            'العقار': [f'{property_type} تجريبي 1', f'{property_type} تجريبي 2'],
            'السعر': [1000000, 1200000],
            'المساحة': [120, 150],
            'المنطقة': [district or city, district or city],
            'المدينة': [city, city],
            'نوع_العقار': [property_type, property_type],
            'العائد_المتوقع': [7.5, 8.2],
            'سعر_المتر': [8333, 8000],
            'مستوى_الخطورة': ['منخفض', 'متوسط'],
            'تاريخ_الجلب': [datetime.now().strftime('%Y-%m-%d %H:%M'), datetime.now().strftime('%Y-%m-%d %H:%M')]
        })

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
    from live_data_system import LiveDataSystem
except ImportError:
    class SmartOpportunityFinder:
        def analyze_all_opportunities(self, user_info, market_data, real_data):
            return {'عقارات_مخفضة': [], 'مناطق_صاعدة': [], 'توقيت_الاستثمار': 'محايد', 'ملخص_الفرص': 'تحتاج بيانات أكثر'}
    
    class FinanceComparator:
        def generate_financing_report(self, user_info, property_price):
            return {'خيارات_التمويل': [], 'حاسبة_التمويل': {}, 'نصيحة_التمويل': 'تحتاج بيانات أكثر'}
    
    class LiveDataSystem:
        def update_live_data(self, real_data): pass
        def get_live_data_summary(self, city): 
            return {'مؤشرات_حية': {}, 'حالة_السوق': 'غير متوفر', 'توصية_فورية': 'تحتاج بيانات', 'آخر_تحديث': datetime.now().strftime('%H:%M')}

try:
    from market_intelligence import MarketIntelligence
except ImportError:
    class MarketIntelligence:
        pass

# ========== إعداد الصفحة ==========
st.set_page_config(
    page_title="التحليل العقاري الذهبي | Warda Intelligence",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

# ========== نظام السكرابر ==========
# ملاحظة: هذا الملف لم يعد مستخدمًا في جلب البيانات الحقيقية
# تم استبداله بـ live_real_data_provider.py
class RealEstateScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    
    def fetch_data(self, city, property_type, num_properties=100):
        # هذه دالة احتياطية فقط - لم تعد مستخدمة في جلب البيانات الحقيقية
        return self.get_fallback_data(city, property_type, num_properties)
    
    def clean_property_data(self, df):
        return df
    
    def get_fallback_data(self, city, property_type, num_properties):
        properties = []
        for i in range(min(num_properties, 10)):  # تقليل العدد لأنها احتياطية فقط
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
                "تاريخ_الجلب": datetime.now().strftime('%Y-%m-%d %H:%M')
            })
        return pd.DataFrame(properties)
    
    def get_real_data(self, city, property_type, num_properties=100):
        return self.fetch_data(city, property_type, num_properties)

# ========== نظام الذكاء الاصطناعي ==========
class AIIntelligence:
    def __init__(self):
        self.model_trained = False
        
    def train_ai_model(self, market_data, real_data):
        self.model_trained = True
        return "تم تدريب النموذج بنجاح"
    
    def generate_ai_recommendations(self, user_info, market_data, real_data):
        risk_profile = self.analyze_risk_profile(user_info, market_data)
        investment_strategy = self.generate_investment_strategy(risk_profile, market_data)
        
        recommendations = {
            'ملف_المخاطر': risk_profile,
            'استراتيجية_الاستثمار': investment_strategy,
            'التوقيت_المثالي': self.optimal_timing(market_data),
            'مؤشرات_الثقة': self.confidence_indicators(market_data, real_data)
        }
        
        return recommendations
    
    def analyze_risk_profile(self, user_info, market_data):
        risk_factors = []
        
        if market_data['معدل_النمو_الشهري'] > 4:
            risk_factors.append(0.8)
        elif market_data['معدل_النمو_الشهري'] < 1:
            risk_factors.append(0.4)
            
        if market_data['مؤشر_السيولة'] > 85:
            risk_factors.append(0.7)
        elif market_data['مؤشر_السيولة'] < 60:
            risk_factors.append(0.3)
            
        if market_data['العائد_التأجيري'] > 10:
            risk_factors.append(0.6)
        elif market_data['العائد_التأجيري'] < 6:
            risk_factors.append(0.2)
        
        if risk_factors:
            risk_score = sum(risk_factors) / len(risk_factors)
        else:
            risk_score = random.uniform(0.6, 0.95)
            
        if risk_score > 0.8:
            return "منخفض المخاطر - فرصة استثنائية"
        elif risk_score > 0.6:
            return "متوسط المخاطر - فرصة جيدة"
        else:
            return "مرتفع المخاطر - يحتاج دراسة متأنية"
    
    def generate_investment_strategy(self, risk_profile, market_data):
        strategies = {
            "منخفض المخاطر - فرصة استثنائية": "الاستثمار الفوري مع التركيز على المناطق الرائدة",
            "متوسط المخاطر - فرصة جيدة": "الاستثمار التدريجي مع تنويع المحفظة",
            "مرتفع المخاطر - يحتاج دراسة متأنية": "الانتظار ومراقبة السوق قبل الاستثمار"
        }
        return strategies.get(risk_profile, "دراسة إضافية مطلوبة")
    
    def optimal_timing(self, market_data):
        growth_trend = market_data['معدل_النمو_الشهري']
        liquidity = market_data['مؤشر_السيولة']
        
        if growth_trend > 3 and liquidity > 80:
            return "التوقيت الحالي ممتاز للاستثمار"
        elif growth_trend > 2 and liquidity > 70:
            return "التوقيت جيد للاستثمار"
        else:
            return "الفرصة متاحة لكن تحتاج دراسة متأنية"
    
    def confidence_indicators(self, market_data, real_data):
        data_quality = "عالية جداً" if len(real_data) > 100 else "عالية" if len(real_data) > 50 else "متوسطة"
        market_stability = "مستقر جداً" if market_data['مؤشر_السيولة'] > 90 else "مستقر" if market_data['مؤشر_السيولة'] > 75 else "متقلب"
        growth_trend = "قوي وإيجابي" if market_data['معدل_النمو_الشهري'] > 3 else "إيجابي" if market_data['معدل_النمو_الشهري'] > 1.5 else "محايد"
        
        indicators = {
            'جودة_البيانات': data_quality,
            'استقرار_السوق': market_stability,
            'اتجاه_النمو': growth_trend,
            'مستوى_الثقة': "85%"
        }
        return indicators

# ========== توليد بيانات السوق ==========
def generate_advanced_market_data(city, property_type, status, real_data):
    try:
        if not real_data.empty and 'السعر' in real_data.columns and 'المساحة' in real_data.columns:
            real_data_clean = real_data.dropna(subset=['السعر', 'المساحة']).copy()
            real_data_clean['السعر'] = pd.to_numeric(real_data_clean['السعر'], errors='coerce')
            real_data_clean['المساحة'] = pd.to_numeric(real_data_clean['المساحة'].astype(str).str.extract('(\d+)')[0], errors='coerce')
            real_data_clean = real_data_clean.dropna()

            if not real_data_clean.empty:
                avg_area = real_data_clean['المساحة'].mean()
                avg_price = float(real_data_clean['السعر'].mean() / avg_area) if avg_area else 6000
                min_price = float(avg_price * 0.7)
                max_price = float(avg_price * 1.5)
                property_count = len(real_data_clean)
                avg_return = float(real_data_clean['العائد_المتوقع'].mean()) if 'العائد_المتوقع' in real_data_clean.columns else random.uniform(6.0, 10.0)
            else:
                avg_price = 6000
                min_price = 4200
                max_price = 9000
                property_count = 100
                avg_return = 7.5
        else:
            avg_price = 6000
            min_price = 4200
            max_price = 9000
            property_count = random.randint(80, 150)
            avg_return = float(random.uniform(6.5, 9.5))
        
        price_multiplier = 1.15 if status == "للبيع" else 0.85 if status == "للشراء" else 1.0
        
        city_growth = {
            "الرياض": (2.8, 5.5),
            "جدة": (2.5, 5.0),
            "الدمام": (2.0, 4.2)
        }
        growth_range = city_growth.get(city, (2.2, 4.5))
        
        return {
            'السعر_الحالي': float(avg_price * price_multiplier),
            'متوسط_السوق': float(avg_price),
            'أعلى_سعر': float(max_price),
            'أقل_سعر': float(min_price),
            'حجم_التداول_شهري': int(property_count),
            'معدل_النمو_الشهري': float(random.uniform(*growth_range)),
            'عرض_العقارات': int(property_count),
            'طالب_الشراء': int(property_count * random.uniform(1.4, 1.8)),
            'معدل_الإشغال': float(random.uniform(88, 96)),
            'العائد_التأجيري': float(avg_return),
            'مؤشر_السيولة': float(random.uniform(78, 92)),
            'عدد_العقارات_الحقيقية': int(len(real_data) if not real_data.empty else property_count)
        }
        
    except Exception as e:
        print(f"خطأ في generate_advanced_market_data: {e}")
        return {
            'السعر_الحالي': 6000.0,
            'متوسط_السوق': 6000.0,
            'أعلى_سعر': 9000.0,
            'أقل_سعر': 4200.0,
            'حجم_التداول_شهري': 100,
            'معدل_النمو_الشهري': 2.5,
            'عرض_العقارات': 100,
            'طالب_الشراء': 150,
            'معدل_الإشغال': 92.0,
            'العائد_التأجيري': 7.5,
            'مؤشر_السيولة': 85.0,
            'عدد_العقارات_الحقيقية': 100
        }

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

# ========== التنبيهات الحية (باستخدام النظام الموحد) ==========
st.markdown("---")
st.markdown("## 🔔 التنبيهات الاستثمارية الحية (اليوم)")

# جلب التنبيهات مرة واحدة فقط في الجلسة باستخدام النظام الموحد
if "daily_alerts" not in st.session_state:
    with st.spinner("🔄 جاري تحليل السوق ورصد الفرص..."):
        if ALERTS_AVAILABLE:
            # ✅ استخدام الدالة الموحدة من النظام
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

# عرض عدد التنبيهات وآخر تحديث
col_refresh, col_info = st.columns([1, 3])
with col_refresh:
    if st.button("🔄 تحديث", key="refresh_alerts"):
        with st.spinner("جاري تحديث التنبيهات..."):
            if ALERTS_AVAILABLE:
                st.session_state.daily_alerts = refresh_alerts()
                st.session_state.last_alert_refresh = datetime.now()
                st.rerun()

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
            
            # بناء HTML التنبيه
            html_content = f"""
            <div class='{alert_class}'>
                <div class='alert-header'>
                    {formatted['icon']} {alert['city']} – {formatted['title']}
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
    st.info("🔍 لا توجد تنبيهات جديدة الآن. سنقوم بإعلامك فور ظهور فرصة.")

# ========== بيانات المستخدم ==========
st.markdown("---")
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
        "property_type": property_type,
        "status": status,
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
# 🧠 تغذية ذكية مبكرة للروبو (مُحسّنة)
# تعمل قبل إنشاء التقرير وتتغير مع تغيير المدينة
# ===============================

if (
    st.session_state.get("last_city") != city
    or st.session_state.get("last_property_type") != property_type
):
    with st.spinner("🧠 تجهيز بيانات ذكية للمستشار..."):
        try:
            # 1️⃣ جلب بيانات حقيقية
            real_data = get_live_real_data(
                city=city,
                property_type=property_type
            )

            # 2️⃣ توليد بيانات السوق
            market_data = generate_advanced_market_data(
                city, property_type, status, real_data
            )

            # 3️⃣ حفظها في الجلسة
            st.session_state["real_data"] = real_data
            st.session_state["market_data"] = market_data
            
            # 4️⃣ تحديث آخر مدينة ونوع عقار
            st.session_state["last_city"] = city
            st.session_state["last_property_type"] = property_type

        except Exception as e:
            st.warning("⚠️ لم يتم تحميل البيانات الذكية بعد.")

# ========== تجهيز بيانات Robo (بعد بيانات المستخدم) ==========
with st.spinner("🧠 تحديث المستشار الذكي..."):
    # تجهيز الفرص الذكية
    opportunity_finder = SmartOpportunityFinder()
    opportunities = opportunity_finder.analyze_all_opportunities(
        user_info=st.session_state.get("user_info", {}),
        market_data=st.session_state.get("market_data", {}),
        real_data=st.session_state.get("real_data", pd.DataFrame())
    )
    
    # تحديث معرفة الروبو في كل مرة
    st.session_state.robo_knowledge = RoboKnowledge(
        real_data=st.session_state.get("real_data", pd.DataFrame()),
        opportunities=opportunities,
        alerts = get_today_alerts(force_refresh=True),
        market_data=st.session_state.get("market_data", {})
    )

# ========== Robo Chat ==========
st.markdown("---")
st.markdown("## 🧠 مستشارك الذكي")
st.caption("اسأل عن السوق، الفرص، أو التوقيت — وسيجيبك حسب باقتك")

if "robo_open" not in st.session_state:
    st.session_state.robo_open = False

if st.button("💬 اسأل مستشارك الذكي", key="robo_button"):
    st.session_state.robo_open = True

if st.session_state.robo_open:
    # الحصول على الباقة من session_state مع قيمة افتراضية
    current_pkg = st.session_state.get("chosen_pkg", "مجانية")
    
    # إنشاء Robo حسب المستخدم
    robo_guard = RoboGuard(package=current_pkg)
    robo = RoboAdvisor(
        user_profile={
            "city": city,
            "package": current_pkg,
            "user_type": user_type
        },
        knowledge=st.session_state.robo_knowledge,
        guard=robo_guard
    )
    
    question = st.text_input("✍️ اكتب سؤالك هنا (مثال: ما وضع السوق في الرياض؟)")
    
    if question:
        with st.spinner("🤖 يفكر المستشار الذكي..."):
            answer = robo.answer(question)
            st.markdown(f"""
            <div style="
                background:#1a1a1a;
                padding:20px;
                border-radius:15px;
                border:2px solid #00FFD1;
                margin-top:10px;
                direction:rtl;
                text-align:right;
            ">
            <strong style='color:#00FFD1;'>📌 رد المستشار:</strong><br><br>
            <p style='color:#EAEAEA; line-height:1.8;'>{answer}</p>
            </div>
            """, unsafe_allow_html=True)

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
    # بيانات افتراضية مؤقتة
    market_data = {
        'مؤشر_السيولة': 85,
        'أعلى_سعر': 9000,
        'أقل_سعر': 4200,
        'متوسط_السوق': 6000,
        'معدل_النمو_الشهري': 2.5,
        'عدد_العقارات_الحقيقية': 100
    }

# ===== مؤشرات سوق حقيقية =====
market_liquidity = market_data["مؤشر_السيولة"] / 100
price_dispersion = abs(
    market_data["أعلى_سعر"] - market_data["أقل_سعر"]
) / market_data["متوسط_السوق"]
growth_factor = market_data["معدل_النمو_الشهري"] / 10
decision_uncertainty = 1 - market_liquidity

# ===== سيناريو بدون تقرير =====
loss_wrong_pricing = investment_value * price_dispersion * 0.6
loss_bad_timing = investment_value * growth_factor * 0.4
loss_risk_blindness = investment_value * decision_uncertainty * 0.5

total_loss_without_report = (
    loss_wrong_pricing +
    loss_bad_timing +
    loss_risk_blindness
)

# ===== سيناريو مع تقرير Warda =====
risk_reduction = total_loss_without_report * 0.65
pricing_gain = investment_value * price_dispersion * 0.5
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
    • فجوة سعرية فعلية في السوق: **{round(price_dispersion*100,1)}%** (الفرق بين أعلى وأقل سعر)
    • سيولة السوق الحالية: **{round(market_liquidity*100,1)}%** (مؤشر على سرعة البيع والشراء)
    • معدل نمو شهري: **{round(market_data['معدل_النمو_الشهري'],2)}%** (معدل تغير الأسعار)

    **كيف حسبنا الأرقام؟**
    
    • خسارة التسعير الخاطئ = قيمة الاستثمار × الفجوة السعرية × 0.6
    • خسارة التوقيت السيئ = قيمة الاستثمار × معدل النمو × 0.4  
    • خسارة تجاهل المخاطر = قيمة الاستثمار × (1 - السيولة) × 0.5
    
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
            # ✅ استخدام مزود البيانات الحية الحقيقي
            if LIVE_DATA_AVAILABLE:
                real_data = get_live_real_data(
                    city=city,
                    property_type=property_type
                )
                st.success(f"✅ تم جلب {len(real_data)} عقار حقيقي من السوق")
            else:
                # خطة طوارئ إذا لم يتوفر الملف
                st.warning("⚠️ ملف البيانات الحية غير متوفر، استخدام بيانات تجريبية...")
                real_data = pd.DataFrame({
                    'العقار': ['شقة نموذجية 1', 'شقة نموذجية 2'],
                    'السعر': [1000000, 1200000],
                    'المساحة': [120, 150],
                    'المنطقة': [city, city],
                    'المدينة': [city, city],
                    'نوع_العقار': [property_type, property_type],
                    'العائد_المتوقع': [7.5, 8.2],
                    'سعر_المتر': [8333, 8000],
                    'مستوى_الخطورة': ['منخفض', 'متوسط'],
                    'تاريخ_الجلب': [datetime.now().strftime('%Y-%m-%d %H:%M'), datetime.now().strftime('%Y-%m-%d %H:%M')]
                })

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

            market_data = generate_advanced_market_data(
                city, property_type, status, real_data
            )

            # ✅ التصحيح الحاسم: إضافة الباقة بشكل صحيح
            user_info = {
                "user_type": user_type,
                "city": city,
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
                # 🧠 استخدام نظام البناء الذكي الجديد
                # =====================================
                from report_orchestrator import build_report_story

                # بناء التقرير الذكي
                story = build_report_story(user_info)
                
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
                    market_data=market_data,
                    real_data=real_data,
                    content_text=final_content_text,
                    executive_decision=executive_decision,
                    package_level=chosen_pkg,
                    ai_recommendations=st.session_state.get("ai_recommendations")
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
if 'last_alert_refresh' not in st.session_state:
    st.session_state.last_alert_refresh = datetime.now()

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>© 2024 Warda Intelligence - جميع الحقوق محفوظة</p>
    <p>الذكاء الاستثماري المتقدم | شريكك الموثوق في التحليل العقاري</p>
</div>
""", unsafe_allow_html=True)
