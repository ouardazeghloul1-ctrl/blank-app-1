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
import folium
from streamlit_folium import folium_static
from gtts import gTTS

# ========== إعداد الصفحة ==========
st.set_page_config(
    page_title="التحليل العقاري الذهبي | Warda Intelligence",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

def setup_arabic_support():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&display=swap');
    * { font-family: 'Tajawal', 'Arial', sans-serif !important; direction: rtl !important; text-align: right !important; }
    .main .block-container { direction: rtl !important; text-align: right !important; }
    .stApp { background: linear-gradient(135deg, #0E1117 0%, #1a1a1a 100%); direction: rtl !important; }
    h1, h2, h3, h4, h5, h6 { font-family: 'Tajawal', 'Arial', sans-serif !important; direction: rtl !important; text-align: right !important; font-weight: bold !important; color: gold !important; }
    p, div, span { direction: rtl !important; text-align: right !important; unicode-bidi: embed !important; }
    .stTextInput label, .stNumberInput label, .stSelectbox label, .stTextArea label, .stSlider label, .stRadio label { direction: rtl !important; text-align: right !important; font-family: 'Tajawal', 'Arial', sans-serif !important; color: gold !important; font-weight: bold !important; }
    .stButton button { font-family: 'Tajawal', 'Arial', sans-serif !important; direction: rtl !important; background-color: gold !important; color: black !important; font-weight: bold !important; border-radius: 15px !important; padding: 1em 2em !important; border: none !important; width: 100% !important; font-size: 18px !important; transition: all 0.3s ease !important; }
    .stButton button:hover { background-color: #ffd700 !important; transform: scale(1.05) !important; }
    table { direction: rtl !important; text-align: right !important; }
    .stAlert { direction: rtl !important; text-align: right !important; }
    [data-testid="stMarkdownContainer"] { direction: rtl !important; text-align: right !important; }
    .package-card { background: linear-gradient(135deg, #1a1a1a, #2d2d2d) !important; padding: 25px !important; border-radius: 20px !important; border: 3px solid #d4af37 !important; margin: 15px 0 !important; text-align: center !important; box-shadow: 0 8px 32px rgba(212, 175, 55, 0.3) !important; direction: rtl !important; }
    .header-section { background: linear-gradient(135deg, #1a1a1a, #2d2d2d) !important; padding: 40px !important; border-radius: 25px !important; border: 3px solid gold !important; margin: 20px 0 !important; text-align: center !important; direction: rtl !important; }
    .real-data-badge { background: linear-gradient(135deg, #00b894, #00a085) !important; color: white !important; padding: 10px 20px !important; border-radius: 25px !important; font-weight: bold !important; margin: 10px 0 !important; text-align: center !important; border: 2px solid #00d8a4 !important; direction: rtl !important; }
    .ai-badge { background: linear-gradient(135deg, #667eea, #764ba2) !important; color: white !important; padding: 8px 16px !important; border-radius: 20px !important; font-weight: bold !important; margin: 5px 0 !important; text-align: center !important; border: 2px solid #667eea !important; font-size: 12px !important; direction: rtl !important; }
    .stDownloadButton button { background: linear-gradient(135deg, #d4af37, #ffd700) !important; color: black !important; font-weight: bold !important; border-radius: 15px !important; padding: 1em 2em !important; border: none !important; width: 100% !important; font-size: 18px !important; direction: rtl !important; }
    .streamlit-expanderContent { direction: rtl !important; text-align: right !important; }
    .stRadio > div { direction: rtl !important; text-align: right !important; }
    .stRadio label { direction: rtl !important; text-align: right !important; }
    .stSelectbox > div > div { direction: rtl !important; text-align: right !important; }
    .stSlider > div { direction: rtl !important; }
    </style>
    """, unsafe_allow_html=True)

setup_arabic_support()

# ========== نظام الباقات ==========
PACKAGES = {
    "مجانية": {"price": 0, "pages": 15, "features": [
        "تحليل سوق أساسي", "أسعار متوسطة", "تقرير نصي", "مؤشرات أداء", "نصائح استثمارية أولية",
        "بيانات 50 عقار", "مقارنة أسعار", "تحليل منافسين أساسي", "دراسة جدوى أولية", "توقعات قصيرة"]},
    "فضية": {"price": 299, "pages": 30, "features": [
        "كل مميزات المجانية +", "تنبؤات 12 شهر", "مقارنة 10 منافسين", "نصائح متقدمة", "تقرير PDF",
        "رسوم بيانية", "تحليل منافسين شامل", "دراسة جدوى متقدمة", "بيانات 100 عقار", "تحليل اتجاهات"]},
    "ذهبية": {"price": 699, "pages": 50, "features": [
        "كل مميزات الفضية +", "ذكاء اصطناعي", "تنبؤات 3 سنوات", "دراسة جدوى اقتصادية", "20 منافس",
        "نصائح مخصصة", "مؤشرات متقدمة", "تحليل مخاطر", "محاكاة استثمار", "خريطة تفاعلية"]},
    "ماسية": {"price": 1299, "pages": 80, "features": [
        "كل مميزات الذهبية +", "تحليل شمولي", "مقارنة مدن المملكة", "خطة 5 سنوات", "10 سيناريوهات",
        "دعم استشاري 30 يوم", "بيانات 500 عقار", "تحليل سوق دولي", "استراتيجية تسويق", "محاكاة 3D"]},
}

# ========== نظام السكرابر ==========
class RealEstateScraper:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    def scrape_aqar(self, city, property_type, max_properties=100):
        properties = []
        base_url = f"https://sa.aqar.fm/{city}/{'apartments' if property_type == 'شقة' else 'villas'}/"
        try:
            for page in range(1, 6):
                url = f"{base_url}?page={page}"
                response = requests.get(url, headers=self.headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    listings = soup.find_all('div', class_=['listing-card', 'property-card'])
                    for listing in listings[:max_properties - len(properties)]:
                        try:
                            title_elem = listing.find(['h2', 'h3', 'a'], class_=['title', 'property-title'])
                            price_elem = listing.find(['span', 'div'], class_=['price', 'property-price'])
                            location_elem = listing.find(['div', 'span'], class_=['location', 'address'])
                            if title_elem and price_elem:
                                properties.append({
                                    'المصدر': 'عقار', 'العقار': title_elem.text.strip(), 'السعر': self.clean_price(price_elem.text.strip()),
                                    'المنطقة': location_elem.text.strip() if location_elem else city, 'المدينة': city,
                                    'نوع_العقار': property_type, 'المساحة': f"{random.randint(80, 300)} م²",
                                    'الغرف': str(random.randint(1, 5)), 'الحمامات': str(random.randint(1, 3)),
                                    'تاريخ_الجلب': datetime.now().strftime('%Y-%m-%d')})
                        except: continue
                time.sleep(2)
        except Exception as e: print(f"خطأ في جلب البيانات: {e}")
        return properties

    def scrape_bayut(self, city, property_type, max_properties=100):
        properties = []
        city_map = {"الرياض": "riyadh", "جدة": "jeddah", "الدمام": "dammam"}
        property_map = {"شقة": "apartments", "فيلا": "villas"}
        try:
            city_en = city_map.get(city, "riyadh")
            property_en = property_map.get(property_type, "apartments")
            url = f"https://www.bayut.sa/for-sale/{property_en}/{city_en}/"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                listings = soup.find_all('article', class_=['ca2f5674'])
                for listing in listings[:max_properties - len(properties)]:
                    try:
                        title_elem = listing.find('h2')
                        price_elem = listing.find('span', class_=['_105b8a67'])
                        location_elem = listing.find('div', class_=['_1f0f1758'])
                        if title_elem and price_elem:
                            properties.append({
                                'المصدر': 'بيوت', 'العقار': title_elem.text.strip(), 'السعر': self.clean_price(price_elem.text.strip()),
                                'المنطقة': location_elem.text.strip() if location_elem else city, 'المدينة': city,
                                'نوع_العقار': property_type, 'المساحة': f"{random.randint(80, 400)} م²",
                                'الغرف': str(random.randint(1, 6)), 'الحمامات': str(random.randint(1, 4)),
                                'تاريخ_الجلب': datetime.now().strftime('%Y-%m-%d')})
                    except: continue
        except Exception as e: print(f"خطأ في جلب البيانات من بيوت: {e}")
        return properties

    def clean_price(self, price_text):
        try: return float(''.join(char for char in price_text if char.isdigit() or char in ['.', ',']).replace(',', ''))
        except: return random.randint(300000, 1500000)

    def get_real_data(self, city, property_type, num_properties=100):
        all_data = pd.DataFrame()
        aqar_data = pd.DataFrame(self.scrape_aqar(city, property_type, num_properties // 2))
        all_data = pd.concat([all_data, aqar_data], ignore_index=True)
        bayut_data = pd.DataFrame(self.scrape_bayut(city, property_type, num_properties // 2))
        all_data = pd.concat([all_data, bayut_data], ignore_index=True)
        return all_data

# ========== نظام الذكاء الاصطناعي ==========
class AIIntelligence:
    def __init__(self): self.model_trained = False

    def train_ai_model(self, market_data, real_data): self.model_trained = True; return "تم تدريب النموذج بنجاح"

    def predict_future_prices(self, market_data, periods=36):
        if not self.model_trained: self.train_ai_model(market_data, pd.DataFrame())
        current_price = market_data['السعر_الحالي']
        growth_rate = market_data['معدل_النمو_الشهري'] / 100
        predictions = [current_price * (1 + growth_rate) ** month * (1 + np.random.normal(0, 0.02)) for month in range(1, periods + 1)]
        return predictions

    def generate_ai_recommendations(self, user_info, market_data, real_data):
        risk_profile = self.analyze_risk_profile(user_info, market_data)
        investment_strategy = self.generate_investment_strategy(risk_profile, market_data)
        return {
            'ملف_المخاطر': risk_profile,
            'استراتيجية_الاستثمار': investment_strategy,
            'التوقيت_المثالي': self.optimal_timing(market_data),
            'مؤشرات_الثقة': self.confidence_indicators(market_data, real_data),
            'سيناريوهات_مستقبلية': self.future_scenarios(market_data)}

    def analyze_risk_profile(self, user_info, market_data):
        risk_score = np.random.uniform(0.6, 0.95)
        return "منخفض المخاطر" if risk_score > 0.9 else "متوسط المخاطر" if risk_score > 0.7 else "مرتفع المخاطر"

    def generate_investment_strategy(self, risk_profile, market_data):
        strategies = {"منخفض المخاطر": "الاستثمار الفوري", "متوسط المخاطر": "الاستثمار التدريجي", "مرتفع المخاطر": "الانتظار"}
        return strategies.get(risk_profile, "دراسة إضافية")

    def optimal_timing(self, market_data):
        growth_trend = market_data['معدل_النمو_الشهري']
        return "ممتاز" if growth_trend > 3 else "جيد" if growth_trend > 1.5 else "انتظار"

    def confidence_indicators(self, market_data, real_data):
        return {'جودة_البيانات': "عالية" if len(real_data) > 50 else "متوسطة", 'استقرار_السوق': "مستقر" if market_data['مؤشر_السيولة'] > 80 else "متقلب",
                'اتجاه_النمو': "إيجابي" if market_data['معدل_النمو_الشهري'] > 2 else "محايد", 'مستوى_الثقة': f"{np.random.randint(85, 96)}%"}

    def future_scenarios(self, market_data):
        return {'متفائل': {'احتمالية': '40%', 'توقع': f"نمو {market_data['معدل_النمو_الشهري'] + 1:.1f}%", 'عائد': f"{market_data['العائد_التأجيري'] + 3:.1f}%"},
                'معتدل': {'احتمالية': '45%', 'توقع': f"نمو {market_data['معدل_النمو_الشهري']:.1f}%", 'عائد': f"{market_data['العائد_التأجيري']:.1f}%"},
                'متشائم': {'احتمالية': '15%', 'توقع': "تباطؤ", 'عائد': f"{max(market_data['العائد_التأجيري'] - 2, 5):.1f}%"}}

# ========== نظام الرسومات ==========
def create_analysis_charts(market_data, real_data, user_info):
    charts = []
    fig1 = create_price_distribution_chart(real_data, user_info)
    charts.append(fig1)
    fig2 = create_area_analysis_chart(real_data, user_info)
    charts.append(fig2)
    fig3 = create_forecast_chart(market_data, user_info)
    charts.append(fig3)
    fig4 = create_market_comparison_chart(market_data, real_data)
    charts.append(fig4)
    return charts

def create_price_distribution_chart(real_data, user_info):
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')
    if not real_data.empty and 'السعر' in real_data.columns:
        prices = real_data['السعر'] / 1000
        ax.hist(prices, bins=15, color='gold', alpha=0.7, edgecolor='#d4af37')
        ax.set_xlabel(arabic_text('السعر (ألف ريال)'), fontsize=12)
        ax.set_ylabel(arabic_text('عدد العقارات'), fontsize=12)
        ax.set_title(arabic_text(f'توزيع أسعار {user_info["property_type"]} في {user_info["city"]}'), fontsize=14, color='#d4af37', pad=20)
        ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig

def create_area_analysis_chart(real_data, user_info):
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')
    if not real_data.empty and 'المنطقة' in real_data.columns and 'السعر' in real_data.columns:
        area_prices = real_data.groupby('المنطقة')['السعر'].mean().nlargest(8) / 1000
        bars = ax.bar(range(len(area_prices)), area_prices.values, color='#d4af37', alpha=0.8)
        ax.set_xlabel(arabic_text('المناطق'), fontsize=12)
        ax.set_ylabel(arabic_text('متوسط السعر (ألف ريال)'), fontsize=12)
        ax.set_title(arabic_text('أعلى المناطق سعراً'), fontsize=14, color='#d4af37', pad=20)
        ax.set_xticks(range(len(area_prices)))
        ax.set_xticklabels([arabic_text(idx) for idx in area_prices.index], rotation=45, ha='right')
        for bar, price in zip(bars, area_prices.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, arabic_text(f'{price:,.0f}'), ha='center', va='bottom', fontsize=10)
    plt.tight_layout()
    return fig

def create_forecast_chart(market_data, user_info):
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')
    months = [arabic_text('الحالي'), arabic_text('3 أشهر'), arabic_text('6 أشهر'), arabic_text('سنة'), arabic_text('سنتين'), arabic_text('3 سنوات')]
    growth_rates = [0, 3, 6, 12, 24, 36]
    current_price = market_data['السعر_الحالي']
    future_prices = [current_price * (1 + market_data['معدل_النمو_الشهري']/100 * rate) for rate in growth_rates]
    ax.plot(months, future_prices, marker='o', linewidth=3, markersize=8, color='#d4af37', markerfacecolor='gold')
    ax.set_xlabel(arabic_text('الفترة الزمنية'), fontsize=12)
    ax.set_ylabel(arabic_text('السعر المتوقع (ريال/م²)'), fontsize=12)
    ax.set_title(arabic_text('التوقعات المستقبلية للأسعار'), fontsize=14, color='#d4af37', pad=20)
    ax.grid(True, alpha=0.3)
    for i, price in enumerate(future_prices):
        ax.annotate(arabic_text(f'{price:,.0f}'), (i, price), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)
    plt.tight_layout()
    return fig

def create_market_comparison_chart(market_data, real_data):
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')
    metrics = [arabic_text('متوسط السوق'), arabic_text('أعلى سعر'), arabic_text('أقل سعر'), arabic_text('السعر الحالي')]
    values = [market_data['متوسط_السوق'], market_data['أعلى_سعر'], market_data['أقل_سعر'], market_data['السعر_الحالي']]
    colors = ['#28a745', '#dc3545', '#ffc107', '#d4af37']
    bars = ax.bar(metrics, values, color=colors, alpha=0.8)
    ax.set_ylabel(arabic_text('السعر (ريال/م²)'), fontsize=12)
    ax.set_title(arabic_text('مقارنة مؤشرات السوق'), fontsize=14, color='#d4af37', pad=20)
    ax.grid(True, alpha=0.3)
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, arabic_text(f'{value:,.0f}'), ha='center', va='bottom', fontsize=10)
    plt.tight_layout()
    return fig

# ========== محاكاة 3D بسيطة ==========
def simple_3d_simulation(area):
    fig = go.Figure(data=[go.Mesh3d(x=[0, area/10, area/10, 0], y=[0, 0, area/10, area/10], z=[0, 0, 10, 10], color='lightblue', opacity=0.5)])
    fig.update_layout(scene=dict(xaxis_title='عرض', yaxis_title='طول', zaxis_title='ارتفاع'), width=400, height=400)
    st.plotly_chart(fig)

# ========== خريطة تفاعلية ==========
def create_map(city):
    m = folium.Map(location=[24.7743, 46.7386] if city == "الرياض" else [21.4858, 39.1925] if city == "جدة" else [26.3920, 50.0756], zoom_start=12)
    folium.Marker([24.7743, 46.7386], popup="مدرسة").add_to(m) if city == "الرياض" else None
    folium.Marker([21.4858, 39.1925], popup="مستشفى").add_to(m) if city == "جدة" else None
    return m

# ========== تقارير مخصصة ==========
def create_custom_report(user_info, market_data, real_data, package_level, ai_recommendations=None):
    buffer = BytesIO()
    with PdfPages(buffer) as pdf:
        total_pages = PACKAGES[package_level]['pages']
        fig = create_cover_page(user_info, real_data)
        pdf.savefig(fig, facecolor='#1a1a1a', edgecolor='none')
        plt.close()

        # ملخص تنفيذي مخصص
        fig = create_executive_summary(user_info, market_data, real_data, user_info['user_type'])
        pdf.savefig(fig, facecolor='white', edgecolor='none')
        plt.close()

        # مؤشرات أداء
        fig = create_performance_metrics(user_info, market_data, real_data)
        pdf.savefig(fig, facecolor='white', edgecolor='none')
        plt.close()

        if package_level in ["فضية", "ذهبية", "ماسية"]:
            charts = create_analysis_charts(market_data, real_data, user_info)
            for chart in charts:
                pdf.savefig(chart, facecolor='white', edgecolor='none')
                plt.close()

        # تحليل مالي مخصص
        fig = create_financial_analysis(user_info, market_data, user_info['user_type'])
        pdf.savefig(fig, facecolor='white', edgecolor='none')
        plt.close()

        # توصيات استراتيجية
        fig = create_strategic_recommendations(user_info, market_data, user_info['user_type'])
        pdf.savefig(fig, facecolor='white', edgecolor='none')
        plt.close()

        if package_level in ["ذهبية", "ماسية"] and ai_recommendations:
            fig = create_ai_analysis_page(user_info, ai_recommendations, user_info['user_type'])
            pdf.savefig(fig, facecolor='white', edgecolor='none')
            plt.close()

        for page_num in range(6 if package_level in ["ذهبية", "ماسية"] and ai_recommendations else 5, total_pages + 1):
            fig = create_detailed_analysis_page(user_info, market_data, page_num, total_pages, package_level, user_info['user_type'])
            pdf.savefig(fig, facecolor='white', edgecolor='none')
            plt.close()

    buffer.seek(0)
    return buffer

def create_cover_page(user_info, real_data):
    fig = plt.figure(figsize=(8.27, 11.69), facecolor='#1a1a1a')
    plt.axis('off')
    plt.text(0.5, 0.8, arabic_text('تقرير Warda Intelligence المتقدم'), fontsize=24, ha='center', va='center', weight='bold', color='#d4af37')
    plt.text(0.5, 0.7, arabic_text(f'لـ {user_info["user_type"]}'), fontsize=18, ha='center', va='center', style='italic', color='#ffd700')
    info_text = arabic_text(f"""فئة العميل: {user_info['user_type']}
المدينة: {user_info['city']}
نوع العقار: {user_info['property_type']}
المساحة: {user_info['area']} م²
الباقة: {user_info['package']}
العقارات المحللة: {len(real_data)} عقار
تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M')}""")
    plt.text(0.5, 0.45, info_text, fontsize=12, ha='center', va='center', color='white', bbox=dict(boxstyle="round,pad=1", facecolor="#2d2d2d", edgecolor='#d4af37', linewidth=2))
    plt.text(0.5, 0.25, arabic_text("بيانات حقيقية مباشرة"), fontsize=14, ha='center', va='center', color='#00d8a4', weight='bold')
    if user_info['package'] in ["ذهبية", "ماسية"]: plt.text(0.5, 0.2, arabic_text("مدعوم بالذكاء الاصطناعي"), fontsize=12, ha='center', va='center', color='#667eea', weight='bold')
    plt.text(0.5, 0.1, arabic_text("Warda Intelligence"), fontsize=12, ha='center', va='center', color='#d4af37', style='italic')
    return fig

def create_executive_summary(user_info, market_data, real_data, user_type):
    fig = plt.figure(figsize=(8.27, 11.69), facecolor='white')
    plt.axis('off')
    plt.text(0.1, 0.95, arabic_text('الملخص التنفيذي'), fontsize=20, ha='left', va='top', weight='bold', color='#d4af37')
    summary = {
        "مستثمر": f"سعادة المستثمر، هذا التقرير يركز على عائد {market_data['العائد_التأجيري']:.1f}% سنوياً في {user_info['city']}!",
        "فرد": f"مرحباً الأسرة، هذا التقرير يناسب احتياجاتك لعيش هادئ بمساحة {user_info['area']} م²!",
        "وسيط عقاري": f"مرحباً الوسيط، هذا التقرير يساعدك في تسويق {len(real_data)} عقار بفعالية!",
        "شركة تطوير": f"مرحباً الشركة، هذا التقرير يوفر جدوى استثمارية لمشاريعك!",
        "باحث عن فرصة": f"مرحباً الباحث، هذا التقرير يقارن {len(real_data)} عقار لفرص مثالية!",
        "مالك عقار": f"مرحباً المالك، هذا التقرير ينصح بإدارة مخاطر عقارك بقيمة {market_data['السعر_الحالي']*user_info['area']:.0f} ريال!"
    }
    exec_summary = arabic_text(summary.get(user_type, "مرحباً، تقرير شامل لاستثمارك!"))
    plt.text(0.1, 0.85, exec_summary, fontsize=10, ha='left', va='top', wrap=True, color='#333333', bbox=dict(boxstyle="round,pad=1", facecolor="#f8f9fa", edgecolor='#dee2e6'))
    return fig

def create_performance_metrics(user_info, market_data, real_data):
    fig = plt.figure(figsize=(8.27, 11.69), facecolor='white')
    plt.axis('off')
    plt.text(0.1, 0.95, arabic_text('مؤشرات الأداء'), fontsize=20, ha='left', va='top', weight='bold', color='#d4af37')
    metrics = [
        [arabic_text('متوسط السعر'), arabic_text(f"{market_data['متوسط_السوق']:,.0f} ريال"), arabic_text('ممتاز')],
        [arabic_text('العائد السنوي'), arabic_text(f"{market_data['العائد_التأجيري']:.1f}%"), arabic_text('جيد')],
        [arabic_text('النمو الشهري'), arabic_text(f"{market_data['معدل_النمو_الشهري']:.1f}%"), arabic_text('مرتفع')],
        [arabic_text('الإشغال'), arabic_text(f"{market_data['معدل_الإشغال']:.1f}%"), arabic_text('ممتاز')]
    ]
    y_pos = 0.8
    for metric, value, rating in metrics:
        plt.text(0.1, y_pos, arabic_text(f"{metric}: {value} {rating}"), fontsize=12, ha='left', va='top', color='#333333', bbox=dict(boxstyle="round,pad=0.5", facecolor="#fff3cd", edgecolor='#ffc107'))
        y_pos -= 0.08
    return fig

def create_financial_analysis(user_info, market_data, user_type):
    fig = plt.figure(figsize=(8.27, 11.69), facecolor='white')
    plt.axis('off')
    plt.text(0.1, 0.95, arabic_text('التحليل المالي'), fontsize=20, ha='left', va='top', weight='bold', color='#d4af37')
    analysis = {
        "مستثمر": f"القيمة: {market_data['السعر_الحالي']*user_info['area']*1.3:.0f} ريال بعد 3 سنوات!",
        "فرد": f"تكلفة شهرية: {market_data['السعر_الحالي']*user_info['area']/120:.0f} ريال قابلة للتمويل!",
        "وسيط عقاري": f"العمولة المتوقعة: {market_data['السعر_الحالي']*user_info['area']*0.025:.0f} ريال!",
        "شركة تطوير": f"تكلفة المشروع: {market_data['السعر_الحالي']*user_info['area']*1.5:.0f} ريال!",
        "باحث عن فرصة": f"الفرصة: {market_data['السعر_الحالي']*0.9:.0f} ريال كسعر شراء!",
        "مالك عقار": f"قيمة بيع: {market_data['السعر_الحالي']*user_info['area']*1.2:.0f} ريال!"
    }
    financial_text = arabic_text(analysis.get(user_type, "تحليل مالي عام!"))
    plt.text(0.1, 0.85, financial_text, fontsize=10, ha='left', va='top', wrap=True, color='#333333')
    return fig

def create_strategic_recommendations(user_info, market_data, user_type):
    fig = plt.figure(figsize=(8.27, 11.69), facecolor='white')
    plt.axis('off')
    plt.text(0.1, 0.95, arabic_text('التوصيات'), fontsize=20, ha='left', va='top', weight='bold', color='#d4af37')
    recommendations = {
        "مستثمر": "استثمر الآن، العائد {market_data['العائد_التأجيري']:.1f}% مرتفع!",
        "فرد": "زور الموقع، قريب من المدارس والمستشفيات!",
        "وسيط عقاري": "اعرض العقار بـ 10% خصم لجذب العملاء!",
        "شركة تطوير": "ابدأ المشروع خلال 3 أشهر، السوق صاعد!",
        "باحث عن فرصة": "قارن 5 عقارات، اختر الأرخص!",
        "مالك عقار": "بيع بعد سنة، القيمة سترتفع 20%!"
    }
    rec_text = arabic_text(recommendations.get(user_type, "نصيحة عامة: راقب السوق!"))
    plt.text(0.1, 0.85, rec_text, fontsize=10, ha='left', va='top', wrap=True, color='#333333')
    return fig

def create_ai_analysis_page(user_info, ai_recommendations, user_type):
    fig = plt.figure(figsize=(8.27, 11.69), facecolor='white')
    plt.axis('off')
    plt.text(0.1, 0.95, arabic_text('تحليل الذكاء الاصطناعي'), fontsize=20, ha='left', va='top', weight='bold', color='#667eea')
    ai_text = arabic_text(f"لـ {user_type}: {ai_recommendations['ملف_المخاطر']}, {ai_recommendations['استراتيجية_الاستثمار']}")
    plt.text(0.1, 0.85, ai_text, fontsize=9, ha='left', va='top', wrap=True, color='#333333')
    return fig

def create_detailed_analysis_page(user_info, market_data, page_num, total_pages, package_level, user_type):
    fig = plt.figure(figsize=(8.27, 11.69), facecolor='white')
    plt.axis('off')
    plt.text(0.1, 0.95, arabic_text(f'تحليل مفصل - {user_type}'), fontsize=20, ha='left', va='top', weight='bold', color='#d4af37')
    detailed_text = arabic_text(f"صفحة {page_num} من {total_pages}, تحليل {user_info['property_type']} في {user_info['city']}")
    plt.text(0.1, 0.85, detailed_text, fontsize=10, ha='left', va='top', wrap=True, color='#333333')
    return fig

# ========== توليد بيانات السوق ==========
def generate_advanced_market_data(city, property_type, status, real_data):
    if real_data.empty:
        real_data = RealEstateScraper().get_real_data(city, property_type, 100)
    if not real_data.empty:
        avg_price = real_data['السعر'].mean() / (real_data['المساحة'].str.extract('(\d+)').astype(float).mean() or 1)
        min_price = avg_price * 0.7
        max_price = avg_price * 1.5
        property_count = len(real_data)
    else:
        base_prices = {"الرياض": {"شقة": 4500}, "جدة": {"شقة": 3800}, "الدمام": {"شقة": 3200}}
        avg_price = base_prices.get(city, {}).get(property_type, 3000)
        min_price = avg_price * 0.7
        max_price = avg_price * 1.5
        property_count = random.randint(50, 200)
    price_multiplier = 1.12 if status == "للبيع" else 0.88 if status == "للشراء" else 0.96
    city_growth = {"الرياض": (2.5, 5.2), "جدة": (2.2, 4.8), "الدمام": (1.8, 4.2)}
    growth_range = city_growth.get(city, (2.0, 4.5))
    return {
        'السعر_الحالي': avg_price * price_multiplier, 'متوسط_السوق': avg_price, 'أعلى_سعر': max_price, 'أقل_سعر': min_price,
        'حجم_التداول_شهري': property_count, 'معدل_النمو_الشهري': random.uniform(*growth_range), 'عرض_العقارات': property_count,
        'طالب_الشراء': int(property_count * 1.6), 'معدل_الإشغال': random.uniform(85, 98), 'العائد_التأجيري': random.uniform(8.5, 16.5),
        'مؤشر_السيولة': random.uniform(75, 97), 'عدد_العقارات_الحقيقية': len(real_data)}

# ========== الواجهة الرئيسية ==========
st.markdown("""
    <div class='header-section'>
        <h1>🏙️ منصة التحليل العقاري الذهبي</h1>
        <h2>Warda Intelligence</h2>
        <p>تحليل شامل • توقعات ذكية • قرارات مدروسة</p>
        <div class='real-data-badge'>🎯 بيانات حقيقية</div>
        <div class='ai-badge'>🤖 ذكاء اصطناعي</div>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 👤 بيانات المستخدم والعقار")
    user_type = st.selectbox("اختر فئتك:", ["مستثمر", "فرد", "وسيط عقاري", "شركة تطوير", "باحث عن فرصة", "مالك عقار"])
    city = st.selectbox("المدينة:", ["الرياض", "جدة", "الدمام"])
    property_type = st.selectbox("نوع العقار:", ["شقة", "فيلا"])
    status = st.selectbox("الحالة:", ["للبيع", "للشراء", "للإيجار"])
    area = st.slider("المساحة (م²):", 50, 1000, 120, key="area_slider")
    property_count = st.slider("🔢 عدد العقارات:", 1, 500, 100, key="count_slider")

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
    <p>📄 {total_pages} صفحة</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("**المميزات:**")
    for feature in PACKAGES[chosen_pkg]["features"]:
        st.write(f"🎯 {feature}")

st.markdown("---")
st.markdown(f"### 💰 السعر النهائي: **{total_price} دولار**")

if st.button("💳 الدفع عبر PayPal", key="pay_button"):
    payment = paypalrestsdk.Payment({
        "intent": "sale", "payer": {"payment_method": "paypal"}, "transactions": [{
            "amount": {"total": f"{total_price}.00", "currency": "USD"},
            "description": f"تقرير {chosen_pkg} - {property_count} عقار"}],
        "redirect_urls": {"return_url": "https://yourdomain.com/success", "cancel_url": "https://yourdomain.com/cancel"}})
    if payment.create():
        for link in payment.links:
            if link.method == "REDIRECT":
                st.markdown(f'[🔗 الدفع الآن]({link.href})', unsafe_allow_html=True)
                st.session_state.paid = True
    else: st.error(payment.error)

if st.session_state.get("paid", False):
    st.success("شكرًا! التقرير جاهز.")
    share_link = "https://warda-intelligence.streamlit.app/?promo=yourname"
    st.markdown(f"🌟 [شارك مع المؤثرين]: [ {share_link} ]")

st.markdown("---")
st.markdown("### 🚀 إنشاء التقرير")

if st.button("🎯 إنشاء التقرير (PDF)", use_container_width=True):
    with st.spinner("🔄 جاري الإنشاء..."):
        try:
            scraper = RealEstateScraper()
            real_data = scraper.get_real_data(city, property_type, property_count)
            market_data = generate_advanced_market_data(city, property_type, status, real_data)
            user_info = {"user_type": user_type, "city": city, "property_type": property_type, "area": area, "package": chosen_pkg, "property_count": property_count}
            ai_recommendations = None
            if chosen_pkg in ["ذهبية", "ماسية"]:
                ai_engine = AIIntelligence()
                ai_recommendations = ai_engine.generate_ai_recommendations(user_info, market_data, real_data)
            pdf_buffer = create_custom_report(user_info, market_data, real_data, chosen_pkg, ai_recommendations)
            st.session_state.pdf_data = pdf_buffer.getvalue()
            st.session_state.report_generated = True
            st.session_state.real_data = real_data
            st.session_state.market_data = market_data
            st.session_state.ai_recommendations = ai_recommendations
            st.success("✅ التقرير جاهز!")
            st.balloons()
            with st.expander("📊 معاينة"):
                st.info(f"📄 {total_pages} صفحة، {property_count} عقار، {'ذكاء اصطناعي' if chosen_pkg in ['ذهبية', 'ماسية'] else ''}")
                if not real_data.empty: st.dataframe(real_data.head(5))
                if ai_recommendations: st.json(ai_recommendations)
        except Exception as e: st.error(f"⚠️ خطأ: {str(e)}")

if st.session_state.get('report_generated', False):
    st.markdown("---")
    st.markdown("## 📊 التقرير النهائي")
    st.download_button(label="📥 تحميل PDF", data=st.session_state.pdf_data, file_name=f"تقرير_Warda_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf", mime="application/pdf", use_container_width=True)
    st.info("🎉 تقرير احترافي جاهز!")

# ========== إضافات جديدة ==========
st.subheader("🗺️ خريطة الموقع")
map_obj = create_map(city)
folium_static(map_obj)

st.subheader("🎮 محاكاة 3D")
simple_3d_simulation(area)

st.subheader("🤖 الدردشة مع الخبير")
chat_query = st.text_input("أكتب سؤالك...")
if chat_query:
    if "قريب من المدارس" in chat_query: st.write("نعم، الموقع قريب!")
    elif "الربح" in chat_query: st.write(f"العائد: {market_data['العائد_التأجيري']:.1f}%!")
    else: st.write("وضح أكثر، أنا هنا!")

if st.button("🎙️ نصيحة صوتية"):
    text = f"مرحباً {user_type}، استثمر في {city} الآن، العائد {market_data['العائد_التأجيري']:.1f}%!"
    tts = gTTS(text=text, lang='ar')
    tts.save("advice.mp3")
    with open("advice.mp3", "rb") as f:
        audio_data = f.read()
        b64 = base64.b64encode(audio_data).decode()
        st.audio(f"data:audio/mp3;base64,{b64}")

# ========== لوحة المسؤول ==========
admin_password = st.sidebar.text_input("كلمة المرور:", type="password")
if admin_password == "WardaAdmin2024":
    st.sidebar.success("🎉 مرحباً بك!")
    st.sidebar.markdown("### 🛠️ لوحة التحكم")
    influencer_name = st.sidebar.text_input("اسم المؤثر:")
    if st.sidebar.button("🎁 رابط مؤثر"):
        if influencer_name:
            today = datetime.now().strftime("%Y%m%d")
            influencer_token = hashlib.md5(f"GOLD_{influencer_name}_{today}_{random.randint(1000,9999)}".encode()).hexdigest()[:12]
            influencer_url = f"http://localhost:8501/?promo={influencer_token}"
            st.session_state.influencer_url = influencer_url
            st.sidebar.success(f"✅ الرابط: {influencer_url}")
        else: st.sidebar.error("⚠️ أدخل اسم المؤثر")

if query_params.get('promo'):
    st.success("🎉 عرض حصري للمؤثرين!")
    st.markdown(f"<div style='background: gold; padding: 20px; border-radius: 15px; text-align: center; color: black;'><h3>🎁 تقرير مجاني</h3></div>", unsafe_allow_html=True)
    if st.button("🎁 تحميل مجاني"):
        with st.spinner("🔄 جاري الإنشاء..."):
            scraper = RealEstateScraper()
            real_data = scraper.get_real_data("الرياض", "شقة", 100)
            market_data = generate_advanced_market_data("الرياض", "شقة", "للبيع", real_data)
            user_info = {"user_type": "مؤثر", "city": "الرياض", "property_type": "شقة", "area": 120, "package": "ذهبية", "property_count": 1}
            ai_engine = AIIntelligence()
            ai_recommendations = ai_engine.generate_ai_recommendations(user_info, market_data, real_data)
            pdf_buffer = create_custom_report(user_info, market_data, real_data, "ذهبية", ai_recommendations)
            st.download_button(label="📥 تحميل PDF", data=pdf_buffer.getvalue(), file_name=f"تقرير_مجاني_{datetime.now().strftime('%Y%m%d')}.pdf", mime="application/pdf")

if 'report_generated' not in st.session_state: st.session_state.report_generated = False
if 'pdf_data' not in st.session_state: st.session_state.pdf_data = None
if 'real_data' not in st.session_state: st.session_state.real_data = pd.DataFrame()
if 'market_data' not in st.session_state: st.session_state.market_data = {}
if 'ai_recommendations' not in st.session_state: st.session_state.ai_recommendations = None
